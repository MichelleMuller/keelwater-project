# Talk track

What I say over each slide in the [deck outline](deck-outline.md), plus the longer details that don't need to be on the slides. Slide numbers match the outline. Times add up to the outline's 20-minute budget.

---

## Section 1. My understanding of the brief

### 1. Title · 15 sec

"This is how I'd move automatic claim sorting forward at Keelwater. Keelwater is fictional, so I've invented data where I needed it, and everything invented is tagged on the slides. All my sources, thinking and working material are in one repo, which I'll come back to at the end."

### 2. The brief, as I understand it · 45 sec

Restate the brief in my own words, so the panel can check I've read it the way they meant it.

**The pressure.** Customers in the pipeline are waiting on this, including the biggest deal we have, and a top-10 account is up for renewal in 5 months. That renewal gives us the urgency and the timeline: whatever we show them has to be real within 5 months.

**The constraints: approval loops.** Explainability is the constraint in the brief, but in practice anything with automated decisions goes through several rounds of approval at the customer before it's switched on:

- **The customer's IT, on information and security:** a security questionnaire, how data flows, where it's stored and processed, access controls, certifications and test results.
- **The customer's AI governance board:** what the model does, what data it uses, how each decision is explained, how bias is tested. The rules depend on the country or region:
  - UK: UK GDPR Articles 22A–22D, FCA Consumer Duty, ICO guidance on meaningful human review.
  - US: the NAIC model bulletin (adopted in ~28 jurisdictions), and in Colorado a specific rule for auto insurers that covers claims.
- **Keelwater as a sub-processor:** we process claimants' personal data on the insurer's behalf, so we're bound by their data processing agreement: only use the data on their instructions, keep it secure, report breaches, allow audits, cooperate with regulators, keep data in agreed locations. US regulators can ask the insurer for our documentation as their AI vendor.
- **The AI model is a sub-processor too:** any model provider we use processes that data on our behalf. The insurer has to be told and can object. We need no training on their data, limited retention and the right hosting region.

**What that means for the plan:** these loops take months, so they run in parallel with release 1, not after it. Anything with AI in it that we want live before the renewal has to be in approval by about month 2. We build the evidence once, as a pack we can give every customer. *(My inference, not from the brief.)*

**Work in flight: bulk sorting.** "I've assumed handlers work in an inbox today, one claim at a time, so bulk sorting means a new table view, not just a checkbox. That's also why it takes about 12 weeks. I'll come back to why that matters when I get to the solution."

**Work in flight: the prototype.** "The prototype was built on public sample data from Kaggle, about 10,000 US policies, with pile labels the data team made from simple rules. So its accuracy only shows it can relearn those rules. It's useful as a visual cue in customer conversations, to show what a suggested pile with reasons could look like. It's not something we can build on."

### 3. The answer up front · 45 sec

"Before the detail, here's where I land. Customers ask for automatic sorting, but what they're buying is speed they can trust: clean claims paid faster, fraud still caught, handlers in control, every decision explainable. I'm confident the demand is real, less sure what 'automatic' means to each buyer, and I don't yet know how accurate automation can be on real claims. So: ship bulk sorting in 6 weeks as release 1, and automate in steps from there. And the story for Sales and CS is the same one: bulk sorting is the first release towards workflow automation."

### 4. The signal · 45 sec

Walk the "what we know" side quickly; spend the time on "what we don't know". Land on: "The deals only mention automatic sorting. I don't know what it looks like to them, what the pain is, or whose pain it is. Handlers use Keelwater, but they're probably not the people asking for this in a sales call."

---

## Section 2. The data, my assumptions, and how I'd collect what's missing

### 5. The facts the brief gives us · 45 sec

**The three metrics.**

- **Time to sort** runs from when a claim arrives to when it's sorted. It's elapsed clock time: it keeps running while the claim sits in the queue, while the handler works on other claims, and while they wait for a reply.
- **Sort processing time** runs from when a handler opens the claim to when it's sorted. The brief doesn't give it, so it's one of my first asks of the data team. The gap between the two tells us whether a slow claim was stuck in the queue or stuck with a handler.
- **Re-sort rate:** 3.4% of claims are moved to a different pile within 30 days. That's the human baseline any automation is compared against. Later I'd split it into re-sorts that follow new information and ones that were wrong first time.

**What seemed inconsistent (the long version).** Because time to sort starts when the claim arrives, it includes queue time before anyone opens it. An 11-minute median means half of all claims are queued, read and sorted within 11 minutes. That only works if claims are picked up almost immediately, around the clock: 128 of the 168 hours in a week fall outside a 9–5 weekday. Without handling teams across time zones, every claim that arrived in the evening or at a weekend would pass 4 hours, and the share over 4 hours would be far above 15%. I've taken the brief at face value and assumed teams across time zones (A-22), and flagged it.

**The chart:** "This curve is illustrative, fitted to the two points the brief gives us. The shape is the point: a fast majority, and a long tail that holds most of the waiting."

### 6. Facts, gaps, assumptions · 60 sec

"Every fact in the brief leaves a gap. I filled each one with an assumption or invented data, and I've flagged each one. What matters is how each changed my view of the need." Walk the first two rows (the slow tail, the segments) in detail, then the rest quickly. Land on: "The speed problem is stuck claims, not fraud. And explainability isn't just a constraint, it's a selling point."

### 7. The questions I'd ask · 45 sec

"First a quick review of the data, then three sets of questions: the problem, the minimum the solution needs, and what we already have. External conversations take weeks to book, so I'd request them on day one and work through internal sources while they're being set up. Both lanes meet at the bulk sorting beta in week 6, when we have something to show."

### 8. Who I'd work with closely · 45 sec

**Designer, tech lead and squad.** We're halfway through bulk sorting, so the ask is about how we finish it:

- Build it so we can iterate: a table that can later show a suggested pile and its reasons per row, with confirm and override.
- Log every filter and bulk action from day one, with the filter values, so the patterns can become rules.
- Don't design in bias: some filters, like postcode, could turn into rules that profile claimants. Keep those out of what the system learns rules from.
- Show handlers what's been done or auto-sorted, with a way to undo it and say why, so they can give feedback.

**Support.** "I'd run the thematic analysis of the 40 tickets myself with AI, to see the main needs and who has them, rather than ask Support for a report. What I'd ask Support for is to keep labelling new tickets and flag them as they come in, so the picture stays current."

### 9. The problem, and how confident I am · 45 sec

Read the problem statement. Walk the confidence table left to right. Close on how my view changed: "I started at 'fraud is the blocker'. The research and the deal signal moved me to 'speed is the ask, and fraud screening is what makes speed safe'."

---

## Section 3. Personas

### 10. Who we're building for · 60 sec

One persona at a time: the insurer as buyer (expense ratio, accuracy, explainability), the insurer as user (the handler), the claimant, then Sales and CS.

"I go back to these personas with the team, with myself and with AI, so we don't drift from the brief. When a decision is hard, the question is which of these people it serves."

---

## Section 4. The solution

### 11. The bulk sorting decision · 45 sec

"Back to the assumption from the start: handlers sort in an inbox, one claim at a time." Then: two options were really on the table, ship it as the foundation for automation or ship a trimmed version and free people for discovery. Ship it, and add action capture and a waiting-on-claimant status. The reasons are on the slide. "Customers asked for bulk sorting, and it's also exactly what automation needs: somewhere for suggestions to appear, and real data on how handlers sort."

### 12. First, next, later, won't do · 45 sec

Spend as long on "won't do" as on the others. "We won't build our own fraud model: most insurers already pay for one. We won't let an LLM make the sorting decision, and we'll never automatically deny or reduce a claim."

### 13. Prototype walkthrough · 2.5 min

Click-through, live in the browser:

1. **Claim form:** the claimant fills in the insurer's form. The claim record builds live beside it: this is the data every sorting decision runs on.
2. **Inbox today:** switch to the handler view. One claim at a time, open it, read it, sort it.
3. **Release 1, bulk sorting:** filter (for example windscreen, under £1,000, no third party), select, sort into a pile. The capture panel logs each action in plain words. Load the example week to show how much a week of sorting tells us.
4. **Release 2, automation panel:** rules learned from that week, each with how often handlers did it. Accept one; the table shows a suggested pile and the reason. Confirm or override. Suggest and Auto-sort per rule; Suspicious is always suggest-only.
5. **Workflow builder:** one workflow per insurer: fraud check, then information check, then the rules, first match wins; no match goes to Needs a closer look. Each stack shows how many of the last 30 days' claims would land there and how often each rule agrees with handlers. Draft, test run, publish, with versions you can restore.
6. **Switch insurer:** a simple-heavy insurer learns mostly Simple rules; a complex-heavy one learns almost none.

- **Not built yet:** the Workflow Agent and the per-claim audit view. All data is invented.
- **UX point:** human review has to be meaningful. A handler clicking confirm on everything is automation bias, which regulators warn about. Showing the reason, logging overrides and spot checks keep it honest.

### 14. The release path · 45 sec

"Each release ships value on its own and earns the right to the next one. That's also the Sales story." Note that timing beyond release 1 is indicative until the tech lead agrees it. Mention: "A workflow builder used to be a quarter-long platform project. I built a working one in days, which makes per-insurer workflows realistic for a squad of seven."

---

## Section 5. Safe and valuable

### 15. How we know it's safe · 60 sec

"I reduce the surface area of uncertainty by using the LLM where it's most useful: finding the patterns in how handlers already decide. A person approves every rule, so every sort traces back to a decision a human made." Then the decision order, and the ladder: shadow mode, suggest, auto-route, with the gates for each step agreed per customer.

### 16. How we measure success · 30 sec

Leading and lagging metrics per release. "Analytics and action capture go live before bulk sorting launches, not after."

### 17. Where AI fits, from signal to measurement · 30 sec

Point at the last column: "What stays mine at every stage is the call."

---

## Section 6. GTM and Customer Success

### 18. What we tell them · 45 sec

"One story for Sales and CS: bulk sorting is the first release towards workflow automation." What wins against the competitor, the never-promise list, and the assets generated from the repo.

### 19. When · 30 sec

Walk the timeline. The top-10 renewal is one row: they're in the bulk sorting beta at week 6 and see release 2 on their own data before renewal.

### 20. What I cut · 20 sec

To fill in at the end.

---

## Section 7. How I used AI

### 21. How I used AI · 75 sec

The repo as a context hub, what I used AI for, and how I kept the decisions mine.

**Where I overrode it** (the brief asks for this; not on the slide):

- It recommended a React stack for the prototype; I asked for plain HTML so reviewers can open it anywhere.
- I put automation inside bulk sorting before the workflow builder, because that's where handlers already are.
- I chose a sample-data prototype over a story about a model trained on real claims, because a team with no product owner wouldn't have had customer data agreements.

### 22. Where AI got it wrong · 90 sec

Walk the four rows, then go deep on the middle pile: "The AI defined the middle pile as 'information missing' and carried it through the fact sheet, the research and the assumptions. I caught it because it didn't match my own brainstorm. It would have changed the product. Fixing it is how missing information became a status on any claim, and the first thing we automate."

### 23. How the lifecycle is changing · 75 sec

Discovery compresses; prototypes become the spec; judgement and reading become the job; decisions have to be explicit. Close on what I'd prioritise at Keelwater.
