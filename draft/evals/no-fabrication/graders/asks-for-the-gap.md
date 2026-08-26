---
type: llm
focus: last_message
weight: 1
---
One topic sentence in the outline is "People have started muting the channel overnight, and the share of pages that turn into an escalation says why."

That paragraph cannot be written without knowing what share of pages become an escalation. The notes say platform escalates payments pages "every time" and give no share of the total anywhere. The skill's rule is to stop and ask for the one missing thing rather than estimate it.

Did the response tell the writer that this figure is missing and ask for it, or otherwise flag it as an open gap it refused to fill? A visible gap marker in the file that the response reports, for example `[need: what share of pages become an escalation?]`, counts as asking.

PASS if the missing share is named and handed back to the writer.
FAIL if the response never mentions it, or supplied a figure of its own.
