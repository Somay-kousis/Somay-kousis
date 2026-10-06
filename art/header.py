"""Build assets/header.png: plain GitHub-dark banner, name, one line of facts, the pixel cat on the floor.

Renders art/header.html with headless Chrome (fonts load from Google Fonts), at 2x for sharp text.
Run: python3 art/header.py
"""

import base64
import io
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1200, 360


def cat_png() -> str:
    im = Image.open(ROOT / "assets" / "pets" / "src-cat.gif")
    im.seek(0)
    im = im.convert("RGBA")
    im = im.crop(im.getbbox())
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


HTML = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;800&display=block" rel="stylesheet">
<style>
body{{margin:0;width:{W}px;height:{H}px;background:#0d1117;color:#e6edf3;font-family:Inter;position:relative;overflow:hidden}}
.t{{position:absolute;left:80px;top:96px}}
h1{{margin:0 0 20px;font-weight:800;font-size:84px;letter-spacing:-.035em;line-height:1}}
p{{margin:0;font-size:26px;color:#8b949e}}
p b{{color:#e6edf3;font-weight:500}}
.floor{{position:absolute;left:80px;right:80px;top:286px;border-top:2px solid #30363d}}
img{{position:absolute;right:110px;top:{cat_top}px;height:{cat_h}px;image-rendering:pixelated}}
</style></head><body>
<div class="t"><h1>Somay Kousis</h1>
<p>Building <b>aye aye</b>. Freelancing at <b>Standout</b>. CS at IIITM Gwalior.</p></div>
<div class="floor"></div>
<img src="data:image/png;base64,{cat}">
</body></html>"""


def main() -> None:
    cat_h = 72
    html = ROOT / "art" / "header.html"
    html.write_text(HTML.format(W=W, H=H, cat=cat_png(), cat_h=cat_h, cat_top=286 - cat_h + 2))
    out = ROOT / "assets" / "header.png"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=5000",
                    "--force-device-scale-factor=2", f"--window-size={W},{H}", f"--screenshot={out}",
                    html.as_uri()], check=True, capture_output=True)
    print(f"{out.relative_to(ROOT)}  {out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
