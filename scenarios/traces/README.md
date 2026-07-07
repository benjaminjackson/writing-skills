# Trace Captures

Use this directory as the reference point for compatibility traces. Do not commit bulky raw transcripts by default. Commit only short, curated trace summaries when they explain a regression or prove a compatibility milestone.

## Required Fields

Each trace summary should include:

| Field | Meaning |
| --- | --- |
| `harness` | `claude-code` or `codex`. |
| `plugin` | `draft` or `pitch`. |
| `skill` | `critique`, `tighten`, `sharpen`, or `page-one-meeting`. |
| `scenario` | Stable scenario id matching a fixture or snippet. |
| `invocation` | Exact slash command, `$skill`, or prompt used. |
| `result` | `pass`, `fail`, or `blocked`. |
| `files_changed` | Expected and actual changed files, or `none`. |

Optional fields:

- `source`: marketplace URL, local path, branch, or commit under test.
- `install_steps`: exact commands or UI steps used to install.
- `inputs`: fixture files or pasted text used.
- `expected_path`: main-thread, Claude subagent, Codex sequential, or Codex explicit-subagent path.
- `assertions`: checks performed after the run.
- `known_gaps`: anything not verified, such as web novelty when web tools were unavailable.

## Template

```yaml
harness:
plugin:
skill:
scenario:
invocation:
result:
files_changed:
source:
install_steps:
inputs:
expected_path:
assertions:
known_gaps:
```
