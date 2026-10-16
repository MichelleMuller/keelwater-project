# Kaggle car insurance claim data and prediction notebook: what we can reuse

**Question:** can we reuse the logic of a public claim prediction model for Keelwater's auto-sorting?

**Short answer:** partly. The notebook predicts **whether a policyholder will file a claim**, which is an underwriting and pricing question. Keelwater needs to decide **how to handle a claim that has already been filed**. The method carries over (handling leakage and missing data, measuring imbalanced classes, comparing a simple model against a complex one); a few features carry over as fraud signals. The demographic features must not.

> Files: [`car_insurance_claim.csv`](../04-working-material/kaggle/car_insurance_claim.csv) (real, public, [Kaggle: xiaomengsun](https://www.kaggle.com/datasets/xiaomengsun/car-insurance-claim-data)) and [`car-insurance-claim-prediction.ipynb`](../04-working-material/kaggle/car-insurance-claim-prediction.ipynb). Analysis 2026-10-16. Check the dataset licence before sharing outside the assignment.

---

## 1. What's in the data

- **10,302 US policyholders**, one row each, amounts in dollars
- **Target:** `CLAIM_FLAG`, whether they filed a claim. **26.7%** did
- **Claim amount** for those who claimed: median **$4,104**; 75% under $5,727; 90% under $8,131; **7% over $10k**; max $123k
- **Driving and claims history:** prior claim count (`CLM_FREQ`) and value (`OLDCLAIM`), licence revoked (`REVOKED`), motor vehicle record points (`MVR_PTS`), years as a customer (`TIF`)
- **Vehicle:** type, value (`BLUEBOOK`), age, private or commercial use, urban or rural
- **Demographics:** age, gender, marital status, children, education, occupation, income, home value
- **Missing values:** 5–6% missing in income, home value, occupation, car age and years in job

## 2. What the notebook does

1. Cleans the data: strips `$` and `z_` prefixes, drops duplicates and ID columns
2. **Removes `CLM_AMT` as leakage:** the claim amount is only known after a claim happens
3. Fills missing values (median and nearest-neighbour imputation), scales and encodes features
4. Compares five models with stratified cross-validation, scored on **balanced accuracy** because claimants are the minority
5. Tunes and trains LightGBM; plots feature importance

| Model | Test balanced accuracy |
|---|---|
| Logistic regression | **71.9%** |
| Decision tree | 61.6% (overfits: 100% on training data) |
| Random forest | 63.1% (overfits) |
| CatBoost | 68.6% |
| LightGBM (tuned) | **~74%** |

## 3. What we can reuse

| From the notebook | How it applies to Keelwater |
|---|---|
| **Remove leakage** (`CLM_AMT`) | Don't train on anything known only after sorting: final outcome, later re-sorts, engineer's report. Learning from handler decisions is a related trap: the model copies their mistakes |
| **Balanced accuracy** for a minority class | Suspicious is a small pile. Overall accuracy hides missed fraud; measure each pile, and weight errors by direction ([discovery-answers.md §3](discovery-answers.md)) |
| **Simple model nearly as good as complex** (logistic regression 71.9% vs LightGBM ~74%) | A strong argument for **explainable models**. Two points of accuracy rarely justify extra complexity. Tree models like LightGBM can still give per-claim reasons by tracing which features drove each prediction, but those explain the model, not the claim, and are harder to defend to examiners than a rule ([examiner-requirements.md](examiner-requirements.md)) |
| **Overfitting check** (train vs test gap) | Validate on held-out claims and on customers the model hasn't seen, since claim mix varies by customer |
| **History features:** prior claims, years as a customer, licence revoked, record points | Candidate fraud gate signals. Claimants have more prior claims (1.23 vs 0.65) and shorter tenure (4.8 vs 5.5 years), in line with "claim soon after policy start" ([motor-claims-triage-and-fraud.md §4](motor-claims-triage-and-fraud.md)) |
| **Claim amount distribution** | A starting point for the Simple value threshold: in this data, 90% of claims are under ~$8k and 7% over $10k. To set per customer |
| **Missing-value handling** | Real data has gaps (5–6% here). For training, impute. **For live claims, don't impute: flag it.** That's the missing-information feature |
| **Realistic seed for synthetic claims** | Field types, value ranges and distributions for the synthetic dataset we'd evaluate on before customer data is available (AS-07) |

## 4. What we must not reuse

- **Demographic features in claim decisions:** gender, marital status, age, education, occupation, income, children. Using them to route claims risks unfair discrimination. Colorado requires bias testing for auto insurers' models, including in claims; FCA Consumer Duty requires fair outcomes; the UK bans gender in insurance pricing ([examiner-requirements.md](examiner-requirements.md)). The notebook uses all of them.
- **"Likely to claim" as a fraud signal:** a score of how likely someone is to claim says nothing about whether *this* claim is genuine. Using it at claim time would profile honest claimants.
- **The target:** whether someone claims isn't the pile. We'd need claim-level labels: the confirmed pile, final outcome, fraud confirmed or not.

## 5. What this data can't tell us

- No claim type, parties, injury, liability, documents or free text: none of the complexity signals for Needs a closer look
- No fraud labels or pile labels
- Policyholder level, not claim level; US only; dated (published 2019)

## 6. Suggested next steps

0. **Done 2026-10-16:** [sorting prototype on sample data](../04-working-material/prototype/results.md), a gradient-boosted model with per-claim reasons, trained on rule-made labels.
1. **Use it as the seed for a synthetic claims dataset:** keep the history and vehicle fields, drop demographics, and add generated claim-level fields (claim type, third party, injury, documents present, fraud label) with **[INVENTED]** rules.
2. **Run a dry-run eval** of the decision order in [auto-sorting-requirements.md](auto-sorting-requirements.md) on it, scored with balanced accuracy per pile. This could be the working material for the submission.
3. **Show the explainability trade-off** in the deck: logistic regression vs LightGBM, two points of accuracy vs per-claim reasons.
