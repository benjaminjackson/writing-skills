# Claude Install Scenario

Use this snippet to verify the existing Claude Code plugin path.

```text
/plugin marketplace add benjaminjackson/writing-skills
/plugin install draft@writing-skills
/plugin install pitch@writing-skills
/plugin list
```

Expected:

- `draft` and `pitch` appear as installed plugins.
- `/critique`, `/tighten`, `/sharpen`, and `/page-one-meeting` are available.
- Claude-native agent files still support `editor` and `managing-editor`.

Unhappy path:

```text
/plugin install draft@writing-skills
/sharpen scenarios/fixtures/pitch-raw.md
```

Expected: `sharpen` is unavailable or the harness gives clear install guidance for `pitch`.
