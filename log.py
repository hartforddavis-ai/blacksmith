"""Evidence log — append-only, parent-side. Ring 0.

Every stage records its decision here at the moment it decides. A stage that
returns its findings and keeps no record leaves nothing to diagnose from once
the process exits.

The log is not placed in any cell's declared tree, so a runner confined to its
tree has no path to it. That is non-declaration, not permission: it becomes a
boundary when SPEC §8 step 0 resolves, and not before.

A write failure is not caught. SPEC §2 rule 6 is fail closed: a stage whose
outcome cannot be recorded has not run to specification.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent / "EVIDENCE.jsonl"

OUTCOMES = ("PASS", "FAIL")


class LogError(ValueError):
    """The record could not be formed."""


def record(stage: str, outcome: str, detail: dict,
           path: Path | None = None) -> None:
    """Append one decision to the evidence log.

    Opened in append mode and never read back, so cost does not grow with the
    length of the log.
    """
    if outcome not in OUTCOMES:
        raise LogError(f"outcome must be one of {OUTCOMES}, not {outcome!r}")
    entry = {
        "at": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        "outcome": outcome,
        "detail": detail,
    }
    target = Path(path) if path is not None else LOG_PATH
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")
