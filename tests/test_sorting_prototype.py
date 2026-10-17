"""Tests for 04-working-material/prototype/sorting_prototype.py (the sample-data model)."""

import unittest
from types import SimpleNamespace

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

from helpers import load_script

proto = load_script("sorting_prototype", "04-working-material/prototype/sorting_prototype.py")


def claim(**overrides):
    """A plain collision claim that passes every check, with fields overridden."""
    fields = dict(
        claim_type="collision", claim_amount=1_500, car_value=10_000, amount_to_car_value=0.15, car_age=5,
        commercial_use=0, prior_claims=0, prior_claims_value=0, licence_revoked=0, record_points=0,
        days_since_policy_start=400, third_party=0, injury=0, has_photos=1, has_police_report=1,
    )
    fields.update(overrides)
    return SimpleNamespace(**fields)


class RuleLabels(unittest.TestCase):
    def test_plain_claim_is_simple(self):
        self.assertEqual(proto.rule_label(claim()), "Simple")

    def test_suspicious_signals(self):
        for overrides in [
            dict(claim_type="theft"),
            dict(days_since_policy_start=30),
            dict(prior_claims=4),
            dict(licence_revoked=1, record_points=7),
            dict(amount_to_car_value=1.6),
        ]:
            with self.subTest(**overrides):
                self.assertEqual(proto.rule_label(claim(**overrides)), "Suspicious")

    def test_high_amount_to_value_with_third_party_is_not_suspicious(self):
        self.assertEqual(proto.rule_label(claim(amount_to_car_value=1.6, third_party=1)), "Needs a closer look")

    def test_closer_look_signals(self):
        for overrides in [
            dict(third_party=1),
            dict(injury=1),
            dict(claim_amount=proto.SIMPLE_MAX_AMOUNT + 1),
            dict(amount_to_car_value=0.71),
        ]:
            with self.subTest(**overrides):
                self.assertEqual(proto.rule_label(claim(**overrides)), "Needs a closer look")

    def test_authority_limit_does_not_change_the_pile(self):
        """A-20: authority limits apply at payment, not sorting."""
        amount = (proto.AUTHORITY_LIMIT + proto.SIMPLE_MAX_AMOUNT) / 2
        self.assertEqual(proto.rule_label(claim(claim_amount=amount)), "Simple")

    def test_missing_info_is_never_a_pile(self):
        """A-19: missing information is a status."""
        self.assertEqual(proto.PILES, ["Simple", "Needs a closer look", "Suspicious"])


class MissingInfo(unittest.TestCase):
    def test_nothing_missing(self):
        self.assertEqual(proto.missing_info(claim()), "")

    def test_no_photos(self):
        self.assertEqual(proto.missing_info(claim(has_photos=0)), "photos")

    def test_police_report_needed_for_theft_third_party_or_injury(self):
        for overrides in [dict(claim_type="theft"), dict(third_party=1), dict(injury=1)]:
            with self.subTest(**overrides):
                self.assertEqual(proto.missing_info(claim(has_police_report=0, **overrides)), "police report")

    def test_police_report_not_needed_for_plain_collision(self):
        self.assertEqual(proto.missing_info(claim(has_police_report=0)), "")


def tiny_claims(n=300, seed=0):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame([vars(claim()) for _ in range(n)])
    df["claim_type"] = rng.choice(["collision", "windscreen", "theft", "vandalism"], n)
    df["claim_amount"] = rng.integers(200, 9_000, n)
    df["prior_claims"] = rng.integers(0, 5, n)
    df["third_party"] = rng.integers(0, 2, n)
    df["days_since_policy_start"] = rng.integers(1, 900, n)
    df["amount_to_car_value"] = df.claim_amount / df.car_value
    return df


class ReasonsFromTheModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        df = tiny_claims()
        cls.X = proto.features(df)
        y = df.apply(proto.rule_label, axis=1).map({p: i for i, p in enumerate(proto.PILES)})
        cls.model = GradientBoostingClassifier(n_estimators=20, max_depth=3, random_state=0).fit(cls.X, y)

    def test_every_feature_has_a_readable_reason(self):
        for j, col in enumerate(self.X.columns):
            with self.subTest(feature=col):
                self.assertIsInstance(proto.reason(col, float(self.X.iloc[0, j]), 1.0), str)

    def test_contributions_explain_the_score_exactly(self):
        """Score minus the summed contributions is the same constant for every claim."""
        scores = self.model.decision_function(self.X)
        for k in range(len(proto.PILES)):
            rest = [
                scores[i, k] - proto.path_contributions(self.model, self.X.iloc[i].to_numpy(dtype=float), k).sum()
                for i in range(len(self.X))
            ]
            self.assertAlmostEqual(float(np.ptp(rest)), 0.0, places=9)

    def test_top_reasons_are_at_most_three(self):
        reasons = proto.top_reasons(self.model, self.X, 0, 0)
        self.assertLessEqual(len(reasons), 3)


class KaggleData(unittest.TestCase):
    def test_loads_the_claims_that_were_filed(self):
        df = proto.load_claims()
        self.assertEqual(len(df), 2_746)
        self.assertFalse(df.claim_amount.isna().any())

    def test_no_demographic_fields(self):
        """kaggle-claim-prediction-review.md §4."""
        cols = set(proto.load_claims().columns)
        self.assertFalse(cols & {"AGE", "GENDER", "MSTATUS", "EDUCATION", "INCOME", "KIDSDRIV", "URBANICITY"})


if __name__ == "__main__":
    unittest.main()
