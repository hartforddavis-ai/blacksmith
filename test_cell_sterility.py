"""Coverage for cell.py.

Written this cycle, by the generator, in the same session as cell.py. These
tests are evidence that the module behaves as its author expected it to. They
are not independent evidence that the cell is sterile in any sense that matters
to SPEC §8, and no test here touches the UID boundary, because nothing in this
tree does.

The tests worth reading are the refusals. A build that succeeds proves the
happy path; a build that refuses to start proves the fail-closed rule, which is
the one SPEC §2 rule 6 rests on.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

import cell as cell_mod


def spec_at(root, **kwargs):
    kwargs.setdefault("evidence_mode", "copy")
    return cell_mod.CellSpec(root=Path(root), **kwargs)


class SpecValidationTests(unittest.TestCase):
    def test_evidence_mode_has_no_default(self):
        with self.assertRaises(TypeError):
            cell_mod.CellSpec(root=Path("/tmp/x"))

    def test_mount_mode_refuses_rather_than_falling_back_to_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = cell_mod.CellSpec(root=Path(tmp) / "cell", evidence_mode="mount")
            with self.assertRaises(cell_mod.RulingRequired):
                cell_mod.build(spec)

    def test_unknown_evidence_mode_rejected(self):
        with self.assertRaises(cell_mod.CellError):
            cell_mod.CellSpec(root=Path("/tmp/x"), evidence_mode="bind")

    def test_scratch_prefix_may_not_cover_evidence(self):
        with self.assertRaises(cell_mod.CellError):
            spec_at("/tmp/x", scratch_prefixes=("evidence",))

    def test_scratch_prefix_may_not_cover_a_path_under_evidence(self):
        with self.assertRaises(cell_mod.CellError):
            spec_at("/tmp/x", scratch_prefixes=("evidence/sub",))

    def test_scratch_prefix_rejects_absolute_and_dotdot(self):
        for bad in ("/etc", "../outside", "a/../../b"):
            with self.subTest(bad=bad):
                with self.assertRaises(cell_mod.CellError):
                    spec_at("/tmp/x", scratch_prefixes=(bad,))


class BuildRefusalTests(unittest.TestCase):
    def test_existing_root_is_refused_not_reused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "cell"
            root.mkdir()
            with self.assertRaises(cell_mod.CellError):
                cell_mod.build(spec_at(root))

    def test_symlinked_root_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            elsewhere = Path(tmp) / "elsewhere"
            elsewhere.mkdir()
            root = Path(tmp) / "cell"
            root.symlink_to(elsewhere)
            with self.assertRaises(cell_mod.CellError):
                cell_mod.build(spec_at(root))

    def test_contaminated_ancestor_blocks_the_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "CLAUDE.md").write_text("host context", encoding="utf-8")
            nested = Path(tmp) / "cells"
            nested.mkdir()
            with self.assertRaises(cell_mod.CellError) as caught:
                cell_mod.build(spec_at(nested / "cell"))
            self.assertIn("contaminated", str(caught.exception))

    def test_ancestor_check_names_the_offending_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".mcp.json").write_text("{}", encoding="utf-8")
            found = cell_mod.ancestor_contamination(Path(tmp) / "cells" / "cell")
            self.assertTrue(any(f.endswith(".mcp.json") for f in found), found)

    def test_symlinked_evidence_source_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            real = Path(tmp) / "real.txt"
            real.write_text("payload", encoding="utf-8")
            link = Path(tmp) / "link.txt"
            link.symlink_to(real)
            with self.assertRaises(cell_mod.CellError):
                cell_mod.build(spec_at(Path(tmp) / "cell", evidence_sources=(link,)))

    def test_directory_evidence_source_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "adir"
            src.mkdir()
            with self.assertRaises(cell_mod.CellError):
                cell_mod.build(spec_at(Path(tmp) / "cell", evidence_sources=(src,)))

    def test_colliding_evidence_basenames_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "a"
            b = Path(tmp) / "b"
            a.mkdir()
            b.mkdir()
            (a / "same.txt").write_text("one", encoding="utf-8")
            (b / "same.txt").write_text("two", encoding="utf-8")
            with self.assertRaises(cell_mod.CellError):
                cell_mod.build(spec_at(
                    Path(tmp) / "cell",
                    evidence_sources=(a / "same.txt", b / "same.txt")))


class BuiltCellTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.source = self.tmp / "finding.txt"
        self.source.write_text("evidence bytes", encoding="utf-8")
        self.cells_root = self.tmp / "cells"
        self.cells_root.mkdir()
        self.cell = cell_mod.build(spec_at(
            self.cells_root / "c1", evidence_sources=(self.source,)))

    def tearDown(self):
        self._tmp.cleanup()

    def test_evidence_is_a_copy_with_the_same_bytes(self):
        placed = self.cell.evidence / "finding.txt"
        self.assertFalse(placed.is_symlink())
        self.assertEqual(placed.read_bytes(), self.source.read_bytes())

    def test_evidence_is_filed_read_only(self):
        mode = (self.cell.evidence / "finding.txt").stat().st_mode & 0o777
        self.assertEqual(mode, cell_mod.FILE_MODE)

    def test_clean_cell_reports_sterile(self):
        report = cell_mod.census(self.cell)
        self.assertTrue(report["sterile"], report)
        self.assertEqual(report["undeclared"], [])
        self.assertEqual(report["missing"], [])

    def test_no_writable_output_directory_exists(self):
        # The transcript is captured by the parent from the child's stdout, so
        # the cell needs nothing writable. If that ever changes, post-attest has
        # to start excusing a directory, and this test should fail first.
        names = {Path(p).name for p in cell_mod.census(self.cell)["present"]}
        self.assertNotIn("out", names)

    def test_undeclared_file_breaks_sterility(self):
        os.chmod(self.cell.home, 0o755)
        (self.cell.home / "stowaway.txt").write_text("x", encoding="utf-8")
        report = cell_mod.census(self.cell)
        self.assertFalse(report["sterile"])
        self.assertIn("stowaway.txt", report["undeclared"])

    def test_planted_context_file_is_named_as_forbidden(self):
        os.chmod(self.cell.home, 0o755)
        (self.cell.home / "CLAUDE.md").write_text("inject", encoding="utf-8")
        report = cell_mod.census(self.cell)
        self.assertFalse(report["sterile"])
        self.assertIn("CLAUDE.md", report["forbidden_names"])

    def test_context_file_planted_at_depth_is_still_found(self):
        os.chmod(self.cell.home, 0o755)
        deep = self.cell.home / "a" / "b"
        deep.mkdir(parents=True)
        (deep / "MEMORY.md").write_text("history", encoding="utf-8")
        report = cell_mod.census(self.cell)
        self.assertIn("a/b/MEMORY.md", report["forbidden_names"])

    def test_symlink_out_of_the_cell_breaks_sterility(self):
        os.chmod(self.cell.home, 0o755)
        (self.cell.home / "escape").symlink_to(self.tmp)
        report = cell_mod.census(self.cell)
        self.assertFalse(report["sterile"])
        self.assertIn("escape", report["symlinks"])

    def test_require_sterile_raises_rather_than_reporting(self):
        os.chmod(self.cell.home, 0o755)
        (self.cell.home / "stowaway.txt").write_text("x", encoding="utf-8")
        with self.assertRaises(cell_mod.CellError):
            cell_mod.require_sterile(self.cell)

    def test_declared_scratch_directory_does_not_break_sterility(self):
        cell = cell_mod.build(spec_at(
            self.cells_root / "c2", evidence_sources=(self.source,),
            scratch_prefixes=("runner/state",)))
        report = cell_mod.census(cell)
        self.assertTrue(report["sterile"], report)
        self.assertIn("runner/state", report["present"])

    def test_scratch_directory_stays_writable_after_seal(self):
        cell = cell_mod.build(spec_at(
            self.cells_root / "c3", scratch_prefixes=("runner",)))
        (cell.home / "runner" / "session.json").write_text("{}", encoding="utf-8")
        self.assertTrue((cell.home / "runner" / "session.json").is_file())


class TeardownTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.cells_root = self.tmp / "cells"
        self.cells_root.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def test_sealed_tree_is_removed(self):
        source = self.tmp / "f.txt"
        source.write_text("bytes", encoding="utf-8")
        cell = cell_mod.build(spec_at(
            self.cells_root / "c1", evidence_sources=(source,)))
        cell_mod.teardown(cell.root, self.cells_root)
        self.assertFalse(cell.root.exists())

    def test_target_outside_the_cells_root_is_refused(self):
        outside = self.tmp / "precious"
        outside.mkdir()
        with self.assertRaises(cell_mod.CellError):
            cell_mod.teardown(outside, self.cells_root)
        self.assertTrue(outside.is_dir())

    def test_the_cells_root_itself_is_refused(self):
        with self.assertRaises(cell_mod.CellError):
            cell_mod.teardown(self.cells_root, self.cells_root)
        self.assertTrue(self.cells_root.is_dir())

    def test_symlink_pointing_inside_is_still_refused(self):
        outside = self.tmp / "precious"
        outside.mkdir()
        (outside / "keepme.txt").write_text("keep", encoding="utf-8")
        link = self.cells_root / "looks-inside"
        link.symlink_to(outside)
        with self.assertRaises(cell_mod.CellError):
            cell_mod.teardown(link, self.cells_root)
        self.assertTrue((outside / "keepme.txt").is_file())


if __name__ == "__main__":
    unittest.main()
