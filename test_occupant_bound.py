"""Coverage for occupant_bound.py.

`run()`'s network path is not exercised here — a unit test that depends on a
live Ollama server is not a unit test, it is a flaky integration test wearing
one's clothes. Only the checks that do not require the network are covered:
input validation, and the output-staging bridge against a real ObjectStore.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

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
