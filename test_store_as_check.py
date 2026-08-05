"""Coverage for store.as_check — the artifact_hash_matches_manifest mechanism.

Four cases, each tied to a named failure per KERNEL_WIRE_GAUGE_CHECK.md's
Law-1 pass: PASS is reachable at all; FAIL on an id nothing was ever staged
under (SPEC's "missing-evidence-as-pass" row); FAIL on bytes altered after
staging (the tamper case this check exists for); FAIL, not a crash, on a
malformed id (no second, un-audited validation path). No UNKNOWN case: a
store lookup only ever succeeds or raises, so there is no third state to
force, and none is tested.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import store as store_mod


class AsCheckTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.store = store_mod.ObjectStore(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def test_pass_when_staged_object_is_intact(self):
        object_id = self.store.put_bytes(b"artifact bytes")
        entry = store_mod.as_check(self.store, object_id)
        self.assertEqual(entry["outcome"], "PASS")

    def test_fail_when_nothing_was_ever_staged_under_the_id(self):
        never_staged = "a" * 64
        entry = store_mod.as_check(self.store, never_staged)
        self.assertEqual(entry["outcome"], "FAIL")

    def test_fail_when_bytes_are_altered_after_staging(self):
        object_id = self.store.put_bytes(b"artifact bytes")
        target = self.store._path_for(object_id)
        target.chmod(0o644)
        target.write_bytes(b"tampered bytes")

        entry = store_mod.as_check(self.store, object_id)
        self.assertEqual(entry["outcome"], "FAIL")

    def test_fail_not_crash_on_malformed_id(self):
        entry = store_mod.as_check(self.store, "not-a-hex-digest")
        self.assertEqual(entry["outcome"], "FAIL")


if __name__ == "__main__":
    unittest.main()
