# What automated sorting needs for examiners

**Question:** Keelwater operates in the US and UK **[INVENTED, A-17]**. What will regulators and examiners expect from automated claim sorting, so we design around it from day one?

**Short answer:** the insurer stays accountable, but Keelwater is their **third-party AI vendor**, so examiners will ask the insurer for things only Keelwater can produce: documentation, validation results, drift monitoring, audit rights and a per-claim decision trail. Build those in, and **never let the system deny or reduce a claim on its own**.

> Research 2026-10-16. Not legal advice; to confirm with legal (LQ-01). Sources marked; secondary sources flagged.

---

## 1. Who's being examined

Examiners regulate **insurers**, not claims software vendors. But both US and UK regimes make insurers answer for AI they buy:

- **US:** the NAIC model bulletin says the insurer's AI programme must cover AI systems **"whether developed by the Insurer or a third-party vendor"**, and examiners may ask for due diligence on the vendor, the vendor contract, audits of the vendor and validation documentation ([NAIC model bulletin](https://content.naic.org/sites/default/files/inline-files/2023-12-4%20Model%20Bulletin%5FAdopted%5F0.pdf)).
- **UK:** firms remain responsible for outcomes under Consumer Duty whoever built the system, and a named senior manager is accountable under the Senior Managers regime ([AIRiskAware](https://airiskaware.com/insights/ai-insurance-uk-governance), secondary).

**So what:** if Keelwater can't hand over this evidence, it becomes a blocker in every enterprise sale. Done well, it becomes a selling point.

## 2. United States

| Rule | What it requires | Status |
|---|---|---|
| **NAIC model bulletin on insurers' use of AI** (Dec 2023) | Written AI programme covering claims and fraud detection: governance, risk controls, validation and testing, **drift monitoring**, data lineage, bias testing, record retention, vendor oversight | Adopted in ~28 jurisdictions as of Oct 2026 ([NAIC adoption map](https://content.naic.org/sites/default/files/legal-adoption-map-ai-model-bulletin.pdf)) |
| **Unfair claims settlement practices** (state laws based on the NAIC model act) | Prompt, fair investigation; no refusal to pay without reasonable investigation; a reasonable explanation for any denial | All states, in some form |
| **Colorado Regulation 10-1-1** (SB21-169) | Auto insurers using external data, algorithms or predictive models, **including in claims**: governance, model inventory, **quantitative bias testing**, monitoring, remediation, annual reporting; consumers get information to act on an adverse decision | Effective 15 Oct 2025 for auto ([Colorado DOI](https://doi.colorado.gov/for-consumers/sb21-169-protecting-consumers-from-unfair-discrimination-in-insurance-practices), [Debevoise](https://www.debevoise.com/insights/publications/2025/09/colorado-approves-extension-of-ai-regulation-to)) |
| **Florida HB 527 / SB 202** (2026) | AI can assist, but **can't be the sole basis to deny or reduce a claim**; a qualified human decides, with records and disclosure in denial letters | Passed the House 108–0, **died in the Senate** Mar 2026 ([Florida Senate](https://flsenate.gov/Session/Bill/2026/527)). A signal of where states are heading |
| **Texas HB 4635** (2025) | Disclose when a denial was based on AI, the basis, and how to appeal | Introduced, not enacted ([Texas Legislature](https://capitol.texas.gov/tlodocs/89R/billtext/pdf/HB04635I.pdf)) |

What examiners can request under the NAIC bulletin: the written programme, model inventory, data lineage, bias and validation testing, drift evaluations, and for vendors: due diligence, contracts (including **audit rights and cooperation with regulators**), and vendor audits.

## 3. United Kingdom

| Rule | What it requires | Status |
|---|---|---|
| **FCA ICOBS 8** | Handle claims **promptly and fairly**, keep the policyholder informed, **don't unreasonably reject** a claim ([FCA Handbook](https://handbook.fca.org.uk/handbook/icobs8)) | In force |
| **FCA Consumer Duty** | Good outcomes, evidenced. No unnecessary barriers in claims. AI mustn't make claims harder or worse for some customers, including vulnerable ones. FCA watches **motor claim settlement times** specifically ([Deloitte](https://www.deloitte.com/uk/en/blogs/ecrs/ai-called-to-duty-in-the-gi-sector.html), secondary) | In force |
| **UK GDPR Articles 22A–22D** (Data (Use and Access) Act 2025, s.80) | For **significant decisions made solely by automation**: tell the person, let them make representations, offer **human intervention**, let them **contest**. Stricter where special-category data (e.g. health, so injury claims) is involved ([legislation.gov.uk](https://www.legislation.gov.uk/ukpga/2025/18/section/80/enacted)) | Replaced Article 22 from 5 Feb 2026 ([AIRiskAware](https://airiskaware.com/insights/ai-insurance-uk-governance), secondary) |
| **ICO guidance on AI** | Regular checks that systems work as intended; human review must be **meaningful**, not rubber-stamping ([ICO](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-do-we-ensure-fairness-in-ai/what-is-the-impact-of-article-22-of-the-uk-gdpr-on-fairness)) | Guidance |

**Automation bias:** UK regulators have warned about handlers confirming AI decisions without real challenge ([Deloitte](https://www.deloitte.com/uk/en/blogs/ecrs/ai-called-to-duty-in-the-gi-sector.html)). A human clicking "approve" on every suggestion isn't meaningful human involvement.

## 4. What this means for which decisions we automate

| Automated action | Risk | Position |
|---|---|---|
| Flag missing information, request it | Low. Speeds the claim up | Automate |
| Sort into Simple and pay faster | Positive outcome for the claimant; the risk is the insurer's (fraud paid out) | Automate only above agreed thresholds, after the fraud gate |
| Route to Needs a closer look | Delays the claim; Consumer Duty watches settlement times | Automate, with reason codes and SLA tracking |
| Route to Suspicious | Delays the claim and profiles the claimant. Bias testing applies (Colorado); can feel adverse to the claimant | Suggest; auto-route only with reason codes, bias testing and quick human review |
| Deny or reduce a claim | Adverse, significant decision | **Never automated.** A qualified human decides |

## 5. Build checklist

What Keelwater's automated sorting must have, mapped to who asks for it.

| # | Requirement | Asked for by |
|---|---|---|
| E-01 | **Per-claim decision record:** inputs used, rules fired, fraud score + vendor version, suggested pile, reason codes, evidence, confidence, timestamp | NAIC (traceability), UK GDPR (information about the decision), unfair claims laws |
| E-02 | **Human decision logged** alongside the suggestion: who, when, confirmed or overrode, why | Florida-style human review; ICO meaningful involvement |
| E-03 | **Plain-language explanation** of why a claim was routed, for handlers and claimants | Consumer Duty, UK GDPR 22C, Colorado (info to act on adverse decisions) |
| E-04 | **No automated denial or reduction.** Hard constraint in the product | Florida direction, UK GDPR 22C, unfair claims laws |
| E-05 | **Contest and override path:** a claimant or handler can challenge a routing and get human review | UK GDPR 22C |
| E-06 | **Model and rule inventory with versions;** every rule or threshold change logged and reversible | NAIC (inventory, lifecycle), Colorado |
| E-07 | **Validation pack:** accuracy against the human baseline, by pile and direction, before go-live and on each change | NAIC (validation and testing) |
| E-08 | **Drift monitoring:** pile mix, override rate and error rate over time, per customer, with alerts | NAIC (drift), ICO (regular checks) |
| E-09 | **Bias testing:** Suspicious rates and outcomes by proxy groups (e.g. postcode); remediation process | Colorado 10-1-1, Consumer Duty |
| E-10 | **Customer controls:** per-customer thresholds, an off switch, opt-in for any auto-action | Insurer governance |
| E-11 | **Data lineage and retention:** where each input came from (FNOL, policy system, fraud vendor), how long it's kept | NAIC (lineage, retention), UK GDPR |
| E-12 | **Special-category data handling:** injury and health data flagged; no solely automated significant decision based on it | UK GDPR 22B |
| E-13 | **Vendor evidence pack for insurers:** model documentation, validation results, security, audit rights, regulator cooperation clause | NAIC (third-party vendor section) |
| E-14 | **Speed and outcome reporting:** time to sort and settle by pile, complaints, overturned routings | Consumer Duty, ICOBS 8 |

## Open questions

- [ ] Is routing a claim to Suspicious a "significant decision" under UK GDPR 22A? (LQ-01)
- [ ] Which US states do Keelwater's customers operate in, beyond the NAIC adopters and Colorado? (CQ)
- [ ] Do customers' fraud vendor contracts allow Keelwater to store and display the score and reason codes?
