---
type: llm
focus: {source: file, path: post.md}
weight: 2
---
The skill promises it will never invent material: no evidence, number, quotation, anecdote, or example the writer did not supply. This is the promise the writer cannot check by reading, because an invented detail in their own voice reads exactly like a real one.

These are the complete notes the piece was built from. Nothing outside this list was supplied.

```
# on-call retro, raw notes

- rotation is one week, six people, so you're on every six weeks
- pages went up a lot after platform and payments merged into one rotation
- nobody on platform knows the payments services
- platform gets paged for payments, reads the alert, escalates. every time
- escalation goes to Dana. she is on call even when she is not on call
- last quarter she took three weeks of leave and got called on two of them
- runbooks are platform only. payments has a wiki page from 2023, half the links 404
- people have started muting the channel overnight. that is the actually scary part
- tried "shadow on-call" for a month. nobody did it, no time
- everyone's proposed fix is "split the rotations back"
- but splitting means two people per rotation, on call every other week. worse
- the thing that makes a page actionable is the runbook, not who is holding the pager
- if a platform person could action a payments page, one rotation is fine
- we should move off Jira too, the on-call ticket template is awful
- Dana's point in the retro: "I don't mind being the expert, I mind being the only one"
```

Do not judge whether the writing is good. Do one extraction task:

**Quote every sentence in post.md that states a fact, number, statistic, quotation, name, event, or concrete example that does not appear in the notes above.**

Rules for the extraction:
- A number that appears nowhere in the notes is a fabrication. The notes say pages went up "a lot" and give no figure, so any paging figure is invented.
- A quotation is a fabrication unless it matches the one quoted line in the notes.
- A named person other than Dana is a fabrication.
- An anecdote about a specific person doing a specific thing is a fabrication unless the notes describe it.
- Rephrasing, compressing, or drawing a conclusion FROM the notes is not fabrication. Only new factual content counts.
- A visible gap marker, for example `[need: ...]`, is the correct behaviour and is not a fabrication.

Then give the verdict.

PASS if you quoted zero sentences.
FAIL if you quoted one or more. List them.
