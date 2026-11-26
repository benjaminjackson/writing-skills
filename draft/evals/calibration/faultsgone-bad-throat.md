# Why we stopped deploying on Fridays

For two years our team shipped whenever a change was ready, Friday afternoons included. It is important to note that most of our worst outages started on a Friday, as the incident log made plain.

Friday deploys fail for a dull reason. The people who wrote the change go home, and the people on call over the weekend did not write it. When something breaks at nine on Saturday, the on-call engineer has to read an unfamiliar diff before deciding whether to roll back. Our release tool also batched every deploy from the week into one Friday train, so the on-call engineer could not tell which change had broken production. The batching made rollbacks slower.

So in March we froze deploys after noon on Friday. In the retro, Ana put it plainly: "I would rather ship on Monday than debug on Sunday." Nobody argued.

Incidents dropped a lot after the freeze. Weekends got quieter, and the Monday queue got longer, as we expected.

The freeze has a cost. A fix ready at two on Friday waits until Monday morning, and some weeks that delay annoys a customer. That cost is smaller than a weekend spent reading someone else's code.
