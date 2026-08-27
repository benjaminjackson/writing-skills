---
name: reorders-the-spine
tags: [skeleton, fidelity]
runs: 3
max_turns: 20
timeout_seconds: 300
allowed_tools: [Read, Write, Edit, Glob, Grep, Bash, Skill]
---
/skeleton standups-draft.md auto

This draft exists already. Audience: engineering managers thinking about dropping their standup. Goal: they should see the argument for it, not just the anecdote. A blog post, about 350 words.

Stage 1 is done. The core idea, chosen and signed off: "You can drop your standup safely, because the jobs it does are each done better as they come up than at a fixed hour every morning."

Reverse outline it and fix what the outline shows. Write the corrected topic sentences into standups-draft.md and stop there; do not fill in the paragraphs.
