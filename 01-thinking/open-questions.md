# Open questions and decisions

Decisions we still need to make for the deliverable, discovery questions grouped by who to ask, and things to verify.

## Decisions

| ID | Question | Options | Status |
|---|---|---|---|
| Q-01 | What happens to bulk sorting? | A) pause and pivot to automation · B) ship as validation layer and training signal · C) ship a trimmed version, free part of the squad for discovery/evals | **decided: B.** No tabular view exists today, so bulk is needed; it also validates the needs, requirements and safety bar for automation |
| Q-02 | Which pile do we automate first? | Simple (rules, low risk, speed value) · Information missing (detect gaps, prompt claimant: low risk, likely biggest speed win) · Suspicious (fraud, high value, high risk) · Assist-only for all three | open. Research leans towards info-missing detection + suggest-only, with a fraud gate on Simple |
| Q-03 | Automate or assist? | Human-in-the-loop suggestions first, auto-action only above an agreed threshold per customer | open |
| Q-04 | What do we tell Sales and CS, and when? | Week 1 holding message · what can be committed to the top-10 renewal (5 months) · what not to promise in the 6 deals | **placeholder in deck** for now |
| Q-05 | Deliverable format | Deck (planned) + one piece of working material (synthetic data eval? AI thematic analysis? this repo?) | leaning deck |
| Q-06 | How to handle the 3h timebox | Decide what to cut and say so in the recording | open |

## Discovery questions, by who to ask

What to find out before committing the squad. Sources: the brainstorm ([brainstorm-organised.md §2](brainstorm-organised.md)) and the review of the product data ([fact-sheet.md](../00-brief/fact-sheet.md)). Ask internal teams first (fast), customers second (slow).

### Data team (incl. the shelved prototype)

| ID | Question | Why it matters |
|---|---|---|
| DQ-01 | What exactly does "time to sort" measure: from claim arrival to sorted, or handler working time? Is it business hours or clock time? | Decides whether the 4h+ tail is queue wait or real effort. A claim arriving Friday 5pm passes 4h without anyone being slow |
| DQ-02 | Can we get the full time-to-sort distribution (histogram), not just median and the >4h share? | The median says nothing about the tail. Our shape (fast majority + stalled tail) is inferred from two points |
| DQ-03 | Split time-to-sort and the >4h share by customer, pile, claim type, and arrival day/time | Pain is likely concentrated in a few large accounts; tells us which segment to pilot with |
| DQ-04 | Why do the >4h claims stall: missing info, waiting on a background check, fraud review queue, out-of-hours arrival? | Each cause points to a different fix (chase claimant vs automate vs nothing) |
| DQ-05 | The 3.4% re-sorts: which direction (Simple → Suspicious or the reverse) and which transitions are most common? | Defines the human error baseline and which mistakes are costly (fraud paid out) vs cheap (extra review) |
| DQ-06 | Do we know final claim outcomes (paid, rejected, fraud confirmed), linked back to the original pile? | Without outcomes there are no labels to train or evaluate an automated sorter |
| DQ-07 | The prototype: what model (rules / classic ML / LLM), trained on what data, how accurate, and why was it put on hold? | Reuse vs restart; may already answer feasibility |
| DQ-08 | Can the prototype's decisions be explained per claim? | The hard constraint: every decision must be explainable to the customer and the regulator |
| DQ-09 | Are we allowed to use customer claims data for training or evaluation? Is PII redaction already in the pipeline? | Decides whether we need synthetic data or per-customer models |

### Engineering (tech lead, squad)

| ID | Question | Why it matters |
|---|---|---|
| EQ-01 | What is actually being built in bulk sorting: table view, filters, multi-select, an API returning all claims? | Confirms whether bulk sorting can double as the validation layer (filters as proto-rules) |
| EQ-02 | Can we log filter and bulk-select actions per user from day one? | Filter usage is the first rule set and training signal for automation |
| EQ-03 | Is there an audit log per claim today (data used, decision, who, when)? | Safety gate before anything is automated |
| EQ-04 | Can sorting rules be configured per customer, or is one model for all realistic? | Customer mix ranges from ~99% simple to mostly complex |
| EQ-05 | What would it take to run a model on claims in shadow mode (suggest only, no action)? | Cheapest way to measure accuracy against the 3.4% baseline |

### Product leadership / whoever prioritised bulk sorting

| ID | Question | Why it matters |
|---|---|---|
| PQ-01 | Why was bulk sorting prioritised? What was validated and which customers are lined up for it? | Avoid redoing discovery; confirms the bulk sorting narrative |
| PQ-02 | Why was the prototype shelved, and what would it take to restart it? | Political and resourcing context, not just technical |
| PQ-03 | Is sorting phase one of a broader claims-automation strategy? | Frames the roadmap (sorting now, full claims processing later) |

### GTM: Sales (AEs)

| ID | Question | Why it matters |
|---|---|---|
| SQ-01 | In the 6 open deals (£2.3M ARR): what exactly did the buyer ask for when they said "automatic sorting"? Speed, headcount, fraud, or a checklist item? | Nothing in the brief says what is blocking the deals |
| SQ-02 | Is automatic sorting a deal blocker or a nice-to-have in each deal? What is the timeline for the biggest one? | Decides what has to be shown and by when |
| SQ-03 | What did the competitor show these buyers, and where did it fall short? | Positioning and unclaimed ground |
| SQ-04 | What has already been promised to prospects? | Avoid overcommitting the squad |

### GTM: Customer Success / Account Management

| ID | Question | Why it matters |
|---|---|---|
| CQ-01 | The 3 accounts that raised it: what problem did they describe, in their words? | Separates the real problem from the feature request |
| CQ-02 | The top-10 account renewing in 5 months: what would they need to see before renewal to stay? | Sets the near-term commitment we can make |
| CQ-03 | Which accounts are at risk because of the competitor launch? | Prioritises pilot customers |
| CQ-04 | Which customers would join a beta and label outcomes? | Validation depends on a labelling beta group |

### GTM: Support

| ID | Question | Why it matters |
|---|---|---|
| SUQ-01 | What do the ~40 tickets that mention sorting actually say: sorting in general, or sorting many at once? | Bulk sorting pain vs automation demand |
| SUQ-02 | Which customers filed them? | Low count across 180 customers suggests concentration |

### Customers (claims handlers, claims ops leads, fraud/SIU teams)

| ID | Question | Why it matters |
|---|---|---|
| KQ-01 | Walk us through a claim from arrival to paid. Where does it get stuck? | The full lifecycle, not just sorting |
| KQ-02 | How do you decide a claim is simple, needs a closer look, or suspicious today? | Becomes the rule set and eval rubric |
| KQ-03 | Do you already have fraud models or fraud signals? What do you use? | Decides whether we build signal detection or plug into theirs |
| KQ-04 | What error rate would you accept from automated sorting, and which errors are unacceptable? | Sets the go-live threshold per customer |
| KQ-05 | Would you want suggestions to approve, or fully automatic actions? | Assist vs automate (Q-03) |

### Customers (IT, governance, legal)

| ID | Question | Why it matters |
|---|---|---|
| GQ-01 | Can you share claims data with us for model evaluation? Under what conditions? | Data access for validation |
| GQ-02 | What explanation and audit trail would you need to sign off on automated decisions? | The explainability constraint, in their terms |
| GQ-03 | Who signs off on go-live? | The sales cycle for this feature is longer than the claims team |

### Internal legal / compliance

| ID | Question | Why it matters |
|---|---|---|
| LQ-01 | What do UK GDPR Art. 22 and FCA Consumer Duty (and US equivalents) require for automated claim decisions? | Defines what we can automate vs suggest |
| LQ-02 | What do our customer contracts allow us to do with their data? | Training and evaluation options |

## To verify

- [ ] "Typesafe/Jev" calibrated decision model: correct name and what it does
- [x] Motor claims triage and fraud: see [motor-claims-triage-and-fraud.md](../02-research/motor-claims-triage-and-fraud.md)
- [ ] GDPR (UK/EU) and US rules on sharing claims data with a vendor for model training; explainability rules for automated decisions (e.g. UK GDPR Art. 22, FCA Consumer Duty)
- [ ] Is there a Gong MCP
- [ ] Hugging Face: open models or datasets for insurance claims / fraud
- [ ] Real competitor examples of automatic claims triage, for realistic positioning
