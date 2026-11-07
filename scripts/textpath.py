"""Outline text to SVG path data with a subset of Inter (OFL, assets/src/OFL.txt).

GitHub serves README images through a proxy as <img>, so an SVG can't load web
fonts. Outlining the text keeps it looking the same for every viewer.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

SRC = Path(__file__).resolve().parent.parent / "assets" / "src"


@lru_cache(maxsize=None)
def _font(weight: int) -> TTFont:
    return TTFont(SRC / f"Inter-{weight}.ttf")


def width(text: str, size: float, weight: int = 400) -> float:
    f = _font(weight)
    cmap, gs = f.getBestCmap(), f.getGlyphSet()
    scale = size / f["head"].unitsPerEm
    return sum(gs[cmap.get(ord(c), cmap[ord("?")])].width for c in text) * scale


def path(text: str, x: float, y: float, size: float, weight: int = 400, anchor: str = "start") -> str:
    """Path data for `text` with its baseline at y. anchor: start, middle or end."""
    f = _font(weight)
    cmap, gs = f.getBestCmap(), f.getGlyphSet()
    scale = size / f["head"].unitsPerEm
    if anchor != "start":
        w = width(text, size, weight)
        x -= w / 2 if anchor == "middle" else w
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    for c in text:
        g = gs[cmap.get(ord(c), cmap[ord("?")])]
        g.draw(TransformPen(pen, (scale, 0, 0, -scale, x, y)))
        x += g.width * scale
    return pen.getCommands()


def fit(text: str, max_width: float, size: float, weight: int = 400) -> str:
    """Cut `text` with an ellipsis-free trim so it fits max_width."""
    while text and width(text, size, weight) > max_width:
        text = text[:-1]
    return text.rstrip()
