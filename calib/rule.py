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

VERDICTS = ("VERIFIED", "MISQUOTED", "UNSUPPORTED")
CLAIM_ID = re.compile(r"\bC(\d+)\b")

# runs/calib_true.qwen3.5-9b.20260807T081500.reply.md -> calib_true
JOB_FROM_NAME = re.compile(r"^(calib_[a-z]+)\.")


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


def rule(reply: str, job: str) -> tuple[bool, list[str]]:
    answers = ANSWERS[job]
    given = read_rows(reply)
    lines, ok = [], True

    for claim, (want, why) in answers.items():
        got, evidence = given.get(claim, ("MISSING", ""))
        hit = got == want
        ok &= hit
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
    return ok, lines


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        raise SystemExit("usage: rule.py <reply file> [job]")
    path = pathlib.Path(argv[1])
    if not path.is_file():
        raise SystemExit(f"no such reply: {path}")

    job = argv[2] if len(argv) == 3 else ""
    if not job:
        found = JOB_FROM_NAME.match(path.name)
        if not found:
            raise SystemExit(
                f"cannot tell which job {path.name!r} answered; pass it as the "
                f"second argument: {sorted(ANSWERS)}")
        job = found.group(1)
    if job not in ANSWERS:
        raise SystemExit(f"unknown job {job!r}: {sorted(ANSWERS)}")

    ok, lines = rule(path.read_text(encoding="utf-8"), job)
    print(f"{job} — {path.name}")
    print("\n".join(lines))
    print(f"\n{'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
