# Codex Compatibility Plan

This repo currently ships Claude Code plugins for two workflows:

- `draft`: critique and tighten prose with the Deirdre editor persona.
- `pitch`: evaluate and develop story pitches with a managing editor and a page-one meeting.

The goal is to make both workflows installable and usable in Codex while preserving the existing Claude Code plugin surface.

## Target Shape

Keep the current `draft/` and `pitch/` product boundary. Add Codex adapters beside the existing Claude adapters instead of collapsing everything into one plugin.

Planned files:

```text
.agents/plugins/marketplace.json
draft/.codex-plugin/plugin.json
pitch/.codex-plugin/plugin.json
docs/codex-compatibility-plan.md
docs/agent-portability.md
```

Each plugin manifest should point at its existing skill directory:

```json
{
  "name": "draft",
  "version": "1.0.0",
  "description": "Prose editing workflows for critique and tightening.",
  "skills": "./skills/"
}
```

Use Ponytail's Codex adapter pattern as the model:

- `.codex-plugin/plugin.json` is the installable plugin manifest.
- `.agents/plugins/marketplace.json` exposes local or repo-scoped plugins.
- `skills/` remains the canonical behavior.
- Host-specific files stay thin and do not duplicate workflow logic.

## Capability Mapping

Codex and Claude do not expose identical runtime capabilities. Rewrite skill instructions so the workflow is portable and the host-specific mechanism is conditional.

| Claude concept | Codex-compatible approach |
| --- | --- |
| `/critique`, `/tighten`, `/sharpen`, `/page-one-meeting` | Skill invocation through `$critique`, `$tighten`, `$sharpen`, `$page-one-meeting`, or `@plugin-skill` in plugin contexts. |
| `Read` | Read files using Codex's available file/shell tools. |
| `Write`, `Edit`, `MultiEdit` | Apply local file edits with Codex editing tools, normally `apply_patch`. |
| `WebSearch`, `WebFetch` | Use available web/search/browser tools when present; otherwise mark research-sensitive claims as unverified. |
| `AskUserQuestion` | Ask the user in chat only when the missing answer is blocking. |
| `Agent` / `Task` | Optional Codex subagents only when the user explicitly asks for parallel agent work or the session exposes a suitable subagent tool. |
| `SendMessage` | No direct Codex equivalent. The main agent acts as chair and routes each round explicitly. |
| `model: opus` | Do not hard-code in portable skill text. For optional Codex custom agents, use `gpt-5.5` for demanding editorial judgment and `gpt-5.4-mini` only for lightweight sidecar passes. |
| `tools:` frontmatter on agents | Keep Claude agent frontmatter for Claude. For Codex, move the reusable persona instructions into references or optional custom-agent TOML. |

## Skill Updates

### `draft`

Files:

- `draft/skills/critique/SKILL.md`
- `draft/skills/tighten/SKILL.md`
- `draft/references/deirdre-method.md`
- `draft/agents/editor.md`

Changes:

1. Keep `critique` read-only.
2. Keep `tighten` file-editing behavior, including automatic application and `updated:` frontmatter bump.
3. Replace "launch one editor agent per chunk" with a host-neutral instruction:
   - Prefer isolated critique passes per chunk when subagents are explicitly available.
   - Otherwise run the same critique prompts sequentially in the main thread.
4. Move the reusable Deirdre persona text into a reference that Codex skills can load directly.
5. Keep `draft/agents/editor.md` for Claude compatibility if Claude still expects that path.
6. Consider adding a deterministic chunking script so the skill does not depend on `tks` being installed.

### `pitch`

Files:

- `pitch/skills/sharpen/SKILL.md`
- `pitch/skills/page-one-meeting/SKILL.md`
- `pitch/agents/managing-editor.md`
- `pitch/skills/page-one-meeting/references/*.md`

Changes:

1. Make `sharpen` a direct single-editor workflow. It can load the managing-editor persona and apply it in the current Codex thread.
2. Keep web research conditional: use web tools when available; otherwise make the editorial verdict clear about any claims that were not independently checked.
3. Move reusable managing-editor instructions into a reference that Codex skills can load.
4. Keep `pitch/agents/managing-editor.md` for Claude compatibility if Claude still expects that path.

## Page-One Meeting Redesign

`page-one-meeting` is the largest compatibility gap. The current implementation assumes Claude's named background agents and `SendMessage` peer routing. Codex subagents exist, but Codex only spawns them when explicitly requested, and there is no direct peer-to-peer `SendMessage` surface.

Codex-compatible behavior:

1. Default mode: single-thread simulated panel.
   - The main agent acts as chair.
   - It creates 3-5 distinct editor personas.
   - It runs opening takes, debate, dissent, and final synthesis in structured phases.
   - It writes `pitches/<YYYY-MM-DD>-<slug>/pitch.md`.

2. Enhanced mode: explicit parallel subagents.
   - Use only when the user explicitly asks for parallel agents or the skill invocation includes a clear parallel instruction.
   - Spawn one Codex subagent per persona.
   - The chair sends each persona the same shared roster and raw material.
   - The chair collects opening takes.
   - The chair routes challenges by sending follow-up prompts to each subagent.
   - The chair assigns the mandatory dissent round.
   - The chair writes the final artifact.

3. Remove hard requirements for:
   - `Agent({ name, run_in_background: true })`
   - `SendMessage`
   - unprompted `agent-message` events
   - `Workflow`

4. Preserve the editorial safeguards:
   - intake can be abbreviated but not skipped silently
   - cast must fit the pitch's tensions
   - novelty/saturation check should usually be represented
   - mandatory dissent does not get skipped
   - chair's outside check remains before finalizing
   - `pitch.md` records dissent findings even when consensus holds

## Codex Skill Metadata

Add `agents/openai.yaml` to each skill for Codex UI metadata.

Suggested policy:

| Skill | Implicit invocation |
| --- | --- |
| `critique` | allowed |
| `tighten` | allowed, but description must state that it edits files |
| `sharpen` | allowed |
| `page-one-meeting` | consider explicit-only to avoid accidentally starting an expensive workflow |

Example:

```yaml
interface:
  display_name: "Critique Draft"
  short_description: "Read-only prose critique"
  default_prompt: "Use $critique to review this draft without editing it."
```

## Documentation Updates

Update `README.md` with separate install and invocation paths.

Claude Code:

```text
/plugin marketplace add benjaminjackson/writing-skills
/plugin install draft@writing-skills
/plugin install pitch@writing-skills
```

Codex:

```bash
codex plugin marketplace add benjaminjackson/writing-skills
codex
```

Then open `/plugins`, choose the `writing-skills` marketplace, and install `draft` and/or `pitch`.

Invocation examples:

```text
$critique path/to/draft.md
$tighten path/to/draft.md
$sharpen
$page-one-meeting
```

Also document that Codex custom prompts are not the target surface. These workflows should be skills, because skills can be invoked explicitly, discovered implicitly, packaged in plugins, and bundled with references.

## Validation

Add a small validation script, for example `scripts/check-codex-compat.js`.

Checks:

1. Parse `.claude-plugin/marketplace.json`.
2. Parse `draft/.claude-plugin/plugin.json` and `pitch/.claude-plugin/plugin.json`.
3. Parse `draft/.codex-plugin/plugin.json` and `pitch/.codex-plugin/plugin.json`.
4. Parse `.agents/plugins/marketplace.json`.
5. Verify every marketplace `source.path` exists.
6. Verify every plugin manifest `skills` path exists.
7. Verify every `SKILL.md` has valid frontmatter with `name` and `description`.
8. Verify every `agents/openai.yaml` is valid YAML when present.
9. Grep Codex-facing files for Claude-only runtime terms:
   - `Agent(`
   - `SendMessage`
   - `AskUserQuestion`
   - `WebSearch`
   - `WebFetch`
   - `subagent_type`
10. Verify README mentions both Claude and Codex installation.

## Implementation Order

1. Add Codex manifests and local marketplace.
2. Add `agents/openai.yaml` metadata.
3. Convert skill wording from Claude-native to host-neutral.
4. Redesign `page-one-meeting` around chair-routed debate with optional Codex subagents.
5. Update README installation and usage docs.
6. Add validation script.
7. Run validation and a manual smoke test in Codex.

## Open Decisions

1. Should `page-one-meeting` allow implicit invocation, or should it require explicit `$page-one-meeting`?
2. Should we publish as two Codex plugins (`draft` and `pitch`) or also provide a combined `writing-skills` wrapper plugin later?
3. Should chunking become deterministic with a bundled script, or is the current text-based method enough?
4. Should optional Codex custom agents live in this repo as examples, or should the skills avoid custom-agent config entirely for portability?
5. Should `tighten` keep applying substantive edits automatically in Codex, or should Codex get a safer review-first mode?
