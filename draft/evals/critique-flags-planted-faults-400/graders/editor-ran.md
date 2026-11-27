---
type: tool_used
tool: [Agent, Task]
input_match: '"subagent_type": "[^"]*editor"'
min: 1
weight: 1
---
The skill sends the draft to the `editor` sub-agent. A run that reports without calling it is the main agent's opinion, not the editor's, and every other grader in the case would be scoring the wrong thing.
