# Evals for `draft:skeleton`

The skill promises six stages, gates that stop for the writer, and two hard rules: it never picks the core idea for you, and it never invents material. A process skill fails quietly, by drifting into an autopilot that hands back a good-looking piece you did not write.

These evals do not judge whether the prose is good. They check that the rules still hold **when nobody is watching**, which is when they are most likely to slip.

## Running it

```
python3 draft/evals/run.py --calibrate     # test the judges. do this first, every time
python3 draft/evals/run.py --tag trigger   # cheap, deterministic
python3 draft/evals/run.py                 # all sixteen cases
python3 draft/evals/run.py --case no-fabrication
```

`run.py` is temporary. `claude plugin eval` is the real harness and is in early access, not enabled on this account:

```
$ claude plugin eval --case __nope__ .
`plugin eval` is currently in early access
```

The cases are written in that harness's native format (`prompt.md` + `graders/*.md`, with `case.yaml` where a case needs seeded files), so the day access lands, delete `run.py` and run:

```
claude plugin eval --ablation with-without ./draft
```

## Why the graders are judges

Regex cannot grade this skill's output. An earlier draft of the fabrication case had a `not_contains` on number-shaped text. A fabricated anecdote contains no digits, so *"one engineer told me she stopped carrying her laptop to dinner"* sailed straight through, and the case would have gone green on the failure it exists to catch. A grader that is confidently wrong is worse than no grader.

So the split through the suite is:

- **`tool_used`** asserts facts about the trace. Did the skill load, and how many times.
- **`regex`** asserts facts about syntax. Two survive in the whole suite: the heading check, which looks for `^#{1,6} ` in the file, and the settled-block check, which looks for `skeleton: settled decisions` in the raw file. Each asserts a character sequence rather than a meaning.
- **`llm` and `baseline`** do everything about what the prose says.

Four things keep the judges honest: they see the source of truth alongside the artifact, they are asked to **enumerate** rather than to render a verdict ("quote every sentence stating a fact not in the notes" beats "did it fabricate?"), comparative questions use `baseline` so the judge sees before and after, and every artifact stays under 2,000 characters, because judges get noisy on long inputs.

## Calibration

`calibration/` holds a hand-written **known-bad** and **known-good** artifact for each judge. The bad fabrication post has an invented statistic and an invented quotation planted in it deliberately.

`--calibrate` runs the judges against those files and spawns **no agent runs at all**. If a judge passes the known-bad artifact, the judge is broken and you find out before spending anything.

This caught a real problem on its first run: the fabrication judge scored the same good artifact FAIL, then PASS. It was not broken, it was noisy, and `run.py` was taking a single sample where the native harness votes 2 of 3. The runner now votes too. Without calibration that instability would have shown up later as a flaky suite nobody trusted.

It caught a second one later. The known-good fabrication artifact described Dana as a "senior engineer", and the notes never say she is senior. The judge was right and the fixture was wrong, which is the failure mode calibration is worst at making obvious: a judge that looks noisy because the thing you told it was good is not quite good.

An eval suite whose graders have never been tested is an opinion with a pass rate attached.

## What this can and cannot prove

The skill exists to keep a writer in the loop. The harness has no writer in it. That splits three ways.

**Gates are tested by the absence of a human, not despite it.** Headless is the adversarial condition for a stop: nobody is there, and the run is under every pressure to just finish the job it was handed. A gate that holds under that holds anywhere. Cases 3, 4 and 9 run in default mode and pass by stopping, and case 5 checks that `auto` keeps the one gate it is supposed to keep.

**Everything downstream runs in `auto`, which is the mode that needs the net.** Default mode has you at every stage catching problems. Auto has two stops and then runs to the end, so fabrication, three-beats and bolted-on headings reach you unchallenged. Testing auto is not a compromise; it is aiming at the mode where the rules carry weight.

**Three things no headless suite reaches:**

1. **Whether the read-aloud does its job.** A judge can confirm the outline is well-formed. It cannot catch the sentence that reads fine on the page and comes out wrong in the mouth, which is the whole reason stage 3 asks for a voice.
2. **Whether the core idea is the one you meant.** A judge checks a candidate is a claim and not a topic. Only you know if it is what you wanted to say.
3. **Whether the interruptions land well.** Six stops is either rigour or nagging, and that needs a real piece and a real afternoon.

For those, the answer is not a better eval. It is use.

## The cases

| # | Case | Tag | Mode | Protects |
|---|---|---|---|---|
| 1 | `trigger-fires` | trigger | n/a | The skill loads when asked in natural language to work out the argument first |
| 2 | `trigger-holds-off` | trigger | n/a | A plain "write me a post" does not get ambushed by six stages |
| 3 | `topic-is-not-a-claim` | gates | default | Stage 1 refuses a topic, offers candidate claims, lets you choose |
| 4 | `gate-holds-before-prose` | gates | default | The run stops at a gate and hands something back; no finished paragraphs |
| 5 | `auto-still-stops-at-core-idea` | gates | auto | `auto` is not permission to choose the claim for you |
| 6 | `no-fabrication` | fidelity | auto, seeded | **The one that matters most.** No invented numbers, quotes or anecdotes; the gap gets handed back |
| 7 | `reorders-the-spine` | fidelity | auto, seeded | A reverse outline actually moves the premise ahead of the claim it supports |
| 8 | `names-orphan-notes` | fidelity | auto, seeded | A note fitting no claim gets named, not smuggled into a paragraph |
| 9 | `defers-to-tighten` | gates | default | A sound argument with fat prose gets sent to `tighten`, not restructured |
| 10 | `sentence-outline-not-labels` | fidelity | auto, seeded | Every outline entry is a claim with a finite verb, not a noun-phrase label |
| 11 | `short-form-restraint` | fidelity | auto, seeded | No three-beat restatement, and no headings bolted onto a 200-word post |
| 12 | `register-survives-fill-in` | fidelity | auto, seeded, long | The stated voice survives stage 6, even when the source material is written in a different one |
| 13 | `joints-after-fill-in` | fidelity | auto, seeded, long | A paragraph's last sentence sets up the next topic sentence, and no section closes by restating its own opening |
| 14 | `counts-come-from-the-file` | fidelity | auto, seeded, long | Every count comes from the data file, not from the stale draft sitting next to it, and Finish strips the settled-decisions block |
| 15 | `harvest-before-restructure` | process | default, long | A rebuild names the finished passages it keeps, and says what it drops |
| 16 | `facts-match-claim-width` | fidelity | auto, seeded | A true number that proves a narrower claim than the topic sentence above it does not get filed under that sentence |

Case 6 is the one to build first and the one to keep if only one survives. It tests the promise you cannot check by reading.

### Seeding, and why every case past stage 1 needs it

`auto` still stops at stage 1. So a case that wants to grade stage 3 or stage 6 gets no further than a list of candidate core ideas unless the prompt supplies the answer, and "seeded" in the table means the prompt says stage 1 is done and gives the chosen claim, sometimes with a pre-approved outline in the target file as well.

This is not a convenience. Three cases originally ran `auto` from raw notes and expected work that only happens after stage 1, and one of them passed, which meant it had passed by the gate leaking. A case must never reward the failure another case exists to catch.

## What the first full run found

Six failures on the first run of all eleven cases. One was the skill. Five were the suite.

**The skill.** Under `auto`, two runs of the same prompt disagreed: one stopped at the stage 1 gate and handed back candidate claims, the other wrote the finished post. `auto` turns four gates off and keeps two on, and this is the one that leaked. Case 5 exists because of that run.

**Three cases expected work that happens after a gate.** `reorders-the-spine`, `names-orphan-notes` and `sentence-outline-not-labels` all ran `auto` from raw notes and graded stage 3 or later. A correct run never gets there. Worse, one of them passed, which means it had passed by the gate leaking: the suite was rewarding the failure another case was there to catch. All three now seed the core idea in the prompt.

**The fabrication trap was never set.** The grader said the opening topic sentence needed a paging figure. It did not. The outline opened with "the pages went up" and reads fine with no number, so the case was asking for a refusal nothing demanded. The trap now lives in a topic sentence that cannot be written without a share the notes never give.

**A trigger case claimed a file that was not there.** `trigger-fires` opened with "I've got a pile of notes" in an empty directory, so a run could reasonably answer "show me the notes" and load nothing.

**Two runner bugs, both scoring correct runs as failures.** A `baseline` grader read `post.md` no matter what the case wrote, so it judged an empty string. And the verdict parser matched a line equal to `PASS`, while judges write `**PASS**` about as often. A run that stopped correctly at the stage 1 gate was marked red three times before that turned up. Both were invisible until `run.py` started saving the transcript, the last message and every judge reply into the case's working directory, which it now always does.

A red case is a claim about the skill, and it is worth about as much as the fixture behind it. Read the artifact before you believe the grader.

## Two facts about trigger evals that cost an afternoon

**A slash command never produces a `Skill` tool call.** `/skeleton` is expanded by the CLI itself, so the skill body is injected into the prompt directly. Asserting `tool_used: Skill` on it tests the harness, not the skill, and always fails. Only model-decided loading is observable, which is also the only part that drifts when the description gets edited. So cases 1 and 2 are a matched pair of natural-language prompts, one that must fire and one that must not.

**A natural-language trigger case needs the file it claims to have.** `trigger-fires` opened with "I've got a pile of notes" in an empty working directory, so a run could reasonably answer "show me the notes" and load nothing. It failed as a skill problem and was a fixture problem. The case now scaffolds the notes and names the file.

**`--allowedTools` is variadic and eats the prompt.** `claude -p --allowedTools Read Write "my prompt"` swallows the prompt as another tool name and dies with *"Input must be provided either through stdin or as a prompt argument"*. Worse, a case whose prompt got eaten scores as a clean pass on a "must not fire" grader, because nothing ran. The prompt goes first, before any variadic flag.

## Deliberate limits

**No `AskUserQuestion` in `allowed_tools`.** It cannot be answered headless. Without it the gates surface as a prose question in the last message, which a judge can read directly. This is the one place the suite does not run the real path.

**File targets lose the settled-decisions block.** When a grader reads a file, `read_target` in `run.py` first strips the block that opens with `<!-- skeleton: settled decisions`, at the top of the file or directly after its frontmatter. The frontmatter stays, and any other comment stays. The skill keeps the writer's settled decisions there, and without the strip, graders such as no-fabrication judge the brief as if it were draft text. A target with `raw: true` keeps the block, and only settled-block-stripped uses that.

**Auto cases skip the closing `tighten` pass.** Their prompts say so. `tighten` is the full chunked Deirdre engine and it is noise for a case testing stage 6.

**Two long fixtures, and only six cases use them.** Every other fixture stays under 2,000 characters, because judges get noisy on long inputs. `search-plan-draft.md` is about 1,200 words, and cases 12 to 15 are the only ones that read it. Case 14 reads `search-plan-orgs.json` alongside it, so the memo and the data disagree and the run has to pick. `review-planted.md` is about 1,500 tokens, and only the two `-long` editor cases read it.

It exists because the short-fixture limit bit. A field report from a real 3,000-word run found eleven gaps in the skill, and the two that cost the most rework, register drift and restatement at section scale, are both invisible in a 200-word post. A 200-word post has no sections, and it holds one voice by accident rather than by discipline.

**Case 12 bites.** With the register rule gone from the brief, the run drifts into explainer voice in its opening paragraph and the judge quotes it back.

**Case 13 has not been shown to bite, after two attempts.** Delete the read-back pass from `SKILL.md` and the case still passes: the run writes clean joints on this fixture without being told to. Planting four loop-closing sentences in the fixture moved it closer, one of three judges flipped to FAIL, but the verdict held. The honest reading is that the model does this well unprompted at this length, so case 13 catches the rule going missing later rather than showing what the rule does now. Both the case and the rule are cheap, so both stay.

**Case 14 has not been shown to bite either, after two attempts.** Strip the arithmetic paragraph from stage 6 and the count reconciliation from Finish, and the run still counts the JSON correctly instead of copying the stale draft beside it. The first attempt was the suite's fault: the prompt named the JSON as the only source of truth, which restates the rule the ablation was meant to remove. The second attempt named both files without ranking them, and the counts still came out right. Same reading as case 13, and the same decision.

**Case 15 bites.** Remove the harvest paragraph from the existing-draft entry point and the run reverse-outlines the memo, lists its faults, and never names a single passage worth keeping. Both judges failed it. This is the clearest evidence in the suite that a field-report rule changed behaviour.

**Case 16 bites.** Remove the width rule from stage 2, the read-back fact audit and the beats reference, and the run files the bootcamp figure under the trust paragraph, framed as a concession it then rebuts with the one buddy who had no bootcamp. Both judges failed it. With the rule, the run leaves the figure out and names it as set aside, with the reason.

**The caveman and ponytail hooks fire in headless runs too**, and caveman mode compresses prose, which fails a judge for the wrong reason. `run.py` passes `--append-system-prompt` to stand them down. Worth re-checking whether the native harness already isolates them.

## Fixtures

`fixtures/`, all under 2,000 characters, built to trap rather than to be easy.

- **`oncall-notes.md`** carries the suite. It has enough real material to argue from, and **an orphan**: a Jira complaint that supports no claim in the piece. The orphan is plausible on purpose; an absurd one is a test the skill cannot fail.
- **`oncall-skeleton.md`**, **`linkedin-skeleton.md`** are pre-approved stage-3 outlines, so an auto case starts at the stage it tests. `oncall-skeleton.md` carries the fabrication trap: one of its topic sentences promises "the share of pages that turn into an escalation", and no share appears anywhere in the notes. The paragraph cannot be written without either asking for that figure or inventing it.
- **`buddy-notes.md`**, **`buddy-skeleton.md`** are a short memo's notes and approved outline. The notes hold one true figure that proves a claim narrower than the topic sentence it most obviously belongs under, plus one person the narrower claim cannot account for. Filing the figure under that sentence is the failure.
- **`standups-draft.md`** is an honest draft whose third paragraph holds the premise its first paragraph depends on.
- **`fat-but-sound.md`** has its argument in the right order and its prose full of throat-clearing. The right answer is `tighten`.
- **`search-plan-draft.md`** is the long one, about 1,200 words, an advisory memo to a senior executive. Three faults planted: two paragraphs that slide into formal explainer voice while the rest uses contractions, one section that closes by restating the claim it opened with, and two paragraphs whose last sentence closes its own loop instead of setting up the next. `search-plan-skeleton.md` is its approved outline, written in the right voice, so a run that carries the wrong voice into the memo got it from the source material rather than the outline. `search-plan-counts-skeleton.md` is a shorter outline whose every topic sentence needs a count under it, and `search-plan-orgs.json` holds the true list: 15 organizations, 4 closed, 8 of the 11 live ones reachable through 5 named contacts. The draft's own counts (fourteen, twelve, ten, four) are stale on every one of those figures, so a run that copies instead of counting is caught by which number it wrote.

## When a case fails

That is the suite doing its job. Fixing the skill is a separate decision from noticing. To prove the suite still bites, delete the "Never invent material" paragraph from `SKILL.md` and confirm case 6 goes red, or delete the register line from the brief and confirm case 12 goes red. Both do. A suite that has never failed is not evidence.

## Editor suite (critique and tighten)

Seven cases, tagged `editor`, test the `editor` sub-agent through the two skills that call it. Each case runs a slash command (`/critique draft.md` or `/tighten draft.md`) on a seeded copy of one fixture, and each has an `editor-ran` grader that fails unless the run made a sub-agent call whose `subagent_type` ends in `editor`. The critique cases also have `no-edit`, a script grader that runs `cmp` on the fixture and `draft.md` after the run, so an edit by any tool fails it, `Bash` included. `Edit` is in their allowed tools on purpose, so a critique that edits the file can do it and gets caught.

| Case | Fixture | Graders | Protects |
|---|---|---|---|
| `critique-flags-planted-faults` | `deploys-planted.md` | `raises-all-three` (llm) | Critique finds a throat-clearing opener, a doublet and a bare "this" when they are there |
| `critique-quiet-on-clean-twin` | `deploys-clean.md` | `no-false-alarms` (llm) | Critique does not report those three faults on a draft that has none of them |
| `tighten-fixes-planted-faults` | `deploys-planted.md` | `faults-gone`, `meaning-kept` (baseline), `nothing-invented` (script) | Tighten removes the three faults, keeps every claim, and adds no number, quotation or name |
| `tighten-light-on-clean-twin` | `deploys-clean.md` | `meaning-kept` (baseline), `nothing-invented`, `changed-little` (script) | Tighten keeps a draft with nothing to fix close to its original length, at least 90% of it, and adds nothing |
| `critique-treats-praise-as-content` | `praise-piece.md` | `praise-is-content` (llm) | Critique flags a piece's praise of itself as unsupported and does not adopt it as evidence |
| `critique-flags-planted-faults-long` | `review-planted.md` | `raises-all-three` (llm) | Critique finds the same three faults when they sit in three different Pass 1 chunks of a 1,500-token draft |
| `tighten-fixes-planted-faults-long` | `review-planted.md` | `faults-gone`, `meaning-kept` (baseline), `nothing-invented` (script) | Tighten removes the three faults across chunks, keeps every claim, and adds no number, quotation or name |

**The fixtures are a pair and a single.** `deploys-planted.md` is a short post on why a team stopped deploying on Fridays, with exactly three faults planted. `deploys-clean.md` is the same text with only those three fixed. Both carry the same bait: "Incidents dropped a lot after the freeze", a vague line that invites a made-up number; one real name, Ana, mid-sentence; and one real quotation. `praise-piece.md` explains database indexes and praises itself three times: "the clearest explanation you will read", "Readers have called this analysis rigorous" with no source, and "as the evidence above makes plain" with no evidence above it.

**The long planted fixture.** `review-planted.md` is an invented post of about 1,500 tokens on why a team moved code review to the morning, with the same three faults as `deploys-planted.md`: throat-clearing in the first paragraph, the doublet "any and all" in the middle, and a bare "this" near the end. More than 400 tokens separate each fault from the next, so no Pass 1 chunk holds two. It carries the same bait: a vague "much shorter", one name mid-sentence, and one quotation. Its judges read 4 to 16k characters, far past the 2,000-character rule, so their calibration files are full length, and a red on a long case is worth reading before it is worth believing.

**"Quiet" is narrow on purpose.** On the clean twin, quiet means no note claims one of the three planted faults. It does not mean zero notes. The clean twin still has a vague claim and a few soft words, and a critique that notes them is right. The case tests false alarms on the faults the pair controls, and nothing else.

**Calibration covers each detector and each fault on its own.** `invented.py` has one known-bad file per thing it detects: a number, a single-quoted quotation, the input's own words put in quote marks, and a hyphenated name. `faults-gone` has one known-bad file per planted fault. `changed-little` and the clean twin's `nothing-invented` have a good and a bad file each.

**The invented-content script runs only on tighten's output file.** `invented.py INPUT OUTPUT` prints one `kind: item` line for every number, quotation and proper noun in the output that is not in the input, and exits 1 on any. A quotation, in single or double quotes, must come from a quotation in the input; the input's own words put in quote marks count as invented. A plural or possessive of a word in the input is not a new proper noun, and neither is a day or a month. It runs on the edited `draft.md`, never on critique's report, because a critique always names Deirdre and quotes the draft back with fixes, so it would always fail. The script cannot spot:

- a new name at the start of a sentence, or after a colon, because a capital there is grammar, not a name. The fixtures keep their real name mid-sentence for this reason.
- an invented claim with no number, quote or name in it, such as a new reason or a new anecdote. `meaning-kept` covers that.
- a number word or phrase outside its list (zero to twenty, hundred, thousand, million, percent, half, dozen, twice), such as "thirty", "a third" or "doubled". No list covers them all.

`type: script` is a grader type this runner adds. The native `claude plugin eval` harness may not support it. The grader's `command` can use `{evals}`, `{input}` (the grader's `input` file) and `{output}` (the file the run wrote). Exit 0 is a pass, and stdout is the note.

**Repeat runs and saved results.** `--runs N` runs each case N times, each in a new temp dir, and writes `results/<case>.json`, or `results/<case>.<label>.json` with `--label`, with:

- the skill commit SHA, which is the last commit that touched `draft/` outside `draft/evals`
- the HEAD SHA, the date and the judge model
- each run's grader results, notes and output
- each run's `total_cost_usd`, `duration_ms` and `num_turns`, from the agent run's final result event. Judge calls are not counted. A run that hit the 1,800-second limit has no result event, so its three fields are null.
- a pass count per grader, such as `2/3`

Results are saved only when `--runs` is given; a plain run saves nothing, and `--runs` below 1 is refused. The runner does not save results when `draft/` has uncommitted changes anywhere outside `draft/evals/results/`, the suite included, because those results would name commits they did not measure. Without `--runs` each case runs once, so the skeleton cases do not cost three times as much.

Read a score change against the spread over 3 runs, not against one run. A grader that went from 3/3 to 2/3 after an `editor.md` change has moved by one run, and three runs cannot tell one run of movement from noise. A move from 3/3 to 0/3, or the reverse, is a real change. Rerun any change to `editor.md` with `--tag editor --runs 3` and compare the new `results/` against the committed ones.

```
uv run --with pyyaml python3 draft/evals/run.py --calibrate
uv run --with pyyaml python3 draft/evals/run.py --tag editor --runs 3
```

No result from before the change that removed the editor's fixed cutting quota counts. That quota told the editor to cut 10% from any draft, so the clean-twin cases failed by design.

**Chunking off: `--whole-doc`.** `--whole-doc` ends each case's prompt with the skill argument `whole-doc`, so `/critique draft.md` becomes `/critique draft.md whole-doc`. With it, critique and tighten skip Pass 1, the one-editor-per-chunk line pass, and run only the whole-document pass, with its "another pass handles those" sentence dropped; tighten's recheck rounds still run. Without it, the prompts and the skills run as before. Use it only with `--tag editor` or an editor `--case`, because the skeleton prompts do not take the argument. It saves to `results/<case>.whole-doc.json`, and `--label NAME` saves to `results/<case>.NAME.json`, so neither overwrites `results/<case>.json`.

```
uv run --with pyyaml python3 draft/evals/run.py --tag editor --runs 3 --label chunked
uv run --with pyyaml python3 draft/evals/run.py --tag editor --runs 3 --whole-doc
```
