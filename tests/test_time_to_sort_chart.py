"""Tests for 02-research/assets/make_time_to_sort_chart.py."""

import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from helpers import load_script

chart = load_script("time_to_sort_chart", "02-research/assets/make_time_to_sort_chart.py")

OVER_4H = 2


def share_of_all(cause_name):
    shares = next(c[1] for c in chart.CAUSES if c[0] == cause_name)
    return sum(sh * sec[2] for sh, sec in zip(shares, chart.SECTIONS))


class CurveMatchesTheBrief(unittest.TestCase):
    def test_median_is_11_minutes(self):
        self.assertAlmostEqual(chart.cdf(11), 0.50, delta=0.01)

    def test_15_percent_take_over_4_hours(self):
        self.assertAlmostEqual(1 - chart.cdf(240), 0.15, delta=0.01)

    def test_section_shares_match_the_curve(self):
        self.assertEqual([s[2] for s in chart.SECTIONS], [0.50, 0.35, 0.15])


class CausesMatchInternalData(unittest.TestCase):
    """The invented causes agreed in internal-data.md §2."""

    def test_each_section_adds_to_100_percent(self):
        for s in range(len(chart.SECTIONS)):
            self.assertAlmostEqual(sum(c[1][s] for c in chart.CAUSES), 1.0, places=9)

    def test_over_4h_causes(self):
        over_4h = {name: shares[OVER_4H] for name, shares, _ in chart.CAUSES}
        self.assertEqual(
            over_4h,
            {
                "Waiting on info from claimant": 0.48,
                "Third party / fault to work out": 0.28,
                "Injury involved": 0.15,
                "Fraud check or referral": 0.06,
                "Other": 0.03,
                "Straightforward, nothing blocking": 0.00,
            },
        )

    def test_authority_limit_is_not_a_cause(self):
        self.assertFalse(any("authority" in c[0].lower() for c in chart.CAUSES))

    def test_about_52_percent_of_all_claims_are_straightforward(self):
        self.assertAlmostEqual(share_of_all("Straightforward, nothing blocking"), 0.52, delta=0.005)

    def test_about_398k_claims_a_year_wait_on_info(self):
        claims = share_of_all("Waiting on info from claimant") * chart.CLAIMS_PER_YEAR
        self.assertAlmostEqual(claims, 398_000, delta=1_000)


class Blending(unittest.TestCase):
    def test_section_weights_add_to_one(self):
        for x in [0.5, 5, 11, 60, 240, 1000, 10000]:
            self.assertAlmostEqual(sum(chart.section_weights(x)), 1.0, places=9)

    def test_all_causes_stack_to_the_full_curve(self):
        for x in [1, 11, 240, 5000]:
            self.assertAlmostEqual(chart.stacked(x, len(chart.CAUSES)), 1.0, places=9)

    def test_far_from_boundaries_the_section_mix_is_used(self):
        self.assertAlmostEqual(chart.section_weights(1)[0], 1.0, places=2)
        self.assertAlmostEqual(chart.section_weights(10000)[2], 1.0, places=2)


class Labels(unittest.TestCase):
    def test_claims_per_year_formatting(self):
        self.assertEqual(chart.claims(0.15), "~315k")
        self.assertEqual(chart.claims(0.50), "~1.05M")


class Rendering(unittest.TestCase):
    def test_writes_two_valid_svgs(self):
        with tempfile.TemporaryDirectory() as tmp:
            chart.main(Path(tmp))
            dist = ET.parse(Path(tmp) / "time-to-sort-distribution.svg").getroot()
            causes = ET.parse(Path(tmp) / "time-to-sort-causes.svg").getroot()
        texts = lambda root: " ".join(t.text or "" for t in root.iter("{http://www.w3.org/2000/svg}text"))
        self.assertIn("median 11 min", texts(dist))
        self.assertIn("[INVENTED]", texts(causes))
        for name, _, _ in chart.CAUSES:
            self.assertIn(name, texts(causes))
        self.assertIn("Total", texts(causes))


if __name__ == "__main__":
    unittest.main()
