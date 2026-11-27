# Why we moved code review to the morning

## The waiting problem

Last spring our team of nine engineers measured where a change spent its time between the first commit and the merge. It is worth pointing out that most of the time a change spent waiting was spent in review, not in CI. A typical pull request sat for a day and a half before anyone opened it, and by the time the comments arrived the author had usually moved on to other work.

## The morning block

From nine to ten each morning, nobody writes code. The first hour of the day belongs to the queue of open pull requests, oldest first, and anyone who empties the queue early can go back to their own work.

The rule needed two adjustments in its first month. Urgent fixes for production could not wait until the next morning, so we kept a separate label for them that anyone may review at any hour. And the block had to cover any and all review requests, including the small ones, or people would quietly route their small changes around it by asking a friend for a quick approval in chat. In the retro, Odile said it best: "I review better before I have written any code of my own."

## What changed

Review waits got much shorter after the change. A pull request opened in the afternoon is now usually reviewed by the end of the next morning's block, and the author gets the comments while the change is still fresh.

## What it cost

An hour a day is an eighth of every engineer's working time, and a few people resented giving their sharpest hour to other people's code. The morning block also moved the standup to ten, and it left the afternoon with no review slot. This made the late-day backlog worse. A change finished at two in the afternoon now waits until the next morning, where before it might have been reviewed by four.

We have kept the block for five months, and nobody has asked to drop it.
