"""Coverage for bundle.assemble -- packaging, not adjudication.

These tests confirm the four check results land under the right keys and
that the scalar fields are right; each check function's own correctness is
already covered by its own test module (test_manifest.py,
test_store_as_check.py, test_attest_delta.py, test_tests_pass.py).

`manifest.as_check` and `tests_pass.as_check` are patched out in every test
here, and must stay patched. Both default to the real tree when called with
no argument, and `bundle.assemble` calls them exactly that way. Calling the
real, unmocked `assemble` from inside this tree's own suite makes
`tests_pass.as_check` subprocess-spawn `python3 -m unittest discover` over
this tree -- which discovers this very file, whose tests call `assemble`
again, which spawns discovery again, unbounded. That happened once, live,
during this module's own first test run; killing the fork bomb and patching
these two calls out is the fix, not a defensive nicety.
"""

from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import bundle
import manifest
import store as store_mod
import tests_pass


def _report(integrity: str) -> dict:
    return {"attest_version": "attest-1", "integrity": integrity,
            "detail": "synthetic report for bundle tests", "deltas": [],
            "scratch_deltas": []}


class AssembleTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.store = store_mod.ObjectStore(Path(self._tmp.name))
        self.artifact_id = self.store.put_bytes(b"artifact bytes")

        self._patches = [
            mock.patch.object(manifest, "as_check",
                               return_value={"outcome": "PASS", "detail": "stub"}),
            mock.patch.object(tests_pass, "as_check",
                               return_value={"outcome": "PASS", "detail": "stub"}),
        ]
        for p in self._patches:
            p.start()
            self.addCleanup(p.stop)

    def tearDown(self):
        self._tmp.cleanup()

    def test_bundle_version_and_contract_hash(self):
        result = bundle.assemble(_report("INTACT"), self.store, self.artifact_id)
        self.assertEqual(result["bundle_version"], bundle.BUNDLE_VERSION)
        self.assertEqual(result["contract_sha256"], bundle.contract_sha256())

    def test_contract_sha256_matches_a_direct_hash_of_the_file(self):
        expected = hashlib.sha256(bundle.CONTRACT.read_bytes()).hexdigest()
        self.assertEqual(bundle.contract_sha256(), expected)

    def test_checks_dict_has_exactly_the_four_required_keys(self):
        result = bundle.assemble(_report("INTACT"), self.store, self.artifact_id)
        self.assertEqual(set(result["checks"]), {
            "no_generator_write_to_checker_tree",
            "artifact_hash_matches_manifest",
            "runner_integrity_verified",
            "tests_pass",
        })

    def test_runner_omitted_by_default(self):
        result = bundle.assemble(_report("INTACT"), self.store, self.artifact_id)
        self.assertNotIn("runner", result)

    def test_runner_included_when_supplied(self):
        result = bundle.assemble(_report("INTACT"), self.store, self.artifact_id,
                                  runner={"id": "blacksmith-gauge-1"})
        self.assertEqual(result["runner"], {"id": "blacksmith-gauge-1"})

    def test_attest_check_wires_through_intact_as_pass(self):
        result = bundle.assemble(_report("INTACT"), self.store, self.artifact_id)
        self.assertEqual(
            result["checks"]["no_generator_write_to_checker_tree"]["outcome"], "PASS")

    def test_attest_check_wires_through_bypassed(self):
        result = bundle.assemble(_report("BYPASSED"), self.store, self.artifact_id)
        self.assertEqual(
            result["checks"]["no_generator_write_to_checker_tree"]["outcome"], "BYPASSED")

    def test_store_check_wires_through_a_missing_artifact_as_fail(self):
        never_staged = "a" * 64
        result = bundle.assemble(_report("INTACT"), self.store, never_staged)
        self.assertEqual(
            result["checks"]["artifact_hash_matches_manifest"]["outcome"], "FAIL")


if __name__ == "__main__":
    unittest.main()
