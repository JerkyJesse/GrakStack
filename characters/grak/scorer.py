#!/usr/bin/env python3
"""scorer.py - the GrakStack built-in scorer.

the built-in scorer; wins pay a credit, failures charge a debt; conduct, not money.

The ledger is append-only JSON Lines at <home>/score.jsonl, one row per event:

    {"ts": "2026-10-15T12:00:00Z", "date": "2026-10-15", "kind": "ship",
     "subject": "grak", "delta": 1, "ref": "cmd: pytest -q", "note": ""}

delta is fixed by kind and is never supplied on the command line; corrections
are compensating rows with a note, and rows are never rewritten or deleted.

Credits (+1): ship, kill, red_first, receipt, debt_cleared
Debts (-1): gate_fail, stub, no_receipt, red_left_open

Commands:

    --log KIND --ref RECEIPT [--subject NAME] [--note TEXT]
    --read [--window N]     standings, all-time, last complete day, streak
    --check                 validate every row; exit 1 on any bad row
    --self-test             temp-dir fixtures; the live ledger untouched

Home: --home DIR, else $GRAKSTACK_HOME, else ~/.grakstack.
Stdlib only. No network. UTF-8. The live ledger is written only by --log.
"""

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import date, datetime, timedelta, timezone

KINDS = {"ship": 1, "kill": 1, "red_first": 1, "receipt": 1, "debt_cleared": 1,
         "gate_fail": -1, "stub": -1, "no_receipt": -1, "red_left_open": -1}
LEDGER_NAME = "score.jsonl"
DEFAULT_SUBJECT = "grak"
DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def resolve_home(flag):
    base = flag or os.environ.get("GRAKSTACK_HOME") or os.path.join(
        os.path.expanduser("~"), ".grakstack"
    )
    return os.path.abspath(os.path.expanduser(base))


def ledger_path(home):
    return os.path.join(home, LEDGER_NAME)


def iso_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def utc_today():
    return datetime.now(timezone.utc).date()


def fmt_net(n):
    return "+%d" % n if n >= 0 else "%d" % n


def build_row(kind, ref, subject=None, note=None, ts=None):
    ts = ts or iso_now()
    return {"ts": ts, "date": ts[:10], "kind": kind, "subject": subject or DEFAULT_SUBJECT,
            "delta": KINDS[kind], "ref": ref, "note": note or ""}


def append_row(home, row):
    os.makedirs(home, exist_ok=True)
    with open(ledger_path(home), "a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(row, ensure_ascii=True) + "\n")


def read_lines(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.readlines()


def parse_row(raw):
    """Return (row, None) for a valid row, else (None, reason)."""
    try:
        row = json.loads(raw)
    except ValueError:
        return None, "bad JSON"
    if not isinstance(row, dict):
        return None, "bad JSON"
    kind = row.get("kind")
    if kind not in KINDS:
        return None, "unknown kind: %s" % (kind,)
    delta = row.get("delta")
    if isinstance(delta, bool) or not isinstance(delta, int) or delta != KINDS[kind]:
        return None, "wrong delta for kind %s" % kind
    ref = row.get("ref")
    if not isinstance(ref, str) or not ref.strip():
        return None, "missing ref"
    ts = row.get("ts")
    day = row.get("date")
    day_ok = isinstance(day, str) and DAY_RE.match(day) is not None
    ts_ok = isinstance(ts, str) and len(ts) >= 10 and ts[:10] == day
    if not (day_ok and ts_ok):
        return None, "date does not match ts"
    return row, None


def collect_problems(ledger):
    """Return (problems, row_count); (None, 0) when the ledger is missing."""
    lines = read_lines(ledger)
    if lines is None:
        return None, 0
    problems = []
    for index, raw in enumerate(lines, 1):
        _row, problem = parse_row(raw.rstrip("\r\n"))
        if problem is not None:
            problems.append("line %d: %s" % (index, problem))
    return problems, len(lines)


def load_rows(ledger):
    rows = []
    skipped = 0
    lines = read_lines(ledger)
    if not lines:
        return rows, skipped
    for raw in lines:
        row, problem = parse_row(raw.rstrip("\r\n"))
        if problem is not None:
            skipped += 1
            continue
        rows.append(row)
    return rows, skipped


def tally(rows):
    stats = {}
    for row in rows:
        subject = row.get("subject") or DEFAULT_SUBJECT
        credit, debt = stats.get(subject, (0, 0))
        if row["delta"] > 0:
            credit += 1
        else:
            debt += 1
        stats[subject] = (credit, debt)
    return stats


def streak_days(rows, today):
    net_by_day = {}
    for row in rows:
        net_by_day[row["date"]] = net_by_day.get(row["date"], 0) + row["delta"]
    if not net_by_day:
        return 0
    earliest = min(net_by_day)
    day = today - timedelta(days=1)
    streak = 0
    while day.isoformat() >= earliest:
        net = net_by_day.get(day.isoformat())
        if net is None or net < 0:
            break
        streak += 1
        day -= timedelta(days=1)
    return streak


def render_read(ledger, window, today):
    out = ["scorer --read window=%dd" % window]
    rows, skipped = load_rows(ledger)
    if skipped:
        out.append("warn: %d unreadable row(s) skipped - run --check" % skipped)
    if not rows:
        out.append("no rows yet")
        return out
    start = today - timedelta(days=window - 1)
    in_window = [row for row in rows if start <= date.fromisoformat(row["date"]) <= today]
    stats = tally(in_window)
    for subject in sorted(stats, key=lambda name: (stats[name][0] - stats[name][1], name)):
        credit, debt = stats[subject]
        out.append("%s net %s (credit %d / debt %d)" % (subject, fmt_net(credit - debt), credit, debt))
    total = tally(rows)
    credit = sum(pair[0] for pair in total.values())
    debt = sum(pair[1] for pair in total.values())
    out.append("all-time net %s (credit %d / debt %d)" % (fmt_net(credit - debt), credit, debt))
    yesterday = today - timedelta(days=1)
    day_rows = [row for row in rows if row["date"] == yesterday.isoformat()]
    if day_rows:
        net = sum(row["delta"] for row in day_rows)
        out.append("day %s: %d row(s), net %s" % (yesterday.isoformat(), len(day_rows), fmt_net(net)))
    else:
        out.append("day %s: unread" % yesterday.isoformat())
    out.append("streak: %d complete day(s)" % streak_days(rows, today))
    return out


def cmd_log(args, home):
    kind = args.log
    if kind not in KINDS:
        print("scorer: unknown kind: %s" % kind, file=sys.stderr)
        print("scorer: known kinds: %s" % ", ".join(KINDS), file=sys.stderr)
        return 2
    ref = (args.ref or "").strip()
    if not ref:
        print("scorer: --log requires --ref RECEIPT", file=sys.stderr)
        return 2
    row = build_row(kind, ref, args.subject, args.note)
    append_row(home, row)
    print("scorer: logged %s %s subject=%s ref=%s date=%s"
          % (kind, fmt_net(row["delta"]), row["subject"], ref, row["date"]))
    return 0


def cmd_check(ledger):
    problems, total = collect_problems(ledger)
    if problems is None:
        print("scorer: no ledger at %s - nothing to check" % ledger)
        return 0
    if problems:
        for problem in problems:
            print(problem)
        print("scorer: check failed, %d bad row(s)" % len(problems))
        return 1
    print("scorer: ledger ok, %d row(s)" % total)
    return 0


def run_self_test():
    """Temp-dir fixtures: clean is green, every red class flips."""
    issues = 0
    today = utc_today()
    yesterday = (today - timedelta(days=1)).isoformat()
    day_before = (today - timedelta(days=2)).isoformat()
    with tempfile.TemporaryDirectory(prefix="grak-scorer-") as tmp:
        home = os.path.join(tmp, "home")
        ledger = ledger_path(home)
        clean_rows = [
            build_row("ship", "cmd: run the focused checks", "grak", ts=today.isoformat() + "T09:00:00Z"),
            build_row("receipt", "scorer.py:1", "grak", ts=yesterday + "T09:00:00Z"),
            build_row("gate_fail", "cmd: red check", "grak-clone", ts=yesterday + "T10:00:00Z"),
            build_row("stub", "lane: docs", "grak-clone", ts=day_before + "T10:00:00Z"),
        ]
        for row in clean_rows:
            append_row(home, row)
        clean_text = "".join(json.dumps(row, ensure_ascii=True) + "\n" for row in clean_rows)

        problems, total = collect_problems(ledger)
        if problems == [] and total == 4:
            print("scorer: fixture clean -> check green ok")
        else:
            issues += 1
            print("scorer: fixture clean -> check red (unexpected): %s" % (problems,))

        expected = [
            "scorer --read window=30d",
            "grak-clone net -2 (credit 0 / debt 2)",
            "grak net +2 (credit 2 / debt 0)",
            "all-time net +0 (credit 2 / debt 2)",
            "day %s: 2 row(s), net +0" % yesterday,
            "streak: 1 complete day(s)",
        ]
        rendered = render_read(ledger, 30, today)
        if rendered == expected:
            print("scorer: fixture clean -> standings and streak ok")
        else:
            issues += 1
            print("scorer: fixture clean -> render mismatch")
            for line in rendered:
                print("scorer:   got: %s" % line)

        missing = ledger_path(os.path.join(tmp, "empty-home"))
        empty_ok = collect_problems(missing) == (None, 0)
        empty_render = render_read(missing, 30, today)
        if empty_ok and empty_render == ["scorer --read window=30d", "no rows yet"]:
            print("scorer: fixture missing ledger -> no rows yet ok")
        else:
            issues += 1
            print("scorer: fixture missing ledger -> unexpected render")

        base = {"ts": today.isoformat() + "T12:00:00Z", "date": today.isoformat(), "kind": "ship",
                "subject": "grak", "delta": 1, "ref": "cmd: run the focused checks", "note": ""}
        mutations = [
            ("bad-json", '{"ts": "%sT12:00:00Z", "date":' % today.isoformat(), "bad JSON"),
            ("unknown-kind", dict(base, kind="bonus"), "unknown kind"),
            ("wrong-delta", dict(base, kind="receipt", delta=-1), "wrong delta"),
            ("bool-delta", dict(base, delta=True), "wrong delta"),
            ("missing-ref", dict(base, ref=None), "missing ref"),
            ("date-ts-mismatch", dict(base, date="1999-01-01"), "date does not match ts"),
        ]
        for name, bad, fragment in mutations:
            bad_text = bad if isinstance(bad, str) else json.dumps(bad, ensure_ascii=True)
            with open(ledger, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(clean_text + bad_text + "\n")
            problems, _total = collect_problems(ledger)
            if problems is None:
                issues += 1
                print("scorer: mutation %s -> ledger unreadable" % name)
            elif len(problems) == 1 and fragment in problems[0]:
                print("scorer: mutation %s -> check red ok" % name)
            elif problems:
                issues += 1
                print("scorer: mutation %s -> red for the wrong reason: %s" % (name, problems))
            else:
                issues += 1
                print("scorer: mutation %s -> check still green" % name)

    if issues:
        print("scorer: self-test failed, %d issue(s)" % issues)
        return 1
    print("scorer: self-test ok")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="scorer.py",
        description="GrakStack built-in scorer: the append-only conduct ledger.",
    )
    parser.add_argument("--home", metavar="DIR", help="base dir (default: $GRAKSTACK_HOME or ~/.grakstack)")
    parser.add_argument("--log", metavar="KIND", help="append one conduct row; kind from the fixed list")
    parser.add_argument("--ref", metavar="RECEIPT",
                        help="the receipt: command, file:line, or pinned check (needed with --log)")
    parser.add_argument("--subject", metavar="NAME",
                        help="who the row counts for (default: %s)" % DEFAULT_SUBJECT)
    parser.add_argument("--note", metavar="TEXT", help="free text note, kept as written")
    parser.add_argument("--read", action="store_true",
                        help="render standings, all-time, last complete day, streak")
    parser.add_argument("--window", type=int, default=30, metavar="N",
                        help="days of standings to render (default: 30)")
    parser.add_argument("--check", action="store_true", help="validate the ledger; exit 1 on any bad row")
    parser.add_argument("--self-test", action="store_true",
                        help="run temp-dir fixtures; the live ledger is untouched")
    args = parser.parse_args(argv)

    surface = [bool(args.log), args.read, args.check, args.self_test]
    if sum(surface) != 1:
        parser.print_usage(sys.stderr)
        print("scorer: pick exactly one of --log, --read, --check, --self-test", file=sys.stderr)
        return 2
    if args.self_test:
        return run_self_test()
    home = resolve_home(args.home)
    if args.log:
        return cmd_log(args, home)
    ledger = ledger_path(home)
    if args.read:
        if args.window < 1:
            print("scorer: --window must be 1 or more", file=sys.stderr)
            return 2
        for line in render_read(ledger, args.window, utc_today()):
            print(line)
        return 0
    return cmd_check(ledger)


if __name__ == "__main__":
    sys.exit(main())
