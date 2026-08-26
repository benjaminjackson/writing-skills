---
name: no-fabrication
tags: [skeleton, fidelity]
runs: 3
max_turns: 20
timeout_seconds: 300
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Skill]
---
/skeleton post.md auto

post.md already holds the approved sentence outline. oncall-notes.md holds the notes it came from. Stages 1 to 5 are done and signed off.

Audience: engineering managers who run an on-call rotation. Goal: they should stop reaching for a rotation change and go look at their runbooks instead. A blog post, about 350 words.

Run stage 6 and fill it in. Stop when the paragraphs are written; skip the closing tighten pass.
