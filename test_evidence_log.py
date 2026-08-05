"""Coverage for evidence_log.py.

Checks the schema is enforced (every field required, verdict pinned to
gauge.VERDICTS) and that render/write do not silently accept a partial
entry — the module's whole reason to exist is refusing that.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import evidence_log as ev


def launch(**over):
    kwargs = dict(launched_by="uid:501/pid:1234", started_at="2026-08-05T18:00:00Z",
                  kernel_digest="sha256:56656c7f065f", job_digest="sha256:bb031466be2e",
                  evidence_mode="copy")
    kwargs.update(over)
    return ev.LaunchRecord(**kwargs)


def execution(**over):
    kwargs = dict(first_token="12s", final_token="340s", exit_code="0")
    kwargs.update(over)
    return ev.Execution(**kwargs)


def integrity(**over):
    kwargs = dict(cell_pre_hash="a" * 64, cell_post_hash="a" * 64,
                  delta="CLEAN", verdict="ACTIVE")
    kwargs.update(over)
    return ev.IntegrityReport(**kwargs)


class FieldValidationTests(unittest.TestCase):
    def test_launch_record_rejects_empty_field(self):
        with self.assertRaises(ev.EvidenceLogError):
            launch(launched_by="")

    def test_launch_record_rejects_missing_field(self):
        with self.assertRaises(TypeError):
            ev.LaunchRecord(launched_by="x", started_at="x", kernel_digest="x",
                             job_digest="x")  # evidence_mode omitted

    def test_execution_rejects_empty_field(self):
        with self.assertRaises(ev.EvidenceLogError):
            execution(exit_code="")

    def test_integrity_rejects_bad_delta(self):
        with self.assertRaises(ev.EvidenceLogError):
            integrity(delta="SUSPICIOUS")

    def test_integrity_rejects_bad_verdict(self):
        with self.assertRaises(ev.EvidenceLogError):
            integrity(verdict="PASS")

    def test_integrity_accepts_every_gauge_verdict(self):
        for verdict in ("ACTIVE", "FAILED", "UNKNOWN", "BYPASSED"):
            with self.subTest(verdict=verdict):
                integrity(verdict=verdict)  # must not raise

    def test_integrity_rejects_empty_hash(self):
        with self.assertRaises(ev.EvidenceLogError):
            integrity(cell_pre_hash="")


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.text = ev.render(
            "verify", "qwen3.5:9b", "20260805T180000",
            launch(), execution(), integrity(),
            "The instrument is only as good as what it is given to check.",
        )

    def test_header_names_job_model_timestamp(self):
        self.assertIn("# verify · qwen3.5:9b · 20260805T180000", self.text)

    def test_all_five_sections_present_in_order(self):
        order = ["## Launch Record", "## Execution", "## Integrity Report",
                  "## Proof Chain", "## Lesson"]
        positions = [self.text.index(h) for h in order]
        self.assertEqual(positions, sorted(positions))

    def test_proof_chain_is_the_fixed_prose(self):
        self.assertIn("All four together = proof that session ran and "
                       "output is credible", self.text)

    def test_lesson_is_included_verbatim(self):
        self.assertIn("The instrument is only as good as what it is given "
                       "to check.", self.text)

    def test_rejects_empty_job(self):
        with self.assertRaises(ev.EvidenceLogError):
            ev.render("", "qwen3.5:9b", "20260805T180000",
                       launch(), execution(), integrity(), "lesson")

    def test_rejects_empty_lesson(self):
        with self.assertRaises(ev.EvidenceLogError):
            ev.render("verify", "qwen3.5:9b", "20260805T180000",
                       launch(), execution(), integrity(), "   ")

    def test_rejects_wrong_type_for_launch(self):
        with self.assertRaises(ev.EvidenceLogError):
            ev.render("verify", "qwen3.5:9b", "20260805T180000",
                       {"not": "a LaunchRecord"}, execution(), integrity(), "lesson")


class WriteTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.out_dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_write_uses_job_model_timestamp_filename(self):
        target = ev.write("verify", "qwen3.5:9b", "20260805T180000",
                           launch(), execution(), integrity(), "lesson",
                           out_dir=self.out_dir)
        self.assertEqual(target.name, "verify.qwen3.5-9b.20260805T180000.md")
        self.assertTrue(target.is_file())

    def test_write_refuses_to_overwrite_existing_entry(self):
        ev.write("verify", "qwen3.5:9b", "20260805T180000",
                  launch(), execution(), integrity(), "lesson",
                  out_dir=self.out_dir)
        with self.assertRaises(ev.EvidenceLogError):
            ev.write("verify", "qwen3.5:9b", "20260805T180000",
                      launch(), execution(), integrity(), "a different lesson",
                      out_dir=self.out_dir)

    def test_write_creates_out_dir_if_absent(self):
        nested = self.out_dir / "nested" / "runs"
        target = ev.write("verify", "qwen3.5:9b", "20260805T180000",
                           launch(), execution(), integrity(), "lesson",
                           out_dir=nested)
        self.assertTrue(target.is_file())


if __name__ == "__main__":
    unittest.main()
