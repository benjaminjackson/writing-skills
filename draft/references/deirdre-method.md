# The Deirdre method

Shared by `tighten` and `critique`. The engine is the **`editor`** sub-agent
(`subagent_type: editor`), Deirdre McCloskey. She has only the `Read` tool and a hard rule
against rewriting — hand her prose to judge, expect a critique back, nothing more.

The one thing that makes or breaks results: **don't overload her.** A fresh agent reading a
paragraph or two gives far sharper line edits than one agent drowning in a whole document. So
chunk, and use a **separate agent per chunk** so each reads with fresh, uncluttered context.

## Chunking: how much to hand Deirdre at once

Size every chunk by token count, measured with `tks` (`cat file.md | tks`, or pipe a slice:
`printf '%s' "$chunk" | tks`). If `tks` is missing, estimate tokens ≈ words × 1.3.

A **block** is one blank-line-separated unit. A whole bulleted or numbered **list counts as
one block**. Skip YAML frontmatter and pure checkbox / fill-in-the-blank form lines (but do
feed Deirdre the prose intros and instructions around them).

**Skip legal language entirely.** Contracts, terms and conditions, warranties, liability
clauses, privacy-policy boilerplate — any legalese embedded in or attached to the document.
Its wording is deliberate and often legally load-bearing; "tighter" can mean "no longer
enforceable." Don't chunk it, don't hand it to Deirdre, don't edit it. Critique or edit the
prose around it (the proposal, the cover letter, the summary) and note in the report that the
legal sections were left untouched. If the *user explicitly asks* for the legal text to be
edited, treat every change to it as substantive and flag rather than apply.

**Pass 1 — line-by-line (section-sized chunks, one fresh agent each):**
- Each chunk is a run of **adjacent blocks packed up to 400 tokens** (aim for 150-400) — keep
  folding in the next block as long as the chunk stays under the ceiling. There's no fixed
  block-count limit: a section with many short blocks (a bulleted list, a run of short
  paragraphs) should still land as a handful of section-sized chunks, not one agent per block.
- A single block over **400 tokens** goes alone.
- A block over **800 tokens** (a long list, or a wall-of-text paragraph) gets split at item or
  sentence boundaries into ≤ 400-token slices. Tell that agent the slice is part of one larger
  block, so it doesn't critique a fragment as if it were the whole thought.
- Tag each chunk with where it sits (e.g. "from the 'Showing up' section") so Deirdre's quotes
  stay locatable in the full file.
- **Sanity-check the chunk count before launching agents:** it should land near
  `document_tokens ÷ 250`. A 2,000-token document should come out to roughly 8 chunks, not 30
  — if your chunking ran fragment-sized instead of section-sized, re-pack it before spinning
  up agents. Over-fragmenting a short document wastes agent calls without sharpening the
  critique; the point of small chunks is to protect a fresh agent from drowning in a *long*
  document, not to atomize a short one.

**Pass 2 — whole-doc (the holistic pass):**
- **Document ≤ 4,000 tokens:** one agent over the **entire document** (pass the file path;
  tell it to skip frontmatter). This is where cross-section repetition, rhythm, and structure
  get caught, so keep it whole whenever you can.
- **Document > 4,000 tokens:** split at top-level `##` headings into chunks of **≤ 3,000
  tokens** each (never split mid-section), one agent per chunk. Then **you** scan across those
  chunks yourself for repetition that spans them, since no single agent saw the whole — hunt
  the same signatures: three-beats, heading-echoes, closing flourishes that only restate.

Run the Pass 1 chunks in parallel batches (about 4-6 agents at a time), then run Pass 2. For
several documents, do this per document.

## The critique prompts

**Granular prompt (Pass 1)** — send the passage inline, delimited:

> Critique this passage against Deirdre McCloskey's *Economical Writing*. It is <LOCATION>
> from a longer document; critique only what is here.
>
> ```
> <PASSAGE>
> ```
>
> Go line by line. Quote the exact phrase at issue, name what's wrong, and say what to do
> (cut / swap / sharpen). Weight toward word- and sentence-level economy: wasted words, weak
> verbs, elegant variation, throat-clearing, "this is / there is" padding, redundant doublets,
> needless qualifiers, actor-hiding passive. If a line is genuinely good, say so and move on.
> For anything you'd cut that carries a distinct idea (not just padding), label it
> **substantive**. Quote exact text so edits can be located.

**Whole-doc prompt (Pass 2):**

> Critique this document against Deirdre McCloskey's *Economical Writing*: `<FILE_PATH>` (skip
> the YAML frontmatter). Step back and judge it as a whole: economy, structure, rhythm, and
> especially repetition across sections, anything only visible at the whole-document level.
> Hunt the claim → elaborate → summarize three-beat, heading-echoes (a first sentence that
> restates its section title), and closing flourishes that only restate the section. Quote
> each sentence or clause you would cut entirely and say why — and flag the load-bearing
> lines that must NOT be cut. You don't need to re-flag every small word fix; another pass
> handles those. Name the few cross-cutting problems and the single change that matters most.
> Flag each as surgical or substantive.

## Surgical vs substantive

This is the line that keeps meaning intact.

**Surgical (preserves all meaning):**
- Cut throat-clearing and "this is / there is" padding.
- Weak verb → strong; Latinate → Saxon (utilize→use, prior to→before).
- Kill intensifiers and hedges (very, really, genuinely, completely, quite).
- Passive → active when the actor is known.
- Collapse a doublet or elegant variation to one word.
- Trim a sentence or clause whose idea already lives elsewhere in the piece — a **verbatim or
  semantic duplicate**. The recurring signatures: a **heading-echo** (a first sentence that
  restates its section title), a **closing flourish** that only restates the section, and
  **beat three** of a claim → elaborate → summarize run. The test: the cut is surgical because
  the idea survives in the other spot — no meaning is lost. Check the emotional/cadence guard
  and the keep-list (Reading rules) first: a closer that restates but lands the feeling, the
  rhythm, or is the section's one line with teeth is the payload, not a duplicate. When it
  isn't clearly a duplicate, treat it as substantive.

**Substantive (changes what it says or its shape):**
- Delete a numbered or bulleted list item.
- Merge or remove a section.
- Cut a sentence or clause that carries a **distinct idea**.
- Cut an example or illustration that adds concreteness the abstract sentence lacks. It is not
  a semantic duplicate — cutting it removes something. Trimming an example stack to one (or
  examples plus summary → keep one) is the canonical purpose-gated call (see "read the
  document's purpose").
- Reduce a phrase repeated for emphasis across sections.
- Any restructure.

## Reading rules

- **Meaning first, economy second.** When a cut would change what a sentence means, it's
  substantive, not surgical.
- **Exact find-and-replace.** Match the text precisely; change only what the note calls for.
- **Don't sand off lines doing real work.** Warmth, a turn of phrase, a deliberate repetition
  that lands. Deirdre will tell you when something is genuinely good. Keep it.
- **Respect a project voice guide, if one exists.** Before editing, check the target project
  for a style/voice guide (e.g. `docs/voice-and-tone.md`, `STYLE.md`, a section in
  `CLAUDE.md`). If one exists, also enforce its mechanicals (things like em-dash rules or a
  house cadence) on the documents it covers. If no such guide exists, skip this step.
- **Read the document's purpose before deciding how hard to cut.** Semantic duplicates go
  regardless — the idea survives elsewhere. But concreteness-for-brevity cuts (trimming an
  example stack to one, pruning elaboration that is dispensable but not redundant) depend on
  whether the reader will *use* this document or *study* it. Reference doc, one-pager, or an
  explicit "make it punchy": cut hard. Manifesto, speech, narrative, marketing where the last
  line is the payload: preserve rhythm and deliberate repetition. Whatever the purpose, never
  trim past the **keep-list**: a concrete list that gives an abstraction meaning, the one line
  with teeth in a section, the sharpest concrete image, and defined terms or real
  distinctions all stay.
- **Economy is not the only axis: protect the emotional and rhythmic lines.** Deirdre
  optimizes for economy and concreteness, and a meaning-drift edit *looks* surgical: one local
  word, clearly tighter. But often the warmest line in a piece is the one she clips, because
  the colder version is always more concrete. Two tells that an economy edit has crossed a
  line it shouldn't: (1) it **flattens a feeling into a fact** ("the fear that no one would
  notice if she disappeared" → "she thought no one would notice if she disappeared" loses the
  dread the frame carries); (2) it **shortens a sentence that was deliberately building to its
  final word** (some lines land *because* they end on the heavy word, and cutting them to the
  bone kills the landing). Never make either kind of edit — flag it instead of applying or
  proposing it. When a line carries the document's emotional thesis or a deliberate cadence,
  name it to Deirdre up front so she knows it's load-bearing.
