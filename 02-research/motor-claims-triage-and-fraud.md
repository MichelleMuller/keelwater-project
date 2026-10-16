# Motor claims triage and fraud

**Question:** Keelwater serves **motor claims** **[INVENTED]**. How are motor claims triaged, what goes in each of the three piles, and does sorting help insurers with fraud?

**Short answer:** Triage is mainly a **speed and routing** tool: getting each claim to the right handler first time. Sorting doesn't detect fraud. It makes sure suspicious claims don't slip into fast payment, and that the large majority of clean claims aren't held up behind them. Fraud screening is the **licence to automate** the Simple pile.

> Desk research 2026-10-15 and 2026-10-16. Several sources are vendor blogs and are marked; treat their figures as directional. Anything about Keelwater is **[INVENTED]**.

---

## 1. How motor claims are triaged

At first notice of loss (FNOL), insurers score each claim on ([Hesper AI](https://gethesperai.com/blog/claims-triage-automation-guide/), vendor):

- **Severity:** likely cost
- **Complexity:** parties, coverages, investigation steps
- **Fraud risk:** often from a specialist vendor using cross-insurer data
- **Line of business**

What triage optimises for, in order of how often it comes up in sources:

- **Cycle time:** how fast a claim gets resolved
- **Routing accuracy:** the claim reaches the right handler first time, and handlers sort consistently
- **Fraud referral:** suspicious claims go to investigation
- **Leakage:** avoiding overpaying on claims

Claims are then routed into three handling streams plus a fraud referral, each with its own SLA and authority level ([SwiftCase](https://swiftcase.co.uk/use-cases/insurance/), [Regure](https://www.getregure.com/solutions/carriers/), both vendors; [Ocean Point Claims](https://oceanpoint.claims/core-guides/how-insurers-evaluate-claims-internally/)). **Any fraud flag pulls a claim out of the fast track.**

**How big is the fast track?** One UK insurer (2.2M motor policies) defined its automatable segment as: under a loss-value threshold, no third-party injury, no coverage ambiguity, no prior-claim flag, no fraud flag. That was **~58% of motor volume**, and 80% of it then settled straight-through ([Mindmap Digital](https://www.mindmapdigital.ai/stories/uk-insurer-motor-claims-automation), vendor case study).

## 2. Keelwater's three piles

| Keelwater pile (brief) | Criteria | Next action | Industry stream |
|---|---|---|---|
| **Simple** ("pay it quickly") | Low value, own damage only, no injury, clear cover, no prior-claim or fraud flag. e.g. cracked windscreen, £600 | Pay | Fast track / straight-through |
| **Needs a closer look** ("check the details first") | Needs a handler's judgement: third party / fault to determine, injury, disputed liability or cover, total loss, above authority limit, multiple parties. e.g. car through a house, £5,000, multiple claimants | Depends on the **reason code**: assign senior handler, supervisor sign-off, appoint engineer, establish fault | Standard + complex |
| **Suspicious** ("send it for investigation") | Fraud indicators (see §4), plus theft, which always needs detailed investigation ([Massachusetts CAR standards](https://www.commauto.com/manuals/performstand/cm/pdf/2016/cmPrintable.pdf), regulator) | Refer to investigation | SIU referral |

**Missing information is a status, not a pile.** Any claim can be "waiting on claimant" (photo, police report, repair estimate). Insurers usually catch it at intake: digital FNOL forms validate fields and trigger follow-up requests before or as the claim is scored ([SwiftCase](https://swiftcase.co.uk/use-cases/insurance/), [Data Operatives](https://dataoperatives.com/insurer-fnol.html), vendors). A Simple claim missing a photo is still Simple once the photo arrives; a complex claim can be complete and still need a senior handler.

**What puts a claim in "Needs a closer look"**, in rough order of how often sources cite it:

- **Third party / fault to determine.** Third-party claims run 40–60% longer than first-party ones ([Finantrix](https://www.finantrix.com/articles/comparing-first-party-vs-third-party-claims-handling-workflows), directional)
- **Injury.** Can't be valued until treatment and prognosis are clearer
- **Disputed liability or cover.** Statements, witnesses, dashcam, police report
- **Total loss.** Valuation, salvage, finance paperwork
- **Above the handler's authority limit.** Supervisor sign-off
- **Other parties in the chain (UK).** Accident and claims management companies and credit hire add delay and cost ([FCA motor claims multi-firm review, 2025](https://www.fca.org.uk/publication/multi-firm-reviews/motor-insurance-claims-analysis-multi-firm-review-2025.pdf), regulator)

## 3. Where claims get stuck, and how big fraud is

**Where claims get stuck.** One worked example of 4,200 auto claims attributes claims that don't go straight through to: adjuster review **30%**, data quality / missing info **20%**, supervisor approval 8%, fraud flag **4%** ([Lorikeet](https://www.lorikeetcx.ai/articles/straight-through-processing-rate-practitioners-guide), vendor, illustrative).

**How big fraud is**

| Figure | Source |
|---|---|
| UK insurers detected **£576M** of motor fraud in 2024 across **51,700 cases**, 53% of all detected general insurance fraud cases. Roughly **£11k per case** (our arithmetic) | ABI via [Insurance Edge](https://insurance-edge.net/2025/11/17/claims-fraud-theres-a-lot-of-it-about-says-abi/) |
| US insurance fraud estimated at **$308.6bn/year**; ~**10%** of US P&C losses and adjustment expenses | Coalition Against Insurance Fraud via [Hesper AI](https://gethesperai.com/blog/claims-triage-automation-guide/); III via [Wikipedia](https://en.wikipedia.org/wiki/Insurance_fraud) |
| **Soft fraud** (inflating a real claim) is more common than **hard fraud** (staged or invented losses) | [Wikipedia](https://en.wikipedia.org/wiki/Insurance_fraud) |
| ~80% of insurers use predictive modelling for fraud (up from 55% in 2018) | III via [Hesper AI](https://gethesperai.com/blog/claims-triage-automation-guide/) |

**So what:** by volume, fraud is a **small pile**; claims needing judgement and claims waiting on information are **much bigger**. By value, fraud is **high per case**.

- **Speed** (what handlers and claimants feel) comes mostly from piles 1 and 2, plus clearing missing information on any claim.
- **Money and risk** (what insurers' finance and fraud teams feel) sit in pile 3.
- The 15% of Keelwater claims taking >4h are more likely **complex or waiting-on-information** claims than fraud. To validate (A-13).

**[INVENTED]** All three points match what we heard internally in Gong calls, Teams recordings and CSM/AM sessions. See [customer-signal.md](customer-signal.md).

## 4. Common motor fraud signals

From [Fraud Conference News](https://www.fraudconferencenews.com/home/spotting-signs-auto-insurance-fraud):

- **Timing:** claim shortly after policy start (sometimes within minutes)
- **Claimant:** hidden excluded drivers, misstated vehicle use, phantom passengers, contradictory statements, prior injury claims
- **Vehicle / damage:** damage inconsistent with the incident, or pre-existing; injury claims from low-speed impacts
- **Repair:** inflated repair estimates, storage and hire charges
- **Injury:** medical bills out of proportion to vehicle damage, recurring clinics or solicitors
- **Staged accidents:** deliberately caused or invented collisions (hard fraud)

Many of these need data Keelwater may not hold: cross-insurer claim history, telematics, repair invoices. **Keelwater probably can't be the fraud model; it can be the place where fraud signals are combined, shown and acted on** (A-10, A-14). Data sources and vendors: [auto-sorting-requirements.md](auto-sorting-requirements.md).

## 5. Regulation

Moved to [examiner-requirements.md](examiner-requirements.md): what US and UK examiners expect from automated claim sorting, and what Keelwater must build in.

## 6. What this means for Keelwater

1. **Reframe the fraud hypothesis (A-03).** Not "customers want automatic sorting to catch fraud". More likely: *"customers want clean claims paid faster, and need confidence that speeding up doesn't let fraud through."*
2. **Pile 2 is "needs a handler's judgement", with reason codes**, because the next action differs: assign senior handler, supervisor approval, appoint engineer, establish fault.
3. **Detecting missing information on any claim may be the biggest speed win.** Low-risk, highly explainable, a strong candidate for the first automation.
4. **The Simple criteria are well established**, so a rule-based Simple pile (A-12) is consistent with industry practice.
5. **Integrate, don't build, the fraud score.** Most insurers already run fraud models or vendors. Keelwater's value is pulling those signals into the sorting decision and making it explainable.
6. **Bulk sorting fits this story.** A table view with filters lets handlers clear the clean pile fast today, and the filters they use become the first rule set for automating it.

## Revision history

- **2026-10-16:** pile 2 redefined. Earlier versions defined it as "information missing"; industry triage puts complexity and judgement in the middle stream, and missing information is a status on any claim. See the AI usage log.
- **2026-10-16:** consolidated two research sessions into one structure; regulation moved to its own file.

## Open threads

- [ ] Real figures for the share of motor claims that go straight through vs referred (non-vendor source)
