"""Regression coverage for the PromotionGate.promote() TOCTOU widening.

has() and get() are two separate calls against the store; nothing makes them
atomic. This proves an object vanishing between them now surfaces as a clean
PromotionRefused instead of an unhandled StoreError escaping promote()."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import promote
import store as store_mod


class PromoteRaceTests(unittest.TestCase):
    def test_object_vanishing_between_has_and_get_refuses_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            object_store = store_mod.ObjectStore(tmp / "objects")

            contract = {
                "contract_version": 1,
                "contract_id": "test-contract",
                "runner_id": "test-runner",
                "precedence": ["BYPASSED", "FAILED", "UNKNOWN", "ACTIVE"],
                "required_checks": ["some_check"],
            }
            contract_path = tmp / "contract.json"
            contract_path.write_text(json.dumps(contract))

            artifact_id = "a" * 64  # well-formed id, never actually stored
            bundle = {"artifact": {"sha256": artifact_id}}
            bundle_id = object_store.put_bytes(json.dumps(bundle).encode("utf-8"))

            gate = promote.PromotionGate(object_store, contract_path, tmp / "records")

            # has() lies (simulating a race where the object is evicted right
            # after has() returns True); the real get() then raises plain
            # StoreError, not IntegrityError, because the file is simply absent.
            object_store.has = lambda object_id: True

            with self.assertRaises(promote.PromotionRefused):
                gate.promote(bundle_id)


if __name__ == "__main__":
    unittest.main()
