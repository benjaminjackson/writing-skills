13 line notes, 2 structural. Biggest: "Review waits got much shorter after the change" is the result the whole post exists to report, and the post admits in the next sentence that nobody measured it.

**Structural**

- "Review waits got much shorter after the change. We did not set out to measure the change carefully, and we did not keep the spreadsheet from the spring, but nobody on the team doubts the direction." The spring measurement opens the post with precise numbers (a day and a half, an hour, twenty minutes), and then the payoff has none. Either give the before and after wait, or cut the admission down to one plain clause and let the concrete examples carry the claim. **Substantive.**
- The "What changed" and "What it cost" sections both end on soft human-interest lines ("the release manager noticed", "two new hires ... said the block was the easiest part"). The second one restates the first sentence of its paragraph, that nobody has asked to drop the block. Cut "Two new hires joined in the autumn ..." or move it up and make it the evidence for "nobody has asked to drop it". **Substantive.**

**Line notes**

*The waiting problem*

- "It is worth pointing out that most of the time a change spent waiting was spent in review, not in CI." Throat-clearing. The opener announces a point instead of making it. Start at "Most of the time a change spent waiting ...". **Surgical.**
- "spent waiting was spent in review" repeats "spent". Try "most of a change's waiting happened in review, not in CI." **Surgical.**
- "Over a month, the waiting added up to more time than the building, the testing and the deploying put together." Good line, keep it; it is the sentence that makes the problem feel large.
- "Nobody on the team was careless about reviews. The trouble was timing." Load-bearing. Keep both.
- "A reviewer who wanted to help still had to choose, every time, between their own deadline and somebody else's, and their own deadline usually won." The comma-set "every time" splits "choose" from its object. "still had to choose between their own deadline and somebody else's every time" reads straighter. **Surgical.**
- "The author, meanwhile, could see the pull request sitting there" — "meanwhile" is filler; cut it. **Surgical.**

*The morning block*

- "The block also gave reviewers permission to ignore review notifications for the rest of the day, which most of them had wanted for a long time." "for a long time" is soft; "which most of them had long wanted". **Surgical.**
- "And the block had to cover any and all review requests, including the small ones" — a doublet. "any and all" says one thing twice; "every review request" is enough. **Surgical.**
- "In the retro, Odile said it best:" Keep the quotation exactly as it is. "said it best" is a small cliché; "Odile put it plainly" or just "Odile said:" would do. **Surgical.**

*What changed*

- "The reviews themselves changed as well." Weak opener; "themselves" and "as well" are padding. "Reviews got better too." **Surgical.**
- "Reviewers also started to notice ... Reviewers also got better at saying ..." Two sentences in one paragraph start "Reviewers also". Vary the second or merge. **Surgical.**

*What it cost*

- "The morning block also moved the standup to ten, and it left the afternoon with no review slot. This made the late-day backlog worse." A bare "this" with two candidates: the standup moving to ten, or the afternoon losing its review slot. The reader has to guess which made the backlog worse. Name it: "The missing afternoon slot made the late-day backlog worse." **Surgical.**
- "People who liked to finish a change and see it merged on the same day lost the same-day merge" repeats "same day". "People who liked a same-day merge lost it, and they said so." **Surgical.**

**The single change that matters most:** put a number, or an honest "we did not measure it" with no hedge around it, under "Review waits got much shorter". Everything else is polish.
