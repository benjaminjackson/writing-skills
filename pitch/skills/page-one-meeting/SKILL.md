---
name: page-one-meeting
description: >-
  Simulates a page-one editorial meeting on a pitch or idea: a dynamic panel
  of editor personas debates it live via SendMessage, then delivers a
  verdict. Trigger on "page one meeting", "run this by the editors",
  "simulate a pitch meeting", "editorial meeting on this", "get the room's
  take", "workshop this with a panel of editors", or /page-one-meeting. For a
  single quick editorial read instead of a multi-agent debate, use the
  managing-editor agent directly, not this skill.
---

# Page One

Run a simulated page-one editorial meeting: a chair (you) convenes a small panel of editor
personas who debate a pitch with each other — not just report to the chair one at a time —
and the meeting ends in a verdict. Default output is a verdict and a shaped pitch. Pass
`brief` as an argument, or have the user ask for it afterward, to extend into a co-authored
drafting brief.

Mechanism: the `Agent` tool with a distinct `name` per persona and `run_in_background: true`,
then `SendMessage` to reach agents by name. Agents message the chair unprompted as they
finish — no polling. Never use the `Workflow` tool for this: the debate has to happen between
named personalities who can message each other and the pitcher, not a deterministic script.

One thing broke the first time this ran by hand, and this skill exists to prevent it:
**groupthink**. Unguided multi-agent LLM debate has documented failure modes — sycophantic
conformity, consensus collapse, lock-in often by the second exchange. The room converged
fast and clean, and missed that the whole angle had already been done — a human had to step
*outside* the simulated room to catch it. Phase 4 (mandatory dissent) and the chair's outside
check in Phase 5 exist specifically because in-room debate alone didn't catch this.

## Phase 0 — Intake (mandatory, abbreviable, no disk writes)

Read whatever raw material the pitcher already gave — if they pasted a page of research and a
general direction, that already satisfies most of intake. Silently check it against
`references/intake-checklist.md`, then ask only the 2-3 highest-value *missing* items at a
time, conversationally (ask, don't tell — see `managing-editor.md`'s voice for the model).
Use `AskUserQuestion` only for genuine either/or forks, not the whole checklist. The moment
the pitcher says "just start" or otherwise signals impatience, proceed — carry anything
unresolved forward as a flagged uncertainty in each persona's briefing, not as a blocker.

If the pitcher names a target outlet, check for `pitch-guides/<outlet-slug>.md` in this repo
(e.g. `pitch-guides/vox.md` already exists). If it exists, load it, brief the panel with its
actual submission format, and shape the final output to match it.

## Phase 1 — Cast Assembly (no disk writes)

Pick 3-5 archetypes suited to *this pitch's* actual tensions, using
`references/archetype-bench.md` as inspiration — not a fixed roster. Invent fresh names and
voices every run. Seriously consider a novelty/saturation-checking archetype; its absence is
what let an unoriginal angle slip through the first time this ran. Post a one-line "seating
the room" announcement naming the cast and why each one is here for this specific pitch.

## Phase 2 — Seating / Opening Takes

Issue all N `Agent` calls in a single parallel message: distinct `name` per persona,
`run_in_background: true`, prompt built from the spawn template in
`references/agent-prompts.md`. Each persona's prompt includes the raw material, the intake
summary plus flagged gaps, and the roster of fellow editors they can message by name.

Wait for opening takes to arrive as `agent-message` events — this is automatic, not
something to poll for. Relay a **synthesized digest** to the user, never a raw dump of agent
messages.

## Phase 3 — Open Debate (one round by default)

Send each seated agent the debate-round follow-up from `references/agent-prompts.md`: message
1-2 named peers directly with a specific, sharp challenge, cap 3 sent messages, then report a
revised position to the chair. Digest again. Default to a single round — only repeat if
positions are still wildly split after this one.

## Phase 4 — Mandatory Dissent Round (structural, not discretionary)

This does not get skipped, and it is not optional even when the room looks unanimous —
especially when it looks unanimous.

From the Phase 3 digest, identify which agent(s) moved *most toward* consensus. Assign dissent
duty to one of them, not to whichever persona's archetype is "the skeptic" — asking a built-in
skeptic to dissent just produces a rehash of their existing position; forcing someone who just
agreed to argue the opposite produces genuinely new reasoning. Use the dissent-round template
in `references/agent-prompts.md`: two required angles every time — (a) steelman the strongest
case that the pitch is fundamentally wrong, not a minor note; (b) name the closest existing
coverage of this exact angle, or say explicitly if you can't rule out that it's been done. If
the agent still believes the consensus holds after genuinely trying, they say so and name the
specific evidence that would change their mind.

Record the dissent findings in `pitch.md` regardless of outcome. The record that the check
happened is part of the artifact, not just a gate to pass through.

## Phase 5 — Verdict + Shaped Pitch (first disk write)

1. Create `pitches/<YYYY-MM-DD>-<slug>/`. Derive the slug from the *shaped angle* the debate
   landed on, not the raw topic — folder creation waits until this point because the angle
   isn't knowable before the debate happens.
2. Synthesize the consensus and the Phase 4 dissent findings.
3. **Chair's outside check.** Before finalizing, briefly step outside the room and reread the
   shaped pitch as a skeptic would, independent of what the panel just agreed on: is this angle
   actually saturated — name the closest coverage, or admit you can't rule it out; has the
   language drifted into sales/scarcity register.
4. For anything under real doubt about novelty or fact-checkability, optionally invoke the
   `managing-editor` agent as a second, genuinely separate gate — it wasn't primed by the
   room's framing and carries live `WebSearch`/`WebFetch`. Skippable when the dissent round and
   outside check already resolved the question.
5. Write `pitch.md`: verdict using `managing-editor.md`'s vocabulary (**Green light** / **Revise
   and resubmit** / **Kill it**), the shaped pitch (angle, headline, spine, reader, proof), the
   cast roster, the debate synthesis, the Phase 4 dissent section (kept even when resolved),
   the outside check, and any flagged gaps carried from intake.
6. Report a short human summary to the user — not the file pasted in full.

## Phase 6 — Drafting Brief (argument-gated, optional)

Triggered by `/page-one-meeting brief`, a follow-up like "build the drafting brief," or by offering it
at the end of Phase 5. Always re-brief the cast fresh from the saved `pitch.md` rather than
relying on agents from earlier phases still being alive — there's no reliable way to confirm
that, especially across a new session. Assign one section per persona (mirrors the shape in
`references/pitch-brief-template.md`), each pulling real published analogues via
`WebSearch`/`WebFetch`. Write `pitch-brief.md`.

## Reference files

Load these only when the phase that needs them is reached:

- `references/intake-checklist.md` — Phase 0 question menu
- `references/archetype-bench.md` — Phase 1 exemplar archetypes
- `references/agent-prompts.md` — Phase 2-4 spawn/debate/dissent templates
- `references/pitch-brief-template.md` — Phase 6 output shape
