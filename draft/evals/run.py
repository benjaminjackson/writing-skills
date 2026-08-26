#!/usr/bin/env python3
"""Interim runner for the draft:skeleton eval suite.

Temporary. `claude plugin eval` is the real harness and is in early access; when
it lands, delete this file and run:

    claude plugin eval --ablation with-without ./draft

Usage:
    python3 draft/evals/run.py --calibrate        # judges only, no agent runs
    python3 draft/evals/run.py --tag trigger      # one tag
    python3 draft/evals/run.py                    # everything
"""
import argparse, json, re, shutil, subprocess, sys, tempfile, os
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
    pat = re.compile(g["input_match"]) if g.get("input_match") else None
    hits = [t for t in tools
            if json.loads(t).get("name") == g["tool"] and (not pat or pat.search(t))]
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


def score_case(case_dir, tags):
    meta, prompt = split_front_matter(case_dir / "prompt.md")
    if tags and not (set(tags) & set(meta.get("tags", []))):
        return None
    cfg = {}
    if (case_dir / "case.yaml").exists():
        cfg = yaml.safe_load((case_dir / "case.yaml").read_text()) or {}

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
    for gf in sorted((case_dir / "graders").glob("*.md")):
        g, rubric = split_front_matter(gf)
        if g["type"] == "tool_used":
            ok, note = grade_tool_used(g, tools)
        elif g["type"] == "regex":
            ok, note = grade_regex(g, read_target(g.get("target"), work, last))
        else:
            target = g.get("focus") or {"source": "file", "path": "post.md"}
            ok, note = grade_llm(g, rubric, read_target(target, work, last), work, gf.stem)
        results.append((gf.stem, ok, note))
    return case_dir.name, results, work


def calibrate():
    """Judges only, against hand-written known-bad and known-good artifacts."""
    pairs = [
        ("no-fabrication/graders/no-invented-material.md", "fabrication"),
        ("sentence-outline-not-labels/graders/every-line-is-a-claim.md", "outline"),
        ("short-form-restraint/graders/no-three-beat.md", "threebeat"),
        ("names-orphan-notes/graders/orphan-named.md", "orphan"),
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
    print("\ncalibration:", "judges are trustworthy" if allok else "A JUDGE IS BROKEN")
    return 0 if allok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--case", default=None)
    args = ap.parse_args()

    if args.calibrate:
        sys.exit(calibrate())

    cases = sorted(d for d in EVALS.iterdir()
                   if (d / "prompt.md").exists()
                   and (not args.case or d.name == args.case))
    failed = 0
    for c in cases:
        out = score_case(c, args.tag)
        if not out:
            continue
        name, results, work = out
        for gname, ok, note in results:
            print(f"  {'ok  ' if ok else 'FAIL'} {name} / {gname}: {note}")
            failed += 0 if ok else 1
        print(f"       artifacts: {work}")
    print(f"\n{failed} grader failure(s)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
