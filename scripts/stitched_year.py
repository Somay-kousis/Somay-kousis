"""Draw assets/stitched-year.svg from the live contribution calendar.

Hornet stands in the middle of the year. Every day with contributions gets one
red stitch (longer and thicker on busier days), days without get a faint dot,
and a thread runs through the stitches in date order, passing behind her.

Run nightly by .github/workflows/nightly.yml. Needs GITHUB_TOKEN.
Deterministic: the same calendar always gives the same file, so the nightly job
only commits when a day actually changed.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
import os
import urllib.request
from datetime import date
from pathlib import Path

USER = "Somay-kousis"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "stitched-year.svg"
HORNET = ROOT / "assets" / "src" / "hornet.png"
SHADOW = ROOT / "assets" / "src" / "shadow.png"

W, H = 920, 310
PITCH = 12.35
LEFT_X0 = 14.0
RIGHT_X_END = 906.0
LEFT_WEEKS = 26          # the rest of the year goes right of Hornet
ROW_Y0, ROW_STEP = 88, 21
RED = "#d3202f"

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
  weeks{contributionDays{date weekday contributionCount}}}}}}"""

STYLE = (
    ".s{animation:a 9s ease-in-out infinite}"
    "@keyframes a{0%,7%,100%{opacity:1}3%{opacity:.35}}"
    ".h{animation:h 5.4s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 100%}"
    "@keyframes h{0%,100%{transform:rotate(-1.2deg)}50%{transform:rotate(1.2deg)}}"
    "@media (prefers-reduced-motion: reduce){.s,.h{animation:none;opacity:1}}"
)


def fetch_weeks() -> list[list[dict]]:
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "Content-Type": "application/json",
        "User-Agent": f"{USER}-stitched-year",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [w["contributionDays"] for w in weeks]


def _jitter(key: str, lo: float, hi: float) -> float:
    """Stable pseudo-random number in [lo, hi) for a given key."""
    h = int.from_bytes(hashlib.sha256(key.encode()).digest()[:4], "big") / 2**32
    return lo + (hi - lo) * h


def column_x(i: int, n: int) -> float:
    if i < LEFT_WEEKS:
        return LEFT_X0 + PITCH * i
    right = n - LEFT_WEEKS
    return RIGHT_X_END - PITCH * (right - 1 - (i - LEFT_WEEKS))


def f1(v: float) -> str:
    return f"{v:.1f}"


def render(weeks: list[list[dict]], today: date | None = None) -> str:
    today = today or date.today()
    n = len(weeks)
    peak = max((d["contributionCount"] for w in weeks for d in w), default=0) or 1
    dots, groups, points = [], [], []
    for i, days in enumerate(weeks):
        x = column_x(i, n)
        stitches = []
        for d in days:
            if date.fromisoformat(d["date"]) > today:
                continue
            y = ROW_Y0 + ROW_STEP * d["weekday"]
            c = d["contributionCount"]
            if c == 0:
                dots.append(f'<circle cx="{f1(x)}" cy="{y}" r="1.1" fill="#5b6577" opacity=".55"/>')
                continue
            frac = math.log1p(c) / math.log1p(peak)
            half = 2.9 + 6.7 * frac
            dy = min(9.0, max(4.5, half * _jitter(d["date"] + "r", 0.95, 1.45)))
            cx = x + _jitter(d["date"] + "x", -1.6, 1.6)
            width = 1.9 + 1.2 * frac
            stitches.append(
                f'<path d="M{f1(cx - half)} {f1(y + dy)}L{f1(cx + half)} {f1(y - dy)}" '
                f'stroke="{RED}" stroke-width="{f1(width)}" stroke-linecap="round"/>'
            )
            points.append((x, y))
        if stitches:
            groups.append(f'<g class="s" style="animation-delay:{0.08 * i:.2f}s">{"".join(stitches)}</g>')

    thread = ""
    if len(points) > 1:
        seg = [f"M{f1(points[0][0])} {f1(points[0][1])}"]
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            dx = x1 - x0
            if dx > 3 * PITCH:
                # A long span hangs: the thread sags below both ends, like real
                # thread pulled across a gap (and behind Hornet's cloak).
                low = min(max(y0, y1) + min(70.0, dx * 0.18), 250.0)
                seg.append(f"C{f1(x0 + dx / 3)} {f1(low)} {f1(x1 - dx / 3)} {f1(low)} {f1(x1)} {f1(y1)}")
            else:
                xm = (x0 + x1) / 2
                seg.append(f"C{f1(xm)} {f1(y0 - 9)} {f1(xm)} {f1(y1 + 9)} {f1(x1)} {f1(y1)}")
        thread = f'<path d="{"".join(seg)}" fill="none" stroke="{RED}" stroke-width="1.1" opacity=".75"/>'

    def png(p: Path) -> str:
        return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        'aria-label="Hornet holds a red thread stitched through my contribution year, '
        'one stitch for each day I contributed.">'
        f"<style>{STYLE}</style>"
        + "".join(dots) + thread + "".join(groups)
        + f'<image x="358" y="267" width="203" height="29" href="{png(SHADOW)}"/>'
        + f'<image class="h" x="353" y="8" width="213" height="289" href="{png(HORNET)}"/>'
        + "</svg>"
    )


def main() -> None:
    svg = render(fetch_weeks())
    if not OUT.exists() or OUT.read_text() != svg:
        OUT.write_text(svg)
        print("stitched-year.svg updated")
    else:
        print("stitched-year.svg unchanged")


if __name__ == "__main__":
    main()
