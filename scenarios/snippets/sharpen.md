# Sharpen Scenario

Claude:

```text
/sharpen scenarios/fixtures/pitch-raw.md
```

Codex:

```text
$sharpen scenarios/fixtures/pitch-raw.md
```

Expected:

- Gives one managing-editor verdict: green light, revise and resubmit, or kill it.
- Does not write files.
- Names any web checks it actually performed.
- If web tools are unavailable, separates editorial judgment from unverified novelty or fact claims.

Unhappy path:

```text
$sharpen scenarios/fixtures/pitch-needs-intake.md
```

Expected: asks only for the missing information needed to make the editorial call, or proceeds outlet-agnostic while flagging gaps.
