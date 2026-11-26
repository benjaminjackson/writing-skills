---
type: regex
pattern: 'skeleton: settled decisions'
match: not_contains
target: {source: file, path: post.md, raw: true}
weight: 1
---
post.md is seeded with the skill's settled-decisions block, the HTML comment that opens with `<!-- skeleton: settled decisions`, above the approved outline. Finish strips that block before tighten, so the finished file must not contain it anywhere.

`raw: true` makes the runner read post.md as the run left it. Every other file target has the block stripped before a grader sees it, which would hide the one thing this grader checks.

It asserts a character sequence, not a meaning, so it is a regex rather than a judge, and it needs no calibration pair.
