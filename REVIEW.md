# Review notes

Check every change for these two patterns. Both came up again and again in review.

## No hard-wrapped lines

Never hard-wrap lines in Markdown or any other multi-line document. Let long lines run, and let the editor wrap them. A hard wrap turns a one-word edit into a diff of the whole paragraph, and a later edit leaves ragged lines that nobody rewraps. Poetry is the only exception.

## One rule, one file

A rule must live in one file. Other files point to that file and do not copy the rule. Copies drift apart: one copy gets fixed and the others do not. For example, the rule that skipped Pass 1 on short documents was pasted into `draft/references/deirdre-method.md`, both `SKILL.md` files and `draft/evals/README.md`, and review rounds kept finding copies that disagreed. When a change touches a rule, search for its other copies and replace them with a pointer.
