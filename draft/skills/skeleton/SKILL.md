---
name: skeleton
description: >-
  Build a piece of writing from the inside out: core idea first, then every
  topic sentence, then the joints between them, then headings, and only then
  the supporting prose. For essays, blog posts, memos, talks, long emails,
  anything where the argument has to hold. Works from nothing, from a pile of
  notes, or from an existing draft whose argument has come loose. Invoke
  explicitly as `/skeleton [file-or-notes] [auto]`, or when the user asks
  in their own words to "build the skeleton", "outline this properly", "work
  out the argument first", "write the topic sentences first", "reverse outline
  this", or "restructure this piece". Do NOT load this on a plain "write me a
  blog post" or "draft an email"; the six stages are a choice the writer makes,
  not a default. For prose whose argument is sound and whose words are fat, use
  `tighten`. For notes on a draft without changing it, use `critique`.
---

# Build a draft from the inside out

Most bad writing is not badly worded. It is well-worded paragraphs in an order that does not
add up, and by the time you can see that, fixing it means a rewrite. So this skill refuses to
write a single supporting sentence until the argument survives being read aloud on its own.

The method has real names behind it. Stage 3 is a **sentence outline** (Chicago and MLA both
distinguish it from a topic outline: every entry is a full sentence, not a noun phrase). The
core-idea-first shape with grouped support beneath it is Barbara Minto's **Pyramid Principle**.
Reading the topic sentences alone to test the argument is Joseph Williams' **reverse outline**
from *Style*, run before the prose exists instead of after.

## Before anything: the brief

Get four things, and write them down verbatim. Every `editor` call quotes them.

1. **Who reads this**, and what they already know. Ask what else they have in hand: a report
   they paid for, an earlier memo, a thread. Name what this piece must not re-explain and what
   it must not contradict.
2. **What they should think or do** after reading.
3. **What it is**: essay, memo, post, talk, email. Roughly how long.
4. **How it should sound.** One sentence, best given as a comparison: "like explaining it to a
   CEO friend over coffee", "like a technical memo to peers". Contractions or not. And who the
   writer is to the reader: peer, advisor, teacher, supplicant.

If the user gave all four, do not ask. If any is missing, one `AskUserQuestion`, then stop
asking. Audience and register are the two only the writer holds, and getting either wrong means
every paragraph written before the correction gets written a second time.

## Where you are starting from

Three entry points. They change stages 1 to 3 only; stages 4 to 6 are the same either way.

**From nothing.** Stage 1 is a conversation. Ask what they are trying to say, then propose
candidate claims back.

**From notes.** Read the notes first. Stage 1 proposes core ideas drawn from what is actually
there, quoted. Stage 2 sorts the notes under the claims. Notes that fit no claim get named out
loud and set aside, not smuggled into a paragraph because they were written down once. Say
which notes went unused and why.

**From an existing draft.** Pull the real topic sentences out of it, one per paragraph, and
read those alone. That is the reverse outline in its original form, and it shows the argument
the draft actually makes against the one the writer meant. Then run stages 3 to 6 on the
result, treating the old paragraphs as raw material to fill from. Before starting, check this
is the right skill: if the argument holds and only the prose is fat, that is `tighten`.

Harvest before you restructure. List the passages that are finished and reusable as they
stand, quote them, and hold them aside. Report them at the stage 3 gate. A restructure that
silently drops working paragraphs costs the writer more than the bad order did. This is the
mirror of naming the unused notes: same rule, opposite direction.

## The working file

Stage 1 writes the core idea as the first line of the target file. Stage 3 writes the topic
sentences into that same file, one per line with a blank line between. Every later stage edits
it in place. The outline becomes the draft; there is no copy step and no scratch file. If the
user did not name a file, propose a path and get agreement before writing.

## The six stages

### 1. The core idea

One sentence, and it must be a claim someone can disagree with.

The test: negate it. If the negation is absurd or says nothing, what you have is a topic, not a
claim. "What benchmarks measure" is a topic. "Benchmarks measure what is easy to score, not
what is useful" is a claim, because someone can argue the opposite.

Propose two or three candidates. The writer picks one or writes their own. Never proceed on a
core idea you chose for them.

### 2. The argument

List what has to be true for the core idea to hold, and what each of those needs to stand up:
evidence, an example, a concession. Group them where they serve the same sub-claim.

This stage produces the paragraphs. It does not produce their sentences.

### 3. The sentence outline

Write every topic sentence. Full sentence, subject and verb, making a claim. A noun phrase is
not a topic sentence, and this stage exists to enforce the difference: "Cost problems" is a
label, "The cost only appears at the second month of use" is a claim you can check.

Then read them alone, in order, out loud, with nothing else in front of you. The writer does
this, not you. It has to be read aloud by the person whose argument it is, which is why this
stage stops and waits.

Reorder until the reasoning holds. Reordering costs nothing now and costs a rewrite later.

Every topic sentence has to be a claim the material can carry. Inventing one here is cheaper to
do and harder to see than inventing a sentence at stage 6, because an outline entry looks like a
plan rather than a claim, and it arrives with no evidence attached for the writer to check
against. If the argument needs a step the material does not support, say so and ask. Do not write
the step and hope.

### 4. The joints

For each adjacent pair, name the relation in one word: so, but, and, therefore, except. If no
relation is there, the order is wrong, and you go back to stage 3.

Fix by rewriting the following topic sentence first. Add a transition sentence to the previous
paragraph only when a rewrite cannot carry the relation. Prefer the fix that adds no words.

Bolted-on connectives are the tell that the relation is not real: "Furthermore", "Building on
this", "Importantly", "That said" used as filler. If a sentence needs one of those to connect,
it is not connected.

### 5. Groups and headings

Add headings only where a group is real: several paragraphs serving one sub-claim. Three
paragraphs and a heading over each is not structure, it is decoration. Give the piece a title as
well as its sections; stage 5 is the only place it gets one.

**The standalone test.** Read the title and the headings alone, in order, with nothing else in
front of you. They have to make sense to someone who reads only those. A heading that needs its
paragraph to be understood is a label for you, not a signpost for the reader.

A heading that restates its first topic sentence is a heading-echo, which
[../../references/deirdre-method.md](../../references/deirdre-method.md) already hunts. Cut the
heading or rewrite the sentence, not both.

### 6. Fill in

The topic sentence stays as written. Supporting sentences carry evidence, an example, the
mechanism, or a concession. Never a restatement.

**A topic sentence is not always a paragraph.** If it has one sentence of evidence behind it and
no more, it belongs inside its neighbour's paragraph. Merge the two and say you did. That is a
normal outcome, not a fault in stage 3, and it does not send you backwards.

No summarising beat at the end of a paragraph. The topic sentence already said it. This is
where the claim, elaborate, summarise three-beat gets born, and here is where it is cheapest to
refuse it.

**Never invent material.** No evidence, number, quotation, anecdote, or example that the writer
did not supply. Where the material runs out, stop and ask for that one thing, then carry on. An
invented example in someone else's voice is the hardest error for them to catch reading back,
and a flagged invention that reads well tends to survive to publication.

When the evidence lives in files rather than in the writer's head, this covers arithmetic. Every
number goes back to the file it came from before it is written down. A count that is close and
stated with confidence is the same error as an invented quotation and much harder to see.

If filling in proves a topic sentence wrong, go back to stage 3 and read the spine aloud again.
That is the only backward path, and it is a normal thing to happen.

### Then read it back

Two passes over the filled-in prose. Both are mechanical, both run without a gate, and both go
before the editor sees anything.

**The joints, again.** Stage 4 named the relation between topic sentences. Now the joint that
matters has moved: read the last sentence of each paragraph against the topic sentence of the
next. If the last sentence only closes its own paragraph, it is a summarising beat wearing a
transition's clothes. Cut it. This is the no-restatement rule in the one form you can check.

**Is this helpful, and why?** Ask it of every sentence that carries a claim, and answer it. Then
ask whether the sentence could describe three different situations. If it could, it names a
category instead of a thing: "gated by", "at your altitude", "point the platform". Rewrite until
it can only mean one thing. Name the specific thing and say what it does.

Run the same check on the evidence, where it shows up as overclaiming. "Half the names on your
list sit in the wrong group" is a sentence you either counted or you did not.

## Gates

**By default, every stage stops.** Show what the stage produced, then wait. This is the writer's
argument being made visible, and the whole method is worth nothing if they only see the end.

**With `auto`, two stages stop:** stage 1 (the core idea) and stage 3 (the sentence outline).
Both are places where a wrong answer cannot be recovered later and where only the writer holds
the information. Stages 2, 4, 5 and 6 show their work and carry on; the writer can interrupt.

Stage 6's request for missing material is not a gate, it is a question, and it happens in both
modes.

**No stage before 6 writes a supporting sentence.** Stages 2 to 5 sort, order, group and label.
The pull toward prose is strongest where there is nothing finished to show yet, and a
paragraph drafted at stage 2 is a paragraph the writer never got to steer.

**A gate shows what its own stage produced and nothing from the next one.** Recommending one of
the candidate core ideas is stage 1. Saying which paragraph it becomes, or which of the others
survives as a concession, is stage 2, and stage 2 waits. Doing the next stage inside the current
stage's message is how a gate leaks while still looking like it held.

## The two checks

### sloplint, at every stage

```
cat FILE | sloplint check --markdown -o json -
```

Exit 0 is clean, 1 means notes were found. Fix the notes before moving on. These are mechanical
tells, so apply them without asking. Running it on a bare topic-sentence outline is worth more
than running it on two thousand finished words, because a tell in a topic sentence gets
elaborated into a whole paragraph of the same.

### The editor agent, at stages 1, 3 and 6

Launch `draft:editor` (Deirdre McCloskey, critique only, she will not rewrite). She runs where a
critic has something to judge: the claim, the argument line, and the finished prose. Stages 2, 4
and 5 are sorting and labelling, and there is nothing there for her.

**Apply her notes yourself, in one round, and show the result at the stage gate.** Do not relay
her critique note by note for approval. Say what changed and what you refused, in a line or two.

**If she does not report, do not stall.** Run the critique yourself against the targets named in
the prompt and say the method changed. If her notes arrive late, re-read the file before applying
any of them: the file has moved, part of what she found is already fixed, and the rest was
computed against a version that no longer exists.

Every prompt quotes the brief, the register and the core idea, says plainly that what follows is
a draft to critique, and names what not to judge at that stage.

**Stage 1** (send the candidate claims inline):

> Audience: <BRIEF>. Goal: <GOAL>. Register: <REGISTER>. These are candidate core ideas for that piece, and they are
> a draft to critique. For each: is it a claim a reader can disagree with, or a topic wearing a
> claim's clothes? Which is sharpest for this audience, and what is it missing? Do not write a
> replacement piece; judge these sentences.

**Stage 3** (send the topic sentences in order, nothing else):

> Audience: <BRIEF>. Goal: <GOAL>. Register: <REGISTER>. Core idea: <CORE IDEA>. What follows is the complete set of
> topic sentences for the piece, in order, one per paragraph, and it is a draft to critique.
> Read them as an argument. Does it hold? Name the step that is missing, the sentence that is
> out of order, the one that is a noun phrase pretending to be a claim, and the one that does
> not support the core idea. Do not line-edit for word economy; the words change when the
> paragraphs get written.

**Stage 6** (pass the file path):

> Audience: <BRIEF>. Goal: <GOAL>. Register: <REGISTER>. Core idea: <CORE IDEA>. Critique this draft: `<FILE_PATH>`.
> Every paragraph opens with a topic sentence that was fixed before the prose was written.
> Judge whether the prose serves it: which paragraphs only restate their opening sentence, where
> the claim, elaborate, summarise three-beat appears, and where the prose drifts off the claim it
> is meant to carry. Hunt restatement at three scales: inside one paragraph, across two adjacent
> paragraphs, and a section's opening claim against its closing line. Judge the register too:
> where does this sound like something other than <REGISTER>. This is not the economy pass;
> another one handles that.

## Finish

First, reconcile the counts. List every number in the document and check that a reader can see
how they relate. Thirteen people, fourteen organisations and ten recommendations can each be true
and still leave the reader unable to draw the picture.

Then run `draft:tighten` on the file. That is the full chunked Deirdre pass, the right tool once,
on prose, and the wrong tool six times, on an outline.

## Reporting

- **At each gate, show the artefact, not a description of it.** The candidate claims. The topic
  sentences in order. The paragraph that just got filled in. One line on what changed since the
  last stage.
- **Say what the editor changed and what you refused.** A line or two, not her full critique.
- **Name the unused notes.** When working from notes, say which ones fit no claim and were set
  aside. The writer decides whether that is right.
- **Name what you harvested.** When working from an existing draft, quote the passages you kept
  unchanged, and say which ones you dropped.
- **List the gaps.** At the end, every place the material ran out and what is still needed.
- **Close with the spine.** The final topic sentences in order, so the writer sees the argument
  the piece ended up making.

## Guardrails

Never invents evidence, numbers, quotations, anecdotes, or examples; it asks for the one thing
missing and waits. Never chooses the core idea for the writer, and never fills in prose before
the sentence outline has been read aloud and approved by them. Writes and edits the target file
directly. Never sends, posts, or touches anything outside the local file it is given. No em
dashes or en dashes in the file it writes or the messages it sends.
