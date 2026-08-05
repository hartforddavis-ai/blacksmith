"""Coverage for attest.py.

Written this cycle, by the generator, in the same session as attest.py. These
tests are evidence that the comparison behaves as its author expected. They are
not evidence that a real runner cannot write to a real cell without being seen
— every write here is performed by the test itself, from the parent, with full
permissions. What the tests establish is narrower: given that a write happened,
the comparison reports it, and given no manifest, the comparison does not
report success.

The mutations are the point. Each one is a different way a tree can change, and
a comparison that catches content but not mode, or content but not absence, is
a comparison that reads INTACT over a cell that was written to.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

import attest
import gauge


class DeltaDetectionTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.cell = self.tmp / "cell"
        (self.cell / "evidence").mkdir(parents=True)
        (self.cell / "evidence" / "finding.txt").write_text("bytes", encoding="utf-8")
        self.pre = attest.freeze("pre", self.cell)

    def tearDown(self):
        self._tmp.cleanup()

    def post(self):
        return attest.freeze("post", self.cell)

    def assert_bypassed(self, change: str):
        report = attest.compare(self.pre, self.post())
        self.assertEqual(report["integrity"], attest.BYPASSED, report)
        self.assertIn(change, [d["change"] for d in report["deltas"]])
        return report

    def test_no_change_reports_intact(self):
        report = attest.compare(self.pre, self.post())
        self.assertEqual(report["integrity"], attest.INTACT)
        self.assertEqual(report["deltas"], [])

    def test_content_change_is_bypassed(self):
        (self.cell / "evidence" / "finding.txt").write_text("tampered", encoding="utf-8")
        self.assert_bypassed("content_changed")

    def test_same_length_content_change_is_bypassed(self):
        # Equal size, so anything comparing stat() alone would read INTACT.
        (self.cell / "evidence" / "finding.txt").write_text("BYTES", encoding="utf-8")
        self.assert_bypassed("content_changed")

    def test_new_file_is_bypassed(self):
        (self.cell / "planted.txt").write_text("x", encoding="utf-8")
        self.assert_bypassed("created")

    def test_removed_file_is_bypassed(self):
        (self.cell / "evidence" / "finding.txt").unlink()
        self.assert_bypassed("removed")

    def test_empty_directory_creation_is_bypassed(self):
        (self.cell / "newdir").mkdir()
        self.assert_bypassed("created")

    def test_mode_change_alone_is_bypassed(self):
        # The chmod-back case: bytes identical, permissions moved. A write
        # happened, and a comparison that only hashes content would miss it.
        target = self.cell / "evidence" / "finding.txt"
        os.chmod(target, 0o666)
        report = self.assert_bypassed("mode_changed")
        self.assertEqual(report["deltas"][0]["before"]["sha256"],
                         report["deltas"][0]["after"]["sha256"])

    def test_directory_mode_change_alone_is_bypassed(self):
        # A sealed cell directory is 0o555. To create a file inside it a
        # same-UID child must first restore the write bit, so a directory left
        # at 0o755 is the trace of that step even when nothing was left behind.
        os.chmod(self.cell / "evidence", 0o555)
        pre = attest.freeze("pre", self.cell)
        os.chmod(self.cell / "evidence", 0o755)
        report = attest.compare(pre, self.post())
        self.assertEqual(report["integrity"], attest.BYPASSED, report)
        self.assertEqual([d["change"] for d in report["deltas"]], ["mode_changed"])

    def test_chmod_out_and_back_with_nothing_left_is_not_detectable(self):
        # Stated as a test so the limit is on the record rather than implied.
        # A before/after snapshot compares two moments; a child that restores
        # every byte and every mode bit leaves this instrument nothing to see.
        # Catching that needs a monitor during the run, not a manifest after it.
        os.chmod(self.cell / "evidence", 0o555)
        pre = attest.freeze("pre", self.cell)
        os.chmod(self.cell / "evidence", 0o755)
        scratch = self.cell / "evidence" / "transient.txt"
        scratch.write_text("came and went", encoding="utf-8")
        scratch.unlink()
        os.chmod(self.cell / "evidence", 0o555)
        self.assertEqual(attest.compare(pre, self.post())["integrity"],
                         attest.INTACT)

    def test_new_symlink_is_bypassed(self):
        (self.cell / "escape").symlink_to(self.tmp)
        self.assert_bypassed("created")

    def test_retargeted_symlink_is_bypassed(self):
        link = self.cell / "link"
        link.symlink_to(self.cell / "evidence")
        pre = attest.freeze("pre", self.cell)
        link.unlink()
        link.symlink_to(self.tmp)
        report = attest.compare(pre, self.post())
        self.assertEqual(report["integrity"], attest.BYPASSED)
        self.assertIn("symlink_retargeted", [d["change"] for d in report["deltas"]])

    def test_symlink_is_recorded_by_target_not_followed(self):
        outside = self.tmp / "outside.txt"
        outside.write_text("host bytes", encoding="utf-8")
        (self.cell / "link").symlink_to(outside)
        entry = attest.freeze("pre", self.cell).entries["link"]
        self.assertEqual(entry["kind"], "symlink")
        self.assertNotIn("sha256", entry)

    def test_file_replaced_by_directory_is_bypassed(self):
        target = self.cell / "evidence" / "finding.txt"
        target.unlink()
        target.mkdir()
        self.assert_bypassed("kind_changed")


class MissingManifestTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.cell = Path(self._tmp.name) / "cell"
        self.cell.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def test_absent_pre_attest_is_unknown_not_intact(self):
        report = attest.compare(None, attest.freeze("post", self.cell))
        self.assertEqual(report["integrity"], attest.UNKNOWN)
        self.assertIn("pre-attest", report["detail"])

    def test_absent_post_attest_is_unknown_not_intact(self):
        report = attest.compare(attest.freeze("pre", self.cell), None)
        self.assertEqual(report["integrity"], attest.UNKNOWN)

    def test_both_absent_is_unknown(self):
        self.assertEqual(attest.compare(None, None)["integrity"], attest.UNKNOWN)

    def test_two_pre_manifests_do_not_compare(self):
        a = attest.freeze("pre", self.cell)
        b = attest.freeze("pre", self.cell)
        self.assertEqual(attest.compare(a, b)["integrity"], attest.UNKNOWN)

    def test_attestation_is_frozen(self):
        taken = attest.freeze("pre", self.cell)
        with self.assertRaises(Exception):
            taken.phase = "post"

    def test_invalid_phase_is_refused_at_freeze(self):
        with self.assertRaises(attest.AttestError):
            attest.freeze("interim", self.cell)

    def test_missing_cell_root_is_refused_rather_than_empty(self):
        with self.assertRaises(attest.AttestError):
            attest.freeze("pre", self.cell / "does-not-exist")


class BindingTests(unittest.TestCase):
    """The two sides of a comparison must be talking about the same thing."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.a = self.tmp / "a"
        self.b = self.tmp / "b"
        for path in (self.a, self.b):
            (path / "runner").mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def test_different_cell_roots_do_not_compare(self):
        report = attest.compare(attest.freeze("pre", self.a),
                                attest.freeze("post", self.b))
        self.assertEqual(report["integrity"], attest.UNKNOWN)
        self.assertIn("different cell roots", report["detail"])

    def test_widening_scratch_after_the_fact_is_refused(self):
        # The fitting attack: take pre with nothing excused, find a delta, then
        # take post declaring the offending directory as scratch. The result is
        # UNKNOWN, not INTACT.
        pre = attest.freeze("pre", self.a, scratch_prefixes=())
        (self.a / "runner" / "session.json").write_text("{}", encoding="utf-8")
        post = attest.freeze("post", self.a, scratch_prefixes=("runner",))
        report = attest.compare(pre, post)
        self.assertEqual(report["integrity"], attest.UNKNOWN)
        self.assertIn("cannot be restated", report["detail"])

    def test_declared_scratch_write_is_reported_but_not_bypassed(self):
        pre = attest.freeze("pre", self.a, scratch_prefixes=("runner",))
        (self.a / "runner" / "session.json").write_text("{}", encoding="utf-8")
        post = attest.freeze("post", self.a, scratch_prefixes=("runner",))
        report = attest.compare(pre, post)
        self.assertEqual(report["integrity"], attest.INTACT)
        self.assertEqual(len(report["scratch_deltas"]), 1)
        self.assertEqual(report["deltas"], [])

    def test_write_outside_the_scratch_region_is_still_bypassed(self):
        pre = attest.freeze("pre", self.a, scratch_prefixes=("runner",))
        (self.a / "elsewhere.txt").write_text("x", encoding="utf-8")
        post = attest.freeze("post", self.a, scratch_prefixes=("runner",))
        self.assertEqual(attest.compare(pre, post)["integrity"], attest.BYPASSED)

    def test_scratch_prefix_does_not_match_by_string_prefix(self):
        # "runner" must not excuse "runner-notes": path components, not
        # characters. A string-prefix implementation passes every other test
        # in this class and fails this one.
        (self.a / "runner-notes").mkdir()
        pre = attest.freeze("pre", self.a, scratch_prefixes=("runner",))
        (self.a / "runner-notes" / "x.txt").write_text("x", encoding="utf-8")
        post = attest.freeze("post", self.a, scratch_prefixes=("runner",))
        self.assertEqual(attest.compare(pre, post)["integrity"], attest.BYPASSED)


class ExternalPathTests(unittest.TestCase):
    """SPEC §4: attest hashes the contract and the runner, not only the cell."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.cell = self.tmp / "cell"
        self.cell.mkdir()
        self.contract = self.tmp / "contract.json"
        self.contract.write_text('{"contract_version": 1}', encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_contract_change_between_pre_and_post_is_bypassed(self):
        pre = attest.freeze("pre", self.cell, external_paths=(self.contract,))
        self.contract.write_text('{"contract_version": 2}', encoding="utf-8")
        post = attest.freeze("post", self.cell, external_paths=(self.contract,))
        self.assertEqual(attest.compare(pre, post)["integrity"], attest.BYPASSED)

    def test_contract_removed_between_pre_and_post_is_bypassed(self):
        pre = attest.freeze("pre", self.cell, external_paths=(self.contract,))
        self.contract.unlink()
        post = attest.freeze("post", self.cell, external_paths=(self.contract,))
        report = attest.compare(pre, post)
        self.assertEqual(report["integrity"], attest.BYPASSED)

    def test_absent_external_path_is_recorded_not_skipped(self):
        taken = attest.freeze("pre", self.cell, external_paths=(self.tmp / "nope",))
        self.assertEqual(list(taken.external.values())[0]["kind"], "absent")


class ManifestSerialisationTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.cell = Path(self._tmp.name) / "cell"
        self.cell.mkdir()
        (self.cell / "f.txt").write_text("a", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_canonical_form_is_stable_across_freezes(self):
        first = attest.freeze("pre", self.cell)
        second = attest.freeze("pre", self.cell)
        self.assertEqual(first.canonical(), second.canonical())
        self.assertEqual(first.root_hash(), second.root_hash())

    def test_root_hash_moves_when_content_moves(self):
        before = attest.freeze("pre", self.cell).root_hash()
        (self.cell / "f.txt").write_text("b", encoding="utf-8")
        self.assertNotEqual(before, attest.freeze("pre", self.cell).root_hash())

    def test_canonical_form_is_json_with_sorted_keys(self):
        text = attest.freeze("pre", self.cell).canonical()
        self.assertEqual(text, json.dumps(json.loads(text), sort_keys=True,
                                          separators=(",", ":")))


class GaugeHandoffTests(unittest.TestCase):
    """as_check must land in gauge's vocabulary, not near it."""

    CONTRACT = {
        "contract_version": 1,
        "contract_id": "attest-handoff-test",
        "runner_id": "blacksmith-gauge-1",
        "precedence": gauge.CANONICAL_PRECEDENCE,
        "required_checks": ["cell_integrity"],
    }

    def bundle_with(self, entry):
        return {
            "bundle_version": 1,
            "contract_sha256": "deadbeef",
            "runner": {"id": "blacksmith-gauge-1"},
            "checks": {"cell_integrity": entry},
        }

    def adjudicate(self, integrity_report):
        entry = attest.as_check(integrity_report)
        return gauge.adjudicate(self.bundle_with(entry), self.CONTRACT, "deadbeef")

    def test_intact_reaches_active(self):
        report = attest._report(attest.INTACT, [], [], "clean")
        self.assertEqual(self.adjudicate(report)["verdict"], "ACTIVE")

    def test_bypassed_reaches_bypassed(self):
        report = attest._report(attest.BYPASSED, [{"path": "x"}], [], "delta")
        self.assertEqual(self.adjudicate(report)["verdict"], "BYPASSED")

    def test_unknown_omits_the_outcome_key_and_reaches_unknown(self):
        report = attest._report(attest.UNKNOWN, [], [], "no manifest")
        entry = attest.as_check(report)
        self.assertNotIn("outcome", entry)
        result = self.adjudicate(report)
        self.assertEqual(result["verdict"], "UNKNOWN")
        self.assertIn("check_indeterminate", [r["code"] for r in result["reasons"]])


if __name__ == "__main__":
    unittest.main()
