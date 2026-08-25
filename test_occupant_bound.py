"""Coverage for occupant_bound.py.

`run()`'s network path is not exercised here — a unit test that depends on a
live Ollama server is not a unit test, it is a flaky integration test wearing
one's clothes. Only the checks that do not require the network are covered:
input validation, and the output-staging bridge against a real ObjectStore.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

import occupant_bound as occ
import store as store_mod


class RunValidationTests(unittest.TestCase):
    def test_refuses_a_non_clean_model(self):
        with self.assertRaises(occ.OccupantError):
            occ.run("skadi:latest", "hello")

    def test_refuses_empty_prompt(self):
        with self.assertRaises(occ.OccupantError):
            occ.run("qwen3.5:9b", "   ")

    def test_accepts_every_clean_model_name_before_the_network_call(self):
        # Bogus port so the call fails fast on connection, not on validation —
        # proves the CLEAN_MODELS check passes before urlopen is ever reached.
        for model in occ.CLEAN_MODELS:
            with self.subTest(model=model):
                with self.assertRaises(occ.OccupantError) as caught:
                    occ.run(model, "hello", timeout=0.01)
                self.assertNotIn("refusing", str(caught.exception))


class FakeStreamResponse:
    """Stands in for `urllib.request.urlopen`'s context-managed response.

    Yields the given chunks as the newline-delimited JSON lines Ollama's
    stream actually sends. `on_yield`, when given, runs after each chunk is
    handed to the caller's `for line in r` loop but before the next one is
    produced — the hook this file uses to assert a prior chunk already
    reached disk, proving the write happened chunk-by-chunk and not once at
    the end.
    """

    def __init__(self, chunks, on_yield=None):
        self._chunks = chunks
        self._on_yield = on_yield

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def __iter__(self):
        for i, chunk in enumerate(self._chunks):
            yield json.dumps(chunk).encode()
            if self._on_yield is not None:
                self._on_yield(i)


class StreamingTests(unittest.TestCase):
    """occupant_bound.run() writing tokens to disk as they arrive (TODO !92).

    No live Ollama call in any of these — `urlopen` is replaced with
    FakeStreamResponse, same no-network contract this file states at the top.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_reply_reaches_disk_before_the_stream_finishes(self):
        reply_path = self.tmp / "reply.md"
        chunks = [
            {"response": "hello "}, {"response": "world"},
            {"done": True, "done_reason": "stop"},
        ]
        seen_after_first = {}

        def on_yield(i):
            if i == 0:
                # The loop has processed chunk 0 (yielded control back here)
                # but not yet chunk 1 — if this already reads "hello ", the
                # write happened per-chunk, not after the whole run.
                seen_after_first["text"] = reply_path.read_text()

        fake = FakeStreamResponse(chunks, on_yield=on_yield)
        with mock.patch.object(occ.urllib.request, "urlopen", return_value=fake):
            run = occ.run("qwen3.5:9b", "hi", reply_path=reply_path)

        self.assertEqual(seen_after_first["text"], "hello ")
        self.assertEqual(reply_path.read_text(), "hello world")
        self.assertEqual(run.response, "hello world")

    def test_thinking_only_opens_think_path_when_there_is_a_thought(self):
        reply_path = self.tmp / "reply.md"
        think_path = self.tmp / "think.md"
        chunks = [
            {"response": "", "thinking": "pondering"},
            {"response": "ok", "done": True, "done_reason": "stop"},
        ]
        fake = FakeStreamResponse(chunks)
        with mock.patch.object(occ.urllib.request, "urlopen", return_value=fake):
            run = occ.run(
                "qwen3.5:9b", "hi", reply_path=reply_path, think_path=think_path)

        self.assertEqual(think_path.read_text(), "pondering")
        self.assertEqual(run.thinking, "pondering")
        self.assertEqual(reply_path.read_text(), "ok")

    def test_no_think_path_file_when_the_model_never_thinks(self):
        reply_path = self.tmp / "reply.md"
        think_path = self.tmp / "think.md"
        chunks = [{"response": "ok", "done": True, "done_reason": "stop"}]
        fake = FakeStreamResponse(chunks)
        with mock.patch.object(occ.urllib.request, "urlopen", return_value=fake):
            occ.run("qwen3.5:9b", "hi", reply_path=reply_path, think_path=think_path)

        self.assertFalse(think_path.exists())

    def test_no_paths_given_writes_nothing_to_disk(self):
        chunks = [{"response": "ok", "done": True, "done_reason": "stop"}]
        fake = FakeStreamResponse(chunks)
        with mock.patch.object(occ.urllib.request, "urlopen", return_value=fake):
            run = occ.run("qwen3.5:9b", "hi")

        self.assertEqual(list(self.tmp.iterdir()), [])
        self.assertEqual(run.response, "ok")

    def test_reply_file_still_closed_on_a_mid_stream_failure(self):
        reply_path = self.tmp / "reply.md"

        def blow_up(_i):
            raise ConnectionResetError("stream dropped")

        chunks = [{"response": "partial"}]
        fake = FakeStreamResponse(chunks, on_yield=blow_up)
        with mock.patch.object(occ.urllib.request, "urlopen", return_value=fake):
            with self.assertRaises(occ.OccupantError):
                occ.run("qwen3.5:9b", "hi", reply_path=reply_path)

        # The file was opened and written before the failure — the handle
        # must not leak, and what arrived must still be readable afterward.
        self.assertEqual(reply_path.read_text(), "partial")


class StageArtifactTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.store = store_mod.ObjectStore(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def test_stages_text_and_returns_its_store_id(self):
        object_id = occ.stage_artifact(self.store, "hello world")
        self.assertEqual(object_id, store_mod.sha256_bytes(b"hello world"))
        self.assertEqual(self.store.get(object_id), b"hello world")

    def test_rejects_non_string_response(self):
        with self.assertRaises(occ.OccupantError):
            occ.stage_artifact(self.store, b"already bytes")

    def test_same_text_stages_to_the_same_id(self):
        first = occ.stage_artifact(self.store, "repeat me")
        second = occ.stage_artifact(self.store, "repeat me")
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
