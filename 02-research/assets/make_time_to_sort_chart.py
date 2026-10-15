"""Draws the illustrative time-to-sort distribution as an SVG.

Only two points come from the brief: median 11 min, 15% of claims over 4 h.
The curve is a two-group mixture of log-normals fitted to those two points.
It is a hypothesis about the shape, not data.

Run: python3 make_time_to_sort_chart.py  (no dependencies)
"""

from math import erf, exp, log, pi, sqrt
from pathlib import Path

W_SLOW, M_FAST, S_FAST, M_SLOW, S_SLOW = 0.17, 8.5, 1.0, 960.0, 1.2
X_MIN, X_MAX = 0.3, 20160.0

WIDTH, HEIGHT = 820, 400
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


xs = [X_MIN * (X_MAX / X_MIN) ** (i / 400) for i in range(401)]
y_max = max(density(x) for x in xs) * 1.3
plot_w, plot_h = WIDTH - LEFT - RIGHT, HEIGHT - TOP - BOTTOM


def sx(x):
    return LEFT + (log(x) - log(X_MIN)) / (log(X_MAX) - log(X_MIN)) * plot_w


def sy(y):
    return TOP + plot_h - y / y_max * plot_h


def area_path(lo, hi):
    pts = [x for x in xs if lo <= x <= hi]
    pts = [lo] + pts + [hi]
    d = f"M{sx(lo):.1f},{sy(0):.1f} "
    d += " ".join(f"L{sx(x):.1f},{sy(density(x)):.1f}" for x in pts)
    d += f" L{sx(hi):.1f},{sy(0):.1f} Z"
    return d


line = "M" + " L".join(f"{sx(x):.1f},{sy(density(x)):.1f}" for x in xs)

ticks = [(1, "1 min"), (10, "10 min"), (60, "1 h"), (240, "4 h"), (1440, "1 day"), (10080, "1 week")]

out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
    f'font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif" font-size="13">',
    f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#ffffff"/>',
    f'<text x="{LEFT}" y="30" font-size="17" font-weight="600" fill="#1f2328">'
    "Time to sort: a fast majority and a long tail (illustrative)</text>",
    f'<text x="{LEFT}" y="52" fill="#59636e">'
    "Known from the brief: median 11 min, 15% over 4 h. Curve shape is a hypothesis fitted to those two points.</text>",
    f'<path d="{area_path(X_MIN, 11)}" fill="#8c959f" fill-opacity="0.35"/>',
    f'<path d="{area_path(11, 240)}" fill="#8c959f" fill-opacity="0.18"/>',
    f'<path d="{area_path(240, X_MAX)}" fill="#e8590c" fill-opacity="0.35"/>',
    f'<path d="{line}" fill="none" stroke="#1f2328" stroke-width="2"/>',
    f'<line x1="{LEFT}" x2="{WIDTH - RIGHT}" y1="{sy(0):.1f}" y2="{sy(0):.1f}" stroke="#8c959f"/>',
]

for v, label in [(11, "median 11 min"), (240, "4 h")]:
    out.append(
        f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{TOP - 5}" y2="{sy(0):.1f}" '
        'stroke="#59636e" stroke-dasharray="4 4"/>'
    )
    out.append(f'<text x="{sx(v) + 5:.1f}" y="{TOP + 8}" fill="#59636e">{label}</text>')

for x, lift, share, name in [
    (4.2, 30, "50%", "sorted within 11 min"),
    (90, 58, "35%", "11 min to 4 h"),
    (1800, 58, "15%", "over 4 h"),
]:
    y = sy(0) - lift
    out.append(
        f'<text x="{sx(x):.1f}" y="{y - 16:.1f}" text-anchor="middle" font-size="16" '
        f'font-weight="600" fill="#1f2328">{share}</text>'
    )
    out.append(f'<text x="{sx(x):.1f}" y="{y:.1f}" text-anchor="middle" fill="#59636e">{name}</text>')

for v, label in ticks:
    out.append(f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{sy(0):.1f}" y2="{sy(0) + 5:.1f}" stroke="#8c959f"/>')
    out.append(f'<text x="{sx(v):.1f}" y="{sy(0) + 22:.1f}" text-anchor="middle" fill="#59636e">{label}</text>')

out.append(
    f'<text x="{LEFT + plot_w / 2:.1f}" y="{HEIGHT - 15}" text-anchor="middle" fill="#59636e">'
    "time from arrival to sorted (log scale)</text>"
)
out.append("</svg>")

target = Path(__file__).with_name("time-to-sort-distribution.svg")
target.write_text("\n".join(out))
print(f"wrote {target}")
print(f"check: share <= 11 min = {cdf(11):.3f}, share > 4 h = {1 - cdf(240):.3f}")
