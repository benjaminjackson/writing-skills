---
type: baseline
baseline_file: fixtures/review-planted-400.md
focus: {source: file, path: draft.md}
weight: 2
---
The baseline is a short post with three faults planted in it on purpose. The produced version is the same post after a line edit.

1. **Throat-clearing:** "It is worth pointing out that most of the time a change spent waiting was spent in review, not in CI."
2. **A doublet:** "any and all review requests".
3. **A bare "this":** "This made the late-day backlog worse." The sentence before it names two things, so "this" could point at either.

For each fault, quote the sentence in the produced version that carries the same content, or write CUT if the content is gone. Then say whether the fault is still there: the opening phrase still in front of the claim, both words of the doublet still side by side, or "this" still standing alone with no noun after it, in any form.

A fix may reword the sentence any way it likes. "The missing afternoon slot made the late-day backlog worse", "That made the late-day backlog worse" with a clear single antecedent, or merging the two sentences all fix fault 3. Only "this" or "that" standing alone where two antecedents compete keeps it.

PASS if none of the three faults is still there.
FAIL if one or more is still there. Name it.
