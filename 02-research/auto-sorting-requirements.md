# Auto-sorting: what we need and how we'd build it

**Question:** what does Keelwater need in order to sort claims automatically into Simple, Needs a closer look and Suspicious, including a fraud score, and how would we build it?

**Short answer:** a **decision order with a safe default**, not one model. Check what's missing, run the fraud gate, check for complexity, and only call a claim Simple if it passes every check. Anything uncertain lands in Needs a closer look. The fraud score comes from the insurer's existing vendor; Keelwater combines it with its own rules and explains the result.

> Research 2026-10-16. Pile definitions: [motor-claims-triage-and-fraud.md §2](motor-claims-triage-and-fraud.md). Regulatory constraints: [examiner-requirements.md](examiner-requirements.md). Anything about Keelwater's data or architecture is **[INVENTED]** or an assumption.

---

## 1. The decision order

Each claim runs through four checks in order. The first one that fires decides the pile.

| Step | Check | Outcome if it fires |
|---|---|---|
| 0 | **Missing information:** are required fields and documents present for this claim type? | Status "waiting on claimant", what's missing, auto-request sent. The claim still gets a provisional pile |
| 1 | **Fraud gate:** fraud score above the customer's threshold, or a hard rule fires (theft, claim within X days of policy start, repeat claims) | **Suspicious**, with the reasons |
| 2 | **Complexity:** third party, injury, disputed liability or cover, total loss, above authority limit, multiple parties | **Needs a closer look**, with a reason code |
| 3 | **Simple criteria:** all met, value under the customer's threshold, fraud score below threshold, confidence high | **Simple** |
| — | Nothing above is conclusive | **Needs a closer look** (the safe default) |

**Why this order:**

- **The fraud gate runs before Simple.** A wrong "Simple" pays out fraud and is hard to reverse.
- **Simple is earned, not assumed.** A claim only gets there by passing every check.
- **The default is Needs a closer look.** It costs handler time, but it never pays out fraud and never labels an honest claimant suspicious.

## 2. Data needed per check

What each check needs, where it comes from, and whether Keelwater is likely to have it.

| Data | Used for | Source | Keelwater has it? |
|---|---|---|---|
| Claim type, date and place of loss, description, claimed amount | All checks | FNOL form | Yes **[assumed]** |
| Photos, police report, repair estimate, medical evidence | Missing info, complexity | Uploaded documents | Yes, unstructured **[assumed]** |
| Parties involved, third-party details, injury yes/no | Complexity | FNOL form + notes | Partly; often in free text |
| Policy start date, cover, excess, named drivers | Fraud gate, Simple | Insurer's policy system | Via integration, per customer |
| Handler authority limits | Complexity | Customer config | Needs adding |
| Prior claims by the same person, **within this insurer** | Fraud gate | Keelwater claims history | Yes **[assumed]** |
| Prior claims **across insurers** | Fraud gate | US: Verisk ClaimSearch. UK: CUE (run by MIB) | No. Insurer's subscription |
| Fraud score + reason codes | Fraud gate | Insurer's fraud vendor | No. Integrate |
| Image tampering / reused photos | Fraud gate | Vendor image forensics | No. Integrate |
| Telematics | Fraud gate | Insurer or telematics provider | No |
| Final outcome (paid, rejected, fraud confirmed) | Training and evaluation | Keelwater + insurer | Unknown (DQ-06) |

**Key gap:** the strongest fraud signals depend on data shared between insurers, which Keelwater can't hold. Access is restricted to approved insurer purposes (e.g. [ClaimSearch](https://www.verisk.com/products/claimsearch/) is credentialed users only; [CUE](https://www.mib.org.uk/for-professionals/insurers-and-brokers/) requires contributing claims data).

## 3. The fraud score

### Where it comes from

Most insurers already run a fraud model or vendor (~80% use predictive modelling, III). Keelwater should **consume** a score, not build one.

| Market | Common sources | What they return |
|---|---|---|
| US | [Verisk ClaimSearch](https://www.verisk.com/products/claimsearch/) (claims shared across 1,850+ contributors) and [Claim Scoring](https://www.verisk.com/products/claim-scoring/) | Match counts by party at FNOL; predictive score **with reason codes**; APIs for loss summary, match reports, image forensics, SIU triage ([developer portal](https://developerportal.verisk.com/solutions/anti-fraud)) |
| UK | [CUE](https://www.mib.org.uk/for-professionals/insurers-and-brokers/) (all reported motor, PI and home claims, via nominated suppliers such as CRIF), [Insurance Fraud Bureau](https://www.insurancefraudbureau.org/about-us/supporting-the-insurance-industry) and the Insurance Fraud Register | Claims history, concurrent and undisclosed claims; IFB entity checks and organised-fraud alerts |
| Both | Shift Technology, [FRISS](https://www.friss.com/press/friss-and-verisk-claims-uk-join-forces-to-combat-digital-media-fraud) | Fraud scores, claims analytics, image and document forensics |

### What Keelwater needs from it

- **Score** (0–1 or a band) and **reason codes**, so the sort can be explained
- **Model or vendor version and timestamp**, for the audit log
- A **threshold set per customer**, agreed with their fraud team
- A **fallback** when there's no vendor or the call fails: rules-only fraud gate, and the claim can't be Simple without a fraud check

### What Keelwater can add itself

Rules on data it holds, explainable on their own:

- Claim filed within X days of policy start
- Repeat claims by the same person or vehicle within the insurer's book (e.g. 7 claims in 3 months)
- Same phone, address, bank details or repairer across unrelated claims
- Theft (always investigate)
- Story vs damage inconsistencies in free text, flagged for a human, never decided by AI alone

## 4. How we'd build it

| Component | Approach | Why |
|---|---|---|
| **Extraction** | LLM reads FNOL notes and documents into structured fields (parties, injury, police report present) with the source text quoted | Most complexity signals sit in free text. The LLM extracts; it doesn't decide |
| **Missing-info detector** | Checklist of required items per claim type, run on extracted fields | Deterministic, easy to explain, safe to automate first |
| **Rules engine** | Configurable rules per customer for the fraud gate, complexity and Simple. Seeded from bulk sorting filter usage | Explainable by construction; matches industry practice for Simple |
| **Fraud score integration** | API connectors to the customer's vendor; score, reason codes and version stored per claim | Integrate, don't build |
| **Decision + explanation** | Applies the decision order, returns pile, reason codes, evidence and confidence | Every sort can be explained to the customer and the regulator |
| **Audit log** | Every input, rule fired, score, model version, suggestion, and the human's final decision | What examiners ask for |
| **Learning loop (later)** | Once outcomes are labelled, an ML model can propose rule changes or rank claims within a pile | Only after the rules and audit trail are proven |

### Rollout

1. **Shadow mode:** the system sorts silently alongside handlers. Compare with their decisions.
2. **Suggest:** handlers see the suggested pile and reasons, then confirm or override. Overrides are logged and reviewed.
3. **Auto-route:** above an agreed confidence, claims move to a pile automatically. Humans can still move them.
4. **Auto-pay Simple:** only for customers who opt in, under their value threshold, after the error rate has been agreed and met.

The system never auto-denies or auto-reduces a claim. See [examiner-requirements.md](examiner-requirements.md).

### How we'd measure it

- **Benchmark:** the 3.4% human re-sort rate (A-05)
- **Errors weighted by direction:** Suspicious sorted as Simple is the costly miss; Simple sorted as Suspicious costs time and goodwill and needs a fairness check
- **Per customer**, since the claim mix varies widely (A-07)
- **Speed:** share of claims sorted without a human, time to sort, and the size of the >4h tail
- **Time to first look:** from claim arrival to the first action on it, by a handler or the system. Kept separate from time to sort (which starts when a handler first opens the claim, A-18) so both stay clean. Auto-sorting runs around the clock, so claims arriving overnight or at weekends can be sorted and have missing information requested before a handler starts work. This is the wait the claimant feels
- **Override rate** in suggest mode, and why handlers overrode

## 5. Questions to work through together

| ID | Question | Options | Leaning / decision |
|---|---|---|---|
| AS-01 | Where does the fraud score come from? | Customer's own vendor (integrate) · Keelwater builds one · Rules only | **Decided 2026-10-16:** integrate the customer's vendor, with Keelwater rules as fallback |
| AS-02 | Can a claim be Simple without a fraud check? | Never · Only under a low value threshold · Customer decides | **Decided 2026-10-16:** never |
| AS-03 | What do we automate first? | Missing-info detection · Simple suggestions · Closer look reason codes · Suspicious flags | **Missing-info flagging decided in scope (2026-10-16).** Leaning: first, then Simple suggestions. Pitch it as part of sorting, since buyers ask for sorting, not for missing-info detection |
| AS-04 | Does Keelwater ever trigger payment for Simple claims, or only sort them? | Sort only · Auto-pay with opt-in | **Decided 2026-10-16:** sort only for v1; payment stays with the insurer |
| AS-05 | One rule set for everyone, or per customer? | Global defaults + per-customer thresholds · Fully per customer | Global defaults + per-customer thresholds |
| AS-06 | Where does the LLM sit? | Extraction only · Extraction + suggested reason codes · Decision | Extraction + suggested reason codes, never the decision |
| AS-07 | What do we evaluate on before customer data is available? | Synthetic claims · One design-partner customer's history · Both | Both |
