# Solution prototype: plan

A clickable prototype of the full claim lifecycle, from the claimant submitting a claim to an AI agent optimising each insurer's sorting workflow. We build it step by step and review each step together before moving on.

> Plan written 2026-10-17. Status per step is tracked in the table at the bottom.

---

## 1. What the prototype has to show

The story for the recording, in the order a viewer clicks through it:

1. **A claimant submits a claim.** As they fill in the form, a floating panel shows the structured claim record (the data schema) being built live. This is the data the sorting system runs on.
2. **Toggle to the handler view.** The same claim lands in the handler's inbox.
3. **Current state:** the inbox. Handlers open claims one at a time and sort each by hand.
4. **Phase 1, bulk sorting** (in flight, ships in 6 weeks): a table with every field, filters, multi-select and "sort selected into…". Every handler action is captured; this is the data that tells us what the automation rules should be.
5. **Phase 2, rules and workflow builder:** the system proposes rules learned from handler behaviour ("you sorted 41 windscreen claims under £1,000 with no third party as Simple"). Rules live in a drag-and-drop workflow: stages and actions connected into a pipeline, one workflow per insurer.
6. **Phase 3, Workflow Agent:** an AI layer over all claim and workflow data. It answers questions about any claim, and proposes workflow improvements with evidence. A human approves each change.

## 2. Guardrails from our research (non-negotiable in the prototype)

These come from [auto-sorting-requirements.md](../../02-research/auto-sorting-requirements.md) and [examiner-requirements.md](../../02-research/examiner-requirements.md). The prototype should make them visible, because they're part of the pitch.

| Guardrail | Where it shows up |
|---|---|
| **Decision order:** missing info → fraud gate → complexity → Simple only if every check passes; default is Needs a closer look | Default workflow in the builder; reasons on every suggestion |
| **Missing information is a status, not a pile** (A-19) | "Waiting on claimant" status in every phase; auto-request in Phase 2 |
| **Never auto-deny or auto-reduce** (E-04) | Builder has no "deny" action; Suspicious routes are suggest-only by default |
| **Every sort is explained** (E-01, E-03) | Reason codes on every row and claim; decision record per claim |
| **Human decision logged next to the suggestion** (E-02) | Confirm / override with reason; overrides feed the learning loop |
| **Every rule change is versioned, tested and reversible** (E-06, E-07) | Workflow versions; "test on last 30 days" before publishing; agent proposals need approval |
| **Per-customer configuration** (AS-05) | Insurer switcher; each has its own workflow and thresholds |
| **Very high-value Simple claims get a senior review before payment** (A-20) | Status on Simple claims above the insurer's limit |

## 3. Where the brief we were given and our repo meet: decisions to make

Points where the requested flow needs a choice, with my recommendation. To decide together before the step they affect.

> **Decided 2026-10-17 (Michelle):** P-01 the agent proposes, a human approves. P-02 scripted, grounded answers labelled as simulated. P-03 the insurer's branded form, used as a reference for the full user flow (not a Keelwater product claim). ~~Technical approach: React + Radix Themes + React Flow, built with Vite into one inlined HTML file.~~ **Revised: plain HTML, CSS and JS in one file, no Node or build step** (portability). Build step 0, then review.

| # | Question | Recommendation | Affects step |
|---|---|---|---|
| P-01 | **Phase 3 "auto-optimises workflows":** does the agent change workflows itself? | **The agent proposes, a human approves.** Each proposal shows the evidence (e.g. override rate on a rule), a backtest on recent claims, and publishes as a new reversible version. Auto-applying rule changes would break E-06/E-07 and the NAIC bulletin's change control | 6 |
| P-02 | **"Answers any question about any claim":** live AI or scripted? | **Scripted, grounded answers.** A static file has no server or API key, so the agent matches a set of question types and answers from the claim record and audit log, citing the fields it used. We say clearly it's simulated | 6 |
| P-03 | **Consumer interface:** Keelwater sells to insurers. Whose form is it? | **The insurer's branded claim form, powered by Keelwater** (white-label first notice of loss). New assumption A-23 | 1 |
| P-04 | **Where does missing-information flagging sit?** We decided it's the first thing to automate | **Status available from Phase 1** (handler sets "waiting on claimant"); **automated as the first node of the Phase 2 workflow** (detect + auto-request) | 3, 5 |
| P-05 | **Phase 2 rollout:** the repo says shadow → suggest → auto-route | **Show a mode switch per workflow:** Suggest (handler confirms) and Auto-route (above a confidence threshold). Suspicious stays suggest-only | 4, 5 |
| P-06 | **Brand:** Keelwater product in the Xelix brand system | Keelwater wordmark set in the Xelix style (Barlow, Xelix rose and navy). Consumer form uses a neutral insurer brand so the two views feel different | 0, 1 |

## 4. Technical approach

**Decided: one plain HTML file with all CSS and JavaScript inline.** No Node, no npm, no build step: edit the file, refresh the browser. Easy to carry around and to put in the repo.

- **The Radix look without the Radix library:** Radix's component library needs React, so instead the file uses Radix Colors scales, Radix Themes-style components written in CSS, and Radix Icons as inline SVG, with Xelix brand tokens on top.
- **Barlow embedded** as a base64 font at the end of the file, so it works offline (~120 KB).
- **Workflow canvas hand-built** with SVG and pointer events (nodes you drag, connectors you draw). Simpler than React Flow, enough for the prototype.
- All data in memory, seeded with 60 synthetic claims across 3 insurers. **[INVENTED]**, values shaped by the Kaggle data and our invented segments.
- Code is organised in labelled sections in the one script: data, state and routing, rendering helpers, one section per screen, events.

> Revised 2026-10-17: step 0 was first built with React + Radix Themes + React Flow, bundled by Vite into one inlined file (~1.3 MB). Michelle asked for no Node modules or build tooling so the prototype stays portable, so it was rewritten in plain HTML, CSS and JS (~145 KB).

**Xelix tokens** (from xelix.com and Brandfetch): font **Barlow**; rose `#EB3FC7` (primary accent), navy `#000A34` (text, sidebar), violet `#6A1BB5` / `#320C5B`, lavender `#CBB2FF` / `#DEE0FF` (surfaces, highlights). Pile colours: Simple green, Needs a closer look amber, Suspicious red, Waiting on claimant blue.

## 5. The claim record (schema)

One shape flows from the consumer form into every handler view. Draft:

```ts
type Claim = {
  id: string; insurer: "Harbour Mutual" | "Northgate Direct" | "Fleetwise Commercial";
  receivedAt: string; channel: "web form" | "phone" | "broker";
  policy: { number: string; startDate: string; cover: "comprehensive" | "third party, fire & theft" | "third party"; excess: number };
  claimant: { name: string; email: string; phone: string; priorClaims5y: number };
  vehicle: { reg: string; make: string; model: string; year: number; value: number };
  incident: { date: string; type: "collision" | "windscreen" | "theft" | "vandalism" | "weather" | "other";
              location: string; description: string; policeReport: boolean; policeRef?: string };
  parties: { thirdPartyInvolved: boolean; thirdParty?: { name: string; insurer?: string; reg?: string };
             injuries: boolean; injuryDetails?: string; witnesses: number };
  damage: { estimatedAmount: number; drivable: boolean; photos: number; repairEstimate: boolean };
  // filled by the system, not the claimant
  missingInfo: string[];                       // e.g. ["police report", "photos"]
  fraud: { score: number; vendor: string; reasons: string[] };   // from the insurer's vendor
  suggestion?: { pile: Pile; reasons: string[]; confidence: number; rule: string; workflowVersion: string };
  pile?: Pile; status: "new" | "waiting on claimant" | "sorted" | "senior review before payment";
  history: { at: string; actor: "system" | "agent" | string; action: string; detail?: string }[];
};
type Pile = "Simple" | "Needs a closer look" | "Suspicious";
```

## 6. Build steps

Each step ends with a review together before the next. **Every step adds tests** to [`tests/prototype.test.html`](../../tests/prototype.test.html) for what it built, and is only done when `./tests/run.sh` passes for the whole project. Layout bugs we fix get a test too, so they can't come back.

| Step | What we build | Done when |
|---|---|---|
| **0. Scaffold and shell** | One HTML file with Radix-style CSS and Xelix tokens. App shell: top bar with **Consumer ↔ Handler toggle**; handler view has a sidebar with **Current · Phase 1 · Phase 2 · Phase 3** and an insurer switcher. Seed data | `keelwater-prototype.html` opens offline and switches views |
| **1. Consumer claim form** | Multi-step form: policy → what happened → vehicle and damage → other people and injuries → photos and documents → review and submit. **Floating schema panel** shows the claim record filling in live, highlighting each field as it changes. Missing items shown before submit. On submit, the claim enters the shared store with a toast "Sent to Harbour Mutual's claims team" and a link to the handler view | A submitted claim appears in the inbox with the same data |
| **2. Current state: inbox** | List of incoming claims; open one at a time in a detail view (all fields, photos placeholders, history); buttons to sort into a pile. A small counter shows claims sorted and median time to sort, to make the one-by-one pain visible | Sorting a claim updates the record and history |
| **3. Phase 1: bulk sorting** | Radix table with all key fields; filters (claim type, amount range, third party, injury, prior claims, missing info, fraud score); multi-select; "Sort selected into…" and "Mark waiting on claimant". **Behaviour capture panel**: every filter + bulk action is logged, e.g. "Filter: windscreen, < £1,000, no third party → 23 claims → Simple" | Bulk actions work; the capture log fills as you use it |
| **4. Phase 2a: rules learned from behaviour** | "Suggested rules" built from the capture log, each with support ("you did this 41 times, overrode it twice"). Accept turns it into a rule in the workflow. Claims now show a **suggested pile with reasons** and confidence; handlers confirm or override (with a reason) | Accepting a suggested rule changes suggestions in the table |
| **5. Phase 2b: workflow builder** | Drag-and-drop canvas per insurer. Node palette: **Start (claim arrives)**, **Missing info check → request from claimant**, **Fraud gate (vendor score + hard rules)**, **Condition** (field, operator, value), **Route to pile**, **Assign** (senior handler, engineer), **Hold for senior review before payment**. Default workflow follows our decision order. Side panel to edit a node. **Test run** on the last 30 days of claims: how many go to each pile and agreement with handlers. **Publish** creates a new version. Mode per workflow: Suggest / Auto-route | Editing the workflow and publishing changes the pile suggestions in the table |
| **6. Phase 3: Workflow Agent** | Agent panel on top of all views. **Ask:** "Why is CLM-1042 in Suspicious?", "What's missing on Sarah Patel's claim?", "Which claims are stuck over 4h?" answered from the record and history, citing fields (scripted, P-02). **Optimise:** proposal cards, e.g. "Handlers override *Third party → Closer look* 34% of the time when liability is admitted; split the rule?", with evidence, backtest and Approve / Dismiss (P-01). Approving publishes a new workflow version | Asking about a claim gives a grounded answer; approving a proposal updates the workflow |
| **7. Decision record, polish and hand-off** | Per-claim decision record (inputs, rules fired, fraud score + vendor, suggestion, human decision) as an "Audit" tab. Empty states, copy pass, [INVENTED] labels where needed. Build, README with how to open it, link from the deck outline and AI log | One file in the repo; walkthrough under 3 minutes of the recording |

## 7. Deck notes to add as we go

- **Phase 1 data capture informs Phase 2 rules:** every filter and bulk action is a labelled example of how handlers sort (deck slide 3).
- **Why a workflow builder is now cheap:** before AI-assisted development, a drag-and-drop workflow builder was a quarter-long platform project. With AI coding tools and off-the-shelf canvas libraries, a working version is days of work, so per-insurer workflows become realistic for a small squad. This prototype is the evidence (deck slide 4).
- **The agent proposes, people decide:** auto-optimisation within change control (P-01).

## 8. Out of scope

Real AI model calls, a backend, logins, a real fraud vendor connection, payments, mobile layout for the handler view, accessibility audit beyond Radix defaults.

## 9. Progress

| Step | Status |
|---|---|
| 0. Scaffold and shell | **done 2026-10-17**, to review. Plain HTML file, works offline (~145 KB); claimant/handler toggle; sidebar by phase; insurer switcher; 60 seeded claims across 3 insurers; deep links via URL hash |
| 1. Consumer claim form | **done 2026-10-17**, to review. Harbour Mutual branded form in 6 steps (details, what happened, vehicle and damage, other people, photos and documents, review) with an "example claim" shortcut. Floating panel shows the claim record building live; fields the insurer's systems add are marked ⏳. The review step says what's still missing, but the claimant can send anyway (missing info is a status, A-19). Submitting creates CLM-2001+ in the handler's data, with a button through to the inbox |
| 2. Current state: inbox | **done 2026-10-17**, to review. Claims list (To sort / Sorted / All) beside the open claim: every field, photos, fraud vendor score, missing info, history. Pile buttons; "Ask claimant for missing info" sets a status, not a pile. After sorting, the next claim opens, as in today's queue. Counters: to sort, sorted by you, median time to sort (brief's 11 min, static), waiting over 4 h. A claim sent from the form arrives open and marked "Just submitted". Seed arrival times changed so about a quarter of the queue has waited over 4 h, closer to the brief. 13 new tests (41 browser tests in all) |
| 3. Phase 1: bulk sorting | **done 2026-10-17**, to review. Table of the insurer's claims (newest first; sort by amount or fraud score) with 8 filters: status, claim type, amount band, third party, injury, prior claims, missing info, fraud score band. Multi-select with a part-selected state; "Sort into" the three piles; "Mark waiting on claimant" only changes claims with something missing. Same claims as the inbox, so bulk sorts show there too. **Capture panel** logs every filter and bulk action in plain words ("14 claims → Simple · Windscreen, under £1,000, no third party · 1 left out by hand"), stored with the filter values so step 4 can learn rules from them. "Load an example week of sorting" adds 55 made-up actions [INVENTED] so step 4 has enough to learn from. Once it's loaded, **sample filters** appear: the example week's filter patterns that match 2+ of today's unsorted claims, each with its count and the pile handlers usually chose; one click applies the filters, ready to select all and sort. Scroll position now kept when ticking boxes (inbox list too). 20 new tests (61 browser tests in all) |
| 4. Phase 2a: rules from behaviour | **done 2026-10-17**, to review. Built as an **Automation panel** on the bulk sorting page, between the metric cards and the table (Michelle's call: automation arrives in bulk sorting before the workflow builder). Suggested rules are learned from the capture log once the same filter-and-pile pattern is repeated 3 times, with support (times, claims, left out by hand) and how many unsorted claims match now; Accept or Dismiss. Active rules have a **Suggest / Auto-sort** switch (Suspicious is suggest-only), undo for auto-sorts and Turn off. The table gets a **Suggested** column with the rule as the reason and a one-click confirm; "Confirm N suggestions" for a selection; a "Suggestion" filter. Decision order enforced: Simple is held back while info is missing or the fraud score is high, and the most cautious matching rule wins. Sorting against a suggestion counts as an override. A claim submitted from the form is auto-sorted on arrival if an auto-sort rule matches. Every rule change is recorded for the step 7 audit view. 17 new tests (78 browser tests in all). **Per-insurer example weeks** [INVENTED], each shaped by its segment's main problem in internal-data.md §1: Harbour Mutual (simple-heavy) learns mostly Simple rules; Northgate Direct (mixed) spends most of the week chasing missing info and sorting third-party collisions, and its "2+ prior claims → Closer look" rule shows the most cautious rule beating a Simple rule; Fleetwise Commercial (complex-heavy) learns large-collision, injury and fraud rules, with almost nothing Simple. 3 more tests (81 browser tests). **Override with a reason (E-02):** sorting against a suggestion, in bulk or from the inbox, opens a "Why not Simple?" dialog with quick-pick reasons and a note ("Other" needs a note); nothing is sorted until a reason is given, and a mixed bulk sort only asks about the claims that go against their suggestion. The reason goes on the claim's history, the capture log and the rule ("Overridden because: Liability is disputed (2)"), ready for the Workflow Agent in step 6. **Suggestion in the inbox:** an open claim shows the suggested pile, kept % and rule with a Confirm button (sorts and moves on), or why Simple was held back. **Live confidence:** a rule's kept % now counts confirms and overrides since it was accepted, so overrides lower it straight away in the panel and the table. 7 more tests (88 browser tests). **Auto-sort feedback** (Michelle found switching modes looked broken because claims silently left the table): switching to Auto-sort sorts straight away, then a banner says how many were sorted and held back, with **View them in the table** (rule filters + Sorted; rows tagged "Auto") and **Undo**; switching back to Suggest says the auto-sorted claims stay sorted, with "Undo those N"; auto-sort with nothing to sort says so. 4 more tests (92 browser tests) |
| 5. Phase 2b: workflow builder | **done 2026-10-17**, to review. Workflow page with a **vertical pipeline**: start → missing info → fraud gate → Suspicious rules → Closer-look rules → Simple rules → assign → senior review → end. Palette with drag-and-drop onto stages (and reorder within a stage); side panel to edit each step. Required steps (missing info, fraud gate, senior review) can be edited but not removed. **One source of truth** (Michelle's call): the rules live in the workflow, so accepting, turning off or switching a rule on the bulk page publishes a new version, and suggestions always come from the live version. Edits go in a draft; **Publish needs a fresh test run** against 30 days of past claims with the handlers' piles **[INVENTED]** (shows how many claims each step decides and how often it agrees with handlers). Every publish is a version with a plain-language note; any version can be restored. **Rule mode** (Michelle's call, a refinement of P-05): a Suggest / Auto-sort switch per rule plus a workflow-level threshold (80–95%, default 90%). A rule whose handlers kept its suggestion less often than the threshold has auto-sort paused. A rule made in the builder has no history, so it can't auto-sort yet. Suspicious stays suggest-only. Missing-info step can auto-request the documents. Assign step routes matching claims to a team; Simple claims at or above the senior-review amount wait for review before payment. 111 browser tests; mutation-checked (publishing without a test, ignoring the threshold, dropping the fraud gate each fail a test). Removed a duplicate click handler that logged filter changes twice |
| 6. Phase 3: Workflow Agent | not started |
| 7. Decision record, polish and hand-off | not started |
