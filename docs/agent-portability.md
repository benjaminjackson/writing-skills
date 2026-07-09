# Agent Portability

`writing-skills` is moving toward an agent-portable distribution. The skills remain the canonical behavior; host-specific files only make those skills discoverable in a given harness.

## Supported Adapters

| Host | Files | Notes |
| --- | --- | --- |
| Claude Code | `.claude-plugin/marketplace.json`, `draft/.claude-plugin/plugin.json`, `pitch/.claude-plugin/plugin.json`, `draft/agents/`, `pitch/agents/`, `*/skills/` | Existing native plugin install path. Claude slash commands and agent files remain supported. |
| Codex | `.agents/plugins/marketplace.json`, `draft/.codex-plugin/plugin.json`, `pitch/.codex-plugin/plugin.json`, `*/skills/*/agents/openai.yaml`, `*/skills/` | Plugin install path for Codex. Skills are invoked explicitly with `$critique`, `$tighten`, `$sharpen`, and `$page-one-meeting`. |

## Adapter Rule

Keep adapters thin. Do not duplicate workflow logic in plugin manifests, marketplace files, or UI metadata. Put reusable behavior in `SKILL.md`, `references/`, and scripts.

## Portable Behavior

- `draft/skills/critique/SKILL.md`: read-only prose critique.
- `draft/skills/tighten/SKILL.md`: automatic in-place prose tightening.
- `pitch/skills/sharpen/SKILL.md`: single managing-editor read.
- `pitch/skills/page-one-meeting/SKILL.md`: editorial panel simulation.

## Current Compatibility Notes

- Claude can keep using native `agents/` files and slash-command workflows.
- Codex skills should explicitly read required reference files; do not assume references are loaded automatically.
- Codex should not require hidden subagent fan-out. Use sequential main-thread workflows unless the user explicitly asks for parallel subagents.
- `page-one-meeting` should remain explicit-only in Codex because it can be expensive and writes files.
