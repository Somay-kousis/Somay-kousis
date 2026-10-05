"""Prepares the Pixels pets for the profile (run locally; needs Pillow).

    python3 art/pets.py

- assets/pets/<name>.gif   each pet cropped and scaled for the README (2x for sharp screens)
- assets/header.gif        the animated header: name, tagline, all five pets on the floor with speech bubbles
- pets/frames.json         small frames of mew, gengar and the cat for the contribution-grid animation
"""

import base64
import io
import json
import random
import sys
from pathlib import Path

from PIL import Image, ImageSequence

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "art"))
from build import GLYPHS, text_width  # noqa: E402  (the 5x7 pixel font)

PETS = ROOT / "assets" / "pets"
NIGHT, INK, CREAM, YELLOW, PINK, FLOOR = (14, 16, 32), (31, 18, 56), (255, 248, 231), (255, 210, 31), (255, 143, 200), (34, 30, 60)

# name: (source, scale for README GIF at 2x, scale in the header at 1x, smooth?)
SPEC = {
    "cat": ("src-cat.gif", 8 / 7, 6 / 7, False),        # 7x pixel art: whole pixels
    "vaporeon": ("src-vaporeon.gif", 4 / 5, 2 / 5, False),
    "lapras": ("src-lapras.gif", 3 / 4, 2 / 4, False),
    "gengar": ("src-gengar.gif", 0.52, 0.27, True),       # resized source: no clean grid
    "mew": ("src-mew.gif", 1.1, 0.55, True),
}


def load(name: str) -> tuple[list[Image.Image], int]:
    src = Image.open(PETS / SPEC[name][0])
    frames = [f.convert("RGBA") for f in ImageSequence.Iterator(src)]
    box = None
    for f in frames:
        b = f.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    return [f.crop(box) for f in frames], src.info.get("duration", 100) or 100


def scaled(frames: list[Image.Image], s: float, smooth: bool) -> list[Image.Image]:
    out = []
    for f in frames:
        w, h = max(1, round(f.width * s)), max(1, round(f.height * s))
        g = f.resize((w, h), Image.LANCZOS if smooth else Image.NEAREST)
        if smooth:   # GIF has 1-bit alpha: snap soft edges so there is no halo
            a = g.getchannel("A").point(lambda v: 255 if v > 110 else 0)
            g.putalpha(a)
        out.append(g)
    return out


def save_gif(frames: list[Image.Image], path: Path, duration: int) -> None:
    pal = []
    for f in frames:
        p = f.convert("RGBA")
        alpha = p.getchannel("A")
        q = p.convert("RGB").quantize(colors=255, method=Image.Quantize.MEDIANCUT)
        q.paste(255, mask=alpha.point(lambda v: 255 if v < 128 else 0))
        q.info["transparency"] = 255
        pal.append(q)
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=duration, loop=0, disposal=2, transparency=255)


# ---------------------------------------------------------------- drawing helpers (PIL)

def ptext(img: Image.Image, s: str, x: int, y: int, scale: int, color, anchor: str = "start") -> None:
    s = s.upper()
    if anchor == "middle":
        x -= text_width(s, scale) // 2
    px = img.load()
    cx = x
    for ch in s:
        g = GLYPHS[ch]
        for r, row in enumerate(g):
            for c, bit in enumerate(row):
                if bit == "#":
                    for dy in range(scale):
                        for dx in range(scale):
                            xx, yy = cx + c * scale + dx, y + r * scale + dy
                            if 0 <= xx < img.width and 0 <= yy < img.height:
                                px[xx, yy] = color
        cx += (len(g[0]) + 1) * scale


def bubble(img: Image.Image, text: str, cx: int, bottom: int) -> None:
    """Pixels-style speech bubble: cream, ink outline, hard shadow, little tail."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    w = text_width(text.upper(), 2) + 20
    h = 30
    x0, y0 = cx - w // 2, bottom - h - 8
    d.rectangle([x0 + 4, y0 + 4, x0 + w + 4, y0 + h + 4], fill=INK)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=CREAM, outline=INK, width=3)
    d.polygon([(cx - 6, y0 + h), (cx + 6, y0 + h), (cx, y0 + h + 8)], fill=INK)
    d.polygon([(cx - 3, y0 + h - 1), (cx + 3, y0 + h - 1), (cx, y0 + h + 3)], fill=CREAM)
    ptext(img, text, x0 + 10, y0 + 8, 2, INK)


# ---------------------------------------------------------------- outputs

def readme_gifs() -> None:
    for name, (_, s2x, _, smooth) in SPEC.items():
        frames, dur = load(name)
        save_gif(scaled(frames, s2x, smooth), PETS / f"{name}.gif", dur)


def header() -> None:
    W, H, FLOOR_Y, STEP, N = 900, 360, 316, 100, 60     # 6 s loop at 10 fps
    rnd = random.Random(5)
    stars = [(rnd.randrange(6, W - 6, 3), rnd.randrange(6, 200, 3), rnd.choice([2, 2, 3]), rnd.random()) for _ in range(55)]
    cast = {}
    for name, (_, _, s1x, smooth) in SPEC.items():
        frames, dur = load(name)
        cast[name] = (scaled(frames, s1x, smooth), dur)
    # x centre, float height, bubble lines (shown in turns), bubble phase
    layout = {
        "vaporeon": (110, 0, ["~", "BLUB", "SPLASH!"], 0),
        "gengar": (275, 34, ["HEHE", "BOO!", ">:)"], 1),
        "cat": (450, 0, ["...", "MRRP", "HMPH."], 2),
        "lapras": (625, 0, ["LA LA~", "LA~"], 3),
        "mew": (795, 44, ["MEW!", "MEW MEW"], 4),
    }
    out = []
    for i in range(N):
        t = i * STEP
        img = Image.new("RGB", (W, H), NIGHT)
        px = img.load()
        for sx, sy, ss, ph in stars:
            if (i / 12 + ph) % 1 < 0.75:
                c = CREAM if ph < 0.6 else (159, 216, 255) if ph < 0.85 else YELLOW
                for dy in range(ss):
                    for dx in range(ss):
                        px[sx + dx, sy + dy] = c
        ptext(img, "SOMAY KOUSIS", W // 2, 40, 7, CREAM, "middle")
        ptext(img, "I BUILD AI AGENTS AND THE PARTS THAT KEEP THEM HONEST", W // 2, 112, 2, YELLOW, "middle")
        img.paste(FLOOR, (0, FLOOR_Y, W, H))
        img.paste(INK, (0, FLOOR_Y, W, FLOOR_Y + 4))
        for name, (cx, lift, lines, phase) in layout.items():
            frames, dur = cast[name]
            f = frames[(t // dur) % len(frames)]
            bob = round(4 * __import__("math").sin((t / 1000) * 2.2 + phase)) if lift else 0
            x, y = cx - f.width // 2, FLOOR_Y - f.height - lift + bob + (2 if not lift else 0)
            img.paste(f, (x, y), f)
            # each pet talks for 2 of every 6 seconds, in turns
            slot = (i // 20 + phase) % 3
            if slot == 0:
                body_top = y + min(f.getchannel("A").getbbox()[1], f.height)
                bubble(img, lines[(i // 60 + phase) % len(lines)] if len(lines) else "", cx, body_top - 4)
        out.append(img)
    pal = [f.quantize(colors=256, method=Image.Quantize.MEDIANCUT) for f in out]
    pal[0].save(ROOT / "assets" / "header.gif", save_all=True, append_images=pal[1:], duration=STEP, loop=0, optimize=True)


def grid_frames() -> None:
    """Tiny frames for the contribution-grid walkers, base64 PNGs, about 34 px tall."""
    data = {}
    for name in ("mew", "gengar", "cat"):
        frames, dur = load(name)
        s = 34 / max(f.getchannel("A").getbbox()[3] - f.getchannel("A").getbbox()[1] for f in frames)
        small = scaled(frames, s * (frames[0].height / frames[0].height), True)
        enc = []
        for f in small:
            buf = io.BytesIO()
            f.save(buf, "PNG", optimize=True)
            enc.append(base64.b64encode(buf.getvalue()).decode())
        data[name] = {"w": small[0].width, "h": small[0].height, "delay": dur / 1000, "frames": enc}
    (ROOT / "pets" / "frames.json").write_text(json.dumps(data))


if __name__ == "__main__":
    readme_gifs()
    header()
    grid_frames()
    for p in sorted(list(PETS.glob("[!s]*.gif")) + [ROOT / "assets" / "header.gif", ROOT / "pets" / "frames.json"]):
        print(f"{p.relative_to(ROOT)}  {p.stat().st_size // 1024} KB")
