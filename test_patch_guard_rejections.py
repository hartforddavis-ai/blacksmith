"""Coverage for patch_guard.py rejection codes not exercised by test_patch_guard.py.

That file covers only the diff-header space-ambiguity fix (unparsable, traversal).
The module docstring names ten rejection codes; eight had zero regression coverage
before this file -- a fail-closed boundary with untested rejection paths is not
proven fail-closed, it's asserted. No security claim is made here, consistent
with the rest of this tree.
"""

from __future__ import annotations

import unittest

import patch_guard


class SymlinkModeTests(unittest.TestCase):
    def test_new_file_symlink_mode_rejected(self):
        patch = (
            "diff --git a/link b/link\n"
            "new file mode 120000\n"
        )
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "symlink_mode" for f in result["findings"]))


class DisallowedModeTests(unittest.TestCase):
    def test_gitlink_mode_rejected(self):
        patch = (
            "diff --git a/sub b/sub\n"
            "new file mode 160000\n"
        )
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "disallowed_mode" for f in result["findings"]))

    def test_tree_mode_in_index_line_rejected(self):
        patch = (
            "diff --git a/x b/x\n"
            "index 111..222 040000\n"
        )
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "disallowed_mode" for f in result["findings"]))

    def test_setuid_bit_mode_rejected(self):
        patch = (
            "diff --git a/x b/x\n"
            "old mode 100644\n"
            "new mode 104755\n"
        )
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "disallowed_mode" for f in result["findings"]))


class AbsolutePathTests(unittest.TestCase):
    def test_absolute_path_in_diff_header_rejected(self):
        patch = "diff --git /etc/passwd /etc/passwd\n"
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "absolute_path" for f in result["findings"]))


class GitMetadataPathTests(unittest.TestCase):
    def test_dotgit_component_in_diff_header_rejected(self):
        patch = "diff --git a/.git/config b/.git/config\n"
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "git_metadata_path" for f in result["findings"]))

    def test_dotgit_component_in_rename_line_rejected(self):
        patch = (
            "diff --git a/x b/y\n"
            "rename from x\n"
            "rename to .git/hooks/pre-commit\n"
        )
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "git_metadata_path" for f in result["findings"]))


class QuotedPathTests(unittest.TestCase):
    def test_quoted_path_in_diff_header_rejected(self):
        patch = 'diff --git "a/has space" "b/has space"\n'
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "quoted_path" for f in result["findings"]))

    def test_quoted_path_in_minus_plus_line_rejected(self):
        patch = (
            "diff --git a/x b/x\n"
            '--- "a/x"\n'
            "+++ b/x\n"
        )
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "quoted_path" for f in result["findings"]))


class BackslashPathTests(unittest.TestCase):
    def test_backslash_in_rename_path_rejected(self):
        patch = (
            "diff --git a/x b/x\n"
            "rename from x\n"
            "rename to a\\b\n"
        )
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "backslash_path" for f in result["findings"]))


class DrivePathTests(unittest.TestCase):
    def test_drive_prefix_in_rename_path_rejected(self):
        patch = (
            "diff --git a/x b/x\n"
            "rename from x\n"
            "rename to C:/Windows/System32\n"
        )
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "drive_path" for f in result["findings"]))


class BinaryPatchTests(unittest.TestCase):
    def test_binary_patch_flagged(self):
        patch = (
            "diff --git a/x.bin b/x.bin\n"
            "index 111..222 100644\n"
            "GIT binary patch\n"
        )
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "binary_patch" for f in result["findings"]))


class UnparsableTests(unittest.TestCase):
    def test_non_string_input_rejected(self):
        result = patch_guard.inspect(123)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "unparsable" for f in result["findings"]))

    def test_empty_input_no_header_rejected(self):
        result = patch_guard.inspect("")
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "unparsable" for f in result["findings"]))

    def test_control_character_in_path_rejected(self):
        patch = (
            "diff --git a/x b/x\n"
            "rename from x\n"
            "rename to a\x00b\n"
        )
        result = patch_guard.inspect(patch)
        self.assertFalse(result["accepted"])
        self.assertTrue(any(f["code"] == "unparsable" for f in result["findings"]))


class DevNullPassthroughTests(unittest.TestCase):
    def test_new_file_against_dev_null_accepted(self):
        patch = (
            "diff --git a/new.py b/new.py\n"
            "new file mode 100644\n"
            "index 000..111 100644\n"
            "--- /dev/null\n"
            "+++ b/new.py\n"
            "@@ -0,0 +1 @@\n"
            "+content\n"
        )
        result = patch_guard.inspect(patch)
        self.assertTrue(result["accepted"])


if __name__ == "__main__":
    unittest.main()
