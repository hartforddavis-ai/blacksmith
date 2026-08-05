"""The only writer of external-review evidence into the claim ledger.

`machine.py` writes the deterministic leg; nothing else writes at all. This
module takes a verdict returned by an external reviewer, checks it is bound to
bytes that were actually shown, and either records it or discards it whole.

Discard is all-or-nothing on purpose. A review that failed grounding has shown
it was not working from the source; keeping the half of it that looks plausible
is how a supplied verdict becomes a verdict. Every discard is written to the
rejection log, because the fact of ignoring a verdict is itself evidence
(SPEC §2 rule 4).

No model runs this. It is the pipeline's `promote`.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import claims as claims_mod
from claims import ClaimsError, REVIEW_ROLES, REVIEW_VERDICTS, repo_root

ACCEPTED = "ACCEPTED"
REJECTED_SHAPE = "REJECTED_SHAPE"
REJECTED_UNBOUND = "REJECTED_UNBOUND"
REJECTED_GROUNDING = "REJECTED_GROUNDING"
REJECTED_CITATION = "REJECTED_CITATION"
REJECTED_INSENSITIVE = "REJECTED_INSENSITIVE"

REFUSED_TRANSPORT = "REFUSED_TRANSPORT"

# Roles whose output is an open-ended defect hunt, and can therefore fail by
# finding nothing. The checker answers a closed question per claim, so silence
# is already visible there and a canary would prove nothing.
CANARY_ROLES = ("auditor", "tiebreak")

# How the bytes reached the reviewer, attested by the operator. Recorded on
# every review row: "who said it" without "how it got there" cannot distinguish
# a vendor boundary that was crossed from one that was asserted.
TRANSPORTS = ("browser", "api", "agent")

# An agent runs on this filesystem, and bundle.meta.json — the grounding
# answers and the canary's location — is on this filesystem. Grounding and the
# canary are the only two gates that catch a reviewer who did not do the work,
# and against a process that can read the answer key they measure nothing. The
# operator pasting into a browser tab cannot reach it; that inability is the
# gate. Refused rather than recorded-and-discounted, because a review that
# cannot be tested should never enter the ledger at all.
TRANSPORT_REFUSED_FOR_REVIEW = ("agent",)


class IngestError(ValueError):
    """The verdict could not be read."""


class TransportError(ValueError):
    """The declared transport cannot carry an external review."""


def _normalise(value: str) -> str:
    """Collapse whitespace and strip quoting a model may have added.

    Tolerant of reformatting, intolerant of different tokens — the quiz asks
    what the line says, not how it was indented.
    """
    text = str(value).strip()
    for wrapper in ('"""', "```", '"', "'", "`"):
        if text.startswith(wrapper) and text.endswith(wrapper) and len(text) > 2 * len(wrapper):
            text = text[len(wrapper):-len(wrapper)].strip()
    return " ".join(text.split())


def check_grounding(meta: dict, answers: dict) -> list[dict]:
    """Return the failures. Empty list means the reviewer had the bytes."""
    failures = []
    for question in meta["grounding"]:
        given = answers.get(question["id"])
        if given is None:
            failures.append({"id": question["id"], "reason": "unanswered"})
        elif _normalise(given) != _normalise(question["expected"]):
            failures.append({"id": question["id"], "reason": "wrong",
                             "given": str(given)[:200]})
    return failures


def check_citations(meta: dict, verdict: dict, root: Path) -> list[dict]:
    """Resolve every cited line against the bundled files.

    Existence only — no script can grade whether a line means what the note
    says it means. This removes the cheapest way to fabricate a citation, and
    claims nothing beyond that.
    """
    subjects = meta.get("shown_files") or meta["subject_files"]
    lengths: dict[str, int] = {}
    for rel in subjects:
        target = root / rel
        if target.is_file():
            lengths[rel] = len(target.read_text(encoding="utf-8").splitlines())
        else:
            # Shown but not on disk: the canary. Its lines cannot be counted
            # from the tree, so range is not checked for it.
            lengths[rel] = -1

    failures = []
    for row in verdict["claims"]:
        for cite in row.get("lines", []):
            text = str(cite)
            name, _, num = text.rpartition(":")
            if not name or not num.isdigit():
                failures.append({"claim": row["id"], "cite": text,
                                 "reason": "not in file:line form"})
                continue
            matches = [r for r in subjects if r == name or r.endswith("/" + name)]
            if not matches:
                failures.append({"claim": row["id"], "cite": text,
                                 "reason": "file was not in the bundle"})
                continue
            line, limit = int(num), lengths[matches[0]]
            if limit == -1:
                continue
            if line < 1 or line > limit:
                failures.append({"claim": row["id"], "cite": text,
                                 "reason": f"line out of range (file has "
                                           f"{lengths[matches[0]]} lines)"})
    return failures


def check_canary(meta: dict, verdict: dict, role: str) -> dict | None:
    """Did the reviewer find the planted defect? Returns the miss, or None.

    The only gate here that catches a false negative. Everything else proves
    the reviewer was honest; this proves it was awake.
    """
    plant = meta.get("canary")
    if not plant or role not in CANARY_ROLES:
        return None
    name = plant["filename"]
    for finding in verdict.get("findings", []):
        cited = str(finding.get("file", ""))
        if cited == name or cited.endswith("/" + name):
            return None
    return {"expected_file": name, "expected_line": plant["line"],
            "defect": plant["kind"],
            "findings_returned": len(verdict.get("findings", []))}


def _validate_shape(verdict: dict) -> None:
    if not isinstance(verdict, dict):
        raise IngestError("verdict must be a JSON object")
    for field in ("bundle_digest", "grounding", "claims"):
        if field not in verdict:
            raise IngestError(f"verdict missing required field {field!r}")
    if not isinstance(verdict["grounding"], dict):
        raise IngestError("verdict grounding must be an object of id -> answer")
    if not isinstance(verdict["claims"], list):
        raise IngestError("verdict claims must be a list")
    for i, row in enumerate(verdict["claims"]):
        if not isinstance(row, dict):
            raise IngestError(f"verdict claims[{i}] is not an object")
        if not row.get("id"):
            raise IngestError(f"verdict claims[{i}] has no claim id")
        if row.get("verdict") not in REVIEW_VERDICTS:
            raise IngestError(
                f"verdict claims[{i}]: {row.get('verdict')!r} not one of "
                f"{REVIEW_VERDICTS}")


def _log(log_path: Path, record: dict) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def check_transport(transport: str, role: str) -> None:
    """Refuse a transport that cannot carry an external review.

    Checked before the verdict is even read: the objection is to how the bytes
    moved, and no amount of well-formed JSON answers it.
    """
    if transport not in TRANSPORTS:
        raise TransportError(
            f"unknown transport {transport!r} — one of {TRANSPORTS}")
    if role in REVIEW_ROLES and transport in TRANSPORT_REFUSED_FOR_REVIEW:
        raise TransportError(
            f"transport {transport!r} cannot carry the {role!r} leg. An agent "
            f"runs on this filesystem and can read bundle.meta.json, which "
            f"holds the grounding answers and the canary's location, so "
            f"neither gate measures anything against it. Run this leg in a "
            f"browser tab and ingest with --transport browser.")


def ingest(verdict_path: Path, meta_path: Path, claims_path: Path,
           vendor: str, role: str, log_path: Path,
           root: Path | None = None, transport: str = "browser") -> dict:
    root = root or repo_root()
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    stamp = datetime.now(timezone.utc).isoformat()
    outcome = {"at": stamp, "vendor": vendor, "role": role,
               "transport": transport, "cycle": meta.get("cycle"),
               "bundle_digest": meta["bundle_digest"]}

    try:
        check_transport(transport, role)
    except TransportError as exc:
        outcome |= {"result": REFUSED_TRANSPORT, "detail": str(exc), "recorded": 0}
        _log(log_path, outcome)
        return outcome

    try:
        raw = json.loads(verdict_path.read_text(encoding="utf-8"))
        _validate_shape(raw)
    except (json.JSONDecodeError, IngestError) as exc:
        outcome |= {"result": REJECTED_SHAPE, "detail": str(exc), "recorded": 0}
        _log(log_path, outcome)
        return outcome

    if raw["bundle_digest"] != meta["bundle_digest"]:
        outcome |= {"result": REJECTED_UNBOUND,
                    "detail": "verdict names a different bundle than the one issued",
                    "claimed": raw["bundle_digest"], "recorded": 0}
        _log(log_path, outcome)
        return outcome

    failures = check_grounding(meta, raw["grounding"])
    if failures:
        outcome |= {"result": REJECTED_GROUNDING, "failures": failures,
                    "recorded": 0}
        _log(log_path, outcome)
        return outcome

    bad_cites = check_citations(meta, raw, root)
    if bad_cites:
        outcome |= {"result": REJECTED_CITATION, "failures": bad_cites,
                    "recorded": 0}
        _log(log_path, outcome)
        return outcome

    missed = check_canary(meta, raw, role)
    if missed:
        outcome |= {"result": REJECTED_INSENSITIVE, "canary": missed,
                    "recorded": 0}
        _log(log_path, outcome)
        return outcome

    ledger = claims_mod.load(claims_path)
    by_id = {c["id"]: c for c in ledger}
    recorded, unknown = 0, []
    for row in raw["claims"]:
        claim = by_id.get(row["id"])
        if claim is None:
            unknown.append(row["id"])
            continue
        # Bound to this claim's own files, not to the whole bundle — otherwise
        # editing any unrelated bundled file would decay every claim at once.
        claim.setdefault("reviews", []).append({
            "at": stamp,
            "vendor": vendor,
            "role": role,
            "transport": transport,
            "verdict": row["verdict"],
            "files_digest": claims_mod.digest_files(claim["subject_files"], root),
            "bundle_digest": meta["bundle_digest"],
            "cited_lines": row.get("lines", []),
            "note": row.get("note", ""),
        })
        recorded += 1

    claims_mod.save(claims_path, ledger)
    if raw.get("findings"):
        findings_path = meta_path.parent / f"findings.{role}.{vendor}.json"
        findings_path.write_text(
            json.dumps(raw["findings"], indent=2) + "\n", encoding="utf-8")

    outcome |= {"result": ACCEPTED, "recorded": recorded,
                "unknown_claim_ids": unknown,
                "findings": len(raw.get("findings", []))}
    _log(log_path, outcome)
    return outcome


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ingest", description="Record an external verdict, or discard it whole.")
    parser.add_argument("--verdict", required=True)
    parser.add_argument("--meta", required=True)
    parser.add_argument("--claims", required=True)
    parser.add_argument("--vendor", required=True,
                        help="gemini | chatgpt | grok — the vendor boundary being relied on")
    parser.add_argument("--role", required=True, choices=REVIEW_ROLES)
    parser.add_argument("--transport", required=True, choices=TRANSPORTS,
                        help="how the bytes reached the reviewer; 'agent' is "
                             "refused for every review role")
    parser.add_argument("--log", default=None)
    args = parser.parse_args(argv)

    meta_path = Path(args.meta)
    log_path = Path(args.log) if args.log else meta_path.parent / "ingest.log.jsonl"
    try:
        outcome = ingest(Path(args.verdict), meta_path, Path(args.claims),
                         args.vendor, args.role, log_path,
                         transport=args.transport)
    except (ClaimsError, OSError, json.JSONDecodeError) as exc:
        print(f"ingest: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(outcome, indent=2))
    return 0 if outcome["result"] == ACCEPTED else 1


if __name__ == "__main__":
    raise SystemExit(main())
