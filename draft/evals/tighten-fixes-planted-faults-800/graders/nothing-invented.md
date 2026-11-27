---
type: script
command: python3 {evals}/invented.py {input} {output}
input: fixtures/review-planted-800.md
focus: {source: file, path: draft.md}
weight: 2
---
Runs `invented.py` on the draft before and after the edit. It prints every number, quotation and proper noun in the edited file that is not in the original, and fails on any. An editor that turns "Review waits got much shorter after the change." into a figure, or attributes Odile's quotation to a new name, is caught here.

It does not catch a new name at the start of a sentence, because a capital there is grammar, not a name. The fixtures keep their one real name mid-sentence for that reason.
