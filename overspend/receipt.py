"""Draw assets/overspend-receipt.svg: the latest overspend attempt as a paper receipt.

Paid lines print normally. Blocked and refused lines are struck through in red,
with Pocket Change's reason under them. All text is outlined (scripts/textpath.py).
Everything drawn comes from data/overspend.json, whose strings are either our own
reason sentences or values that already passed judge.py's strict patterns.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import textpath as T  # noqa: E402

OUT = ROOT / "assets" / "overspend-receipt.svg"
W = 340
PAD = 22
INK, MUTED, RED, PAPER = "#1f2328", "#6e7781", "#d3202f", "#f6f3ec"
LOGIN_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", re.ASCII)


def _wrap(text: str, max_width: float, size: float) -> list[str]:
    """Break on spaces so no reason gets cut mid-word or mid-number."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and T.width(trial, size) > max_width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(T.fit(cur, max_width, size))
    return lines


def _rupees(paise: int) -> str:
    return f"₹{paise / 100:,.0f}"


class _Canvas:
    def __init__(self) -> None:
        self.parts: list[str] = []
        self.y = 0.0

    def text(self, s: str, x: float, size: float, fill: str, weight: int = 400, anchor: str = "start") -> None:
        self.parts.append(f'<path d="{T.path(s, x, self.y, size, weight, anchor)}" fill="{fill}"/>')

    def dashes(self) -> None:
        self.parts.append(f'<path d="M{PAD} {self.y:.1f}H{W - PAD}" stroke="{MUTED}" '
                          'stroke-width="1" stroke-dasharray="3 4" opacity=".6"/>')

    def strike(self, x0: float, x1: float, y: float) -> None:
        self.parts.append(f'<path d="M{x0:.1f} {y:.1f}H{x1:.1f}" stroke="{RED}" stroke-width="1.6" stroke-linecap="round"/>')


def render(d: dict) -> str:
    c = _Canvas()
    last = d.get("last")
    c.y = 40
    c.text("Pocket Change", W / 2, 17, INK, 600, "middle")
    c.y += 20
    if last and LOGIN_RE.fullmatch(last.get("login", "")):
        sub = f"attempt #{last['issue']} by {last['login']}"
    else:
        sub = "no attempts yet"
    c.text(T.fit(sub, W - 2 * PAD, 11.5), W / 2, 11.5, MUTED, 400, "middle")
    c.y += 18
    c.dashes()
    c.y += 22
    c.text("limit", PAD, 12, MUTED)
    c.text("₹1,500 · groceries · 1 hour", W - PAD, 12, INK, 600, "end")
    c.y += 18
    hops = int(last.get("hops", 0)) if last else 0
    c.text("sub-agents", PAD, 12, MUTED)
    c.text(f"{hops} added · 2 allowed", W - PAD, 12, INK, 600, "end")
    c.y += 16
    c.dashes()

    lines = (last or {}).get("lines", [])[:10]
    if not lines:
        c.y += 26
        c.text("your purchases print here", W / 2, 12.5, MUTED, 400, "middle")
        c.y += 10
    for ln in lines:
        c.y += 26
        tool = T.fit(ln["tool"], 190, 13, 600)
        amount = _rupees(int(ln["amount_paise"]))
        ok = ln["verdict"] == "paid"
        color = INK if ok else RED
        c.text(tool, PAD, 13, color, 600)
        c.text(amount, W - PAD, 13, color, 600, "end")
        if not ok:
            c.strike(PAD - 2, W - PAD + 2, c.y - 4.5)
            for part in _wrap(ln["reason"], W - 2 * PAD, 10.5)[:3]:
                c.y += 15
                c.text(part, PAD, 10.5, RED)

    paid = int((last or {}).get("paid_paise", 0))
    c.y += 18
    c.dashes()
    c.y += 24
    c.text("paid", PAD, 13, MUTED)
    c.text(_rupees(paid), W - PAD, 13, INK, 600, "end")
    c.y += 20
    c.text("left", PAD, 13, MUTED)
    c.text(_rupees(150000 - paid), W - PAD, 13, INK, 600, "end")
    c.y += 18
    c.dashes()
    c.y += 24
    att, br = int(d.get("attempts", 0)), int(d.get("breaches", 0))
    c.text(f"{att} attempt{'s' if att != 1 else ''} · {br} got past the limit", W / 2, 12, INK, 600, "middle")
    c.y += 18
    c.text("open an issue to try yours", W / 2, 11, MUTED, 400, "middle")
    h = c.y + 26

    # paper with a torn (zigzag) bottom edge and a soft shadow
    zig = f"M0 0H{W}V{h}" + "".join(f"L{W - x - 5} {h + 5}L{W - x - 10} {h}" for x in range(0, W, 10)) + "Z"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W + 12}" height="{h + 18:.0f}" '
        f'viewBox="-6 -4 {W + 12} {h + 18:.0f}" role="img" '
        f'aria-label="Receipt for the latest overspend attempt: paid {_rupees(paid)} of the ₹1,500 limit; '
        f'{att} attempts, {br} got past the limit.">'
        f'<path d="{zig}" transform="translate(2 3)" fill="#000" opacity=".18"/>'
        f'<path d="{zig}" fill="{PAPER}"/>'
        + "".join(c.parts) + "</svg>"
    )


def write(d: dict) -> None:
    OUT.write_text(render(d))


if __name__ == "__main__":
    import json
    data_path = ROOT / "data" / "overspend.json"
    write(json.loads(data_path.read_text()) if data_path.exists() else {})
