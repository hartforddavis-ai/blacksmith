"""Coverage for watch_bound.py.

No live Ollama, no live runner — that would be a flaky integration test
wearing a unit test's clothes. Covered instead: filename classification
against fake files with the two runners' real shapes, header/footer
parsing against text the runners actually write, the delta-event
rendering, and an integration test driving main()'s loop against real
files on disk with time.sleep patched, proving state-change events fire
on real deltas and stay silent otherwise — the actual proof the JOB asked
for, not a description of the mechanism.

13 Aug 2026: the baseline-file and bar/rate-rendering tests that used to
live here were deleted along with the code they covered. Scott's call,
after a live run showed the rate math was wrong the first time it ran
against reality: "clock is not a solution, state change is the trigger."
"""

from __future__ import annotations

import contextlib
import io
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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


class SealFileCompletionTests(unittest.TestCase):
    """run_sealed.py's evidence_log.write() (e.g. calib_bind) never appends
    run_bound.py's footer text to its primary .md — it signals completion
    with a sibling <name>.md.sha256 instead. is_done() must recognize that
    second signal without needing the footer, and must not be fooled into
    firing early when only the primary file exists."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_is_done_true_when_sha256_seal_sibling_exists(self):
        primary = self.dir / "calib_bind.gemma4-12b-it-qat.20260812T073935.md"
        text = "# calib_bind · gemma4:12b-it-qat · 20260812T073935\n\nno footer here\n"
        primary.write_text(text)
        (self.dir / (primary.name + ".sha256")).write_text("deadbeef\n")
        self.assertTrue(wb.is_done(primary, len(text)))

    def test_is_done_false_without_seal_or_footer(self):
        primary = self.dir / "calib_bind.gemma4-12b-it-qat.20260812T073935.md"
        text = "# calib_bind · gemma4:12b-it-qat · 20260812T073935\n\nstill running\n"
        primary.write_text(text)
        self.assertFalse(wb.is_done(primary, len(text)))

    def test_is_done_still_true_on_bound_footer_with_no_seal(self):
        # The other signal must keep working unchanged for run_bound.py's
        # own files, which never get a .sha256 sibling.
        primary = self.dir / "verify.gemma4-12b.20260812T101010.md"
        text = ("some header\n\nfull reply\n\n---\n\n"
                "prompt eval: 100 tok in 5s\ngeneration:  50 tok in 2s\n")
        primary.write_text(text)
        self.assertTrue(wb.is_done(primary, len(text)))


class _NoSealPath:
    """Result of _FakePath.parent / name — a seal sibling that never exists,
    since is_done() checks that before it ever reads bytes."""

    def exists(self):
        return False


class _NoSeal:
    """A path-like stand-in for _FakePath.parent: `/` yields a path whose
    seal sibling never exists."""

    def __truediv__(self, other):
        return _NoSealPath()


class _FakePath:
    """A minimal stand-in with just what wb._tail() and wb._seal_path() call
    (open("rb") + read, parent/name), so the stall-detection tests don't
    need a real temp file on disk for a one-line tail check."""

    parent = _NoSeal()
    name = "fake.md"

    def __init__(self, text):
        self._data = text.encode()

    def open(self, mode):
        import io
        return io.BytesIO(self._data)


class DeltaRenderingTests(unittest.TestCase):
    """render_delta/render_done carry no clock: no elapsed figure, no rate,
    no percentage, no predicted anything. Just what changed and the running
    total, or (for done) the model's own reported counts."""

    def test_delta_line_carries_no_clock_derived_number(self):
        line = wb.render_delta("thinking", delta=203, total=203)
        self.assertIn("thinking", line)
        self.assertIn("+203 chars", line)
        self.assertIn("203 total", line)
        for forbidden in ("%", "chars/s", "elapsed", "predicted"):
            self.assertNotIn(forbidden, line)

    def test_delta_line_total_is_cumulative_not_the_delta(self):
        line = wb.render_delta("writing", delta=40, total=310)
        self.assertIn("+40 chars", line)
        self.assertIn("310 total", line)

    def test_done_line_with_footer_quotes_ollamas_own_numbers(self):
        footer = {"prompt_eval_tok": 100, "prompt_eval_s": 5,
                   "eval_tok": 50, "eval_s": 2}
        line = wb.render_done(grown=200, thought=1500, footer=footer)
        self.assertIn("200 reply chars", line)
        self.assertIn("1,500 reasoning chars", line)
        self.assertIn("100 tok", line)
        self.assertIn("5s", line)

    def test_done_line_without_footer_omits_ollama_numbers_not_fakes_them(self):
        line = wb.render_done(grown=50, thought=0, footer=None)
        self.assertIn("50 reply chars", line)
        self.assertNotIn("Ollama reports", line)


class EventDrivenLoopTests(unittest.TestCase):
    """Integration proof for main()'s loop: it prints a line only when a
    file it watches actually changed, carries a delta and a running total,
    and computes nothing from time.monotonic(). Reproduces the 13 Aug
    correction directly — the earlier version printed every second whether
    or not anything had changed, and computed a rate from a clock that (in
    a real run) had been running since before the phase it described even
    started."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.runs = self.root / "runs"
        self.runs.mkdir()
        self._saved_out, self._saved_bs = wb.OUT, wb.build_paste.BS
        wb.OUT = self.runs
        wb.build_paste.BS = self.root

    def tearDown(self):
        wb.OUT, wb.build_paste.BS = self._saved_out, self._saved_bs
        self._tmp.cleanup()

    def test_only_real_deltas_print_and_no_number_is_clock_derived(self):
        prefix = "verify.gemma4-12b."
        stamp = "20260813T070000"
        header = "# header\n\nprompt chars:  100\n\n---\n\n"
        primary = self.runs / f"{prefix}{stamp}.md"
        primary.write_text(header)
        think_path = self.runs / f"{prefix}{stamp}.thinking.md"

        # One step per poll. Steps 1 and 3 change nothing on disk — the
        # loop must stay silent on those polls, not redraw a stale line.
        script = [
            lambda: None,                                       # 1: prompt-eval, no change
            lambda: think_path.write_text("x" * 10),             # 2: thinking +10
            lambda: think_path.write_text("x" * 10),             # 3: unchanged, no event
            lambda: think_path.write_text("x" * 30),             # 4: thinking +20
            lambda: primary.write_text(header + "hello"),        # 5: writing +5
            lambda: primary.write_text(
                header + "hello world\n\n---\n\n"
                "prompt eval: 10 tok in 1s\ngeneration:  5 tok in 1s\n"
                "reasoning:   30 chars (separate file)\n"),      # 6: done
        ]
        steps = iter(script)

        def fake_sleep(_):
            next(steps, lambda: None)()

        buf = io.StringIO()
        with mock.patch.object(wb.time, "sleep", side_effect=fake_sleep), \
             contextlib.redirect_stdout(buf):
            wb.main("verify", "gemma4:12b", attach=True)

        out = buf.getvalue()

        self.assertIn("thinking · +10 chars · 10 total", out)
        self.assertIn("thinking · +20 chars · 30 total", out)
        self.assertIn("writing · +5 chars · 5 total", out)
        self.assertEqual(out.count("thinking ·"), 2)  # step 3's no-op must not print a third
        done_lines = [l for l in out.splitlines() if l.startswith("✓")]
        self.assertEqual(len(done_lines), 1)
        self.assertIn("Ollama reports", done_lines[0])

        for forbidden in ("s elapsed", "chars/s", "%", "predicted"):
            self.assertNotIn(forbidden, out)
        self.assertNotRegex(out, r"\[[-#?]+\]")  # no bar, no wandering marker


class SealedHonestyTests(unittest.TestCase):
    """The 12 Aug finding: for a run_sealed.py run the watcher is blind, and
    both places it spoke anyway reported something it had not observed."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.runs = self.root / "runs"
        self.runs.mkdir()
        self._saved_out, self._saved_bs = wb.OUT, wb.build_paste.BS
        wb.OUT = self.runs
        wb.build_paste.BS = self.root
        self.prefix = "calib_govern2.gemma4-12b-it-qat."

    def tearDown(self):
        wb.OUT, wb.build_paste.BS = self._saved_out, self._saved_bs
        self._tmp.cleanup()

    def _attach_output(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            wb.main("calib_govern2", "gemma4:12b-it-qat", attach=True)
        return buf.getvalue()

    def test_attaching_to_a_finished_run_does_not_claim_to_have_watched_it(self):
        reply = self.runs / f"{self.prefix}20260812T090000.reply.md"
        reply.write_text("the whole reply, written once at the end")
        out = self._attach_output()
        self.assertIn("already complete when attached", out)
        # The defect: the old path fell into the loop and printed a done line
        # two ticks later, against an elapsed measured from the attach — so a
        # run that took 17 minutes reported "2s elapsed · done". No duration
        # figure may appear at all; the word itself is fine in a disclaimer.
        self.assertIsNone(re.search(r"\d+\s*s elapsed", out))
        self.assertNotIn("✓", out)

    def test_attaching_reports_the_files_own_finish_time_not_the_attach_time(self):
        reply = self.runs / f"{self.prefix}20260812T090000.reply.md"
        reply.write_text("x" * 42)
        out = self._attach_output()
        self.assertIn("42 chars", out)
        self.assertIn("finished", out)

    def test_sealed_completion_line_quotes_no_duration(self):
        line = wb.render_sealed_done(1234)
        self.assertIn("1,234 chars", line)
        self.assertNotIn("elapsed", line)
        self.assertIn("not", line)

    def test_thinking_sidecar_is_found_under_both_runners_naming(self):
        """The sealed shape was never matched: path.stem keeps `.reply`, so
        the watcher looked for `<stamp>.reply.thinking.md` and nothing writes
        that. Both runners write `<stamp>.thinking.md`."""
        bound = self.runs / f"{self.prefix}20260812T101010.md"
        sealed = self.runs / f"{self.prefix}20260812T101010.reply.md"
        want = self.runs / f"{self.prefix}20260812T101010.thinking.md"
        self.assertEqual(wb.think_path_for(bound), want)
        self.assertEqual(wb.think_path_for(sealed), want)

    def test_thinking_sidecar_resolves_against_a_real_run_on_disk(self):
        real = Path.home() / (
            "Documents/_PROJECTS/SOFTWARE/blacksmith/runs/"
            "calib_govern2.gemma4-12b-it-qat.20260812T232241.reply.md")
        if not real.is_file():
            self.skipTest("phase 2 run not on this machine")
        self.assertTrue(wb.think_path_for(real).is_file())

    def test_is_stable_is_true_for_a_file_that_is_not_growing(self):
        p = self.runs / "static.md"
        p.write_text("finished")
        self.assertTrue(wb.is_stable(p, interval=0))

    def test_is_stable_is_false_for_a_file_still_being_written(self):
        sizes = iter([10, 40])

        class _Growing:
            def stat(self):
                return type("st", (), {"st_size": next(sizes)})()

        self.assertFalse(wb.is_stable(_Growing(), interval=0))

    def test_attaching_to_a_still_growing_sealed_file_does_not_call_it_complete(self):
        """Guards the trap: today the runner writes once at the end, so
        "exists" happens to mean "finished". If it is ever changed to stream,
        an existence check alone would report a live run as already done."""
        reply = self.runs / f"{self.prefix}20260812T090000.reply.md"
        reply.write_text("partial reply, still arriving")
        saved = wb.is_stable
        wb.is_stable = lambda path, interval=1.0: False
        try:
            out = self._attach_output()
        finally:
            wb.is_stable = saved
        self.assertNotIn("already complete", out)
        self.assertIn("sealed reply landed", out)

    def test_the_blind_window_is_announced_not_left_in_the_docstring(self):
        note = wb.SEALED_BLIND_NOTE
        self.assertIn("run_sealed.py", note)
        self.assertIn("not a stall", note)


if __name__ == "__main__":
    unittest.main()
