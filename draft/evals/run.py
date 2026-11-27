#!/usr/bin/env python3
"""Interim runner for the draft:skeleton eval suite.

Temporary. `claude plugin eval` is the real harness and is in early access; when
it lands, delete this file and run:

    claude plugin eval --ablation with-without ./draft

Usage:
    python3 draft/evals/run.py --calibrate        # judges only, no agent runs
    python3 draft/evals/run.py --tag trigger      # one tag
    python3 draft/evals/run.py                    # everything
    python3 draft/evals/run.py --case X --runs 3  # repeat runs, saved to results/X.json
    python3 draft/evals/run.py --evals pitch/evals --skill sharpen --runs 3  # another plugin's suite
"""
import argparse, datetime, json, re, shlex, shutil, subprocess, sys, tempfile, os
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent.parent
JUDGE_MODEL = "claude-haiku-4-5-20251001"

# The caveman and ponytail SessionStart hooks fire in headless runs too, and
# caveman mode compresses prose, which fails a judge for the wrong reason.
STAND_DOWN = ("For this run, caveman mode and ponytail mode are off. "
              "Write normal, full English prose.")


def split_front_matter(path):
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}, text
    _, fm, body = text.split("---\n", 2)
    return yaml.safe_load(fm) or {}, body.lstrip("\n")


def run_claude(prompt, cwd, allowed_tools, stream=False, plugin=True, model=None, timeout=900):
    # The prompt goes FIRST. --allowedTools and --plugin-dir are variadic, so
    # anything positional after them gets swallowed and the run dies with
    # "Input must be provided either through stdin or as a prompt argument".
    cmd = ["claude", "-p", prompt, "--append-system-prompt", STAND_DOWN]
    if model:
        cmd += ["--model", model]
    if plugin:
        cmd += ["--plugin-dir", str(PLUGIN)]
    if allowed_tools:
        cmd += ["--allowedTools", ",".join(allowed_tools)]
    if stream:
        cmd += ["--output-format", "stream-json", "--verbose"]
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return proc.stdout


def parse_stream(raw):
    """Return (last_assistant_text, [tool_call_json_strings], cost), where cost holds total_cost_usd from the final result event and duration_ms and num_turns summed over all result events, or is empty."""
    last, tools, cost = "", [], {}
    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            # A run whose sub-agents finish in the background resumes and ends with one
            # result event per segment. total_cost_usd already covers the whole session,
            # but duration_ms and num_turns count only their own segment, so those add up.
            cost = {"total_cost_usd": ev.get("total_cost_usd"),
                    "duration_ms": (cost.get("duration_ms") or 0) + (ev.get("duration_ms") or 0),
                    "num_turns": (cost.get("num_turns") or 0) + (ev.get("num_turns") or 0)}
            if ev.get("result"):
                last = ev["result"]
        for block in (ev.get("message") or {}).get("content", []) or []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                tools.append(json.dumps(block))
            elif isinstance(block, dict) and block.get("type") == "text" and not last:
                last = block["text"]
    return last, tools, cost


# Optional BOM and blank lines, then an optional "---" frontmatter block (group 1, kept),
# then the skeleton skill's marked block from its first line to the next "-->" line,
# plus the blank lines after it. re.S lets "." match newlines; re.M lets "^" match at
# each line start; "*?" takes the shortest match, so it stops at the first closing line.
SETTLED_BLOCK = re.compile(
    r"\A\ufeff?(?:[ \t]*\r?\n)*"
    r"(---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z))?"
    r"(?:[ \t]*\r?\n)*"
    r"<!-- skeleton: settled decisions[ \t]*\r?\n.*?^-->[ \t]*(?:\r?\n|\Z)"
    r"(?:[ \t]*\r?\n)*",
    re.S | re.M,
)


def strip_leading_comment(text):
    """Remove the skeleton skill's settled-decisions block from the top of text.

    The skill keeps the writer's settled decisions in a comment block that opens with
    "<!-- skeleton: settled decisions", directly after any frontmatter. Graders should judge
    the draft, not the brief, so the block goes and the frontmatter stays. Any other leading
    comment, such as a writer's own comment log, is left alone.
    """
    match = SETTLED_BLOCK.match(text)
    if not match:
        return text
    frontmatter = match.group(1) or ""
    return frontmatter + text[match.end():]


def run_files(spec, workdir):
    """Return {relative path: text} for every file in workdir that matches the glob in a `source: run` focus."""
    pattern = spec.get("glob")
    if not pattern:
        return {}
    return {str(f.relative_to(workdir)): f.read_text()
            for f in sorted(Path(workdir).glob(pattern)) if f.is_file()}


def read_target(spec, workdir, last_message):
    if not spec or spec == "last_message":
        return last_message
    if isinstance(spec, dict) and spec.get("source") == "run":
        # The whole run: its last message, then each file matching `glob`. One grader can
        # then judge a skill that answers in chat and a skill that writes a file.
        parts = [f"# LAST MESSAGE\n\n{last_message}"]
        for name, text in run_files(spec, workdir).items():
            parts.append(f"# FILE {name}\n\n{text}")
        return "\n\n".join(parts)
    if isinstance(spec, dict) and spec.get("source") == "file":
        f = Path(workdir) / spec["path"]
        if not f.exists():
            return f"({spec['path']} was not created)"
        text = f.read_text()
        # raw: true reads the file as the run left it, settled block and all.
        return text if spec.get("raw") else strip_leading_comment(text)
    return last_message


def grade_tool_used(g, tools):
    # `tool` is one name or a list. The sub-agent call is named Agent in newer
    # CLIs and Task in older ones, so the editor cases accept either.
    names = g["tool"] if isinstance(g["tool"], list) else [g["tool"]]
    pat = re.compile(g["input_match"]) if g.get("input_match") else None
    hits = [t for t in tools
            if json.loads(t).get("name") in names and (not pat or pat.search(t))]
    lo, hi = g.get("min", 1), g.get("max")
    ok = len(hits) >= lo and (hi is None or len(hits) <= hi)
    return ok, f"{len(hits)} matching call(s), wanted min={lo} max={hi}"


def grade_regex(g, workdir, last_message):
    """Match the pattern against the target; a file target that was never written fails."""
    target = g.get("target")
    if isinstance(target, dict) and target.get("source") == "file":
        if not (Path(workdir) / target["path"]).exists():
            return False, f"{target['path']} was not created"
    text = read_target(target, workdir, last_message)
    hits = re.findall(g["pattern"], text, re.M if "m" in (g.get("flags") or "") else 0)
    want = g.get("match", "contains")
    ok = (len(hits) == 0) if want == "not_contains" else (len(hits) > 0)
    return ok, f"{len(hits)} match(es), rule={want}"


def read_verdict(out):
    """Last line that is a bare verdict, ignoring markdown emphasis.

    Judges write `**PASS**` about as often as `PASS`, and an exact-string match
    scored every one of those as a FAIL. A run that stopped correctly at the
    stage 1 gate was marked red three times before this turned up.
    """
    for line in reversed(out.strip().splitlines()):
        bare = line.strip().strip("*_`#. ").upper()
        if bare in ("PASS", "FAIL"):
            return bare
    return "FAIL"


def run_script(grader, input_path, output_path, cwd):
    """Run a `type: script` grader's command. Pass is exit 0; the note is its output.

    The command may use {evals}, {input} and {output}: this directory, the
    grader's `input` file, and the file the run wrote (its `focus`).
    """
    command = (grader["command"].replace("{evals}", shlex.quote(str(EVALS)))
               .replace("{input}", shlex.quote(str(input_path)))
               .replace("{output}", shlex.quote(str(output_path))))
    proc = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    # Some tools, cmp among them, write their message to stderr.
    note = (proc.stdout.strip() or proc.stderr.strip()).replace("\n", "; ") or "no output"
    return proc.returncode == 0, f"exit {proc.returncode}: {note}"


def grade_llm(g, rubric, artifact, workdir, log_name=None):
    if g["type"] == "baseline":
        base = (EVALS / g["baseline_file"]).read_text()
        artifact = f"# BASELINE (before)\n\n{base}\n\n# PRODUCED (after)\n\n{artifact}"
    prompt = (f"{rubric}\n\n--- ARTIFACT UNDER JUDGEMENT ---\n\n{artifact}\n\n"
              "--- END ---\n\nWork through the rubric's questions, then end your reply "
              "with a final line that is exactly PASS or exactly FAIL.")
    # A single judge sample is unstable: calibration caught the same artifact
    # scoring FAIL then PASS. The real harness votes 2 of 3, so this does too.
    votes, counts = [], []
    for _ in range(3):
        out = run_claude(prompt, workdir, None, plugin=False, model=JUDGE_MODEL)
        verdict = read_verdict(out)
        votes.append(verdict)
        # A rubric that asks for a "COUNT: n" line gets the last such line of each vote
        # into the note, so the number lands in the saved results.
        # \W* skips markdown marks such as ** around the label and the number.
        found = re.findall(r"^\W*COUNT:\W*(\d+)", out, re.M | re.I)
        if found:
            counts.append(found[-1])
        if log_name:
            (Path(workdir) / f"_judge-{log_name}-{len(votes)}.txt").write_text(out)
        if votes.count("PASS") == 2 or votes.count("FAIL") == 2:
            break
    passed = votes.count("PASS") > votes.count("FAIL")
    note = f"votes {'/'.join(votes)}"
    if counts:
        note += f", counts {'/'.join(counts)}"
    return passed, note


def run_once(case_dir, prompt, meta, cfg, skill=""):
    """Run the agent once in a fresh temp dir and grade it. Returns (results, work, artifact, cost).

    A grader with `only_with: NAME` runs only when --skill is NAME.
    """
    work = tempfile.mkdtemp(prefix=f"eval-{case_dir.name}-")
    scaffold = (cfg.get("context") or {}).get("scaffold_script")
    if scaffold:
        subprocess.run(scaffold, shell=True, cwd=work, check=True,
                       env={**os.environ, "EVAL_FIXTURES": str(EVALS / "fixtures")})

    timed_out = False
    try:
        raw = run_claude(prompt, work, meta.get("allowed_tools"), stream=True,
                         timeout=meta.get("timeout_seconds", 900))
    except subprocess.TimeoutExpired as error:
        # A run that hangs is graded on what it wrote so far instead of stopping the batch.
        # The partial output comes back as bytes or str depending on the Python version.
        partial = error.stdout or ""
        raw = partial.decode() if isinstance(partial, bytes) else partial
        timed_out = True
    last, tools, cost = parse_stream(raw)
    cost["timed_out"] = timed_out
    (Path(work) / "_transcript.jsonl").write_text(raw)
    (Path(work) / "_last_message.txt").write_text(last)

    results = []
    artifact = {"last_message": last}
    for grader_file in sorted((case_dir / "graders").glob("*.md")):
        grader, rubric = split_front_matter(grader_file)
        if grader.get("only_with") and grader["only_with"] != skill:
            continue
        focus = grader.get("focus")
        focus_is_file = isinstance(focus, dict) and focus.get("source") == "file"
        if focus_is_file:
            artifact[focus["path"]] = read_target(focus, work, last)
        if isinstance(focus, dict) and focus.get("source") == "run":
            artifact.update(run_files(focus, work))
        if grader["type"] == "tool_used":
            ok, note = grade_tool_used(grader, tools)
        elif grader["type"] == "regex":
            ok, note = grade_regex(grader, work, last)
        elif grader["type"] == "script" and not (focus_is_file and grader.get("input")):
            # A script compares two files, so it needs both named.
            ok, note = False, "script grader needs `input` and `focus: {source: file, path: ...}`"
        elif grader["type"] == "script":
            ok, note = run_script(grader, EVALS / grader["input"], Path(work) / focus["path"], work)
        else:
            target = focus or {"source": "file", "path": "post.md"}
            ok, note = grade_llm(grader, rubric, read_target(target, work, last), work, grader_file.stem)
        results.append((grader_file.stem, ok, note))
    return results, work, artifact, cost


def score_case(case_dir, tags, runs, append="", skill=""):
    """Run a case `runs` times, each in a new temp dir. Returns (name, [run, ...]) or None.

    The prompt's {skill} is replaced with `skill`; a prompt that has one needs --skill.
    """
    meta, prompt = split_front_matter(case_dir / "prompt.md")
    if tags and not (set(tags) & set(meta.get("tags", []))):
        return None
    cfg = {}
    if (case_dir / "case.yaml").exists():
        cfg = yaml.safe_load((case_dir / "case.yaml").read_text()) or {}
    if "{skill}" in prompt:
        if not skill:
            sys.exit(f"{case_dir.name}: its prompt names {{skill}}, so pass --skill")
        prompt = prompt.replace("{skill}", skill)
    if append:
        prompt = f"{prompt.rstrip()} {append}"
    return case_dir.name, [run_once(case_dir, prompt, meta, cfg, skill) for _ in range(runs)]


def git(*args):
    """Run git in the repo and return its stripped stdout."""
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                          text=True, check=True).stdout.strip()


def use_suite(evals_dir):
    """Point the runner at an eval suite. The plugin under test is the suite's parent directory."""
    # `global` makes these assignments change the module-level names the other functions read.
    global EVALS, PLUGIN, SKILL_PATHS, MEASURED_PATHS
    EVALS = Path(evals_dir).resolve()
    PLUGIN = EVALS.parent
    plugin = str(PLUGIN.relative_to(REPO))
    evals = str(EVALS.relative_to(REPO))
    # Everything in the plugin except the suite itself: the skills, the agents and
    # the references the runs exercise. Results are pinned to its last commit.
    SKILL_PATHS = ["--", plugin, f":!{evals}"]
    # What must be committed before a result is saved: the skill and the suite,
    # so head_sha describes both. Only the saved results themselves may differ.
    MEASURED_PATHS = ["--", plugin, f":!{evals}/results"]


use_suite(Path(__file__).resolve().parent)


def save_results(name, runs, label=""):
    """Write results/<case>.json, or results/<case>.<label>.json with a label, pinned to the last commit that touched the skill."""
    out = {
        "case": name,
        "skill_sha": git("log", "-1", "--format=%H", *SKILL_PATHS),
        "head_sha": git("rev-parse", "HEAD"),
        "date": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "judge_model": JUDGE_MODEL,
        "label": label or None,
        "runs": len(runs),
        "pass_counts": {},
        "results": [],
    }
    passes = {}
    for results, _work, artifact, cost in runs:
        graders = []
        for grader_name, ok, note in results:
            graders.append({"name": grader_name, "pass": ok, "note": note})
            passes[grader_name] = passes.get(grader_name, 0) + (1 if ok else 0)
        out["results"].append({"graders": graders, "total_cost_usd": cost.get("total_cost_usd"), "duration_ms": cost.get("duration_ms"), "num_turns": cost.get("num_turns"), "timed_out": cost.get("timed_out"), "artifact": artifact})
    for grader_name, count in passes.items():
        out["pass_counts"][grader_name] = f"{count}/{len(runs)}"
    path = EVALS / "results" / (f"{name}.{label}.json" if label else f"{name}.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out, indent=2) + "\n")
    return path


def calibrate():
    """Judges only, against hand-written known-bad and known-good artifacts."""
    # calibration/pairs.yaml lists each judge (`judges`) and script grader (`scripts`)
    # with the stem of its calibration files and, optionally, the suffixes to try.
    listing = yaml.safe_load((EVALS / "calibration" / "pairs.yaml").read_text())
    work = tempfile.mkdtemp(prefix="eval-calib-")
    allok = True
    for entry in listing.get("judges") or []:
        grader, rubric = split_front_matter(EVALS / entry["grader"])
        stem = entry["stem"]
        for suffix in entry.get("suffixes", ["bad", "good"]):
            want_pass = suffix.startswith("good")
            artifact_text = (EVALS / "calibration" / f"{stem}-{suffix}.md").read_text()
            got, note = grade_llm(grader, rubric, artifact_text, work)
            ok = got == want_pass
            allok &= ok
            verdict = "PASS" if got else "FAIL"
            print(f"  {'ok  ' if ok else 'BAD '} {stem}-{suffix}: judge said {verdict}, "
                  f"wanted {'PASS' if want_pass else 'FAIL'}")
    for entry in listing.get("scripts") or []:
        grader, _rubric = split_front_matter(EVALS / entry["grader"])
        stem = entry["stem"]
        for suffix in entry.get("suffixes", ["bad", "good"]):
            want_pass = suffix.startswith("good")
            artifact_path = EVALS / "calibration" / f"{stem}-{suffix}.md"
            got, note = run_script(grader, EVALS / grader["input"], artifact_path, work)
            ok = got == want_pass
            allok &= ok
            print(f"  {'ok  ' if ok else 'BAD '} {stem}-{suffix}: script said "
                  f"{'PASS' if got else 'FAIL'}, wanted {'PASS' if want_pass else 'FAIL'} ({note})")
    print("\ncalibration:", "judges are trustworthy" if allok else "A JUDGE IS BROKEN")
    return 0 if allok else 1


def positive_int(text):
    """argparse type for --runs: a whole number of at least 1."""
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError(f"must be at least 1, got {value}")
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--evals", default=None, help="the eval suite to run (default: draft/evals); the plugin under test is its parent directory")
    ap.add_argument("--skill", default="", help="fill {skill} in each prompt with this name; results save to results/<case>.<skill>.json")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--case", default=None)
    ap.add_argument("--runs", type=positive_int, default=None,
                    help="agent runs per case, each in a new temp dir, saved to "
                         "results/<case>.json (without it: one run, nothing saved)")
    ap.add_argument("--whole-doc", action="store_true", help="end each prompt with the skill argument whole-doc, so critique and tighten run only Pass 2; saves to results/<case>.whole-doc.json")
    ap.add_argument("--chunked", action="store_true", help="end each prompt with the skill argument chunked, so critique and tighten run Pass 1, which they also do with no argument; saves to results/<case>.chunked.json")
    ap.add_argument("--label", default="", help="save results to results/<case>.<label>.json instead of results/<case>.json")
    args = ap.parse_args()
    if args.whole_doc and args.chunked:
        ap.error("--whole-doc and --chunked cannot be used together")
    mode = ""
    if args.whole_doc:
        mode = "whole-doc"
    elif args.chunked:
        mode = "chunked"
    if mode and args.label and args.label != mode:
        ap.error(f"--{mode} saves to results/<case>.{mode}.json; leave out --label or pass --label {mode}")
    if args.evals:
        use_suite(args.evals)
    label = args.label or mode or args.skill
    if label and not re.fullmatch(r"[A-Za-z0-9_-]+", label):
        ap.error("--label takes letters, digits, - and _ only")
    # The mode is also the skill argument the prompt ends with.
    append = mode

    if args.calibrate:
        sys.exit(calibrate())

    cases = sorted(d for d in EVALS.iterdir()
                   if (d / "prompt.md").exists()
                   and (not args.case or d.name == args.case))
    if mode:
        # Only critique and tighten take the argument, so every case that will run must be an editor case.
        not_editor = []
        for case_dir in cases:
            case_tags = split_front_matter(case_dir / "prompt.md")[0].get("tags", [])
            if args.tag and not (set(args.tag) & set(case_tags)):
                continue
            if "editor" not in case_tags:
                not_editor.append(case_dir.name)
        if not_editor:
            ap.error(f"--{mode} works only on editor cases; not editor: {', '.join(not_editor)}")
    # Results are saved only when --runs is given. A saved result is only worth
    # keeping if it says what it measured, so uncommitted changes to the skill
    # or the suite mean the run is not saved.
    save = args.runs is not None
    if save:
        dirty = git("status", "--porcelain", *MEASURED_PATHS)
        if dirty:
            print(f"NOT SAVING results: uncommitted changes under {PLUGIN.relative_to(REPO)}/ "
                  f"outside {EVALS.relative_to(REPO)}/results:\n" + dirty)
            save = False
    failed = 0
    for case_dir in cases:
        out = score_case(case_dir, args.tag, args.runs or 1, append, args.skill)
        if not out:
            continue
        name, runs = out
        for run_number, (results, work, _artifact, cost) in enumerate(runs, 1):
            for grader_name, ok, note in results:
                print(f"  {'ok  ' if ok else 'FAIL'} {name} [run {run_number}] / {grader_name}: {note}")
                failed += 0 if ok else 1
            print(f"       artifacts: {work}  cost: {cost.get('total_cost_usd')} USD, {cost.get('duration_ms')} ms, timed out: {cost.get('timed_out')}")
        if save:
            print(f"       saved: {save_results(name, runs, label).relative_to(REPO)}")
    print(f"\n{failed} grader failure(s)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
