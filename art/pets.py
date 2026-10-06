"""Prepares the Pixels pets for the profile (run locally; needs Pillow).

    python3 art/pets.py

- assets/pets/<name>.gif   each pet cropped and scaled for the README (2x for sharp screens)
- pets/frames.json         small frames of mew, gengar and the cat for the contribution-grid animation
"""

import base64
import io
import json
from pathlib import Path

from PIL import Image, ImageSequence

ROOT = Path(__file__).resolve().parent.parent

PETS = ROOT / "assets" / "pets"

# name: (source, scale for README GIF at 2x, smooth?)
SPEC = {
    "cat": ("src-cat.gif", 8 / 7, False),        # 7x pixel art: whole pixels
    "vaporeon": ("src-vaporeon.gif", 4 / 5, False),
    "lapras": ("src-lapras.gif", 3 / 4, False),
    "gengar": ("src-gengar.gif", 0.52, True),       # resized source: no clean grid
    "mew": ("src-mew.gif", 1.1, True),
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


# ---------------------------------------------------------------- outputs

def readme_gifs() -> None:
    for name, (_, s2x, smooth) in SPEC.items():
        frames, dur = load(name)
        save_gif(scaled(frames, s2x, smooth), PETS / f"{name}.gif", dur)


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
    grid_frames()
    for p in sorted(list(PETS.glob("[!s]*.gif")) + [ROOT / "pets" / "frames.json"]):
        print(f"{p.relative_to(ROOT)}  {p.stat().st_size // 1024} KB")
