---
type: baseline
baseline_file: fixtures/review-planted.md
focus: {source: file, path: draft.md}
weight: 2
---
The baseline is a long post on why a team moved code review to the morning. The produced version is the same post after a line edit for economy. A line edit may cut words, merge sentences and reword. It must not change what the post claims.

Do not judge whether the edit is good. Do one extraction task:

**List every claim in the baseline that the produced version drops, reverses, weakens into something different, or makes stronger than the baseline supports.** Check at least these: the team of nine measured where a change spent its time, and most of the waiting was in review, not in CI, which takes about twenty minutes; a pull request sat a day and a half, and switching back to an old branch cost an hour; the trouble was timing, not careless reviewers, and the rotating reviewer and the reminder bot both faded; the fix treated the reviewer as the problem when a review had no set place in the day; in June the team blocked nine to ten each morning for the review queue, oldest first; authors were asked to split any change that takes more than twenty minutes to read; urgent production fixes kept a separate label, and the block covered every review request, small ones included; Odile's quotation, word for word; review waits got much shorter, with no figure given, and the team did not measure it carefully; second rounds got faster, fewer merge conflicts, and the release manager's list got short; reviews got more careful and reviewers approved clean changes quickly; the block costs an eighth of working time, moved the standup to ten and left the afternoon with no review slot, which made the late-day backlog worse; the team kept the block for five months and expects to split the queue past twelve people.

Cutting a word that repeats what another word already says is not a change of meaning. Replacing the bare "This" in "This made the late-day backlog worse." with a noun for what made the backlog worse is the edit the post needed, not a change of meaning, whichever of the two things before it the noun names. Turning "much shorter" into a figure is a change of meaning. Cutting "much" from "much shorter" weakens the claim and is a change of meaning. Cutting "The block was not free." from the start of "What it cost" is not a change of meaning, because the heading already says it. The baseline calls one backlog both "late-day backlog" and "afternoon backlog"; using one of the two names throughout is not a change of meaning.

Changing the words that introduce a quotation is not a change of meaning when the quoted words stay the same. "Odile said it best:" and "Odile said:" make the same claim, because the quotation itself shows how she put it.

For each item that changed, quote the baseline and the produced version side by side. Write NONE if nothing changed.

Then end with a verdict line. Writing NONE is not the verdict.

PASS if you wrote NONE.
FAIL if you listed one or more.
