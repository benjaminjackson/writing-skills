# Page-One Persona Templates

These templates support both host modes:

- **Claude native room:** Run each persona as a named background editor and use the host's
  native peer-message surface for challenges. Claude Code tool pattern:
  `Agent({name, run_in_background: true, prompt, description})` to spawn and
  `SendMessage({to, message, summary})` to communicate. Personas report back to the chair.
- **Codex default room:** The chair simulates each persona in the current thread. Keep notes
  labeled by persona and phase. Do not invent a raw transcript; write only the takes needed
  for synthesis.
- **Codex explicit subagent room:** Use separate Codex subagents only when the user explicitly
  asks. The chair sends each subagent its persona brief and phase prompt, waits for responses,
  and synthesizes. Subagents report to the chair, not directly to each other.

## Opening Take Template (Phase 2)

Use once per persona.

```text
You are {PERSONA_NAME}, {one-line archetype and what you care about}.

You are seated at a page-one editorial meeting for this pitch:

RAW MATERIAL:
{raw research / pitcher's material}

INTAKE SUMMARY:
{confirmed facts, target outlet, flagged open gaps, outlet-guide specifics if loaded}

FELLOW EDITORS:
- {Name2}: {one-line archetype}
- {Name3}: {one-line archetype}
- {Name4}: {one-line archetype}

Evaluate through your lens. Form an opinion; do not hedge into blandness. Return 3-5
sentences: your verdict-leaning read and the one thing you would fight for or against.
Do not conclude the meeting yourself.

Claude native room: send this opening take to the chair with `SendMessage(to: "main", ...)`.
```

## Debate-Round Template (Phase 3)

Use once per persona after all opening takes are available.

```text
Open debate round. Pick 1-2 editors whose position you most want to pressure-test. Challenge
each with a specific, sharp question, not "thoughts?". Then return your revised position:
what changed, if anything, and why.

Claude native room: message peers directly by name with `SendMessage`. Cap yourself at 3 sent
messages total, then send the revised position to the chair with `SendMessage(to: "main", ...)`.
```

For Codex default mode, the chair writes the challenge and response notes directly:

```text
{PERSONA_NAME} challenges {PEER_NAME}: {specific challenge}
{PEER_NAME} response: {short answer}
{PERSONA_NAME} revised position: {what changed, if anything}
```

## Dissent-Round Template (Phase 4)

Assign this to the persona identified from the Phase 3 digest as having moved most toward
consensus, not to whichever persona is the natural skeptic.

```text
Mandatory dissent. Steelman the strongest case AGAINST where the room is heading.

Two required angles:
1. What would make this pitch fundamentally wrong, not just flawed?
2. Has this exact angle been done before? Name the closest existing coverage you know of, or
   say explicitly that you cannot rule it out.

If, after genuinely trying, you still believe the consensus is right, say so and name the
specific evidence that would change your mind.
```

## Relay Discipline

Synthesize persona outputs into a short digest at the end of each phase. Never paste raw
persona transcripts to the user. Raw transcript detail is noisy and makes the final artifact
harder to trust.
