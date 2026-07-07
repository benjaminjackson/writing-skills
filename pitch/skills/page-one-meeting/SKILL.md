---
name: page-one-meeting
description: >-
  Simulates a page-one editorial meeting on a pitch or idea: a chair convenes
  a dynamic panel of editor personas, pressure-tests the idea, forces a dissent
  round, and delivers a verdict plus shaped pitch. Trigger on "page one
  meeting", "run this by the editors", "simulate a pitch meeting", "editorial
  meeting on this", "get the room's take", "workshop this with a panel of
  editors", or /page-one-meeting. For a single quick editorial read instead of
  a multi-persona debate, use the sharpen skill.
---

# Page One

Run a simulated page-one editorial meeting. The chair (you) convenes a small panel of editor
personas who pressure-test a pitch, challenge one another's assumptions, force a mandatory
dissent round, and end with a verdict plus shaped pitch. Default output is a verdict and a
saved `pitch.md`. Pass `brief` as an argument, or have the user ask for it afterward, to
extend into a co-authored drafting brief.

The core behavior is editorial, not mechanical: the panel must avoid groupthink. Unguided
LLM debate can collapse into polite consensus and miss that an angle has already been done.
Phase 4 (mandatory dissent) and the chair's outside check in Phase 5 exist because in-room
agreement alone is not reliable.

Before starting, read [../../references/managing-editor.md](../../references/managing-editor.md)
for the verdict vocabulary and editorial standards.

## Host Behavior

- **Claude Code:** May use the native background-agent room and peer-message workflow from
  [references/agent-prompts.md](references/agent-prompts.md). Keep the same phase structure
  and relay only synthesized digests to the user.
- **Codex default:** Run the meeting as a chair-led simulation in the current thread. Create
  3-5 distinct editor personas, write their opening takes, challenge pairs, revised positions,
  and dissent in labeled notes, then synthesize. Do not spawn hidden subagents.
- **Codex explicit subagent mode:** Use separate Codex subagents only when the user explicitly
  asks for parallel agents or separate editor agents. The chair still owns routing, phase
  order, synthesis, outside check, and final artifact writing.

## Phase 0 - Intake (mandatory, abbreviable, no disk writes)

Read whatever raw material the pitcher already gave. Pasted research plus a general direction
often satisfies most of intake. Silently check it against
[references/intake-checklist.md](references/intake-checklist.md), then ask only the 2-3
highest-value missing items at a time. Ask in the managing-editor voice. Use direct chat
questions only for genuine forks or missing essentials, not the whole checklist.

The moment the pitcher says "just start" or otherwise signals impatience, proceed. Carry
anything unresolved forward as a flagged uncertainty in each persona's briefing, not as a
blocker.

If the pitcher names a target outlet, check for `pitch-guides/<outlet-slug>.md` in this repo.
If it exists, load it, brief the panel with its actual submission format, and shape the final
output to match it.

## Phase 1 - Cast Assembly (no disk writes)

Pick 3-5 archetypes suited to this pitch's actual tensions, using
[references/archetype-bench.md](references/archetype-bench.md) as inspiration, not a fixed
roster. Invent fresh names and voices every run. Seriously consider a novelty/saturation
archetype; its absence is what let an unoriginal angle slip through the first time this ran.

Post a one-line "seating the room" announcement naming the cast and why each persona is here
for this pitch.

## Phase 2 - Seating / Opening Takes

Run one opening take per persona using the Phase 2 template in
[references/agent-prompts.md](references/agent-prompts.md). Each persona receives the raw
material, intake summary, flagged gaps, target outlet, and roster of fellow editors.

Claude may run these as native background agents. Codex default mode should write each opening
take sequentially in the current thread, clearly labeled by persona. Codex explicit subagent
mode may run these in parallel, but each subagent reports back to the chair only.

Relay a synthesized digest to the user, never raw persona transcripts.

## Phase 3 - Open Debate (one round by default)

Use the debate-round template from [references/agent-prompts.md](references/agent-prompts.md).
Each persona pressures 1-2 named peers with specific challenges, then returns a revised
position. In Codex default mode, the chair simulates the exchange as labeled challenge and
response notes. In explicit subagent mode, the chair routes prompts and waits for responses.

Digest again. Default to a single round. Repeat only if positions are still wildly split.

## Phase 4 - Mandatory Dissent Round (structural, not discretionary)

This does not get skipped, and it is not optional even when the room looks unanimous -
especially when it looks unanimous.

From the Phase 3 digest, identify which persona moved most toward consensus. Assign dissent
duty to that persona, not to whichever archetype is the natural skeptic. Asking a built-in
skeptic to dissent just rehashes their existing position; forcing someone who just agreed to
argue the opposite produces new reasoning.

Use the dissent-round template in [references/agent-prompts.md](references/agent-prompts.md).
Two angles are required every time:

- Steelman the strongest case that the pitch is fundamentally wrong, not merely imperfect.
- Name the closest existing coverage of this exact angle, or say explicitly if the host cannot
  rule out that it has been done.

If the dissent still believes the consensus holds after genuinely trying, they say so and name
the specific evidence that would change their mind.

Record the dissent findings in `pitch.md` regardless of outcome. The record that the check
happened is part of the artifact, not just a gate to pass through.

## Phase 5 - Verdict + Shaped Pitch (first disk write)

1. Create `pitches/<YYYY-MM-DD>-<slug>/`. Derive the slug from the shaped angle the debate
   landed on, not the raw topic. Folder creation waits until this point because the angle is
   not knowable before the debate happens.
2. Synthesize the consensus and the Phase 4 dissent findings.
3. **Chair's outside check.** Before finalizing, briefly step outside the room and reread the
   shaped pitch as a skeptic would, independent of what the panel just agreed on. Ask: is this
   angle saturated; what is the closest coverage; can the host actually verify novelty; has
   the language drifted into sales or scarcity register?
4. For anything under real doubt about novelty or fact-checkability, run a second editorial
   gate using the managing-editor reference. Use web search/fetch tools when available and
   relevant. If web tools are unavailable, separate editorial judgment from unverified novelty
   or factual claims.
5. Write `pitch.md`: verdict using the managing-editor vocabulary (**Green light** /
   **Revise and resubmit** / **Kill it**), the shaped pitch (angle, headline, spine, reader,
   proof), the cast roster, debate synthesis, Phase 4 dissent section, outside check, and any
   flagged gaps carried from intake.
6. Report a short human summary to the user, not the file pasted in full.

## Phase 6 - Drafting Brief (argument-gated, optional)

Triggered by `/page-one-meeting brief`, a follow-up like "build the drafting brief," or by
offering it at the end of Phase 5. Always re-brief the cast fresh from the saved `pitch.md`
rather than relying on personas from earlier phases still being alive across a new session.
Assign one section per persona using
[references/pitch-brief-template.md](references/pitch-brief-template.md). Pull real published
analogues only when web tools are available; otherwise say the example section is blocked on
web access. Write `pitch-brief.md`.

## Reference Files

Load these only when the phase that needs them is reached:

- `../../references/managing-editor.md` - verdict vocabulary and editorial standards
- `references/intake-checklist.md` - Phase 0 question menu
- `references/archetype-bench.md` - Phase 1 exemplar archetypes
- `references/agent-prompts.md` - Phase 2-4 Claude native and Codex simulation templates
- `references/pitch-brief-template.md` - Phase 6 output shape
