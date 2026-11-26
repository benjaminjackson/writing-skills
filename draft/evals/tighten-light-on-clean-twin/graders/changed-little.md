---
type: script
command: 'in=$(wc -c < {input}); out=$(wc -c < {output}); echo "output $out chars, input $in chars"; [ $((out * 10)) -ge $((in * 9)) ]'
input: fixtures/deploys-clean.md
focus: {source: file, path: draft.md}
weight: 1
---
The clean twin has none of the planted faults, so a good edit leaves it close to its original length. Passes when the edited file is at least 90% of the original's length in characters. An editor told to cut a fixed share from any draft fails here.
