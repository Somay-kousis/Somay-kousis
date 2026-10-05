"""Builds every image on the profile into assets/: header, cards, titles, trophy shelf, inventory, buttons.

Everything is drawn here as pixel art in plain SVG (no fonts or images to load), so it renders the same
inside GitHub's <img> tags. Standard library only.

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


# ---------------------------------------------------------------- header

def header() -> str:
    W, H = 900, 300
    rnd = random.Random(7)
    css = [
        "@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}",
        ".st{animation:tw 3s ease-in-out infinite}",
        "@keyframes blink{0%,90%,100%{transform:scaleY(1)}93%,95%{transform:scaleY(.08)}}",
        ".eye{transform-box:fill-box;transform-origin:center;animation:blink 4.2s infinite}",
        "@keyframes look{0%,18%{transform:translate(0,0)}24%,42%{transform:translate(-8px,0)}"
        "48%,66%{transform:translate(8px,0)}72%,86%{transform:translate(0,4px)}92%,100%{transform:translate(0,0)}}",
        ".pupil{animation:look 9s steps(1,end) infinite}",
        "@keyframes peek{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}",
        ".pk{animation:peek 3.2s ease-in-out infinite}",
    ]
    body = [f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>']
    for i in range(46):
        x, y = rnd.randrange(8, W - 8, 4), rnd.randrange(8, H - 70, 4)
        size = rnd.choice([2, 2, 3, 4])
        body.append(f'<rect class="st" x="{x}" y="{y}" width="{size}" height="{size}" fill="{rnd.choice([CREAM, CREAM, SKY, YELLOW])}" '
                    f'style="animation-delay:-{rnd.uniform(0, 3):.2f}s;animation-duration:{rnd.uniform(2.2, 4.8):.2f}s"/>')
    body.append(f'<rect y="{H - 34}" width="{W}" height="34" fill="#15182e"/>')

    # The eyes: blink (the name) and look around.
    px, R = 4, 7
    for cx in (402, 498):
        eye = []
        for gy in range(-R - 1, R + 2):
            for gx in range(-R - 1, R + 2):
                d = (gx * gx + gy * gy) ** 0.5
                if d <= R - 0.3:
                    eye.append((gx, gy, CREAM))
                elif d <= R + 0.8:
                    eye.append((gx, gy, INK))
        rects = "".join(f'<rect x="{cx + gx * px}" y="{78 + gy * px}" width="{px}" height="{px}" fill="{f}"/>' for gx, gy, f in eye)
        pupil = (f'<g class="pupil"><rect x="{cx - 10}" y="{78 - 10}" width="20" height="20" fill="{INK}"/>'
                 f'<rect x="{cx - 6}" y="{78 - 6}" width="6" height="6" fill="{CREAM}"/></g>')
        body.append(f'<g class="eye" shape-rendering="crispEdges">{rects}{pupil}</g>')

    body.append(pixel_text("SOMAY KOUSIS", W / 2, 130, 6, CREAM, "middle"))
    body.append(pixel_text("AKA BLINK", W / 2, 186, 3, PINK, "middle"))
    body.append(pixel_text("AGENTS · MEMORY · THINGS THAT FEEL A LITTLE ALIVE", W / 2, 222, 2, YELLOW, "middle"))

    # The pets peeking up from the bottom edge, like Pixels' hide mode.
    for name, x, delay in (("ghost", 70, 0), ("axolotl", 715, -1.1), ("cat", 790, -2.2)):
        h = len(SPRITES[name]["art"]) * 5
        body.append(f'<g class="pk" style="animation-delay:{delay}s">{sprite_art(name, x, H - h * 0.62, 5)}</g>')
    return svg(W, H, "".join(body), "Somay Kousis, aka Blink: a pair of pixel eyes blinking over a night sky", "".join(css))


# ---------------------------------------------------------------- cards

def card(icon: str, title: str, tag: tuple[str, str], text: str, chip_list: list[tuple[str, str]],
         W: int = 440, H: int = 236, wrap_at: int = 46, title_scale: int | None = None, icon_scale: int = 4) -> str:
    body = [sticker(4, 4, W - 16, H - 16)]
    art = ICONS[icon] if icon in ICONS else SPRITES[icon]["art"]
    colors = None if icon in ICONS else SPRITES[icon]["colors"]
    body.append(pixel_art(art, 26, 26, icon_scale, colors))
    tx = 26 + len(art[0]) * icon_scale + 16
    tag_text, tag_color = tag
    tw = text_width(tag_text, 2) + 20
    room = (W - 32 - tw) - tx - 14          # space between the icon and the tag
    ts = title_scale or (3 if text_width(title, 3) <= room else 2)
    body.append(pixel_text(title, tx, 34 if ts >= 3 else 38, ts, INK))
    body.append(f'<rect x="{W - 32 - tw}" y="24" width="{tw}" height="26" fill="{tag_color}" stroke="{INK}" stroke-width="2.5"/>')
    body.append(pixel_text(tag_text, W - 32 - tw + 10, 30, 2, INK))
    y = 98 if icon_scale <= 4 else 26 + len(art) * icon_scale + 26
    for i, line in enumerate(wrap(text, wrap_at)):
        body.append(f'<text x="26" y="{y + i * 22}" font-family="{SANS}" font-size="15" fill="{INK}">{esc(line)}</text>')
    body.append(chips(chip_list, 26, H - 60))
    return svg(W, H, "".join(body), f"{title}: {text}")


CARDS = {
    "paperplanes": ("plane", "PaperPlanes", ("3RD PLACE", YELLOW),
                    "a research buddy whose memory stays right after it's proven wrong. old facts get closed, not overwritten.",
                    [("25/25 writes held", MINT), ("flat file kept 1", PINK)]),
    "pocket-change": ("coin", "Pocket Change", ("LIVE", MINT),
                      "permissions for ai agents that only shrink as they get passed down. a sub-agent never gets more than its parent had.",
                      [("400 tests, offline", SKY), ("10/12 attacks stopped", YELLOW)]),
    "apocalypse": ("lock", "Apocalypse", ("SPRINT", PINK),
                   "a 9-rule containment standard for a real ai sandbox escape, plus a broken lab and a fixed lab to prove it works.",
                   [("broken 0/9", PINK), ("fixed 9/9", MINT), ("118 tests", SKY)]),
    "podman": ("flake", "podman-flake-agent", ("LFX", SKY),
               "sorts flaky ci failures for podman and says 'unknown' instead of guessing. a confident wrong guess hides real bugs.",
               [("logs 76-93% smaller", YELLOW), ("zero deps", MINT)]),
    "oversight": ("spy", "Perceived Oversight", ("PAPER", YELLOW),
                  "does an ai hide less from a watcher it thinks is just a teammate? the spy on the team vs the camera on the wall.",
                  [("6 conditions", SKY), ("AAAI-27 UC submitted", PINK)]),
    "graduation": ("cap", "Graduation", ("CLIENT", SKY),
                   "know who to talk to on linkedin, then actually talk to them. it drafts the message. it never clicks send for you.",
                   [("chrome extension", YELLOW), ("langgraph + claude", MINT)]),
    "rabbithole": ("rabbit", "RabbitHole", ("AGENTS", MINT),
                   "an ai courtroom over real legal docs. asked for 2 perspectives, got 8, so the limit moved from the prompt into the state.",
                   [("19.8s -> 9.8s", YELLOW), ("hybrid retrieval", SKY)]),
    "coop": ("cart", "Co-op Purchase", ("AGENTS", MINT),
             "when shopping agents collide, settle it with auctions and group discounts instead of a bidding war.",
             [("~7 rounds to a price", PINK), ("46 tests", SKY)]),
    "cofounder-memory": ("floppy", "Co-Founder Memory", ("AGENTS", MINT),
                         "a 19-node langgraph that remembers your project and writes you a catch-up every night.",
                         [("pgvector + hnsw", SKY), ("19 nodes", YELLOW)]),
    "pixels": ("cat", "Pixels", ("FOR FUN", PINK),
               "desktop pets that make me drink water. ignore the cat for 10 minutes and it takes over the whole screen.",
               [("swift", YELLOW), ("built in a day", MINT)]),
    "something": ("tomb", "Something", ("R.I.P.", "#d9d4e4"),
                  "a founder-investor matching platform. 573 people joined in the first month. it still didn't make it.",
                  [("573 waitlist", YELLOW), ("open source now", MINT)]),
    "portfolio": ("window", "Portfolio", ("WEB", SKY),
                  "my site. every number on it links to the repo that proves it, which was the only rule.",
                  [("next.js", YELLOW), ("framer motion", PINK)]),
}


def now_card() -> str:
    return card("eye", "aye aye", ("NOW · CEO", YELLOW),
                "ai writes more of the code that ships now, and review is where it quietly breaks: someone hits approve on a diff "
                "they never read. aye aye makes sure the person shipping it can explain it, out loud, graded against the real diff.",
                [("pre-launch", PINK), ("waitlist open", MINT), ("with charlotte liu", SKY)],
                W=900, H=250, wrap_at=96, title_scale=5, icon_scale=5)


# ---------------------------------------------------------------- titles, shelf, inventory, buttons

def title(s: str) -> str:
    w = text_width(s, 3) + 44
    return svg(w + 12, 60, sticker(4, 4, w, 44, YELLOW, 5, 3) + pixel_text(s, 26, 15, 3, INK), s)


def shelf() -> str:
    W, H = 900, 250
    body = [sticker(4, 4, W - 16, H - 16)]
    body.append(f'<rect x="30" y="150" width="{W - 68}" height="12" fill="{"#b07a45"}" stroke="{INK}" stroke-width="3"/>')
    wins = [("1ST", "EGOIST MACHINES", "IDEATHON", YELLOW), ("2ND", "HACKSAGON 2024", "HARDWARE TRACK", "#d3d7e3"),
            ("3RD", "COCKROACHDB X AWS", "HACKATHON", "#d98a4e"), ("6TH", "SMART INDIA", "HACKATHON 2025", SKY)]
    col = (W - 16) / 4
    for i, (place, name, sub, color) in enumerate(wins):
        cx = 4 + col * i + col / 2
        body.append(pixel_art(ICONS["cup"], cx - 25, 104, 5, {**PALETTE, "y": color}))
        body.append(pixel_text(place, cx, 36, 4, INK, "middle"))
        body.append(pixel_text(name, cx, 178, 2, INK, "middle"))
        body.append(pixel_text(sub, cx, 198, 2, "#6b6480", "middle"))
    return svg(W, H, "".join(body), "Trophy shelf: 1st Egoist Machines ideathon, 2nd Hacksagon 2024, 3rd CockroachDB x AWS hackathon, 6th Smart India Hackathon 2025")


def inventory() -> str:
    items = ["PYTHON", "LANGGRAPH", "FASTAPI", "CLAUDE API", "MCP", "COCKROACHDB", "POSTGRES", "SUPABASE",
             "PINECONE", "NEXT.JS", "TYPESCRIPT", "TAILWIND", "SWIFT", "CHROME MV3", "DOCKER", "CLOUD RUN"]
    W, cols, sw, sh, gap = 900, 4, 196, 46, 14
    rows = (len(items) + cols - 1) // cols
    H = 36 + rows * (sh + gap) + 22
    body = [sticker(4, 4, W - 16, H - 16)]
    x0 = (W - 12 - (cols * sw + (cols - 1) * gap)) / 2
    fills = [SKY, YELLOW, PINK, MINT]
    for i, it in enumerate(items):
        x, y = x0 + (i % cols) * (sw + gap), 30 + (i // cols) * (sh + gap)
        body.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sh}" fill="#f1ead8" stroke="{INK}" stroke-width="3"/>')
        body.append(f'<rect x="{x + 10}" y="{y + 15}" width="16" height="16" fill="{fills[i % 4]}" stroke="{INK}" stroke-width="2"/>')
        body.append(pixel_text(it, x + 38, y + 16, 2, INK))
    return svg(W, H, "".join(body), "Inventory: " + ", ".join(i.lower() for i in items))


def button(s: str, color: str) -> str:
    w = text_width(s + " >", 3) + 44
    return svg(w + 12, 64, sticker(4, 4, w, 48, color, 5, 3) + pixel_text(s + " >", 26, 17, 3, INK), s)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    files = {"header.svg": header(), "card-ayeaye.svg": now_card(), "shelf.svg": shelf(), "inventory.svg": inventory()}
    for slug, args in CARDS.items():
        files[f"card-{slug}.svg"] = card(*args)
    for slug, s in {"now": "NOW", "built": "THINGS I BUILT", "shelf": "TROPHY SHELF", "offscreen": "OFF-SCREEN",
                    "inventory": "INVENTORY", "hi": "SAY HI"}.items():
        files[f"title-{slug}.svg"] = title(s)
    for slug, (s, color) in {"aye": ("AYE AYE", YELLOW), "portfolio": ("PORTFOLIO", SKY), "linkedin": ("LINKEDIN", MINT),
                             "x": ("X", PINK)}.items():
        files[f"btn-{slug}.svg"] = button(s, color)
    for name, content in files.items():
        (OUT / name).write_text(content)
    print(f"{len(files)} files -> {OUT}")


if __name__ == "__main__":
    main()
