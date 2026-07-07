# Critique Scenario

Claude:

```text
/critique scenarios/fixtures/draft-short.md
```

Codex:

```text
$critique scenarios/fixtures/draft-short.md
```

Expected:

- Reads the draft.
- Reports line-level and structural notes.
- Leaves the working tree unchanged.
- If the user asks it to rewrite, it redirects to `tighten`.

Unhappy path:

```text
$critique "scenarios/fixtures/draft path with spaces.md"
```

Expected: reads the file with spaces in the path and leaves it unchanged.
