"""Coverage for the OBJECT_ID regex anchor fix.

`$` matches end-of-string OR just before a trailing "\\n", not only
end-of-string -- so a 64-hex digest with a trailing newline (65 bytes)
satisfied the old `^[0-9a-f]{64}$` pattern. That string would then reach
`_path_for` and become part of an on-disk filename: the same logical id,
clean and newline-suffixed, could file under two different paths. \\Z fixes
this. No security claim is made here, consistent with the rest of this tree.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import store as store_mod


class ObjectIdTrailingNewlineTests(unittest.TestCase):
    def setUp(self):
        self.dirty_id = "a" * 64 + "\n"

    def test_valid_id_rejects_trailing_newline(self):
        with self.assertRaises(store_mod.StoreError):
            store_mod._valid_id(self.dirty_id)

    def test_has_returns_false_not_true(self):
        with tempfile.TemporaryDirectory() as tmp:
            os = store_mod.ObjectStore(tmp)
            self.assertFalse(os.has(self.dirty_id))

    def test_get_refuses_rather_than_reading_a_newline_suffixed_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            os = store_mod.ObjectStore(tmp)
            with self.assertRaises(store_mod.StoreError):
                os.get(self.dirty_id)

    def test_clean_id_unaffected(self):
        with tempfile.TemporaryDirectory() as tmp:
            os = store_mod.ObjectStore(tmp)
            object_id = os.put_bytes(b"payload")
            self.assertTrue(os.has(object_id))
            self.assertEqual(os.get(object_id), b"payload")


if __name__ == "__main__":
    unittest.main()
