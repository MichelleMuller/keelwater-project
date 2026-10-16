# Internal data: what Keelwater's own data and people told us

**Everything in this file is [INVENTED]** for the exercise. Each finding says **how we would have found it**, so the method is real even where the numbers aren't. Numbers are built to stay consistent with the brief (2.1M claims, ~180 customers, median 11 min, 15% over 4h, 3.4% re-sorts, ~40 tickets).

> 2026-10-16. Answers the 🔒 questions in [discovery-answers.md](discovery-answers.md).

---

## 1. Per-customer breakdown and the main problem per customer

**How we found it:** data team query of the claims table for the last 12 months, grouped by customer; customers clustered by claim mix (DQ-02, DQ-03).

| Segment | Customers | Share of claims | Claims/customer/year | Median time to sort | Share over 4h | Main problem |
|---|---|---|---|---|---|---|
| **Simple-heavy** (direct personal motor insurers) | ~110 | 45% (~945k) | ~8.6k | 6 min | 7% | Handler effort on a large clean pile |
| **Mixed** | ~55 | 35% (~735k) | ~13.4k | 14 min | 18% | Claims waiting on information and third-party fault |
| **Complex-heavy** (fleet, commercial, broker-led) | ~15 | 20% (~420k) | ~28k | 35 min | 30% | Getting complex claims to the right expert, with confidence fraud is caught |

Weighted, this gives ~15% over 4h, matching the brief. **The 15 complex-heavy customers are a small share of accounts but a large share of the slow tail**, and include most of the largest accounts.

## 2. Why some claims take hours

**How we found it:** data team pulled a random sample of 200 claims that took over 4h. An LLM classified each from the handler notes and claim history; the PM checked a quarter of them by hand (DQ-04).

| Cause | Share of >4h claims |
|---|---|
| Waiting on information from the claimant | 38% |
| Third party / fault to determine | 22% |
| Arrived out of hours, sat in the queue | 14% |
| Injury involved | 12% |
| Above the handler's authority limit | 6% |
| Fraud check or referral | 5% |
| Other | 3% |

**What "time to sort" measures (DQ-01):** clock time from claim arrival to pile assigned, including nights and weekends. So 14% of the slow tail is queue time, not difficulty.

This supports A-13: complex and waiting-on-information claims drive the tail, not fraud.

## 3. The 3.4% re-sorts

**How we found it:** data team query of pile-change history for claims re-sorted within 30 days (~71k claims a year), with the reason recorded on the claim (DQ-05).

| From → to | Share of re-sorts | Claims/year |
|---|---|---|
| Simple → Closer look | 48% | ~34k |
| Closer look → Simple | 14% | ~10k |
| Closer look → Suspicious | 17% | ~12k |
| Suspicious → Simple or Closer look | 12% | ~8.6k |
| **Simple → Suspicious** | **9%** | **~6.4k** |

- **~60% of re-sorts follow new information** (engineer's report, police report, a third party coming forward). **~40% were wrong first time.** So the true first-sort error rate is closer to **~1.4%** than 3.4% (A-05).
- **The costly miss:** ~6.4k claims a year go from Simple to Suspicious. About a third had already been paid when they were re-sorted.

## 4. The ~40 support tickets

**How we found it:** thematic analysis of the ticket text with an LLM, reviewed by the PM; tickets linked to customer accounts (SUQ-01, SUQ-02).

| Theme | Tickets |
|---|---|
| Sorting many claims at once / no list view | 22 |
| Wrong or inconsistent sorts between handlers | 9 |
| Asking directly for automatic sorting | 6 |
| Can't see why a claim is in a pile | 3 |

- **Concentrated:** the 40 tickets came from 14 customers; 3 customers filed 18 of them.
- **More than half are the bulk sorting problem**, which supports shipping it.

## 5. Why bulk sorting was prioritised

**How we found it:** reconstructed from the previous PM's spec, the Jira epic, and Gong and Teams recordings of the customer calls that led to it, summarised with AI and checked with the tech lead (PQ-01).

- **Prioritised ~6 months ago** after 5 large customers asked for a list view to clear claims faster.
- **Validated:** usability, in design sessions with 4 customers. **Not validated:** whether it reduces time to sort.
- **Lined up:** 3 beta customers, including the **top-10 account renewing in 5 months**.
- Confirms A-01: there's no table view today.

## 6. The shelved prototype

**How we found it:** interview with the data scientist who built it, review of the notebooks and model repo (DQ-07, DQ-08, PQ-02).

| | |
|---|---|
| **Model** | Classic ML: a gradient-boosted classifier |
| **Trained on** | ~600k claims from 12 customers who consented, labelled with the **pile handlers chose**, not final outcomes |
| **Inputs** | Structured fields only: claim type, amount, policy age, parties, prior claims within the insurer. No free text, no fraud score |
| **Accuracy** | 89% agreement with handlers overall; **weak on Suspicious** (catches ~55%) |
| **Explainability** | Feature importance across the model, but **no reasons per claim** |
| **Why it stopped** | Data team moved to a reporting project; no product owner |
| **Shown to customers?** | No |

- **Can it be shown to customers?** Only as a concept. Without per-claim reasons it fails the explainability constraint.
- **What's reusable:** the feature pipeline and the labelled dataset. **What isn't:** learning from handler decisions copies their mistakes, and it misses too much fraud to sit before the Simple pile (A-11).
