"""The deterministic leg — checks the parent can run without asking anyone.

Manifest verification, the test suites, and the assay range scan. Each result
is bound to a digest of the files it was gathered over, so it decays the moment
those files change rather than standing as a permanent fact.

Nothing here interprets. A test that passes means a test passed; whether that
establishes the claim it was written for is the checker leg's question, and
this module deliberately cannot answer it. That separation is the whole reason
same-session test-writing stopped counting as confirmation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import claims as claims_mod
from claims import ClaimsError, digest_files, repo_root

BLACKSMITH_DIR = "Documents/_PROJECTS/SOFTWARE/blacksmith"
MANIFEST = f"{BLACKSMITH_DIR}/MANIFEST.sha256"

# Listed separately, not discovered recursively: `unittest discover` skips a
# non-package subdirectory, so running the parent alone silently omits these.
TEST_DIRS = (BLACKSMITH_DIR, "blacksmith", f"{BLACKSMITH_DIR}/pipeline")


class MachineError(RuntimeError):
    """A deterministic check could not be run at all."""


def verify_manifest(root: Path | None = None) -> dict:
    """Re-hash every file the manifest names. Missing file is a failure."""
    root = root or repo_root()
    path = root / MANIFEST
    if not path.is_file():
        return {"kind": "manifest", "passed": False, "detail": "MANIFEST.sha256 absent",
                "checked": 0}
    base = path.parent
    mismatches, checked = [], 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, _, name = line.partition("  ")
        target = base / name.strip()
        checked += 1
        if not target.is_file():
            mismatches.append({"file": name.strip(), "reason": "absent"})
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected.strip():
            mismatches.append({"file": name.strip(), "reason": "hash mismatch"})
    return {"kind": "manifest", "passed": not mismatches, "checked": checked,
            "mismatches": mismatches}


def run_tests(root: Path | None = None) -> dict:
    """Run both trees' suites. Exit code is the result; no output is parsed.

    stdlib unittest, not pytest — pytest is not installed on this machine and
    both existing suites are written against unittest. Discovery runs with cwd
    set to the tree so the flat `import promote` style in those tests resolves.
    """
    root = root or repo_root()
    results = []
    for rel in TEST_DIRS:
        target = root / rel
        if not target.is_dir():
            results.append({"dir": rel, "passed": False, "detail": "absent"})
            continue
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", ".",
             "-p", "test_*.py"],
            capture_output=True, text=True, cwd=str(target))
        results.append({
            "dir": rel,
            "passed": proc.returncode == 0,
            "exit_code": proc.returncode,
            "tail": proc.stderr.strip().splitlines()[-1:] or [""],
        })
    return {"kind": "tests", "passed": all(r["passed"] for r in results),
            "suites": results}


NO_RECORD = 10


def assay_range(git_range: str, record: Path | None = None,
                root: Path | None = None) -> dict:
    """Run Assay's deterministic scan over a commit range.

    Without a record Assay exits NO_RECORD by design — it has findings but
    nothing to gate them against. That is not a failure, and recording it as
    one would put a false negative row on every claim. `passed: None` means
    informational: it is reported and excluded from evidence.
    """
    root = root or repo_root()
    assay = root / "Documents/_PROJECTS/SOFTWARE/assay/assay.py"
    if not assay.is_file():
        return {"kind": "assay", "passed": False, "detail": "assay.py absent"}
    out = root / ".pipeline-tmp-changeset.json"
    try:
        proc = subprocess.run(
            [sys.executable, str(assay), "collect", "--git-range", git_range,
             "--repo", str(root), "--out", str(out)],
            capture_output=True, text=True)
        if proc.returncode != 0:
            return {"kind": "assay", "passed": False,
                    "detail": proc.stderr.strip()[:400]}
        cmd = [sys.executable, str(assay), "run", "--changeset", str(out),
               "--json", "--no-ledger"]
        if record:
            cmd += ["--record", str(record)]
        scan = subprocess.run(cmd, capture_output=True, text=True)
        if not record and scan.returncode == NO_RECORD:
            return {"kind": "assay", "passed": None, "exit_code": NO_RECORD,
                    "range": git_range,
                    "detail": "scan only — no record supplied to gate against"}
        return {"kind": "assay", "passed": scan.returncode == 0,
                "exit_code": scan.returncode,
                "range": git_range}
    finally:
        out.unlink(missing_ok=True)


def record(claims_path: Path, results: list[dict],
           root: Path | None = None) -> int:
    """Attach passing/failing results to every claim, bound to its own files."""
    root = root or repo_root()
    ledger = claims_mod.load(claims_path)
    stamp = datetime.now(timezone.utc).isoformat()
    written = 0
    evidence = [r for r in results if r["passed"] is not None]
    for claim in ledger:
        current = digest_files(claim["subject_files"], root)
        for result in evidence:
            claim.setdefault("machine", []).append({
                "at": stamp,
                "kind": result["kind"],
                "passed": bool(result["passed"]),
                "files_digest": current,
            })
            written += 1
    claims_mod.save(claims_path, ledger)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="machine", description="Run the deterministic leg and record it.")
    parser.add_argument("--claims", required=True)
    parser.add_argument("--git-range", default=None,
                        help="run Assay over this range as well")
    parser.add_argument("--skip-tests", action="store_true",
                        help="report tests as not run rather than running them")
    parser.add_argument("--record", action="store_true",
                        help="write the results into the claim ledger")
    args = parser.parse_args(argv)

    results = [verify_manifest()]
    if not args.skip_tests:
        results.append(run_tests())
    if args.git_range:
        results.append(assay_range(args.git_range))

    written = 0
    if args.record:
        try:
            written = record(Path(args.claims), results)
        except ClaimsError as exc:
            print(f"machine: {exc}", file=sys.stderr)
            return 2

    print(json.dumps({"results": results, "rows_written": written}, indent=2))
    return 0 if all(r["passed"] is not False for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
