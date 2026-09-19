#!/usr/bin/env python3
"""GRAK LEVEL 100 CREDENTIAL EXAM.

Runner and validator for mcq_bank.json (20 papers, 5 questions each,
100 questions, 100 XP max). Stdlib only. No network. No deps.

Usage:
    python exam.py --check       validate the bank structure, answer keys, and
                                 GRAK_CREDENTIALS.md parity
    python exam.py --self-test   run the scoring engine over the answer key
    python exam.py --list        list the papers
    python exam.py               take the exam, paper by paper
    python exam.py --paper cs-01 take one paper

Rules: 1 correct answer = 1 XP. A paper passes at 4 of 5; a
5/5 paper is OP. 100/100 XP = GOD LEVEL 100 OP.
"""

import argparse
import json
import os
import re
import sys

BANK_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcq_bank.json")
LETTERS = "ABCD"
SIDES = ("rock-logic", "mark-making")

RANKS = (
    (100, "GOD LEVEL 100 OP - OBSIDIAN BRAIN"),
    (80, "Cave Elder"),
    (60, "Rock Sage"),
    (40, "Stone Smith"),
    (20, "Pebble Apprentice"),
    (0, "Larva"),
)


def rank_for(xp):
    for floor, name in RANKS:
        if xp >= floor:
            return name
    return RANKS[-1][1]


def load_bank(path=BANK_PATH):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def validate(bank):
    """Return a list of problems. Empty list means the bank is valid."""
    errors = []
    if bank.get("schema") != 1:
        errors.append("schema must be 1")

    rules = bank.get("rules", {})
    if rules.get("answers_per_paper") != 5:
        errors.append("rules.answers_per_paper must be 5")
    if rules.get("pass_mark_per_paper") != 4:
        errors.append("rules.pass_mark_per_paper must be 4")
    if rules.get("xp_per_answer") != 1:
        errors.append("rules.xp_per_answer must be 1")
    if rules.get("max_xp") != 100:
        errors.append("rules.max_xp must be 100")

    papers = bank.get("papers", [])
    if len(papers) != 20:
        errors.append("expected 20 papers, found %d" % len(papers))

    seen_papers = set()
    seen_questions = set()
    total_questions = 0
    total_xp = 0

    for paper in papers:
        pid = paper.get("id", "?")
        if not pid or pid in seen_papers:
            errors.append("paper id missing or duplicated: %r" % pid)
        seen_papers.add(pid)

        if paper.get("side") not in SIDES:
            errors.append("%s: side must be one of %s" % (pid, ", ".join(SIDES)))
        for field in ("caveman", "real", "proof"):
            if not str(paper.get(field, "")).strip():
                errors.append("%s: empty field %s" % (pid, field))

        xp = paper.get("xp")
        if not isinstance(xp, int) or xp <= 0:
            errors.append("%s: xp must be a positive int" % pid)
        else:
            total_xp += xp

        questions = paper.get("questions", [])
        if len(questions) != rules.get("answers_per_paper", 5):
            errors.append("%s: expected %d questions, found %d"
                          % (pid, rules.get("answers_per_paper", 5), len(questions)))

        for q in questions:
            qid = q.get("id", "?")
            if not qid or qid in seen_questions:
                errors.append("question id missing or duplicated: %r" % qid)
            seen_questions.add(qid)
            total_questions += 1

            if not str(q.get("prompt", "")).strip():
                errors.append("%s: empty prompt" % qid)
            options = q.get("options", [])
            if not isinstance(options, list) or len(options) != 4:
                errors.append("%s: needs exactly 4 options" % qid)
            elif any(not str(opt).strip() for opt in options):
                errors.append("%s: has an empty option" % qid)
            if len(set(map(str, options))) != len(options):
                errors.append("%s: duplicate options" % qid)
            answer = q.get("answer")
            if not isinstance(answer, int) or not (0 <= answer <= 3):
                errors.append("%s: answer must be an int 0..3" % qid)
            if not str(q.get("why", "")).strip():
                errors.append("%s: missing why" % qid)

    if total_questions != 100:
        errors.append("expected 100 questions, found %d" % total_questions)
    if total_xp != rules.get("max_xp"):
        errors.append("paper xp sums to %d, rules.max_xp is %r"
                      % (total_xp, rules.get("max_xp")))

    cred_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GRAK_CREDENTIALS.md")
    try:
        with open(cred_path, "r", encoding="utf-8") as fh:
            credentials = fh.read()
        record_ids = set(re.findall(r"^\|\s*((?:CS|AR)\d{1,2})\s*\|", credentials, re.M))
        if len(record_ids) != 20:
            errors.append("expected 20 credentials papers, found %d" % len(record_ids))
        bank_ids = set()
        for paper in papers:
            parts = str(paper.get("id", "")).split("-")
            if len(parts) == 2 and parts[0] in ("cs", "ar") and parts[1].isdigit():
                bank_ids.add(parts[0].upper() + str(int(parts[1])))
        for missing in sorted(record_ids - bank_ids):
            errors.append("credentials paper %s has no bank paper" % missing)
        for orphan in sorted(bank_ids - record_ids):
            errors.append("bank paper %s has no credentials line" % orphan)
    except OSError:
        errors.append("GRAK_CREDENTIALS.md missing")

    return errors


def score_paper(paper, picked):
    """picked: list of answer indexes, one per question (None = skipped)."""
    correct = 0
    for question, choice in zip(paper["questions"], picked):
        if choice == question["answer"]:
            correct += 1
    return correct


def paper_passed(correct, pass_mark):
    return correct >= pass_mark


def ask(question):
    while True:
        raw = input("  %s? [A-D, or q to quit] " % question["id"]).strip().upper()
        if raw in ("Q", "QUIT"):
            return None
        if len(raw) == 1 and raw in LETTERS:
            return LETTERS.index(raw)
        if raw.isdigit() and 1 <= int(raw) <= 4:
            return int(raw) - 1
        print("  Answer A, B, C, or D.")


def take_paper(paper):
    print("")
    print("=" * 68)
    print("%s  |  %s" % (paper["id"].upper(), paper["caveman"]))
    print("Real: %s" % paper["real"])
    print("-" * 68)
    picked = []
    for i, question in enumerate(paper["questions"], 1):
        print("")
        print("Q%d. %s" % (i, question["prompt"]))
        for j, option in enumerate(question["options"]):
            print("  %s) %s" % (LETTERS[j], option))
        choice = ask(question)
        if choice is None:
            picked.append(None)
            break
        picked.append(choice)
        verdict = "ok" if choice == question["answer"] else "no"
        print("  -> %s. %s" % (verdict, question["why"]))
    return picked


def run_exam(bank, only=None, answers=None, quiet=False):
    """answers: optional dict qid -> index, used to simulate a run.

    Returns (xp, papers_passed, papers_seen, perfect_papers). A perfect
    paper is 5/5 and earns the OP mark.
    """
    rules = bank["rules"]
    pass_mark = rules["pass_mark_per_paper"]
    xp = 0
    passed = 0
    perfect = 0
    papers = [p for p in bank["papers"] if only is None or p["id"] == only]
    for paper in papers:
        if answers is None:
            picked = take_paper(paper)
        else:
            picked = [answers.get(q["id"]) for q in paper["questions"]]
        correct = score_paper(paper, picked)
        ok = paper_passed(correct, pass_mark)
        xp += correct
        if ok:
            passed += 1
        if correct == len(paper["questions"]):
            perfect += 1
        if not quiet:
            if ok and correct == len(paper["questions"]):
                mark = "PASS (OP)"
            elif ok:
                mark = "PASS"
            else:
                mark = "IN PROGRESS"
            print("")
            print("%s: %d/%d - %s" % (paper["id"], correct, len(paper["questions"]), mark))
        if answers is None and any(c is None for c in picked):
            print("Left the fire circle early.")
            break
    return xp, passed, len(papers), perfect


def self_test(bank):
    rules = bank["rules"]
    pass_mark = rules["pass_mark_per_paper"]

    key = {}
    for paper in bank["papers"]:
        for question in paper["questions"]:
            key[question["id"]] = question["answer"]

    xp, passed, total, perfect = run_exam(bank, answers=key, quiet=True)
    if (xp, passed, total, perfect) != (100, 20, 20, 20):
        print("self-test FAILED: got %d XP, %d/%d papers, %d perfect"
              % (xp, passed, total, perfect))
        return 1
    if "OP" not in rank_for(xp):
        print("self-test FAILED: top rank lost the OP mark")
        return 1

    # Boundary: 4 of 5 passes a paper, 3 of 5 does not.
    paper = bank["papers"][0]
    four = [q["answer"] for q in paper["questions"]]
    four[0] = (four[0] + 1) % 4
    if not paper_passed(score_paper(paper, four), pass_mark):
        print("self-test FAILED: 4/5 did not pass %s" % paper["id"])
        return 1
    three = list(four)
    three[1] = (three[1] + 1) % 4
    if paper_passed(score_paper(paper, three), pass_mark):
        print("self-test FAILED: 3/5 passed %s" % paper["id"])
        return 1

    print("self-test ok: 100/100 XP, 20/20 papers, 20 OP papers, rank %s" % rank_for(xp))
    print("boundary ok: 4/5 passes, 3/5 held in progress")
    return 0


def cmd_check(bank):
    errors = validate(bank)
    if errors:
        print("check FAILED:")
        for err in errors:
            print("  - %s" % err)
        return 1
    questions = sum(len(p["questions"]) for p in bank["papers"])
    xp = sum(p["xp"] for p in bank["papers"])
    print(
        "check ok: %d papers, %d questions, %d XP max; 20/20 match GRAK_CREDENTIALS.md"
        % (len(bank["papers"]), questions, xp)
    )
    return 0


def cmd_list(bank):
    print("GRAK LEVEL 100 OP CREDENTIAL EXAM - 20 papers")
    for paper in bank["papers"]:
        print("  %-6s %-12s %s" % (paper["id"], paper["side"], paper["caveman"]))
        print("         real: %s" % paper["real"])
    return 0


def main():
    parser = argparse.ArgumentParser(description="Grak Level 100 OP credential exam.")
    parser.add_argument("--check", action="store_true", help="validate the question bank")
    parser.add_argument("--self-test", action="store_true", help="run the scoring engine over the answer key")
    parser.add_argument("--list", action="store_true", help="list the papers")
    parser.add_argument("--paper", metavar="ID", help="take a single paper, e.g. cs-01")
    args = parser.parse_args()

    bank = load_bank()

    if args.check:
        return cmd_check(bank)
    if args.self_test:
        return self_test(bank)
    if args.list:
        return cmd_list(bank)

    errors = validate(bank)
    if errors:
        print("Bank is invalid; refusing to run.")
        for err in errors:
            print("  - %s" % err)
        return 1

    if args.paper and args.paper not in [p["id"] for p in bank["papers"]]:
        print("No such paper: %s (try --list)" % args.paper)
        return 1

    print("GRAK LEVEL 100 OP CREDENTIAL EXAM")
    print("20 papers, 5 questions each. 4/5 passes a paper; 5/5 is OP. 100/100 XP is GOD LEVEL 100 OP.")
    print("Answer with A, B, C, or D. q quits.")
    try:
        xp, passed, total, perfect = run_exam(bank, only=args.paper)
    except (EOFError, KeyboardInterrupt):
        print("")
        print("Left the fire circle early.")
        return 130

    print("")
    print("=" * 68)
    print("XP: %d of 100  |  papers passed: %d of %d  |  OP papers: %d  |  rank: %s"
          % (xp, passed, total, perfect, rank_for(xp)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
