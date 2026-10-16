# Internal data: what Keelwater's own data and people told us

**Everything in this file is [INVENTED]** for the exercise. Each finding says **how we would have found it**, so the method is real even where the numbers aren't. Numbers are built to stay consistent with the brief (2.1M claims, ~180 customers, median 11 min, 15% over 4h, 3.4% re-sorts, ~40 tickets).

> 2026-10-16. Answers the 🔒 questions in [discovery-answers.md](discovery-answers.md).

---

## 1. Per-customer breakdown and the main problem per customer

**How we found it:** data team query of the claims table for the last 12 months, grouped by customer; customers clustered by claim mix (DQ-02, DQ-03).

| Segment | Customers | Share of claims | Claims per insurer per year | Median time to sort | Share over 4h | Share of all >4h claims | Main problem |
|---|---|---|---|---|---|---|---|
| **Simple-heavy** (large direct personal motor insurers) | ~60 | 55% (~1.16M) | ~19k | 6 min | 7% | 25% | Handler effort on a very large clean pile |
| **Mixed** (regional and mid-size insurers) | ~80 | 33% (~690k) | ~8.7k | 15 min | 20% | 43% | Claims waiting on information and third-party fault |
| **Complex-heavy** (fleet, commercial, specialist, broker-led) | ~40 | 12% (~250k) | ~6.3k | 40 min | 40% | 31% | Getting complex claims to the right expert, with confidence fraud is caught |

Weighted, this gives ~15% over 4h, matching the brief.

- **The largest accounts are simple-heavy**, as expected: simple claims are the most common, and large personal motor insurers handle the most claims. Even at a 7% slow rate, their volume makes them a quarter of the slow tail.
- **Mixed customers hold the biggest share of the slow tail (43%).**
- **Complex-heavy customers are slow most often** (40% over 4h) but handle fewer claims each.

> Revised 2026-10-16: an earlier version had complex-heavy insurers as the largest accounts (~28k claims each) and simple-heavy as the smallest (~8.6k). Michelle flagged that this contradicts how the market works.

## 2. Why some claims take hours

**How we found it:** data team pulled a random sample of 200 claims that took over 4h. An LLM classified each from the handler notes and claim history; the PM checked a quarter of them by hand (DQ-04).

| Cause | Share of >4h claims |
|---|---|
| Waiting on information from the claimant | 48% |
| Third party / fault to determine | 28% |
| Injury involved | 15% |
| Fraud check or referral | 6% |
| Other | 3% |

> Revised 2026-10-16: an earlier version listed "Above the handler's authority limit" at 7% (with info 44%, third party 26%, injury 14%). Authority limits apply when a claim is **paid**, not when it's sorted, so they can't explain slow sorting (A-20). The 7% was spread across the other causes in proportion.

**What "time to sort" measures (DQ-01, A-18):** elapsed clock time from when a claim **arrives** to when it's sorted, as the brief says. It includes queue time. Queue time barely shows up as a cause here because customers' handling teams work across time zones and pick claims up quickly (A-22); the little that remains sits in "Other". So a claim over 4h is mostly one a handler opened but couldn't sort: waiting on information, working out fault, or assessing an injury.

> Revised 2026-10-16: an interim version measured time to sort from when a handler first opened the claim. Reverted, because the brief says "from a claim arriving". The original "arrived out of hours, sat in the queue" category (14%) stays out: with teams across time zones (A-22), overnight queueing isn't a major cause. ⚠️ The brief's 11-minute median from arrival isn't realistic for queue time plus reading and deciding; flagged in the [fact sheet](../00-brief/fact-sheet.md).

**Why handlers wait for information before sorting (A-19):** Keelwater has no "waiting on claimant" status today, so a handler can't sort the claim and mark it as blocked. They leave it unsorted until the information arrives. Missing-information flagging fixes this.

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

**What reviewing the prototype adds (2026-10-16).** The prototype didn't cause this decision: it was shelved a year before bulk sorting was prioritised. But reviewing it now **confirms bulk sorting should ship before auto-sorting**:

1. **Suggestions need somewhere to appear.** Without a table, a suggested pile appears one claim at a time and confirming it saves seconds. In a table, a handler filters to "suggested Simple", checks the reasons and confirms 50 at once. The suggest step of the rollout depends on bulk sorting (A-21).
2. **The prototype isn't ready anyway.** It was trained on sample data with rule-made labels (§6). Bulk sorting ships in 6 weeks.
3. **Bulk sorting produces what the prototype lacked.** Filters handlers actually use become the first rules; their confirmations and overrides become real, labelled Keelwater data.

So customers asked for bulk sorting, and it's also the foundation automated sorting needs.

## 6. The shelved prototype

**How we found it:** interview with the data scientist who built it, review of the notebooks and model repo (DQ-07, DQ-08, PQ-02).

| | |
|---|---|
| **Model** | Classic ML: a gradient-boosted classifier |
| **Trained on** | A **public sample dataset** (the Kaggle car insurance claim data, ~10k US policies) with pile labels the data team **generated from simple rules**. Customer claims couldn't be used without consent and data agreements (A-08) |
| **Inputs** | Structured fields in the sample: claim amount, vehicle type and value, prior claims, years as a customer, licence revoked, record points. No free text, no fraud score, no third party or injury fields |
| **Accuracy** | High agreement with its own rule-made labels on held-out sample data. That only shows it can relearn the rules. **Never tested on real Keelwater claims** |
| **Explainability** | **Reasons per claim are possible.** For tree models, the features that pushed each claim towards a pile can be traced (e.g. "prior claims: 3" pushed it towards Suspicious). The data team showed this for a handful of claims; it isn't built into the prototype |
| **Why it stopped** | Data team moved to a reporting project; no product owner |
| **Shown to customers?** | No |

- **Useful as a concept, not something we can rely on.** It shows what a suggested pile with reasons could look like, which helps in customer sessions. It can't tell us how accurate auto-sorting would be: the data isn't Keelwater's, the labels came from rules, and it has none of the complexity or fraud signals.
- **On the per-claim reasons:** they explain what drove the *model's* suggestion, not why the claim is genuinely complex or suspicious. Related features can share or swap credit, and raw feature names need turning into reasons a handler understands. Good enough for a "why this suggestion" panel; checked by a human, never the basis for an adverse decision ([examiner-requirements.md](examiner-requirements.md)).
- **What's reusable:** the feature pipeline and the per-claim reason approach. **What isn't:** the model or its accuracy figure (A-11).
- **Recreated as working material:** [04-working-material/prototype](../04-working-material/prototype/results.md) rebuilds it on the Kaggle data, with per-claim reasons and an example of what the bulk sorting table would show.

> Revised 2026-10-16: an earlier version said the prototype was trained on ~600k real claims from 12 customers, labelled with handlers' piles, with 89% agreement and **no reasons per claim**. Michelle pointed out that a gradient-boosted model can trace which features drove each prediction, and suggested a sample-data prototype is more realistic for a team that had no product owner or customer data agreements.
