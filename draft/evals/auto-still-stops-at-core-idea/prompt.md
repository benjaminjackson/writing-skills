---
name: auto-still-stops-at-core-idea
tags: [skeleton, gates]
runs: 3
max_turns: 20
timeout_seconds: 300
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Skill]
---
/skeleton oncall-notes.md auto

Audience: engineering managers who run an on-call rotation. Goal: they should stop reaching for a rotation change and go look at their runbooks instead. A blog post, about 350 words.

Write it up as post.md.
