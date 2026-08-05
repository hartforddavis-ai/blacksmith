#!/usr/bin/env python3.12
"""The founding invariant, exercised under the failure condition.

A model cannot raise a claim's provenance. Every test here tries to make that
happen and checks that it did not. The happy path — evidence present, claim
CONFIRMED — is the least interesting case and is covered once.

    python3.12 test_provenance.py
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

import claims as claims_mod


def _claim(**over) -> dict:
    base = {"id": "C-0001", "text": "guard rejects None",
            "subject_files": ["src/guard.py"], "raised_cycle": 1}
    base.update(over)
    return base


def _machine(digest: str, passed: bool = True) -> dict:
    return {"at": "2026-07-31T00:00:00Z", "kind": "tests",
            "passed": passed, "files_digest": digest}


def _review(digest: str, verdict: str = "PROVES", role: str = "checker",
            vendor: str = "gemini") -> dict:
    return {"at": "2026-07-31T00:00:00Z", "vendor": vendor, "role": role,
            "verdict": verdict, "files_digest": digest}


class ProvenanceTests(unittest.TestCase):
    """Each test builds a throwaway repo root: a .git marker and one file."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / ".git").mkdir()
        (self.root / "src").mkdir()
        (self.root / "src" / "guard.py").write_text(
            "def check(x):\n    return x is not None\n", encoding="utf-8")
        self.digest = claims_mod.digest_files(["src/guard.py"], self.root)
        self.addCleanup(self._tmp.cleanup)

    def test_bare_claim_is_asserted(self):
        claim = _claim()
        self.assertEqual(claims_mod.provenance(claim, self.root), "ASSERTED")
        self.assertFalse(claims_mod.closes_gate(claim, self.root))

    def test_machine_alone_does_not_close_a_gate(self):
        claim = _claim(machine=[_machine(self.digest)])
        self.assertEqual(claims_mod.provenance(claim, self.root), "MACHINE")
        self.assertFalse(claims_mod.closes_gate(claim, self.root))

    def test_review_alone_does_not_close_a_gate(self):
        claim = _claim(reviews=[_review(self.digest)])
        self.assertEqual(claims_mod.provenance(claim, self.root), "REVIEWED")
        self.assertFalse(claims_mod.closes_gate(claim, self.root))

    def test_both_legs_confirm(self):
        claim = _claim(machine=[_machine(self.digest)],
                       reviews=[_review(self.digest)])
        self.assertEqual(claims_mod.provenance(claim, self.root), "CONFIRMED")
        self.assertTrue(claims_mod.closes_gate(claim, self.root))

    def test_one_byte_changed_decays_confirmed_to_stale(self):
        claim = _claim(machine=[_machine(self.digest)],
                       reviews=[_review(self.digest)])
        self.assertEqual(claims_mod.provenance(claim, self.root), "CONFIRMED")

        target = self.root / "src" / "guard.py"
        target.write_text(target.read_text(encoding="utf-8") + "\n",
                          encoding="utf-8")

        self.assertEqual(claims_mod.provenance(claim, self.root), "STALE")
        self.assertFalse(claims_mod.closes_gate(claim, self.root))

    def test_deleting_a_reviewed_file_invalidates_the_review(self):
        claim = _claim(machine=[_machine(self.digest)],
                       reviews=[_review(self.digest)])
        (self.root / "src" / "guard.py").unlink()
        self.assertEqual(claims_mod.provenance(claim, self.root), "STALE")

    def test_failing_machine_row_is_not_evidence(self):
        claim = _claim(machine=[_machine(self.digest, passed=False)],
                       reviews=[_review(self.digest)])
        self.assertEqual(claims_mod.provenance(claim, self.root), "REVIEWED")

    def test_does_not_prove_is_not_evidence(self):
        claim = _claim(machine=[_machine(self.digest)],
                       reviews=[_review(self.digest, verdict="DOES_NOT_PROVE")])
        self.assertEqual(claims_mod.provenance(claim, self.root), "MACHINE")

    def test_partial_is_not_evidence(self):
        claim = _claim(machine=[_machine(self.digest)],
                       reviews=[_review(self.digest, verdict="PARTIAL")])
        self.assertEqual(claims_mod.provenance(claim, self.root), "MACHINE")

    def test_a_same_family_review_cannot_confirm(self):
        """Haiku is Claude. Relabelling it 'checker' does not make it a checker."""
        for vendor in ("haiku", "claude-haiku-4-5", "Opus 5", "sonnet"):
            claim = _claim(machine=[_machine(self.digest)],
                           reviews=[_review(self.digest, vendor=vendor)])
            self.assertEqual(claims_mod.provenance(claim, self.root), "MACHINE",
                             f"{vendor} was treated as independent")

    def test_recognised_external_vendors_are_independent(self):
        for vendor in ("gemini-flash-lite", "chatgpt", "grok-4", "gpt-5.5"):
            self.assertTrue(claims_mod.is_independent(vendor), vendor)

    def test_unknown_vendor_is_allowed_through(self):
        self.assertTrue(claims_mod.is_independent("some-new-lab"))

    def test_tiebreak_alone_cannot_confirm(self):
        """A tiebreak resolves a disagreement; it is not a standing leg."""
        claim = _claim(machine=[_machine(self.digest)],
                       reviews=[_review(self.digest, role="tiebreak")])
        self.assertEqual(claims_mod.provenance(claim, self.root), "MACHINE")

    def test_stale_evidence_cannot_be_replayed_by_adding_a_new_claim(self):
        """A digest from other bytes never matches, however it is introduced."""
        claim = _claim(machine=[_machine("0" * 64)],
                       reviews=[_review("0" * 64)])
        self.assertEqual(claims_mod.provenance(claim, self.root), "STALE")

    def test_forged_provenance_field_is_ignored(self):
        """Writing CONFIRMED into the ledger by hand achieves nothing."""
        path = self.root / "claims.json"
        forged = _claim(provenance="CONFIRMED", verified=True,
                        note="Gemini independent review completed")
        claims_mod.save(path, [forged])

        loaded = claims_mod.load(path)[0]
        self.assertEqual(claims_mod.provenance(loaded, self.root), "ASSERTED")
        self.assertFalse(claims_mod.closes_gate(loaded, self.root))

    def test_disagreement_is_recorded_not_resolved(self):
        claim = _claim(reviews=[
            _review(self.digest, verdict="PROVES"),
            _review(self.digest, verdict="DOES_NOT_PROVE", vendor="grok"),
        ])
        found = claims_mod.disagreements(claim)
        self.assertEqual({d["verdict"] for d in found},
                         {"PROVES", "DOES_NOT_PROVE"})

    def test_agreement_is_not_a_disagreement(self):
        claim = _claim(reviews=[
            _review(self.digest, vendor="gemini"),
            _review(self.digest, vendor="grok"),
        ])
        self.assertEqual(claims_mod.disagreements(claim), [])

    def test_digest_distinguishes_absent_from_empty(self):
        (self.root / "src" / "guard.py").write_text("", encoding="utf-8")
        when_empty = claims_mod.digest_files(["src/guard.py"], self.root)
        (self.root / "src" / "guard.py").unlink()
        when_absent = claims_mod.digest_files(["src/guard.py"], self.root)
        self.assertNotEqual(when_empty, when_absent)

    def test_repo_root_is_anchored_to_file_not_cwd(self):
        """The secure_import lesson: cwd must not be able to move the root."""
        anchored = claims_mod.repo_root(Path(__file__))
        cwd = os.getcwd()
        try:
            os.chdir(self.root)
            self.assertEqual(claims_mod.repo_root(Path(__file__)), anchored)
        finally:
            os.chdir(cwd)


class ValidationTests(unittest.TestCase):
    def test_subject_files_reject_traversal(self):
        with self.assertRaisesRegex(claims_mod.ClaimsError, "repo-relative"):
            claims_mod.validate([_claim(subject_files=["../../etc/passwd"])])

    def test_subject_files_reject_absolute_paths(self):
        with self.assertRaisesRegex(claims_mod.ClaimsError, "repo-relative"):
            claims_mod.validate([_claim(subject_files=["/etc/passwd"])])

    def test_empty_subject_files_rejected(self):
        with self.assertRaisesRegex(claims_mod.ClaimsError, "non-empty list"):
            claims_mod.validate([_claim(subject_files=[])])

    def test_duplicate_claim_ids_rejected(self):
        with self.assertRaisesRegex(claims_mod.ClaimsError, "duplicate"):
            claims_mod.validate([_claim(), _claim()])

    def test_unknown_review_role_rejected(self):
        with self.assertRaisesRegex(claims_mod.ClaimsError, "role"):
            claims_mod.validate([_claim(reviews=[
                {"vendor": "x", "role": "generator", "verdict": "PROVES",
                 "files_digest": "d"}])])

    def test_unknown_verdict_rejected(self):
        with self.assertRaisesRegex(claims_mod.ClaimsError, "verdict"):
            claims_mod.validate([_claim(reviews=[
                {"vendor": "x", "role": "checker", "verdict": "CONFIRMED",
                 "files_digest": "d"}])])

    def test_review_without_digest_rejected(self):
        with self.assertRaisesRegex(claims_mod.ClaimsError, "files_digest"):
            claims_mod.validate([_claim(reviews=[
                {"vendor": "x", "role": "checker", "verdict": "PROVES"}])])

    def test_machine_row_needs_boolean_passed(self):
        with self.assertRaisesRegex(claims_mod.ClaimsError, "boolean"):
            claims_mod.validate([_claim(machine=[
                {"kind": "tests", "passed": "yes", "files_digest": "d"}])])


if __name__ == "__main__":
    unittest.main()
