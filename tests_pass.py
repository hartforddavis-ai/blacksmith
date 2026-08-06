"""tests_pass — run this tree's own test suite and report the result as data.

No security claim is made here. This module runs `python3 -m unittest
discover` against this tree's `test_*.py` files and reports whether the
process exited zero. It cannot tell you a passing suite means the pipeline
is correct, only that the suite that exists did not report a failure.

`tests_pass` is the last of the four checks `contract.json` requires
(KERNEL_WIRE_TESTS_PASS_CHECK.md). It answers a different question than
`manifest.as_check`: manifest asks whether the Ring 0 bytes on disk match
what was sealed; this asks whether the code those bytes describe still
satisfies its own suite. A file can be re-sealed while a test regresses,
and a suite can stay green while an unrelated Ring 0 edit goes unsealed —
the two checks do not answer the same question, so wiring this one is not
redundant with `runner_integrity_verified`.

Subprocess, not in-process: a failure inside the suite's own import graph
(a bad import, a syntax error in a Ring 0 module) must surface as a plain
non-zero exit code to whatever calls `as_check`, not as an exception raised
in the caller's own process.

No UNKNOWN branch: a run either succeeds or it doesn't, and there is no
third state to force, matching `store.as_check`'s reasoning.

The exit code alone is not enough. `unittest discover` exits 5 on an empty
discovery only from Python 3.12; the interpreter this actually runs under
(`sys.executable`) is 3.9.6 here, which exits 0 and prints "Ran 0 tests".
An empty tree therefore certified PASS — SPEC §9 step 5's
missing-evidence-as-pass, inside one of the four checks `contract.json`
requires. The run count is read back from the runner's own output instead,
and no tests run is FAIL, per SPEC §2 rule 6.

Bounded: a hung suite is a demonstrated failure, not a hypothetical one --
this session's own bundle.py bug drove this exact subprocess into a live,
unbounded recursive hang that needed a manual `pkill` to end. A timeout
turns that into an ordinary FAIL instead of a wait with no ceiling on
whatever called `as_check`.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

TIMEOUT_SECONDS = 120

RAN = re.compile(r"^Ran (\d+) tests? in ", re.MULTILINE)


def as_check(root: Path | None = None) -> dict:
    """Run the test suite under `root` and render its exit code as a check entry.

    `root` defaults to this file's own directory — the real Blacksmith tree.
    The parameter exists so tests can point discovery at a disposable
    directory of synthetic test files instead of recursively invoking this
    tree's own suite, of which this check's test is itself a member.
    """
    target = root or HERE
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover",
             "-s", str(target), "-p", "test_*.py"],
            cwd=str(target),
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return {"outcome": "FAIL",
                "detail": f"test suite did not finish within {TIMEOUT_SECONDS}s"}
    if result.returncode != 0:
        return {"outcome": "FAIL",
                "detail": f"test suite failed (exit code {result.returncode})"}
    match = RAN.search(result.stderr)
    ran = int(match.group(1)) if match else 0
    if not ran:
        return {"outcome": "FAIL",
                "detail": "test suite reported no tests run"}
    return {"outcome": "PASS", "detail": f"test suite passed ({ran} tests)"}
