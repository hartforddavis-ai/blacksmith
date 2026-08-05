"""SPEC §9 step 1 — the sterile-launch proof, end to end.

Written this cycle, by the generator, in the same session as the `cell` and
`attest` changes it exercises. That is a conflict of interest and it is not
cured by the tests being thorough: these are evidence that the lifecycle
behaves as its author expected, not that the expectation is right.

What separates this file from `test_cell_sterility.py`, `test_attest_delta.py`
and `test_launch_sterile_env.py` is that those exercise one module against
inputs the test wrote, and this one runs SPEC §5 steps 2, 3, 4 and 6 in
sequence — build the cell, freeze the pre-attest, spawn a real child process
into it, freeze the post-attest, adjudicate the delta. The seam is the subject.
A defect found here is one every green unit test was structurally unable to
reach, because each module was correct about a base the other did not share.

What this file still does not establish:

  Isolation. Every child here runs at `same_uid_policy_grade`, the labelled
  fallback SPEC §8 names as the one that kills the design's central claim. The
  UID boundary is step 0 and step 0 is UNKNOWN. `test_the_cell_does_not_confine
  _reads_at_same_uid_grade` measures the fallback's actual reach rather than
  leaving it implied.

  The real runner. No test here runs `claude`. The stub consumes SPEC §5 step
  4's flags and ignores them, so nothing here shows that `--safe-mode` or
  `--tools` binds; ASSUMPTIONS 19 stands untouched.

Two tests assert behaviour that is wrong. They are written as characterisation,
named for the gap, and cited in ASSUMPTIONS — a blind spot with a passing test
over it is at least measured, and deleting the test would not close the gap.
"""

from __future__ import annotations

import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

import attest
import cell as cell_mod
import launch

# Consumes SPEC §5 step 4's flags the way the real runner would, then execs the
# payload. It honours none of them; see the module docstring.
STUB_RUNNER = """#!/bin/sh
while [ $# -gt 0 ]; do
  case "$1" in
    --safe-mode) shift ;;
    --tools|--output-format|--append-system-prompt-file) shift 2 ;;
    *) break ;;
  esac
done
exec {python} "$@"
"""


class LifecycleTestCase(unittest.TestCase):
    """Runs SPEC §5 steps 2-3-4-6 against a payload the test supplies."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.cells = self.tmp / "cells"
        self.cells.mkdir()
        self.runner = self.tmp / "stub_runner.sh"
        self.runner.write_text(
            STUB_RUNNER.format(python=sys.executable), encoding="utf-8")
        self.runner.chmod(self.runner.stat().st_mode | stat.S_IXUSR)

    def tearDown(self):
        self._tmp.cleanup()

    def build(self, **kwargs):
        kwargs.setdefault("evidence_mode", "copy")
        return cell_mod.build(cell_mod.CellSpec(root=self.cells / "c", **kwargs))

    def cycle(self, built, payload: str, timeout: float = 60):
        """Steps 3, 4, 6. Returns (launch record, integrity report)."""
        script = self.tmp / "payload.py"
        script.write_text(payload, encoding="utf-8")
        args = cell_mod.attest_args(built)
        pre = attest.freeze("pre", **args)
        plan = launch.plan(built, self.runner, launch.SAME_UID,
                           prompt_args=[str(script)])
        record = launch.run(plan, timeout=timeout)
        post = attest.freeze("post", **args)
        return record, attest.compare(pre, post)


class ScratchDeclarationTests(LifecycleTestCase):
    """The seam: `cell` counts from the home, `attest` counts from the root."""

    def test_a_declared_scratch_write_is_not_bypassed(self):
        # The regression this cycle exists for. Before `cell.attest_args`, the
        # spec's home-relative prefix was measured against root-relative
        # entries, matched nothing, and the runner writing its own session
        # state — the thing the declaration is for — reported BYPASSED.
        built = self.build(scratch_prefixes=("session",))
        record, report = self.cycle(built, """
import os
open(os.path.join(os.environ['HOME'], 'session', 'state.json'), 'w').write('{}')
""")
        self.assertEqual(record["exit_code"], 0, record["stderr"])
        self.assertEqual(report["integrity"], attest.INTACT)
        self.assertEqual(report["deltas"], [])
        self.assertEqual([d["path"] for d in report["scratch_deltas"]],
                         ["home/session/state.json"])

    def test_the_rebased_prefix_is_the_one_attest_receives(self):
        built = self.build(scratch_prefixes=("session",))
        self.assertEqual(cell_mod.attest_args(built)["scratch_prefixes"],
                         ("home/session",))

    def test_handing_attest_the_raw_home_relative_prefix_now_fails_closed(self):
        # The old silent misclassification, in the shape a caller would hit it.
        built = self.build(scratch_prefixes=("session",))
        with self.assertRaises(attest.AttestError) as caught:
            attest.freeze("pre", built.root,
                          scratch_prefixes=built.spec.scratch_prefixes)
        self.assertIn("binds to nothing", str(caught.exception))

    def test_a_scratch_prefix_naming_the_home_itself_is_refused(self):
        # Found by Temper. '.' and '' parse to zero parts, so both slipped past
        # the evidence-tree check, which asks for parts[0]. The declaration was
        # accepted, `attest_args` rebased it to 'home', and every path in the
        # cell became scratch: evidence could be rewritten and `compare` still
        # returned INTACT with outcome PASS. Refused at declaration time.
        for prefix in (".", ""):
            with self.subTest(prefix=prefix):
                with self.assertRaises(cell_mod.CellError) as caught:
                    cell_mod.CellSpec(root=self.cells / "c", evidence_mode="copy",
                                      scratch_prefixes=(prefix,))
                self.assertIn("attests nothing", str(caught.exception))

    def test_the_evidence_tree_cannot_be_declared_scratch_by_any_spelling(self):
        for prefix in ("evidence", "evidence/nested", ".", ""):
            with self.subTest(prefix=prefix):
                with self.assertRaises(cell_mod.CellError):
                    cell_mod.CellSpec(root=self.cells / "c", evidence_mode="copy",
                                      scratch_prefixes=(prefix,))

    def test_a_removed_scratch_directory_is_a_delta_at_post_not_a_crash(self):
        # The stated reason the pre-phase guard is not applied at post: a
        # scratch directory the run removed must come back as a delta, not as
        # an AttestError that loses the run. Asserted directly on `attest`
        # rather than through a child, because a child would first have to
        # clear the seal on the cell home and that chmod is itself an attested
        # delta, which would mask the behaviour under test.
        built = self.build(scratch_prefixes=("session",))
        args = cell_mod.attest_args(built)
        pre = attest.freeze("pre", **args)

        sealed = attest.stat_mode(built.home)
        os.chmod(built.home, 0o755)
        (built.home / "session").rmdir()
        os.chmod(built.home, int(sealed, 8))

        post = attest.freeze("post", **args)
        report = attest.compare(pre, post)
        self.assertEqual(report["integrity"], attest.INTACT)
        self.assertEqual(report["deltas"], [])
        self.assertEqual([(d["path"], d["change"]) for d in report["scratch_deltas"]],
                         [("home/session", "removed")])

    def test_a_write_outside_the_declared_scratch_is_still_bypassed(self):
        built = self.build(scratch_prefixes=("session",))
        record, report = self.cycle(built, """
import os
home = os.environ['HOME']
os.chmod(home, 0o755)
open(os.path.join(home, 'elsewhere.txt'), 'w').write('x')
""")
        self.assertEqual(report["integrity"], attest.BYPASSED)
        self.assertIn("home/elsewhere.txt", [d["path"] for d in report["deltas"]])


class SealTests(LifecycleTestCase):
    def test_the_seal_refuses_an_undeclared_write_and_the_cell_stays_intact(self):
        built = self.build()
        record, report = self.cycle(built, """
import os, sys
try:
    open(os.path.join(os.environ['HOME'], '.claude.json'), 'w').write('{}')
    print('WROTE')
except PermissionError as exc:
    print('REFUSED', exc.errno)
""")
        self.assertIn("REFUSED", record["stdout"])
        self.assertEqual(report["integrity"], attest.INTACT)

    def test_the_seal_is_a_tamper_indicator_not_a_boundary(self):
        # ASSUMPTIONS 17, measured rather than assumed: at the same UID the
        # owner clears the mode bits it set. The value of the seal is that
        # clearing it is itself a delta.
        built = self.build()
        record, report = self.cycle(built, """
import os
home = os.environ['HOME']
os.chmod(home, 0o755)
open(os.path.join(home, 'canary.txt'), 'w').write('i was here')
print('SEAL DEFEATED')
""")
        self.assertIn("SEAL DEFEATED", record["stdout"])
        self.assertEqual(report["integrity"], attest.BYPASSED)
        changes = {d["path"]: d["change"] for d in report["deltas"]}
        self.assertEqual(changes.get("home"), "mode_changed")
        self.assertEqual(changes.get("home/canary.txt"), "created")

    def test_the_cell_does_not_confine_reads_at_same_uid_grade(self):
        # SPEC §6 row "read the memory store" is UNPROVEN and gated on §8. At
        # this grade it is not merely unproven, it is false: a sterile HOME
        # relocates `~`, and an absolute path ignores that. Recorded so no
        # reading of "the cell is sterile" can be taken as confinement.
        outside = self.tmp / "host_store"
        outside.mkdir()
        (outside / "MEMORY.md").write_text("host context", encoding="utf-8")
        built = self.build()
        record, report = self.cycle(built, f"""
import os
print('HOME IS', os.path.expanduser('~'))
print('READ', open({str(outside / 'MEMORY.md')!r}).read())
""")
        self.assertIn(str(built.home), record["stdout"])
        self.assertIn("READ host context", record["stdout"])
        self.assertEqual(report["integrity"], attest.INTACT)


class MeasuredBlindSpotTests(LifecycleTestCase):
    """Two things the instrument cannot see. Asserted, not hidden."""

    def test_a_write_reverted_before_post_attest_is_invisible(self):
        # ASSUMPTIONS 18. Two moments are compared, not the interval between
        # them. Closing this needs a monitor during the run, not a better hash.
        built = self.build()
        record, report = self.cycle(built, """
import os
home = os.environ['HOME']
before = os.stat(home).st_mode & 0o7777
os.chmod(home, 0o755)
path = os.path.join(home, 'transient.txt')
open(path, 'w').write('gone before post-attest')
os.remove(path)
os.chmod(home, before)
print('WROTE AND REVERTED')
""")
        self.assertIn("WROTE AND REVERTED", record["stdout"])
        self.assertEqual(report["integrity"], attest.INTACT)
        self.assertEqual(report["deltas"], [])

    def test_a_child_that_never_ran_reports_pass(self):
        # The gap this cycle found and did not fix. `attest.compare` has no
        # notion of whether the child executed, so a cell nothing ran in is
        # trivially INTACT and `as_check` renders that as outcome PASS. On this
        # path the runner exits non-zero and writes nothing; the integrity
        # check gauge receives is indistinguishable from a clean run.
        #
        # The fix belongs to `collect` (SPEC §4, §5 step 7), which does not
        # exist and whose name is [SCOTT] ruling 1. Raised, not patched here.
        built = self.build()
        script = self.tmp / "payload.py"
        script.write_text("print('never reached')\n", encoding="utf-8")
        args = cell_mod.attest_args(built)
        pre = attest.freeze("pre", **args)
        plan = launch.plan(built, sys.executable, launch.SAME_UID,
                           prompt_args=[str(script)])
        record = launch.run(plan, timeout=30)
        post = attest.freeze("post", **args)
        report = attest.compare(pre, post)

        self.assertNotEqual(record["exit_code"], 0)
        self.assertNotIn("never reached", record["stdout"])
        self.assertEqual(report["integrity"], attest.INTACT)
        self.assertEqual(attest.as_check(report)["outcome"], "PASS")


class RecordTests(LifecycleTestCase):
    def test_the_launch_record_denies_isolation_on_every_path(self):
        built = self.build()
        record, _ = self.cycle(built, "print('ok')\n")
        self.assertFalse(record["isolation_established"])
        self.assertEqual(record["isolation_grade"], launch.SAME_UID)
        self.assertTrue(record["env_is_a_floor_not_a_ceiling"])

    def test_teardown_removes_the_sealed_tree(self):
        built = self.build()
        self.cycle(built, "print('ok')\n")
        cell_mod.teardown(built.root, self.cells)
        self.assertFalse(built.root.exists())


if __name__ == "__main__":
    unittest.main()
