---
type: llm
focus: last_message
weight: 2
---
The artifact is a critique of a short post on why a team stopped deploying on Fridays. Three faults were planted in the post on purpose:

1. **Throat-clearing:** "It is important to note that most of our worst outages started on a Friday." The opening phrase says nothing; the sentence should start at "Most".
2. **A doublet:** "each and every deploy". Two words for one idea; "every deploy" says it.
3. **A bare "this":** "This made rollbacks slower." The sentence before it names two things (the release tool batching deploys into one train, and the on-call engineer not knowing which change broke production), so "this" could point at either.

Do not judge whether the critique is good. Do one extraction task:

**For each of the three planted faults, quote the note in the critique that raises it.** A note raises a fault when it points at that phrase or sentence and says what is wrong with it, in any words. A suggested fix that removes the fault counts, for example "cut 'It is important to note that'". A note that only mentions the sentence for some other reason does not count.

Write the three faults as a list. Under each, quote the note, or write NONE.

PASS if all three have a quoted note.
FAIL if any of them is NONE.
