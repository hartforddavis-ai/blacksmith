"""Attest — freeze a manifest of the cell before launch, re-derive it after.

No security claim is made here. This module hashes bytes and compares two sets
of hashes. It cannot tell you *who* wrote a file, only that the bytes are not
the bytes that were there before.

That limitation is the instrument, not a weakness in it. SPEC §5 step 6: the
question is not whether a write was denied, it is whether one happened. A
denial that reads *pending* is a boundary a human can click through; a changed
digest is not.

Three properties are held deliberately:

  A manifest is frozen. `Attestation` is immutable and there is no amend path.
  SPEC §4: a missing manifest reports integrity UNKNOWN and is never filled in
  later. An UNKNOWN that can be upgraded after the fact by supplying the
  manifest you wish you had taken is not an UNKNOWN.

  The two sides are bound. `compare` refuses a pre/post pair that disagrees
  about the cell root or about the declared scratch region, and refuses one
  where post was taken before pre. Widening the scratch declaration after a
  delta is found is the obvious way to make a BYPASSED go away, so it is a
  refusal rather than a judgement call.

  Absence is a delta. A path in pre and not in post is reported exactly as
  loudly as changed content. Deleting the evidence is a write.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path

ATTEST_VERSION = "attest-1"

INTACT = "INTACT"
BYPASSED = "BYPASSED"
UNKNOWN = "UNKNOWN"

PHASES = ("pre", "post")


class AttestError(Exception):
    """The attestation could not be taken, or two of them could not be compared."""


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _entry(path: Path) -> dict:
    """One manifest row.

    Symlinks record their target string and are never followed. Following one
    would hash the destination, so a symlink retargeted between attestations
    would leave the manifest unchanged.

    Mode is recorded because a chmod is a write. A tree whose read-only bits
    were restored after the fact is not a tree that was never written to.
    """
    if path.is_symlink():
        return {"kind": "symlink", "target": os.readlink(path),
                "mode": stat_mode(path, follow=False)}
    if path.is_dir():
        return {"kind": "dir", "mode": stat_mode(path)}
    if path.is_file():
        return {"kind": "file", "sha256": _hash_file(path), "mode": stat_mode(path),
                "size": path.stat().st_size}
    return {"kind": "other", "mode": stat_mode(path, follow=False)}


def stat_mode(path: Path, follow: bool = True) -> str:
    info = path.stat() if follow else path.lstat()
    return format(info.st_mode & 0o7777, "04o")


def _walk(root: Path) -> dict:
    entries = {}
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in list(dirnames) + list(filenames):
            target = current_path / name
            entries[str(target.relative_to(root))] = _entry(target)
    return entries


@dataclass(frozen=True)
class Attestation:
    """A frozen measurement. Construct it with `freeze`; never edit one."""

    phase: str
    cell_root: str
    scratch_prefixes: tuple
    entries: dict
    external: dict

    def canonical(self) -> str:
        return json.dumps({
            "attest_version": ATTEST_VERSION,
            "phase": self.phase,
            "cell_root": self.cell_root,
            "scratch_prefixes": sorted(self.scratch_prefixes),
            "entries": self.entries,
            "external": self.external,
        }, sort_keys=True, separators=(",", ":"))

    def root_hash(self) -> str:
        return hashlib.sha256(self.canonical().encode("utf-8")).hexdigest()


def freeze(phase: str, cell_root, scratch_prefixes=(), external_paths=()) -> Attestation:
    """Measure the cell now.

    `external_paths` covers what SPEC §4 names alongside the cell — the
    contract and the runner. They live outside the tree, so they are recorded
    by absolute path; a missing one is recorded as absent rather than skipped,
    because a runner that vanished between pre and post is a delta.
    """
    if phase not in PHASES:
        raise AttestError(f"phase must be one of {PHASES}, got {phase!r}")
    root = Path(os.path.realpath(str(cell_root)))
    if not root.is_dir():
        raise AttestError(f"cell root {str(root)!r} is not a directory")

    external = {}
    for item in external_paths:
        target = Path(os.path.realpath(str(item)))
        external[str(target)] = (
            _entry(target) if target.exists() else {"kind": "absent"})

    entries = _walk(root)
    prefixes = tuple(sorted(str(p) for p in scratch_prefixes))

    # A prefix matching nothing binds to nothing, silently: the runner's own
    # writes then report BYPASSED. Usually a base mismatch, which
    # `cell.attest_args` prevents.
    #
    # Pre only. At post, a deleted scratch directory is a delta, not a crash.
    if phase == "pre":
        unbound = [p for p in prefixes
                   if p not in entries and not any(
                       _in_scratch(rel, (p,)) for rel in entries)]
        if unbound:
            raise AttestError(
                f"scratch prefixes {unbound} match no path in {str(root)!r}; a "
                "declaration that binds to nothing would report the runner's "
                "own writes as BYPASSED. Check the base: entries here are "
                "relative to the cell root, and cell.attest_args rebases a "
                "CellSpec's home-relative prefixes onto it")

    return Attestation(
        phase=phase,
        cell_root=str(root),
        scratch_prefixes=prefixes,
        entries=entries,
        external=external,
    )


def _in_scratch(rel: str, scratch_prefixes) -> bool:
    path = Path(rel)
    return any(path == Path(p) or Path(p) in path.parents for p in scratch_prefixes)


def _delta(rel: str, before, after) -> dict | None:
    if before == after:
        return None
    if before is None:
        return {"path": rel, "change": "created", "after": after}
    if after is None:
        return {"path": rel, "change": "removed", "before": before}
    if before.get("kind") != after.get("kind"):
        return {"path": rel, "change": "kind_changed", "before": before, "after": after}
    if before.get("sha256") != after.get("sha256"):
        return {"path": rel, "change": "content_changed", "before": before, "after": after}
    if before.get("target") != after.get("target"):
        return {"path": rel, "change": "symlink_retargeted", "before": before, "after": after}
    return {"path": rel, "change": "mode_changed", "before": before, "after": after}


def compare(pre: Attestation | None, post: Attestation | None) -> dict:
    """Re-derive the integrity state from two frozen measurements.

    Returns one of INTACT, BYPASSED, UNKNOWN. There is no fourth state and no
    partial credit: SPEC §5 step 6 reads "ANY delta = write capability =
    BYPASSED", and a rule that admits a small delta is a rule about magnitude,
    not about capability.
    """
    if pre is None or post is None:
        missing = "pre-attest" if pre is None else "post-attest"
        return _report(UNKNOWN, [], [], f"{missing} manifest is absent")
    if pre.phase != "pre" or post.phase != "post":
        return _report(UNKNOWN, [], [],
                       f"manifests are phased {pre.phase!r}/{post.phase!r}, not pre/post")
    if pre.cell_root != post.cell_root:
        return _report(UNKNOWN, [], [], "manifests describe different cell roots")
    if pre.scratch_prefixes != post.scratch_prefixes:
        return _report(UNKNOWN, [], [],
                       "manifests declare different scratch regions; the declaration "
                       "is made before launch and cannot be restated afterwards")

    scratch = pre.scratch_prefixes
    attested, scratch_deltas = [], []
    for rel in sorted(set(pre.entries) | set(post.entries)):
        delta = _delta(rel, pre.entries.get(rel), post.entries.get(rel))
        if delta is None:
            continue
        (scratch_deltas if _in_scratch(rel, scratch) else attested).append(delta)

    for name in sorted(set(pre.external) | set(post.external)):
        delta = _delta(name, pre.external.get(name), post.external.get(name))
        if delta is not None:
            attested.append(delta)

    if attested:
        return _report(BYPASSED, attested, scratch_deltas,
                       f"{len(attested)} attested path(s) changed between pre and post")
    return _report(INTACT, [], scratch_deltas,
                   "no attested path changed between pre and post")


def _report(integrity: str, deltas, scratch_deltas, detail: str) -> dict:
    return {
        "attest_version": ATTEST_VERSION,
        "integrity": integrity,
        "detail": detail,
        "deltas": deltas,
        # Reported, never used to reach a verdict. A runner that writes its own
        # session state is expected; the row exists so an operator can see the
        # declared region was not silently doing something else.
        "scratch_deltas": scratch_deltas,
    }


def as_check(report: dict) -> dict:
    """Render an integrity report as a gauge check entry.

    INTACT maps to PASS and BYPASSED to BYPASSED. UNKNOWN maps to *no outcome
    key at all*, which gauge reads as `check_indeterminate` and resolves to a
    non-promoting UNKNOWN. Emitting a named "UNKNOWN" outcome instead would put
    a string outside gauge's CHECK_OUTCOMES into the bundle, and gauge's
    handling of that is a fallback rather than the stated path.
    """
    entry = {"detail": report["detail"], "delta_count": len(report["deltas"])}
    if report["integrity"] == INTACT:
        entry["outcome"] = "PASS"
    elif report["integrity"] == BYPASSED:
        entry["outcome"] = "BYPASSED"
    return entry
