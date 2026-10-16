# Assumptions log

The brief allows us to invent detail as long as it's flagged. Status: **open** (untested), **validated**, **rejected**, **invented** (deliberately made up for the exercise).

| ID | Assumption | Source | How to test | Status |
|---|---|---|---|---|
| A-01 | No table view exists today; handlers sort claims one by one. **Basis for the bulk sorting narrative** | Inferred from bulk sorting taking ~12 weeks | Ask tech lead; review bulk sorting spec | **adopted** |
| A-02 | Bulk sorting required a new API returning all claims at once | Inferred | Ask tech lead | open |
| A-03 | **Customers want triage for speed and routing: every claim reaches the right handler first time.** Sorting doesn't detect fraud; it makes sure suspicious claims don't slip into fast payment, and that the large majority of clean claims aren't held up behind them. Fraud screening is what makes speed safe, not the main ask. *(Reframed 2026-10-16 from: ~~"Fraud detection is the main thing blocking the 6 deals"~~)* | Research: industry triage optimises for cycle time and routing first; any fraud flag pulls a claim out of fast track ([research §1](../02-research/motor-claims-triage-and-fraud.md)). Brief only says deals "mention" automatic sorting | Gong / CRM notes on the 6 deals; 15-min calls with AEs (SQ-01, SQ-02); CS account reviews (CQ-01): do buyers describe speed, headcount or fraud? | open |
| A-04 | ~80%+ of claims are relatively easy to sort | Derived from 15% >4h | Per-customer distribution of time-to-sort and pile | open |
| A-05 | 3.4% re-sort rate is a fair error benchmark for automation | Human baseline | Break down by direction; confirm re-sorts reflect errors, not new info arriving | open |
| A-06 | Long sort times are driven by complex/suspicious claims, not queue wait or missing info | Inferred | Split wait time vs touch time; cross with pile | superseded by A-13 |
| A-07 | Customer claim mix varies widely (some ~99% simple, some mostly complex) | Brainstorm | Per-customer breakdown | open |
| A-08 | Claims data contains PII; Keelwater can't train on raw data by default | Domain knowledge | Check contracts / DPA; legal | open |
| A-09 | Insurers are mostly Microsoft shops (Teams recordings available) | Brainstorm | CS confirmation | open |
| A-10 | Some carriers already run their own fraud models | Hypothesis | Customer interviews; market research | open |
| A-11 | The prototype is reusable as a starting point | Unknown | Review with data team | open |
| A-12 | Rule-based logic is sufficient for the Simple pile | Brainstorm | Test rules against historical sorted claims | open |
| A-13 | Complex claims and claims waiting on information, not fraud, drive most of the 15% taking >4h | Research: in one industry example, adjuster review (30%) and missing info (20%) dwarf fraud flags (4%) among non-straight-through claims. Internal signal agrees **[INVENTED]**, see I-03 | Cross time-to-sort with pile and reason; sample 50 slow claims | open |
| A-14 | Most Keelwater customers already run a fraud model or vendor; Keelwater should integrate, not build | Research: ~80% of insurers use predictive fraud modelling (III) | Customer interviews; CSM survey | open |
| A-15 | For the problem we're solving, the slow end (the 15% of claims taking >4h) matters more than the typical claim (median 11 min) | Inferred from median vs tail, see [time-to-sort-distribution.md](../02-research/time-to-sort-distribution.md) | Real histogram (DQ-02); ask Sales/CS what pain the deals and accounts describe (SQ-01, CQ-01) | open |
| A-16 | The slow end holds most of the total handler time and customer waiting time | Illustrative curve fitted to median and >4h share | Split waiting vs working time (DQ-01); total time per bucket (DQ-10). May hold for waiting time but not handler time | open |

## Invented for the exercise

Track every invented data point, quote or org detail here so it can be flagged in the deck.

| ID | What | Where used |
|---|---|---|
| I-01 | Keelwater serves **motor claims** (car damage and repair) | Everywhere |
| I-02 | ~~Pile 2 is defined mainly as "information missing" (plus complex)~~ **Revised 2026-10-16:** pile 2 = needs a handler's judgement (complex: third party, injury, disputed liability/coverage, total loss, above authority), with reason codes. Missing information is a status flag on any claim, not a pile. See [research §6](../02-research/motor-claims-triage-and-fraud.md) | Brainstorm, research, deck |
| I-03 | Internal signal from Gong calls, Teams recordings and CSM/AM sessions: speed comes from piles 1 and 2 plus missing info; money and risk sit in pile 3; the >4h tail is complex or waiting-on-information claims | [customer-signal.md](../02-research/customer-signal.md), research §2, deck |
