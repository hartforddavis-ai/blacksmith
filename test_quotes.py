"""Coverage for quotes.check -- does a VERIFIED row quote the pasted bytes.

Each case is tied to a named failure. The first is the negative control and
is the one that matters most: without it a check that rejected every row
would pass every other test here and look correct.

The stitching pair (`test_elision_across...` / `test_elision_within...`) is
one finding split in two on purpose. Refusing a stitched quote is only worth
anything if an honest elision still passes; a check that failed both would
satisfy the first test by banning elisions outright, which would reject every
legitimate quote in a real reply.
"""

from __future__ import annotations

import unittest

import quotes

# Stands in for the pasted material. The two anchors sit far apart so a quote
# stitching them cannot land inside one window.
CORPUS = {"SPEC": quotes.normalise(
    "Step 0 decides affordability of everything. One test. "
    + "filler sentence that carries the distance between them. " * 12
    + "Read-scope confinement is policy denial, not capability absence, "
      "and the gate remains OPEN until it is exercised."
)}


def table(verdict: str, evidence: str) -> str:
    return (
        "TOOLS HELD: <none>\n\n"
        "| Item | Ruled | Verdict | Evidence |\n"
        "|---|---|---|---|\n"
        f"| a thing | APPROVE | {verdict} | {evidence} |\n"
    )


class CheckTests(unittest.TestCase):
    def test_a_real_quote_in_a_verified_row_is_clean(self):
        reply = table("VERIFIED", 'SPEC: "Read-scope confinement is policy denial"')
        self.assertEqual(quotes.check(reply, CORPUS), [])

    def test_verified_row_with_no_quote_is_reported(self):
        reply = table("VERIFIED", "SPEC supports this generally")
        findings = quotes.check(reply, CORPUS)
        self.assertEqual([f["reason"] for f in findings], ["NO_QUOTE"])

    def test_quote_absent_from_every_source_is_reported(self):
        reply = table("VERIFIED", '"a line nobody ever wrote anywhere"')
        findings = quotes.check(reply, CORPUS)
        self.assertEqual([f["reason"] for f in findings], ["NOT_IN_SOURCE"])

    def test_elision_across_distant_passages_is_reported(self):
        # The 5 Aug fabrication: both halves are real, hundreds of characters
        # apart, and the pairing the row claims does not exist.
        reply = table("VERIFIED", '"Step 0 ... OPEN"')
        findings = quotes.check(reply, CORPUS)
        self.assertEqual([f["reason"] for f in findings], ["NOT_IN_SOURCE"])

    def test_elision_within_one_passage_is_clean(self):
        reply = table("VERIFIED",
                      '"Read-scope confinement ... capability absence"')
        self.assertEqual(quotes.check(reply, CORPUS), [])

    def test_a_reply_with_no_engagement_line_is_refused_not_passed(self):
        # !34: a cell where nothing ran is trivially delta-free upstream in
        # attest.compare. Same gap, the reply's own side of it: an empty or
        # never-generated reply has no first line to match, and must not
        # read the same as a real reply that happens to have no rows yet.
        findings = quotes.check("", CORPUS)
        self.assertEqual([f["reason"] for f in findings], ["NO_ENGAGEMENT"])

    def test_engagement_line_survives_markdown_emphasis(self):
        # Every other match in this module runs through normalise() because
        # markdown is the transport's, not the model's — a bolded
        # declaration split across spans must still be recognised.
        reply = "**TOOLS** **HELD**: none\n\n" + table("VERIFIED",
            '"Read-scope confinement is policy denial"').split("\n\n", 1)[1]
        self.assertEqual(quotes.check(reply, CORPUS), [])

    def test_a_reply_that_skips_straight_to_rows_is_refused(self):
        # K1 requires the declaration first, before anything else. A reply
        # that ignores K1 but still produces a well-formed table must not
        # pass just because the rows happen to check out.
        reply = table("VERIFIED", '"Read-scope confinement is policy denial"')
        reply = reply.split("\n\n", 1)[1]  # strip the TOOLS HELD line only
        findings = quotes.check(reply, CORPUS)
        self.assertEqual([f["reason"] for f in findings], ["NO_ENGAGEMENT"])

    def test_a_reply_with_no_ruled_rows_is_refused_not_passed(self):
        # A header-only run file reported clean before this: nothing was
        # compared, and the check said so as a pass. Same defect as
        # tests_pass certifying an empty suite, rebuilt here the same day.
        findings = quotes.check("TOOLS HELD: <none>\n\n# verify\n", CORPUS)
        self.assertEqual([f["reason"] for f in findings], ["NO_ROWS"])

    def test_rows_that_are_not_verified_are_not_checked(self):
        # A real reply carries far more negative rows than positive ones, and
        # they paraphrase freely. K3 binds positive verdicts only.
        reply = table("MISQUOTED", '"a line nobody ever wrote anywhere"')
        self.assertEqual(quotes.check(reply, CORPUS), [])


if __name__ == "__main__":
    unittest.main()
