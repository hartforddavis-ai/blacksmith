"""Cell — builds and destroys the sterile tree. Ring 0, parent-side.

No security claim is made here. This module builds a directory tree and
enumerates what is in it. Whether the occupant is *contained* is not a question
it can answer: containment is the UID boundary, and that is SPEC §8 step 0,
which is UNKNOWN.

What it does establish: the tree contains what was declared and nothing else,
measured by walking it rather than by trusting the build steps that produced it.

Design rules taken from SPEC §2:

  Rule 3, sterility by construction. Built by `mkdir` into empty space,
  populated only from an explicit declaration. Nothing is copied in and then
  deleted, hidden, renamed or disabled, so there is no suppression step to
  fail open.

  Rule 6, fail closed. Every refusal here raises. A cell that cannot be built
  to specification is not built at a lower specification.

Two things this module deliberately refuses to decide:

  SPEC §11 ruling 3 — evidence as a copy, or as a read-only mount — is Scott's
  and is open. `evidence_mode` therefore has no default. `"copy"` is
  implemented; `"mount"` raises. Supplying a default would settle an owner
  ruling by making one option the path of least resistance.

  SPEC §8 step 0 — the UID switch — is not attempted here. Consequently the
  read-only mode bits this module sets are a *tamper indicator*, not a
  boundary: a process running as the owning UID can chmod them back. They
  become a boundary only if step 0 resolves, and not before.
"""

from __future__ import annotations

import os
import shutil
import stat
from dataclasses import dataclass, field
from pathlib import Path

import log as log_mod

# Names the harness may read as context if it finds them. Checked on the cell's
# ancestor chain, because a sterile HOME does not stop a discovery mechanism
# that walks upward from cwd. Whether the runner walks is UNKNOWN in
# ASSUMPTIONS.md; cheap check, silent failure, so it runs regardless.
HOST_CONTEXT_NAMES = frozenset({
    "CLAUDE.md", "CLAUDE.local.md", ".claude", ".claude.json", ".mcp.json",
})

# Anything from this set inside the cell is a contamination, whatever placed it.
# Wider than the ancestor list: inside a cell that holds only declared evidence,
# a `skills` directory has no innocent reading.
CELL_FORBIDDEN_NAMES = HOST_CONTEXT_NAMES | frozenset({
    "MEMORY.md", "settings.json", "settings.local.json", "skills", "hooks",
    "AGENTS.md", ".codex",
})

EVIDENCE_DIRNAME = "evidence"

FILE_MODE = 0o444
DIR_MODE = 0o555


class CellError(Exception):
    """The cell could not be built, measured, or destroyed to specification."""


class RulingRequired(CellError):
    """An owner ruling this module refuses to pre-empt has not been made."""


def confine(root: Path, candidate) -> Path:
    """Resolve `candidate` and require it to sit inside `root`.

    realpath before the prefix comparison, so a symlink cannot present an
    inside-looking path for an outside target. Same shape as store.confine and
    forensic_checker/scope.py; see ASSUMPTIONS.md on whether to consolidate.
    """
    real_root = Path(os.path.realpath(str(root)))
    real = Path(os.path.realpath(str(candidate)))
    if real != real_root and real_root not in real.parents:
        raise CellError(f"path {str(candidate)!r} resolves outside {str(real_root)!r}")
    return real


def ancestor_contamination(path) -> list[str]:
    """Context files on `path`'s ancestor chain, nearest first.

    The cell's own contents are not consulted — this is about where the cell was
    put, not what was put in it.
    """
    start = Path(os.path.realpath(str(path)))
    found = []
    for parent in start.parents:
        for name in sorted(HOST_CONTEXT_NAMES):
            if (parent / name).exists():
                found.append(str(parent / name))
    return found


@dataclass(frozen=True)
class CellSpec:
    """What the cell is to contain. Declared before it exists.

    `scratch_prefixes` names cell-relative directories whose contents the runner
    itself is expected to write — harness session state, and nothing else. They
    are declared here, before launch, precisely so they cannot be widened
    afterwards to explain away a delta that post-attest found. `attest.compare`
    binds the declaration into the manifest and refuses a comparison whose two
    sides disagree about it.

    An empty tuple is the strict case: every byte in the cell is attested, and
    any change at all is a write that happened.
    """

    root: Path
    evidence_mode: str
    evidence_sources: tuple = ()
    scratch_prefixes: tuple = ()
    extra_dirs: tuple = field(default=())

    def __post_init__(self):
        if self.evidence_mode not in ("copy", "mount"):
            raise CellError(
                f"evidence_mode must be 'copy' or 'mount', got {self.evidence_mode!r}")
        for prefix in self.scratch_prefixes:
            rel = Path(prefix)
            if rel.is_absolute() or ".." in rel.parts:
                raise CellError(
                    f"scratch prefix {prefix!r} must be cell-relative with no '..'")
            # '.' and '' both parse to zero parts, which slipped past the
            # evidence check below and declared the whole home as scratch —
            # every delta reported as expected, evidence included, and no
            # possible BYPASSED. Refused before the two checks that assume
            # there is a first component to look at.
            if not rel.parts:
                raise CellError(
                    f"scratch prefix {prefix!r} names the cell home itself; a "
                    "cell whose entire tree is scratch attests nothing and can "
                    "never report BYPASSED")
            # A scratch prefix over the evidence tree would make evidence
            # tampering unattested by declaration. Refused, not warned about.
            if rel.parts[0] == EVIDENCE_DIRNAME:
                raise CellError(
                    f"scratch prefix {prefix!r} covers the evidence tree; "
                    "evidence is attested by definition")


@dataclass(frozen=True)
class Cell:
    root: Path
    home: Path
    evidence: Path
    spec: CellSpec


def build(spec: CellSpec) -> Cell:
    """Create the sterile tree. The root must not already exist.

    Refusing an existing root is not fastidiousness. Building into a directory
    that is already there means inheriting whatever is already in it, which is
    the suppression model SPEC §2 rule 3 deletes.
    """
    root = Path(os.path.realpath(str(Path(spec.root).parent))) / Path(spec.root).name
    if root.exists() or root.is_symlink():
        raise CellError(f"cell root {str(root)!r} already exists; refusing to reuse it")
    if not root.parent.is_dir():
        raise CellError(f"cell parent {str(root.parent)!r} is not a directory")

    contaminated = ancestor_contamination(root.parent)
    if contaminated:
        raise CellError(
            "cell location is contaminated: context files exist above it — "
            + ", ".join(contaminated))

    if spec.evidence_mode == "mount":
        raise RulingRequired(
            "evidence as a read-only mount is SPEC §11 ruling 3 and is Scott's "
            "call; it is not implemented, and choosing 'copy' by default would "
            "settle the ruling by making it the only path that works")

    root.mkdir(parents=False, exist_ok=False)
    home = root / "home"
    home.mkdir()
    evidence = home / EVIDENCE_DIRNAME
    evidence.mkdir()

    for rel in spec.extra_dirs:
        target = confine(home, home / rel)
        target.mkdir(parents=True, exist_ok=True)

    for source in spec.evidence_sources:
        _place_evidence(evidence, source)

    for rel in spec.scratch_prefixes:
        (home / rel).mkdir(parents=True, exist_ok=True)

    _seal(home, spec.scratch_prefixes)
    return Cell(root=root, home=home, evidence=evidence, spec=spec)


def _place_evidence(evidence_root: Path, source) -> Path:
    """Copy one host file into the evidence tree under its own basename.

    Regular files only, and the source is not followed through a symlink: a
    symlinked source would put bytes in the cell that the manifest attributes to
    a path the host never checked.
    """
    src = Path(str(source))
    if src.is_symlink():
        raise CellError(f"evidence source {str(src)!r} is a symlink")
    if not src.is_file():
        raise CellError(f"evidence source {str(src)!r} is not a regular file")
    target = evidence_root / src.name
    if target.exists():
        raise CellError(f"two evidence sources share the basename {src.name!r}")
    shutil.copyfile(src, target, follow_symlinks=False)
    return target


def _seal(home: Path, scratch_prefixes) -> None:
    """Set read-only mode bits on everything outside the declared scratch.

    Deepest-first: a directory has to stay writable while its children are being
    walked. Mode bits are a tamper indicator here, not a boundary — see the
    module docstring.
    """
    scratch = {Path(p) for p in scratch_prefixes}

    def in_scratch(rel: Path) -> bool:
        return any(rel == s or s in rel.parents for s in scratch)

    for current, dirnames, filenames in os.walk(home, topdown=False):
        current_path = Path(current)
        rel_dir = current_path.relative_to(home)
        for name in filenames:
            target = current_path / name
            if target.is_symlink() or in_scratch(rel_dir / name):
                continue
            os.chmod(target, FILE_MODE)
        if rel_dir != Path(".") and in_scratch(rel_dir):
            continue
        os.chmod(current_path, DIR_MODE)


def census(cell: Cell) -> dict:
    """Walk the built cell and report what is actually in it.

    The distinction this draws is the point of the module: `declared` is what
    the build was asked for, `present` is what a walk of the filesystem found.
    They are compared rather than assumed equal, because a build step that
    silently did something else is exactly the failure a build log cannot show.
    """
    present, forbidden, symlinks = [], [], []
    for current, dirnames, filenames in os.walk(cell.home):
        current_path = Path(current)
        for name in sorted(dirnames) + sorted(filenames):
            target = current_path / name
            rel = str(target.relative_to(cell.home))
            present.append(rel)
            if name in CELL_FORBIDDEN_NAMES:
                forbidden.append(rel)
            if target.is_symlink():
                symlinks.append(rel)

    declared = {EVIDENCE_DIRNAME}
    for source in cell.spec.evidence_sources:
        declared.add(f"{EVIDENCE_DIRNAME}/{Path(str(source)).name}")
    for rel in tuple(cell.spec.extra_dirs) + tuple(cell.spec.scratch_prefixes):
        parts = Path(rel).parts
        for depth in range(1, len(parts) + 1):
            declared.add(str(Path(*parts[:depth])))

    present_set = set(present)
    return {
        "home": str(cell.home),
        "declared": sorted(declared),
        "present": sorted(present_set),
        "undeclared": sorted(present_set - declared),
        "missing": sorted(declared - present_set),
        "forbidden_names": sorted(forbidden),
        "symlinks": sorted(symlinks),
        "sterile": not (present_set - declared) and not forbidden and not symlinks,
    }


def attest_args(cell: Cell) -> dict:
    """The arguments `attest.freeze` must be given to measure this cell.

    The two modules count from different places. `attest` walks from the cell
    root, so its entries are keyed `home/...`; `CellSpec.scratch_prefixes` are
    home-relative, because that is the base the declaration is written in. A
    caller that passes the spec's prefixes straight through declares a region
    one segment shallower than the tree it is measuring, the declaration matches
    nothing, and every write the runner was expected to make is reported as an
    attested delta — BYPASSED, on the ordinary path, with no way to tell it from
    a real one.

    Rebasing is done here rather than at each call site because a call site that
    gets it wrong produces a plausible verdict rather than an error.
    """
    rel_home = cell.home.relative_to(cell.root)
    return {
        "cell_root": cell.root,
        "scratch_prefixes": tuple(
            str(rel_home / p) for p in cell.spec.scratch_prefixes),
    }


def require_sterile(cell: Cell, log_path: Path | None = None) -> dict:
    """`census`, but a non-sterile result raises instead of being returned.

    Callers that only report sterility give an operator something to weigh.
    SPEC §2 rule 6 says there is nothing to weigh: if the cell is not sterile
    there is no session.

    Both outcomes are recorded before either is returned or raised.
    """
    report = census(cell)
    if not report["sterile"]:
        log_mod.record("cell.sterility", "FAIL", report, log_path)
        raise CellError(
            "cell is not sterile: "
            f"undeclared={report['undeclared']} "
            f"forbidden={report['forbidden_names']} "
            f"symlinks={report['symlinks']}")
    log_mod.record("cell.sterility", "PASS", report, log_path)
    return report


def teardown(cell_root, cells_root) -> None:
    """Destroy the cell. `cells_root` is host configuration and confines it.

    The destructive verb in Ring 0 gets the narrowest signature in Ring 0: the
    caller must name the root it is permitted to delete inside, the target is
    resolved before the prefix comparison, and the target may not itself be the
    permitted root.
    """
    real_root = Path(os.path.realpath(str(cells_root)))
    target = Path(str(cell_root))
    if target.is_symlink():
        raise CellError(f"cell root {str(target)!r} is a symlink; refusing to remove it")
    real_target = confine(real_root, target)
    if real_target == real_root:
        raise CellError("refusing to remove the cells root itself")
    if not real_target.is_dir():
        raise CellError(f"cell root {str(real_target)!r} is not a directory")

    # Sealed trees are mode 0o555 and cannot be unlinked from until the
    # directory bit is restored. Restore top-down, remove after.
    for current, dirnames, filenames in os.walk(real_target):
        os.chmod(current, stat.S_IRWXU)
    shutil.rmtree(real_target)
