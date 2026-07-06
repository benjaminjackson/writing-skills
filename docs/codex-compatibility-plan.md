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
scenarios/fixtures/*.md
scenarios/snippets/*.md
scenarios/traces/README.md
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

## Test Evidence

The compatibility work should leave behind enough evidence to answer three questions:

1. Can both plugins be installed in Claude Code and Codex from the intended marketplace path?
2. Does each skill take the intended path in both harnesses?
3. Do failure cases fail safely, without editing the wrong files, inventing research, or relying on unavailable host tools?

Commit hand-authored scenarios and prompt snippets. Do not commit bulky raw transcripts by default; keep generated traces out of normal diffs unless a trace is short and explains a regression. Add `scenarios/traces/README.md` to define where local trace captures go and which summaries should be copied into issues or PRs.

Suggested structure:

```text
scenarios/
  fixtures/
    draft-short.md
    draft-frontmatter.md
    draft-long.md
    pitch-raw.md
    pitch-needs-intake.md
    pitch-saturated-angle.md
  snippets/
    claude-install.md
    codex-install.md
    critique.md
    tighten.md
    sharpen.md
    page-one-meeting.md
  traces/
    README.md
```

Trace captures should record:

| Field | Purpose |
| --- | --- |
| `harness` | `claude-code` or `codex`. |
| `source` | Marketplace URL, local path, branch, or commit under test. |
| `plugin` | `draft` or `pitch`. |
| `skill` | `critique`, `tighten`, `sharpen`, or `page-one-meeting`. |
| `scenario` | Stable scenario id, matching the fixture/snippet name. |
| `install_steps` | Exact commands or UI steps used to install. |
| `invocation` | Exact slash command, `$skill`, or explicit prompt used. |
| `inputs` | Fixture files or pasted text used. |
| `expected_path` | Main-thread, Claude subagent, Codex sequential, or Codex explicit-subagent path. |
| `files_changed` | Expected changed files, or `none` for read-only skills. |
| `assertions` | Pass/fail checks performed after the run. |
| `known_gaps` | Anything not verified, such as web novelty when web tools were unavailable. |

## Installation Scenarios

Validate both a local-development install path and the eventual repository marketplace path.

### Claude Code

Happy paths:

```text
/plugin marketplace add benjaminjackson/writing-skills
/plugin install draft@writing-skills
/plugin install pitch@writing-skills
/plugin list
```

Expected:

- `draft` and `pitch` appear as installed plugins.
- `critique`, `tighten`, `sharpen`, and `page-one-meeting` are invokable.
- Claude-specific agent files still work for `editor` and `managing-editor`.

Unhappy paths:

- Install only `draft`, then invoke `/sharpen`. Expected: unavailable or clear install guidance, not a broken partial workflow.
- Install only `pitch`, then invoke `/tighten`. Expected: unavailable or clear install guidance.
- Remove and reinstall a plugin. Expected: no stale command or agent behavior.
- Use a fixture path with spaces. Expected: command examples and skill instructions handle it.

### Codex

Happy paths:

```bash
codex plugin marketplace add benjaminjackson/writing-skills
codex
```

Then in Codex:

```text
/plugins
```

Expected:

- The `writing-skills` marketplace appears.
- `draft` and `pitch` can be installed independently.
- Installed skills appear in `/skills` and can be invoked explicitly with `$skill` or `@plugin-skill`.
- `agents/openai.yaml` metadata renders readable names and default prompts.

Unhappy paths:

- Install `draft` only, then invoke `$sharpen`. Expected: Codex does not silently choose the wrong skill; user gets a clear missing-plugin path.
- Invoke `$tighten` in a read-only or untrusted workspace. Expected: it reports that edits cannot be applied instead of presenting edits as completed.
- Invoke `$page-one-meeting` without explicit parallel-agent permission. Expected: it uses the single-thread chair workflow, not hidden subagent fan-out.
- Invoke `$page-one-meeting` while web tools are unavailable. Expected: novelty and closest-coverage checks are marked unverified rather than invented.

## Invocation Snippets

Each snippet file should include the exact user prompt, fixture path, expected tool path, and acceptance checks. Keep snippets short enough to paste into either harness.

### `critique`

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
- Does not edit the fixture.
- If the user asks it to rewrite, it redirects to `tighten`.

### `tighten`

Claude:

```text
/tighten scenarios/fixtures/draft-frontmatter.md
```

Codex:

```text
$tighten scenarios/fixtures/draft-frontmatter.md
```

Expected:

- Applies exact edits only to the target file.
- Preserves meaning.
- Updates `updated:` when frontmatter exists.
- Reports applied substantive changes and skipped cadence/emotional-line edits.

### `sharpen`

Claude:

```text
/sharpen
```

Codex:

```text
$sharpen
```

Prompt body should paste or mention `scenarios/fixtures/pitch-raw.md`.

Expected:

- Gives a single managing-editor verdict.
- Does not write files.
- If web tools are used, names what was checked.
- If web tools are unavailable, separates editorial judgment from unverified novelty/fact claims.

### `page-one-meeting`

Claude:

```text
/page-one-meeting
```

Codex:

```text
$page-one-meeting
```

Prompt body should paste or mention `scenarios/fixtures/pitch-saturated-angle.md`.

Expected:

- Runs intake or explicitly carries missing details as flagged gaps.
- Seats 3-5 pitch-specific personas.
- Includes a novelty/saturation voice unless clearly unnecessary.
- Runs mandatory dissent.
- Writes `pitches/<YYYY-MM-DD>-<slug>/pitch.md`.
- Records dissent findings and chair outside-check findings in `pitch.md`.

Codex explicit-subagent variant:

```text
$page-one-meeting Use parallel Codex subagents for the editor personas, then have the chair synthesize the meeting.
```

Expected:

- Spawns subagents only because the user explicitly asked.
- Main chair routes all debate prompts.
- Final output remains one coherent `pitch.md`, not raw subagent transcripts.

## Scenario Matrix

| Skill | Harness | Scenario | Expected result |
| --- | --- | --- | --- |
| `critique` | Claude + Codex | Short draft | Reports notes; no file changes. |
| `critique` | Claude + Codex | Long draft | Chunks sensibly; avoids one-agent overload; no edits. |
| `critique` | Claude + Codex | User asks for rewrite | Declines rewrite path and points to `tighten`. |
| `tighten` | Claude + Codex | Draft with frontmatter | Applies safe edits; bumps `updated:`. |
| `tighten` | Claude + Codex | Draft without frontmatter | Applies edits; does not add frontmatter. |
| `tighten` | Claude + Codex | Load-bearing emotional line | Skips flattening edit and reports why. |
| `tighten` | Codex | Read-only workspace | Reports inability to edit; does not claim success. |
| `sharpen` | Claude + Codex | Complete pitch | Gives green/revise/kill verdict; no disk writes. |
| `sharpen` | Claude + Codex | Missing target outlet | Asks only if outlet is necessary; otherwise evaluates outlet-agnostic. |
| `sharpen` | Claude + Codex | Web unavailable | Flags research uncertainty explicitly. |
| `page-one-meeting` | Claude | Native multi-agent path | Uses Claude agents and chair synthesis; writes `pitch.md`. |
| `page-one-meeting` | Codex | Default path | Uses single-thread chair simulation; writes `pitch.md`. |
| `page-one-meeting` | Codex | Explicit parallel path | Uses Codex subagents by request; chair routes debate; writes `pitch.md`. |
| `page-one-meeting` | Claude + Codex | Pitch lacks raw material | Asks for raw material before seating the room. |
| `page-one-meeting` | Claude + Codex | Saturated angle | Mandatory dissent or outside check catches closest existing coverage, or records that novelty could not be ruled out. |
| install | Claude | `draft` only | `critique`/`tighten` work; pitch workflows are unavailable. |
| install | Claude | `pitch` only | `sharpen`/`page-one-meeting` work; draft workflows are unavailable. |
| install | Codex | `draft` only | `$critique`/`$tighten` work; pitch skills are absent or clearly unavailable. |
| install | Codex | `pitch` only | `$sharpen`/`$page-one-meeting` work; draft skills are absent or clearly unavailable. |

## Pass Criteria

A compatibility pass is complete when:

1. Both plugins install in Claude Code from the Claude marketplace path.
2. Both plugins install in Codex from the Codex marketplace path.
3. Each skill has at least one happy-path trace in each harness.
4. Each destructive or write-capable workflow has at least one unhappy-path trace.
5. `critique` and `sharpen` leave the working tree unchanged in their happy paths.
6. `tighten` changes only the intended fixture file in its happy path.
7. `page-one-meeting` writes only under `pitches/<YYYY-MM-DD>-<slug>/`.
8. Codex skills do not require Claude-only runtime terms.
9. Claude skills still preserve their existing native agent behavior.
10. README gives a complete install path for both harnesses.

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
