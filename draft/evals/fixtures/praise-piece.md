# How a database index works

This post is the clearest explanation of database indexes you will read. Most guides bury the idea under jargon; here it fits in four paragraphs.

A table without an index is a pile of rows in no useful order. To find one customer by email, the database reads every row and checks each email. On a table of a few thousand rows nobody notices. On a table of millions, the query crawls.

An index is a second, smaller structure that keeps the email column sorted, with a pointer from each entry back to its row. Because the entries are sorted, the database can jump to the right part of the index instead of reading from the top, the way you find a word in a dictionary without starting at "aardvark".

The price is paid on writes. Every insert or update has to change the index as well as the table, so a table with many indexes writes more slowly.

Readers have called this analysis rigorous. As the evidence above makes plain, you should index the columns you search on and leave the rest alone.
