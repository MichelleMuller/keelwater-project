# Discovery questions: what the research answers

Going through the questions from the brainstorm ([brainstorm-organised.md §2](../01-thinking/brainstorm-organised.md)) one by one: what the research already answers, and what only Keelwater's own data can answer.

**Status key:** ✅ answered by research · 🟡 partly answered · 🔒 needs Keelwater internal data (simulated in this exercise, flagged **[INVENTED]** if we fill it in)

> 2026-10-16. Sources are in the linked research files.

---

## 1. What's the main problem per customer? Why do some claims take hours? What's the full claim lifecycle, sort → paid? 🟡

**Lifecycle (answered by research):**

1. **First notice of loss:** claim reported by form, phone, email or broker
2. **Intake and validation:** fields and documents checked; missing information requested
3. **Triage:** severity, complexity and fraud scored; claim sorted into fast track, standard/complex or investigation
4. **Handling, by pile:**
   - Simple: verify cover, pay
   - Closer look: establish fault and cover, value the damage (estimate, engineer, total loss valuation), supervisor sign-off above authority limits
   - Suspicious: investigation unit; claim paid, reduced or denied by a human
5. **Settlement and payment**

Sources: [motor-claims-triage-and-fraud.md §1–2](motor-claims-triage-and-fraud.md), [auto-sorting-requirements.md](auto-sorting-requirements.md). The brief only measures **step 3**: "time to sort".

**Why some claims take hours (answered by research, to confirm with data):** third party / fault to determine, injury, disputed liability or cover, total loss, above the handler's authority limit, missing documents. Fraud flags are a small share (4% of claims that don't go straight through in one example). Part of the >4h tail may also be queue time and out-of-hours arrival (DQ-01). See A-13.

**Main problem per customer (🔒):** research says customers differ by claim mix (simple-heavy, complex-heavy, fraud-heavy), so the main problem will too. Which customers are which needs Keelwater data (DQ-03).

## 2. Breakdown per customer of volume, time to sort, and >4h share 🔒

Not answerable by research. Needs Keelwater data (DQ-02, DQ-03). What we know from the brief: 2.1M claims a year across ~180 customers (~11.7k each on average), median 11 min, 15% over 4h. The real histogram is the first ask ([time-to-sort-distribution.md](time-to-sort-distribution.md)).

## 3. The 3.4% re-sorts: which direction, and which transitions are most common? 🔒 (research gives the framing)

Direction needs Keelwater data (DQ-05). Research tells us **which directions matter**:

| Re-sort | Cost | Why |
|---|---|---|
| Simple → Suspicious | **Highest** | Fraud may already have been paid out |
| Closer look → Suspicious | High | Fraud got through first-pass checks |
| Simple → Closer look | Medium | Claim was under-assessed; possible overpayment |
| Suspicious → Simple / Closer look | Time and goodwill; fairness check | An honest claimant was delayed and profiled |
| Closer look → Simple | Low | Handler time wasted |

A re-sort also isn't always an error: new information can arrive (police report, engineer's report). We'd need to split "wrong first time" from "new information" (A-05).

## 4. What's in the ~40 support tickets: sorting in general, or doing many at once? 🔒

Not answerable by research. Needs a thematic analysis of the tickets (SUQ-01, SUQ-02), a good AI task. Context: ~40 tickets across 180 customers in 6 months is low, which suggests the pain is concentrated in a few accounts.

## 5. Why was bulk sorting prioritised? What was validated, which customers are lined up? 🔒

Not answerable by research. Needs product leadership and the original decision record (PQ-01). Our working assumption is that no table view exists today, so handlers sort one claim at a time (A-01).

## 6. What's in the prototype: model type, training data, why it stopped, can customers see it? 🔒

Not answerable by research. Needs the data team (DQ-07, DQ-08, PQ-02). Research tells us **what to check it against**: can every prediction be explained with reasons? Was it trained on outcomes or on handler decisions? Does it handle the fraud gate? See [examiner-requirements.md](examiner-requirements.md).

## 7. Deterministic vs probabilistic: is any incorrect sort acceptable? Is this a good LLM use case? ✅

- **Some wrong sorts are acceptable.** Humans re-sort 3.4% today. The bar is to match or beat that, **weighted by direction** (see question 3), agreed per customer before go-live.
- **Some errors are never acceptable:** auto-denying or reducing a claim. A human always decides adverse outcomes ([examiner-requirements.md §4](examiner-requirements.md)).
- **The decision should be rules plus scores, not an LLM.** Rules are explainable by construction, and industry triage uses rules for the fast track.
- **LLMs fit extraction:** reading free-text notes and documents into structured fields (parties, injury, police report present), with the source quoted. They can also suggest reason codes for a human. Not the final decision (AS-06).

Sources: [auto-sorting-requirements.md §4](auto-sorting-requirements.md), [examiner-requirements.md](examiner-requirements.md).

## 8. Same for all customers, or configurable per customer? ✅

**Global defaults, plus per-customer settings.** Customers differ on:

- Claim mix (some ~99% simple, others mostly complex, A-07)
- Value thresholds for Simple, and handler authority limits
- Fraud vendor and fraud score threshold
- Appetite for automation (suggest only vs auto-route)
- Regulator (US state rules vs UK) (A-17)

Industry triage tools are configured the same way: rules per insurer, separate SLAs and authority levels per stream (AS-05).

## 9. Do carriers already have fraud models? What signals do they use? ✅

- **Yes, most do.** ~80% of insurers use predictive modelling for fraud (III).
- **Sources:** US: Verisk ClaimSearch and Claim Scoring. UK: CUE (MIB), Insurance Fraud Bureau and the Insurance Fraud Register. Both: Shift Technology, FRISS.
- **Signals:** claim soon after policy start, prior and concurrent claims across insurers, contradictory statements, damage that doesn't match the story, inflated repair or hire costs, recurring clinics or solicitors, staged accidents, reused or edited photos.
- **Decision AS-01:** integrate the customer's vendor, with Keelwater rules as a fallback.

Sources: [motor-claims-triage-and-fraud.md §4](motor-claims-triage-and-fraud.md), [auto-sorting-requirements.md §3](auto-sorting-requirements.md). Which vendors **Keelwater's** customers use is still open (A-14).

## 10. What does the competitor offer, how do they position it, where does it fail? 🟡

The brief's competitor is fictional. The real market splits into four types of product (2026 comparison sites, directional):

| Type | Examples | Positioning | Where it falls short |
|---|---|---|---|
| End-to-end claims automation | Sprout.ai, Five Sigma | "Resolve most claims automatically"; triage, coverage checks, fraud and settlement in one | Newer platforms; long implementations; harder to prove explainability across the whole flow |
| Fraud and decisioning | Shift Technology, FRISS | Fraud detection, coverage and liability support | Broad scope means long implementation; modules bought separately |
| Photo damage assessment | Tractable, CCC | Instant damage estimates and repair-vs-total-loss from photos | Only sees visible damage; a module, not a workflow; CCC brings ecosystem lock-in |
| Core claims systems | Guidewire, Duck Creek | System of record with AI add-ons | Triage comes from marketplace partners, not built in |

Sources: [Rework 2026 guide](https://resources.rework.com/tools/ai-tools/best-ai-tools-for-insurance-claims-2026), [AI Insurance Tools](https://insuranceaitools.com/guides/ccc-vs-tractable-vs-claim-genius/), [Sprout.ai](https://sprout.ai/), [AIPicksy](https://aipicksy.com/compare/ai-insurance-claim-analysis-tools).

**Possible gap for Keelwater:** it's already where handlers spend their day. Competitors either replace the claims system or add a module beside it. Keelwater can sort **inside the workflow**, with fraud scores from the vendor the insurer already uses and an explanation per claim. What the specific competitor in the brief does is still open (SQ-03).

---

## Summary

| # | Question | Status |
|---|---|---|
| 1 | Main problem, why hours, lifecycle | 🟡 Lifecycle and causes answered; per-customer needs data |
| 2 | Per-customer breakdown | 🔒 |
| 3 | Re-sort direction | 🔒 (framing answered) |
| 4 | Support tickets | 🔒 |
| 5 | Why bulk sorting was prioritised | 🔒 |
| 6 | The prototype | 🔒 (what to check answered) |
| 7 | Deterministic vs probabilistic, LLM fit | ✅ |
| 8 | Same for all or configurable | ✅ |
| 9 | Carrier fraud models and signals | ✅ |
| 10 | Competitor | 🟡 Market answered; the brief's competitor is fictional |
