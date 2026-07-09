# Codex Install Scenario

Use this snippet to verify the Codex local marketplace path during development.

```bash
codex plugin marketplace add ./.
codex
```

Then open:

```text
/plugins
```

Expected:

- The `writing-skills` marketplace appears.
- `draft` and `pitch` can be installed independently.
- Installed skills appear in `/skills`.
- `$critique`, `$tighten`, `$sharpen`, and `$page-one-meeting` are available after installing the matching plugins.

Remote marketplace path after upstream merge:

```bash
codex plugin marketplace add benjaminjackson/writing-skills
codex
```
