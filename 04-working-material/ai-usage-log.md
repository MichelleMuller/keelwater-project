# AI usage log

Running log for the "How you used AI" part of the recording. Capture what AI did, what I kept, what I overrode, and anything it got wrong.

| Date | Task | Tool | What it produced | What I changed / overrode | Wrong or rejected? |
|---|---|---|---|---|---|
| 2026-10-15 | Brainstorm session | Claude (voice / chat) | Structured notes from spoken brainstorm | | |
| 2026-10-15 | Organising context into repo | Claude (Cowork) | Repo structure, fact sheet with derived numbers, brainstorm organised by task question, assumptions log | | Flagged: "fraud is the blocker" isn't in the brief; a wrong company name in the data-privacy notes (fixed); brainstorm holds two contradictory bulk-sorting options |
| 2026-10-15 | Testing "sorting helps with fraud" | Claude (web research) | Research note on motor claims triage, fraud scale, signals, regulation | Michelle chose motor claims as the domain and asked to test the fraud assumption rather than accept it | Partly rejected my own framing: triage is mainly about speed; fraud screening is the gate that makes speed safe. Several sources are vendor blogs, flagged as directional |
| 2026-10-15 | Reading the time-to-sort data | Cursor (Claude) | Illustrative distribution fitted to the two known points (median 11 min, 15% > 4h): fast majority plus a stalled tail that holds most of the waiting time | Michelle challenged "half sorted within 11 min" (correct by definition of median, but only if "time to sort" means what we think) | The curve shape is inferred, not data; labelled illustrative. Raised DQ-01: is time to sort elapsed time or handler time? |
| 2026-10-15 | Discovery questions by stakeholder | Cursor (Claude) | Brainstorm questions + data questions consolidated in open-questions.md, grouped by who to ask (data, engineering, product leadership, sales, CS/AM, support, customers, legal) | | |

## Candidates for "one thing it got wrong"

Note them as they come up, pick the strongest at the end.

- Brainstorm (AI-structured) treated "fraud is the blocker" as fact. The brief never says that; research suggests speed is the primary ask.
