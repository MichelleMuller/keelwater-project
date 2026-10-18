# Deck outline

Slide-by-slide plan for the deck and the ≤20 minute recording, in seven sections: the brief, the data, the personas, the solution, safe and valuable, GTM, and how I used AI. Each slide is tagged with the brief question it answers (Q1–Q5, plus the two closing asks), and the coverage check at the end confirms nothing is missing.

**The narrative in one line:** customers ask for "automatic sorting", but what they're buying is speed they can trust. **Bulk sorting is the first of a series of releases towards workflow automation**, and every release earns the right to automate a bit more.

> Decided 2026-10-17 (Michelle): live prototype walkthrough inside the solution section; Sales/CS story = bulk sorting as release 1 of an iterative path to workflow automation; AI-got-wrong as a table (what it affected, how I caught it, what we learn).
> Decided 2026-10-18 (Michelle): seven sections (brief, data, personas, solution, safe and valuable, GTM, how I used AI). Personas are the anchor we return to. Safety rests on using the LLM where it's most useful: finding patterns in how handlers already decide. "Where AI got it wrong" gets its own slide with the first four examples.

---

## Time budget


| Section | Slides | Time |
|---|---|---|
| 1. My understanding of the brief, and the answer up front | 1–4 | 2.5 min |
| 2. The data, my assumptions, and how I'd collect what's missing | 5–9 | 4 min |
| 3. Personas: the ecosystem | 10 | 1 min |
| 4. The solution: what we ship and what we don't, incl. live prototype | 11–14 | 4.75 min |
| 5. Safe and valuable | 15–17 | 2 min |
| 6. GTM and Customer Success, plus what I cut | 18–20 | 1.5 min |
| **Main content** | | **15.75 min** |
| 7. How I used AI; where it got it wrong; how the lifecycle is changing | 21–23 | 4 min |
| **Total** | | **19.75 min** |


Tight. Slides marked *(backup)* in the appendix are for the panel session, not the recording.

---

## Section 1. My understanding of the brief

### 1. Title

Keelwater: the roadmap towards automated claim sorting. Name, date. 

The talk track for every slide, with the longer details that don't need to be on the slides, is in [talk-track.md](talk-track.md).

### 2. The brief, as I understand it · Q1

One slide that restates the situation in my own words, so the panel can check I've read it the way they meant it.

- **Keelwater:** claims software for ~180 enterprise insurers. Handlers spend most of their day in it. We assume motor claims **[INVENTED]**.
- **Sorting:** a handler puts each new claim in one of three piles: Simple (pay quickly), Needs a closer look (check the details), Suspicious (investigate). It changes the handler's day and how fast people get paid.
- **The pressure:** customers, Sales and CS are asking for sorting to happen automatically, and a competitor has launched it. Customers in the pipeline are waiting on it, and a top-10 account might churn at renewal. That sets the urgency and the timeline: **5 months**.
- **The constraints:** insurers must explain every claim decision to the customer and the regulator. Before anything ships, it goes through several rounds of approval: the customer's IT (information and security) and their AI governance board, region by region. We have to meet every obligation as a sub-processor, and so does the AI model we choose. *(Detail in the talk track.)*
- **Work in flight:**
  - **Bulk sorting** is halfway built and ships in 6 weeks. My assumption: handlers work in an inbox, one claim at a time, so they need a table view to sort many at once (A-01).
  - **A data team prototype** that predicts the pile has been on hold for 18 months. It was built on Kaggle sample data: useful as a visual cue to steer customer conversations, not something to build on (A-11).
- **The ask:** show how I'd move this forward. Five questions: the problem and my confidence; what to find out first; priorities, including bulk sorting; signal to measurement, including where AI fits and when automation is safe; and what to tell Sales and CS.
- *Visual:* the three piles as cards, the in-flight work and constraints around them. *Source:* [assignment-brief.md](../00-brief/assignment-brief.md).

### 3. The answer up front · Q1, Q3, Q5

A busy leadership team and a commercial team that wants an answer get it before the detail.

- **The problem:** customers want clean claims paid faster without paying out fraud, with their handlers in control and every decision explainable. The slow claims are waiting on information or a third party, not on fraud checks **[INVENTED]**.
- **How confident I am:** high that the demand is real; medium on what "automatic" means to buyers; low on how accurate automated sorting can be, because nothing has been tested on real Keelwater claims yet.
- **The recommendation:** ship bulk sorting in 6 weeks as release 1. Then automate in steps: missing-information flagging, suggested piles learned from how handlers sort, then per-insurer workflows with the insurer's fraud vendor as a gate.
- **What we tell Sales and CS:** one story. Bulk sorting is the first release towards workflow automation.
- *Visual:* four short blocks, one per line above. The release path (slide 14) as a thin strip along the bottom.

### 4. The signal: what it tells us, and what it doesn't · Q1, Q4 (first signal)

- **What it tells us:** demand is real and coming from every direction. Several large customers asking; 6 deals worth £2.3M ARR, incl. the biggest in the pipeline; 3 accounts in reviews, one top-10 renewing in 5 months; ~40 tickets; a competitor launched last quarter.
- **What it doesn't tell us:** the deals only "mention" automatic sorting. Nothing says:
  - **What automatic sorting looks like** to them: suggestions a handler confirms, or claims moved without a human? All three piles, or only Simple? Does it stop at sorting, or do they expect payment too?
  - **What the exact pain point is:** speed for claimants, handler headcount, inconsistent sorts between handlers, or a competitive checkbox? And which claims hurt: the fast majority or the slow 15%?
  - **Who the pain belongs to:** handlers use Keelwater, but they're probably not the buyers (A-24). The ask likely comes from heads of claims, operations, finance or fraud teams, so the problem they describe may not be the handler's day.
  - **Where fraud fits:** do they expect sorting to catch fraud, or do they already have a fraud vendor and just need fast sorting not to pay fraud out?
  - **How concentrated it is:** ~40 tickets across ~180 customers is low. Is this a few large accounts or the whole base?
  - **What the competitor actually offers**, and whether it's what these buyers want or just what they've seen.
- *Visual:* the signals on one side ("what we know"), the open questions on the other ("what we don't"). *Source:* [fact-sheet.md](../00-brief/fact-sheet.md).

---

## Section 2. The data, my assumptions, and how I'd collect what's missing

### 5. The facts the brief gives us, and what doesn't add up · Q1

- **The data points, with simple arithmetic on top:**
  - 2.1M claims sorted in 12 months: ~175k a month, ~11.7k per customer a year on average.
  - Median time to sort: 11 minutes. Most claims aren't slow.
  - 15% take over 4 hours: ~315k claims a year.
  - 3.4% moved to a different pile within 30 days: ~71k claims a year. The human baseline any automation is compared against.
- **The metrics, defined:**

| Metric | From | To | In the brief? |
|---|---|---|---|
| **Time to sort** | Claim arrives | Claim is sorted | Yes: median 11 min, 15% over 4h |
| **Sort processing time** | A handler opens the claim | Claim is sorted | No. A first data ask |
| **Re-sort rate** | Claim is sorted | Moved to a different pile within 30 days | Yes: 3.4% |

- **What seemed inconsistent:** an 11-minute median from arrival includes queue time, which only works if claims are picked up around the clock (A-18, A-22). *(Detail in the talk track.)*
- *Visual:* the illustrative time-to-sort curve on a log time axis, with the 11 min and 4 h lines marked: a fast majority and a long stalled tail that holds most of the waiting time. Labelled illustrative: fitted to two data points. [time-to-sort-distribution.svg](../02-research/assets/time-to-sort-distribution.svg).
- *Sources:* [fact-sheet.md](../00-brief/fact-sheet.md), [time-to-sort-distribution.md](../02-research/time-to-sort-distribution.md).

### 6. Facts, gaps, assumptions: what they mean for the need · Q1

Each fact from the brief leaves a gap. I filled each gap with an assumption or invented data **[INVENTED]**, and each one changed my understanding of what customers need and where the value is.


| Fact from the brief                 | The gap                     | What I assumed or invented                                                                                                                                           | What it changes about the need and the value                                                                                      |
| ----------------------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 15% of claims take over 4h          | Why?                        | Waiting on the claimant 48%, third party 28%, injury 15%, fraud 6%. No "waiting on claimant" status exists, so handlers leave those claims unsorted (A-13, A-19)     | The speed problem is stuck claims, not fraud. A waiting-on-claimant status and missing-information flagging are cheap, early wins |
| 2.1M claims across ~180 customers   | Is every customer the same? | Three segments: simple-heavy (55% of claims), mixed (33%), complex-heavy (12%), each with a different main problem (A-07)                                            | One model for everyone won't work. Per-insurer rules and thresholds                                                               |
| ~40 tickets mention sorting         | What do they say?           | 22 of 40 are about sorting many claims at once; 3 customers filed 18                                                                                                 | Bulk sorting answers a real, concentrated pain. Ship it                                                                           |
| 6 deals "mention" automatic sorting | What are buyers buying?     | Speed, confidence that fraud is caught within that cycle, and an expert in the loop. Most already have a fraud vendor. None asked for automatic payment (A-03, I-06) | Sell speed you can trust: suggestions a handler confirms, using the insurer's own fraud vendor                                    |
| Bulk sorting takes ~12 weeks        | Why so long?                | There's no table view today; handlers sort one claim at a time (A-01)                                                                                                | Bulk sorting is the foundation: suggestions need a table to appear in (A-21)                                                      |
| A prototype, shelved 18 months      | What is it?                 | A gradient-boosted model trained on public sample data with rule-made labels. Per-claim reasons possible, never tested on real claims (A-11)                         | A concept for customer sessions, not a shortcut to automation                                                                     |
| Every decision must be explainable  | To what standard?           | Regulation depends on the country or region of business (US NAIC bulletin, UK GDPR 22A–D, FCA Consumer Duty): decision records, human review, no automated denial    | Explainability is a selling point, and it rules out an LLM making the decision                                                    |


- *Visual:* the cause-split chart: the time-to-sort curve with each section split by what claims are waiting on. [time-to-sort-causes.png](../02-research/assets/time-to-sort-causes.png).
- *Sources:* [assumptions-log.md](../01-thinking/assumptions-log.md), [internal-data.md](../02-research/internal-data.md), [customer-signal.md](../02-research/customer-signal.md), [examiner-requirements.md](../02-research/examiner-requirements.md).

### 7. The questions I'd ask, and how I'd collect the answers · Q2

Before deciding anything: a quick review of the data to size the problem and check we're building the right thing. Then three sets of questions.

- **The questions:**
  - **A clear sense of the problem:** what's the main problem per customer? Why do some claims take hours? What's the full lifecycle from sorted to paid? How do volume, time to sort and the >4h share break down per customer? Which way do the 3.4% re-sorts go?
  - **The minimum the solution needs:** must every sort be right (deterministic), or is some error acceptable (probabilistic)? Is it the same for every customer, or configurable? Is this a good job for an LLM?
  - **What we already have:** why are we building bulk sorting, and what was validated? What's in the shelved prototype: what model, trained on what, why did it stop, can we show it to customers? Do customers already have fraud checks, and what signals do they use?
- **How: internal data now, while external conversations are put in motion.** External conversations take weeks to book, so I'd request them on day one and work through internal sources while they're being set up.


| Internal: start now, answers in days                      | External: request on day one, answers in weeks                                   |
| --------------------------------------------------------- | -------------------------------------------------------------------------------- |
| The shelved prototype and the data scientist who built it | Customer interviews: handlers, claims ops leads, fraud teams                     |
| Bulk sorting spec, Jira and the tech lead                 | Customer IT, governance and legal: data sharing, explainability                  |
| Two years of Gong recordings; Teams calls going forward   | Competitor: what they offer, how they position it, where it falls short          |
| Usage data, support tickets, pipeline, at-risk accounts   | Market: how mature fraud detection is for motor claims; open models and datasets |
| Account manager and CSM feedback                          | Regulation: UK and US rules on automated claim decisions and data sharing        |


- Gong may not hold the answers if reps never asked the right questions. Where data is missing, state the assumption.
- **Timing:** internal answers in ~2 weeks. Customer validation lands at the week-6 bulk sorting beta, when there's something to show.
- *Visual:* two lanes on a timeline, internal and external, converging at week 6.
- *Sources:* [brainstorm-raw.md](../01-thinking/brainstorm-raw.md), [brainstorm-organised.md](../01-thinking/brainstorm-organised.md) §2.

### 8. Who I'd work with closely, and what each answer changes · Q2


| Who                                     | What I'd ask                                                                                                               | What it changes                                                |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Data team**                           | Full time-to-sort histogram, split by customer, pile and cause (first ask); re-sort directions; is the prototype reusable  | Which segment and cause to fix first; reuse or restart         |
| **Designer, tech lead and squad**       | Build bulk sorting so we can iterate and add automated rules later; log every filter and bulk action from day one; make sure we don't design in bias; show handlers what's been done or auto-sorted so they can give feedback | Bulk sorting becomes the foundation and data source for automation, not a dead end |
| **AEs**                                 | What each of the 6 buyers asked for, in their words; blocker or checklist item; what's been promised                       | What we show, and by when                                      |
| **CSMs and account managers**           | What the 3 accounts and the top-10 renewal need to see                                                                     | Pilot customers and the near-term commitment                   |
| **Support**                             | I run the thematic analysis of the 40 tickets myself, with AI, to see the main needs and who has them. From Support: label new tickets and flag them as they come in | Bulk sorting pain vs automation demand, kept up to date |
| **Legal; customers' IT and governance** | Can we use claims data; what explanation and sign-off do automated decisions need                                          | What we can automate vs only suggest                           |


- **Where AI speeds this up:** thematic analysis of Gong calls, recording transcripts and tickets; all the answers in one place; working out why bulk sorting was prioritised from old records instead of new interviews.
- *Source:* [open-questions.md](../01-thinking/open-questions.md).

### 9. The problem, and how confident I am · Q1

- **The problem:** handlers can't move clean claims fast enough, and the slow ones are stuck waiting on information or a third party with no way to flag it. Buyers want that speed only if fraud is still caught before payment and every sort can be explained to their regulator.
- **Confidence:**


| Confident                                                     | Less sure                                           | Don't know yet                                                             | What would raise confidence                                                                                                                                  |
| ------------------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Demand is real; speed is the ask; bulk sorting is a real pain | The cause split; the segments; what each deal needs | Accuracy on real claims; data-sharing rights; the competitor's weak points | The time-to-sort histogram; calls with customers who want it and the ones in the pipeline; get a design partner to work through the claim lifecycle together |


- **How my view changed:** I started at "fraud is the blocker". Research and deal signal moved me to "speed is the ask; fraud screening is the licence to automate".

---

## Section 3. Personas: the ecosystem

### 10. Who we're building for · Q1, Q5

The anchor for every decision that follows. Three groups, each wanting something different from the same feature.

**1. The insurance company: the buyer and the user**

- **As the buyer** (heads of claims, operations, finance, fraud, compliance):
  - **Expense ratio:** the cost of handling claims against the premium revenue they bring in. They want to process more claims without hiring more handlers: scaling profitably.
  - **Accuracy,** including from an audit perspective: fewer re-sorts, and no fraud paid out because a claim was rushed through.
  - **Explainable and reliable** to any regulator: every sort can be explained and traced.
- **As the user** (handlers): get through the queue, see why a claim is where it is, stay in control of the decision, and stop chasing missing information by hand.

**2. The consumer: the claimant** *(to confirm, drawn from research)*

- Paid quickly and fairly, and kept informed while they wait.
- Not delayed or treated as suspicious without a reason.
- Able to challenge a decision and reach a human (UK GDPR 22C, FCA Consumer Duty).
- They never see Keelwater, but they feel every sorting decision in how fast they're paid.

**3. The business team: Sales and Customer Success**

- A solution they can sell confidently, with a differentiator and a clear story that maps to both the buyer and the user.
- Ultimately Sales cares about commission. A product they can rally behind and sell well gives them the confidence to hit it.
- A long-term, durable advantage, not a checkbox matched to the competitor.
- *Visual:* ecosystem diagram: the insurer in the centre (buyer and handler), the claimant on one side, Keelwater's Sales and CS on the other, the regulator above.
- *Script:* "I go back to these personas with the team, with myself and with AI, so we don't drift from the brief."

---

## Section 4. The solution: what we ship and what we don't

### 11. The bulk sorting decision · Q3

- **Options:**
  1. **Ship it as the validation layer** for automation.
  2. **Ship a trimmed version** and free part of the squad for discovery.
- **Decision: ship it,** plus capture of every filter and bulk action, and a "waiting on claimant" status.
- **Why:**
  - Real ticket demand: 22 of 40 tickets are about sorting many claims at once **[INVENTED]**.
  - There's no table view today, so handlers sort one claim at a time (A-01).
  - 3 beta customers are lined up, including the top-10 renewal **[INVENTED]**.
  - It produces what automation needs: the filters handlers actually use become the first rules, and their bulk actions become labelled data.
- **The prototype confirms the order:** suggestions need a table to appear in; the shelved model was trained on sample data and isn't ready; bulk sorting generates the real data it lacked.

### 12. First, next, later, won't do · Q3

- **First:** bulk sorting + user action capture + waiting-on-claimant status. 
- **Next:** missing-information flagging and auto-request; suggested piles with reasons in the table.
- **Later:** per-insurer workflows with fraud vendor gate; Claims sorting agent; claims processing beyond sorting.
- **Won't do:** pause bulk sorting; build our own fraud model; let an LLM make the sorting decision; auto-deny or reduce a claim; assume one global model for all customers; revive the shelved prototype as-is.
- *Visual:* four columns, with "won't do" as clearly as the others.

### 13. Prototype walkthrough (2–3 min) · Q4

A single slide that hands over to the live prototype. Click-through steps are in the talk track.

- **On the slide:** "From one claim at a time to workflow automation", with a screenshot strip: claim form → inbox → bulk sorting → automation panel → workflow builder. A link to [keelwater-prototype.html](solution-prototype/keelwater-prototype.html), and "All data invented".

### 14. The release path: from bulk sorting to workflow automation · Q3, Q4, Q5

The spine of the deck and of the Sales and CS story. Each release ships value on its own and earns the right to the next.


| Release                      | What handlers get                                                                                                                                                        | What it gives the next release                                |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| **1. Bulk sorting** (week 6) | Table, filters, multi-select, sort many at once; waiting-on-claimant status                                                                                              | Every filter + bulk action captured: how handlers really sort |
| **2. Suggestions**           | Rules learned from handler behaviour; suggested pile + reasons in the table; confirm or override; missing info detected and requested automatically                      | Override data; agreement with handlers per rule               |
| **3. Workflows**             | Per-insurer workflow: missing info → fraud gate (vendor score) → complexity → Simple only if every check passes. Shadow → suggest → auto-route above an agreed threshold | Proven accuracy per customer; audit trail                     |
| **4. Claims sorting agent**   | Answers questions about any claim; proposes workflow changes with evidence and a backtest; a human approves                                                              | Path to claims processing beyond sorting                      |


- Timing beyond release 1 to agree with the tech lead after discovery; flag as indicative.
- *Note for the panel:* a workflow builder used to be a quarter-long platform project. With AI-assisted development it's days, which makes per-insurer workflows realistic for a squad of seven.

---

## Section 5. Safe and valuable

### 15. How we know it's safe · Q4

**Reduce the surface area of uncertainty.** Use the LLM where it's most useful, finding the patterns in how handlers already decide, and keep it away from the decision itself.

- **Rules come from handlers' own decisions.** Bulk sorting captures every filter and bulk action. The system proposes rules from those patterns ("you sorted 41 windscreen claims under £1,000 with no third party as Simple"). A human accepts each rule, so every sort traces back to a rule a person approved.
- **The LLM finds patterns and extracts; it never decides.** It reads free text and documents into structured fields, quoting the source, and suggests rules and reason codes. The decision itself is rules plus the insurer's fraud score: explainable by construction.
- **A decision order with a safe default:** missing information → fraud gate → complexity → Simple only if every check passes. Anything uncertain goes to Needs a closer look. Never Simple without a fraud check (AS-02).
- **A ladder, not a switch:** shadow mode → suggest → auto-route. Each step needs, per customer:
  - Accuracy at or better than the human baseline (~1.4% true first-sort error), weighted by direction: Suspicious sorted as Simple is the costly miss.
  - A per-claim decision record: inputs, rules fired, fraud score and vendor version, suggestion, human decision.
  - Bias testing on Suspicious routing; legal view on UK GDPR 22A–D and the NAIC bulletin.
  - Sign-off from the customer's claims, IT and governance teams; an off switch.
- **Never automated:** denying or reducing a claim. Suspicious stays suggest-only by default.
- **Who decides:** a threshold agreed with each customer before go-live, not set by us alone.
- *Sources:* [auto-sorting-requirements.md](../02-research/auto-sorting-requirements.md), [examiner-requirements.md](../02-research/examiner-requirements.md) (checklist E-01 to E-14).

### 16. How we measure success · Q4


| Release         | Leading                                               | Lagging                                       |
| --------------- | ----------------------------------------------------- | --------------------------------------------- |
| 1. Bulk sorting | Adoption, claims sorted per bulk action, filters used | Time to sort, >4h share, tickets              |
| 2. Suggestions  | Override rate and reasons, agreement per rule         | Time to first look, re-sort rate by direction |
| 3. Workflows    | Share sorted without a human, drift per customer      | End-to-end time to payment, fraud paid out    |
| Commercial      | Pilot sign-ups from the 6 deals and 3 accounts        | Deals won, top-10 renewal, competitive losses |


- **Valuable enough to automate:** override rate low and falling in suggest mode; handlers actually using suggestions; time to first look and the >4h share going down.
- **Three time metrics:** time to first look (the queue), time to sort (the brief's), end-to-end to payment (what the claimant and the FCA see).
- Analytics and action capture live **before** the bulk sorting launch.

### 17. From signal to measurement: where AI fits · Q4

One row per stage, so "where AI changes how I work, where it doesn't, what stays mine" is answered in one place.


| Stage           | What happens                         | Where AI changes how I work                                                                      | Where it doesn't                                                  | What stays mine                           |
| --------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- | ----------------------------------------- |
| **Signal**      | Deals, accounts, tickets, competitor | Thematic analysis of calls and tickets in hours; keeps listening after launch to track sentiment | Hearing what a buyer means but doesn't say                        | Deciding which signal is the real problem |
| **Decision**    | Ship bulk sorting; release path      | Research with sources, simulated data, options laid out with trade-offs                          | Weighing commercial pressure against the squad's capacity         | The call, and owning it with leadership   |
| **Validation**  | Beta sessions, shadow mode           | Synthetic claims for dry-run evals; clickable prototype in a day                                 | Customer conversations; the threshold each customer accepts       | What counts as good enough, per customer  |
| **Delivery**    | Releases 1–4                         | Prototype and tests in days; workflow builder no longer a platform project                       | Engineering judgement on architecture, security and data handling | Scope, sequencing, what we don't build    |
| **Measurement** | Metrics, drift, overrides            | Monitoring and explaining drift and override patterns                                            | Deciding whether a metric moved for the right reason              | Go / no-go at each step up the ladder     |


---

## Section 6. GTM and Customer Success

### 18. What we tell them · Q5

- **The story:** bulk sorting is the first release towards workflow automation. It's how your handlers teach the system how they sort, and it's what makes automation explainable to your regulator.
- **What wins against the competitor:** sorting inside the workflow handlers already use, with the fraud vendor the insurer already pays for, and a reason for every sort that compliance can read (4 of 6 buyers saw the competitor's demo **[INVENTED]**).
- **Maps to the personas:** buyers get a lower expense ratio and an audit trail; handlers stay in control; Sales gets a differentiator, not a checkbox.
- **Pitch by segment:** simple-heavy = handler effort; mixed = unsticking claims waiting on information; complex-heavy = expert routing with fraud confidence.
- **Never promise:** automatic payment, automatic denial, our own fraud detection, dates beyond release 1 before the tech lead agrees them.
- **Assets:** battle card, objection handling, a vendor evidence pack for insurers' governance teams (E-13), generated from the repo and checked by me.

### 19. When · Q5


| When                      | Who                                                   | What                                                                                                                     |
| ------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Week 1                    | Sales and CS leads                                    | Holding message: we've heard it, here's how we're finding out what buyers need. Ask AEs and CSMs the discovery questions |
| Weeks 2–3                 | Commercial, tech, design                              | Findings and release path shared async, then a Q&A in one room                                                           |
| Week 6                    | Beta customers (incl. top-10 renewal), the 3 accounts | Bulk sorting launch; CSM-led sessions to validate needs and fraud signals                                                |
| Release 2                 | Design partners from the 6 deals and 3 accounts       | Suggestions pilot on their own claims                                                                                    |
| Before renewal (~month 4) | Top-10 account                                        | Show release 2 working on their data                                                                                     |


### 20. What I cut, and why · checklist

To fill in at the end. Candidates: competitor deep dive; open models and datasets; prototype refinements, a real eval on synthetic claims.

---

## Section 7. How I used AI, and where it got it wrong (≤5 min combined)

### 21. How I used AI · closing ask 1

1. **The repo as a context hub.** Everything lives in a git repo that an LLM or agent can query: the brief, my brainstorm, assumptions, research with sources, decisions, prototypes.
  - **For me:** agents start with full context, so research, the prototype and this deck are faster, easier and more accurate.
  - **For GTM and internal teams:** they can see my sources and structured thinking, and query it with their own questions.
  - **Kept alive and in sync** as we build, it becomes the source for GTM material and battle cards, and for feeding Sales answers while they're on calls.
2. **What I used it for:** structuring a voice brainstorm; research with sources; simulating internal data; analysis and charts; a sample-data model built on Kaggle claims data; the solution prototype and its tests.
3. **How I kept the decisions mine:** I read everything it produced, and had it ask me through question forms so every decision was mine before anything was written down as decided.

- *Visual:* repo map at the centre, with arrows out to research, prototype, deck and GTM material.

### 22. Where AI got it wrong · closing ask 1


| Where AI got it wrong                                                                           | What it affected                                                     | How I caught it                                                                                                            | What we learn                                                                                                                                                      |
| ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Defined the middle pile as "information missing" and called it the largest addressable category | Fact sheet, research and assumptions: we'd have built the wrong pile | **Reading:** it didn't match my own brainstorm ("complex but not suspicious"); a quick search on motor triage confirmed it | A wrong framing compounds across documents. Check definitions against the source early. It also turned missing info into a status, and the first thing to automate |
| Stated "fraud is the blocker" as fact in the organised brainstorm                               | The whole strategy would have been a fraud model                     | **Brainstorming the next step:** I asked to test it before building on it                                                  | Test the framing before the solution. The brief only says deals "mention" it                                                                                       |
| Invented per-customer data with complex-heavy insurers as the biggest accounts                  | Segment sizes and which segment to pilot with                        | **Reading:** the totals matched the brief but contradicted how the market works                                            | Invented data can add up and still be implausible                                                                                                                  |
| Listed "above authority limit" as a cause of slow sorting                                       | The cause split and the decision order                               | **Reading:** I asked what it meant and why it was there                                                                    | Research about the whole claim journey doesn't always apply to the step you measure. It became a review before payment instead                                     |


*Recording:* walk through the table, then go deep on one row. Suggest the middle-pile row, because it would have changed the product.

### 23. How the lifecycle is changing · closing ask 2

- **Discovery compresses:** thematic analysis of calls and tickets takes hours, not weeks. The bottleneck moves to asking the right questions and checking the answers.
- **Prototypes become the spec:** a clickable prototype with tests in a day, so we validate with customers before committing the squad. A workflow builder is days, not a quarter.
- **Judgement and reading become the job:** every error on slide 22 was caught by me reading or using the output.
- **Decisions have to be explicit:** AI writes fluently enough that unmade decisions look made.
- **What I'd prioritise at Keelwater:**
  - A shared context hub (calls, tickets, research, decisions) that agents and people both use.
  - Evals and audit trails as part of the definition of done.
  - Designers and engineers prototyping with customers from week one.
  - The same human-in-the-loop discipline for ourselves that we ask of insurers' handlers.

---

## Appendix (backup for the panel session)

- A1. Re-sort directions and costs *(backup)*: [internal-data.md §3](../02-research/internal-data.md)
- A2. Data needed per check, and what Keelwater doesn't hold (cross-insurer claims history) *(backup)*: [auto-sorting-requirements.md §2](../02-research/auto-sorting-requirements.md)
- A3. Examiner checklist E-01 to E-14, US and UK *(backup)*
- A4. Sample-data model results and the table a handler would see *(backup)*: [results.md](../04-working-material/prototype/results.md)
- A5. Competitor landscape (four product types) *(backup)*: [discovery-answers.md §10](../02-research/discovery-answers.md)
- A6. Assumptions and invented items *(backup)*
- A7. More places AI got it wrong *(backup)*:


| Where AI got it wrong                                                                               | What it affected                                   | How I caught it                                                                                                                                   | What we learn                                                                          |
| --------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Said the shelved prototype had no per-claim reasons, and invented it as trained on 600k real claims | The explainability argument and the reuse decision | **Brainstorming the next step:** tree models can trace their reasons, and a team with no product owner wouldn't have had customer data agreements | Check AI's technical claims against what you know                                      |
| Built the prototype with React, Radix and Vite (1.3 MB, Node tooling)                               | Portability for reviewers                          | **Playing with the prototype:** reviewing the first build                                                                                         | AI optimises for what it's asked. State the real constraint up front                   |
| Layout bugs in the prototype (misaligned progress bar and inputs)                                   | Credibility of the demo                            | **Playing with the prototype**                                                                                                                    | Each bug got a test; I checked the tests catch it by undoing the fix                   |
| I picked every option AI marked "Recommended"                                                       | Ownership of decisions                             | **Reflecting on the question forms**                                                                                                              | Recommended labels nudge. It's the same automation bias we design against for handlers |


## Working material to submit

- The solution prototype, with [PLAN.md](solution-prototype/PLAN.md) showing the decisions and revisions
- The [AI usage log](../04-working-material/ai-usage-log.md), including the question-form screenshot

---

## Coverage check


| Brief asks | Slides |
|---|---|
| Q1. What problem, how confident | 2, 3, 4, 5, 6, 9, 10 |
| Q2. What to find out before committing the squad, and how, quickly | 7, 8 |
| Q3. Prioritise: first, can wait, won't do, incl. bulk sorting | 3, 11, 12, 14 |
| Q4. Signal → decision → validation → delivery → measurement | 17 (the whole arc), plus 4 (signal), 11 (decision), 13 and 15 (validation), 14 (delivery), 16 (measurement) |
| Q4. Where AI changes how I work, where it doesn't, what stays mine | 17, supported by 8, 15 |
| Q4. Safe and valuable enough before automating | 15, 16 |
| Q5. What to tell Sales and CS, and when | 3, 10, 18, 19 |
| How I used AI, incl. where I overrode it and one thing it got wrong | 21, 22; the overrides are in the talk track for slide 21 |
| How the lifecycle is changing; what I'd change at Keelwater | 23 |
| Invented items flagged | [INVENTED] tags on slides 2, 3, 6, 11, 18; say it on slide 1 in the talk track |
| What I cut and why | 20 |
| 1–2 pieces of working material | Working material section |
| Something for each panellist | PM: 3, 6, 9, 10, 12 · Engineer: 15, 17 · Designer: 8, 10, 13 · Commercial: 2, 4, 10, 14, 18, 19 |


**Open:**

- [ ] Confirm the consumer persona on slide 10 (drafted from research)
- [ ] Fill in slide 20 (what I cut) at the end
- [ ] Indicative timing for releases 2–4 (slide 14)
