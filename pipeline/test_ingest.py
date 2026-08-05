#!/usr/bin/env python3.12
"""Every way a verdict can be refused, and the one way it is accepted.

The historical failure is test one: a prompt asserted an independent review that
never happened. The regression for it is that STATE.md says NONE ON RECORD no
matter what any model wrote down.

    python3.12 test_ingest.py
"""

from __future__ import annotations

import json
import tempfile
import unittest
import unittest.mock
from pathlib import Path

import bundle as bundle_mod
import canary
import claims as claims_mod
import check as check_mod
import cycle as cycle_mod
import ingest as ingest_mod
import state as state_mod


class IngestTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / ".git").mkdir()
        src = self.root / "src"
        src.mkdir()
        (src / "guard.py").write_text(
            "def check(value):\n"
            "    if value is None:\n"
            "        raise ValueError('value must not be None')\n"
            "    return value\n", encoding="utf-8")

        self.claims_path = self.root / "claims.json"
        claims_mod.save(self.claims_path, [{
            "id": "C-0001",
            "text": "guard.check rejects None",
            "subject_files": ["src/guard.py"],
            "raised_cycle": 1,
        }])
        self.out = self.root / "cycle"
        self.meta = bundle_mod.build(
            self.claims_path, 1, self.out, "auditor", [], root=self.root)
        self.log = self.out / "ingest.log.jsonl"
        self.addCleanup(self._tmp.cleanup)

    def _verdict(self, **over) -> Path:
        body = {
            "bundle_digest": self.meta["bundle_digest"],
            "grounding": {q["id"]: q["expected"] for q in self.meta["grounding"]},
            "claims": [{"id": "C-0001", "verdict": "PROVES",
                        "lines": ["src/guard.py:3"], "note": "raises on None"}],
            "findings": [{"severity": "high",
                          "file": self.meta["canary"]["filename"],
                          "line": self.meta["canary"]["line"],
                          "issue": "planted defect"}],
        }
        body.update(over)
        path = self.out / "verdict.json"
        path.write_text(json.dumps(body), encoding="utf-8")
        return path

    def _ingest(self, path: Path, role: str = "auditor"):
        return ingest_mod.ingest(path, self.out / "bundle.meta.json",
                                 self.claims_path, "gemini", role, self.log,
                                 root=self.root)

    def test_a_clean_verdict_is_accepted(self):
        outcome = self._ingest(self._verdict())
        self.assertEqual(outcome["result"], ingest_mod.ACCEPTED)
        self.assertEqual(outcome["recorded"], 1)

    def test_wrong_grounding_answer_discards_the_whole_review(self):
        first = self.meta["grounding"][0]["id"]
        answers = {q["id"]: q["expected"] for q in self.meta["grounding"]}
        answers[first] = "not what the line says"
        outcome = self._ingest(self._verdict(grounding=answers))
        self.assertEqual(outcome["result"], ingest_mod.REJECTED_GROUNDING)
        self.assertEqual(outcome["recorded"], 0)
        self.assertEqual(claims_mod.load(self.claims_path)[0].get("reviews", []), [])

    def test_unanswered_grounding_discards_the_whole_review(self):
        outcome = self._ingest(self._verdict(grounding={}))
        self.assertEqual(outcome["result"], ingest_mod.REJECTED_GROUNDING)

    def test_grounding_tolerates_reindentation_but_not_different_tokens(self):
        answers = {q["id"]: f"   {q['expected']}   "
                   for q in self.meta["grounding"]}
        self.assertEqual(self._ingest(self._verdict(grounding=answers))["result"],
                         ingest_mod.ACCEPTED)

    def test_verdict_for_a_different_bundle_is_refused(self):
        outcome = self._ingest(self._verdict(bundle_digest="0" * 64))
        self.assertEqual(outcome["result"], ingest_mod.REJECTED_UNBOUND)

    def test_citation_beyond_end_of_file_discards_the_review(self):
        outcome = self._ingest(self._verdict(claims=[
            {"id": "C-0001", "verdict": "PROVES", "lines": ["src/guard.py:9999"]}]))
        self.assertEqual(outcome["result"], ingest_mod.REJECTED_CITATION)

    def test_citation_of_a_file_not_in_the_bundle_discards_the_review(self):
        outcome = self._ingest(self._verdict(claims=[
            {"id": "C-0001", "verdict": "PROVES", "lines": ["elsewhere.py:1"]}]))
        self.assertEqual(outcome["result"], ingest_mod.REJECTED_CITATION)

    def test_no_citations_is_allowed(self):
        outcome = self._ingest(self._verdict(claims=[
            {"id": "C-0001", "verdict": "PARTIAL", "lines": [],
             "note": "could not locate the assertion"}]))
        self.assertEqual(outcome["result"], ingest_mod.ACCEPTED)

    def test_missing_the_canary_discards_the_review(self):
        """The only gate that catches a reviewer who simply did not look."""
        outcome = self._ingest(self._verdict(findings=[]))
        self.assertEqual(outcome["result"], ingest_mod.REJECTED_INSENSITIVE)
        self.assertEqual(outcome["recorded"], 0)

    def test_canary_is_not_required_of_the_checker(self):
        outcome = self._ingest(self._verdict(findings=[]), role="checker")
        self.assertEqual(outcome["result"], ingest_mod.ACCEPTED)

    def test_malformed_json_is_refused_not_read_charitably(self):
        path = self.out / "verdict.json"
        path.write_text("{not json at all", encoding="utf-8")
        self.assertEqual(self._ingest(path)["result"], ingest_mod.REJECTED_SHAPE)

    def test_unknown_verdict_value_is_refused(self):
        outcome = self._ingest(self._verdict(claims=[
            {"id": "C-0001", "verdict": "CONFIRMED", "lines": []}]))
        self.assertEqual(outcome["result"], ingest_mod.REJECTED_SHAPE)

    def test_every_rejection_is_logged(self):
        self._ingest(self._verdict(bundle_digest="0" * 64))
        self._ingest(self._verdict(findings=[]))
        rows = [json.loads(line)
                for line in self.log.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([r["result"] for r in rows],
                         [ingest_mod.REJECTED_UNBOUND,
                          ingest_mod.REJECTED_INSENSITIVE])

    def test_review_binds_to_the_claim_not_the_whole_bundle(self):
        self._ingest(self._verdict())
        row = claims_mod.load(self.claims_path)[0]["reviews"][0]
        expected = claims_mod.digest_files(["src/guard.py"], self.root)
        self.assertEqual(row["files_digest"], expected)


class StateTests(unittest.TestCase):
    """The regression for the failure that prompted the whole pipeline."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / ".git").mkdir()
        (self.root / "src").mkdir()
        (self.root / "src" / "guard.py").write_text("x = 1\n", encoding="utf-8")
        self.claims_path = self.root / "claims.json"
        self.addCleanup(self._tmp.cleanup)

    def test_a_generator_claiming_a_review_gets_none_on_record(self):
        claims_mod.save(self.claims_path, [{
            "id": "C-0001",
            "text": "Gemini independent review completed",
            "subject_files": ["src/guard.py"],
            "raised_cycle": 1,
            "provenance": "CONFIRMED",
            "note": "independent evidence confirms",
        }])
        text = state_mod.render(self.root, None, self.claims_path)
        self.assertIn("INDEPENDENT REVIEW: NONE ON RECORD", text)
        self.assertIn("| C-0001 | ASSERTED |", text)
        self.assertNotIn("✓", text)

    def test_empty_ledger_is_a_valid_state(self):
        text = state_mod.render(self.root, None, self.claims_path)
        self.assertIn("No claims raised. That is a valid state", text)

    def test_step_zero_is_never_assigned(self):
        objective = state_mod.next_objective(state_mod.build_order())
        self.assertIsNotNone(objective)
        self.assertNotEqual(objective["step"], 0)

    def test_prerequisites_gate_the_assignment(self):
        steps = [
            {"step": 1, "name": "first", "status": "OPEN", "requires": []},
            {"step": 2, "name": "second", "status": "OPEN", "requires": [1]},
        ]
        self.assertEqual(state_mod.next_objective(steps)["step"], 1)
        steps[0]["status"] = "DONE"
        self.assertEqual(state_mod.next_objective(steps)["step"], 2)


class BuildOrderTests(unittest.TestCase):
    """A step closes on evidence, or the build order never moves.

    Before this, nothing in the pipeline ever wrote DONE — the only test that
    exercised the transition set the status by hand in a fixture, so a suite
    could stay green while `start` re-assigned step 1 forever.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / ".git").mkdir()
        (self.root / "src").mkdir()
        (self.root / "src" / "guard.py").write_text("x = 1\n", encoding="utf-8")
        self.claims_path = self.root / "claims.json"
        self.steps = [
            {"step": 1, "name": "first", "status": "OPEN", "requires": []},
            {"step": 2, "name": "second", "status": "OPEN", "requires": [1]},
        ]
        self.addCleanup(self._tmp.cleanup)

    def _claim(self, cid: str, step: int, confirmed: bool) -> dict:
        digest = claims_mod.digest_files(["src/guard.py"], self.root)
        claim = {
            "id": cid,
            "text": f"{cid} holds",
            "subject_files": ["src/guard.py"],
            "raised_cycle": 1,
            "objective_step": step,
            "machine": [{"at": "now", "kind": "tests", "passed": True,
                         "files_digest": digest}],
        }
        if confirmed:
            claim["reviews"] = [{
                "at": "now", "vendor": "gemini-flash-lite", "role": "auditor",
                "transport": "browser", "verdict": "PROVES",
                "files_digest": digest, "bundle_digest": "b"}]
        return claim

    def test_a_step_closes_when_every_claim_under_it_confirms(self):
        ledger = [self._claim("C-0001", 1, True), self._claim("C-0002", 1, True)]
        self.assertTrue(claims_mod.step_is_done(ledger, 1, self.root))
        objective = state_mod.next_objective(self.steps, ledger, self.root)
        self.assertEqual(objective["step"], 2)

    def test_one_unconfirmed_claim_holds_the_step_open(self):
        ledger = [self._claim("C-0001", 1, True), self._claim("C-0002", 1, False)]
        self.assertFalse(claims_mod.step_is_done(ledger, 1, self.root))
        self.assertEqual(
            state_mod.next_objective(self.steps, ledger, self.root)["step"], 1)

    def test_a_step_with_no_claims_is_never_done(self):
        """Vacuous truth would close every step at once on a fresh checkout."""
        self.assertFalse(claims_mod.step_is_done([], 1, self.root))
        self.assertEqual(
            state_mod.next_objective(self.steps, [], self.root)["step"], 1)

    def test_evidence_decaying_reopens_a_closed_step(self):
        ledger = [self._claim("C-0001", 1, True)]
        (self.root / "src" / "guard.py").write_text("x = 2\n", encoding="utf-8")
        self.assertFalse(claims_mod.step_is_done(ledger, 1, self.root))
        self.assertEqual(
            state_mod.next_objective(self.steps, ledger, self.root)["step"], 1)

    def test_evidence_cannot_close_a_step_blocked_on_the_owner(self):
        """Step 0 is the SPEC's kill criterion. No cycle may prove it closed."""
        steps = [
            {"step": 0, "name": "kill criterion", "status": "BLOCKED_OWNER",
             "requires": []},
            {"step": 1, "name": "first", "status": "OPEN", "requires": [0]},
        ]
        ledger = [self._claim("C-0001", 0, True)]
        self.assertTrue(claims_mod.step_is_done(ledger, 0, self.root))
        self.assertIsNone(state_mod.next_objective(steps, ledger, self.root))

    def test_a_claim_with_no_step_closes_nothing(self):
        claim = self._claim("C-0001", 1, True)
        del claim["objective_step"]
        self.assertFalse(claims_mod.step_is_done([claim], 1, self.root))

    def test_load_refuses_a_cycle_that_was_never_started(self):
        cycles = self.root / "cycles"
        (cycles / "001").mkdir(parents=True)
        (cycles / "001" / "CANDIDATE.json").write_text(
            json.dumps({"claims": [{"id": "C-0001", "text": "holds",
                                    "subject_files": ["src/guard.py"]}]}),
            encoding="utf-8")
        with unittest.mock.patch.multiple(
                cycle_mod, CYCLES=cycles, CLAIMS=self.claims_path):
            with self.assertRaises(claims_mod.ClaimsError) as caught:
                cycle_mod.load_candidate(1)
        self.assertIn("objective.json", str(caught.exception))
        self.assertEqual(claims_mod.load(self.claims_path), [])

    def test_load_stamps_the_step_the_generator_was_assigned(self):
        cycles = self.root / "cycles"
        (cycles / "001").mkdir(parents=True)
        (cycles / "001" / "CANDIDATE.json").write_text(
            json.dumps({"claims": [{"id": "C-0001", "text": "holds",
                                    "subject_files": ["src/guard.py"]}]}),
            encoding="utf-8")
        (cycles / "001" / "objective.json").write_text(
            json.dumps({"cycle": 1, "step": 3, "name": "third"}),
            encoding="utf-8")
        with unittest.mock.patch.multiple(
                cycle_mod, CYCLES=cycles, CLAIMS=self.claims_path,
                LOG=self.root / "log.jsonl"):
            cycle_mod.load_candidate(1)
        self.assertEqual(claims_mod.load(self.claims_path)[0]["objective_step"], 3)


class FreezeTests(unittest.TestCase):
    """FREEZE was the string 'NOT READY', printed unconditionally.

    Under a sentence claiming it had been derived from the claim table — the
    defect this pipeline exists to catch, in the module that generates the page
    asserting nothing here is asserted.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / ".git").mkdir()
        (self.root / "src").mkdir()
        (self.root / "src" / "guard.py").write_text("x = 1\n", encoding="utf-8")
        spec = self.root / state_mod.SPEC
        spec.parent.mkdir(parents=True, exist_ok=True)
        spec.write_text("# SPEC\n\nNo open rulings.\n", encoding="utf-8")

        self.claims_path = self.root / "claims.json"
        digest = claims_mod.digest_files(["src/guard.py"], self.root)
        claims_mod.save(self.claims_path, [{
            "id": "C-0001", "text": "guard holds",
            "subject_files": ["src/guard.py"], "raised_cycle": 1,
            "objective_step": 1,
            "machine": [{"at": "now", "kind": "tests", "passed": True,
                         "files_digest": digest}],
            "reviews": [{"at": "now", "vendor": "gemini-flash-lite",
                         "role": "auditor", "transport": "browser",
                         "verdict": "PROVES", "files_digest": digest,
                         "bundle_digest": "b"}],
        }])
        self.order = self.root / "build_order.json"
        self.order.write_text(json.dumps(
            [{"step": 1, "name": "first", "status": "OPEN", "requires": [],
              "why": "the objective"}]), encoding="utf-8")
        self.addCleanup(self._tmp.cleanup)

    def _render(self) -> str:
        return state_mod.render(self.root, None, self.claims_path, self.order)

    def test_ready_when_every_condition_holds(self):
        self.assertIn("READY — every claim CONFIRMED", self._render())

    def test_an_unconfirmed_claim_blocks_the_freeze(self):
        ledger = claims_mod.load(self.claims_path)
        del ledger[0]["reviews"]
        claims_mod.save(self.claims_path, ledger)
        text = self._render()
        self.assertIn("NOT READY", text)
        self.assertIn("0 of 1 claims are CONFIRMED", text)

    def test_an_empty_ledger_blocks_the_freeze(self):
        claims_mod.save(self.claims_path, [])
        text = self._render()
        self.assertIn("NOT READY", text)
        self.assertIn("no claim has been raised", text)

    def test_a_step_blocked_on_the_owner_blocks_the_freeze(self):
        self.order.write_text(json.dumps(
            [{"step": 0, "name": "kill criterion", "status": "BLOCKED_OWNER",
              "requires": [], "why": "needs a design session"},
             {"step": 1, "name": "first", "status": "OPEN", "requires": [],
              "why": "the objective"}]), encoding="utf-8")
        text = self._render()
        self.assertIn("NOT READY", text)
        self.assertIn("blocked on the owner: step 0", text)

    def test_an_open_scott_ruling_blocks_the_freeze(self):
        (self.root / state_mod.SPEC).write_text(
            "# SPEC\n\n1. **[SCOTT]** the assay name collision.\n",
            encoding="utf-8")
        text = self._render()
        self.assertIn("NOT READY", text)
        self.assertIn("1 [SCOTT] ruling(s) still open", text)

    def test_a_contested_claim_blocks_the_freeze(self):
        ledger = claims_mod.load(self.claims_path)
        ledger[0]["reviews"].append({
            "at": "now", "vendor": "chatgpt", "role": "checker",
            "transport": "browser", "verdict": "DOES_NOT_PROVE",
            "files_digest": ledger[0]["reviews"][0]["files_digest"],
            "bundle_digest": "b"})
        claims_mod.save(self.claims_path, ledger)
        text = self._render()
        self.assertIn("NOT READY", text)
        self.assertIn("contested and unresolved", text)


class CanaryTests(unittest.TestCase):
    def test_selection_is_deterministic_for_a_seed(self):
        self.assertEqual(canary.select("abc")["filename"],
                         canary.select("abc")["filename"])

    def test_selection_varies_across_seeds(self):
        names = {canary.select(str(i))["kind"] for i in range(40)}
        self.assertGreater(len(names), 1)

    def test_every_defect_marker_resolves_to_a_real_line(self):
        for i in range(len(canary.DEFECTS) * 4):
            plant = canary.select(f"seed-{i}")
            self.assertGreater(plant["line"], 0, plant["filename"])
            line = plant["body"].splitlines()[plant["line"] - 1]
            self.assertIn(line.strip()[:20], plant["body"])


class ExtractionTests(unittest.TestCase):
    def test_fenced_json_is_extracted(self):
        parsed = check_mod.extract_json(
            'here you go\n```json\n{"a": 1}\n```\nhope that helps')
        self.assertEqual(parsed, {"a": 1})

    def test_bare_json_is_extracted(self):
        self.assertEqual(check_mod.extract_json('{"a": 1}'), {"a": 1})

    def test_two_blocks_is_refused_rather_than_guessed(self):
        with self.assertRaisesRegex(check_mod.CheckError, "more than one"):
            check_mod.extract_json('```json\n{"a": 1}\n```\n```json\n{"b": 2}\n```')

    def test_no_json_is_refused(self):
        with self.assertRaisesRegex(check_mod.CheckError, "no JSON object"):
            check_mod.extract_json("I could not complete this review.")


class BundleTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / ".git").mkdir()
        (self.root / "src").mkdir()
        (self.root / "src" / "guard.py").write_text(
            "def check(value):\n"
            "    if value is None:\n"
            "        raise ValueError('value must not be None')\n"
            "    return value\n", encoding="utf-8")
        self.claims_path = self.root / "claims.json"
        claims_mod.save(self.claims_path, [{
            "id": "C-0001", "text": "rejects None",
            "subject_files": ["src/guard.py"], "raised_cycle": 1}])
        self.addCleanup(self._tmp.cleanup)

    def test_the_answer_key_never_appears_in_the_pasted_parts(self):
        """Answers are source lines, so they are in the bundle by necessity.

        What must not leak is the mapping — which line answers which question —
        and the canary's hint.
        """
        meta = bundle_mod.build(self.claims_path, 1, self.root / "c",
                                "auditor", [], root=self.root)
        pasted = "\n".join(Path(p).read_text(encoding="utf-8")
                           for p in meta["parts"])
        for question in meta["grounding"]:
            self.assertIn(question["question"], pasted)
        self.assertNotIn('"expected":', pasted)
        self.assertNotIn(meta["canary"]["hint"], pasted)
        self.assertNotIn("bundle.meta.json", pasted)

    def test_grounding_never_asks_about_the_canary(self):
        """A question about the plant proves nothing about the real code."""
        meta = bundle_mod.build(self.claims_path, 1, self.root / "c",
                                "auditor", [], root=self.root)
        for question in meta["grounding"]:
            self.assertNotIn(meta["canary"]["filename"], question["question"])

    def test_grounding_spreads_across_files_when_there_are_several(self):
        (self.root / "src" / "other.py").write_text(
            "def helper(argument_name):\n"
            "    return argument_name.strip().lower()\n", encoding="utf-8")
        claims_mod.save(self.claims_path, [{
            "id": "C-0001", "text": "rejects None",
            "subject_files": ["src/guard.py", "src/other.py"],
            "raised_cycle": 1}])
        meta = bundle_mod.build(self.claims_path, 1, self.root / "c",
                                "auditor", [], root=self.root)
        asked = {q["question"].split(" of ")[1].rstrip(" verbatim.")
                 for q in meta["grounding"]}
        self.assertEqual(len(asked), 2)

    def test_grounding_answers_match_the_real_lines(self):
        meta = bundle_mod.build(self.claims_path, 1, self.root / "c",
                                "auditor", [], root=self.root)
        source = (self.root / "src" / "guard.py").read_text(encoding="utf-8")
        for question in meta["grounding"]:
            if "src/guard.py" in question["question"]:
                self.assertIn(question["expected"], source)

    def test_canary_appears_in_the_bundle_text(self):
        meta = bundle_mod.build(self.claims_path, 1, self.root / "c",
                                "auditor", [], root=self.root)
        pasted = "\n".join(Path(p).read_text(encoding="utf-8")
                           for p in meta["parts"])
        self.assertIn(meta["canary"]["filename"], pasted)

    def test_canary_is_camouflaged_among_its_neighbours(self):
        """A bare filename among repo-relative paths identifies the plant."""
        meta = bundle_mod.build(self.claims_path, 1, self.root / "c",
                                "auditor", [], root=self.root)
        self.assertTrue(meta["canary"]["filename"].startswith("src/"),
                        meta["canary"]["filename"])

    def test_canary_takes_no_directory_when_neighbours_have_none(self):
        self.assertEqual(canary._camouflage([]), "")
        self.assertEqual(canary._camouflage(["a.py", "b.py"]), "")

    def test_canary_can_be_omitted(self):
        meta = bundle_mod.build(self.claims_path, 1, self.root / "c",
                                "auditor", [], root=self.root, with_canary=False)
        self.assertIsNone(meta["canary"])


if __name__ == "__main__":
    unittest.main()
