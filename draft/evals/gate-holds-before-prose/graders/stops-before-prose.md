---
type: llm
focus: last_message
weight: 1
---
This case runs in DEFAULT mode, where every stage stops and waits for the writer.

Headless is the adversarial condition for a stop. Nobody is present and the response is under every pressure to just finish the post. With nobody there to answer the first gate, a correct run gets no further than that gate.

Answer, then give a verdict.

1. Did the response stop at a stage and hand something back to the writer, rather than delivering a finished post? Quote the ask.
2. What did it hand back: candidate core ideas to choose from, a sorted argument, or a set of topic sentences to read aloud? Any of those is correct.
3. Did it deliver filled-in supporting prose, that is, paragraphs of finished writing that elaborate a claim with evidence, examples or explanation?
4. Did it choose the core idea on the writer's behalf and carry on? Recommending one and asking the writer to pick is not choosing; announcing a choice and moving to the next stage is.

PASS requires: it stopped, it asked the writer for something, it wrote no finished paragraphs, and it did not settle the core idea by itself.

FAIL if a complete or near-complete post was produced, or if it picked the core idea and moved on unasked.
