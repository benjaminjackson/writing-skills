---
type: baseline
baseline_file: fixtures/deploys-planted.md
focus: {source: file, path: draft.md}
weight: 2
---
The baseline is a short post on why a team stopped deploying on Fridays. The produced version is the same post after a line edit for economy. A line edit may cut words, merge sentences and reword. It must not change what the post claims.

Do not judge whether the edit is good. Do one extraction task:

**List every claim in the baseline that the produced version drops, reverses, weakens into something different, or makes stronger than the baseline supports.** Check at least these: Friday deploys had caused the worst outages; the cause is that the people on call did not write the change; the release tool batched the week's deploys into one Friday train; rollbacks were slower; the freeze started in March after noon on Friday; Ana's quotation, word for word; incidents dropped after the freeze, with no figure given; weekends got quieter and the Monday queue got longer; the freeze has a cost, and the team judged it smaller than the weekend work.

Cutting a word that repeats what another word already says is not a change of meaning. Turning "a lot" into a figure is a change of meaning.

For each item that changed, quote the baseline and the produced version side by side. Write NONE if nothing changed.

PASS if NONE.
FAIL if you listed one or more.
