"""Recount merged upstream work and redraw the numbers under each logo.

Run nightly by .github/workflows/nightly.yml. Needs GITHUB_TOKEN (read-only is enough).

What counts:
  * merged pull requests by the user in each org (GitHub search), and
  * commits by the user in google/adk-python, because Google lands outside
    changes through Copybara: the commit lands, the pull request shows closed.

The digits are outlined to paths with a 10-digit subset of Inter (OFL), so the
SVGs need no font at view time and look the same everywhere.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

USER = "Somay-kousis"
ROOT = Path(__file__).resolve().parent.parent
LOGOS = ROOT / "assets" / "logos"
FONT = ROOT / "assets" / "src" / "Inter-digits.ttf"
README = ROOT / "README.md"

# logo file -> (search org, label used in alt text and aria-label)
ORGS = {
    "nvidia": ("NVIDIA", "NVIDIA"),
    "microsoft": ("microsoft", "Microsoft"),
    "intel": ("openvinotoolkit", "Intel OpenVINO"),
    "krkn": ("krkn-chaos", "CNCF krkn"),
    "llm4s": ("llm4s", "LLM4S"),
}

COUNT_FILL = "#8b949e"
CENTER_X = 52.0     # logos are 104 wide
BASELINE = 88.0
CAP_HEIGHT = 14.6   # height of a digit in px, matches the original art


def _get(url: str) -> object:
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "User-Agent": f"{USER}-profile-counts",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def merged_prs(org: str) -> int:
    q = f"is:pr is:merged author:{USER} org:{org}"
    data = _get("https://api.github.com/search/issues?" + urllib.parse.urlencode({"q": q, "per_page": 1}))
    return int(data["total_count"])


def adk_commits() -> int:
    n, page = 0, 1
    while True:
        batch = _get(f"https://api.github.com/repos/google/adk-python/commits?author={USER}&per_page=100&page={page}")
        n += len(batch)
        if len(batch) < 100:
            return n
        page += 1


def outline(text: str) -> str:
    """SVG path data for `text`, centred on CENTER_X with its baseline on BASELINE."""
    font = TTFont(FONT)
    cmap, gs = font.getBestCmap(), font.getGlyphSet()
    upm = font["head"].unitsPerEm
    cap = font["OS/2"].sCapHeight or 0.727 * upm
    scale = CAP_HEIGHT / cap
    width = sum(gs[cmap[ord(c)]].width for c in text) * scale
    x = CENTER_X - width / 2
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    for c in text:
        g = gs[cmap[ord(c)]]
        g.draw(TransformPen(pen, (scale, 0, 0, -scale, x, BASELINE)))
        x += g.width * scale
    return pen.getCommands()


def redraw(name: str, label: str, count: int) -> bool:
    path = LOGOS / f"{name}.svg"
    svg = path.read_text()
    new_digits = f'<path d="{outline(str(count))}" fill="{COUNT_FILL}"/>'
    # The count is always the last path, the only one filled with COUNT_FILL.
    svg2, n = re.subn(rf'<path d="[^"]*" fill="{COUNT_FILL}"/>(?!.*<path)', new_digits, svg, flags=re.S)
    if n != 1:
        sys.exit(f"{name}.svg: expected one count path, found {n}")
    svg2 = re.sub(r'aria-label="[^"]*"', f'aria-label="{label} {count} merged"', svg2, count=1)
    if svg2 != svg:
        path.write_text(svg2)
        return True
    return False


def update_readme(counts: dict[str, int], total: int) -> bool:
    text = README.read_text()
    new = re.sub(r"(<!-- total:start -->).*?(<!-- total:end -->)", rf"\g<1>{total}\g<2>", text, flags=re.S)
    for name, (_, label) in {**ORGS, "google": ("", "Google")}.items():
        new = re.sub(rf'alt="{re.escape(label)} \d+ merged"', f'alt="{label} {counts[name]} merged"', new)
    if new != text:
        README.write_text(new)
        return True
    return False


def main() -> None:
    counts = {name: merged_prs(org) for name, (org, _) in ORGS.items()}
    counts["google"] = adk_commits()
    total = sum(counts.values())
    changed = [n for n, (_, label) in {**ORGS, "google": ("", "Google")}.items() if redraw(n, label, counts[n])]
    readme = update_readme(counts, total)
    print(json.dumps({"counts": counts, "total": total, "logos_changed": changed, "readme_changed": readme}))


if __name__ == "__main__":
    main()
