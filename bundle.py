"""bundle — assemble a gauge-ready evidence bundle from already-produced checks.

No security claim is made here. This module adjudicates nothing; it packages
the output of four existing `as_check()` functions, plus a contract hash it
computes itself, into the shape `gauge.adjudicate()` expects. `gauge` is the
only adjudicator in this tree.

`contract_sha256` is re-derived by reading `contract.json` fresh on every
call, never pinned or cached. A stored hash is exactly the drift
`manifest.py`'s own docstring warns a hand-maintained list would silently
reintroduce, and every other check in this tree already re-derives rather
than trusts a stored value (store re-hashes on read, attest re-hashes the
cell, manifest re-hashes the Ring 0 tree).

`attest_report` and `(store, artifact_id)` are accepted as arguments, not
produced here: they are a specific run's evidence, already owned by
`attest.py` and `store.py`. Re-deriving them in this module would be a
second path to the same evidence.

`runner` is optional and omitted by default. Populating
`bundle["runner"]["id"]` in the Blacksmith-pipeline sense is a separate,
undecided call (KERNEL_WIRE_TESTS_PASS_CHECK.md) -- an absent runner
reports UNKNOWN via gauge's own `runner_mismatch` check, honestly, not a
gap this module patches over.

No CLI: a command-line entry needs a real, already-serialized run to read,
and nothing in this tree yet writes an attest report or a staged artifact
id to disk -- `runs/pivot_smoke...md` is still hand-written. Adding one now
would be a command with nothing real to point it at.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import attest
import manifest
import store as store_mod
import tests_pass

HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "contract.json"

BUNDLE_VERSION = 1


def contract_sha256(path: Path | None = None) -> str:
    """Hash contract.json fresh. Never pinned -- see module docstring."""
    target = path or CONTRACT
    return hashlib.sha256(target.read_bytes()).hexdigest()


def assemble(attest_report: dict, store: store_mod.ObjectStore, artifact_id: str,
             runner: dict | None = None) -> dict:
    """Package one run's already-produced evidence into a gauge-ready bundle."""
    result = {
        "bundle_version": BUNDLE_VERSION,
        "contract_sha256": contract_sha256(),
        "checks": {
            "no_generator_write_to_checker_tree": attest.as_check(attest_report),
            "artifact_hash_matches_manifest": store_mod.as_check(store, artifact_id),
            "runner_integrity_verified": manifest.as_check(),
            "tests_pass": tests_pass.as_check(),
        },
    }
    if runner is not None:
        result["runner"] = runner
    return result
