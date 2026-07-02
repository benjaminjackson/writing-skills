---
name: critique
description: >-
  Use this skill whenever someone wants feedback on a piece of writing without
  committing to changing it: essays, emails, board policies, internal docs,
  marketing copy, blog posts, or any prose draft. Trigger on phrases like
  "critique this", "how does this read?", "what's wrong with this", "give me
  notes on this", "review this draft", "does this land", "get me a second
  opinion on this", or "/critique <file>". This is a read-only pass — it never
  edits the file. If the user wants the writing actually fixed, not just
  assessed, use `tighten` instead.
---

# Critique a document

Runs a document through **Deirdre** (the `editor` sub-agent, a critic built on Deirdre
McCloskey's *Economical Writing*) and reports what she finds. This skill only reads and
reports — it never touches the file. For the version that applies the fixes, use `tighten`.

## How it works

See [../../references/deirdre-method.md](../../references/deirdre-method.md) for the full
method: how the `editor` sub-agent works, chunking rules, the critique prompts, and the
surgical/substantive distinction.

## The workflow

1. **Read & chunk.** Read each document, measure tokens with `tks`, and split it into Pass 1
   chunks per the chunking rules in the shared method file.
2. **Pass 1 — line by line.** Launch one `editor` agent per chunk (parallel batches) with the
   granular prompt. Collect the line-by-line notes.
3. **Pass 2 — whole doc.** Launch the holistic pass with the whole-doc prompt.
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
