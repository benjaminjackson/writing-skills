---
type: script
command: cmp {input} {output}
input: fixtures/review-planted-400.md
focus: {source: file, path: draft.md}
weight: 1
---
Critique is read-only. This compares draft.md after the run with the fixture it was copied from, so a change made by any tool fails it: `Edit`, `Write` or a `Bash` command. `Edit` is in this case's allowed tools on purpose, so a critique that edits the file can do it and gets caught here rather than being blocked silently.
