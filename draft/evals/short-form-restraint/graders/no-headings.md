---
type: regex
pattern: '^#{1,6} '
flags: m
match: not_contains
target: {source: file, path: post.md}
weight: 1
---
A 200-word LinkedIn post takes no headings. Stage 5 adds them only where a group is real, meaning several paragraphs serving one sub-claim, and four short paragraphs cannot contain one.

This is the suite's only regex grader, and it asserts a character sequence rather than a meaning: does a markdown ATX heading appear in the file. A judge would be worse at this, not better.
