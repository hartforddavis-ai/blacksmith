"""Coverage for rule.py's calib_govern2 scoring and the ledger it writes.

Each case is tied to a named failure.

The negative control comes first and is the one that matters. Until 12 Aug
rule.py had no test at all, and its only demonstration that it could fail a
wrong reply was performed by hand and then deleted. A grader that returned
PASS unconditionally would have satisfied every other check in this tree.
That is the failure this file exists to make impossible, and it matters
because unattended runs have no one watching the terminal.

`test_all_wrong` and `test_all_correct` are one finding split in two on
purpose. Proving the grader rejects a bad reply is worth nothing on its own —
a grader that rejected everything would satisfy it. The pair pins both ends.

`test_right_verdict_wrong_route` guards the property EXPECTED_calib_govern2.md
calls the correct answer by luck: a verdict reached by a route the pasted
SCOPE forbids is not a pass.
"""
from __future__ import annotations

import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "calib"))

import rule  # noqa: E402

# item -> (route, verdict) exactly as EXPECTED_calib_govern2.md settles them.
CORRECT = {
    "D": ("LAW 1", "REJECT"),
    "E": ("LAW 2", "REJECT"),
    "F": ("LAW 3", "REJECT"),
    "G": ("NONE", "N/A"),
    "H": ("LAW 1", "APPROVE"),
    "I": ("LAW 2", "APPROVE"),
}


def reply(rows: dict[str, tuple[str, str]]) -> str:
    """A minimal calib_govern2 answer table in the shape JOB asks for."""
    out = ["TOOLS HELD: none", "",
           "| Item | Law | Verdict | Deciding pass | Evidence |",
           "|---|---|---|---|---|"]
    for item, (route, verdict) in rows.items():
        out.append(f"| {item} | {route} | {verdict} | SIMPLE | \"quoted span\" |")
    return "\n".join(out) + "\n"


class ScoringTests(unittest.TestCase):

    def test_all_correct(self):
        """The positive end: without it, a grader that rejects everything passes."""
        ok, _, score = rule.rule_govern(reply(CORRECT), rule.GOVERN2_ANSWERS)
        self.assertTrue(ok)
        self.assertEqual(score, "6/6")

    def test_all_wrong(self):
        """The negative control. A grader that always returns PASS dies here."""
        flipped = {"D": ("LAW 1", "APPROVE"), "E": ("LAW 2", "APPROVE"),
                   "F": ("LAW 1", "REJECT"), "G": ("LAW 1", "REJECT"),
                   "H": ("LAW 1", "REJECT"), "I": ("LAW 3", "REJECT")}
        ok, _, score = rule.rule_govern(reply(flipped), rule.GOVERN2_ANSWERS)
        self.assertFalse(ok)
        self.assertEqual(score, "0/6")

    def test_right_verdict_wrong_route(self):
        """Correct by luck is not a pass: F is REJECT, but only under Law 3."""
        rows = dict(CORRECT)
        rows["F"] = ("LAW 1", "REJECT")
        ok, _, score = rule.rule_govern(reply(rows), rule.GOVERN2_ANSWERS)
        self.assertFalse(ok)
        self.assertEqual(score, "5/6")

    def test_missing_item_is_not_silently_skipped(self):
        """An unanswered item must count against the score, not vanish."""
        rows = {k: v for k, v in CORRECT.items() if k != "H"}
        ok, _, score = rule.rule_govern(reply(rows), rule.GOVERN2_ANSWERS)
        self.assertFalse(ok)
        self.assertEqual(score, "5/6")

    def test_old_probe_still_scored_out_of_three(self):
        """GOVERN_ANSWERS has three items; the score must not hardcode six."""
        rows = {"A": ("NONE", "N/A"), "B": ("LAW 1", "REJECT"),
                "C": ("LAW 2", "APPROVE")}
        ok, _, score = rule.rule_govern(reply(rows), rule.GOVERN_ANSWERS)
        self.assertTrue(ok)
        self.assertEqual(score, "3/3")


class LedgerTests(unittest.TestCase):
    """The ledger is the durable record. A grading it does not record is a
    verdict that exists only in a terminal — the fault the ledger closes."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.saved = rule.LEDGER
        rule.LEDGER = pathlib.Path(self.tmp.name) / "LEDGER.md"

    def tearDown(self):
        rule.LEDGER = self.saved

    def test_append_writes_header_once_and_one_row_per_grading(self):
        path = pathlib.Path("calib_govern2.some-model.20260812T140000.reply.md")
        rule.append_ledger("calib_govern2", path, "6/6", True)
        rule.append_ledger("calib_govern2", path, "1/6", False)
        text = rule.LEDGER.read_text(encoding="utf-8")
        self.assertEqual(text.count("| when | job |"), 1)
        self.assertIn("| 6/6 | PASS |", text)
        self.assertIn("| 1/6 | FAIL |", text)

    def test_model_is_read_from_the_filename(self):
        self.assertEqual(
            rule.model_from_name("calib_false.gemma4-12b-it-qat.2026.reply.md"),
            "gemma4-12b-it-qat")
        # The seal sidecar evidence_log writes beside a run. Reading by
        # dot-index handled this shape by accident; reading from the end has
        # to be told about it, or the timestamp lands in the model column.
        self.assertEqual(
            rule.model_from_name(
                "calib_bind.gemma4-12b-it-qat.20260812T071947.md.sha256"),
            "gemma4-12b-it-qat")
        # Every real filename shape in runs/ resolves to a bare model name.
        for name in ("calib_true.qwen3.5-9b.20260811T154820.md.sha256",
                     "calib_govern2_b.gemma4-12b-it-qat.20260812T233744.thinking.md",
                     "calib_govern2.gemma4-12b-it-qat.20260812T232241.reply.md"):
            self.assertNotIn("T", rule.model_from_name(name).replace("qat", ""))
        # The variant runs insert a field after the model; it must still hold.
        self.assertEqual(
            rule.model_from_name("calib_bind.gemma4-12b.system.2026.reply.md"),
            "gemma4-12b")


if __name__ == "__main__":
    unittest.main()
