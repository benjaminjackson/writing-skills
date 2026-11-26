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
"""
import argparse, datetime, json, re, shlex, shutil, subprocess, sys, tempfile, os
from pathlib import Path

import yaml

EVALS = Path(__file__).resolve().parent
PLUGIN = EVALS.parent
REPO = PLUGIN.parent
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


def run_claude(prompt, cwd, allowed_tools, stream=False, plugin=True, model=None):
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
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=900)
    return proc.stdout


def parse_stream(raw):
    """Return (last_assistant_text, [tool_call_json_strings])."""
    last, tools = "", []
    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result" and ev.get("result"):
            last = ev["result"]
        for block in (ev.get("message") or {}).get("content", []) or []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                tools.append(json.dumps(block))
            elif isinstance(block, dict) and block.get("type") == "text" and not last:
                last = block["text"]
    return last, tools


def read_target(spec, workdir, last_message):
    if not spec or spec == "last_message":
        return last_message
    if isinstance(spec, dict) and spec.get("source") == "file":
        f = Path(workdir) / spec["path"]
        return f.read_text() if f.exists() else f"({spec['path']} was not created)"
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


def grade_regex(g, text):
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


def run_script(g, input_path, output_path, cwd):
    """Run a `type: script` grader's command. Pass is exit 0; the note is stdout.

    The command may use {evals}, {input} and {output}: this directory, the
    grader's `input` file, and the file the run wrote (its `focus`).
    """
    command = (g["command"].replace("{evals}", shlex.quote(str(EVALS)))
               .replace("{input}", shlex.quote(str(input_path)))
               .replace("{output}", shlex.quote(str(output_path))))
    proc = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    note = proc.stdout.strip().replace("\n", "; ") or "no output"
    return proc.returncode == 0, f"exit {proc.returncode}: {note}"


def grade_llm(g, rubric, artifact, workdir, log_name=None):
    if g["type"] == "baseline":
        base = (REPO / "draft" / "evals" / g["baseline_file"]).read_text()
        artifact = f"# BASELINE (before)\n\n{base}\n\n# PRODUCED (after)\n\n{artifact}"
    prompt = (f"{rubric}\n\n--- ARTIFACT UNDER JUDGEMENT ---\n\n{artifact}\n\n"
              "--- END ---\n\nWork through the rubric's questions, then end your reply "
              "with a final line that is exactly PASS or exactly FAIL.")
    # A single judge sample is unstable: calibration caught the same artifact
    # scoring FAIL then PASS. The real harness votes 2 of 3, so this does too.
    votes = []
    for _ in range(3):
        out = run_claude(prompt, workdir, None, plugin=False, model=JUDGE_MODEL)
        verdict = read_verdict(out)
        votes.append(verdict)
        if log_name:
            (Path(workdir) / f"_judge-{log_name}-{len(votes)}.txt").write_text(out)
        if votes.count("PASS") == 2 or votes.count("FAIL") == 2:
            break
    passed = votes.count("PASS") > votes.count("FAIL")
    return passed, f"votes {'/'.join(votes)}"


def run_once(case_dir, prompt, meta, cfg):
    """Run the agent once in a fresh temp dir and grade it. Returns (results, work, artifact)."""
    work = tempfile.mkdtemp(prefix=f"eval-{case_dir.name}-")
    scaffold = (cfg.get("context") or {}).get("scaffold_script")
    if scaffold:
        subprocess.run(scaffold, shell=True, cwd=work, check=True,
                       env={**os.environ, "EVAL_FIXTURES": str(EVALS / "fixtures")})

    raw = run_claude(prompt, work, meta.get("allowed_tools"), stream=True)
    last, tools = parse_stream(raw)
    (Path(work) / "_transcript.jsonl").write_text(raw)
    (Path(work) / "_last_message.txt").write_text(last)

    results = []
    artifact = {"last_message": last}
    for gf in sorted((case_dir / "graders").glob("*.md")):
        g, rubric = split_front_matter(gf)
        focus = g.get("focus")
        if isinstance(focus, dict) and focus.get("source") == "file":
            artifact[focus["path"]] = read_target(focus, work, last)
        if g["type"] == "tool_used":
            ok, note = grade_tool_used(g, tools)
        elif g["type"] == "regex":
            ok, note = grade_regex(g, read_target(g.get("target"), work, last))
        elif g["type"] == "script":
            ok, note = run_script(g, EVALS / g["input"], Path(work) / focus["path"], work)
        else:
            target = focus or {"source": "file", "path": "post.md"}
            ok, note = grade_llm(g, rubric, read_target(target, work, last), work, gf.stem)
        results.append((gf.stem, ok, note))
    return results, work, artifact


def score_case(case_dir, tags, runs):
    """Run a case `runs` times, each in a new temp dir. Returns (name, [run, ...]) or None."""
    meta, prompt = split_front_matter(case_dir / "prompt.md")
    if tags and not (set(tags) & set(meta.get("tags", []))):
        return None
    cfg = {}
    if (case_dir / "case.yaml").exists():
        cfg = yaml.safe_load((case_dir / "case.yaml").read_text()) or {}
    return case_dir.name, [run_once(case_dir, prompt, meta, cfg) for _ in range(runs)]


def git(*args):
    """Run git in the repo and return its stripped stdout."""
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                          text=True, check=True).stdout.strip()


# Everything under draft/ except the suite itself: the skills, the agent and
# the references the runs exercise. Results are pinned to its last commit.
SKILL_PATHS = ["--", "draft", ":!draft/evals"]


def save_results(name, runs):
    """Write results/<case>.json, pinned to the last commit that touched the skill."""
    out = {
        "case": name,
        "skill_sha": git("log", "-1", "--format=%H", *SKILL_PATHS),
        "head_sha": git("rev-parse", "HEAD"),
        "date": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "judge_model": JUDGE_MODEL,
        "runs": len(runs),
        "pass_counts": {},
        "results": [],
    }
    for results, _work, artifact in runs:
        out["results"].append({
            "graders": [{"name": g, "pass": ok, "note": note} for g, ok, note in results],
            "artifact": artifact,
        })
    for gname in [g for g, _ok, _note in runs[0][0]]:
        passes = sum(1 for results, _w, _a in runs for g, ok, _n in results if g == gname and ok)
        out["pass_counts"][gname] = f"{passes}/{len(runs)}"
    path = EVALS / "results" / f"{name}.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out, indent=2) + "\n")
    return path


def calibrate():
    """Judges only, against hand-written known-bad and known-good artifacts."""
    pairs = [
        ("no-fabrication/graders/no-invented-material.md", "fabrication"),
        ("sentence-outline-not-labels/graders/every-line-is-a-claim.md", "outline"),
        ("short-form-restraint/graders/no-three-beat.md", "threebeat"),
        ("names-orphan-notes/graders/orphan-named.md", "orphan"),
        ("register-survives-fill-in/graders/holds-the-register.md", "register"),
        ("joints-after-fill-in/graders/last-sentence-sets-up-next.md", "joints"),
        ("joints-after-fill-in/graders/no-section-scale-restatement.md", "section"),
        ("topic-is-not-a-claim/graders/brief-asks-for-register.md", "askregister"),
        ("counts-come-from-the-file/graders/counts-match-the-source.md", "counts"),
        ("harvest-before-restructure/graders/names-what-it-keeps.md", "harvest"),
        ("facts-match-claim-width/graders/facts-prove-the-claim-above.md", "width"),
        ("critique-flags-planted-faults/graders/raises-all-three.md", "raised"),
        ("critique-quiet-on-clean-twin/graders/no-false-alarms.md", "falsealarm"),
        ("tighten-fixes-planted-faults/graders/faults-gone.md", "faultsgone"),
        ("tighten-fixes-planted-faults/graders/meaning-kept.md", "meaning"),
        ("tighten-light-on-clean-twin/graders/meaning-kept.md", "meaningclean"),
        ("critique-treats-praise-as-content/graders/praise-is-content.md", "praise"),
    ]
    # Script graders, run on their own known-bad and known-good output files.
    script_pairs = [
        ("tighten-fixes-planted-faults/graders/nothing-invented.md", "invented"),
    ]
    work = tempfile.mkdtemp(prefix="eval-calib-")
    allok = True
    for grader_path, stem in pairs:
        g, rubric = split_front_matter(EVALS / grader_path)
        for want_pass, suffix in ((False, "bad"), (True, "good")):
            art = (EVALS / "calibration" / f"{stem}-{suffix}.md").read_text()
            got, note = grade_llm(g, rubric, art, work)
            ok = got == want_pass
            allok &= ok
            verdict = "PASS" if got else "FAIL"
            print(f"  {'ok  ' if ok else 'BAD '} {stem}-{suffix}: judge said {verdict}, "
                  f"wanted {'PASS' if want_pass else 'FAIL'}")
    for grader_path, stem in script_pairs:
        g, _rubric = split_front_matter(EVALS / grader_path)
        for want_pass, suffix in ((False, "bad"), (True, "good")):
            art = EVALS / "calibration" / f"{stem}-{suffix}.md"
            got, note = run_script(g, EVALS / g["input"], art, work)
            ok = got == want_pass
            allok &= ok
            print(f"  {'ok  ' if ok else 'BAD '} {stem}-{suffix}: script said "
                  f"{'PASS' if got else 'FAIL'}, wanted {'PASS' if want_pass else 'FAIL'} ({note})")
    print("\ncalibration:", "judges are trustworthy" if allok else "A JUDGE IS BROKEN")
    return 0 if allok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--case", default=None)
    ap.add_argument("--runs", type=int, default=1,
                    help="agent runs per case, each in a new temp dir (default 1)")
    args = ap.parse_args()

    if args.calibrate:
        sys.exit(calibrate())

    cases = sorted(d for d in EVALS.iterdir()
                   if (d / "prompt.md").exists()
                   and (not args.case or d.name == args.case))
    # A result is only worth keeping if it says which skill it measured, so
    # uncommitted skill changes mean the run is not saved.
    dirty = git("status", "--porcelain", *SKILL_PATHS)
    if dirty:
        print("NOT SAVING results: uncommitted changes under draft/ outside draft/evals:\n" + dirty)
    failed = 0
    for c in cases:
        out = score_case(c, args.tag, args.runs)
        if not out:
            continue
        name, runs = out
        for i, (results, work, _artifact) in enumerate(runs, 1):
            for gname, ok, note in results:
                print(f"  {'ok  ' if ok else 'FAIL'} {name} [run {i}] / {gname}: {note}")
                failed += 0 if ok else 1
            print(f"       artifacts: {work}")
        if not dirty:
            print(f"       saved: {save_results(name, runs).relative_to(REPO)}")
    print(f"\n{failed} grader failure(s)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
