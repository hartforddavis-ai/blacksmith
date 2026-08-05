"""Drive the checker leg: emit its prompt, then parse what comes back.

Transport-agnostic by design. Today the transport is Scott's clipboard; the
`codex` CLI is quota-exhausted on the free plan until 20 Aug 2026 and an API
key is a purchase, not a dependency. Nothing above this line cares — `emit`
produces a prompt and `parse` consumes a response, and either end can be
automated later without the middle changing.

The claim list handed to the checker carries statements only. No provenance,
no prior verdict, not even its own from last cycle. A checker who knows a claim
was confirmed before is checking its memory, not the code.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import claims as claims_mod
from claims import ClaimsError

HERE = Path(__file__).resolve().parent
FENCE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


class CheckError(ValueError):
    """The checker prompt could not be built, or the response not parsed."""


# `how_i_tested` is meant to name the test and say who wrote it. Left unbounded
# it arrives as several hundred characters of the generator's narrative about
# its own confidence — which is the one thing roles/checker.md says the checker
# must not be given. Cut to the first sentence: enough to locate the test, too
# little to argue with.
PROVENANCE_STAMP_CHARS = 120


def _stamp(text: str) -> str:
    """First sentence of a provenance note, hard-capped."""
    first = str(text).strip().split(". ")[0].strip()
    if len(first) > PROVENANCE_STAMP_CHARS:
        first = first[:PROVENANCE_STAMP_CHARS].rsplit(" ", 1)[0] + "…"
    return first


def claim_brief(ledger: list[dict]) -> list[dict]:
    """Statements only. Stripping provenance here is the context gate."""
    return [{"id": c["id"],
             "text": c["text"],
             "subject_files": c["subject_files"],
             "how_i_tested": _stamp(
                 c.get("how_i_tested") or "not stated by the generator")}
            for c in ledger]


def emit(claims_path: Path, out_path: Path, role_path: Path | None = None) -> dict:
    ledger = claims_mod.load(claims_path)
    if not ledger:
        raise CheckError("no claims to check — nothing for this leg to do")
    brief = claim_brief(ledger)
    contract = (role_path or HERE / "roles" / "checker.md").read_text(encoding="utf-8")

    text = "\n".join([
        contract,
        "",
        "=" * 60,
        "CLAIMS TO ADJUDICATE",
        "=" * 60,
        "",
        json.dumps(brief, indent=2),
        "",
        "=" * 60,
        "The source and tests follow as bundle parts. Answer only after you have",
        "them. If a bundle part is missing, say so and return no claim rows —",
        "an unanswered claim is recorded as unanswered, which is correct, while",
        "a guess is recorded as a verdict, which is not.",
        "=" * 60,
        "",
    ])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    return {"claims": len(brief), "prompt": str(out_path)}


def extract_json(response: str) -> dict:
    """Pull the verdict object out of a pasted reply.

    Refuses ambiguity rather than guessing: prose around the block is fine,
    two candidate blocks is not.
    """
    fenced = FENCE.findall(response)
    if len(fenced) > 1:
        raise CheckError("response contains more than one JSON block — "
                         "cannot tell which is the verdict")
    candidates = fenced or []
    if not candidates:
        start, end = response.find("{"), response.rfind("}")
        if start == -1 or end <= start:
            raise CheckError("no JSON object found in the response")
        candidates = [response[start:end + 1]]
    try:
        parsed = json.loads(candidates[0])
    except json.JSONDecodeError as exc:
        raise CheckError(f"verdict block is not valid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise CheckError("verdict must be a JSON object")
    return parsed


def parse(response_path: Path, out_path: Path) -> dict:
    parsed = extract_json(response_path.read_text(encoding="utf-8"))
    out_path.write_text(json.dumps(parsed, indent=2) + "\n", encoding="utf-8")
    return {"verdict": str(out_path),
            "claim_rows": len(parsed.get("claims", [])),
            "findings": len(parsed.get("findings", []))}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check", description="Emit the checker prompt; parse its reply.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_emit = sub.add_parser("emit", help="write the checker prompt")
    p_emit.add_argument("--claims", required=True)
    p_emit.add_argument("--out", required=True)
    p_emit.add_argument("--role", default=None)

    p_parse = sub.add_parser("parse", help="extract the verdict from a reply")
    p_parse.add_argument("--response", required=True)
    p_parse.add_argument("--out", required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "emit":
            result = emit(Path(args.claims), Path(args.out),
                          Path(args.role) if args.role else None)
        else:
            result = parse(Path(args.response), Path(args.out))
    except (CheckError, ClaimsError, OSError) as exc:
        print(f"check: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
