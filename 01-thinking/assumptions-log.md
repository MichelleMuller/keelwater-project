# Assumptions log

The brief allows us to invent detail as long as it's flagged. Status: **open** (untested), **validated**, **rejected**, **invented** (deliberately made up for the exercise).

| ID | Assumption | Source | How to test | Status |
|---|---|---|---|---|
| A-01 | No table view exists today; handlers sort claims one by one. **Basis for the bulk sorting narrative** | Inferred from bulk sorting taking ~12 weeks | Ask tech lead; review bulk sorting spec | **adopted** |
| A-02 | Bulk sorting required a new API returning all claims at once | Inferred | Ask tech lead | open |
| A-03 | Fraud detection is the main thing blocking the 6 deals | Hypothesis; brief says deals "mention" automatic sorting | Gong / CRM notes on the 6 deals; 15-min calls with AEs | open. Research suggests reframing: speed is the main ask, fraud screening is what makes speed safe |
| A-04 | ~80%+ of claims are relatively easy to sort | Derived from 15% >4h | Per-customer distribution of time-to-sort and pile | open |
| A-05 | 3.4% re-sort rate is a fair error benchmark for automation | Human baseline | Break down by direction; confirm re-sorts reflect errors, not new info arriving | open |
| A-06 | Long sort times are driven by complex/suspicious claims, not queue wait or missing info | Inferred | Split wait time vs touch time; cross with pile | superseded by A-13 |
| A-07 | Customer claim mix varies widely (some ~99% simple, some mostly complex) | Brainstorm | Per-customer breakdown | open |
| A-08 | Claims data contains PII; Keelwater can't train on raw data by default | Domain knowledge | Check contracts / DPA; legal | open |
| A-09 | Insurers are mostly Microsoft shops (Teams recordings available) | Brainstorm | CS confirmation | open |
| A-10 | Some carriers already run their own fraud models | Hypothesis | Customer interviews; market research | open |
| A-11 | The prototype is reusable as a starting point | Unknown | Review with data team | open |
| A-12 | Rule-based logic is sufficient for the Simple pile | Brainstorm | Test rules against historical sorted claims | open |
| A-13 | Information-missing claims, not fraud, drive most of the 15% taking >4h | Research: missing info is the largest non-straight-through category in industry examples | Cross time-to-sort with pile and reason; sample 50 slow claims | open |
| A-14 | Most Keelwater customers already run a fraud model or vendor; Keelwater should integrate, not build | Research: ~80% of insurers use predictive fraud modelling (III) | Customer interviews; CSM survey | open |
| A-15 | For the problem we're solving, the slow end (the 15% of claims taking >4h) matters more than the typical claim (median 11 min) | Inferred from median vs tail, see [time-to-sort-distribution.md](../02-research/time-to-sort-distribution.md) | Real histogram (DQ-02); ask Sales/CS what pain the deals and accounts describe (SQ-01, CQ-01) | open |
| A-16 | The slow end holds most of the total handler time and customer waiting time | Illustrative curve fitted to median and >4h share | Split waiting vs working time (DQ-01); total time per bucket (DQ-10). May hold for waiting time but not handler time | open |

## Invented for the exercise

Track every invented data point, quote or org detail here so it can be flagged in the deck.

| ID | What | Where used |
|---|---|---|
| I-01 | Keelwater serves **motor claims** (car damage and repair) | Everywhere |
| I-02 | Pile 2 is defined mainly as "information missing" (plus complex) | Brainstorm, research, deck |
