# Keelwater: Automatic Claim Sorting

Take-home assignment (Senior/Lead PM, Xelix). Keelwater is fictional: B2B claims software, ~180 enterprise insurers. Customers, Sales and CS are pushing for **automatic sorting** of claims into *Simple / Needs a closer look / Suspicious*.

**The ask:** "Show us how you would move this forward." Format is open. Timebox: **3 hours**. Submit a **≤20 min recording** plus what was produced and 1–2 pieces of working material.

## Repo map

| Folder | What's in it |
|---|---|
| [`00-brief/`](00-brief) | The original brief (verbatim), a structured fact sheet with derived numbers, and the submission checklist |
| [`01-thinking/`](01-thinking) | Raw brainstorm (verbatim), the brainstorm reorganised against the five task questions, assumptions log, open questions |
| [`02-research/`](02-research) | Research plan and findings: internal data, competitor, fraud maturity, regulation |
| [`03-deliverables/`](03-deliverables) | The deck outline and final outputs |
| [`04-working-material/`](04-working-material) | AI usage log and drafts/approaches to include as working material |

## Key files

| What | File |
|---|---|
| **Solution prototype** (claim form → inbox → bulk sorting → workflow builder → agent). Open the HTML file by double-clicking | [`keelwater-prototype.html`](03-deliverables/solution-prototype/keelwater-prototype.html) · [plan and progress](03-deliverables/solution-prototype/PLAN.md) · [how to run](03-deliverables/solution-prototype/README.md) |
| Sample-data sorting prototype: gradient-boosted model with per-claim reasons | [`results.md`](04-working-material/prototype/results.md) · [`sorting_prototype.py`](04-working-material/prototype/sorting_prototype.py) |
| Time to sort: distribution and what claims are waiting on (charts) | [`time-to-sort-distribution.md`](02-research/time-to-sort-distribution.md) · [PNG for the deck](02-research/assets/time-to-sort-causes.png) |
| Research index (triage, auto-sorting requirements, examiner requirements, internal data, customer signal, Kaggle review) | [`02-research/README.md`](02-research/README.md) |
| Assumptions (A-01 to A-22) and invented items (I-01 to I-06) | [`assumptions-log.md`](01-thinking/assumptions-log.md) |
| Decisions and discovery questions by stakeholder | [`open-questions.md`](01-thinking/open-questions.md) |
| Deck outline | [`deck-outline.md`](03-deliverables/deck-outline.md) |
| AI usage log, incl. "one thing it got wrong" candidates | [`ai-usage-log.md`](04-working-material/ai-usage-log.md) |
| Kaggle claim data and notebook | [`04-working-material/kaggle/`](04-working-material/kaggle) |
| **Tests** for all the code: charts, sample-data prototype, solution prototype. Run `./tests/run.sh` (needs Python and Google Chrome; `pip install -r requirements.txt` into `.venv` for the model tests) | [`tests/`](tests) |

## Where we are

- [x] Brief and brainstorm captured
- [x] Brainstorm organised against the five task questions
- [x] Research: motor claims triage and fraud, auto-sorting requirements, examiner requirements, internal data and customer signal (invented), Kaggle review
- [ ] Research: competitor deep dive
- [x] Decide bulk sorting: **ship it** as the validation layer for automation (no tabular view exists today)
- [x] Sample-data sorting prototype (working material)
- [ ] Solution prototype: step 0 of 7 done ([progress](03-deliverables/solution-prototype/PLAN.md#9-progress))
- [ ] Build deck
- [ ] Record walkthrough (≤20 min, incl. ≤5 min on AI use + lifecycle)

## Conventions

- Anything invented (data, quotes, org detail) is tagged **[INVENTED]**. The brief requires this.
- Assumptions live in [`01-thinking/assumptions-log.md`](01-thinking/assumptions-log.md) with a status.
- Every meaningful AI-assisted step gets a line in [`04-working-material/ai-usage-log.md`](04-working-material/ai-usage-log.md). That log feeds the "How you used AI" section.
