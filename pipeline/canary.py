"""Planted defects, used to measure whether a reviewer was actually looking.

Every other gate in this pipeline catches a reviewer that fabricates. None of
them catch one that skims and returns nothing — an empty finding list passes
grounding, citation, and binding checks perfectly. That is the whole failure
mode of running a cheap model on an open-ended question, and it is invisible
without this.

So each bundle carries one synthetic module containing a defect of a shape this
codebase has actually produced. A reviewer who misses it did not review. The
verdict is discarded as insensitive, and the miss is logged, so the catch-rate
becomes a measurement of the model rather than an opinion about it.

Rotating by bundle digest means the same defect never appears twice running,
and the file name never marks itself out as the plant.
"""

from __future__ import annotations

import hashlib

# Each entry mirrors a defect that was real in this repository. `marker` is the
# line the reviewer has to land on; `line` is computed, not hand-counted.
DEFECTS = (
    {
        "kind": "empty-credential comparison passes",
        "module": "session_token",
        "body": '''"""Compare a presented token against the expected one."""

import hmac


def token_matches(presented: str, expected: str) -> bool:
    return hmac.compare_digest(presented, expected)


def authorise(request: dict, expected: str) -> bool:
    presented = request.get("token", "")
    if token_matches(presented, expected):
        return True
    return False
''',
        "marker": "return hmac.compare_digest(presented, expected)",
        "hint": "empty against empty compares equal",
    },
    {
        "kind": "regex anchored with $ accepts a trailing newline",
        "module": "object_name",
        "body": '''"""Validate an object name before it is used as a path segment."""

import re

NAME = re.compile(r"^[a-z0-9_]{1,32}$")


def valid(name: str) -> bool:
    return bool(NAME.match(name))


def resolve(root, name: str):
    if not valid(name):
        raise ValueError(f"bad object name: {name!r}")
    return root / name
''',
        "marker": 'NAME = re.compile(r"^[a-z0-9_]{1,32}$")',
        "hint": "$ matches before a trailing newline; \\Z does not",
    },
    {
        "kind": "swallowed exception returns the permissive default",
        "module": "integrity_probe",
        "body": '''"""Report whether an artifact still matches its recorded hash."""

import hashlib
from pathlib import Path


def matches(path: Path, expected: str) -> bool:
    try:
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        return actual == expected
    except OSError:
        return True
''',
        "marker": "return True",
        "hint": "an unreadable artifact reports as intact",
    },
    {
        "kind": "path check inspects only the first and last segment",
        "module": "patch_path",
        "body": '''"""Reject patch paths that try to escape the work tree."""


def path_is_safe(raw: str) -> bool:
    parts = raw.split("/")
    if parts[0] == ".." or parts[-1] == "..":
        return False
    return True


def apply_to(root, raw: str):
    if not path_is_safe(raw):
        raise ValueError(f"unsafe path: {raw!r}")
    return root / raw
''',
        "marker": 'if parts[0] == ".." or parts[-1] == "..":',
        "hint": "a .. in a middle segment is never inspected",
    },
    {
        "kind": "truncating write leaves a partial file on failure",
        "module": "record_writer",
        "body": '''"""Persist a promoted record."""

import json
from pathlib import Path


def write_record(path: Path, record: dict) -> None:
    with open(path, "wb") as fh:
        fh.write(json.dumps(record).encode("utf-8"))


def promote(path: Path, record: dict) -> None:
    write_record(path, record)
''',
        "marker": 'with open(path, "wb") as fh:',
        "hint": "truncates before it writes; a crash leaves a valid-looking stub",
    },
)


def _camouflage(neighbours: list[str]) -> str:
    """The directory the plant should appear to live in.

    Without this the plant is a bare filename sitting among repo-relative
    paths — a tell that identifies it without reading a line of it. A reviewer
    who learns that pattern flags the canary every cycle for free, and the gate
    keeps reporting passes while measuring nothing. So the plant takes the
    directory its neighbours use.
    """
    dirs = [rel.rsplit("/", 1)[0] for rel in neighbours if "/" in rel]
    if not dirs:
        return ""
    return max(sorted(set(dirs)), key=dirs.count)


def select(seed: str, neighbours: list[str] | None = None) -> dict:
    """Pick a defect deterministically from the bundle's own digest."""
    index = int.from_bytes(
        hashlib.sha256(f"canary:{seed}".encode()).digest()[:8], "big")
    defect = DEFECTS[index % len(DEFECTS)]

    lines = defect["body"].splitlines()
    line_no = next(
        (i for i, text in enumerate(lines, start=1)
         if defect["marker"] in text), 0)
    directory = _camouflage(neighbours or [])
    name = f"{defect['module']}.py"
    return {
        "filename": f"{directory}/{name}" if directory else name,
        "body": defect["body"],
        "line": line_no,
        "kind": defect["kind"],
        "hint": defect["hint"],
    }
