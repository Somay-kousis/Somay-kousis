"""Judge one "try to make my agent overspend" attempt with Pocket Change's real checks.

The setup is fixed. I give my shopping agent Rs 1,500 for groceries, valid for
one hour, and it may hand work on to at most 2 more sub-agents. A visitor opens
an issue (template .github/ISSUE_TEMPLATE/overspend.yml) that describes:

  * sub-agents: each line is a budget in rupees and the tools that sub-agent
    claims, e.g. "50000 pay.groceries pay.electronics". Each one is appended to
    the token as a Biscuit block, exactly as Pocket Change attenuates.
  * purchases: each line is a tool and an amount, e.g. "pay.groceries 900".
    Every purchase is checked against the whole token chain, then reserved on
    one ledger that holds the Rs 1,500 ceiling across all of them.
  * minutes from now: when the purchases happen.

No model runs and nothing is charged. The verdicts come from pocketchange.token
(Biscuit Datalog checks) and pocketchange.ledger.MemoryLedger, imported from the
Pocket-Change repo at a pinned commit.

Security: the issue body is attacker-controlled. It is read from the event JSON
file, parsed with strict ASCII patterns, and never echoed back except as the
parsed numbers and tool names. Nothing from it reaches a shell.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pocketchange import identity, token
from pocketchange.ledger import InsufficientBudget, MemoryLedger
from pocketchange.policy import RUPEE, Grant, Operation

CAP_RUPEES = 1500
ALLOWED_TOOL = "pay.groceries"
MAX_DEPTH = 3          # me -> agent is depth 1, so 2 more hand-offs fit
MAX_HOPS = 5
MAX_BUYS = 10
TOOL_RE = re.compile(r"[a-z][a-z0-9._-]{0,31}", re.ASCII)
AMOUNT_RE = re.compile(r"-?\d{1,9}(?:\.\d{1,2})?", re.ASCII)


@dataclass
class Attempt:
    hops: list[tuple[int, tuple[str, ...]]] = field(default_factory=list)   # (budget paise, tools)
    buys: list[tuple[str, int]] = field(default_factory=list)               # (tool, amount paise)
    minutes: int = 0
    ignored: list[str] = field(default_factory=list)


@dataclass
class Result:
    line: str
    verdict: str          # "paid" | "blocked" | "refused"
    reason: str
    amount_paise: int
    tool: str


def _section(body: str, heading: str) -> str:
    m = re.search(rf"^###\s*{re.escape(heading)}\s*$(.*?)(?=^###\s|\Z)", body, re.M | re.S)
    if not m:
        return ""
    text = m.group(1).strip()
    return "" if text == "_No response_" else text


def _paise(raw: str) -> int | None:
    if not AMOUNT_RE.fullmatch(raw):
        return None
    neg = raw.startswith("-")
    whole, _, frac = raw.lstrip("-").partition(".")
    value = int(whole) * RUPEE + int((frac + "00")[:2])
    return -value if neg else value


def parse(body: str) -> Attempt:
    a = Attempt()
    for n, line in enumerate(_section(body, "Sub-agents").splitlines(), 1):
        parts = line.strip().strip("`").split()
        if not parts:
            continue
        if len(a.hops) >= MAX_HOPS:
            a.ignored.append(f"sub-agent line {n}: more than {MAX_HOPS}")
            continue
        budget = _paise(parts[0])
        tools = tuple(t for t in parts[1:] if TOOL_RE.fullmatch(t))
        if budget is None or not tools or len(tools) != len(parts) - 1:
            a.ignored.append(f"sub-agent line {n}: expected `<rupees> <tool> [tool...]`")
            continue
        a.hops.append((budget, tools))
    for n, line in enumerate(_section(body, "Purchases").splitlines(), 1):
        parts = line.strip().strip("`").split()
        if not parts:
            continue
        if len(a.buys) >= MAX_BUYS:
            a.ignored.append(f"purchase line {n}: more than {MAX_BUYS}")
            continue
        amount = _paise(parts[-1]) if len(parts) == 2 else None
        if amount is None or not TOOL_RE.fullmatch(parts[0]):
            a.ignored.append(f"purchase line {n}: expected `<tool> <rupees>`")
            continue
        a.buys.append((parts[0], amount))
    raw_min = _section(body, "Minutes from now")
    if re.fullmatch(r"-?\d{1,6}", raw_min, re.ASCII):
        a.minutes = max(-100000, min(100000, int(raw_min)))
    elif raw_min:
        a.ignored.append("minutes: not a whole number, used 0")
    return a


def _explain(err: str, hops: list[tuple[int, tuple[str, ...]]]) -> str:
    """Turn a Biscuit failure into plain sentences, one per broken rule."""
    found = re.findall(r"Check n°\d+ in block n°(\d+): check if (\w+)", err)
    if not found:
        return "the token refused it"
    order = {"tool": 0, "time": 1, "depth": 2, "budget": 3}
    said, out = set(), []
    for block, kind in sorted(((int(b), k) for b, k in found), key=lambda bk: (order.get(bk[1], 9), bk[0])):
        if kind == "tool":
            msg = ("I only allowed pay.groceries" if block <= 1
                   else f"sub-agent {block - 1} did not get that tool")
        elif kind == "budget":
            msg = (f"over my ₹{CAP_RUPEES:,} limit" if block <= 1
                   else f"over sub-agent {block - 1}'s own ₹{hops[block - 2][0] / RUPEE:,.0f} limit")
        elif kind == "depth":
            msg = f"too many hand-offs: {len(hops) + 1} deep, {MAX_DEPTH} allowed"
        elif kind == "time":
            msg = "the hour was up"
        else:
            msg = "a check failed"
        if msg not in said:
            said.add(msg)
            out.append(msg)
    return "; ".join(out)


def judge(a: Attempt, now: datetime | None = None) -> tuple[list[Result], dict]:
    now = now or datetime.now(timezone.utc)
    expires = now + timedelta(hours=1)
    me = identity.ephemeral()
    root = token.mint(me, budget_paise=CAP_RUPEES * RUPEE, max_depth=MAX_DEPTH, expires=expires)
    tok = token.attenuate(root, to="aip:web:example.com/shopping-agent",
                          grant=Grant((ALLOWED_TOOL,), CAP_RUPEES * RUPEE, expires),
                          context="weekly groceries")
    for i, (budget, tools) in enumerate(a.hops, 1):
        try:
            tok = token.attenuate(tok, to=f"aip:web:example.com/sub-agent-{i}",
                                  grant=Grant(tools, budget), context=f"visitor sub-agent {i}")
        except ValueError as exc:   # e.g. a negative budget: Grant refuses it
            return [Result(f"sub-agent {i}", "refused", f"Pocket Change refused the grant: {exc}", 0, "")], {}

    ledger = MemoryLedger()
    mandate = token.mandate_id(tok)
    ledger.open(mandate, CAP_RUPEES * RUPEE)
    at = now + timedelta(minutes=a.minutes)
    depth = 1 + len(a.hops)
    results: list[Result] = []
    for i, (tool, amount) in enumerate(a.buys, 1):
        label = f"{tool} ₹{amount / RUPEE:,.2f}".replace(".00", "")
        try:
            op = Operation(tool, amount, depth=depth, at=at)
        except ValueError as exc:
            results.append(Result(label, "refused", f"Pocket Change refused the operation: {exc}", amount, tool))
            continue
        try:
            token.verify(tok, op)
        except token.Denied as exc:
            results.append(Result(label, "blocked", _explain(str(exc), a.hops), amount, tool))
            continue
        try:
            res = ledger.reserve(mandate, amount, idempotency_key=f"buy-{i}")
        except InsufficientBudget as exc:
            results.append(Result(label, "blocked",
                                  f"the ledger only had ₹{exc.available / RUPEE:,.0f} of ₹{CAP_RUPEES:,} left", amount, tool))
            continue
        except ValueError as exc:
            results.append(Result(label, "refused", f"Pocket Change refused the reservation: {exc}", amount, tool))
            continue
        ledger.commit(res.id)
        results.append(Result(label, "paid", "inside every limit", amount, tool))

    paid = [r for r in results if r.verdict == "paid"]
    total = sum(r.amount_paise for r in paid)
    # A breach is anything the setup forbids that still got paid.
    breach = (total > CAP_RUPEES * RUPEE
              or any(r.tool != ALLOWED_TOOL for r in paid)
              or (paid and (at > expires or depth > MAX_DEPTH)))
    return results, {"paid_paise": total, "breach": bool(breach), "depth": depth, "at_minutes": a.minutes}


def comment(a: Attempt, results: list[Result], summary: dict) -> str:
    lines = ["**Pocket Change checked your attempt.**", ""]
    if summary.get("breach"):
        lines += ["**You got past the limit.** That is a real bug, and I will fix it and credit you. Thank you.", ""]
    elif results and all(r.verdict != "paid" for r in results):
        lines += ["Nothing got through.", ""]
    else:
        lines += [f"Paid ₹{summary.get('paid_paise', 0) / RUPEE:,.0f} of ₹{CAP_RUPEES:,}. Nothing went over.", ""]
    if a.hops:
        chain = " → ".join(f"₹{b / RUPEE:,.0f} [{', '.join(t)}]" for b, t in a.hops)
        lines += [f"Sub-agents: {chain}", ""]
    if results:
        lines += ["| purchase | result | why |", "|---|---|---|"]
        lines += [f"| `{r.line}` | {r.verdict} | {r.reason} |" for r in results]
    else:
        lines += ["No purchases I could read. Each line should look like `pay.groceries 900`."]
    if a.ignored:
        lines += ["", "Skipped: " + "; ".join(a.ignored)]
    lines += ["", "<sub>Checks: Biscuit token blocks (tool, per-payment budget, depth, time) "
              "and one ledger holding the ₹1,500 ceiling across all purchases. "
              "Code: [Pocket Change](https://github.com/Somay-kousis/Pocket-Change).</sub>"]
    return "\n".join(lines)


def main(event_path: str, out_dir: str) -> None:
    event = json.loads(Path(event_path).read_text())
    issue = event["issue"]
    a = parse(issue.get("body") or "")
    results, summary = judge(a)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "comment.md").write_text(comment(a, results, summary))
    record = {
        "issue": issue["number"],
        "login": issue["user"]["login"],
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "purchases": len(results),
        "paid_paise": summary.get("paid_paise", 0),
        "blocked_paise": sum(r.amount_paise for r in results if r.verdict != "paid" and r.amount_paise > 0),
        "breach": summary.get("breach", False),
    }
    (out / "record.json").write_text(json.dumps(record))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
