"""Keep the overspend scoreboard: data/overspend.json and the README line.

  python tally.py allowed <login>        exit 0 if this login may play now, 1 if not
  python tally.py add <record.json>      add one judged attempt, rewrite the README line

Logins are GitHub usernames; GitHub restricts them to letters, digits and
single hyphens, and we re-check that before writing one into the README.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "overspend.json"
README = ROOT / "README.md"
PER_DAY = 3
LOGIN_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", re.ASCII)
REPO = "https://github.com/Somay-kousis/Somay-kousis"


def load() -> dict:
    if DATA.exists():
        return json.loads(DATA.read_text())
    return {"attempts": 0, "purchases": 0, "blocked_paise": 0, "breaches": 0, "recent": []}


def allowed(login: str, now: datetime | None = None) -> bool:
    now = now or datetime.now(timezone.utc)
    since = now - timedelta(days=1)
    mine = [r for r in load()["recent"]
            if r["login"] == login and datetime.fromisoformat(r["at"]) > since]
    return len(mine) < PER_DAY


def line(d: dict) -> str:
    att = d["attempts"]
    if att == 0:
        return "**No attempts yet.** Be the first."
    rupees = d["blocked_paise"] // 100
    s = (f"**{att} attempt{'s' if att != 1 else ''} so far, "
         f"{d['breaches']} got past the limit.** ₹{rupees:,} blocked.")
    latest = [r for r in reversed(d["recent"]) if LOGIN_RE.fullmatch(r["login"])][:3]
    if latest:
        s += " Latest: " + ", ".join(f"[#{r['issue']}]({REPO}/issues/{r['issue']}) by {r['login']}" for r in latest)
    return s


def write_readme(d: dict) -> None:
    text = README.read_text()
    new, n = re.subn(r"(<!-- overspend:start -->).*?(<!-- overspend:end -->)",
                     lambda m: f"{m.group(1)}\n{line(d)}\n{m.group(2)}", text, flags=re.S)
    if n != 1:
        raise SystemExit("README is missing the overspend markers")
    README.write_text(new)


def add(record_path: str) -> None:
    rec = json.loads(Path(record_path).read_text())
    d = load()
    d["attempts"] += 1
    d["purchases"] += int(rec["purchases"])
    d["blocked_paise"] += int(rec["blocked_paise"])
    d["breaches"] += 1 if rec["breach"] else 0
    d["recent"] = (d["recent"] + [{k: rec[k] for k in ("issue", "login", "at", "breach")}])[-50:]
    d["last"] = {k: rec.get(k) for k in ("issue", "login", "paid_paise", "hops", "lines")}
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(json.dumps(d, indent=1) + "\n")
    write_readme(d)
    import receipt
    receipt.write(d)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "allowed":
        sys.exit(0 if allowed(sys.argv[2]) else 1)
    if cmd == "add":
        add(sys.argv[2])
    elif cmd == "readme":
        write_readme(load())
