# writing-skills

A Claude Code plugin marketplace with three plugins: **draft**, which critiques and tightens prose with a critic built on Deirdre McCloskey's *Economical Writing*; **pitch**, which develops and stress-tests story pitches; and **documentation**, which writes technical docs that don't waste the reader's time.

## Installation

```
claude plugin marketplace add benjaminjackson/writing-skills
claude plugin install draft@writing-skills
claude plugin install pitch@writing-skills
claude plugin install documentation@writing-skills
```

## draft

Prose editing built on Deirdre McCloskey's *Economical Writing*. One agent, two skills: **editor** is a critic that judges prose against McCloskey's standards and refuses to rewrite it; **critique** and **tighten** both run a document through editor and share the same chunking engine — one just reports the findings, the other applies them.

### editor

`editor` (agent, `subagent_type: editor`, model: opus, tools: `Read`) is Deirdre McCloskey herself — economist, rhetorician, author of *Economical Writing*. Handed a draft, she hunts for fat, throat-clearing, hedges, elegant variation, passive voice that hides who did what, vague abstractions, and cleverness for its own sake. She goes line by line, quotes the offending phrase, names what's wrong, and says what to do: cut, swap, or sharpen.

She has one hard rule: she critiques, she doesn't rewrite. Hand her a request to write or edit prose and she declines and asks for the draft instead.

### How it works

editor works best reading a paragraph or two with uncluttered context, so neither skill hands it a whole document at once. Instead each runs editor in two passes: a line-by-line pass, with a separate agent per section-sized chunk, then a single whole-document pass that catches repetition, rhythm, and structure no chunk-level agent can see. editor triages every finding into **surgical** (preserves meaning: cut padding, weak verb → strong, passive → active, collapse a doublet) or **substantive** (changes what it says or its shape: delete a list item, merge a section, cut a sentence with a distinct idea). `critique` and `tighten` share this process — what differs is what happens after.

### critique

Read-only. Runs the document through editor and reports what she finds — no edits, ever. For when you want a second opinion, not a rewrite.

#### Usage

- **Explicitly:** `/critique <file>`
- **Automatically:** on phrases like "critique this," "how does this read?," "what's wrong with this," "give me notes," or "review this draft."

### tighten

Applies the edits. No approval step, no mode to pick — surgical and substantive fixes both apply, as exact find-and-replace. The one thing it holds back: an edit that would flatten a line's emotion or kill a deliberately-built cadence. tighten skips it and names it in the report instead of applying it.

#### Usage

- **Explicitly:** `/tighten <file>`
- **Automatically:** on phrases like "tighten this," "clean this up," "fix this," "edit this for economy," or "make this leaner."

Both work on one document or a batch — several board policies, a folder of drafts — in one run. Want the notes first and the edits later? Run `critique`, then `tighten` once you've seen what it found.

## pitch

One agent, two skills: **managing-editor** gives a single Socratic editorial read; **sharpen** runs a pitch through managing-editor for a quick verdict; **page-one-meeting** simulates a multi-persona debate.

### managing-editor

`managing-editor` (agent, model: opus, tools: `Read`, `WebSearch`, `WebFetch`) is a managing editor at a digital-first publication, evaluating pitches by the editorial standards of the NYT, Vox, The Atlantic, or The New Yorker. Socratic, not prescriptive — it asks the questions that help a writer see what's working, rather than handing over a list of fixes.

#### How it works

Unlike `editor`, it isn't limited to judging the prose handed to it: `WebSearch` and `WebFetch` let it check whether a pitch's claims hold up and whether the angle's already been covered, not just whether the writing works. Name a publication and it pivots to that outlet's editorial voice and priorities; leave it unnamed and it applies standard journalism ethics.

It evaluates a pitch against four questions:

1. **Is this newsworthy?** — impact, timeliness, proximity, prominence, conflict, novelty, human interest.
2. **Does this work as a story?** — a specific angle, narrative tension, a human element, a reporting plan.
3. **Will this resonate?** — audience fit, publication fit, emotional or intellectual stakes.
4. **Does this meet our standards?** — accuracy, fairness, independence, sourcing, accessibility.

Then it makes the call: **green light**, **revise and resubmit**, or **kill it** — with reasoning, not a hedge.

### sharpen

A single editorial pass, not a debate. Launches `managing-editor` with your pitch material verbatim (plus a named outlet, if you gave one) and relays the verdict to you word for word. Everything stays in the conversation; `page-one-meeting` is the one that writes to disk.

#### Usage

- **Explicitly:** `/sharpen`
- **Automatically:** on phrases like "sharpen this pitch," "quick editorial read," "give me an editor's take," or "run this by an editor."

For a multi-persona debate instead of one editor's read, use `page-one-meeting`.

### page-one-meeting

A simulated page-one editorial meeting: a chair (Claude) convenes 3-5 editor personas who debate a pitch — not just report to the chair one at a time — and the meeting ends in a verdict and a shaped pitch.

#### How it works

The chair launches each persona as a separate `Agent` call with a distinct `name`, then reaches it by name via `SendMessage`. Agents message the chair unprompted as they finish. The meeting runs as a live debate among named personas, not a deterministic script, so it uses `Agent`/`SendMessage` rather than the `Workflow` tool.

#### The phases

0. **Intake** — read what the pitcher gave, ask only for what's missing and matters most, proceed the moment they signal impatience.
1. **Cast assembly** — pick 3-5 archetypes suited to this pitch's tensions, fresh names each run.
2. **Seating / opening takes** — spawn all personas in parallel, then digest their opening positions for the user.
3. **Open debate** — by default, each persona challenges 1-2 named peers in a single round, then reports a revised position.
4. **Mandatory dissent round** — see below.
5. **Verdict + shaped pitch** — first disk write, `pitches/<date>-<slug>/pitch.md`: verdict and shaped pitch, plus the debate synthesis and dissent findings.
6. **Drafting brief** (optional, argument-gated) — `pitch-brief.md`, one section per persona, each pulling real published analogues.

#### Why the mandatory dissent round exists

Unguided multi-agent debate has a known failure mode: sycophantic conformity, where positions converge and lock in, often by the second exchange. Left unchecked, the room agrees with itself and nothing forces a check on whether that consensus is right — a weak angle or a bad premise can sail through if every persona is built to agree.

So Phase 4 doesn't get skipped, especially when the room looks unanimous. Dissent duty goes to whichever persona moved *most toward* consensus in Phase 3, not the built-in skeptic, who would rehash their existing position. They must argue two things: steelman the case that the pitch is wrong, and name the closest coverage of this angle (or admit they can't rule it out). If they still believe the consensus holds after trying, they say so and name what would change their mind. They record the finding in `pitch.md` either way, so it becomes part of the output rather than a checkpoint that leaves no trace.

The chair adds one more check in Phase 5. They reread the shaped pitch as a skeptic, independent of what the panel just agreed, before it's finalized.

#### Usage

- **Explicitly:** `/page-one-meeting`, or `/page-one-meeting brief` to jump straight to the drafting brief.
- **Automatically:** on phrases like "page one meeting," "run this by the editors," "simulate a pitch meeting," or "get the room's take."

For a single editorial read instead of a multi-agent debate, use `sharpen`.

## documentation

Technical writing is a different job from prose editing. `draft` protects a writer's voice while cutting fat; `documentation` assumes there's no voice to protect.

One skill: **write**. It edits the file directly.

### write

Two things happen before a word is drafted.

**Name the reader.** Who reads this, what must they do, what do they already know? A skeptical non-technical reader needs every silent failure called out, and reads an admiring sentence about the architecture as a sales pitch. An engineer who has done this four times needs neither. Tone and coverage follow from the answer.

**Verify.** Every proper noun in a doc is a factual claim, and docs rot silently because nobody re-reads the install guide while changing the code. So it greps for every path, command, flag, and env var before describing any of them. A section documenting code that no longer exists isn't badly worded — it's fiction, and it gets deleted rather than reworded. Install flows and menu paths aren't greppable, so it never describes one it hasn't watched run.

Then it drafts, holding every sentence to one test: **what does the reader do differently because they read this?** "Nothing, they just feel better" means it doesn't go in. That cuts reassurance ("it just works out of the box"), closing flourishes ("that's the whole setup"), design essays defending an architecture nobody attacked, and the one that sneaks in unnoticed — **session leakage**, where a doc drafted at the end of a long working session inherits the session, answering questions nobody asked and narrating what changed instead of describing what is.

It insists on one addition: **the silent failure**. If doing step 2 without step 1 produces a plausible-looking success that's actually broken, that goes in the doc, in the step and in troubleshooting both.

It closes by telling you — in chat, not in the doc — what it verified and what it only reasoned about, including any UI flow it has never watched anyone click through.

It also covers **commit messages and PR descriptions**, which are documentation with a hostile deadline: written at the end of a long session, when the session is the only thing in your head. That makes them where session leakage does the most damage, and the reader — someone bisecting a regression eighteen months from now — is the least equipped to survive it. So the message describes what the code does now and why it needed to, not the three approaches you abandoned or the bug you introduced at 2pm and fixed at 3pm. The reader has the diff; they can see what moved. Why it moved is the only thing a commit message adds.

#### Usage

It loads on its own whenever documentation is being written or updated — "write a README," "document this," "update the install guide," "our docs are out of date" — and whenever a commit message or PR description gets drafted. There's no command to type, because the failures it prevents are the ones you'd never think to ask for help with.

It won't touch writing that has a voice — essays, posts, emails, marketing copy. That's `draft`.

## Author

Benjamin Jackson ([@benjaminjackson](https://github.com/benjaminjackson))
