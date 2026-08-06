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
    cell_pre_hash: str
    cell_post_hash: str
    delta: str
    verdict: str

    def __post_init__(self):
        for name in ("cell_pre_hash", "cell_post_hash"):
            _require(getattr(self, name), name)
        if self.delta not in DELTAS:
            raise EvidenceLogError(f"delta must be one of {DELTAS}, got {self.delta!r}")
        if self.verdict not in gauge.VERDICTS:
            raise EvidenceLogError(
                f"verdict must be one of {gauge.VERDICTS}, got {self.verdict!r}")

    def render(self) -> str:
        return (
            "## Integrity Report\n"
            f"- cell pre-hash: {self.cell_pre_hash}\n"
            f"- cell post-hash: {self.cell_post_hash}\n"
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


def write(job: str, model: str, timestamp: str, launch: LaunchRecord,
          execution: Execution, integrity: IntegrityReport, lesson: str,
          out_dir: Path | None = None) -> Path:
    """Render one entry and write it under the `<job>.<model>.<timestamp>.md`
    convention `run_bound.py` already uses, so both land in the same set.

    Refuses to overwrite an existing entry — each entry is frozen once
    written, the same rule `attest.Attestation` holds for a single
    measurement.
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
    return target
