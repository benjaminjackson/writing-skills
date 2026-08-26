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

Get three things, and write them down verbatim. Every `editor` call quotes them.

1. **Who reads this**, and what they already know.
2. **What they should think or do** after reading.
3. **What it is**: essay, memo, post, talk, email. Roughly how long.

If the user gave all three, do not ask. If any is missing, one `AskUserQuestion`, then stop
asking. Guessing the audience of an essay wrecks every stage downstream, so this is the one
thing worth interrupting for.

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
paragraphs and a heading over each is not structure, it is decoration.

A heading that restates its first topic sentence is a heading-echo, which
[../../references/deirdre-method.md](../../references/deirdre-method.md) already hunts. Cut the
heading or rewrite the sentence, not both.

### 6. Fill in

The topic sentence stays as written. Supporting sentences carry evidence, an example, the
mechanism, or a concession. Never a restatement.

No summarising beat at the end of a paragraph. The topic sentence already said it. This is
where the claim, elaborate, summarise three-beat gets born, and here is where it is cheapest to
refuse it.

**Never invent material.** No evidence, number, quotation, anecdote, or example that the writer
did not supply. Where the material runs out, stop and ask for that one thing, then carry on. An
invented example in someone else's voice is the hardest error for them to catch reading back,
and a flagged invention that reads well tends to survive to publication.

If filling in proves a topic sentence wrong, go back to stage 3 and read the spine aloud again.
That is the only backward path, and it is a normal thing to happen.

## Gates

**By default, every stage stops.** Show what the stage produced, then wait. This is the writer's
argument being made visible, and the whole method is worth nothing if they only see the end.

**With `auto`, two stages stop:** stage 1 (the core idea) and stage 3 (the sentence outline).
Both are places where a wrong answer cannot be recovered later and where only the writer holds
the information. Stages 2, 4, 5 and 6 show their work and carry on; the writer can interrupt.

Stage 6's request for missing material is not a gate, it is a question, and it happens in both
modes.

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

Every prompt quotes the brief and the core idea, says plainly that what follows is a draft to
critique, and names what not to judge at that stage.

**Stage 1** (send the candidate claims inline):

> Audience: <BRIEF>. Goal: <GOAL>. These are candidate core ideas for that piece, and they are
> a draft to critique. For each: is it a claim a reader can disagree with, or a topic wearing a
> claim's clothes? Which is sharpest for this audience, and what is it missing? Do not write a
> replacement piece; judge these sentences.

**Stage 3** (send the topic sentences in order, nothing else):

> Audience: <BRIEF>. Goal: <GOAL>. Core idea: <CORE IDEA>. What follows is the complete set of
> topic sentences for the piece, in order, one per paragraph, and it is a draft to critique.
> Read them as an argument. Does it hold? Name the step that is missing, the sentence that is
> out of order, the one that is a noun phrase pretending to be a claim, and the one that does
> not support the core idea. Do not line-edit for word economy; the words change when the
> paragraphs get written.

**Stage 6** (pass the file path):

> Audience: <BRIEF>. Goal: <GOAL>. Core idea: <CORE IDEA>. Critique this draft: `<FILE_PATH>`.
> Every paragraph opens with a topic sentence that was fixed before the prose was written.
> Judge whether the prose serves it: which paragraphs only restate their opening sentence, where
> the claim, elaborate, summarise three-beat appears, and where the prose drifts off the claim it
> is meant to carry. This is not the economy pass; another one handles that.

## Finish

Run `draft:tighten` on the file. That is the full chunked Deirdre pass, the right tool once, on
prose, and the wrong tool six times, on an outline.

## Reporting

- **At each gate, show the artefact, not a description of it.** The candidate claims. The topic
  sentences in order. The paragraph that just got filled in. One line on what changed since the
  last stage.
- **Say what the editor changed and what you refused.** A line or two, not her full critique.
- **Name the unused notes.** When working from notes, say which ones fit no claim and were set
  aside. The writer decides whether that is right.
- **List the gaps.** At the end, every place the material ran out and what is still needed.
- **Close with the spine.** The final topic sentences in order, so the writer sees the argument
  the piece ended up making.

## Guardrails

Never invents evidence, numbers, quotations, anecdotes, or examples; it asks for the one thing
missing and waits. Never chooses the core idea for the writer, and never fills in prose before
the sentence outline has been read aloud and approved by them. Writes and edits the target file
directly. Never sends, posts, or touches anything outside the local file it is given. No em
dashes or en dashes in the file it writes or the messages it sends.
