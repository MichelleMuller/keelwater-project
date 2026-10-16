"""Sample-data sorting prototype: a concept, not something to rely on.

Recreates the shelved data-team prototype (internal-data.md §6) on public data:
- Claims: the Kaggle car insurance rows where a claim was filed (CLAIM_FLAG = 1).
- Claim-level fields the dataset lacks (claim type, third party, injury, documents,
  days since policy start) are generated with fixed random rules. [INVENTED]
- Pile labels come from simple rules, plus 3% random flips to mimic handler
  inconsistency. [INVENTED] The model can only relearn these rules.
- Demographic fields are dropped (kaggle-claim-prediction-review.md §4).

Per-claim reasons: for each tree in the gradient-boosted model, the change in
score at every split on the claim's path is credited to the split's feature
(path attribution). Summed over trees, this decomposes the model's score for
the suggested pile exactly into per-feature contributions.

Run: .venv/bin/python 04-working-material/prototype/sorting_prototype.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import balanced_accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
DATA = HERE.parent / "kaggle" / "car_insurance_claim.csv"
SEED = 7

SIMPLE_MAX_AMOUNT = 6_000  # per-customer setting in the real product
AUTHORITY_LIMIT = 5_000  # Simple claims above this get a senior review before payment (A-20)
LABEL_NOISE = 0.03

PILES = ["Simple", "Needs a closer look", "Suspicious"]


def money(s):
    return s.astype(str).str.replace(r"[$,]", "", regex=True).replace("", np.nan).astype(float)


def load_claims():
    raw = pd.read_csv(DATA)
    raw = raw[raw.CLAIM_FLAG == 1].reset_index(drop=True)
    return pd.DataFrame(
        {
            "claim_amount": money(raw.CLM_AMT),
            "car_value": money(raw.BLUEBOOK),
            "car_age": raw.CAR_AGE.fillna(raw.CAR_AGE.median()).clip(lower=0),
            "car_type": raw.CAR_TYPE.str.replace("z_", ""),
            "commercial_use": (raw.CAR_USE == "Commercial").astype(int),
            "prior_claims": raw.CLM_FREQ,
            "prior_claims_value": money(raw.OLDCLAIM),
            "licence_revoked": (raw.REVOKED == "Yes").astype(int),
            "record_points": raw.MVR_PTS,
            "years_as_customer": raw.TIF,
        }
    )


def add_invented_fields(df, rng):
    n = len(df)
    df["claim_type"] = rng.choice(
        ["collision", "windscreen", "vandalism", "theft", "other damage"],
        size=n,
        p=[0.62, 0.15, 0.10, 0.03, 0.10],
    )
    windscreen = df.claim_type == "windscreen"
    df.loc[windscreen, "claim_amount"] = rng.integers(250, 1_500, windscreen.sum())

    collision = df.claim_type == "collision"
    df["third_party"] = (collision & (rng.random(n) < 0.45)).astype(int)
    injury_p = np.where(df.third_party == 1, 0.25, np.where(collision, 0.05, 0.0))
    df["injury"] = (rng.random(n) < injury_p).astype(int)

    first_year = df.years_as_customer <= 1
    df["days_since_policy_start"] = np.where(
        first_year,
        rng.integers(1, 366, n),
        (df.years_as_customer - 1) * 365 + rng.integers(0, 365, n),
    )
    df["amount_to_car_value"] = (df.claim_amount / df.car_value).round(3)

    df["has_photos"] = (rng.random(n) < 0.90).astype(int)
    df["has_police_report"] = (rng.random(n) < 0.70).astype(int)
    return df


def rule_label(row):
    if (
        row.claim_type == "theft"
        or row.days_since_policy_start <= 30
        or row.prior_claims >= 4
        or (row.licence_revoked and row.record_points >= 7)
        or (row.amount_to_car_value > 1.5 and not row.third_party and not row.injury)
    ):
        return "Suspicious"
    if (
        row.third_party
        or row.injury
        or row.claim_amount > SIMPLE_MAX_AMOUNT
        or row.amount_to_car_value > 0.7
    ):
        return "Needs a closer look"
    return "Simple"


def missing_info(row):
    missing = []
    if not row.has_photos:
        missing.append("photos")
    needs_report = row.claim_type == "theft" or row.third_party or row.injury
    if needs_report and not row.has_police_report:
        missing.append("police report")
    return ", ".join(missing)


def features(df):
    X = df[
        [
            "claim_amount",
            "car_value",
            "amount_to_car_value",
            "car_age",
            "commercial_use",
            "prior_claims",
            "prior_claims_value",
            "licence_revoked",
            "record_points",
            "days_since_policy_start",
            "third_party",
            "injury",
        ]
    ].copy()
    for t in ["theft", "windscreen", "vandalism", "collision"]:
        X[f"type_{t}"] = (df.claim_type == t).astype(int)
    return X


def path_contributions(model, x, k):
    """Per-feature contributions to the raw score of class k for one claim."""
    contrib = np.zeros(len(x))
    for tree in model.estimators_[:, k]:
        t = tree.tree_
        node = 0
        while t.children_left[node] != -1:
            f = t.feature[node]
            child = t.children_left[node] if x[f] <= t.threshold[node] else t.children_right[node]
            contrib[f] += t.value[child][0][0] - t.value[node][0][0]
            node = child
    return contrib * model.learning_rate


def reason(feature, value, push):
    v = value
    phrases = {
        "claim_amount": f"claimed ${v:,.0f}",
        "car_value": f"car worth ${v:,.0f}",
        "amount_to_car_value": f"claim is {v:.0%} of the car's value",
        "car_age": f"car is {v:.0f} years old",
        "commercial_use": "commercial vehicle" if v else "private vehicle",
        "prior_claims": f"{v:.0f} prior claim{'' if v == 1 else 's'} in 5 years",
        "prior_claims_value": f"${v:,.0f} claimed before",
        "licence_revoked": "licence revoked before" if v else "licence never revoked",
        "record_points": f"{v:.0f} driving record points",
        "days_since_policy_start": f"claim {v:.0f} days after policy start",
        "third_party": "third party involved" if v else "no third party",
        "injury": "injury reported" if v else "no injury",
        "type_theft": "theft claim" if v else "not a theft",
        "type_windscreen": "windscreen claim" if v else "not a windscreen claim",
        "type_vandalism": "vandalism claim" if v else "not vandalism",
        "type_collision": "collision" if v else "not a collision",
    }
    return phrases[feature]


def top_reasons(model, X, i, k, n=3):
    x = X.iloc[i].to_numpy(dtype=float)
    c = path_contributions(model, x, k)
    order = np.argsort(-c)[:n]
    return [reason(X.columns[j], x[j], c[j]) for j in order if c[j] > 0]


def main():
    rng = np.random.default_rng(SEED)
    df = add_invented_fields(load_claims(), rng)
    df["rule_pile"] = df.apply(rule_label, axis=1)
    flip = rng.random(len(df)) < LABEL_NOISE
    df["label"] = df.rule_pile
    df.loc[flip, "label"] = [rng.choice([p for p in PILES if p != r]) for r in df.loc[flip, "rule_pile"]]
    df["missing_info"] = df.apply(missing_info, axis=1)

    X = features(df)
    y = df.label.map({p: i for i, p in enumerate(PILES)})
    idx_train, idx_test = train_test_split(df.index, test_size=0.25, stratify=y, random_state=SEED)

    model = GradientBoostingClassifier(n_estimators=150, max_depth=3, learning_rate=0.1, random_state=SEED)
    model.fit(X.loc[idx_train], y.loc[idx_train])

    Xt, yt = X.loc[idx_test].reset_index(drop=True), y.loc[idx_test].reset_index(drop=True)
    test = df.loc[idx_test].reset_index(drop=True)
    proba = model.predict_proba(Xt)
    pred = proba.argmax(axis=1)

    test["suggested_pile"] = [PILES[k] for k in pred]
    test["confidence"] = proba.max(axis=1).round(2)
    test["reasons"] = ["; ".join(top_reasons(model, Xt, i, pred[i])) for i in range(len(Xt))]
    test["status"] = [
        f"waiting on claimant: {m}" if m else "" for m in test.missing_info
    ]
    review = (test.suggested_pile == "Simple") & (test.claim_amount > AUTHORITY_LIMIT)
    test.loc[review, "status"] = (test.loc[review, "status"] + "; senior review before payment").str.lstrip("; ")

    acc = (pred == yt).mean()
    bal = balanced_accuracy_score(yt, pred)
    cm = confusion_matrix(yt, pred, labels=[0, 1, 2])
    recall = cm.diagonal() / cm.sum(axis=1)
    share = df.label.value_counts(normalize=True).reindex(PILES)

    cols = ["claim_type", "claim_amount", "suggested_pile", "confidence", "reasons", "status", "label", "rule_pile"]
    test[cols].to_csv(HERE / "suggestions.csv", index_label="claim")

    def row_md(i, r):
        return (
            f"| {i} | {r.claim_type} | ${r.claim_amount:,.0f} | **{r.suggested_pile}** | {r.confidence:.0%} "
            f"| {r.reasons} | {r.status or '—'} | {r.label} | {r.rule_pile} |"
        )

    picks = []
    for pile in PILES:
        picks += test.index[(test.suggested_pile == pile) & (test.label == pile)][:2].tolist()
    picks += test.index[test.status.str.contains("senior review")][:1].tolist()
    picks += test.index[test.status.str.contains("waiting")][:1].tolist()
    picks += test.index[test.suggested_pile != test.label][:2].tolist()
    picks = list(dict.fromkeys(int(p) for p in picks))

    lines = [
        "# Sorting prototype on sample data: results",
        "",
        "Generated by [`sorting_prototype.py`](sorting_prototype.py). **A concept, not something we can rely on:** public sample data, invented claim fields, rule-made labels. See [internal-data.md §6](../../02-research/internal-data.md).",
        "",
        "## Setup",
        "",
        f"- **{len(df):,} claims**: the Kaggle rows where a claim was filed. Demographic fields dropped.",
        "- **Invented fields** (fixed random rules): claim type, third party, injury, photos and police report present, days since policy start.",
        f"- **Labels from rules**, with {LABEL_NOISE:.0%} flipped at random to mimic handler inconsistency. Pile shares: "
        + ", ".join(f"{p} {share[p]:.0%}" for p in PILES)
        + ".",
        f"- **Model:** gradient-boosted trees (150 trees, depth 3). Trained on {len(idx_train):,} claims, tested on {len(idx_test):,} it hadn't seen.",
        "",
        "## How well it relearns the rules",
        "",
        "| Measure | Result |",
        "|---|---|",
        f"| Agreement with labels | {acc:.1%} |",
        f"| Balanced accuracy (each pile counts equally) | {bal:.1%} |",
    ]
    lines += [f"| Recall: {p} | {r:.1%} |" for p, r in zip(PILES, recall)]
    lines += [
        "",
        "Confusion matrix (rows = label, columns = suggestion):",
        "",
        "| | " + " | ".join(PILES) + " |",
        "|---|---|---|---|",
    ]
    lines += [f"| **{p}** | " + " | ".join(str(v) for v in cm[i]) + " |" for i, p in enumerate(PILES)]
    lines += [
        "",
        f"The ceiling is about {1 - LABEL_NOISE * 2 / 3:.0%}, because {LABEL_NOISE:.0%} of labels were flipped at random. **This shows the model can relearn rules; it says nothing about real claims.**",
        "",
        "## What a handler would see in the bulk sorting table (A-21)",
        "",
        "A sample of test claims. Reasons are the three features that pushed the model most towards its suggestion. Status shows missing information (any pile) and the senior review before payment for high-value Simple claims (A-20).",
        "",
        "| # | Type | Amount | Suggested pile | Confidence | Why | Status | Label | Rules alone say |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    lines += [row_md(i, test.loc[i]) for i in picks]
    lines += [
        "",
        "Full test set: [`suggestions.csv`](suggestions.csv). Where the suggestion and the label disagree but match \"rules alone say\", the label was one of the randomly flipped ones: the model was right and the \"handler\" was inconsistent.",
        "",
        "**Some reasons look odd.** A claim can be in Needs a closer look because it's over the $6,000 Simple limit, yet the top reasons list prior claims or days since policy start. The model splits credit across features that move together, so its reasons don't always match the rule a person would give. That's why reasons need testing with handlers before they're shown as fact.",
        "",
        f"**Suspicious is too big ({share['Suspicious']:.0%}).** Real fraud referrals are a small share of claims. The invented rules are blunt; with real data, each customer's fraud team would set them.",
        "",
        "## What this shows, and what it doesn't",
        "",
        "- **Shows:** a suggested pile can come with readable reasons per claim, traced from a classic ML model. That's what to put in front of customers in the bulk sorting sessions.",
        "- **Shows:** missing information and the pre-payment review work as statuses alongside the pile, not as piles.",
        "- **Doesn't show:** accuracy on real claims. The data isn't Keelwater's, half the fields are invented and the labels are rules.",
        "- **Reasons explain the model, not the claim.** Related features share credit (claim amount, car value and amount-to-value overlap), so a handler checks them; they're never the basis for an adverse decision.",
        "- **The rules would do the same job here**, and are easier to explain. On real data, a model earns its place only if it beats the rules on held-out customers.",
    ]
    (HERE / "results.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:30]))


if __name__ == "__main__":
    main()
