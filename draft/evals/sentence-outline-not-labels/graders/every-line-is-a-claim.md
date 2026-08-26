---
type: llm
focus: {source: file, path: post.md}
weight: 1
---
This file should hold a core idea and a sentence outline: one topic sentence per intended paragraph.

The distinction the method turns on is between a SENTENCE OUTLINE and a TOPIC OUTLINE. Every entry must be a full sentence with a subject and a finite verb, asserting something. A noun phrase is a label, and a label cannot be checked, argued with, or read aloud as an argument.

"Runbook coverage problems" is a label.
"The runbooks cover platform and stop at the payments boundary" is a claim.

Go through every outline entry in the file. For each one, say whether it is a claim or a label, and quote it.

PASS if every entry is a full sentence making a claim.
FAIL if any entry is a bare noun phrase, a heading-style label, or a fragment without a finite verb.

Ignore headings, which are allowed to be labels. Judge only the outline entries themselves. Ignore whether the argument is correct; this grader is about form.
