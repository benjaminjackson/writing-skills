# Why we moved code review to the morning

## The waiting problem

Last spring our team of nine engineers measured where a change spent its time between the first commit and the merge. We expected the build to be the slow part, since a full run of the test suite takes about twenty minutes. It is worth pointing out that most of the time a change spent waiting was spent in review, not in CI. A typical pull request sat for a day and a half before anyone opened it, and by the time the comments arrived the author had usually moved on to other work. Switching back to an old branch cost each of us an hour of rereading our own code, and a second round of comments often meant a second day of waiting.

Nobody on the team was careless about reviews. The trouble was timing. Review requests arrived all day, and each one landed in the middle of somebody's own work. We tried a rotating reviewer of the day, which helped for a week and then faded, since the person on duty still had their own tickets due. We tried a bot that posted a reminder after four hours, and people learned to ignore the bot. Each fix treated the reviewer as the problem, when the real problem was that a review had no set place in anyone's day.

## The morning block

In June we tried a fixed block instead. From nine to ten each morning, nobody writes code. The first hour of the day belongs to the queue of open pull requests, oldest first, and anyone who empties the queue early can go back to their own work. We picked the morning because the queue is at its longest then, after a full day of requests has piled up, and because most of us arrive with no half-finished thought to protect.

The rule needed two adjustments in its first month. Urgent fixes for production could not wait until the next morning, so we kept a separate label for them that anyone may review at any hour. And the block had to cover any and all review requests, including the small ones, or people would quietly route their small changes around it by asking a friend for a quick approval in chat. Once every request went through the same queue, the queue became something the team could see and talk about at standup. In the retro, Odile said it best: "I review better before I have written any code of my own." Several people nodded, and the block stayed.

## What changed

Review waits got much shorter after the change. We did not set out to measure the change carefully, and we did not keep the spreadsheet from the spring, but nobody on the team doubts the direction. A pull request opened in the afternoon is now usually reviewed by the end of the next morning's block, and the author gets the comments while the change is still fresh. The reviews themselves changed as well. A reviewer with an hour set aside reads the whole diff instead of skimming it between tasks, and the comments got longer and more useful.

## What it cost

The block was not free. An hour a day is an eighth of every engineer's working time, and a few people resented giving their sharpest hour to other people's code. The morning block also moved the standup to ten, and it left the afternoon with no review slot. This made the late-day backlog worse. A change finished at two in the afternoon now waits until the next morning, where before it might have been reviewed by four.

We have kept the block for five months, and nobody has asked to drop it. The afternoon backlog is the cost we chose to accept, because a day of waiting at a known time is easier to plan around than a day and a half of waiting at an unknown one. If the team grows past twelve, we expect to split the queue by area of the code, so that one hour still covers it.
