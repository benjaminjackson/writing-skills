# writing-skills

A writing plugin marketplace with two plugins:

- **draft** critiques and tightens prose with a critic built on Deirdre McCloskey's
  *Economical Writing*.
- **pitch** develops and stress-tests story pitches with a managing-editor read or a simulated
  page-one meeting.

The repo supports both Claude Code and Codex. The skills are the source of behavior; host
manifests only make them installable and discoverable.

## Installation

### Claude Code

Inside a Claude Code session:

```text
/plugin marketplace add benjaminjackson/writing-skills
/plugin install draft@writing-skills
/plugin install pitch@writing-skills
/plugin list
```

### Codex

For local development from this checkout:

```bash
codex plugin marketplace add ./.
codex
```

Then open `/plugins`, install `draft` and `pitch`, and confirm the installed skills in
`/skills`.

After this branch is merged upstream, the remote marketplace path is:

```bash
codex plugin marketplace add benjaminjackson/writing-skills
codex
```

## Invocation

| Workflow | Claude Code | Codex |
| --- | --- | --- |
| Read-only prose critique | `/critique path/to/file.md` | `$critique path/to/file.md` |
| Apply prose edits | `/tighten path/to/file.md` | `$tighten path/to/file.md` |
| Single pitch verdict | `/sharpen path/to/pitch.md` | `$sharpen path/to/pitch.md` |
| Page-one pitch meeting | `/page-one-meeting` | `$page-one-meeting` |
| Optional drafting brief | `/page-one-meeting brief` | `$page-one-meeting brief` |

Install `draft` for `critique` and `tighten`. Install `pitch` for `sharpen` and
`page-one-meeting`.

## draft

Prose editing built on Deirdre McCloskey's *Economical Writing*. `critique` and `tighten`
share the same method: Deirdre critiques a draft line by line and at the whole-document level.
`critique` reports the findings without changing files. `tighten` applies the edits.

Claude Code may use the native `editor` agent. Codex reads the shared persona and method
references directly and runs the critique passes in the current thread unless the user
explicitly asks for separate subagents.

### critique

Read-only. Runs the document through Deirdre and reports what she finds. It never edits the
file. Use it when you want a second opinion, not a rewrite.

Examples:

```text
/critique drafts/memo.md
$critique drafts/memo.md
```

### tighten

Applies edits with no approval step. Surgical and substantive fixes both apply as exact
find-and-replace, while edits that flatten emotion or kill deliberate cadence are skipped and
called out in the report.

Examples:

```text
/tighten drafts/memo.md
$tighten drafts/memo.md
```

`tighten` updates valid note frontmatter `updated:` dates when present and reports when
frontmatter is absent or malformed.

## pitch

Editorial workflows for story pitches. `sharpen` gives one managing-editor read.
`page-one-meeting` simulates a multi-persona editorial meeting with mandatory dissent and an
outside novelty/saturation check.

### sharpen

A single editorial pass, not a debate. It uses the managing-editor persona to produce one
verdict: **Green light**, **Revise and resubmit**, or **Kill it**.

Examples:

```text
/sharpen pitches/raw.md
$sharpen pitches/raw.md
```

Claude Code may use the native `managing-editor` agent. Codex reads the shared
`pitch/references/managing-editor.md` reference and performs the single-editor read in the
current thread. When web tools are available and useful, `sharpen` can check novelty,
timeliness, saturation, or factual claims. If web tools are unavailable, it separates the
editorial judgment from unverified novelty or fact claims.

### page-one-meeting

A simulated page-one editorial meeting. A chair convenes 3-5 editor personas suited to the
pitch, synthesizes opening takes, runs one debate round, forces a mandatory dissent round,
performs an outside check, and writes:

```text
pitches/<YYYY-MM-DD>-<slug>/pitch.md
```

Examples:

```text
/page-one-meeting
$page-one-meeting
```

Claude Code may use its native background-agent room. Codex defaults to a chair-led
current-thread simulation so it does not assume hidden subagent fan-out. Codex uses explicit
subagents only when the user asks for parallel agents or separate editor agents.

#### How it works

The chair runs the meeting as a live debate among named personas, not a deterministic script.
In Claude Code, that can use separate agents and chair-to-persona messages when available.
In Codex, the chair keeps the personas' positions separate in the current thread unless the
session exposes a suitable subagent tool and the user asks to use it.

#### The phases

0. **Intake** — read what the pitcher gave, ask only for what's missing and matters most, proceed the moment they signal impatience.
1. **Cast assembly** — pick 3-5 archetypes suited to this pitch's tensions, fresh names each run.
2. **Seating / opening takes** — gather each persona's opening position, then digest those positions for the user.
3. **Open debate** — by default, each persona challenges 1-2 named peers in a single round, then reports a revised position.
4. **Mandatory dissent round** — see below.
5. **Verdict + shaped pitch** — first disk write, `pitches/<YYYY-MM-DD>-<slug>/pitch.md`: verdict and shaped pitch, plus the debate synthesis and dissent findings.
6. **Drafting brief** (optional, argument-gated) — `pitch-brief.md`, one section per persona, each pulling real published analogues.

#### Why the mandatory dissent round exists

Unguided multi-agent debate has a known failure mode: sycophantic conformity, where positions converge and lock in, often by the second exchange. Left unchecked, the room agrees with itself and nothing forces a check on whether that consensus is right — a weak angle or a bad premise can sail through if every persona is built to agree.

So Phase 4 doesn't get skipped, especially when the room looks unanimous. Dissent duty goes to whichever persona moved *most toward* consensus in Phase 3, not the built-in skeptic, who would rehash their existing position. They must argue two things: steelman the case that the pitch is wrong, and name the closest coverage of this angle (or admit they can't rule it out). If they still believe the consensus holds after trying, they say so and name what would change their mind. They record the finding in `pitch.md` either way — not just a gate passed through, but part of the output.

The chair adds one more check in Phase 5. They reread the shaped pitch as a skeptic, independent of what the panel just agreed, before it's finalized.

#### Usage

- **Explicitly:** `/page-one-meeting`, or `/page-one-meeting brief` to jump straight to the drafting brief.
- **Codex:** `$page-one-meeting`, or `$page-one-meeting brief`.
- **Automatically:** on phrases like "page one meeting," "run this by the editors," "simulate a pitch meeting," or "get the room's take."

For a single editorial read instead of a multi-agent debate, use `sharpen`.

## Verification

Static compatibility checks:

```bash
node scripts/check-codex-compat.js
git diff --check
```

Skill validation examples:

```bash
python3 /Users/vicente/.codex/skills/.system/skill-creator/scripts/quick_validate.py draft/skills/critique
python3 /Users/vicente/.codex/skills/.system/skill-creator/scripts/quick_validate.py draft/skills/tighten
python3 /Users/vicente/.codex/skills/.system/skill-creator/scripts/quick_validate.py pitch/skills/sharpen
python3 /Users/vicente/.codex/skills/.system/skill-creator/scripts/quick_validate.py pitch/skills/page-one-meeting
```

Scenario fixtures and trace templates live under `scenarios/`.

## Repo Structure

```text
.claude-plugin/marketplace.json        # Claude marketplace manifest
.agents/plugins/marketplace.json       # Codex marketplace manifest
draft/.claude-plugin/plugin.json       # Claude draft plugin manifest
draft/.codex-plugin/plugin.json        # Codex draft plugin manifest
draft/agents/editor.md                 # Claude editor agent
draft/references/editor-persona.md     # portable Deirdre persona
draft/references/deirdre-method.md     # shared chunking rules and critique prompts
draft/scripts/chunk-markdown.js        # deterministic Markdown chunking fallback
draft/skills/critique/                 # read-only critique skill
draft/skills/tighten/                  # in-place editing skill
pitch/.claude-plugin/plugin.json       # Claude pitch plugin manifest
pitch/.codex-plugin/plugin.json        # Codex pitch plugin manifest
pitch/agents/managing-editor.md        # Claude managing-editor agent
pitch/references/managing-editor.md    # portable managing-editor persona
pitch/skills/sharpen/                  # single-editor pitch read
pitch/skills/page-one-meeting/         # page-one meeting simulation
scenarios/                             # fixtures, snippets, and trace templates
scripts/check-codex-compat.js          # static compatibility checker
```

## Author

Benjamin Jackson ([@benjaminjackson](https://github.com/benjaminjackson))
