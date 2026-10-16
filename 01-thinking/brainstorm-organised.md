# Brainstorm, organised

The raw notes ([`brainstorm-raw.md`](brainstorm-raw.md)) reorganised against the five task questions. Content is Michelle's; structure and the ⚠️ flags are added. Nothing decided yet.

---

## 1. The problem and confidence

**Domain (decided):** Keelwater serves **motor claims** (car damage and repair). **[INVENTED]**, the brief only uses a car as an example.

**Working problem statement:** a lot of claims arrive at once and some get stuck. The value isn't sorting itself, it's getting claims to a **resolved** state (paid or rejected) faster and safely.

**Ideal end state**
- Simple → auto-sorted and routed to payment
- Needs a closer look → flagged with a reason and suggested next step (e.g. assign senior handler, establish fault)
- Suspicious → routed to investigation
- Any claim missing information → claimant chased automatically, whatever the pile

**Bucket definitions (working, revised 2026-10-16 after [research §2](../02-research/motor-claims-triage-and-fraud.md))**
- *Simple:* low value, own damage only, no injury, clear cover, no prior-claim or fraud flag → process and pay. e.g. cracked windscreen, £600, no other parties
- *Closer look:* complex but not suspicious; needs a handler's judgement. Third party / fault to determine, injury, disputed liability or cover, total loss, ~~above authority~~, multiple parties or large payout. *(Authority limit removed 2026-10-16: it's a payment step, not a sorting reason, A-20.)* e.g. car through a house, £5,000, multiple claimants. Carries a **reason code**
- *Suspicious:* fraud indicators. e.g. 7 claims from one person in 3 months, claim soon after policy start, damage that doesn't match the story
- *Missing information:* a **status on any claim**, not a pile

> ✏️ An earlier version of this file said pile 2 was "mainly information missing". That emphasis was added when organising; the raw brainstorm defines it as "complex but not suspicious", which matches industry triage.

**Reading of the data**
- ~80%+ of claims should be relatively easy to sort; 15% are the hard ones
- 4h+ to sort means it isn't simple
- Customer mix matters: some have ~99% simple claims, others are mostly complex
- 3.4% re-sort rate = a benchmark for acceptable error (human baseline)
**The problem (updated 2026-10-16 after [research](../02-research/motor-claims-triage-and-fraud.md))**

Triage is mainly about **speed**: getting every claim to the right handler first time. Fraud screening is the **licence to automate** the Simple pile, so speeding up doesn't pay out fraud. By volume, fraud is a small pile, and complex claims and claims waiting on information are much bigger. By value, fraud is high per case. See A-03.

> Earlier hypothesis, now replaced: ~~"fraud is the primary problem to solve"~~. The brief never said fraud was blocking the deals, only that they "mention" automatic sorting.

**Confidence:** to be stated explicitly in the deck. Demand for *something* is high-confidence; *what* customers mean by automatic sorting is low-confidence.

---

## 2. What to find out before committing the squad

**Questions**
- What's the main problem per customer? Why do some claims take hours? What's the full claim lifecycle, sort → paid?
- Breakdown per customer of volume, time-to-sort, and >4h share
- The 3.4% re-sorts: which direction (simple → suspicious or the reverse)? Which transitions are most common?
- What's in the ~40 support tickets: sorting in general, or doing many at once (the bulk sorting case)?
- Why was bulk sorting prioritised? What was validated, which customers are lined up?
- What's in the prototype: what model (rules / classic ML / LLM), trained on what, why was it stopped? Can it be shown to customers?
- Deterministic vs probabilistic: is any incorrect sort acceptable? Is this a good LLM use case?
- Same for all customers, or does each need configurable context/rules?
- Do carriers already have fraud models? What signals do they use?
- What does the competitor offer, how do they position it, where does it fail?

**Sources: internal first (fast), external second (slow)**
- Internal: the prototype, bulk sorting work, last 2 years of Gong recordings, usage data, support tickets, pipeline, at-risk accounts, AM feedback
- External: direct customer interviews to validate what internal data can't answer
- Note: Gong may not hold the answers if reps never asked the right questions. State assumptions where data is missing.
- Customer calls going forward: Teams over Gong (carriers are Microsoft shops; transcripts live in the meeting chat). Gong for historical calls.

**How AI speeds this up**
- Thematic analysis across support tickets and call transcripts
- Reconstruct why bulk sorting was prioritised from past calls and decisions, instead of fresh interviews
- Summarise competitor research; check fraud-detection maturity for auto claims; check Hugging Face for open models/datasets
- Leave it running: keep ingesting calls and tickets to track sentiment once rollout starts

---

## 3. Prioritisation, including bulk sorting

**Decided narrative:** the platform has **no tabular view today**, so handlers sort one claim at a time. Bulk sorting (table + filters + multi-select) is therefore needed in its own right. **We ship it**, and use it to validate the needs, requirements and safety bar for automated sorting: filter usage becomes the first rule set, and the launch is the moment to run customer sessions.

**Earlier read on bulk sorting (kept for context)**
- Likely implies no table view exists today; handlers sort one by one. Bulk = table + filters + multi-select + an API returning all claims, not just a checkbox.
- Filters act as a **proto-ruleset** ("all claims with every field filled, returning customer" → select all → Simple). Those actions become training data for automation.
- Has no fraud detection.
- Probably doesn't deliver the perceived value or win the deals on its own.
- Once automation exists, bulk may matter mostly for the simple bulk, or become less relevant.

**Two options considered in the notes**
- **A. Pause bulk sorting** and pivot the squad to automated sorting: evals → LLM-as-judge → run on synthetic data → customer pilot
- **B. Ship bulk sorting as the validation layer**: ship in 6 weeks, use it to confirm the simple-claim problem, collect filter usage as training signal, then auto-sort simple claims next

> ✅ Decided: **B**, ship bulk sorting as the validation layer for automation. See Q-01.

**Phasing in the deck outline**
- Phase 1: bulk sorting track (GTM, success metrics, analytics pre-launch, CSM-led review sessions)
- Phase 2: automated sorting track (tech lead + note-taker with customers; competitor displacement)
- Later: sorting is phase one; full claims processing is phase two

**Rule-based is fine** for the simple-claim flow; no ML needed there.

---

## 4. Signal → decision → validation → delivery → measurement

**Solution shape: fraud / suspicious detection**
- If the customer knows its fraud signals: enumerate them as questions, feed a calibrated decision model that returns structured outputs only (boolean, 0–1 score, category). No upfront training; evaluates against a rubric. Provenance per decision (which data point drove which output).
- If the customer doesn't: unsupervised learning on historical claims + outcomes to surface features. Risk: too few features (name, address, background check) for a significant model.
- Example signals: background check, prior claims, car type, location, driving history, claim frequency
- Agent framing: what skills and tools does it need; how do they hand off to one another

> ⚠️ "Typesafe/Jev" for the calibrated decision model: name to verify before it goes in the deck.

**Validation**
- Evals first, LLM-as-judge, run on synthetic data generated from realistic claim patterns
- Blind cases through the model; beta customers label outcomes; measure accuracy against the 3.4% baseline
- Need a beta group of customers willing to label
- Customer sessions around the bulk prototype at the 6-week mark; probe fraud-signal knowledge

**Safety gates before anything is automated**
- Full audit log per claim: all data used, every decision, scores, final outcome
- Sign-off from customer IT, governance, likely legal (not just the claims team)
- Customer and Keelwater agree a performance threshold before go-live

**Data, privacy, governance**
- Claims data contains PII (vehicles, injuries). Keelwater can't train on raw customer data by default; customers may not be allowed to share it (GDPR / US equivalents; to verify)
- Mitigation: auto-redact PII before data reaches a model or durable storage; local or in-memory processing. Check if redaction already exists in the pipeline.

**AI workflow setup**
- Context hub as the foundation for all AI-assisted work (Notion suggested: MCP, auto-transcription, sharing)
- Git repo for version control, connected to stakeholder-facing tools (this repo)

---

## 5. Sales and Customer Success

- Once the context hub exists, use agents to produce battle cards, sales scenarios, objection handlers, value props, customer-specific decks, AE training
- Segment customers by problem distribution (simple-heavy / complex-heavy / fraud-heavy) to sharpen positioning and pick a segment to own
- Competitor: find their failure points and unclaimed ground (if they own simple cases, go after fraud/complex)
- Team comms: share the deck async as a grooming debrief, then a Q&A with commercial, tech and design in the room. Design then explores the UX once it's confirmed worth prioritising.

> ⏸️ **Placeholder in the deck** for now: what to tell Sales/CS and when (week 1 holding message, what can be promised to the top-10 renewal in 5 months, what not to promise). See Q-04.
