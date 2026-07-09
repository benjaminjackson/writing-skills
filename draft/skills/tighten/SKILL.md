---
name: tighten
description: >-
  Use this skill whenever someone hands you a piece of writing and wants it
  actually fixed: tightened, cut for economy, given a rigorous line edit.
  Essays, emails, board policies, internal docs, marketing copy, blog posts,
  or any prose draft. Applies every edit automatically, no approval step —
  the right call whenever the ask is "just make this better" and the user
  doesn't want to review each change. Trigger on phrases like "tighten this",
  "clean this up", "fix this", "edit this for economy", "make this leaner",
  "cut the fluff from this doc", "give this a line edit and apply it", "this
  feels bloated, fix it", or "/tighten [file]". Works on a single document or
  a batch in one run: several board policies, a folder of drafts, a stack of
  emails. If the user wants feedback without the file being changed, use
  `critique` instead. Don't reach for this when the request is to write
  something new, brainstorm, or restructure unprompted; it edits prose that
  already exists, it doesn't ghostwrite.
---

# Tighten A Document

This skill takes a document, runs it through **Deirdre**, a critic built on Deirdre
McCloskey's *Economical Writing*, and applies the edits - surgical and substantive alike -
with no approval step. If the user wants a review instead of a rewrite, that's `critique`, not
this.

The prime directive: **preserve all original meaning. Tighten the words, not the message.**
Deirdre only critiques; she refuses to rewrite. So the flow is: she finds what's fat, weak, or
repetitive; **you** (the agent running this skill) make the edits, carefully, as exact
find-and-replace, then apply them without stopping to ask.

## How it works

Before starting, read:

- [../../references/editor-persona.md](../../references/editor-persona.md) for Deirdre's voice.
- [../../references/deirdre-method.md](../../references/deirdre-method.md) for chunking,
  critique prompts, host execution rules, and the surgical/substantive distinction.

Everything below is specific to `tighten`'s no-approval apply step.

## The workflow

1. **Read and chunk.** Read each document. For long or non-trivial Markdown, run
   `node draft/scripts/chunk-markdown.js <file.md>` from the repository root and use its Pass 1
   and Pass 2 chunk plan. If you cannot run the script, follow the chunking rules in the shared
   method file manually.
2. **Pass 1 - line by line.** Run one isolated Deirdre critique per Pass 1 chunk with the
   granular prompt. Claude may use the native `editor` agent. Codex should perform the passes
   sequentially in the main thread unless the user explicitly asks for parallel subagents.
3. **Pass 2 - whole doc.** Run the holistic pass with the whole-doc prompt or Pass 2 chunk
   plan from the chunker.
4. **Triage.** Merge Pass 1 + Pass 2 findings, dedupe overlaps, and sort each into surgical or
   substantive per the shared method file.
5. **Apply everything.** Make every surgical and substantive edit via exact find-and-replace.
   The one exception: an edit that flattens emotional meaning or kills a deliberate cadence
   (see "protect the emotional and rhythmic lines" in the shared method file) — skip that one
   and note it in the report instead of applying it. Nothing else waits for approval; this
   skill never asks, it applies.
6. **Bump `updated:`.** For any edited file that has valid note frontmatter, set `updated:` to
   today (`MM-DD-YYYY`). Skip files without frontmatter or with malformed frontmatter, and say
   so in the report.
7. **Report.** Present findings per **Reporting** below. There's nothing left to approve —
   this is a summary of what changed, not a request for sign-off.

## Reporting

- **Open with one line.** "N safe tightenings, M structural changes applied." That's the whole
  run at a glance.
- **Collapse the surgical.** Don't show every before→after. Give the count and the **rewritten
  final paragraphs**, so the user eyeballs the clean result instead of diffing each word.
- **Spotlight the substantive.** These already happened, but they're the ones worth a second
  look — number each, show before→after, and say why it was safe to apply.
- **Call out anything skipped.** If an edit was held back for flattening emotion or killing a
  cadence, name it and say why, so the user knows it wasn't missed, it was a judgment call.

## Guardrails

Preserves all original meaning, with one named exception path (skip, don't apply, edits that
flatten emotion or kill a deliberate cadence). Editing local markdown is automatic in this
project. Claude should use its normal edit tool. Codex should use `apply_patch` for manual
edits. This skill always applies its edits, both surgical and substantive, with no approval
step and no asking first. Never sends, posts, or touches anything outside the local file(s)
it's given.
