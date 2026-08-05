"""Freeze the bytes sent for external review, and bind them to a digest.

Two jobs. First, assemble the source an external reviewer needs, split into
parts small enough to survive a paste. Second, bind the result: the digest
covers exactly the bytes shown, so a verdict can only be ingested against the
tree it was actually formed over. That binding is what stops a review of
superseded code riding forward as though it still applied.

The grounding quiz proves the reviewer had the bytes. Questions are quotation
only — quote line N of file F — deliberately, because counting and hashing are
things an honest reviewer gets wrong and a gate that rejects honest reviewers
is worse than no gate. Retrieval is the discriminator: trivial with the text
in hand, impossible without it.

Expected answers are written to the meta file, never into the pastable parts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import canary
from claims import ClaimsError, digest_files, load, repo_root

# Bigger than this and a paste starts getting truncated by the receiving UI.
PART_CHAR_BUDGET = 45_000

QUIZ_QUESTIONS = 4
MIN_QUIZ_LINE_LEN = 24


class BundleError(ValueError):
    """The bundle could not be assembled."""


def _quiz_candidates(text: str) -> list[int]:
    """1-indexed lines substantial enough to be an unambiguous quotation."""
    out = []
    for n, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if len(stripped) >= MIN_QUIZ_LINE_LEN and not stripped.startswith("#"):
            out.append(n)
    return out


def build_quiz(files: dict[str, str], seed: str,
               count: int = QUIZ_QUESTIONS) -> list[dict]:
    """Pick quotation questions deterministically from the bundle's own bytes.

    Seeded by the bundle digest, so the questions change whenever the code
    changes and cannot be memorised across cycles, while staying reproducible
    for the same bundle.
    """
    by_file = {rel: _quiz_candidates(files[rel]) for rel in sorted(files)}
    by_file = {rel: lines for rel, lines in by_file.items() if lines}
    if not by_file:
        raise BundleError("no line in the bundle is long enough to quote")

    # Round-robin across files rather than sampling one flat pool. A flat pool
    # can land every question on one file by chance, and a reviewer who answers
    # four questions about one file has not shown they read the others.
    order = sorted(by_file)
    questions = []
    used: set[tuple[str, int]] = set()
    for i in range(count):
        rel = order[i % len(order)]
        candidates = by_file[rel]
        h = hashlib.sha256(f"{seed}:{rel}:{i}".encode()).digest()
        start = int.from_bytes(h[:8], "big") % len(candidates)
        for probe in range(len(candidates)):
            n = candidates[(start + probe) % len(candidates)]
            if (rel, n) not in used:
                break
        else:
            continue
        used.add((rel, n))
        questions.append({
            "id": f"G{len(questions) + 1}",
            "question": f"Quote line {n} of {rel} verbatim.",
            "expected": files[rel].splitlines()[n - 1].strip(),
        })
    if not questions:
        raise BundleError("could not build any grounding question")
    return questions


def _read_subjects(claim_path: Path, extra: list[str],
                   root: Path) -> tuple[list[str], dict[str, str]]:
    rels: set[str] = set(extra)
    for claim in load(claim_path):
        rels.update(claim["subject_files"])
    files: dict[str, str] = {}
    for rel in sorted(rels):
        target = root / rel
        if not target.is_file():
            raise BundleError(f"bundle subject not on disk: {rel}")
        files[rel] = target.read_text(encoding="utf-8")
    if not files:
        raise BundleError("bundle would be empty — no subject files")
    return sorted(rels), files


def _split_parts(blocks: list[tuple[str, str]]) -> list[list[tuple[str, str]]]:
    """Pack (title, body) blocks into parts under the paste budget.

    A single block larger than the budget gets its own part rather than being
    cut — a truncated source file produces a review of code that does not
    exist, which is the failure this whole module is built to prevent.
    """
    parts: list[list[tuple[str, str]]] = []
    current: list[tuple[str, str]] = []
    size = 0
    for title, body in blocks:
        if current and size + len(body) > PART_CHAR_BUDGET:
            parts.append(current)
            current, size = [], 0
        current.append((title, body))
        size += len(body)
    if current:
        parts.append(current)
    return parts


def build(claim_path: Path, cycle: int, out_dir: Path, role: str,
          extra: list[str], root: Path | None = None,
          with_canary: bool = True) -> dict:
    root = root or repo_root()
    rels, files = _read_subjects(claim_path, extra, root)
    bundle_digest = digest_files(rels, root)

    # The canary is synthetic, so it stays out of the on-disk digest — that
    # digest means "these are the real bytes", and a plant is not one of them.
    plant = canary.select(bundle_digest, rels) if with_canary else None
    shown = dict(files)
    if plant:
        shown[plant["filename"]] = plant["body"]

    # Quiz drawn from the real files only. Grounding exists to prove the
    # reviewer read the code under review; a question about the plant proves
    # nothing about that.
    quiz = build_quiz(files, bundle_digest)

    blocks = [(name, shown[name]) for name in sorted(shown)]
    parts = _split_parts(blocks)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = []
    for i, part in enumerate(parts, start=1):
        lines = [
            f"BLACKSMITH REVIEW BUNDLE — cycle {cycle}, part {i} of {len(parts)}",
            f"role: {role}",
            f"bundle_digest: {bundle_digest}",
            "",
            "This part carries verbatim source. Do not infer content you cannot see.",
            "",
        ]
        if i == len(parts):
            lines += [
                "=" * 60,
                "GROUNDING — answer every question from the text above.",
                "A wrong answer discards this entire review.",
                "",
            ]
            lines += [f"{q['id']}: {q['question']}" for q in quiz]
            lines.append("")
        for title, body in part:
            lines += ["=" * 60, f"FILE: {title}", "=" * 60, body, ""]
        path = out_dir / f"bundle.part{i}.txt"
        path.write_text("\n".join(lines), encoding="utf-8")
        written.append(str(path))

    meta = {
        "cycle": cycle,
        "role": role,
        "bundle_digest": bundle_digest,
        "subject_files": rels,
        "shown_files": sorted(shown),
        "parts": written,
        "grounding": quiz,
        "canary": {k: plant[k] for k in ("filename", "line", "kind", "hint")}
                  if plant else None,
    }
    (out_dir / "bundle.meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bundle", description="Freeze a review bundle and bind it.")
    parser.add_argument("--claims", required=True)
    parser.add_argument("--cycle", required=True, type=int)
    parser.add_argument("--out", required=True)
    parser.add_argument("--role", default="auditor",
                        choices=("auditor", "checker", "tiebreak"))
    parser.add_argument("--include", action="append", default=[],
                        help="extra repo-relative file to bundle; repeatable")
    parser.add_argument("--no-canary", action="store_true",
                        help="omit the planted defect; the review can then no "
                             "longer be tested for sensitivity")
    args = parser.parse_args(argv)

    try:
        meta = build(Path(args.claims), args.cycle, Path(args.out),
                     args.role, args.include, with_canary=not args.no_canary)
    except (BundleError, ClaimsError) as exc:
        print(f"bundle: {exc}", file=sys.stderr)
        return 2
    redacted = {k: v for k, v in meta.items() if k not in ("grounding", "canary")}
    print(json.dumps(redacted, indent=2))
    print(f"\n{len(meta['grounding'])} grounding questions and the canary "
          f"answer are in bundle.meta.json — do not paste that file.",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
