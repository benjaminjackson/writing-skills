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

- `kills` (saturated cases): the verdict on the pitch as submitted stops it. The definition comes from the Decision comment on write-034.
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

Cost, estimated and not yet measured: 4 cases, 2 skills and 3 runs make 24 skill runs, plus 2 smoke runs, about $130 in all. Most of it is page-one-meeting. The judges add about $1 per calibration.

## Results

Not yet run: no paid run starts before Benjamin approves a spending cap.

| Case | Skill | Kills (n/3) | Leaves alone (n/3) | Invented fatal flaws per run | Mean cost per run |
|---|---|---|---|---|---|
| `remote-loneliness-saturated` | page-one-meeting | | — | — | |
| `remote-loneliness-saturated` | sharpen | | — | — | |
| `remote-loneliness-fresh` | page-one-meeting | — | | | |
| `remote-loneliness-fresh` | sharpen | — | | | |
| `teen-phones-saturated` | page-one-meeting | | — | — | |
| `teen-phones-saturated` | sharpen | | — | — | |
| `teen-phones-fresh` | page-one-meeting | — | | | |
| `teen-phones-fresh` | sharpen | — | | | |
