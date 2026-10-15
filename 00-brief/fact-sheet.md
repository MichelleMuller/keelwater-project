# Fact sheet

Everything the brief gives us, in one place, plus simple derived figures. Derived numbers are arithmetic on brief data, not new data.

## Company and team

| | |
|---|---|
| Product | Claims handling software; handlers spend most of their day in it. We assume **motor claims** (car damage/repair) **[INVENTED]** |
| Customers | ~180 enterprise insurers |
| My squad | 1 designer, 1 tech lead, 5 engineers |
| In flight | **Bulk sorting** (sort many claims at once), halfway built, ships in **6 weeks** |
| Shelved asset | Data team prototype that predicts the pile. On hold **18 months** (team moved to other work) |
| Hard constraint | Insurers must be able to **explain every claim decision** to the customer and the regulator |

## Demand signals

| Source | Signal |
|---|---|
| Customers | Several large customers asked directly |
| Sales | 6 open deals mention it, **£2.3M ARR** combined; includes the biggest deal in the pipeline |
| Customer Success | 3 important accounts raised it in reviews; one is **top-10, renewal in 5 months** |
| Support | ~40 tickets in 6 months mention sorting |
| Market | A competitor launched automatic sorting last quarter |

## Product data (last 12 months)

| Metric | Brief | Derived |
|---|---|---|
| Claims sorted | 2.1M | ~175k/month; ~11.7k per customer/year on average (~32/day) |
| Median time to sort | 11 min | Most claims are *not* slow |
| Claims taking >4h | 15% | **~315k claims/year**, ~26k/month |
| Moved to a different pile within 30 days | 3.4% | **~71k claims/year**, ~6k/month |
| Avg deal size in the 6 deals | | ~£383k ARR |

## What the numbers do and don't tell us

- **Time to sort ≠ time handlers spend sorting.** 11 min median may be mostly queue wait. 4h+ could be waiting, not effort. Need to split wait time vs touch time.
- **The 3.4% is the human error baseline.** Any automated sorter is compared against this, not against perfection. Direction matters: Suspicious → Simple misses are costly (fraud paid out); Simple → Suspicious mostly costs time and customer goodwill.
- **Averages hide the distribution.** ~40 tickets across 180 customers is low; pain is likely concentrated in a few large accounts. Need per-customer breakdown.
- **Nothing says what's blocking the deals.** "Mentions automatic sorting" could mean speed, headcount, fraud, or a competitive checkbox.
