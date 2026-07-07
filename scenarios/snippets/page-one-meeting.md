# Page-One Meeting Scenario

Claude:

```text
/page-one-meeting
```

Prompt body:

```text
Use scenarios/fixtures/pitch-saturated-angle.md
```

Codex default:

```text
$page-one-meeting
```

Prompt body:

```text
Use scenarios/fixtures/pitch-saturated-angle.md
```

Expected:

- Runs intake or carries missing details as flagged gaps.
- Seats 3-5 pitch-specific personas.
- Includes a novelty/saturation voice unless clearly unnecessary.
- Runs mandatory dissent.
- Writes `pitches/<YYYY-MM-DD>-<slug>/pitch.md`.
- Records dissent and chair outside-check findings in `pitch.md`.

Codex explicit subagent variant:

```text
$page-one-meeting Use parallel Codex subagents for the editor personas, then have the chair synthesize the meeting. Use scenarios/fixtures/pitch-saturated-angle.md.
```

Expected:

- Spawns subagents only because the user explicitly asked.
- The chair routes all debate prompts.
- Final output remains one coherent `pitch.md`, not raw subagent transcripts.
