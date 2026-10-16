# Research

Findings go in one file per stream. Since Keelwater is fictional, "internal" research is simulated: write down what we'd look for and invent plausible findings, flagged **[INVENTED]**.

| Stream | File | Type | Status |
|---|---|---|---|
| Discovery questions checked against the research: what's answered, what needs Keelwater data | [`discovery-answers.md`](discovery-answers.md) | Synthesis | **draft** |
| Internal data: per-customer breakdown, why claims take hours, re-sorts, tickets, bulk sorting rationale, prototype | [`internal-data.md`](internal-data.md) | Simulated **[INVENTED]**, with how we'd find it | **done (v1)** |
| Customer and deal signal (Gong / Teams, AE and CSM input) | [`customer-signal.md`](customer-signal.md) | Simulated, reconfirmed with market research | **done (v1)**: incl. what the 6 deals value |
| Competitor automatic sorting: features, models, positioning, failure points | `competitor.md` | Real market + invented competitor | not started |
| Time to sort: median vs tail, illustrative distribution, first data ask | [`time-to-sort-distribution.md`](time-to-sort-distribution.md) | Analysis of brief data | **done (v1)** |
| Motor claims triage and fraud: how claims are triaged, **the three pile definitions (§2)**, where claims get stuck, fraud scale and signals | [`motor-claims-triage-and-fraud.md`](motor-claims-triage-and-fraud.md) | Real | **done (v3, consolidated)** |
| Auto-sorting: decision order, data needed per pile, fraud score sources, how we'd build and roll it out | [`auto-sorting-requirements.md`](auto-sorting-requirements.md) | Real + design | **draft**: decisions AS-01 to AS-07 to work through |
| What examiners expect (US + UK) and the build checklist E-01 to E-14 | [`examiner-requirements.md`](examiner-requirements.md) | Real | **done (v1)**, to confirm with legal |
| Open models/datasets for claims and fraud (Hugging Face) | `open-models.md` | Real | not started |
| Regulation: data sharing, PII, explainability of automated decisions | see [`examiner-requirements.md`](examiner-requirements.md) | Real | explainability covered; data sharing for training still open |
| Synthetic claims dataset for a dry-run eval | `synthetic-data/` | Built | not started |
