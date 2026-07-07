---
name: critique
description: >-
  Use this skill whenever someone wants feedback on a piece of writing without
  committing to changing it: essays, emails, board policies, internal docs,
  marketing copy, blog posts, or any prose draft. Trigger on phrases like
  "critique this", "how does this read?", "what's wrong with this", "give me
  notes on this", "review this draft", "does this land", "get me a second
  opinion on this", or "/critique [file]". This is a read-only pass — it never
  edits the file. If the user wants the writing actually fixed, not just
  assessed, use `tighten` instead.
---

# Critique A Document

Run a document through **Deirdre**, a critic built on Deirdre McCloskey's *Economical
Writing*, and report what she finds. This skill only reads and reports; it never touches the
file. For the version that applies the fixes, use `tighten`.

## How it works

Before starting, read:

- [../../references/editor-persona.md](../../references/editor-persona.md) for Deirdre's voice.
- [../../references/deirdre-method.md](../../references/deirdre-method.md) for chunking,
  critique prompts, host execution rules, and the surgical/substantive distinction.

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
4. **Merge & report.** Combine Pass 1 + Pass 2 findings, dedupe overlaps, and report per below.
   Make no edits, propose none, ask nothing.

## Reporting

- **Open with one line.** "N line notes, M structural. Biggest: <the one that matters most>."
- **Group by severity, not by location.** Lead with the substantive/structural notes (they're
  the ones worth acting on), then the word- and sentence-level notes as a shorter list
  underneath — quote, verdict, fix. This is feedback to read and decide on, not a diff to
  approve, so there's no need for before/after pairs on every line.
- **Name the single change that matters most**, drawn from the Pass 2 pass.
- If most of the notes are minor word-level fixes and the user seems to want them applied, say
  so: "Most of this is safe tightening — run `tighten` and I'll just apply it."

## Guardrails

Read-only. Never edits, sends, posts, or touches anything outside its own report.
