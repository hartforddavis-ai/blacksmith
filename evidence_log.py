"""Evidence log — formal proof chain. Ring 0, parent-side.

Formalises SPEC_EVIDENCE_LOG_SCHEMA.md: one markdown file per run, joining
Launch Record + Execution + Integrity Report + Proof Chain + Lesson into a
single entry. This module renders what it is given; it adjudicates nothing.
The verdict field is gauge's, taken verbatim — computing one here would put
a second adjudicator in the tree, which SPEC §2 rule 5 forbids.

`run_bound.py`'s Ollama calls still run with no cell around them, so they
have no integrity report to supply honestly — wiring them into this schema
would mean fabricating a pre/post-hash or leaving a required field blank,
and SPEC_EVIDENCE_LOG_SCHEMA.md is explicit that no field is optional. That
gap is real, not an oversight, and remains open.

The bound-occupant pivot (`occupant_bound.py`) does have a cell around it,
and exercised this module for the first time on 5 Aug 2026:
`runs/pivot_smoke.qwen3.5-9b.20260805T091739.md`, a genuine INTACT
integrity report with an honestly UNKNOWN gauge verdict (the bundle it was
adjudicated against was deliberately left partial, not fabricated).

Every field is required. `render` raises rather than writing a partial
entry — SPEC §2 rule 6, the same fail-closed rule cell.py and attest.py
hold.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import gauge

OUT_DIR = Path(__file__).resolve().parent / "runs"

DELTAS = ("CLEAN", "MODIFIED")


class EvidenceLogError(ValueError):
    """A required field was missing, empty, or out of range; nothing was written."""


def _require(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceLogError(f"{name} is required and must be a non-empty string")
    return value


@dataclass(frozen=True)
class LaunchRecord:
    launched_by: str
    started_at: str
    kernel_digest: str
    job_digest: str
    evidence_mode: str

    def __post_init__(self):
        for name in ("launched_by", "started_at", "kernel_digest",
                     "job_digest", "evidence_mode"):
            _require(getattr(self, name), name)

    def render(self) -> str:
        return (
            "## Launch Record\n"
            f"- launched by: {self.launched_by}\n"
            f"- started at: {self.started_at}\n"
            f"- kernel: {self.kernel_digest}\n"
            f"- job: {self.job_digest}\n"
            f"- evidence_mode: {self.evidence_mode}\n"
        )


@dataclass(frozen=True)
class Execution:
    first_token: str
    final_token: str
    exit_code: str

    def __post_init__(self):
        for name in ("first_token", "final_token", "exit_code"):
            _require(getattr(self, name), name)

    def render(self) -> str:
        return (
            "## Execution\n"
            f"- first token: {self.first_token}\n"
            f"- final token: {self.final_token}\n"
            f"- exit code: {self.exit_code}\n"
        )


@dataclass(frozen=True)
class IntegrityReport:
    makers_mark_pre: str
    makers_mark_post: str
    delta: str
    verdict: str

    def __post_init__(self):
        for name in ("makers_mark_pre", "makers_mark_post"):
            _require(getattr(self, name), name)
        if self.delta not in DELTAS:
            raise EvidenceLogError(f"delta must be one of {DELTAS}, got {self.delta!r}")
        if self.verdict not in gauge.VERDICTS:
            raise EvidenceLogError(
                f"verdict must be one of {gauge.VERDICTS}, got {self.verdict!r}")

    def render(self) -> str:
        return (
            "## Integrity Report\n"
            f"- maker's mark, pre: {self.makers_mark_pre}\n"
            f"- maker's mark, post: {self.makers_mark_post}\n"
            f"- delta: {self.delta}\n"
            f"- verdict: {self.verdict}\n"
        )


# Fixed prose per SPEC_EVIDENCE_LOG_SCHEMA.md — the chain's logic does not
# vary per run, only the values it chains together do.
PROOF_CHAIN = (
    "## Proof Chain\n"
    "1. Launch-record proves session started (timestamp, who, what job)\n"
    "2. Execution proves session ran (tokens arrived, exit status)\n"
    "3. Integrity-report proves output wasn't tampered — the delta line is\n"
    "   the evidence. The two hashes identify the measurements it compared;\n"
    "   they are never equal to each other, because each covers its own\n"
    "   phase name.\n"
    "4. Verdict proves adjudication (ACTIVE/FAILED/UNKNOWN/BYPASSED)\n"
    "5. **All four together = proof that session ran and output is "
    "credible**\n"
)


def render(job: str, model: str, timestamp: str, launch: LaunchRecord,
           execution: Execution, integrity: IntegrityReport, lesson: str) -> str:
    """Compose the schema's markdown. Raises rather than returning a partial entry."""
    _require(job, "job")
    _require(model, "model")
    _require(timestamp, "timestamp")
    _require(lesson, "lesson")
    if not isinstance(launch, LaunchRecord):
        raise EvidenceLogError("launch must be a LaunchRecord")
    if not isinstance(execution, Execution):
        raise EvidenceLogError("execution must be an Execution")
    if not isinstance(integrity, IntegrityReport):
        raise EvidenceLogError("integrity must be an IntegrityReport")

    return (
        f"# {job} · {model} · {timestamp}\n\n"
        f"{launch.render()}\n"
        f"{execution.render()}\n"
        f"{integrity.render()}\n"
        f"{PROOF_CHAIN}\n"
        "## Lesson\n"
        f"{lesson.strip()}\n"
    )


def _seal_path(entry: Path) -> Path:
    return entry.parent / (entry.name + ".sha256")


def write(job: str, model: str, timestamp: str, launch: LaunchRecord,
          execution: Execution, integrity: IntegrityReport, lesson: str,
          out_dir: Path | None = None) -> Path:
    """Render one entry and write it under the `<job>.<model>.<timestamp>.md`
    convention `run_bound.py` already uses, so both land in the same set.

    Refuses to overwrite an existing entry — each entry is frozen once
    written, the same rule `attest.Attestation` holds for a single
    measurement.

    A `<name>.md.sha256` sidecar is written beside it, holding the sha256 of
    the entry's exact bytes at write time. This does not prove the run was
    genuine — it proves the entry hasn't been edited since. Same-UID
    filesystem access is a real, named path (`launch.py`'s own docstring:
    "everything the parent can reach, the child can reach"), and nothing
    before this caught a post-write edit. `verify()` is the other half.
    """
    text = render(job, model, timestamp, launch, execution, integrity, lesson)
    target_dir = Path(out_dir) if out_dir is not None else OUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    safe_model = model.replace(":", "-")
    target = target_dir / f"{job}.{safe_model}.{timestamp}.md"
    if target.exists():
        raise EvidenceLogError(
            f"evidence log entry {str(target)!r} already exists; refusing to overwrite")
    target.write_text(text, encoding="utf-8")
    # Re-read rather than hash `text` from memory — the seal must certify
    # what is actually on disk, not what was intended to be written. Same
    # rule bundle.py states for contract_sha256: no module in this tree
    # trusts a stored/in-memory value over the real bytes.
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    _seal_path(target).write_text(digest + "\n", encoding="utf-8")
    return target


def verify(entry: Path) -> bool:
    """Recompute the entry's sha256 and compare to its sidecar.

    Raises EvidenceLogError if the sidecar is missing (an entry written
    before this existed, or one that never went through `write()`) rather
    than reporting a silent pass — a missing seal is not the same claim as
    a matching one.
    """
    entry = Path(entry)
    seal = _seal_path(entry)
    if not entry.is_file():
        raise EvidenceLogError(f"no such evidence log entry: {str(entry)!r}")
    if not seal.is_file():
        raise EvidenceLogError(f"no seal for {str(entry)!r}; cannot verify")
    recorded = seal.read_text(encoding="utf-8").strip()
    actual = hashlib.sha256(entry.read_bytes()).hexdigest()
    return actual == recorded
