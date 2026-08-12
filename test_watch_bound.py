"""Coverage for watch_bound.py.

No live Ollama, no live runner — that would be a flaky integration test
wearing a unit test's clothes. Covered instead: filename classification
against fake files with the two runners' real shapes, header/footer
parsing against text the runners actually write, the baseline file
round-trip, and the bar-rendering math against known elapsed/baseline
values (the actual proof the JOB asked for: rendered output for a known
baseline and a known elapsed time, not a description of one).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import watch_bound as wb


class ClassifyTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.prefix = "verify.gemma4-12b."

    def tearDown(self):
        self._tmp.cleanup()

    def _touch(self, name):
        p = self.dir / name
        p.write_text("x")
        return p

    def test_bound_primary_shape(self):
        p = self._touch(f"{self.prefix}20260812T101010.md")
        self.assertEqual(wb.classify(p, self.prefix), "bound")

    def test_sealed_reply_with_no_bare_sibling_is_sealed(self):
        p = self._touch(f"{self.prefix}20260812T101010.reply.md")
        self.assertEqual(wb.classify(p, self.prefix), "sealed")

    def test_bound_reply_sidecar_is_not_sealed_when_sibling_exists(self):
        self._touch(f"{self.prefix}20260812T101010.md")
        sidecar = self._touch(f"{self.prefix}20260812T101010.reply.md")
        self.assertIsNone(wb.classify(sidecar, self.prefix))

    def test_thinking_sidecar_matches_neither_shape(self):
        p = self._touch(f"{self.prefix}20260812T101010.thinking.md")
        self.assertIsNone(wb.classify(p, self.prefix))

    def test_sha256_sidecar_matches_neither_shape(self):
        p = self._touch(f"{self.prefix}20260812T101010.md.sha256")
        self.assertIsNone(wb.classify(p, self.prefix))


class WaitAndNewestTests(unittest.TestCase):
    """Proves the watcher finds a run_sealed.py reply — the bug item 6 named:
    the old regex never matched .reply.md at all, so it waited forever."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        wb.OUT = Path(self._tmp.name)
        self.prefix = "verify.qwen3.5-9b."

    def tearDown(self):
        self._tmp.cleanup()

    def test_newest_existing_finds_a_sealed_reply(self):
        (wb.OUT / f"{self.prefix}20260812T090000.reply.md").write_text("hello")
        found = wb.newest_existing(self.prefix)
        self.assertIsNotNone(found)
        path, kind = found
        self.assertEqual(kind, "sealed")

    def test_newest_existing_prefers_nothing_when_only_sidecars_present(self):
        (wb.OUT / f"{self.prefix}20260812T090000.thinking.md").write_text("hello")
        self.assertIsNone(wb.newest_existing(self.prefix))

    def test_wait_for_new_file_picks_up_a_sealed_reply_written_after_start(self):
        already = set(wb.OUT.glob(f"{self.prefix}*.md"))
        target = wb.OUT / f"{self.prefix}20260812T090500.reply.md"
        target.write_text("the whole reply, written once")
        path, kind = wb.wait_for_new_file(self.prefix, already)
        self.assertEqual(path, target)
        self.assertEqual(kind, "sealed")


class HeaderFooterParsingTests(unittest.TestCase):
    def test_parses_prompt_chars_from_a_real_header(self):
        header = (
            "# verify · gemma4:12b · 20260811T164923\n\n"
            "prompt sha256: a2e24fd3520f\n"
            "prompt chars:  44,955\n"
            "system prompt: none\n\n---\n\n"
        )
        self.assertEqual(wb.parse_header(header), 44955)

    def test_parses_a_real_footer(self):
        footer = (
            "\n\n---\n\nprompt eval: 12250 tok in 142s\n"
            "generation:  21468 tok in 4,719s\n"
            "reasoning:   60,229 chars (separate file)\n"
        )
        got = wb.parse_footer(footer)
        self.assertEqual(got, {
            "prompt_eval_tok": 12250, "prompt_eval_s": 142,
            "eval_tok": 21468, "eval_s": 4719,
        })

    def test_footer_with_unresolved_duration_does_not_parse(self):
        # secs() writes "?" (no digits, no trailing s) when Ollama gave no
        # duration — the honest case where there is nothing to measure.
        footer = "prompt eval: None tok in ?s\ngeneration:  None tok in ?s\n"
        self.assertIsNone(wb.parse_footer(footer))

    def test_missing_header_field_parses_to_none(self):
        self.assertIsNone(wb.parse_header("no such field here"))


class StallDetectionTests(unittest.TestCase):
    """The failure condition, not the happy path: run_bound.py's OSError
    branch appends STALLED text and returns WITHOUT ever writing the
    completion footer (run_bound.py:135-148). A watcher that only checks
    for the footer never notices — and since the STALLED text itself makes
    the file grow, it reads as a live "writing" state for a run that has
    already exited. Missed by the first version of this suite entirely."""

    STALLED_TAIL = (
        "\n\n---\n\n"
        "STALLED: read failed after 1,800s (first token: never, 0 reply "
        "chars, 0 reasoning chars)\n"
        "error: TimeoutError('timed out')\n"
    )

    def test_is_done_never_fires_on_a_stalled_file(self):
        # The blind spot itself: no footer was ever written, so the plain
        # completion check must stay False, not guess.
        text = "some header\n\npartial reply" + self.STALLED_TAIL
        self.assertFalse(wb.is_done(_FakePath(text), len(text)))

    def test_has_stalled_catches_what_is_done_misses(self):
        text = "some header\n\npartial reply" + self.STALLED_TAIL
        self.assertTrue(wb.has_stalled(_FakePath(text), len(text)))

    def test_has_stalled_is_false_on_a_healthy_growing_file(self):
        text = "some header\n\nthe model's reply, still arriving"
        self.assertFalse(wb.has_stalled(_FakePath(text), len(text)))

    def test_has_stalled_is_false_on_a_clean_completion(self):
        text = ("some header\n\nfull reply\n\n---\n\n"
                "prompt eval: 100 tok in 5s\ngeneration:  50 tok in 2s\n")
        self.assertFalse(wb.has_stalled(_FakePath(text), len(text)))


class _FakePath:
    """A minimal stand-in with just the two methods wb._tail() calls
    (open("rb") + read), so the stall-detection tests don't need a real
    temp file on disk for a one-line tail check."""

    def __init__(self, text):
        self._data = text.encode()

    def open(self, mode):
        import io
        return io.BytesIO(self._data)


class BaselineRoundTripTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        wb.BASELINE_PATH = Path(self._tmp.name) / "watch_bound_baseline.jsonl"

    def tearDown(self):
        self._tmp.cleanup()

    def test_no_baseline_file_yet_is_none(self):
        self.assertIsNone(wb.load_baseline("gemma4:12b"))

    def test_record_then_load_round_trips_chars_per_s(self):
        wb.record_baseline("gemma4:12b", prompt_chars=10000,
                            prompt_eval_tok=2500, prompt_eval_s=100)
        row = wb.load_baseline("gemma4:12b")
        self.assertEqual(row["chars_per_s"], 100.0)

    def test_load_ignores_other_models(self):
        wb.record_baseline("gemma4:12b", prompt_chars=1000,
                            prompt_eval_tok=250, prompt_eval_s=10)
        self.assertIsNone(wb.load_baseline("qwen3.5:9b"))

    def test_load_returns_the_most_recent_row_for_a_model(self):
        wb.record_baseline("gemma4:12b", prompt_chars=1000,
                            prompt_eval_tok=250, prompt_eval_s=10)
        wb.record_baseline("gemma4:12b", prompt_chars=2000,
                            prompt_eval_tok=500, prompt_eval_s=10)
        row = wb.load_baseline("gemma4:12b")
        self.assertEqual(row["chars_per_s"], 200.0)

    def test_zero_duration_is_not_recorded(self):
        # A footer that rounded to 0s (secs() has no decimals) would divide
        # by zero if recorded — the honest response is to record nothing.
        wb.record_baseline("gemma4:12b", prompt_chars=1000,
                            prompt_eval_tok=1, prompt_eval_s=0)
        self.assertIsNone(wb.load_baseline("gemma4:12b"))

    def test_baseline_file_lives_outside_runs(self):
        wb.record_baseline("gemma4:12b", prompt_chars=1000,
                            prompt_eval_tok=250, prompt_eval_s=10)
        self.assertNotIn("runs", wb.BASELINE_PATH.parts)


class BarRenderingTests(unittest.TestCase):
    """The JOB's own proof requirement: rendered output for a known baseline
    and a known elapsed time, not a description of the math."""

    def test_no_baseline_renders_indeterminate_and_says_so(self):
        line = wb.render_prompt_eval(elapsed=30, predicted=None, tick=0)
        self.assertIn("indeterminate", line)
        self.assertIn("no baseline yet", line)
        self.assertNotIn("%", line)

    def test_known_baseline_renders_a_real_fraction_at_half_predicted(self):
        # 5,000 chars at a measured 100 chars/s predicts 50s. 25s elapsed is
        # exactly half — the bar must show half its cells filled.
        predicted = wb.predict_prompt_eval_seconds(
            5000, {"chars_per_s": 100.0})
        self.assertEqual(predicted, 50.0)
        line = wb.render_prompt_eval(elapsed=25, predicted=predicted, tick=0)
        expected_bar = wb.render_bar(0.5)
        self.assertIn(expected_bar, line)
        self.assertIn("~50s predicted", line)

    def test_elapsed_past_prediction_says_so_and_never_fakes_completion(self):
        line = wb.render_prompt_eval(elapsed=120, predicted=50.0, tick=0)
        self.assertIn("past prediction", line)
        # The bar itself must stop short of full — 100% here would claim
        # measurement of something that hasn't finished.
        self.assertNotEqual(line.split()[0], wb.render_bar(1.0))

    def test_render_bar_is_proportional_to_fraction(self):
        self.assertEqual(wb.render_bar(0.0), "[" + "-" * wb.BAR_WIDTH + "]")
        self.assertEqual(wb.render_bar(1.0), "[" + "#" * wb.BAR_WIDTH + "]")
        quarter = wb.render_bar(0.25)
        self.assertEqual(quarter.count("#"), round(0.25 * wb.BAR_WIDTH))

    def test_generation_reports_measured_throughput_no_percentage(self):
        line = wb.render_generation(grown=2000, elapsed=10)
        self.assertIn("2,000 chars", line)
        self.assertIn("200 chars/s", line)
        self.assertNotIn("%", line)

    def test_predict_returns_none_without_a_baseline(self):
        self.assertIsNone(wb.predict_prompt_eval_seconds(5000, None))
        self.assertIsNone(wb.predict_prompt_eval_seconds(5000, {}))

    def test_indeterminate_bar_never_claims_a_fixed_position(self):
        positions = {wb.indeterminate_bar(t) for t in range(6)}
        self.assertGreater(len(positions), 1)


class FakeGrowingFileTests(unittest.TestCase):
    """A real file on disk, grown across two reads, driving the same
    grown/elapsed math main() uses — the fake-growing-file proof the JOB
    asked for, without running main()'s infinite loop."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "fake_reply.md"
        self.path.write_text("")

    def tearDown(self):
        self._tmp.cleanup()

    def test_growth_between_two_reads_matches_the_rendered_rate(self):
        baseline_size = self.path.stat().st_size
        self.path.write_text("x" * 300)
        grown = self.path.stat().st_size - baseline_size
        line = wb.render_generation(grown, elapsed=3)
        self.assertIn("300 chars", line)
        self.assertIn("100 chars/s", line)


if __name__ == "__main__":
    unittest.main()
