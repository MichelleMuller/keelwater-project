# Customer and deal signal

Keelwater is fictional, so internal signal is simulated. Everything in this file is **[INVENTED]** unless it links to a real source.

## Sources [INVENTED]

- Gong recordings of sales calls, including the 6 open deals
- Teams meeting recordings with customers (transcripts from the meeting chat)
- Sessions with CSMs and AMs, including the 3 accounts that raised automatic sorting in reviews

## What we heard, reconfirmed by market research

| Finding | Internal signal | Market research |
|---|---|---|
| **Speed** (what handlers and claimants feel) comes mostly from piles 1 and 2, plus clearing missing information on any claim | **[INVENTED]** Handlers and claims ops leads describe the pain as claims sitting open, waiting on something, not as sorting being hard | Industry triage optimises for cycle time first; non-straight-through claims are mostly adjuster review (30%) and missing info (20%), not fraud (4%) ([research §1, §3](motor-claims-triage-and-fraud.md)) |
| **Money and risk** (what insurers' finance and fraud teams feel) sit in pile 3 | **[INVENTED]** Fraud comes up with finance and fraud stakeholders, framed as "don't let speed pay out fraud" rather than "find more fraud" | Fraud is a small share of claims but high value per case: ~£11k per detected UK motor fraud case ([research §3](motor-claims-triage-and-fraud.md)) |
| The 15% of claims taking >4h are more likely **complex or waiting-on-information** claims than fraud | **[INVENTED]** CSMs and AMs point to claims with a third party, injury or missing documents as the ones that get stuck | Third party, injury, disputed liability, total loss and missing documents are the most cited causes of motor claim delays ([research §2](motor-claims-triage-and-fraud.md)) |

## The 6 open deals (£2.3M ARR) [INVENTED]

**How we found it:** review of all Gong recordings for the 6 deals, summarised with AI by theme, then 15-minute calls with each AE to check the summary (SQ-01, SQ-02).

**What buyers value:**

1. **Speed:** clean claims paid faster, without adding handlers.
2. **Confidence that fraud is caught within that faster cycle.** Speeding up is only acceptable if suspicious claims are stopped before payment, not found afterwards.
3. **An expert in the loop.** Buyers want their handlers to confirm or override suggestions, and want the system to learn from those decisions over time.

**Also heard:**

- Fraud detection itself isn't what they're buying: most already have a fraud vendor. They want the sorting to **use** it.
- 4 of the 6 have seen the competitor's demo. "Automatic sorting" is a checklist item for them, but what wins is being able to explain each sort to their compliance team.
- None of the 6 asked for fully automatic payment.

This supports A-03: speed is the ask; fraud confidence and a human in the loop are what make it safe to buy.

## Still to validate

- The >4h tail split by cause: answered with invented data in [internal-data.md §2](internal-data.md); in reality a data request (A-13, DQ-03, DQ-04)
- The deal findings rest on Gong and AE input; confirm with buyers directly in the first customer sessions
