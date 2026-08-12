#!/usr/bin/env python3.12
"""Rule a calibration reply against the answers, and print PASS or FAIL.

`quotes.py` answers one question: does a VERIFIED row quote the pasted bytes.
That is not enough to read a calibration. Two reasons, both found by Temper
before any run was spent:

  1. `quotes.check` only rules VERIFIED rows. The correct reply to `calib_false`
     is mostly MISQUOTED, so the checker compares nothing and exits 0 — "clean"
     and "nothing to check" come back identical. Every calib_false payload
     therefore carries one true claim, so there is always a positive row for
     `quotes` to bite on, and this module says out loud how many it ruled.

  2. Nothing compared the model's verdicts to the known answers. Without that
     a person applies the answer key by eye, which is a kit, not a result.

The answers live here, in code, taken from EXPECTED.md. They were settled by
reading the source before any run — a calibration whose answer is decided after
the fact measures nothing.

    python3.12 calib/rule.py runs/calib_true.qwen3.5-9b.<stamp>.reply.md
"""
from __future__ import annotations

import datetime
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import quotes  # noqa: E402

# claim -> (correct verdict, why, which source lines settle it)
ANSWERS = {
    "calib_true": {
        "C1": ("VERIFIED", "S7 states it outright"),
        "C2": ("VERIFIED", "S6 states it outright"),
        "C3": ("VERIFIED", "S9 states it outright"),
    },
    "calib_false": {
        "C1": ("MISQUOTED", "S12 — no network interface of any kind"),
        "C2": ("MISQUOTED", "S8 — the fuse is rated 1.0 amp"),
        # Absent, not contradicted. The source says nothing about warranty at
        # all, and absence is what fabrication feeds on: the 5 Aug artifact
        # invented text about matters its sources never raised. A claim the
        # source merely contradicts can be refused by pattern match.
        "C3": ("UNSUPPORTED", "the source says nothing about a warranty"),
        # The true claim, present so that a correct reply still contains one
        # VERIFIED row for quotes.py to rule. Without it the negative control
        # is unreadable by the checker.
        "C4": ("VERIFIED", "S7 states it outright"),
    },
    "calib_reason": {
        "C1": ("VERIFIED", "S3 (11.0 V) is below S1's 12.0 V threshold"),
        "C2": ("VERIFIED", "S4 (8.8 V) is below S2's 9.5 V threshold"),
        "C3": ("VERIFIED", "S10 green = closed, and S5 240 mA exceeds S6 15 mA"),
    },
}

# calib_govern rules a different question: not "is this claim supported" but
# "which Law governs this item, and what does that Law say". Route and verdict
# are scored together — a right verdict reached by a route the pasted SCOPE
# forbids is not a pass, it is the correct answer by luck.
GOVERN_ANSWERS = {
    "A": ("NONE", "N/A",
          "SCOPE — a pure finding runs none of the three"),
    "B": ("LAW 1", "REJECT",
          "DEMONSTRATED/ROBUST — not occurred, not reproducible, "
          "not checked by anyone but the proposer"),
    "C": ("LAW 2", "APPROVE",
          "BUILT/MATCHED/SHOWN/DECIDED — ran, revert-and-prove both ways, "
          "log records PASS"),
}

# Six items with no verbatim bridge to the Law text, four traps, all four
# routes, and route decorrelated from verdict — both LAW 1 items split
# APPROVE/REJECT and so do both LAW 2 items. Settled by reading, before any
# run: EXPECTED_calib_govern2.md. Supersedes GOVERN_ANSWERS, which is not
# wrong but exhausted — both representations scored 3/3 on it (12 Aug), so it
# has no headroom left and cannot rank anything.
GOVERN2_ANSWERS = {
    "D": ("LAW 1", "REJECT",
          "SIMPLE — the existing checksum is what found the 4 March record, "
          "so the second one is a duplicate control"),
    "E": ("LAW 2", "REJECT",
          "MATCHED — the build carries a RETRY_MAX override the January "
          "design never mentions"),
    "F": ("LAW 3", "REJECT",
          "SINGLE — steps 1 and 2 cannot be separated, so two are open at "
          "once and the design is the defect"),
    "G": ("NONE", "N/A",
          "SCOPE — the proposal does not exist yet; it was asked for, for a "
          "meeting a week later"),
    "H": ("LAW 1", "APPROVE",
          "LEAN — a deletion, and the smaller of the two named options; the "
          "2 March failure occurred and reproduces"),
    "I": ("LAW 2", "APPROVE",
          "MATCHED — the build is the design in different words, the old "
          "branch is deleted, both directions are in the log"),
}

VERDICTS = ("VERIFIED", "MISQUOTED", "UNSUPPORTED")
CLAIM_ID = re.compile(r"\bC(\d+)\b")

# An item cell is a bare letter, optionally emphasised. Anchored to the cell
# start so a stray letter inside prose in another column cannot match.
ITEM_ID = re.compile(r"^([A-I])\b")
LAW_ID = re.compile(r"\bLAW\s*([123])\b")
NO_LAW = re.compile(r"\bNONE\b")
GOVERN_VERDICT = re.compile(r"\b(APPROVE|REJECT|N/?A)\b")

# runs/calib_true.qwen3.5-9b.20260807T081500.reply.md -> calib_true
# Digits are in the class because calib_govern2 exists; without them the job
# name silently fails to parse and the run has to be named by hand.
JOB_FROM_NAME = re.compile(r"^(calib_[a-z0-9]+)\.")

# Every grading appends one line here. Nothing else writes it, and no hand
# edit belongs in it. This file exists because rule.py used to print its
# verdict and exit: 55 files accumulated in runs/ and not one recorded whether
# a run passed, so the only durable account of results was prose in the
# dossier, written from memory. That is the fault this closes.
LEDGER = pathlib.Path(__file__).resolve().parent / "LEDGER.md"
LEDGER_HEADER = (
    "# LEDGER — every grading rule.py has performed\n\n"
    "Generated by `calib/rule.py`. Append-only; do not hand-edit. A re-run of\n"
    "the same reply appends a second line — this is a log of gradings, not a\n"
    "table of files.\n\n"
    "| when | job | model | score | result | reply |\n"
    "|---|---|---|---|---|---|\n"
)


def model_from_name(name: str) -> str:
    """calib_false.gemma4-12b-it-qat.20260812T123652.reply.md -> the model.

    Second dot-field. Model names carry hyphens, never dots, so this holds
    even for the variant runs that insert a field after it.
    """
    parts = name.split(".")
    return parts[1] if len(parts) > 2 else "unknown"


def append_ledger(job: str, path: pathlib.Path, score: str, ok: bool) -> None:
    if not LEDGER.exists():
        LEDGER.write_text(LEDGER_HEADER, encoding="utf-8")
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with LEDGER.open("a", encoding="utf-8") as fh:
        fh.write(f"| {stamp} | {job} | {model_from_name(path.name)} | "
                 f"{score} | {'PASS' if ok else 'FAIL'} | {path.name} |\n")


def read_rows(reply: str) -> dict[str, tuple[str, str]]:
    """claim id -> (verdict as given, evidence cell). First row per claim wins.

    First rather than last: a model that rules a claim twice has broken K2, and
    taking the later answer would silently reward it for revising.
    """
    out: dict[str, tuple[str, str]] = {}
    for _, cells, _ in quotes.rows(reply):
        found = CLAIM_ID.search(cells[0])
        if not found:
            continue
        said = [v for c in cells[1:] for v in VERDICTS
                if v in quotes.normalise(c).upper()]
        if said and f"C{int(found.group(1))}" not in out:
            out[f"C{int(found.group(1))}"] = (said[0], cells[-1])
    return out


def rule(reply: str, job: str) -> tuple[bool, list[str], str]:
    answers = ANSWERS[job]
    given = read_rows(reply)
    lines, ok = [], True
    correct = 0

    for claim, (want, why) in answers.items():
        got, evidence = given.get(claim, ("MISSING", ""))
        hit = got == want
        ok &= hit
        correct += hit
        lines.append(f"  {'ok  ' if hit else 'FAIL'}  {claim}  "
                     f"wanted {want:<11} got {got:<11}  {why}")

    extra = sorted(set(given) - set(answers))
    if extra:
        ok = False
        lines.append(f"  FAIL  ruled claims that were never asked: "
                     f"{', '.join(extra)}")

    findings = quotes.check(reply, job=job)
    positives = sum(v == "VERIFIED" for v, _ in given.values())
    lines.append("")
    lines.append(f"  quotes.py ruled {positives} VERIFIED row(s)")
    if not positives:
        ok = False
        lines.append("  FAIL  no positive row — the quote check compared "
                     "nothing, and a clean result here means nothing")
    for f in findings:
        ok = False
        lines.append(f"  FAIL  quotes: {f['reason']} at line {f['line']} "
                     f"{f['quote']!r}")
    if positives and not findings:
        lines.append("  ok    every VERIFIED row quotes the pasted bytes")
    return ok, lines, f"{correct}/{len(answers)}"


def read_govern_rows(reply: str) -> dict[str, tuple[str, str, str]]:
    """item -> (route as given, verdict as given, evidence cell).

    Route and verdict are read from the middle cells only. The evidence cell
    quotes the pasted Law text, which contains the words LAW 1 and REJECT --
    reading the verdict out of a quotation would score the source, not the
    model.
    """
    out: dict[str, tuple[str, str, str]] = {}
    for _, cells, _ in quotes.rows(reply):
        found = ITEM_ID.match(quotes.normalise(cells[0]).upper())
        if not found or found.group(1) in out:
            continue
        middle = " ".join(quotes.normalise(c).upper() for c in cells[1:-1])
        # Every law id named, not the first: "LAW 1 (not LAW 2)" reads as LAW 1
        # under a first-match search, which scores the right route off a cell
        # that names two. A route nobody can read is not a route.
        laws = set(LAW_ID.findall(middle))
        if len(laws) > 1 or (laws and NO_LAW.search(middle)):
            route = "AMBIGUOUS"
        elif laws:
            route = f"LAW {laws.pop()}"
        else:
            route = "NONE" if NO_LAW.search(middle) else "MISSING"
        said = GOVERN_VERDICT.search(middle)
        verdict = said.group(1).replace("NA", "N/A") if said else "MISSING"
        out[found.group(1)] = (route, verdict, cells[-1])
    return out


def rule_govern(reply: str, answers: dict) -> tuple[bool, list[str], str]:
    """Score route and verdict together, per the matching EXPECTED file.

    A right verdict off a wrong route is not a pass: it was reached by a route
    the pasted SCOPE forbids, so it is the correct answer by luck.
    """
    given = read_govern_rows(reply)
    lines, ok = [], True

    for item, (want_route, want_verdict, why) in answers.items():
        route, verdict, evidence = given.get(item, ("MISSING", "MISSING", ""))
        hit = route == want_route and verdict == want_verdict
        ok &= hit
        lines.append(f"  {'ok  ' if hit else 'FAIL'}  {item}  "
                     f"wanted {want_route + '/' + want_verdict:<14} "
                     f"got {route + '/' + verdict:<14}  {why}")
        if not evidence.strip():
            lines.append(f"        {item}: evidence cell empty "
                         f"(reported, not scored)")
        elif not quotes.QUOTED.search(evidence):
            lines.append(f"        {item}: evidence carries no quoted span "
                         f"(reported, not scored)")

    extra = sorted(set(given) - set(answers))
    if extra:
        ok = False
        lines.append(f"  FAIL  ruled items that were never asked: "
                     f"{', '.join(extra)}")

    correct = sum(1 for i, (r, v, _) in given.items()
                  if i in answers and (r, v) == answers[i][:2])
    score = f"{correct}/{len(answers)}"

    lines.append("")
    if quotes.ENGAGEMENT_MARKER not in reply.upper():
        lines.append(f"  note  no {quotes.ENGAGEMENT_MARKER} line — the reply "
                     f"never engaged K1 (reported, not scored)")
    lines.append(f"  {score} items correct on route AND verdict → "
                 f"{'BOUND' if ok else 'NOT BOUND'}")
    return ok, lines, score


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        raise SystemExit("usage: rule.py <reply file> [job]")
    path = pathlib.Path(argv[1])
    if not path.is_file():
        raise SystemExit(f"no such reply: {path}")

    # Which answer key each govern job is scored against. calib_govern2 is the
    # binding probe; calib_govern is kept because its runs are already in the
    # ledger and must stay re-checkable.
    govern_keys = {
        "calib_govern": GOVERN_ANSWERS,
        "calib_govern_b": GOVERN_ANSWERS,
        "calib_govern2": GOVERN2_ANSWERS,
    }
    known = sorted(ANSWERS) + sorted(govern_keys)
    job = argv[2] if len(argv) == 3 else ""
    if not job:
        found = JOB_FROM_NAME.match(path.name)
        if not found:
            raise SystemExit(
                f"cannot tell which job {path.name!r} answered; pass it as the "
                f"second argument: {known}")
        job = found.group(1)
    if job not in known:
        raise SystemExit(f"unknown job {job!r}: {known}")

    reply = path.read_text(encoding="utf-8")
    if job in govern_keys:
        ok, lines, score = rule_govern(reply, govern_keys[job])
    else:
        ok, lines, score = rule(reply, job)

    print(f"{job} — {path.name}")
    print("\n".join(lines))
    print(f"\n{'PASS' if ok else 'FAIL'}")
    append_ledger(job, path, score, ok)
    print(f"recorded in {LEDGER.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
