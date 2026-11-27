---
name: tighten
description: >-
  Use this skill whenever someone hands you a piece of writing and wants it
  actually fixed: tightened, cut for economy, given a rigorous line edit.
  Essays, emails, board policies, internal docs, marketing copy, blog posts,
  or any prose draft. Applies every edit automatically, no approval step
  (at most a one-line calibration question on a long doc whose purpose is
  ambiguous) — the right call whenever the ask is "just make this better"
  and the user doesn't want to review each change. Trigger on phrases like "tighten this",
  "clean this up", "fix this", "edit this for economy", "make this leaner",
  "cut the fluff from this doc", "give this a line edit and apply it", "this
  feels bloated, fix it", or "/tighten [file]". Works on a single document or
  a batch in one run: several board policies, a folder of drafts, a stack of
  emails. If the user wants feedback without the file being changed, use
  `critique` instead. Don't reach for this when the request is to write
  something new, brainstorm, or restructure unprompted; it edits prose that
  already exists, it doesn't ghostwrite.
---

# Tighten a document

This skill takes a document, runs it through **Deirdre** (the `editor` sub-agent, a critic
built on Deirdre McCloskey's *Economical Writing*), and applies the edits — surgical and
substantive alike — with no approval step. If the user wants a review instead of a rewrite,
that's `critique`, not this.

The prime directive: **preserve all original meaning. Tighten the words, not the message.**
Deirdre only critiques; she refuses to rewrite. So the flow is: she finds what's fat, weak, or
repetitive; **you** (the agent running this skill) make the edits, carefully, as exact
find-and-replace — then apply them without stopping to ask.

## How it works

See [../../references/deirdre-method.md](../../references/deirdre-method.md) for the full
method: how the `editor` sub-agent works, chunking rules, the critique prompts, and the
surgical/substantive distinction. Everything below is specific to `tighten`'s no-approval
apply step.

## The workflow

1. **Read & chunk.** Read each document, note its purpose (see "read the document's purpose" in the shared method file), measure tokens with `tks`, and split it into Pass 1 chunks per the chunking rules in the shared method file, unless the request ends with `whole-doc`.
2. **Pass 1 — line by line.** Unless the request ends with `whole-doc`, launch one `editor` agent per chunk (parallel batches) with the granular prompt. Collect the line-by-line notes.
3. **Pass 2 — whole doc.** Launch the holistic pass with the whole-doc prompt.
4. **Triage.** Merge Pass 1 + Pass 2 findings, dedupe overlaps, and sort each into surgical or
   substantive per the shared method file. When a note that contains
   "Fact needed from the writer:" and a cut land on the same sentence, the fact-needed note
   wins: the sentence stays and is listed in the report.
5. **Apply everything.** Make every surgical and substantive edit via exact find-and-replace.
   Keep every word that states part of a claim: what is claimed, its scope, its cause, its condition, its timing, or who it applies to ("tried to" in "we tried to fix it", "only on weekdays", "because the server was down", "for new hires"). Cut such words only when a note shows the claim is still stated elsewhere in the document. A word swap that changes a claim ("safe changes" to "good changes") counts as cutting it. Emphasis that sets how strong a claim is counts as part of it: "even" in "nobody even opened the report" says the report got no attention at all, so keep it. Filler that states no part of any claim ("in order to") is still cut, and so are "very" and "really" when they add no force to what is claimed. This rule holds whatever a note suggests, and the duplicate cuts below follow it too.
   Semantic-duplicate cuts — heading-echoes, restatements, closing flourishes that only
   restate — are surgical and apply by default when every note on that sentence calls it a duplicate. A cut is conditional when a note offers it on a condition ("consider cutting", "if you keep it"), when the notes on that sentence disagree about whether it is a duplicate, or when it is a concreteness-for-brevity cut or a length target (see "read the document's purpose" in the shared method file). Apply a conditional cut only when the document's stated purpose asks for it: the user's request or the document itself says what the document is for, and that purpose asks for it to be short (a length target, a one-pager, "make it punchy"). A purpose you guess from the kind of document does not count. If the purpose is genuinely ambiguous *and*
   the document is over 4,000 tokens, ask one line; otherwise keep the sentence and list the conditional cut under "Call out anything skipped" in the report. The other exception: an edit that flattens emotional meaning or
   kills a deliberate cadence (see "protect the emotional and rhythmic lines") — skip it and
   note it in the report instead of applying it. A cut that removes the link between two
   sentences is not applied either: rewrite that sentence so the link survives (see the
   linking-sentence rule in [../../references/deirdre-method.md](../../references/deirdre-method.md)).
   When a note contains "Fact needed from the writer:", apply its other fixes, leave the
   vague phrase as written, and list it in the report. Nothing else waits for approval; this skill
   never asks for sign-off, it applies.
6. **Recheck in rounds.** Round one is steps 1 to 5. Each round, round one included, ends with a recheck. The run makes at most 3 rounds of edits, so it stops after the third round's recheck at the latest.
   - Before each round's edits, keep the text as it stands in your own context, and keep a numbered list of the round's edits, each quoted before → after. Write no file other than the ones the user gave.
   - Each round's recheck, round one's included, spawns a fresh `editor` agent that reads the after text, writes its own first read of the new text, and only then reads the before text and the list of edits. It never sees an earlier round's notes.
   - Send that agent the after text alone in the first recheck message below and wait for its first read. Then send the before text and the list in the second recheck message, as a follow-up to the same agent with `SendMessage`. If you cannot send a follow-up to the same agent, say so in the report and send one message: the first recheck message with its last two sentences replaced by "Write that first read before you read anything below.", then the second recheck message.
   - It marks each edit closed, open or worse: closed means the fault is gone and nothing was lost, and worse means the meaning moved, a cadence flattened, or a link between sentences broke.
   - It raises new problems only in sentences the last round rewrote, and each new problem counts as open. Drop any new problem it raises in a sentence that no edit of the last round rewrote; only problems in rewritten sentences become open items. Untouched prose was already judged, and judging it again every round would ratchet the voice away.
   - Stop when nothing is open or worse, or when a round closes nothing, and stop after the third round's recheck in any case: the cap of 3 rounds of edits is a placeholder, not a measured number.
   - When the rounds stop, put every edit still marked worse back to its before text. That edit is then settled, and the report lists it with the fault it leaves.
   - Until then, the open and worse items, worse first, are the next round's work. Fix a worse edit by rewriting it so the fault it fixed stays fixed and the meaning, cadence or link returns. Put the before text back only when no rewrite does both; that edit is then settled: no later round rechecks it, and the report lists it with the fault it leaves. Then fix the open ones, under the same rules as step 5. That round's recheck covers those edits.
   - On a document over 4,000 tokens, split the recheck the way Pass 2 splits (see the shared method file): each agent gets the whole after text, the before text of its part, and only the edits in its part. In a batch, run the rounds per document.
7. **Claim check.** After the recheck rounds stop and the edited text is written, and before the report, launch one fresh `general-purpose` agent with the claim check prompt below. It gets only the original text, the edited text, and the step-5 rule: the paragraph that starts "Keep every word that states part of a claim", quoted word for word from this file at launch time. It lists each place where the edit cut or swapped words that state part of a claim and the claim is not stated elsewhere in the edited text. Put each listed passage back to its original words, and do not apply anything else it says. This step runs with `whole-doc`, `chunked` or neither, and on a batch it runs once per document. The report lists what it restored.
8. **Bump `updated:`.** For any edited file that has note frontmatter, set `updated:` to today
   (`MM-DD-YYYY`). Skip files without frontmatter.
9. **Report.** Present findings per **Reporting** below. There's nothing left to approve —
   this is a summary of what changed, not a request for sign-off.

**Switches: `chunked` and `whole-doc`.** They exist to measure whether Pass 1 earns its cost. `chunked` runs Pass 1 and then Pass 2 with its prompt as written, which is the same as running with no argument; it stays so eval runs can name the setting. If the request ends with `whole-doc`, run only Pass 2: still read the document, note its purpose and measure it with `tks`, but do not split it into chunks or run Pass 1, and send the Pass 2 prompt without the sentence "You don't need to re-flag every small word fix; another pass handles those.", since no other pass runs. Triage and apply from that pass alone. The recheck rounds run as usual with either argument or with none.

**Recheck prompt (every round)**: send the texts and the list inline, delimited, in two messages to the same agent.

First message, when you spawn the agent:

> Critique this edited draft against Deirdre McCloskey's *Economical Writing*:
>
> ```
> <AFTER>
> ```
>
> Write your own first read of it in three or four lines: what it says, how it sounds, and where a reader snags. Write only that first read for now. The text as it was before the edit, and the list of edits, come in the next message.

Second message, after its first read:

> Here is the text as it was before the edit:
>
> ```
> <BEFORE>
> ```
>
> and the numbered list of edits:
>
> <EDITS>
>
> Mark each edit closed (the fault is gone and nothing was lost), open (the fault is still there), or worse (the meaning moved, a cadence flattened, or a link between sentences broke), and quote the text for each. Raise new problems only in sentences these edits rewrote; the rest was judged already. Supply no new fact, number, name or example.

**Claim check prompt (step 7)**: send the texts and the rule inline, delimited, in one message.

> Here is a rule about which words state part of a claim:
>
> ```
> <STEP-5 RULE>
> ```
>
> Here is a text before an edit:
>
> ```
> <ORIGINAL>
> ```
>
> and after it:
>
> ```
> <EDITED>
> ```
>
> List each place where the edit cut or swapped words that the rule says state part of a claim, and the claim is not stated elsewhere in the edited text. For each one, quote the original words and the edited words. If there are none, say "None". Suggest no other edit: only list words to put back.

## Reporting

- **Open with one line.** "N safe tightenings, M structural changes applied." That's the whole
  run at a glance.
- **Say how the rounds ended.** Name how many rounds ran and which stop rule ended them, quote every edit still open, with what is wrong, and quote every settled edit with the fault it leaves. If the recheck could not go to the same agent in two messages, say so.
- **Say what the claim check restored.** Quote each passage step 7 put back, or say it restored nothing.
- **Collapse the surgical.** Don't show every before→after. Give the count and the **rewritten
  final paragraphs**, so the user eyeballs the clean result instead of diffing each word.
- **List the semantic-duplicate cuts.** Unlike word-level tightenings they're judgment calls,
  so give a compact locator list — each cut quoted, one line on where its idea survives. No
  before/after needed.
- **Spotlight the substantive.** These already happened, but they're the ones worth a second
  look — number each, show before→after, and say why it was safe to apply.
- **Call out anything skipped.** If an edit was held back for flattening emotion or killing a
  cadence, or as a conditional cut the stated purpose did not ask for, name it and say why, so the user knows it wasn't missed, it was a judgment call.
- **List the facts needed.** A phrase whose note contains "Fact needed from the writer:" was
  left as written. Quote each one and say what fact it needs, so the writer can supply it.

## Guardrails

Preserves all original meaning, with three named exception paths: edits that flatten emotion or
kill a deliberate cadence are skipped, not applied; an edit the recheck rounds leave settled with its fault is listed in the report with that fault; and when a long document's purpose is
genuinely ambiguous, the skill asks one calibration line before choosing how hard to cut —
calibration, not approval. Editing local markdown is automatic in this project — this skill
always applies its edits, both surgical and substantive, with no per-edit approval step.
Never sends, posts, or touches anything outside the local file(s) it's given.

Fixes follow the no-new-facts rule in "How you respond" in [../../agents/editor.md](../../agents/editor.md), and so do your own rewrites: when a note contains "Fact needed from the writer:", apply its other fixes, leave the vague phrase as written, and list it in the report.

Never cut a sentence that links the one before it to the one after it, even when the editor flags it; rewrite it so the link survives. The full linking-sentence rule is under "Reading rules" in [../../references/deirdre-method.md](../../references/deirdre-method.md).
