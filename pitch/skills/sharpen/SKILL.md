---
name: sharpen
description: >-
  Runs a pitch through a single managing-editor read instead of the full
  page-one-meeting panel: one Socratic verdict (green light / revise / kill),
  no cast, no debate, no dissent round. Trigger on "sharpen this pitch",
  "sharpen my pitch", "quick editorial read", "give me an editor's take",
  "run this by an editor", or /sharpen. For a full multi-persona debate
  instead, use the page-one-meeting skill.
---

# Sharpen

One editor, one pass. Take whatever pitch material the user gives you — pasted text, a doc,
a raw idea — and launch the `managing-editor` agent (`Agent` tool, `subagent_type:
managing-editor`) with it verbatim, plus the target outlet if the user named one.

Relay the agent's verdict and questions back directly. Don't summarize or soften its voice,
and don't write anything to disk — this is a conversational read, not an artifact.
