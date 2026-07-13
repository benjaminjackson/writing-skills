---
name: write
description: >-
  Use this skill whenever you are writing or updating technical documentation:
  a README, an install guide, setup or config docs, dev docs, API docs, help
  text, a troubleshooting section — and also every commit message and pull
  request description. Trigger on "write a README", "document this", "update
  the install guide", "our docs are out of date", "write the commit message",
  "open a PR", or "write the PR description". It edits the file directly, and
  it verifies every path, command, and flag against the actual code before
  writing about them. This is technical writing — transactional prose, no
  author's voice to preserve. Do NOT use it for writing that has a voice:
  essays, blog posts, emails, marketing copy, anything persuasive or personal.
  Those belong to the `draft` plugin. Do not use it to ghostwrite something new
  from nothing; it documents systems that already exist.
---

# Write or update a document

Documentation earns the reader's time or wastes it. There is no third option, and no credit
for sounding good. Every rule below exists because a real doc broke one of them.

Work in this order. Steps 1 and 2 happen before a word gets drafted.

## 1. Name the reader

Answer three questions and write the answers down where you can see them:

- **Who reads this?** Not "users" — the actual person. A senior engineer on your team, or a
  non-technical staffer who is already half-convinced this won't work.
- **What must they do?** The doc exists to get them from not-having-done-it to having-done-it.
- **What do they already know?** Everything they know and you explain again is theft.

The rest of the doc follows from this. For a skeptical, non-technical reader, a silent failure
is worse than a loud one, and a sentence admiring the architecture reads as a sales pitch —
which is what makes a skeptic close the tab. For an engineer who has done this four times,
the same sentence is just in the way. Same fact, opposite treatment, and the only thing that
decides it is who is reading.

Don't skip this because the doc is small. A troubleshooting entry has a reader too.

## 2. Verify before you write

Every proper noun in a doc is a factual claim: file paths, command names, flags, env vars,
package names, menu items. Claims can be false, and docs rot silently — nobody re-reads the
install guide while changing the code.

**Grep everything greppable.** Before writing about it, confirm it exists:

- Every file path and directory the doc will name.
- Every command, subcommand, and flag. Run `<tool> --help` rather than trusting memory.
- Every env var, config key, and package name.

If a doc already exists and describes something that is no longer in the repo, that section is
not badly worded — it is **fiction**. Delete it and say so. Do not sync its wording to the
current code and call the doc updated; there is nothing under it to sync. (A real one: an
install guide walked users through a `.env` file, a Node check, and hand-editing a JSON config
— for a skill that had been deleted from the repo months earlier.)

**Do not invent the UI.** Install flows, menu paths, click sequences and dialogs are not
greppable. If you have not watched it run, you do not know what it does. Symmetry with a
neighboring feature is not evidence — one file being a double-click does not make the file
next to it a double-click. When you have not seen the flow: ask, mark it unverified, or leave
it out. Never guess.

**Check hard limits before writing, not after.** If a field has a documented maximum — a
1024-character skill description, a 72-character commit subject, a 160-character meta
description — measure it while drafting. A limit you plan to eyeball at the end is a limit you
will break.

## 3. What never gets written

Hold every sentence to one question: **what does the reader do differently because they read
this?** If the answer is "nothing, they just feel better," it does not go in. Reassurance is
not information. Absence of a problem is not a feature — the reader does not know or care what
the install *could* have been.

The tells, all of which are cheap to spot:

- **Praise-by-negation.** "No Node, no hand-edited config files." "Nothing to configure." "You
  don't have to think about Z." This is the author admiring the system in the reader's time.
- **The closing flourish.** The section after the last useful section, there to land a note
  rather than to inform. "That's it." "That's the whole setup." Also the editorial about the
  failure mode — "that's the one way this goes wrong, and the fix is always the same" — when
  the reader needs the symptom and the fix, not your view of how tidy the failure is.
- **Design defense.** Explain a design choice only where the explanation changes what the
  reader does. "Why two files, not one" earns its place *because* it tells you which file holds
  the token, which is why the other one can't stand alone, which is why you can't skip step 1.
  It stops earning its place the moment it becomes an essay defending the architecture. Never
  justify to pre-empt criticism. Never justify to show your work.
- **Session leakage.** This is the one that gets written without noticing. A doc drafted at the
  end of a long working session inherits the session: it answers questions nobody asked,
  defends decisions the reader never watched anyone make, and narrates what changed instead of
  describing what is. No "as we discussed." No "we decided." No "this previously worked by…"
  No walking through the alternative that got rejected an hour ago. **The reader arrived just
  now.** They have no memory of the conversation, and nothing they need is in it.

**Cut the clause, not the sentence.** Reassurance usually arrives fused to a real instruction,
and over-correcting throws away the warning. "Paste the token once, into a masked field, never
into a chat, and nobody reads it back to you" contains two instructions (paste it there; never
in a chat) and one comfort. The comfort goes. The sentence stays.

## 4. Line-level economy

Section 3 is about sentences that should not exist. This is the ordinary tax on the ones that
should. Hunt these:

- **Fat.** Ten percent comes out of any draft, usually more. Find it.
- **Throat-clearing.** "It is important to note that," "in order to," "the fact that." Delete.
- **`this` with no noun.** "This means…" — this *what*? Name it: "this flag means…"
- **Hedges and intensifiers.** Very, really, quite, simply, just. "Simply run" helps nobody and
  insults anyone for whom it isn't simple.
- **Elegant variation.** Three words for one thing, to avoid repeating yourself. In prose this
  is a style flaw; in a doc it is a **bug**. If the token, the key, and the credential are the
  same object, the reader cannot tell. Pick one name per thing and repeat it forever.
- **Passive that hides the actor.** "The config is generated" — by whom? By the reader, or by
  the installer? Their next action depends entirely on the answer.
- **Vague abstractions.** Process, factor, context, framework, aspect. Name the thing.
- **Latinate pomp.** utilize → use, prior to → before, terminate → stop.
- **Cleverness.** The pun, the wink, the fragment dropped in for effect. It makes the reader
  stop to admire you, and it costs them the meaning.

## 5. What always gets written

**The silent failure.** For any multi-step setup, ask: *what happens if someone does step 2 but
not step 1?* If the answer is a loud error, fine — the software is telling them. If the answer
is a **plausible-looking success that is actually broken**, that is the single most valuable
paragraph in the document. (A real one: install the skills but not the connector and everything
looks right, except every answer comes back empty.) It goes in three places — the step itself,
the troubleshooting section, and anywhere the reader might stop early thinking they're done.

The happy path is the easy half. Anyone can write it. Write the other half.

## 6. Commit messages and pull requests

A commit message is documentation with a hostile deadline: it gets written at the end of a
long session, when the session is the only thing in your head. That makes it the place session
leakage does the most damage, and the reader — someone bisecting a regression eighteen months
from now — is the least equipped to survive it.

Everything above applies. These are the parts that bite hardest here:

- **Describe the change, not the journey.** What the code does now, and why it needed to. Not
  what you tried first, not what the review said, not the bug you introduced at 2pm and fixed
  at 3pm. The three approaches you abandoned are not history — they never shipped.
- **The reader has the diff.** They can see *what* lines moved. They cannot see *why*, and that
  is the only thing a commit message adds. Don't narrate the patch back to them.
- **No conversational residue.** "As requested," "per the discussion," "addressing the feedback,"
  "as we decided." The reviewer was not in the room and the future reader never will be.
- **The subject line is a claim about behavior**, in the imperative, under 50 characters: what
  the tree does after this commit that it didn't before.
- **Verify the body against the diff, not against your memory of the work.** Read the actual
  patch before describing it. A commit message that describes an earlier draft of the change
  is the same failure as a doc that describes deleted code.
- **A PR description answers three questions:** what changed, why it changed, and how a reviewer
  can convince themselves it works. Everything else is optional. What you didn't test goes in,
  plainly — that is the rule below, and a PR is where it matters most.

## 7. Say what you didn't verify

When you finish, tell the user — **in chat, not in the doc** — what you actually confirmed and
what you only reasoned about. Which paths you grepped. Which commands you ran. Which UI flow
you have never watched anyone click through.

"I did not install these packages into a clean environment and click through" is a sentence you
are allowed to write, and the user is far better off for reading it. Gloss over it and the next
person to find out is a reader, in the middle of a setup that doesn't work.

## Guardrails

Writes and edits the target file directly — this is a drafting skill, not a read-only review.
Never describes a UI or install flow it has not watched run: it asks, marks the flow unverified,
or omits it. Never rewords a section that documents code which no longer exists; it deletes the
section and reports it. Never finishes without telling the user what went unverified. Never
touches prose with a voice — essays, posts, emails, marketing copy belong to the `draft`
plugin's `critique` and `tighten`.
