---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?skeleton"'
min: 1
arm: both
---
The positive half of a matched pair with `trigger-holds-off`. Both prompts are natural
language, and the frontmatter description is the only thing deciding between them.

This one asks for the argument to be worked out and the topic sentences written before any
prose, which is the method by name. It must load.

Note on what this can and cannot test: a `/skeleton` slash command is expanded by the CLI
itself, so it never produces a Skill tool call and always "works" by construction. Asserting
on it would test the harness rather than the skill. Only model-decided loading is observable
here, which is also the only part that can drift when the description gets edited.
