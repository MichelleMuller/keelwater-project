# Motor claims triage and fraud

**Question:** We're assuming Keelwater serves **motor (car damage/repair) claims**, and that sorting into three piles (1. simple → pay, 2. information missing, 3. investigate) helps insurers with fraud. Is that true?

**Short answer:** Partly. In industry practice, triage is mainly a **speed and routing** tool (getting each claim to the right handler first time). Fraud screening is one of its inputs, and its most important job is as a **gate on the fast-track pile**. Sorting doesn't detect fraud by itself. What it does is make sure suspicious claims don't slip into fast payment, and that the large majority of clean claims aren't held up behind them.

> Status: desk research on 2026-10-15. Several sources are vendor blogs and say so; treat their figures as directional. Real figures are marked with sources; anything for Keelwater is **[INVENTED]**.

---

## 1. What triage is for

Industry triage at first notice of loss (FNOL) usually scores each claim on four things ([Hesper AI](https://gethesperai.com/blog/claims-triage-automation-guide/), vendor):

- **Severity:** likely cost
- **Complexity:** parties, coverages, investigation steps
- **Fraud risk:** often from a specialist vendor using cross-insurer data
- **Line of business**

It then routes to one of roughly four outcomes: straight-through payment, fast-track handler, senior specialist, or SIU (special investigations unit) referral. **Any fraud flag pulls a claim out of straight-through processing.**

What it optimises for, in order of how often it comes up: **cycle time**, routing accuracy and consistency across handlers, fraud referral, leakage (overpaying).

**Mapping to Keelwater's three piles**

| Keelwater pile (brief) | Our working definition | Industry equivalent |
|---|---|---|
| Simple | Clean, low value, all info present → pay | Straight-through / fast track |
| Needs a closer look | **Information missing** (plus complex: multi-party, high value) | Desk adjuster / senior specialist |
| Suspicious | Fraud signals → investigate | SIU referral |

> ⚠️ Our definition of pile 2 ("information missing") is narrower than the brief's ("check the details first"). Industry splits this into *missing info* and *complex*. Worth keeping both inside pile 2 with a reason code, since the next action differs: chase the claimant vs assign a senior handler.

## 2. How big is fraud, relative to everything else?

| Figure | Source |
|---|---|
| UK insurers detected **£576M** of motor fraud in 2024 across **51,700 cases**, 53% of all detected general insurance fraud cases | ABI via [Insurance Edge](https://insurance-edge.net/2025/11/17/claims-fraud-theres-a-lot-of-it-about-says-abi/) |
| That's roughly **£11k per detected motor fraud case** (our arithmetic) | derived |
| Total UK detected general insurance fraud: £1.16bn, 98,400 cases (2024) | ABI, as above |
| US insurance fraud estimated at **$308.6bn/year** | Coalition Against Insurance Fraud, via [Hesper AI](https://gethesperai.com/blog/claims-triage-automation-guide/) |
| Fraud is ~**10%** of US P&C incurred losses and adjustment expenses | Insurance Information Institute, via [Wikipedia](https://en.wikipedia.org/wiki/Insurance_fraud) |
| **Soft (opportunistic) fraud**, inflating a real claim, is more common than **hard fraud** (staged or invented losses) | [Wikipedia](https://en.wikipedia.org/wiki/Insurance_fraud) |
| ~80% of insurers use predictive modelling for fraud (up from 55% in 2018) | III, via [Hesper AI](https://gethesperai.com/blog/claims-triage-automation-guide/) |

**Where claims actually get stuck.** One worked example of 4,200 auto claims attributes non-straight-through claims to: data quality / missing info **20%**, adjuster review 30%, supervisor approval 8%, **SIU fraud flag 4%** ([Lorikeet](https://www.lorikeetcx.ai/articles/straight-through-processing-rate-practitioners-guide), vendor, illustrative). It calls missing or incorrect intake data "the largest addressable category."

**So what:** by volume, fraud is a **small pile**; missing information is a **much bigger** one. By value, fraud is **high per case**. That suggests:

- **Speed** (what handlers and claimants feel) comes mostly from piles 1 and 2.
- **Money and risk** (what insurers' finance and fraud teams feel) sit in pile 3.
- The 15% of Keelwater claims taking >4h are more likely **information-missing** claims than fraud. To validate (A-06).

## 3. Common motor fraud signals

From [Fraud Conference News](https://www.fraudconferencenews.com/home/spotting-signs-auto-insurance-fraud):

- **Timing:** claim shortly after policy inception (sometimes within minutes)
- **Claimant:** excluded drivers hidden, vehicle use misstated, phantom passengers, statements that contradict each other or the evidence, prior injury claims
- **Vehicle / damage:** damage inconsistent with the reported incident, or pre-existing; injury claims from low-speed impacts
- **Repair:** inflated repair estimates, inflated storage and hire charges
- **Injury:** medical bills out of proportion to vehicle damage, same clinics or solicitors recurring
- **Staged accidents:** deliberately caused or invented collisions (hard fraud)

Many of these need data Keelwater may not hold: cross-insurer claim history, telematics, repair invoices. **Keelwater probably can't be the fraud model; it can be the place where fraud signals are combined, shown and acted on.** To validate with customers (A-10).

## 4. Regulation and explainability

- **US:** the NAIC model bulletin on AI (adopted by ~25 states + DC) doesn't ban AI in claims. It requires documented governance: testing, bias review, vendor oversight, ready for examiners ([Insurance Edge](https://insurance-edge.net/2026/07/17/why-claims-triage-is-the-new-compliance-battleground/)).
- **EU AI Act:** motor claims triage isn't automatically "high-risk" (life/health underwriting is). But a system that can deny or reduce a claim is likely to be treated as high-stakes, so documentation, testing and human oversight are the safe default (same source).
- **UK:** FCA Consumer Duty requires good customer outcomes and evidence of them. Complaints (and Financial Ombudsman decisions) are a key indicator, and AI-assisted decisions and their explanations must meet customer expectations ([Mind Foundry](https://mindfoundry.ai/blog/impact-of-uk-and-eu-ai-regulations-on-insurers)).
- **What examiners ask for:** logs of what was detected, from which evidence, at what confidence, and why the claim was routed where it was.

**Implications for Keelwater**

- Suggest first, act later. Human confirms the pile; auto-action only above an agreed confidence, per customer.
- **Auto-routing to Suspicious is safer than auto-paying Simple.** A wrong "suspicious" costs time and goodwill; a wrong "simple" pays out fraud and is hard to reverse.
- Every suggestion carries **reason codes + evidence + confidence**, logged per claim.

## 5. What this changes in our thinking

1. **Reframe the fraud hypothesis.** Not "customers want automatic sorting to catch fraud". More likely: *"customers want clean claims paid faster, and need confidence that speeding up doesn't let fraud through."* Fraud screening is the **licence to automate** the simple pile.
2. **Pile 2 (information missing) may be the biggest speed win.** Auto-detecting what's missing and prompting the claimant is low-risk and highly explainable. A strong candidate for the first automation.
3. **Integrate, don't build, the fraud score.** Most insurers already run fraud models or vendors. Keelwater's value is in pulling those signals into the sorting decision and making it explainable.
4. **Bulk sorting fits this story.** A table view with filters lets handlers clear the clean pile fast today, and the filters they use become the first rule set for automating it.

## Open threads

- [ ] Find real figures for the share of motor claims that are straight-through vs referred (non-vendor source)
- [ ] Which fraud vendors are common in motor (e.g. Shift Technology) and do they expose scores via API
- [ ] UK GDPR Article 22 (solely automated decisions) after the Data (Use and Access) Act 2025: confirm current position
