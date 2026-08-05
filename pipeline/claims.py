"""The claim ledger, and the provenance rule that governs it.

A claim is a statement about the system that someone wants to be true. This
module never stores whether it *is* true. It stores the evidence, and derives
the provenance from that evidence every time it is asked — SPEC §2 rule 4,
applied to the pipeline that builds the SPEC.

Storing a provenance would make it forgeable by whoever can write the file.
Deriving it means the only thing that can be forged is evidence, and evidence
is bound to a digest of the exact bytes it was gathered over. Change the bytes
and the evidence stops matching; the claim decays to STALE on its own, with no
one deciding that it should.

Only CONFIRMED closes a gate. A generator can write nothing but ASSERTED.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

# Ordered strongest first; the first state a claim qualifies for is its state.
PROVENANCE = ("CONFIRMED", "REVIEWED", "MACHINE", "STALE", "ASSERTED")

# What a machine leg or a review leg can be, before they are combined.
VALID, STALE, NONE = "VALID", "STALE", "NONE"

MACHINE_KINDS = ("tests", "manifest", "assay", "git")
REVIEW_ROLES = ("auditor", "checker", "tiebreak")
REVIEW_VERDICTS = ("PROVES", "PARTIAL", "DOES_NOT_PROVE")

# The generator is Claude. A review from the same family is not independent
# however it is labelled — same lineage, correlated blind spots — so it cannot
# raise provenance no matter which role it is filed under. Enforced here rather
# than left to whoever fills in --vendor, because "use a different vendor" is a
# convention and conventions are what this pipeline exists to stop relying on.
GENERATOR_FAMILY = "anthropic"
VENDOR_FAMILY = {
    "claude": "anthropic", "opus": "anthropic", "sonnet": "anthropic",
    "haiku": "anthropic", "fable": "anthropic",
    "chatgpt": "openai", "gpt": "openai", "codex": "openai", "openai": "openai",
    "gemini": "google", "flash": "google", "google": "google",
    "grok": "xai", "xai": "xai",
}


def vendor_family(vendor: str) -> str:
    """Map a vendor string to its model family; unknown vendors stay unknown.

    An unrecognised vendor is treated as independent — refusing it outright
    would block a legitimate new reviewer, and the canary and grounding gates
    already catch one that is not doing the work.
    """
    name = str(vendor).strip().lower()
    for key, family in VENDOR_FAMILY.items():
        if key in name:
            return family
    return "unknown"


def is_independent(vendor: str) -> bool:
    return vendor_family(vendor) != GENERATOR_FAMILY

CLAIM_FIELDS = ("id", "text", "subject_files", "raised_cycle")


class ClaimsError(ValueError):
    """The claim ledger could not be read, or an entry is invalid."""


def repo_root(start: Path | None = None) -> Path:
    """The git root, found by walking up from this file — never from cwd.

    Ring 0's secure_import shipped with a cwd-relative TRUSTED_ROOT and had to
    be remediated (f908bc0). Same mistake, same fix, applied up front.
    """
    here = (start or Path(__file__)).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise ClaimsError(f"no git root above {here}")


def digest_files(paths: list[str], root: Path | None = None) -> str:
    """sha256 over the named files' bytes, order-independent.

    A missing file is not an error and not a blank — it contributes its own
    absence to the digest, so deleting a reviewed file invalidates the review
    rather than silently preserving it.
    """
    root = root or repo_root()
    h = hashlib.sha256()
    for rel in sorted(set(paths)):
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        target = root / rel
        if target.is_file():
            h.update(hashlib.sha256(target.read_bytes()).digest())
        else:
            h.update(b"ABSENT")
        h.update(b"\0")
    return h.hexdigest()


def _validate_claim(claim: dict, index: int) -> None:
    if not isinstance(claim, dict):
        raise ClaimsError(f"claims[{index}] is not an object")
    for field in CLAIM_FIELDS:
        if field not in claim:
            raise ClaimsError(f"claims[{index}] missing required field {field!r}")
    if not isinstance(claim["id"], str) or not claim["id"].strip():
        raise ClaimsError(f"claims[{index}] id must be a non-empty string")
    if not isinstance(claim["text"], str) or not claim["text"].strip():
        raise ClaimsError(f"claim {claim['id']!r}: text must be a non-empty string")
    files = claim["subject_files"]
    if not isinstance(files, list) or not files:
        raise ClaimsError(f"claim {claim['id']!r}: subject_files must be a non-empty list")
    if not all(isinstance(f, str) and f.strip() for f in files):
        raise ClaimsError(f"claim {claim['id']!r}: subject_files must all be strings")
    for rel in files:
        if Path(rel).is_absolute() or ".." in Path(rel).parts:
            raise ClaimsError(
                f"claim {claim['id']!r}: subject_files must be repo-relative "
                f"with no '..' segment, got {rel!r}")
    if not isinstance(claim["raised_cycle"], int):
        raise ClaimsError(f"claim {claim['id']!r}: raised_cycle must be an integer")
    if "objective_step" in claim and not isinstance(claim["objective_step"], int):
        raise ClaimsError(
            f"claim {claim['id']!r}: objective_step must be an integer")

    for row in claim.get("machine", []):
        if row.get("kind") not in MACHINE_KINDS:
            raise ClaimsError(
                f"claim {claim['id']!r}: machine kind {row.get('kind')!r} "
                f"not one of {MACHINE_KINDS}")
        if not isinstance(row.get("passed"), bool):
            raise ClaimsError(f"claim {claim['id']!r}: machine row needs a boolean 'passed'")
        if not row.get("files_digest"):
            raise ClaimsError(f"claim {claim['id']!r}: machine row needs a files_digest")

    for row in claim.get("reviews", []):
        if row.get("role") not in REVIEW_ROLES:
            raise ClaimsError(
                f"claim {claim['id']!r}: review role {row.get('role')!r} "
                f"not one of {REVIEW_ROLES}")
        if row.get("verdict") not in REVIEW_VERDICTS:
            raise ClaimsError(
                f"claim {claim['id']!r}: review verdict {row.get('verdict')!r} "
                f"not one of {REVIEW_VERDICTS}")
        if not row.get("files_digest"):
            raise ClaimsError(f"claim {claim['id']!r}: review row needs a files_digest")
        if not row.get("vendor"):
            raise ClaimsError(f"claim {claim['id']!r}: review row needs a vendor")


def validate(claims: list) -> list[dict]:
    if not isinstance(claims, list):
        raise ClaimsError("claims must be a JSON list")
    seen: set[str] = set()
    for i, claim in enumerate(claims):
        _validate_claim(claim, i)
        if claim["id"] in seen:
            raise ClaimsError(f"duplicate claim id {claim['id']!r}")
        seen.add(claim["id"])
    return claims


def load(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.is_file():
        return []
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ClaimsError(f"claims file is not valid JSON: {exc}") from exc
    return validate(raw)


def save(path: str | Path, claims: list[dict]) -> None:
    validate(claims)
    Path(path).write_text(
        json.dumps(claims, indent=2) + "\n", encoding="utf-8")


def _leg_state(rows: list[dict], current_digest: str, accept) -> str:
    """VALID if a qualifying row is bound to the current bytes, else STALE/NONE."""
    if not rows:
        return NONE
    qualifying = [r for r in rows if accept(r)]
    if not qualifying:
        return NONE
    if any(r["files_digest"] == current_digest for r in qualifying):
        return VALID
    return STALE


def provenance(claim: dict, root: Path | None = None) -> str:
    """Derive the claim's state from its evidence and the bytes on disk now."""
    current = digest_files(claim["subject_files"], root)
    machine = _leg_state(
        claim.get("machine", []), current, lambda r: r["passed"])
    review = _leg_state(
        claim.get("reviews", []), current,
        lambda r: (r["verdict"] == "PROVES"
                   and r["role"] in ("auditor", "checker")
                   and is_independent(r["vendor"])))

    if machine == VALID and review == VALID:
        return "CONFIRMED"
    if review == VALID:
        return "REVIEWED"
    if machine == VALID:
        return "MACHINE"
    if STALE in (machine, review):
        return "STALE"
    return "ASSERTED"


def closes_gate(claim: dict, root: Path | None = None) -> bool:
    return provenance(claim, root) == "CONFIRMED"


def step_is_done(ledger: list[dict], step: int, root: Path | None = None) -> bool:
    """Has this build-order step been closed by evidence?

    Derived like everything else here: the step is done when every claim raised
    under it stands at CONFIRMED. `build_order.json`'s status field cannot say
    so, because a status anyone can type is a status the generator can ask for.

    The "at least one claim" requirement is load-bearing, not defensive. An
    empty ledger satisfies "every claim is CONFIRMED" vacuously — for every step
    at once — which would close the whole build order on a fresh checkout.
    """
    raised = [c for c in ledger if c.get("objective_step") == step]
    return bool(raised) and all(closes_gate(c, root) for c in raised)


def disagreements(claim: dict) -> list[dict]:
    """Reviews of the same claim that reached different verdicts.

    Recorded, never resolved — resolving it is what the tiebreak leg is for,
    and a tiebreak that has not run is not a resolution.
    """
    current = {}
    for row in claim.get("reviews", []):
        current.setdefault(row["verdict"], []).append(row)
    if len(current) < 2:
        return []
    return [{"verdict": v, "vendors": [r["vendor"] for r in rows]}
            for v, rows in sorted(current.items())]
