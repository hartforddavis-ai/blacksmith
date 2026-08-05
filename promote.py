"""Promotion gate — host-controlled, deterministic.

No security claim is made here. This module refuses promotions; it does not
certify the ones it allows. A returned record states which conditions were
re-derived, not that the artifact is correct.

It does NOT write verified memory. Wiring a promotion record into the Marrow
store is a separate host action and is not implemented (see ASSUMPTIONS.md).

Remediation (area 4):
  - the bundle and the artifact are addressed by content hash, never by a path
    supplied in untrusted data, so untrusted input cannot select a read target
  - the contract path and the record directory are host-supplied at
    construction, so untrusted input cannot select a write destination
  - the verdict is re-derived here; a verdict present in the bundle is ignored
    and the fact of ignoring it is carried into the record
  - only ACTIVE promotes; every other verdict raises
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import gauge
import store as store_mod


class PromotionRefused(Exception):
    """The promotion did not meet a condition and was not performed."""


class PromotionGate:
    def __init__(self, object_store: store_mod.ObjectStore, contract_path, record_dir):
        """`contract_path` and `record_dir` are host configuration. Passing
        either from untrusted data defeats this module."""
        self._store = object_store
        self._contract_path = Path(os.path.realpath(str(contract_path)))
        self._record_dir = Path(os.path.realpath(str(record_dir)))
        self._record_dir.mkdir(parents=True, exist_ok=True)

    def _load_contract(self):
        if not self._contract_path.is_file():
            raise PromotionRefused("contract is not a regular file")
        raw = self._contract_path.read_bytes()
        try:
            contract = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PromotionRefused(f"contract is not readable JSON: {exc}")
        return contract, store_mod.sha256_bytes(raw)

    def promote(self, bundle_object_id: str) -> dict:
        """Re-derive the verdict for a stored bundle and promote only on ACTIVE."""
        try:
            bundle_bytes = self._store.get(bundle_object_id)
        except store_mod.StoreError as exc:
            raise PromotionRefused(f"bundle unavailable: {exc}")

        try:
            bundle = json.loads(bundle_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PromotionRefused(f"bundle is not readable JSON: {exc}")
        if not isinstance(bundle, dict):
            raise PromotionRefused("bundle is not an object")

        contract, contract_sha256 = self._load_contract()

        artifact = bundle.get("artifact")
        if not isinstance(artifact, dict):
            raise PromotionRefused("bundle declares no artifact")
        artifact_id = artifact.get("sha256")
        try:
            store_mod._valid_id(artifact_id)
        except store_mod.StoreError as exc:
            raise PromotionRefused(f"artifact is not addressed by digest: {exc}")
        if "path" in artifact:
            # Recorded, never followed.
            pass
        if not self._store.has(artifact_id):
            raise PromotionRefused(f"artifact {artifact_id} is not in the store")
        try:
            self._store.get(artifact_id)
        except store_mod.StoreError as exc:
            # StoreError, not just IntegrityError: has() and this get() aren't
            # atomic, so the object can vanish between them (GC, eviction, race).
            # Widening the catch keeps that a clean refusal, not an unhandled raise.
            raise PromotionRefused(f"artifact failed re-hash: {exc}")

        result = gauge.adjudicate(bundle, contract, contract_sha256)
        if result["verdict"] != "ACTIVE":
            raise PromotionRefused(
                f"verdict {result['verdict']} does not promote; "
                f"{len(result['reasons'])} reason(s) recorded"
            )

        record = {
            "record_version": 1,
            "bundle_object_id": bundle_object_id,
            "artifact_object_id": artifact_id,
            "contract_sha256": contract_sha256,
            "contract_id": result["contract_id"],
            "gauge_version": result["gauge_version"],
            "verdict": result["verdict"],
            "ignored_bundle_keys": result["ignored_bundle_keys"],
            "artifact_path_field_ignored": "path" in artifact,
            "memory_write_performed": False,
        }
        payload = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
        record_id = store_mod.sha256_bytes(payload)

        # Destination is derived from the record's own digest inside the
        # host-declared directory. No component comes from the bundle.
        target = self._record_dir / f"{record_id}.json"
        target.write_bytes(payload)
        os.chmod(target, 0o444)

        return dict(record, record_id=record_id)
