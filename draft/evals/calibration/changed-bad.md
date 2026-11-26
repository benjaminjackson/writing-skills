# Why we stopped deploying on Fridays

For two years our team shipped whenever a change was ready, Friday afternoons included. Most of our worst outages started on a Friday.

Friday deploys fail for a dull reason. The people who wrote the change go home, and the people on call over the weekend did not write it. Our release tool also batched every deploy from the week into one Friday train, and the on-call engineer could not tell which change had broken production. The batching made rollbacks slower.

So in March we froze deploys after noon on Friday. In the retro, Ana put it plainly: "I would rather ship on Monday than debug on Sunday." Nobody argued.

Incidents dropped a lot after the freeze. Weekends got quieter, and the Monday queue got longer, which we expected.
