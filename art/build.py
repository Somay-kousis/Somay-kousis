"""Builds the profile's SVGs into assets/: the pets' speech bubbles, project cards, and link buttons.

The pets themselves (GIFs, grid frames) come from art/pets.py; the banner comes from art/header.py. Everything here is plain SVG
with a built-in pixel font, so it renders the same inside GitHub's <img> tags. Standard library only.

    python3 art/build.py
"""

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pets"))
from generate import SPRITES  # noqa: E402  (the same three critters that eat the contribution grid)

OUT = ROOT / "assets"

NIGHT = "#0e1020"
INK = "#1f1238"
CREAM = "#fff8e7"
YELLOW = "#ffd21f"
PINK = "#ff8fc8"
SKY = "#9fd8ff"
MINT = "#9ff0c4"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SFMono-Regular', Menlo, Consolas, monospace"

# ---------------------------------------------------------------- pixel font (5x7)

GLYPHS = {
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    "C": [" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    "F": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    "G": [" ####", "#    ", "#    ", "#  ##", "#   #", "#   #", " ####"],
    "H": ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "#####"],
    "J": ["  ###", "   # ", "   # ", "   # ", "#  # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    "S": [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"],
    "X": ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    "Y": ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    "0": [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "2": [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    "3": ["#### ", "    #", "    #", " ### ", "    #", "    #", "#### "],
    "4": ["#   #", "#   #", "#   #", "#####", "    #", "    #", "    #"],
    "5": ["#####", "#    ", "#    ", "#### ", "    #", "    #", "#### "],
    "6": [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    "7": ["#####", "    #", "   # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "8": [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    "9": [" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "],
    ".": ["  ", "  ", "  ", "  ", "  ", "##", "##"],
    ",": ["  ", "  ", "  ", "  ", "  ", " #", "# "],
    "!": ["#", "#", "#", "#", "#", " ", "#"],
    "?": [" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "],
    "-": ["    ", "    ", "    ", "####", "    ", "    ", "    "],
    "/": ["    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "],
    ":": [" ", "#", "#", " ", "#", "#", " "],
    "'": ["#", "#", " ", " ", " ", " ", " "],
    "&": [" ##  ", "#  # ", "#  # ", " ##  ", "# # #", "#  # ", " ## #"],
    "+": ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    "@": [" ### ", "#   #", "# ###", "# # #", "# ###", "#    ", " ####"],
    "·": [" ", " ", " ", "#", " ", " ", " "],
    ">": ["#   ", " #  ", "  # ", "   #", "  # ", " #  ", "#   "],
    "~": ["     ", "     ", " #  #", "# ## ", "     ", "     ", "     "],
    "(": ["  #", " # ", "#  ", "#  ", "#  ", " # ", "  #"],
    ")": ["#  ", " # ", "  #", "  #", "  #", " # ", "#  "],
    "♪": ["  ## ", "  # #", "  #  ", "  #  ", "###  ", "###  ", "     "],
    " ": ["   "] * 7,
}


def text_width(s: str, scale: int) -> int:
    return sum((len(GLYPHS[c][0]) + 1) * scale for c in s.upper()) - scale


def pixel_text(s: str, x: float, y: float, scale: int, fill: str, anchor: str = "start") -> str:
    """Pixel-font text as one <path>; (x, y) is the top-left corner (or top-centre / top-right)."""
    s = s.upper()
    w = text_width(s, scale)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    d, cx = [], x
    for ch in s:
        g = GLYPHS[ch]
        for r, row in enumerate(g):
            for c, bit in enumerate(row):
                if bit == "#":
                    d.append(f"M{cx + c * scale:g} {y + r * scale:g}h{scale}v{scale}h-{scale}z")
        cx += (len(g[0]) + 1) * scale
    return f'<path d="{"".join(d)}" fill="{fill}" shape-rendering="crispEdges"/>'


# ---------------------------------------------------------------- pixel art

PALETTE = {"k": INK, "w": CREAM, "y": YELLOW, "p": PINK, "b": SKY, "g": "#b8b3c4", "o": "#d98a4e",
           "n": "#6fcf8f", "r": "#ff5d6c", "s": "#cfd6e6"}

ICONS = {
    "eye": ["..kkkkkk..", ".kwwwwwwk.", "kwwwkkwwwk", "kwwkkkkwwk", "kwwkkkkwwk", "kwwwkkwwwk", ".kwwwwwwk.", "..kkkkkk.."],
    "plane": [".........k", ".......kkk", ".....kkwwk", "...kkwwwk.", ".kkwwwwwk.", "kkkkkkwk..", ".....kwk..", ".....kk...", "......k..."],
    "coin": ["..kkkkkk..", ".kyyyyyyk.", "kyywwyyyyk", "kywyyyyyyk", "kyyyyyyyyk", "kyyyyyyyyk", "kyyyyyywyk", "kyyyyywwyk", ".kyyyyyyk.", "..kkkkkk.."],
    "lock": ["...kkkk...", "..k....k..", "..k....k..", ".kkkkkkkk.", ".kyyyyyyk.", ".kyyykyyk.", ".kyyykyyk.", ".kyyyyyyk.", ".kkkkkkkk."],
    "flake": ["....b....", "..b.b.b..", "...bbb...", "bbbbbbbbb", "...bbb...", "..b.b.b..", "....b...."],
    "rabbit": [".k...k..", "kwk.kwk.", "kwk.kwk.", "kwk.kwk.", ".kwwwwk.", "kwwwwwwk", "kwkwwkwk", "kwwwppwk", ".kwwwwk.", "..kkkk.."],
    "cap": ["....kk....", "..kkkkkk..", "kkkkkkkkkk", "..kkkkkky.", "..kkkkkky.", "...kkkk.y.", "........y.", ".......yy."],
    "spy": ["...kkkk...", "..kkkkkk..", "kkkkkkkkkk", "..........", "kkkkkkkkkk", ".kbk..kbk.", ".kkk..kkk."],
    "cart": ["k.........", "kk........", ".kkkkkkkkk", ".kyyyyyyk.", ".kyyyyyyk.", "..kkkkkkk.", "..........", "...k...k.."],
    "floppy": ["kkkkkkkkk.", "kbbwwwwbkk", "kbbwwkwbbk", "kbbwwwwbbk", "kbbbbbbbbk", "kbwwwwwwbk", "kbwkkkkwbk", "kbwwwwwwbk", "kkkkkkkkkk"],
    "tomb": ["..kkkkkk..", ".kggggggk.", "kgggkggggk", "kggkkkgggk", "kgggkggggk", "kgggkggggk", "kggggggggk", "kggggggggk", "nnnnnnnnnn"],
    "window": ["kkkkkkkkkk", "kpkykbkkkk", "kkkkkkkkkk", "kwwwwwwwwk", "kwbbwwwwwk", "kwbbwkkkwk", "kwwwwwwwwk", "kwkkkkkkwk", "kkkkkkkkkk"],
    "cup": ["kkkkkkkkkk", "kyyyyyyyyk", "kyyyyyyyyk", ".kyyyyyyk.", "..kyyyyk..", "...kyyk...", "....kk....", "...kyyk...", "..kkkkkk.."],
}


def pixel_art(rows: list[str], x: float, y: float, scale: int, colors: dict | None = None) -> str:
    cols = colors or PALETTE
    by_color: dict[str, list[str]] = {}
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != ".":
                by_color.setdefault(cols[ch], []).append(f"M{x + c * scale:g} {y + r * scale:g}h{scale}v{scale}h-{scale}z")
    return "".join(f'<path d="{"".join(d)}" fill="{f}" shape-rendering="crispEdges"/>' for f, d in by_color.items())


def sprite_art(name: str, x: float, y: float, scale: int) -> str:
    s = SPRITES[name]
    return pixel_art(s["art"], x, y, scale, s["colors"])


def svg(w: int, h: int, body: str, label: str, style: str = "") -> str:
    css = f"<style>{style}@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>" if style else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}">{css}{body}</svg>\n')


def sticker(x: float, y: float, w: float, h: float, fill: str = CREAM, shadow: int = 6, stroke: int = 4) -> str:
    """The Pixels speech-bubble look: flat fill, thick ink outline, hard offset shadow."""
    return (f'<rect x="{x + shadow}" y="{y + shadow}" width="{w}" height="{h}" fill="{INK}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="{stroke}"/>')


def wrap(text: str, width: int) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + ([cur] if cur else [])


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chips(items: list[tuple[str, str]], x: float, y: float) -> str:
    out = []
    for label, color in items:
        w = len(label) * 7.6 + 22
        out.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="{color}" stroke="{INK}" stroke-width="2.5"/>'
                   f'<text x="{x + w / 2:.1f}" y="{y + 17.5}" text-anchor="middle" font-family="{MONO}" font-size="12.5" '
                   f'font-weight="700" fill="{INK}">{esc(label)}</text>')
        x += w + 10
    return "".join(out)


# ---------------------------------------------------------------- speech bubbles (one per pet-hosted section)

def bubble_frame(W: int, h: int, tail: str) -> tuple[str, int]:
    """Cream bubble with ink outline, hard shadow, and a tail pointing down at the pet. Returns (svg, total height)."""
    bx, by, bw = 4, 4, W - 24
    base = 60 if tail == "left" else bw - 60
    tip_x = base - 34 if tail == "left" else base + 34
    l, r = base - 16, base + 16
    tip_y = by + h + 30
    pts = f"{l},{by + h} {r},{by + h} {tip_x},{tip_y}"
    shadow_pts = f"{l + 6},{by + h + 6} {r + 6},{by + h + 6} {tip_x + 6},{tip_y + 6}"
    out = (f'<rect x="{bx + 6}" y="{by + 6}" width="{bw}" height="{h}" fill="{INK}"/>'
           f'<polygon points="{shadow_pts}" fill="{INK}"/>'
           f'<rect x="{bx}" y="{by}" width="{bw}" height="{h}" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>'
           f'<polygon points="{pts}" fill="{CREAM}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
           f'<rect x="{l + 3}" y="{by + h - 3}" width="{r - l - 6}" height="5" fill="{CREAM}"/>')
    return out, tip_y + 12

def chip_rows(items: list[tuple[str, str]], x0: float, y: float, max_w: float) -> tuple[str, float]:
    """Chips that wrap onto new rows; returns (svg, y after the last row)."""
    out, x = [], x0
    for label, color in items:
        w = len(label) * 7.6 + 22
        if x + w > x0 + max_w:
            x, y = x0, y + 36
        out.append(chips([(label, color)], x, y))
        x += w + 10
    return "".join(out), y + 26


def say(voice: str, paragraphs: list[str] = (), bullets: list[str] = (), chip_list: list[tuple[str, str]] = (),
        tail: str = "left", W: int = 700, wrap_at: int = 84) -> str:
    """A Pixels speech bubble: the pet's line in pixel type, then the content. The tail points at the pet."""
    pad, body = 30, []
    y = 30
    body.append(pixel_text(voice, pad, y, 3, INK))
    y += 21 + 26
    for para in paragraphs:
        for line in wrap(para, wrap_at):
            body.append(f'<text x="{pad}" y="{y + 12}" font-family="{SANS}" font-size="15.5" fill="{INK}">{esc(line)}</text>')
            y += 23
        y += 10
    for b in bullets:
        lines = wrap(b, wrap_at - 4)
        body.append(f'<rect x="{pad}" y="{y + 4}" width="7" height="7" fill="{INK}"/>')
        for line in lines:
            body.append(f'<text x="{pad + 18}" y="{y + 12}" font-family="{SANS}" font-size="15.5" fill="{INK}">{esc(line)}</text>')
            y += 23
        y += 6
    if chip_list:
        y += 4
        svg_chips, y = chip_rows(list(chip_list), pad, y, W - 2 * pad - 20)
        body.append(svg_chips)
        y += 6
    frame, total = bubble_frame(W, y + 14, tail)
    return svg(W, total, frame + "".join(body), voice)


SECTIONS = {
    "intro": dict(voice="HMPH. FINE. I'LL DO THE INTRO.", tail="left", paragraphs=[
        "this is somay. third-year cs at abv-iiitm gwalior. he builds ai agents, and then the boring parts that keep "
        "them honest: memory that stays right after it's proven wrong, permissions a sub-agent can't sneak around, "
        "proof that a human actually read the code before it shipped.",
        "co-founder at aye aye, freelancing at standout. before that he interned at ryse, where his orchestrator "
        "routed 10,000+ tasks a day. "
        "he also made me, to remind him to drink water. he ignores me. so i take over his screen.",
    ]),
    "now": dict(voice="MEW! LOOK WHAT HE'S MAKING NOW", tail="right", paragraphs=[
        "aye aye. ai writes more and more of the code that ships, and review is where it quietly breaks: someone hits "
        "approve on a diff they never read. aye aye makes the person shipping a risky change explain it out loud, and "
        "a separate judge analyses that against the real diff. boring changes get skipped on purpose.",
        "the name: an aye-aye taps on wood and listens for the hollow spot before it trusts it. and \"aye aye\" means "
        "an order was heard and understood, not just received.",
    ], chip_list=[("pre-launch", PINK), ("waitlist open", MINT), ("with charlotte liu", SKY), ("ayeayecaptain.vercel.app", YELLOW)]),
    "built": dict(voice="HEHE. LOOK AT ALL THE STUFF HE MADE.", tail="left", paragraphs=[
        "every card opens its repo, except graduation (client work, it's private). i'm hiding behind one of them.",
    ]),
    "wins": dict(voice="♪ LA LA~ HIS WINS ♪", tail="right", bullets=[
        "1st at the egoistic ideathon 2026",
        "2nd at hacksagon 2024, hardware track",
        "3rd at the cockroachdb x aws hackathon, with paperplanes",
        "6th in the whole country at smart india hackathon 2025, leading a team of six",
        "also: the apart x cesia ai incident response sprint (that's apocalypse), and anthropic's mcp course",
    ], paragraphs=[], chip_list=[]),
    "stack": dict(voice="♪ AND I CARRY HIS TOOLBOX ♪", tail="right", chip_list=[
        ("python", YELLOW), ("langgraph", MINT), ("fastapi", SKY), ("claude api", PINK), ("mcp", YELLOW),
        ("cockroachdb", MINT), ("postgres", SKY), ("supabase", PINK), ("pinecone", YELLOW), ("next.js", MINT),
        ("typescript", SKY), ("tailwind", PINK), ("swift", YELLOW), ("chrome extensions", MINT), ("docker", SKY),
        ("cloud run", PINK)]),
    "offscreen": dict(voice="~ BLUB. THE OFF-SCREEN STUFF", tail="left", bullets=[
        "writes poetry. published in cama magazine (canada), performed to rooms of 350+.",
        "teaches math, english and life skills to kids with the sgm social initiative, most weeks.",
        "ran logistics for a 1000+ person college fest.",
        "7,000+ people follow his writing on dev.to.",
    ], paragraphs=[
        "still bad at: finishing one thing before starting five more (see gengar's pile), dsa consistency, and "
        "writing the limitations section before someone else finds it.",
    ]),
    "hi": dict(voice="...ANYWAY. SAY HI. OR DON'T.", tail="left", W=560, wrap_at=62, paragraphs=[
        "he answers faster than i come when called.",
    ]),
}


def section(name: str) -> str:
    kw = dict(SECTIONS[name])
    paragraphs, bullets = kw.pop("paragraphs", []), kw.pop("bullets", [])
    if name == "offscreen":                 # bullets first, then a closing aside
        return _bullets_then_text(kw, bullets, paragraphs)
    return say(paragraphs=paragraphs, bullets=bullets, **kw)


def _bullets_then_text(kw: dict, bullets: list[str], paragraphs: list[str]) -> str:
    W, wrap_at = kw.get("W", 700), kw.get("wrap_at", 84)
    pad, y, body = 30, 30, [pixel_text(kw["voice"], 30, 30, 3, INK)]
    y += 47
    for b in bullets:
        body.append(f'<rect x="{pad}" y="{y + 4}" width="7" height="7" fill="{INK}"/>')
        for line in wrap(b, wrap_at - 4):
            body.append(f'<text x="{pad + 18}" y="{y + 12}" font-family="{SANS}" font-size="15.5" fill="{INK}">{esc(line)}</text>')
            y += 23
        y += 6
    y += 8
    for para in paragraphs:
        for line in wrap(para, wrap_at):
            body.append(f'<text x="{pad}" y="{y + 12}" font-family="{SANS}" font-size="15.5" font-style="italic" fill="#4a4060">{esc(line)}</text>')
            y += 23
    frame, total = bubble_frame(W, y + 14, kw.get("tail", "left"))
    return svg(W, total, frame + "".join(body), kw["voice"])


# ---------------------------------------------------------------- project cards

def card(title: str, color: str, tag: str, text: str, chip_list: list[tuple[str, str]], W: int = 440, H: int = 214) -> str:
    """Cream card with a coloured name strip, like a sticker label."""
    body = [sticker(4, 4, W - 16, H - 16)]
    body.append(f'<rect x="6" y="6" width="{W - 20}" height="52" fill="{color}"/>'
                f'<rect x="6" y="56" width="{W - 20}" height="4" fill="{INK}"/>')
    tw = text_width(tag, 2) + 18
    room = W - 16 - 22 - tw - 18 - 20
    ts = 3 if text_width(title, 3) <= room else 2
    body.append(pixel_text(title, 24, 22 if ts == 3 else 25, ts, INK))
    body.append(f'<rect x="{W - 30 - tw}" y="19" width="{tw}" height="24" fill="{CREAM}" stroke="{INK}" stroke-width="2.5"/>')
    body.append(pixel_text(tag, W - 30 - tw + 9, 24, 2, INK))
    for i, line in enumerate(wrap(text, 47)):
        body.append(f'<text x="24" y="{92 + i * 21}" font-family="{SANS}" font-size="14.5" fill="{INK}">{esc(line)}</text>')
    body.append(chips(chip_list, 24, H - 56))
    return svg(W, H, "".join(body), f"{title}: {text}")


CARDS = {
    "paperplanes": ("PaperPlanes", SKY, "3RD PLACE",
                    "a research buddy with a memory that stays right after it's proven wrong. old facts get closed, never overwritten.",
                    [("25/25 writes held", MINT), ("flat file kept 1", PINK)]),
    "pocket-change": ("Pocket Change", YELLOW, "LIVE",
                      "permissions for ai agents that only shrink as they're handed down. a sub-agent never ends up with more than its parent.",
                      [("400 tests, offline", SKY), ("10/12 attacks stopped", MINT)]),
    "apocalypse": ("Apocalypse", PINK, "SPRINT",
                   "a containment standard for a real ai sandbox escape, with a broken lab and a fixed lab you can run in seconds.",
                   [("broken 0/9", PINK), ("fixed 9/9", MINT), ("118 tests", SKY)]),
    "podman": ("podman-flake-agent", MINT, "LFX",
               "sorts flaky ci failures for podman. says 'unknown' instead of guessing, because a confident wrong answer hides real bugs.",
               [("logs 76-93% smaller", YELLOW), ("zero deps", SKY)]),
    "oversight": ("Perceived Oversight", "#c9b8ff", "PAPER",
                  "will an ai hide less from a watcher it thinks is just a teammate? the spy on the team vs the camera on the wall.",
                  [("6 conditions", SKY), ("AAAI-27 UC submitted", PINK)]),
    "graduation": ("Graduation", SKY, "CLIENT",
                   "find the right people on linkedin, then actually talk to them. it drafts the message. you press send. always.",
                   [("chrome extension", YELLOW), ("langgraph + claude", MINT)]),
    "rabbithole": ("RabbitHole", YELLOW, "AGENTS",
                   "an ai courtroom over real legal docs. asked for 2 perspectives, got 8, so the limit moved from the prompt into the state.",
                   [("19.8s -> 9.8s", PINK), ("hybrid retrieval", SKY)]),
    "coop": ("Co-op Purchase", MINT, "AGENTS",
             "shopping agents that would fight over the same seller settle it with auctions and group discounts instead.",
             [("~7 rounds to a price", YELLOW), ("46 tests", PINK)]),
    "cofounder-memory": ("Co-Founder Memory", PINK, "AGENTS",
                         "a 19-node langgraph that remembers your project and writes you a catch-up every night.",
                         [("pgvector + hnsw", SKY), ("19 nodes", YELLOW)]),
    "pixels": ("Pixels", YELLOW, "THAT'S US",
               "us! desktop pets that make him drink water and go for walks. ignore the cat for 10 minutes and it takes over the screen.",
               [("swift", PINK), ("5 pets", MINT)]),
    "something": ("Something", "#d9d4e4", "R.I.P.",
                  "founder-investor matching. 573 people joined in the first month. it still didn't make it. open source now.",
                  [("573 waitlist", YELLOW), ("open source", MINT)]),
    "portfolio": ("Portfolio", "#c9b8ff", "WEB",
                  "his site. every number on it links to the repo that proves it, which was the only rule.",
                  [("next.js", YELLOW), ("framer motion", PINK)]),
}


def button(s: str, color: str) -> str:
    w = text_width(s + " >", 3) + 44
    return svg(w + 12, 64, sticker(4, 4, w, 48, color, 5, 3) + pixel_text(s + " >", 26, 17, 3, INK), s)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):          # everything here is generated; start clean
        old.unlink()
    files = {f"say-{name}.svg": section(name) for name in SECTIONS}
    for slug, args in CARDS.items():
        files[f"card-{slug}.svg"] = card(*args)
    for slug, (s, color) in {"aye": ("AYE AYE", YELLOW), "portfolio": ("PORTFOLIO", SKY), "linkedin": ("LINKEDIN", MINT),
                             "x": ("X", PINK)}.items():
        files[f"btn-{slug}.svg"] = button(s, color)
    for name, content in files.items():
        (OUT / name).write_text(content)
    print(f"{len(files)} files -> {OUT}")


if __name__ == "__main__":
    main()
