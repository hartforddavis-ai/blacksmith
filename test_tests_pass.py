"""Coverage for tests_pass.as_check -- the `tests_pass` mechanism.

Three cases: PASS when the discovered suite is green; FAIL when a
discovered test fails; and FAIL, not PASS, when discovery finds nothing to
run at all -- per G5 in KERNEL_WIRE_TESTS_PASS_CHECK.md, a check that
reports PASS because nothing was compared is not a check, and unittest's
own exit code (5, on an empty run) already refuses to call that a success.
Each case runs against a disposable temp directory, never against this
tree's own test_*.py files, so the check under test never re-invokes the
suite it is itself a member of.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import tests_pass


class AsCheckTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def _write(self, name: str, body: str) -> None:
        (self.root / name).write_text(body, encoding="utf-8")

    def test_pass_when_the_discovered_suite_is_green(self):
        self._write("test_ok.py", (
            "import unittest\n"
            "class T(unittest.TestCase):\n"
            "    def test_it(self):\n"
            "        self.assertEqual(1, 1)\n"
        ))
        self.assertEqual(tests_pass.as_check(self.root)["outcome"], "PASS")

    def test_fail_when_a_discovered_test_fails(self):
        self._write("test_bad.py", (
            "import unittest\n"
            "class T(unittest.TestCase):\n"
            "    def test_it(self):\n"
            "        self.assertEqual(1, 2)\n"
        ))
        self.assertEqual(tests_pass.as_check(self.root)["outcome"], "FAIL")

    def test_fail_not_pass_when_nothing_is_discovered(self):
        # Empty directory: no test_*.py files at all.
        self.assertEqual(tests_pass.as_check(self.root)["outcome"], "FAIL")


if __name__ == "__main__":
    unittest.main()
