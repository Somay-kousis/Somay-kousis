"""Pixel pets on the contribution grid.

Draws a GitHub user's contribution calendar as an animated SVG: three small pixel critters walk the
grid in lanes and eat the squares they cross, and the squares grow back behind them.
Standard library only.

    GITHUB_TOKEN=... python3 pets/generate.py Somay-kousis dist
"""

import datetime
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

CELL, GAP = 11, 3
PITCH = CELL + GAP
PX = 2                     # one sprite pixel = 2 SVG units
LOOP = 26.0                # seconds for one full pass and reset
WALK = 19.0                # seconds the critters spend walking
TOP, SIDE, BOTTOM = 26, 14, 12

PALETTES = {
    # Warm yellows, the accent colour of the profile's pixel art.
    "dark": ["#161b22", "#3d3314", "#7a6113", "#d4a514", "#ffd21f"],
    "light": ["#ebedf0", "#fbe9a6", "#f5cf4a", "#dba60f", "#94690a"],
}

# Original sprites (front-facing, so they never need flipping). k = outline.
SPRITES = {
    "cat": {
        "art": [
            ".k........k.",
            ".kk......kk.",
            ".kgkkkkkkgk.",
            "kggggggggggk",
            "kgkggggggkgk",
            "kggggnnggggk",
            ".kggggggggk.",
            ".kggggggggk.",
            "..kk....kk..",
        ],
        "colors": {"k": "#1b1f24", "g": "#9aa4ad", "n": "#f08aa8"},
    },
    "ghost": {
        "art": [
            "..kkkkkk..",
            ".kwwwwwwk.",
            "kwwwwwwwwk",
            "kwwkwwkwwk",
            "kwwkwwkwwk",
            "kwcwwwwcwk",
            "kwwwwwwwwk",
            "kwwwkkwwwk",
            ".kkk..kkk.",
        ],
        "colors": {"k": "#241a45", "w": "#e9e3ff", "c": "#ff9cc8"},
    },
    "axolotl": {
        "art": [
            "r..........r",
            ".r.kkkkkk.r.",
            "rrkppppppkrr",
            ".kppppppppk.",
            "rkpkppppkpkr",
            ".kppppppppk.",
            ".kpppkkpppk.",
            "..kppppppk..",
            "..kk....kk..",
        ],
        "colors": {"k": "#3a1430", "p": "#ffb3c9", "r": "#ff5d8f"},
    },
}

# Which rows each critter grazes (every row belongs to exactly one critter).
LANES = [("ghost", [0, 1]), ("cat", [2, 3, 4]), ("axolotl", [5, 6])]


def fetch_levels(user: str) -> list[dict[int, int]]:
    """One {weekday: level 0-4} per week, oldest week first (the first and last weeks are partial)."""
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        try:
            return fetch_levels_graphql(user, token)
        except Exception as e:     # an Actions token without user scope, rate limit, outage: read the page instead
            print(f"GraphQL failed ({e}); reading the public calendar page", file=sys.stderr)
    return fetch_levels_page(user)


def fetch_levels_graphql(user: str, token: str) -> list[dict[int, int]]:
    query = """query($login: String!) { user(login: $login) { contributionsCollection {
        contributionCalendar { weeks { contributionDays { weekday contributionLevel } } } } } }"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": user}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    rank = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [{d["weekday"]: rank[d["contributionLevel"]] for d in w["contributionDays"]} for w in weeks]


def fetch_levels_page(user: str) -> list[dict[int, int]]:
    html = urllib.request.urlopen(f"https://github.com/users/{user}/contributions", timeout=30).read().decode()
    cells = re.findall(r'data-date="(\d{4}-\d\d-\d\d)"[^>]*?data-level="(\d)"', html)
    cells += [(d, l) for l, d in re.findall(r'data-level="(\d)"[^>]*?data-date="(\d{4}-\d\d-\d\d)"', html)]
    days = sorted(set(cells))
    if not days:
        raise RuntimeError("could not read the contribution calendar")
    weeks: list[dict[int, int]] = []
    for date, level in days:
        weekday = (datetime.date.fromisoformat(date).weekday() + 1) % 7    # Sunday = 0, like GitHub
        if not weeks or weekday == 0:
            weeks.append({})
        weeks[-1][weekday] = int(level)
    return weeks


def sprite_svg(name: str) -> str:
    s = SPRITES[name]
    rects = []
    for y, row in enumerate(s["art"]):
        for x, ch in enumerate(row):
            if ch != ".":
                rects.append(f'<rect x="{x * PX}" y="{y * PX}" width="{PX}" height="{PX}" fill="{s["colors"][ch]}"/>')
    return f'<g id="{name}" shape-rendering="crispEdges">{"".join(rects)}</g>'


def render(weeks: list[dict[int, int]], palette: list[str]) -> str:
    cols = len(weeks)
    width = SIDE * 2 + cols * PITCH - GAP
    height = TOP + 7 * PITCH - GAP + BOTTOM
    css, cells, critters = [], [], []

    for level in range(1, 5):
        # A square is eaten at 0%, stays bare, then grows back.
        css.append(
            f"@keyframes eat{level}{{0%{{fill:{palette[0]}}}55%{{fill:{palette[0]}}}"
            f"70%{{fill:{palette[level]}}}100%{{fill:{palette[level]}}}}}"
        )

    eaten_at: dict[tuple[int, int], float] = {}
    for idx, (name, rows) in enumerate(LANES):
        # Serpentine path over the lane: one row left to right, the next right to left.
        path = []
        for i, r in enumerate(rows):
            order = range(cols) if i % 2 == 0 else range(cols - 1, -1, -1)
            path += [(c, r) for c in order]
        step = WALK / len(path)
        for n, cell in enumerate(path):
            eaten_at[cell] = n * step

        art = SPRITES[name]["art"]
        w, h = len(art[0]) * PX, len(art) * PX

        def where(c: int, r: int) -> tuple[float, float]:
            x = SIDE + c * PITCH + CELL / 2 - w / 2
            y = TOP + r * PITCH + CELL - h + 2          # feet resting on the square
            return round(x, 1), round(y, 1)

        frames = []
        for n, (c, r) in enumerate(path):
            if n in (0, len(path) - 1) or path[n - 1][1] != r or path[n + 1][1] != r:
                x, y = where(c, r)
                frames.append(f"{n * step / LOOP * 100:.3f}%{{transform:translate({x}px,{y}px)}}")
        lx, ly = where(*path[-1])
        fx, fy = where(*path[0])
        frames.append(f"{WALK / LOOP * 100:.3f}%{{transform:translate({lx}px,{ly}px)}}")
        frames.append(f"{WALK / LOOP * 100 + 0.01:.3f}%{{transform:translate({fx}px,{fy}px)}}")
        frames.append(f"100%{{transform:translate({fx}px,{fy}px)}}")
        css.append(f"@keyframes walk{idx}{{{''.join(frames)}}}")
        fade = WALK / LOOP * 100
        css.append(
            f"@keyframes show{idx}{{0%{{opacity:1}}{fade - 2:.2f}%{{opacity:1}}{fade:.2f}%{{opacity:0}}"
            f"{100 - 2:.2f}%{{opacity:0}}100%{{opacity:1}}}}"
        )
        css.append(f".c{idx}{{animation:walk{idx} {LOOP}s linear infinite,show{idx} {LOOP}s linear infinite}}")
        critters.append(
            f'<g class="c{idx}"><g class="bob" style="animation-delay:-{idx * 0.13:.2f}s">'
            f'<use href="#{name}"/></g></g>'
        )

    css.append("@keyframes bob{0%,49%{transform:translateY(0)}50%,100%{transform:translateY(-2px)}}")
    css.append(".bob{animation:bob .36s linear infinite}")
    css.append("@media (prefers-reduced-motion: reduce){*{animation:none!important}}")

    for c, week in enumerate(weeks):
        for r, level in sorted(week.items()):
            x, y = SIDE + c * PITCH, TOP + r * PITCH
            style = ""
            if level and (c, r) in eaten_at:
                style = f' style="animation:eat{level} {LOOP}s linear {eaten_at[(c, r)]:.2f}s infinite"'
            cells.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{palette[level]}"{style}/>')

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-label="Contribution grid with pixel pets eating the squares">'
        f'<defs>{"".join(sprite_svg(n) for n in SPRITES)}<style>{"".join(css)}</style></defs>'
        f'{"".join(cells)}{"".join(critters)}</svg>'
    )


def main() -> None:
    user = sys.argv[1] if len(sys.argv) > 1 else "Somay-kousis"
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "dist")
    out.mkdir(parents=True, exist_ok=True)
    weeks = fetch_levels(user)
    for name, palette in PALETTES.items():
        (out / f"pixel-pets-{name}.svg").write_text(render(weeks, palette))
    print(f"{len(weeks)} weeks, {sum(1 for w in weeks for l in w.values() if l)} active days -> {out}")


if __name__ == "__main__":
    main()
