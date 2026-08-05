"""Coverage for manifest.py.

Written this cycle, by the generator, in the same session as manifest.py.

The test that earns its place is the membership one. A manifest that hashes
correctly but omits a module is exactly as wrong as one with a stale hash, and
it is the failure that does not announce itself — `verify_manifest` only checks
what it was told about.
"""

from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

import manifest


class MembershipTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        for name in ("SPEC.md", "ASSUMPTIONS.md", "contract.json"):
            (self.root / name).write_text(name, encoding="utf-8")
        (self.root / "gauge.py").write_text("g", encoding="utf-8")
        (self.root / "cell.py").write_text("c", encoding="utf-8")
        (self.root / "test_gauge.py").write_text("t", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_sources_and_fixed_files_are_members(self):
        self.assertEqual(
            manifest.members(self.root),
            ["ASSUMPTIONS.md", "SPEC.md", "contract.json", "cell.py", "gauge.py"])

    def test_tests_are_excluded(self):
        self.assertNotIn("test_gauge.py", manifest.members(self.root))

    def test_a_new_module_joins_without_anyone_listing_it(self):
        (self.root / "collect.py").write_text("x", encoding="utf-8")
        self.assertIn("collect.py", manifest.members(self.root))

    def test_absent_fixed_file_is_omitted_not_hashed_as_empty(self):
        (self.root / "contract.json").unlink()
        self.assertNotIn("contract.json", manifest.members(self.root))

    def test_render_is_stable_and_matches_sha256_of_the_bytes(self):
        first = manifest.render(self.root)
        self.assertEqual(first, manifest.render(self.root))
        expected = hashlib.sha256(b"c").hexdigest()
        self.assertIn(f"{expected}  cell.py", first)

    def test_render_moves_when_a_member_changes(self):
        before = manifest.render(self.root)
        (self.root / "cell.py").write_text("changed", encoding="utf-8")
        self.assertNotEqual(before, manifest.render(self.root))

    def test_line_format_matches_what_machine_verify_manifest_parses(self):
        # machine.verify_manifest splits on a two-space separator. A one-space
        # manifest parses to a filename with a leading space and every file
        # reports absent, which reads as a failed integrity check rather than
        # as a format error.
        for line in manifest.render(self.root).splitlines():
            digest, sep, name = line.partition("  ")
            self.assertEqual(sep, "  ")
            self.assertEqual(len(digest), 64)
            self.assertTrue(name and not name.startswith(" "))


class LiveTreeTests(unittest.TestCase):
    def test_the_checked_in_manifest_is_current(self):
        self.assertEqual(manifest.MANIFEST.read_text(encoding="utf-8"),
                         manifest.render())

    def test_every_ring0_module_written_this_cycle_is_covered(self):
        covered = set(manifest.members())
        for name in ("cell.py", "attest.py", "launch.py"):
            self.assertIn(name, covered)


if __name__ == "__main__":
    unittest.main()
