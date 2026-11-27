# Evals for `pitch`: does page-one-meeting's debate beat one sharpen read?

`page-one-meeting` seats a room of editor agents that debate a pitch, then argue against their own consensus. `sharpen` asks the `managing-editor` agent once. The debate costs far more, so it has to earn its place. These evals ask whether it does, on the two things a pitch editor is for: stopping an idea that has already been done, and leaving a sound pitch alone without inventing reasons to stop it. This is ticket write-034.

The suite runs on `draft/evals/run.py`. The grader format, calibration and saved results are described in [draft/evals/README.md](../../draft/evals/README.md).

## The cases

Two pairs, each on one topic. In each pair the saturated pitch is a trend take with no reporting of its own, and the fresh twin is on the same topic but built on records and interviews the pitcher already holds, with a news peg. The fixtures are in `fixtures/` and are invented, so the room cannot find the county, the district or their records online.

| Case | Tags | Fixture |
|---|---|---|
| `remote-loneliness-saturated` | `pitch saturated pair-a` | "Remote work is making us lonely" |
| `remote-loneliness-fresh` | `pitch fresh pair-a` | Harlan County's counselling records before a return-to-office hearing |
| `teen-phones-saturated` | `pitch saturated pair-b` | "Smartphones are rewiring our kids" |
| `teen-phones-fresh` | `pitch fresh pair-b` | Ridgeway's nurse's-office logs before a state phone-ban vote |

Each case runs one skill, chosen with `--skill`. The prompt asks the skill to start without intake questions, which page-one-meeting's Phase 0 allows.

## What is measured

Each grader file holds its own definition; they are not repeated here. The graders live once in `graders/`, and each case's `graders/` links to the ones it uses.

- `kills` (saturated cases): the verdict on the pitch as submitted stops it. The definition comes from the Decision comment on write-034. The judge does not check that a linked piece is real. At merge, every link in the 8 kill runs was requested: 41 of 56 returned 200, 15 returned 403 from sites that block scripts (cdc.gov, JAMA, Axios and similar), none returned 404, and every kill run cites 2 to 11 links that loaded.
- `leaves-alone` (fresh cases): the verdict does not stop the sound pitch.
- `invented-flaws` (fresh cases): how many fatal flaws the verdict stands behind that the pitch does not have. It passes at 0, and the count is saved in the grader's note.
- `room-convened`, `room-debated` (page-one-meeting only) and `editor-ran` (sharpen only): the skill did what it claims, so a score is not a score of a skill that never ran.

The judges read the last message and any `pitches/*/pitch.md` the run wrote. A page-one-meeting artifact is far longer than the 2,000 characters the draft suite keeps its judges under, so read a surprising verdict before you believe it.

## Decision rule

Fixed before the runs, in the Decision comment on write-034: the debate beats sharpen only if its kill count over both pairs is strictly higher, and its invented-flaw total and leave-alone count are no worse. A tie means cut the debate.

## Running it

```
uv run --with pyyaml python3 draft/evals/run.py --evals pitch/evals --calibrate
uv run --with pyyaml python3 draft/evals/run.py --evals pitch/evals --tag pitch --skill page-one-meeting --runs 3
uv run --with pyyaml python3 draft/evals/run.py --evals pitch/evals --tag pitch --skill sharpen --runs 3
```

Results save to `results/<case>.<skill>.json`. Without `--runs`, each case runs once and nothing is saved, which is the smoke run.

Cost, measured on 2026-11-27: 4 cases, 2 skills and 3 runs made 24 skill runs, plus 2 smoke runs, $74.08 in reported cost in all. A page-one-meeting run costs about $4.80 and a sharpen run about $0.90. The judges add about $1 per calibration.

## Results

Run on 2026-11-27, 3 runs per case and skill, results in `results/<case>.<skill>.json`. No run timed out. In every page-one-meeting run the room made 4 to 6 Agent calls and 24 to 34 SendMessage calls, and sharpen launched the managing-editor agent every time.

| Case | Skill | Kills (n/3) | Leaves alone (n/3) | Invented fatal flaws per run | Mean cost per run |
|---|---|---|---|---|---|
| `remote-loneliness-saturated` | page-one-meeting | 3/3 | — | — | $4.83 |
| `remote-loneliness-saturated` | sharpen | 1/3 | — | — | $0.91 |
| `remote-loneliness-fresh` | page-one-meeting | — | 3/3 | 0, 0, 0 | $4.70 |
| `remote-loneliness-fresh` | sharpen | — | 3/3 | 0, 0, 0 | $0.89 |
| `teen-phones-saturated` | page-one-meeting | 3/3 | — | — | $4.98 |
| `teen-phones-saturated` | sharpen | 1/3 | — | — | $0.87 |
| `teen-phones-fresh` | page-one-meeting | — | 3/3 | 0, 0, 0 | $4.79 |
| `teen-phones-fresh` | sharpen | — | 3/3 | 0, 0, 0 | $0.92 |

Over both pairs, page-one-meeting kills 6 of 6 saturated runs and sharpen kills 2 of 6. Both leave the fresh twin alone 6 of 6, and neither invents a fatal flaw. By the decision rule, the debate beats sharpen.

Sharpen's four misses are all Revise and resubmit verdicts that name prior pieces with links. In the two `remote-loneliness-saturated` misses, the main reason is something else (a topic with its conclusion attached, evidence more contested than the pitch says), and the editor calls it an old story only as an "also". The two `teen-phones-saturated` misses are close calls. In run 2 the first reason given is "Novelty and timeliness fail", and the judges voted FAIL 2 to 1 because the reason joins saturation to the lack of a peg. In run 3 the editor opens with "what do you know that the last two years of coverage doesn't?", and the judges voted FAIL 2 to 0 because the six problems listed after it are about reporting and structure. If both close calls counted as kills, sharpen would kill 4 of 6, and the result would not change.
