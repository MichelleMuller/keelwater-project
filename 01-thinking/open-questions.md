# Open questions and decisions

Decisions we still need to make for the deliverable, plus things to verify.

## Decisions

| ID | Question | Options | Status |
|---|---|---|---|
| Q-01 | What happens to bulk sorting? | A) pause and pivot to automation · B) ship as validation layer and training signal · C) ship a trimmed version, free part of the squad for discovery/evals | **decided: B.** No tabular view exists today, so bulk is needed; it also validates the needs, requirements and safety bar for automation |
| Q-02 | Which pile do we automate first? | Simple (rules, low risk, speed value) · Information missing (detect gaps, prompt claimant: low risk, likely biggest speed win) · Suspicious (fraud, high value, high risk) · Assist-only for all three | open. Research leans towards info-missing detection + suggest-only, with a fraud gate on Simple |
| Q-03 | Automate or assist? | Human-in-the-loop suggestions first, auto-action only above an agreed threshold per customer | open |
| Q-04 | What do we tell Sales and CS, and when? | Week 1 holding message · what can be committed to the top-10 renewal (5 months) · what not to promise in the 6 deals | **placeholder in deck** for now |
| Q-05 | Deliverable format | Deck (planned) + one piece of working material (synthetic data eval? AI thematic analysis? this repo?) | leaning deck |
| Q-06 | How to handle the 3h timebox | Decide what to cut and say so in the recording | open |

## To verify

- [ ] "Typesafe/Jev" calibrated decision model: correct name and what it does
- [x] Motor claims triage and fraud: see [motor-claims-triage-and-fraud.md](../02-research/motor-claims-triage-and-fraud.md)
- [ ] GDPR (UK/EU) and US rules on sharing claims data with a vendor for model training; explainability rules for automated decisions (e.g. UK GDPR Art. 22, FCA Consumer Duty)
- [ ] Is there a Gong MCP
- [ ] Hugging Face: open models or datasets for insurance claims / fraud
- [ ] Real competitor examples of automatic claims triage, for realistic positioning
