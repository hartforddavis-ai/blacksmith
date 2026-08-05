"""Gauge — deterministic adjudicator.

This module makes no security claim. It computes a verdict from supplied data
and nothing else. It performs no I/O, so it cannot verify any fact it is told;
it can only report what the supplied evidence does and does not establish.

Constraints held here:
  - no filesystem, no network, no subprocess, no environment, no clock,
    no randomness, no float arithmetic
  - output depends only on (bundle, contract, contract_sha256)

Remediation:
  F17 / area 3 — precedence is structural. A contract can no longer reorder it,
  and `ACTIVE` is unreachable while any reason exists.
  area 3 — a demonstrated failure is not downgraded by missing evidence:
  FAILED outranks UNKNOWN.
  area 3 — malformed input yields a non-promoting verdict, never ACTIVE.
"""

from __future__ import annotations

import json
import unicodedata

GAUGE_VERSION = "gauge-2"

VERDICTS = ("ACTIVE", "FAILED", "UNKNOWN", "BYPASSED")
CHECK_OUTCOMES = ("PASS", "FAIL", "BYPASSED")

# Structural precedence. Not data. ACTIVE is absent by construction: it is the
# result of an empty reason set, never a selectable category.
_ORDER = ("BYPASSED", "FAILED", "UNKNOWN")
CANONICAL_PRECEDENCE = list(_ORDER) + ["ACTIVE"]

_BUNDLE_VERSION = 1
_CONTRACT_VERSION = 1

_AUTHORITY_KEYS = ("verdict", "promotion", "verified", "gauge_result", "approved")


def _reason(category: str, code: str, detail: str) -> dict:
    return {"category": category, "code": code, "detail": detail}


def _nfc(value):
    return unicodedata.normalize("NFC", value) if isinstance(value, str) else value


def adjudicate(bundle, contract, contract_sha256) -> dict:
    """(evidence bundle, proof contract, contract hash) -> verdict record.

    `contract_sha256` is supplied by the caller because computing it would mean
    reading a file, and this module does no I/O.
    """
    reasons = []
    ignored = []

    if not isinstance(contract, dict) or contract.get("contract_version") != _CONTRACT_VERSION:
        return _result([_reason("UNKNOWN", "contract_unusable",
                                "contract is not a v1 contract object")], ignored, None)

    contract_id = contract.get("contract_id")
    if not isinstance(contract_id, str) or not contract_id:
        return _result([_reason("UNKNOWN", "contract_unusable",
                                "contract declares no contract_id")], ignored, None)

    # The contract may no longer set precedence. It must declare the canonical
    # order, and a mismatch is reported rather than silently overridden.
    if contract.get("precedence") != CANONICAL_PRECEDENCE:
        reasons.append(_reason("UNKNOWN", "contract_precedence_mismatch",
                               "contract precedence does not match the structural order"))

    required = contract.get("required_checks")
    if not isinstance(required, list) or not required:
        reasons.append(_reason("UNKNOWN", "contract_unusable",
                               "contract declares no required_checks"))
        return _result(reasons, ignored, contract_id)
    if not all(isinstance(c, str) and c for c in required):
        reasons.append(_reason("UNKNOWN", "contract_unusable",
                               "contract required_checks contains a non-string entry"))
        return _result(reasons, ignored, contract_id)

    if not isinstance(contract_sha256, str) or not contract_sha256:
        reasons.append(_reason("UNKNOWN", "contract_hash_absent",
                               "caller supplied no contract hash to bind evidence against"))

    if not isinstance(bundle, dict):
        reasons.append(_reason("UNKNOWN", "bundle_unusable",
                               "evidence bundle is not an object"))
        return _result(reasons, ignored, contract_id)

    for key in _AUTHORITY_KEYS:
        if key in bundle:
            ignored.append(key)

    if bundle.get("bundle_version") != _BUNDLE_VERSION:
        reasons.append(_reason("UNKNOWN", "bundle_unusable",
                               "evidence bundle is not a v1 bundle"))
        return _result(reasons, ignored, contract_id)

    if bundle.get("contract_sha256") != contract_sha256:
        reasons.append(_reason("UNKNOWN", "contract_mismatch",
                               "evidence was collected against a different contract"))

    runner = bundle.get("runner")
    if not isinstance(runner, dict) or runner.get("id") != contract.get("runner_id"):
        reasons.append(_reason("UNKNOWN", "runner_mismatch",
                               "evidence was collected by a runner the contract does not pin"))

    checks = bundle.get("checks")
    if not isinstance(checks, dict):
        reasons.append(_reason("UNKNOWN", "checks_absent",
                               "evidence bundle carries no checks object"))
        return _result(reasons, ignored, contract_id)

    folded = {}
    for raw_key in checks:
        key = _nfc(raw_key)
        if not isinstance(key, str):
            reasons.append(_reason("UNKNOWN", "check_key_unusable",
                                   "evidence bundle carries a non-string check key"))
            continue
        if key in folded:
            reasons.append(_reason("UNKNOWN", "check_key_ambiguous",
                                   f"two check keys normalise to {key!r}"))
            continue
        folded[key] = checks[raw_key]

    for check_id in sorted({_nfc(c) for c in required}):
        entry = folded.get(check_id)
        if not isinstance(entry, dict):
            reasons.append(_reason("UNKNOWN", "check_missing",
                                   f"required check {check_id!r} is absent from the evidence"))
            continue
        outcome = entry.get("outcome")
        if outcome not in CHECK_OUTCOMES:
            reasons.append(_reason("UNKNOWN", "check_indeterminate",
                                   f"required check {check_id!r} has no usable outcome"))
        elif outcome == "BYPASSED":
            reasons.append(_reason("BYPASSED", "check_bypassed",
                                   f"required check {check_id!r} did not run: the control was bypassed"))
        elif outcome == "FAIL":
            reasons.append(_reason("FAILED", "check_failed",
                                   f"required check {check_id!r} ran and failed"))

    return _result(reasons, ignored, contract_id)


def _pick(reasons) -> str:
    present = {r["category"] for r in reasons}
    for verdict in _ORDER:
        if verdict in present:
            return verdict
    return "ACTIVE"


def _result(reasons, ignored, contract_id) -> dict:
    verdict = _pick(reasons)
    if reasons and verdict == "ACTIVE":
        # Unreachable by construction. Retained so a future edit to _pick or
        # _ORDER cannot make ACTIVE co-exist with an unmet condition.
        reasons = list(reasons) + [_reason("UNKNOWN", "internal_inconsistency",
                                           "reasons present with no category in the structural order")]
        verdict = "UNKNOWN"
    return {
        "gauge_version": GAUGE_VERSION,
        "contract_id": contract_id,
        "verdict": verdict,
        "reasons": sorted(reasons, key=lambda r: (r["category"], r["code"], r["detail"])),
        "ignored_bundle_keys": sorted(set(ignored)),
    }


def canonical(result: dict) -> str:
    """Byte-stable serialisation. Determinism is asserted against this form."""
    return json.dumps(result, sort_keys=True, separators=(",", ":"))
