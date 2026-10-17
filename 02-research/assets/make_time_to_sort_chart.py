"""Draws the illustrative time-to-sort distribution as SVGs.

Only two points come from the brief: median 11 min, 15% of claims over 4 h.
The curve is a two-group mixture of log-normals fitted to those two points.
It is a hypothesis about the shape, not data.

Writes two charts:
- time-to-sort-distribution.svg: the curve with its three sections
- time-to-sort-causes.svg: the same curve, with every section split by what
  claims are waiting on (invented internal data, internal-data.md §2), and a
  table of shares and claims per year

Run: python3 make_time_to_sort_chart.py  (no dependencies)
"""

from math import erf, exp, log, pi, sqrt
from pathlib import Path

W_SLOW, M_FAST, S_FAST, M_SLOW, S_SLOW = 0.17, 8.5, 1.0, 960.0, 1.2
X_MIN, X_MAX = 0.3, 20160.0
CLAIMS_PER_YEAR = 2_100_000

SECTIONS = [(X_MIN, 11, 0.50, "Within 11 min"), (11, 240, 0.35, "11 min to 4 h"), (240, X_MAX, 0.15, "Over 4 h")]

# Share of claims in each section, by what they're waiting on. [INVENTED], internal-data.md §2
CAUSES = [
    ("Waiting on info from claimant", (0.06, 0.25, 0.48), "#9a3412"),
    ("Third party / fault to work out", (0.08, 0.24, 0.28), "#ea580c"),
    ("Injury involved", (0.02, 0.08, 0.15), "#fdba74"),
    ("Fraud check or referral", (0.01, 0.04, 0.06), "#b91c1c"),
    ("Other", (0.03, 0.04, 0.03), "#a8a29e"),
    ("Straightforward, nothing blocking", (0.80, 0.35, 0.00), "#d0d7de"),
]

WIDTH = 820
LEFT, RIGHT, TOP, BOTTOM = 40, 30, 80, 70


def phi(z):
    return exp(-0.5 * z * z) / sqrt(2 * pi)


def cdf_norm(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def density(x):
    u = log(x)
    return (1 - W_SLOW) * phi((u - log(M_FAST)) / S_FAST) / S_FAST + W_SLOW * phi(
        (u - log(M_SLOW)) / S_SLOW
    ) / S_SLOW


def cdf(x):
    u = log(x)
    return (1 - W_SLOW) * cdf_norm((u - log(M_FAST)) / S_FAST) + W_SLOW * cdf_norm(
        (u - log(M_SLOW)) / S_SLOW
    )


def claims(share):
    n = share * CLAIMS_PER_YEAR
    return f"~{n / 1e6:.2f}M".replace("0M", "M") if n >= 1e6 else f"~{n / 1e3:.0f}k"


xs = [X_MIN * (X_MAX / X_MIN) ** (i / 400) for i in range(401)]
y_max = max(density(x) for x in xs) * 1.3
ticks = [(1, "1 min"), (10, "10 min"), (60, "1 h"), (240, "4 h"), (1440, "1 day"), (10080, "1 week")]


def section_weights(x, width=0.3):
    """Blend the section mixes smoothly across the 11 min and 4 h boundaries."""
    past = [1 / (1 + exp(-(log(x) - log(b)) / width)) for b in (11, 240)]
    return [1 - past[0], past[0] - past[1], past[1]]


def stacked(x, k):
    """Cumulative share of the first k causes at time x."""
    w = section_weights(x)
    return sum(ws * sum(c[1][s] for c in CAUSES[:k]) for s, ws in enumerate(w))


def render(target, title, subtitle, with_causes):
    plot_h = 250
    table_h = 30 + 22 * (len(CAUSES) + 1) + 20 if with_causes else 0
    height = TOP + plot_h + BOTTOM + table_h
    plot_w = WIDTH - LEFT - RIGHT

    def sx(x):
        return LEFT + (log(x) - log(X_MIN)) / (log(X_MAX) - log(X_MIN)) * plot_w

    def sy(y):
        return TOP + plot_h - y / y_max * plot_h

    def band_path(lo, hi, f_lo=lambda x: 0.0, f_hi=lambda x: 1.0):
        pts = [lo] + [x for x in xs if lo <= x <= hi] + [hi]
        top = " ".join(f"L{sx(x):.1f},{sy(density(x) * f_hi(x)):.1f}" for x in pts)
        bottom = " ".join(f"L{sx(x):.1f},{sy(density(x) * f_lo(x)):.1f}" for x in reversed(pts))
        return f"M{sx(lo):.1f},{sy(density(lo) * f_lo(lo)):.1f} {top} {bottom} Z"

    line = "M" + " L".join(f"{sx(x):.1f},{sy(density(x)):.1f}" for x in xs)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" '
        f'font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif" font-size="13">',
        f'<rect width="{WIDTH}" height="{height}" fill="#ffffff"/>',
        f'<text x="{LEFT}" y="30" font-size="17" font-weight="600" fill="#1f2328">{title}</text>',
        f'<text x="{LEFT}" y="52" fill="#59636e">{subtitle}</text>',
    ]

    if with_causes:
        for k in range(len(CAUSES)):
            out.append(
                f'<path d="{band_path(X_MIN, X_MAX, lambda x: stacked(x, k), lambda x: stacked(x, k + 1))}" '
                f'fill="{CAUSES[k][2]}" fill-opacity="0.85"/>'
            )
    else:
        out += [
            f'<path d="{band_path(X_MIN, 11)}" fill="#8c959f" fill-opacity="0.35"/>',
            f'<path d="{band_path(11, 240)}" fill="#8c959f" fill-opacity="0.18"/>',
            f'<path d="{band_path(240, X_MAX)}" fill="#e8590c" fill-opacity="0.35"/>',
        ]

    out += [
        f'<path d="{line}" fill="none" stroke="#1f2328" stroke-width="2"/>',
        f'<line x1="{LEFT}" x2="{WIDTH - RIGHT}" y1="{sy(0):.1f}" y2="{sy(0):.1f}" stroke="#8c959f"/>',
    ]

    for v, label in [(11, "median 11 min"), (240, "4 h")]:
        out.append(
            f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{TOP - 5}" y2="{sy(0):.1f}" '
            'stroke="#59636e" stroke-dasharray="4 4"/>'
        )
        out.append(f'<text x="{sx(v) + 5:.1f}" y="{TOP + 8}" fill="#59636e">{label}</text>')

    if with_causes:
        labels = [(1.6, TOP + 70), (110, TOP + 120), (1800, TOP + 120)]
        for (x, y), (_, _, share, name) in zip(labels, SECTIONS):
            out.append(
                f'<text x="{sx(x):.1f}" y="{y:.1f}" text-anchor="middle" font-size="16" '
                f'font-weight="600" fill="#1f2328">{share:.0%}</text>'
            )
            out.append(
                f'<text x="{sx(x):.1f}" y="{y + 17:.1f}" text-anchor="middle" fill="#59636e">'
                f"{name.lower()}</text>"
            )
            out.append(
                f'<text x="{sx(x):.1f}" y="{y + 33:.1f}" text-anchor="middle" fill="#59636e">'
                f"{claims(share)} claims/yr</text>"
            )
    else:
        for x, lift, share, name in [
            (4.2, 30, 0.50, "sorted within 11 min"),
            (90, 58, 0.35, "11 min to 4 h"),
            (1800, 58, 0.15, "over 4 h"),
        ]:
            y = sy(0) - lift
            out.append(
                f'<text x="{sx(x):.1f}" y="{y - 16:.1f}" text-anchor="middle" font-size="16" '
                f'font-weight="600" fill="#1f2328">{share:.0%}</text>'
            )
            out.append(f'<text x="{sx(x):.1f}" y="{y:.1f}" text-anchor="middle" fill="#59636e">{name}</text>')

    for v, label in ticks:
        out.append(f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{sy(0):.1f}" y2="{sy(0) + 5:.1f}" stroke="#8c959f"/>')
        out.append(f'<text x="{sx(v):.1f}" y="{sy(0) + 22:.1f}" text-anchor="middle" fill="#59636e">{label}</text>')

    out.append(
        f'<text x="{LEFT + plot_w / 2:.1f}" y="{sy(0) + 50:.1f}" text-anchor="middle" fill="#59636e">'
        "time from arrival to sorted (log scale)</text>"
    )

    if with_causes:
        ty = sy(0) + BOTTOM + 20
        cols = [370, 480, 590, 760]
        heads = [s[3] for s in SECTIONS] + ["All claims"]
        out.append(f'<text x="{LEFT}" y="{ty:.1f}" font-weight="600" fill="#1f2328">What claims are waiting on</text>')
        for cx, h in zip(cols, heads):
            out.append(f'<text x="{cx}" y="{ty:.1f}" text-anchor="end" font-weight="600" fill="#1f2328">{h}</text>')
        out.append(f'<line x1="{LEFT}" x2="{WIDTH - RIGHT}" y1="{ty + 8:.1f}" y2="{ty + 8:.1f}" stroke="#d0d7de"/>')
        rows = list(reversed(CAUSES)) + [("Total", (1.0, 1.0, 1.0), None)]
        for r, (name, shares, colour) in enumerate(rows):
            y = ty + 30 + r * 22
            if colour:
                out.append(f'<rect x="{LEFT}" y="{y - 11:.1f}" width="12" height="12" fill="{colour}" fill-opacity="0.85"/>')
            weight = ' font-weight="600"' if colour is None else ""
            out.append(f'<text x="{LEFT + 20}" y="{y:.1f}" fill="#1f2328"{weight}>{name}</text>')
            overall = sum(sh * sec[2] for sh, sec in zip(shares, SECTIONS))
            cells = [(sh, sh * sec[2]) for sh, sec in zip(shares, SECTIONS)] + [(overall, overall)]
            for cx, (pct, of_all) in zip(cols, cells):
                text = f"{pct:.0%} · {claims(of_all)}" if of_all else "—"
                out.append(f'<text x="{cx}" y="{y:.1f}" text-anchor="end" fill="#1f2328"{weight}>{text}</text>')

    out.append("</svg>")
    target.write_text("\n".join(out))
    print(f"wrote {target}")


def main(out_dir=Path(__file__).parent):
    for s in range(len(SECTIONS)):
        assert abs(sum(c[1][s] for c in CAUSES) - 1) < 1e-9, f"section {s} shares don't add to 100%"

    render(
        out_dir / "time-to-sort-distribution.svg",
        "Time to sort: a fast majority and a long tail (illustrative)",
        "Known from the brief: median 11 min, 15% over 4 h. Curve shape is a hypothesis fitted to those two points.",
        with_causes=False,
    )
    render(
        out_dir / "time-to-sort-causes.svg",
        "Time to sort: what claims are waiting on (illustrative)",
        "Brief: 2.1M claims/yr, median 11 min, 15% over 4 h. Curve shape is a hypothesis; causes are [INVENTED].",
        with_causes=True,
    )
    print(f"check: share <= 11 min = {cdf(11):.3f}, share > 4 h = {1 - cdf(240):.3f}")


if __name__ == "__main__":
    main()
