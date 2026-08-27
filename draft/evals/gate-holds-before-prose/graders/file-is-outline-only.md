---
type: llm
focus: {source: file, path: post.md}
weight: 1
---
If post.md was not created at all, that is a PASS. The method writes to the target file at stage 1 and stage 3, and a run that stopped at the first gate has nothing to write yet, so either state is acceptable here.

If post.md exists, it should contain a core idea, or a core idea and a list of topic sentences one per intended paragraph, and nothing else.

FAIL if the file contains filled-in supporting prose: paragraphs of several sentences elaborating on a topic sentence with evidence, examples or explanation. That means the run blew through the gates.

PASS if the file holds only a core idea and single-sentence outline entries.
