"""Regenerate MANIFEST.sha256 from the tree, rather than by hand.

No security claim is made here. A manifest the author edits by hand records
what the author believed; this records what is on disk. The difference only
matters in one direction, and it is the direction that lets a changed file keep
a stale hash next to it.

The membership rule is a glob, not a list. A hand-maintained list is wrong the
first time someone adds a Ring 0 module and forgets the manifest, and that
particular wrongness is silent: `verify_manifest` re-hashes what it is told
about, so a file nobody listed passes by not being checked. Globbing makes the
failure mode "a junk file got hashed", which is visible in the diff.

Tests are excluded deliberately. The manifest is the sealed set the parent
attests before launch; a test file changing is not a Ring 0 integrity event.

This module is not excluded. It decides what the sealed set contains, so a
manifest that skips its own author reports all clear on the edit worth making.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "MANIFEST.sha256"

FIXED = ("ASSUMPTIONS.md", "SPEC.md", "contract.json")


def members(root: Path | None = None) -> list[str]:
    """Every Ring 0 source plus the spec, the assumptions, and the contract."""
    root = root or HERE
    sources = sorted(
        p.name for p in root.glob("*.py") if not p.name.startswith("test_"))
    fixed = sorted(name for name in FIXED if (root / name).is_file())
    return fixed + sources


def render(root: Path | None = None) -> str:
    root = root or HERE
    lines = []
    for name in members(root):
        digest = hashlib.sha256((root / name).read_bytes()).hexdigest()
        lines.append(f"{digest}  {name}")
    return "\n".join(lines) + "\n"


def as_check() -> dict:
    """Render the manifest's own re-derivation as a gauge check entry.

    Compares `render()` to `MANIFEST.sha256` on disk -- the same comparison
    `--check` already performs. No second hashing path: this reads the
    existing result rather than re-deriving Ring 0 integrity a different way,
    which is the drift `members()`'s docstring warns a hand-maintained list
    would silently reintroduce.

    No `root` argument, matching `main()`: `MANIFEST` is a fixed path to the
    real tree's sealed manifest, so hashing an arbitrary root and comparing it
    against that fixed file would not be a check of that root, only a
    guaranteed mismatch dressed up as one.

    A missing manifest omits the outcome key entirely, which gauge reads as
    indeterminate. SPEC §4: a missing manifest reports integrity UNKNOWN and
    is never filled in later -- that rule binds this manifest as much as the
    cell's.
    """
    current = render()
    count = len(members())
    if not MANIFEST.is_file():
        return {"detail": f"{MANIFEST.name} is absent; the Ring 0 set was never sealed"}
    on_disk = MANIFEST.read_text(encoding="utf-8")
    if on_disk != current:
        return {"outcome": "FAIL",
                "detail": f"manifest is stale against {count} files on disk"}
    return {"outcome": "PASS", "detail": f"manifest current: {count} files"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="manifest", description="Regenerate or check MANIFEST.sha256.")
    parser.add_argument("--check", action="store_true",
                        help="exit 1 if the manifest on disk is not current")
    args = parser.parse_args(argv)

    current = render()
    if args.check:
        on_disk = MANIFEST.read_text(encoding="utf-8") if MANIFEST.is_file() else ""
        if on_disk == current:
            print(f"manifest current: {len(members())} files")
            return 0
        print("manifest is stale; run without --check to regenerate",
              file=sys.stderr)
        return 1

    MANIFEST.write_text(current, encoding="utf-8")
    print(f"manifest written: {len(members())} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
