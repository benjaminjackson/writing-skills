# Tighten Scenario

Claude:

```text
/tighten scenarios/fixtures/draft-frontmatter.md
```

Codex:

```text
$tighten scenarios/fixtures/draft-frontmatter.md
```

Expected:

- Applies edits only to the target file.
- Preserves meaning.
- Updates `updated:` when frontmatter is valid.
- Reports substantive edits and skipped cadence/emotional-line edits.

Unhappy paths:

```text
$tighten scenarios/fixtures/draft-malformed-frontmatter.md
```

Expected: applies body edits only, skips the `updated:` bump, and reports malformed frontmatter.

```text
$tighten scenarios/fixtures/draft-frontmatter.md
```

Run from a read-only or untrusted workspace.

Expected: reports that edits cannot be applied and does not claim success.
