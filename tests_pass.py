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

No UNKNOWN branch: `python3 -m unittest discover` exits 0 only when every
discovered test passed, and non-zero otherwise — including exit 5 when
discovery finds nothing to run. Unittest's own contract already refuses to
call an empty run a pass, so there is no zero-tests-reported-as-PASS case
left to guard against separately. A run either succeeds or it doesn't;
there is no third state to force, matching `store.as_check`'s reasoning.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def as_check(root: Path | None = None) -> dict:
    """Run the test suite under `root` and render its exit code as a check entry.

    `root` defaults to this file's own directory — the real Blacksmith tree.
    The parameter exists so tests can point discovery at a disposable
    directory of synthetic test files instead of recursively invoking this
    tree's own suite, of which this check's test is itself a member.
    """
    target = root or HERE
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover",
         "-s", str(target), "-p", "test_*.py"],
        cwd=str(target),
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return {"outcome": "PASS", "detail": "test suite passed"}
    return {"outcome": "FAIL",
            "detail": f"test suite failed (exit code {result.returncode})"}
