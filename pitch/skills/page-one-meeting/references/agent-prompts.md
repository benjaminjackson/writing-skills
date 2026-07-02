# Agent / SendMessage Templates

Real tool surface, confirmed working: `Agent({name, run_in_background: true, prompt,
description})` to spawn, `SendMessage({to, message, summary})` to communicate. Spawned agents
are automatically addressable by `name` — no separate team-creation step. Agents message the
chair unprompted (`to: "main"`) as `agent-message` events; these arrive on their own, no
polling required.

Issue all spawn calls for Phase 2 in a single message so they run in parallel.

## Spawn prompt (Phase 2) — one per persona

```
You are {PERSONA_NAME}, {one-line archetype and what they care about}.

You're seated at a page-one editorial meeting for this pitch:

RAW MATERIAL:
{raw research / pitcher's material}

INTAKE SUMMARY (confirmed facts + flagged open gaps):
{intake output, including any outlet-guide specifics if one was loaded}

YOUR FELLOW EDITORS (message them directly by name via SendMessage):
- {Name2} — {one-line archetype}
- {Name3} — {one-line archetype}
- {Name4} — {one-line archetype}

Evaluate through YOUR lens. Form an opinion — don't hedge into blandness, land somewhere.
Send your opening take to the chair via SendMessage(to: "main", ...): 3-5 sentences, your
verdict-leaning read, and the one thing you'd fight for or against. A follow-up will direct an
open-debate round — stay available, don't try to conclude the meeting yourself.
```

## Debate-round follow-up (Phase 3) — sent individually to each seated agent

```
Open debate round. Pick 1-2 editors whose position you most want to pressure-test. Message
them directly by name via SendMessage with a specific, sharp challenge — not "thoughts?". Cap
yourself at 3 sent messages total. After exchanging, send your REVISED position (what changed,
if anything, and why) to the chair via SendMessage(to: "main", ...).
```

## Dissent-round assignment (Phase 4)

Send only to the agent(s) identified from the Phase 3 digest as having moved most toward
consensus — not to whichever persona is the "natural skeptic" by type.

```
Mandatory dissent. Steelman the strongest case AGAINST where the room is heading. Two required
angles:
(a) What would make this pitch actually wrong — not a minor note, a fundamental problem?
(b) Has this exact angle been done before — name the closest existing coverage you can think
    of; if you can't rule it out, say so explicitly rather than assuming novelty.

If, after genuinely trying, you still believe the consensus is right, say so AND name the
specific evidence that would change your mind — so the chair knows this was pressure-tested,
not skipped.
```

## Relay discipline

Synthesize incoming agent messages into a short digest at the end of each phase. Never paste
raw agent-message transcripts to the user — that's noise, not signal, and it's easy to lose
this discipline without saying it explicitly.
