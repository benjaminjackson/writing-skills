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

One editor, one pass. Take whatever pitch material the user gives you - pasted text, a file,
or a raw idea - and run one managing-editor read against it.

Before starting, read [../../references/managing-editor.md](../../references/managing-editor.md)
for the editor persona, verdict vocabulary, and outlet-adaptation rules.

## Workflow

1. **Collect the pitch.** Use pasted text as-is, or read the named file. If the user gives only
   a raw idea, evaluate the idea but flag missing pitch details. If critical information is
   missing and the user appears to want a full outlet-specific verdict, ask one concise
   clarifying question; otherwise proceed outlet-agnostic and name the gaps.
2. **Identify the target outlet.** If the user names one, apply the outlet weighting in the
   managing-editor reference. If none is named, use universal editorial standards.
3. **Check novelty only when tools are available and useful.** If the host exposes web search
   or fetch tools and the pitch depends on novelty, saturation, timeliness, or factual claims,
   run a small targeted check. Name the searches or sources used. If web tools are unavailable,
   do not pretend to have checked the market; separate editorial judgment from unverified
   novelty or factual claims.
4. **Give one verdict.** Use exactly one of: **Green light**, **Revise and resubmit**, or
   **Kill it**. Explain the reasoning through the managing-editor framework.
5. **Return questions and next moves.** Ask only the questions needed to improve the pitch or
   make the next editorial decision.

## Host Behavior

- **Claude Code:** May use the native `pitch/agents/managing-editor.md` agent when available,
  passing the pitch, target outlet, and any web-check findings.
- **Codex:** Read the managing-editor reference and perform the single-editor read in the
  current thread. Do not spawn hidden subagents for `sharpen`.
- **Any host:** Do not write files. This is a conversational read, not an artifact.

Relay the editor's verdict and questions directly. Do not summarize or soften its voice.
