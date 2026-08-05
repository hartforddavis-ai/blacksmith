"""Generate STATE.md from the repository. No model authors any line of it.

Every prompt in the loop this replaces opened with a hand-compiled CURRENT
STATE block, carried forward from the previous cycle's own summary and marked
with ticks. One of them asserted an independent review that never happened.
Nothing re-derived any of it, which is SPEC §2 rule 4 broken by the pipeline
building the thing that enforces it.

So the inputs here are files and process results, and that is all. Notably
absent: CANDIDATE.json. The generator's own account of its cycle is never read
by this module, because a state block that can quote the generator is a state
block the generator can write.

There is no tick mark in the output vocabulary. A tick reads identically
whoever typed it; a provenance token does not.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import claims as claims_mod
from claims import ClaimsError, repo_root

BLACKSMITH_DIR = "Documents/_PROJECTS/SOFTWARE/blacksmith"
SPEC = f"{BLACKSMITH_DIR}/SPEC.md"
SCOTT_MARKER = re.compile(r"\[SCOTT[^\]]*\]")

HERE = Path(__file__).resolve().parent


def git_head(root: Path) -> str:
    proc = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
                          capture_output=True, text=True)
    return proc.stdout.strip() or "UNKNOWN"


def git_range_summary(root: Path, since: str | None) -> list[str]:
    if not since:
        return []
    proc = subprocess.run(
        ["git", "-C", str(root), "log", "--oneline", f"{since}..HEAD"],
        capture_output=True, text=True)
    return [line for line in proc.stdout.strip().splitlines() if line]


def scott_markers(root: Path) -> list[dict]:
    """Grep the SPEC live. A marker resolved in conversation is still open."""
    path = root / SPEC
    if not path.is_file():
        return [{"line": 0, "text": "SPEC.md absent — cannot enumerate markers"}]
    out = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if SCOTT_MARKER.search(line):
            out.append({"line": n, "text": line.strip()})
    return out


def build_order(path: Path | None = None) -> list[dict]:
    return json.loads((path or HERE / "build_order.json").read_text(encoding="utf-8"))


def next_objective(steps: list[dict], ledger: list[dict] | None = None,
                   root: Path | None = None) -> dict | None:
    """First OPEN step whose prerequisites are all done. Blocked steps skip.

    A step counts as done when the ledger says so — every claim raised under it
    at CONFIRMED — or when build_order.json records DONE by hand.

    The derived half is what makes the order move at all. Nothing in this
    pipeline ever wrote that status field, so every cycle was assigned step 1
    again however much work landed; the build order could only advance if Scott
    edited the file, and the RUNBOOK never told him to. A step closed by
    evidence is skipped whatever its recorded status still says.
    """
    ledger = ledger if ledger is not None else []
    done = {s["step"] for s in steps if s["status"] == "DONE"}

    # A step blocked on the owner can never be closed by evidence, however many
    # claims confirm against it. Today nothing can stamp a claim with a blocked
    # step — this function refuses to assign one, so it never reaches
    # objective.json — but that is a consequence of another rule rather than a
    # statement of this one, and step 0 is the SPEC's own kill criterion. A
    # design session Scott has not held is not a thing a generator can prove.
    blocked = {s["step"] for s in steps if s["status"] == "BLOCKED_OWNER"}
    done |= {s["step"] for s in steps
             if s["step"] not in blocked
             and claims_mod.step_is_done(ledger, s["step"], root)}
    for step in sorted(steps, key=lambda s: s["step"]):
        if step["status"] != "OPEN" or step["step"] in done:
            continue
        if all(req in done for req in step.get("requires", [])):
            return step
    return None


def _claim_rows(ledger: list[dict], root: Path) -> list[dict]:
    rows = []
    for claim in ledger:
        rows.append({
            "id": claim["id"],
            "provenance": claims_mod.provenance(claim, root),
            "text": claim["text"],
            "reviews": claim.get("reviews", []),
            "disagreements": claims_mod.disagreements(claim),
        })
    return rows


def review_summary(rows: list[dict]) -> list[str]:
    """The section that would have caught the false claim, stated plainly."""
    vendors = sorted({r["vendor"] for row in rows for r in row["reviews"]})
    independent = sorted(v for v in vendors if claims_mod.is_independent(v))
    same_family = sorted(v for v in vendors if not claims_mod.is_independent(v))

    if not independent:
        out = ["INDEPENDENT REVIEW: NONE ON RECORD",
               "",
               "No external verdict has ever been ingested. Any statement that a",
               "review occurred is unsupported by this repository."]
        if same_family:
            out += ["",
                    f"Recorded but not independent — same family as the generator: "
                    f"{', '.join(same_family)}. Held as commentary, never as evidence."]
        return out

    lines = [f"INDEPENDENT REVIEW: {len(independent)} external vendor(s) on "
             f"record — {', '.join(independent)}"]
    if same_family:
        lines.append(f"  same-family reviews recorded but not counted: "
                     f"{', '.join(same_family)}")
    live = [r for r in rows if r["provenance"] in ("REVIEWED", "CONFIRMED")]
    stale = [r for r in rows if r["provenance"] == "STALE"]
    lines.append(f"  claims currently carrying a bound review: {len(live)}")
    lines.append(f"  claims whose evidence decayed against current bytes: {len(stale)}")
    return lines


def render(root: Path, since: str | None, claims_path: Path,
           order_path: Path | None = None) -> str:
    ledger = claims_mod.load(claims_path)
    rows = _claim_rows(ledger, root)
    steps = build_order(order_path)
    objective = next_objective(steps, ledger, root)
    markers = scott_markers(root)
    commits = git_range_summary(root, since)

    counts = {p: 0 for p in claims_mod.PROVENANCE}
    for row in rows:
        counts[row["provenance"]] += 1

    contested = [r for r in rows if r["disagreements"]]
    blocked = [s for s in steps if s["status"] == "BLOCKED_OWNER"]

    # The freeze conditions, each one a fact about a file on disk. This block
    # used to be the string "NOT READY" printed unconditionally, under a
    # sentence claiming it had been derived from the claim table — the exact
    # defect this pipeline exists to catch, in the module that generates the
    # page asserting nothing here is asserted.
    unmet = []
    if not rows:
        unmet.append("no claim has been raised")
    elif counts["CONFIRMED"] != len(rows):
        unmet.append(f"{counts['CONFIRMED']} of {len(rows)} claims are CONFIRMED")
    if blocked:
        unmet.append(f"{len(blocked)} build-order step(s) blocked on the owner: "
                     + ", ".join(f"step {s['step']}" for s in blocked))
    if markers:
        unmet.append(f"{len(markers)} [SCOTT] ruling(s) still open in SPEC.md")
    if contested:
        unmet.append(f"{len(contested)} claim(s) contested and unresolved")

    out = [
        "# STATE — generated by pipeline/state.py",
        "",
        f"generated: {datetime.now(timezone.utc).isoformat()}",
        f"git HEAD: {git_head(root)}",
        "author: none. Every line below is derived from files on disk or from a",
        "process exit code. No model wrote any part of this, and no prior cycle's",
        "summary was read to produce it.",
        "",
        "## FREEZE",
        "",
    ]
    if unmet:
        out += ["NOT READY — and this line is not a judgement. It is the freeze",
                "conditions evaluated against files on disk this run. Outstanding:",
                ""]
        out += [f"- {reason}" for reason in unmet]
    else:
        out += ["READY — every claim CONFIRMED, no step blocked on the owner, no",
                "[SCOTT] ruling open in SPEC.md, no claim contested. Derived from",
                "the same evidence as the table below, not declared by anyone."]
    out += [
        "",
        "## ASSIGNED OBJECTIVE THIS CYCLE",
        "",
    ]
    if objective:
        out += [f"SPEC §9 step {objective['step']} — {objective['name']}",
                f"  {objective['why']}"]
    else:
        out += ["NONE — every step is DONE or BLOCKED. Do not invent one."]
    out.append("")

    if blocked:
        out.append("Blocked on the owner, skipped by the assigner, not by the generator:")
        for step in blocked:
            out.append(f"  step {step['step']} — {step['name']}: {step['why']}")
        out.append("")

    out += ["## INDEPENDENT REVIEW", ""] + review_summary(rows) + [""]

    out += ["## CLAIMS", "",
            "Provenance is derived on every run from evidence bound to a digest of",
            "the subject files. It is not stored, so it cannot be edited to say",
            "something else. Only CONFIRMED closes a gate.",
            ""]
    if rows:
        out += ["| claim | provenance | statement |", "|---|---|---|"]
        for row in rows:
            text = row["text"].replace("|", "\\|")
            out.append(f"| {row['id']} | {row['provenance']} | {text} |")
        out.append("")
        out.append("counts: " + ", ".join(
            f"{p}={counts[p]}" for p in claims_mod.PROVENANCE if counts[p]))
    else:
        out.append("No claims raised. That is a valid state, not an omission.")
    out.append("")

    if contested:
        out += ["### Contested — recorded, not resolved", ""]
        for row in contested:
            detail = "; ".join(
                f"{d['verdict']} from {', '.join(d['vendors'])}"
                for d in row["disagreements"])
            out.append(f"- {row['id']}: {detail}")
        out.append("")

    out += ["## OPEN RULINGS — grepped from SPEC.md this run", ""]
    for marker in markers:
        out.append(f"- SPEC.md:{marker['line']} — {marker['text'][:160]}")
    out.append("")

    if since:
        out += [f"## COMMITS {since}..HEAD", ""]
        out += [f"- {line}" for line in commits] or ["- none"]
        out.append("")

    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="state", description="Generate STATE.md from the repository.")
    parser.add_argument("--claims", required=True)
    parser.add_argument("--since", default=None, help="git ref to summarise from")
    parser.add_argument("--out", default=None, help="write here instead of stdout")
    parser.add_argument("--order", default=None, help="alternate build_order.json")
    args = parser.parse_args(argv)

    try:
        text = render(repo_root(), args.since, Path(args.claims),
                      Path(args.order) if args.order else None)
    except ClaimsError as exc:
        print(f"state: {exc}", file=sys.stderr)
        return 2
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
