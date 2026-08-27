---
name: sentence-outline-not-labels
tags: [skeleton, fidelity]
runs: 3
max_turns: 16
timeout_seconds: 300
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Skill]
---
/skeleton oncall-notes.md auto

Audience: engineering managers who run an on-call rotation. Goal: they should stop reaching for a rotation change and go look at their runbooks instead. A blog post, about 350 words. Write it as post.md.

Stage 1 is done. The core idea, chosen and signed off: "If your fix for on-call is a schedule change, you are treating a knowledge problem as arithmetic."

Stop after the sentence outline. Do not fill in any supporting prose.
