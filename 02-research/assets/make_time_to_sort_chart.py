"""Draws the illustrative time-to-sort distribution as SVGs.

Only two points come from the brief: median 11 min, 15% of claims over 4 h.
The curve is a two-group mixture of log-normals fitted to those two points.
It is a hypothesis about the shape, not data.

Writes two charts:
- time-to-sort-distribution.svg: the curve with its three sections
- time-to-sort-causes.svg: the same curve, with the >4h tail split by cause
  (invented internal data, internal-data.md §2) and claim counts per year

Run: python3 make_time_to_sort_chart.py  (no dependencies)
"""

from math import erf, exp, log, pi, sqrt
from pathlib import Path

W_SLOW, M_FAST, S_FAST, M_SLOW, S_SLOW = 0.17, 8.5, 1.0, 960.0, 1.2
X_MIN, X_MAX = 0.3, 20160.0
CLAIMS_PER_YEAR = 2_100_000

CAUSES = [
    ("Waiting on info from claimant", 0.48, "#9a3412"),
    ("Third party / fault to work out", 0.28, "#ea580c"),
    ("Injury involved", 0.15, "#fdba74"),
    ("Fraud check or referral", 0.06, "#b91c1c"),
    ("Other", 0.03, "#a8a29e"),
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


def render(target, height, title, subtitle, with_causes):
    plot_w, plot_h = WIDTH - LEFT - RIGHT, height - TOP - BOTTOM

    def sx(x):
        return LEFT + (log(x) - log(X_MIN)) / (log(X_MAX) - log(X_MIN)) * plot_w

    def sy(y):
        return TOP + plot_h - y / y_max * plot_h

    def band_path(lo, hi, f_lo=0.0, f_hi=1.0):
        pts = [lo] + [x for x in xs if lo <= x <= hi] + [hi]
        top = " ".join(f"L{sx(x):.1f},{sy(density(x) * f_hi):.1f}" for x in pts)
        bottom = " ".join(f"L{sx(x):.1f},{sy(density(x) * f_lo):.1f}" for x in reversed(pts))
        return f"M{sx(lo):.1f},{sy(density(lo) * f_lo):.1f} {top} {bottom} Z"

    line = "M" + " L".join(f"{sx(x):.1f},{sy(density(x)):.1f}" for x in xs)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" '
        f'font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif" font-size="13">',
        f'<rect width="{WIDTH}" height="{height}" fill="#ffffff"/>',
        f'<text x="{LEFT}" y="30" font-size="17" font-weight="600" fill="#1f2328">{title}</text>',
        f'<text x="{LEFT}" y="52" fill="#59636e">{subtitle}</text>',
        f'<path d="{band_path(X_MIN, 11)}" fill="#8c959f" fill-opacity="0.35"/>',
        f'<path d="{band_path(11, 240)}" fill="#8c959f" fill-opacity="0.18"/>',
    ]

    if with_causes:
        cum = 0.0
        for _, share, colour in CAUSES:
            out.append(f'<path d="{band_path(240, X_MAX, cum, cum + share)}" fill="{colour}" fill-opacity="0.85"/>')
            cum += share
    else:
        out.append(f'<path d="{band_path(240, X_MAX)}" fill="#e8590c" fill-opacity="0.35"/>')

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

    extra = 18 if with_causes else 0
    sections = [(4.2, 30 + extra, 0.50, "sorted within 11 min"), (90, 58 + extra, 0.35, "11 min to 4 h")]
    if not with_causes:
        sections.append((1800, 58, 0.15, "over 4 h"))
    for x, lift, share, name in sections:
        y = sy(0) - lift
        out.append(
            f'<text x="{sx(x):.1f}" y="{y - 16:.1f}" text-anchor="middle" font-size="16" '
            f'font-weight="600" fill="#1f2328">{share:.0%}</text>'
        )
        out.append(f'<text x="{sx(x):.1f}" y="{y:.1f}" text-anchor="middle" fill="#59636e">{name}</text>')
        if with_causes:
            out.append(
                f'<text x="{sx(x):.1f}" y="{y + 16:.1f}" text-anchor="middle" fill="#59636e">'
                f"{claims(share)} claims/yr</text>"
            )

    if with_causes:
        lx, ly = sx(240) + 18, TOP + 34
        out.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="16" font-weight="600" fill="#1f2328">'
            f"15% over 4 h: {claims(0.15)} claims/yr</text>"
        )
        out.append(f'<text x="{lx:.1f}" y="{ly + 18:.1f}" fill="#59636e">why they take longer (share of the slow tail)</text>')
        for i, (name, share, colour) in enumerate(reversed(CAUSES)):
            y = ly + 44 + i * 22
            out.append(f'<rect x="{lx:.1f}" y="{y - 11:.1f}" width="12" height="12" fill="{colour}" fill-opacity="0.85"/>')
            out.append(
                f'<text x="{lx + 20:.1f}" y="{y:.1f}" fill="#1f2328"><tspan font-weight="600">{share:.0%}</tspan> '
                f'{name} <tspan fill="#59636e">{claims(0.15 * share)}</tspan></text>'
            )

    for v, label in ticks:
        out.append(f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{sy(0):.1f}" y2="{sy(0) + 5:.1f}" stroke="#8c959f"/>')
        out.append(f'<text x="{sx(v):.1f}" y="{sy(0) + 22:.1f}" text-anchor="middle" fill="#59636e">{label}</text>')

    out.append(
        f'<text x="{LEFT + plot_w / 2:.1f}" y="{height - 15}" text-anchor="middle" fill="#59636e">'
        "time from arrival to sorted (log scale)</text>"
    )
    out.append("</svg>")
    target.write_text("\n".join(out))
    print(f"wrote {target}")


here = Path(__file__).parent
render(
    here / "time-to-sort-distribution.svg",
    400,
    "Time to sort: a fast majority and a long tail (illustrative)",
    "Known from the brief: median 11 min, 15% over 4 h. Curve shape is a hypothesis fitted to those two points.",
    with_causes=False,
)
render(
    here / "time-to-sort-causes.svg",
    460,
    "Time to sort: what keeps the slow 15% waiting (illustrative)",
    "Brief: 2.1M claims/yr, median 11 min, 15% over 4 h. Curve shape is a hypothesis; causes are [INVENTED].",
    with_causes=True,
)
print(f"check: share <= 11 min = {cdf(11):.3f}, share > 4 h = {1 - cdf(240):.3f}")
