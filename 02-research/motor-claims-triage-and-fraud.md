# Motor claims triage and fraud

**Question:** We're assuming Keelwater serves **motor (car damage/repair) claims**, and that sorting into three piles (1. simple → pay, 2. needs a closer look, 3. investigate) helps insurers with fraud. Is that true?

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

What triage optimises for, in order of how often it comes up in sources:

- **Cycle time:** how fast a claim gets resolved
- **Routing accuracy:** the claim reaches the right handler first time, and handlers sort consistently
- **Fraud referral:** suspicious claims go to investigation
- **Leakage:** avoiding overpaying on claims

**Keelwater's three piles (working definitions, revised 2026-10-16)**

| Keelwater pile (brief) | Criteria | Next action | Industry equivalent |
|---|---|---|---|
| **Simple** ("pay it quickly") | Low value, own damage only, no injury, clear cover, no prior-claim or fraud flag. e.g. cracked windscreen, £600 | Pay | Fast track / straight-through |
| **Needs a closer look** ("check the details first") | Needs a handler's judgement: third party / fault to determine, injury, disputed liability or cover, total loss, above authority limit, multiple parties. e.g. car through a house, £5,000, multiple claimants | Depends on the **reason code**: assign senior handler, supervisor sign-off, appoint engineer, establish fault | Standard + complex streams (desk adjuster / senior specialist) |
| **Suspicious** ("send it for investigation") | Fraud indicators: claim soon after policy start, inconsistent facts, damage that doesn't match the story, repeated claims (e.g. 7 claims in 3 months), theft | Refer to investigation | SIU referral |

**Missing information is a status, not a pile.** Any claim can be "waiting on claimant" (photo, police report, repair estimate). It's flagged on the claim with what's missing, and chasing it can be automated regardless of pile. A Simple claim missing a photo is still Simple once the photo arrives.

> Earlier versions defined pile 2 as "information missing". Revised after [§6](#6-is-pile-2-information-missing-research-2026-10-16): industry triage puts complexity and judgement in the middle stream.

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

**Where claims actually get stuck.** One worked example of 4,200 auto claims attributes non-straight-through claims to: data quality / missing info **20%**, adjuster review 30%, supervisor approval 8%, **SIU fraud flag 4%** ([Lorikeet](https://www.lorikeetcx.ai/articles/straight-through-processing-rate-practitioners-guide), vendor, illustrative). It calls missing or incorrect intake data "the largest addressable category" (addressable meaning fixable at intake; by size, adjuster review is bigger).

**So what:** by volume, fraud is a **small pile**; claims needing a handler's judgement (adjuster review, 30%) and claims waiting on information (20%) are **much bigger**. By value, fraud is **high per case**. That suggests:

- **Speed** (what handlers and claimants feel) comes mostly from piles 1 and 2, plus clearing missing information on any claim.
- **Money and risk** (what insurers' finance and fraud teams feel) sit in pile 3.
- The 15% of Keelwater claims taking >4h are more likely **complex or waiting-on-information** claims than fraud. To validate (A-13).

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
2. **Detecting missing information may be the biggest speed win.** Auto-detecting what's missing on any claim and prompting the claimant is low-risk and highly explainable. A strong candidate for the first automation. (Revised: missing information is a status across piles, not pile 2; see §6.)
3. **Integrate, don't build, the fraud score.** Most insurers already run fraud models or vendors. Keelwater's value is in pulling those signals into the sorting decision and making it explainable.
4. **Bulk sorting fits this story.** A table view with filters lets handlers clear the clean pile fast today, and the filters they use become the first rule set for automating it.

## 6. Is pile 2 "information missing"? (research 2026-10-16)

**Question:** the brief defines pile 2 as *"Needs a closer look: check the details first."* We've been treating it as "information missing". Is that how motor claims are triaged?

**Short answer: mostly no.** In industry triage the middle stream is about **complexity and judgement**, not missing data. Missing information is a **state a claim can be in** (in any pile), usually caught at intake before or alongside triage.

### How motor claims are usually triaged

Most sources describe three handling streams plus a fraud referral:

| Stream | Typical criteria | Keelwater pile |
|---|---|---|
| **Fast track / straight-through** | Low value, own damage only, no injury, clear cover, no prior-claim or fraud flag. Examples: windscreen, minor own damage | Simple |
| **Standard** | Routine third-party or repair claims needing normal desk handling | Needs a closer look |
| **Complex** | Injury, disputed liability or coverage, multiple parties, legal involvement, high reserve, total loss | Needs a closer look |
| **SIU referral** | Fraud indicators: inconsistent facts, suspicious timing, damage mismatch, duplicate claims | Suspicious |

Sources: [SwiftCase](https://swiftcase.co.uk/use-cases/insurance/) (vendor; "fast-track, standard and complex streams", each with its own SLA and authority level), [Regure](https://www.getregure.com/solutions/carriers/) (vendor; route by loss type, amount, expertise, workload; fraud to SIU), [Ocean Point Claims](https://oceanpoint.claims/core-guides/how-insurers-evaluate-claims-internally/) (desk adjuster within authority limits, escalation above it, SIU for red flags).

**How big is fast track?** One UK insurer (2.2M motor policies) defined its automatable segment as: under a loss-value threshold, no third-party injury, no coverage ambiguity, no prior-claim flag, no fraud flag at FNOL. That was **~58% of motor volume**; 80% of it then settled straight-through ([Mindmap Digital](https://www.mindmapdigital.ai/stories/uk-insurer-motor-claims-automation), vendor case study, directional).

### What actually puts a claim in the middle pile

What makes motor claims slow or need a handler, in rough order of how often sources cite it:

- **Third party involved / fault to determine.** Third-party claims run 40–60% longer than first-party ones ([Finantrix](https://www.finantrix.com/articles/comparing-first-party-vs-third-party-claims-handling-workflows), directional)
- **Injury.** Can't be valued until treatment and prognosis are clearer; takes longest
- **Disputed liability or coverage.** Statements, witnesses, dashcam, police report
- **Total loss.** Valuation, salvage, finance/lien paperwork
- **Above the handler's authority limit.** Supervisor sign-off adds a review step
- **Missing documents.** Photos, police report, repair estimate, medical records
- **Other parties in the chain (UK).** Accident and claims management companies and credit hire add delay and cost ([FCA motor claims multi-firm review, 2025](https://www.fca.org.uk/publication/multi-firm-reviews/motor-insurance-claims-analysis-multi-firm-review-2025.pdf), regulator)

Massachusetts commercial auto performance standards say every new notice must be screened for fraud warning signs, and **theft and arson always require detailed investigation** ([CAR standards](https://www.commauto.com/manuals/performstand/cm/pdf/2016/cmPrintable.pdf), regulator).

### Where missing information fits

- Vendors and insurers handle it **at intake**: digital FNOL forms validate fields in real time and trigger targeted follow-up requests before or as the claim is scored ([SwiftCase](https://swiftcase.co.uk/use-cases/insurance/), [Data Operatives](https://dataoperatives.com/insurer-fnol.html), both vendors).
- One routing design puts "Return for additional information" as its own path, checked before any other route ([example routing spec on GitHub](https://github.com/JK0321/auto-claims-next-action-routing-operator-v1), hobby project, illustrative only).
- A simple claim missing a photo is still simple once the photo arrives. A complex claim can be complete and still need a senior handler.

### So what for Keelwater

1. **Pile 2 should be "needs a handler's judgement"**, matching the brief ("check the details first") and industry's standard + complex streams. Not "information missing".
2. **Missing information is a status, not a pile.** Better modelled as a flag ("waiting on claimant: police report") that can sit on any claim. Detecting it and auto-requesting it is still a strong, low-risk first automation, and probably a big driver of the >4h tail (A-13).
3. **Pile 2 needs reason codes**, because the next action differs: chase claimant, assign senior handler, request supervisor approval, appoint engineer for total loss.
4. **The Simple criteria are well established** (low value, own damage, no injury, clear cover, no prior or fraud flag). A rule-based Simple pile (A-12) is consistent with industry practice.

## Open threads

- [ ] Find real figures for the share of motor claims that are straight-through vs referred (non-vendor source)
- [ ] Which fraud vendors are common in motor (e.g. Shift Technology) and do they expose scores via API
- [ ] UK GDPR Article 22 (solely automated decisions) after the Data (Use and Access) Act 2025: confirm current position
