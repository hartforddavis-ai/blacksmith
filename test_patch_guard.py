"""Verification coverage for the diff-header space-ambiguity fix.

No security claim is made here, consistent with the rest of this tree.
"""

from __future__ import annotations

import unittest

import patch_guard


class PatchGuardTests(unittest.TestCase):
    def test_embedded_space_traversal_now_rejected(self):
        patch = (
            "diff --git a/x ../y z b/x ../y z\n"
            "old mode 100644\n"
            "new mode 100755\n"
        )
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "unparsable" for f in result["findings"]))

    def test_ordinary_mode_change_still_accepted(self):
        patch = (
            "diff --git a/x.py b/x.py\n"
            "old mode 100644\n"
            "new mode 100755\n"
        )
        result = patch_guard.inspect(patch)
        self.assertTrue(result["accepted"])

    def test_ordinary_content_diff_still_accepted(self):
        patch = (
            "diff --git a/x.py b/x.py\n"
            "index 111..222 100644\n"
            "--- a/x.py\n"
            "+++ b/x.py\n"
            "@@ -1 +1 @@\n"
            "-old\n"
            "+new\n"
        )
        result = patch_guard.inspect(patch)
        self.assertTrue(result["accepted"])

    def test_traversal_in_header_without_spaces_still_rejected(self):
        patch = (
            "diff --git a/../etc/passwd b/../etc/passwd\n"
            "old mode 100644\n"
            "new mode 100755\n"
        )
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "traversal" for f in result["findings"]))


if __name__ == "__main__":
    unittest.main()
