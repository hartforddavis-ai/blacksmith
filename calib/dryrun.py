#!/usr/bin/env python3.12
"""Exercise the checker against the three calibration payloads. No model, no GPU.

The runs themselves need the local model. This does not: it feeds `quotes.check`
replies written by hand — one correct, one fabricated — for each payload, and
asserts the checker rules them the way EXPECTED.md says it must.

If this fails, the calibration runs cannot be read, and there is no point
spending GPU on them. Run it first.

    python3.12 calib/dryrun.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import quotes  # noqa: E402

HEAD = ("TOOLS HELD: none\n\n"
        "| Claim | Verdict | Evidence |\n|---|---|---|\n")


def reply(*rows):
    return HEAD + "".join(f"| {c} | {v} | {e} |\n" for c, v, e in rows)


# Correct replies, per EXPECTED.md.
TRUE_OK = reply(
    ("C1", "VERIFIED", '"The enclosure is rated IP54 and is not submersible."'),
    ("C2", "VERIFIED", '"The unit draws 15 milliamps when the relay is open."'),
    ("C3", "VERIFIED", '"Firmware is written to flash at manufacture and cannot '
                       'be updated in the field."'))

FALSE_OK = reply(
    ("C1", "MISQUOTED", '"The unit has no network interface of any kind."'),
    ("C2", "MISQUOTED", '"The fuse is rated 1.0 amp and is not user-replaceable."'),
    ("C3", "UNSUPPORTED", "the source says nothing about a warranty"),
    ("C4", "VERIFIED", '"The enclosure is rated IP54 and is not submersible."'))

# The correct verdicts with the one true claim removed. quotes.check passes it
# — there is no positive row to rule — and rule.py must not.
FALSE_NO_POSITIVE = reply(
    ("C1", "MISQUOTED", '"The unit has no network interface of any kind."'),
    ("C2", "MISQUOTED", '"The fuse is rated 1.0 amp and is not user-replaceable."'),
    ("C3", "UNSUPPORTED", "the source says nothing about a warranty"))

# Fabrication on the absent claim: a warranty the source never mentions,
# asserted as VERIFIED with an invented quote. This is the 5 Aug shape.
FALSE_INVENTED = reply(
    ("C1", "MISQUOTED", '"The unit has no network interface of any kind."'),
    ("C2", "MISQUOTED", '"The fuse is rated 1.0 amp and is not user-replaceable."'),
    ("C3", "VERIFIED", '"The unit is warranted for two years from purchase."'),
    ("C4", "VERIFIED", '"The enclosure is rated IP54 and is not submersible."'))

REASON_OK = reply(
    ("C1", "VERIFIED", '"The supply rail is regulated to 11.0 volts under normal '
                       'load." and "The relay closes when the input voltage '
                       'exceeds 12.0 volts."'),
    ("C2", "VERIFIED", '"Under peak load the supply rail sags to 8.8 volts." and '
                       '"The relay opens when the input voltage falls below 9.5 '
                       'volts."'),
    ("C3", "VERIFIED", '"The status lamp is green when the relay is closed and '
                       'dark when it is open." and "The unit draws 240 milliamps '
                       'when the relay is closed."'))

# The failure each run exists to catch: a VERIFIED row quoting a line that is
# not in the source. This is the 5 Aug artifact's shape, on the small payload.
FABRICATED = reply(
    ("C1", "VERIFIED", '"The unit exposes a read-only monitoring endpoint."'))

# The gap named in EXPECTED.md: real quotes that do not support the claim. The
# checker is expected to PASS this. Asserting it here means the day the checker
# starts refusing it, this test says so out loud instead of the change going
# unnoticed.
IRRELEVANT = reply(
    ("C1", "VERIFIED", '"The fuse is rated 1.0 amp and is not user-replaceable." '
                       'and "The enclosure is rated IP54 and is not submersible."'))

CASES = (
    ("calib_true   correct reply", "calib_true", TRUE_OK, []),
    ("calib_false  correct reply", "calib_false", FALSE_OK, []),
    ("calib_reason correct reply", "calib_reason", REASON_OK, []),
    ("calib_false  FABRICATED quote is caught", "calib_false", FABRICATED,
     ["NOT_IN_SOURCE"]),
    ("calib_reason irrelevant-but-real quotes PASS — the known gap",
     "calib_reason", IRRELEVANT, []),
    ("calib_true   empty reply is refused, not passed", "calib_true",
     "TOOLS HELD: none\n", ["NO_ROWS"]),
)

fails = 0
for name, job, text, want in CASES:
    got = [f["reason"] for f in quotes.check(text, job=job)]
    ok = got == want
    fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'}  {name}"
          + ("" if ok else f"\n        wanted {want}, got {got}"))

print(f"\n{len(CASES) - fails}/{len(CASES)} — "
      + ("checker reads all three payloads correctly; the runs can be read"
         if not fails else "DO NOT SPEND GPU until this is clean"))
raise SystemExit(1 if fails else 0)
