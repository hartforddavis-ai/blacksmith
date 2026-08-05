"""Drive one cycle, and say at every point what has actually been established.

The loop this replaces had no orchestrator: each cycle was a prompt someone
assembled by hand from the last cycle's summary, which is how an independent
review that never happened ended up recorded as complete. Here the steps are
ordered, the state is regenerated from the repository between them, and the
parts a model performs are the only parts a model performs.

    python3.12 cycle.py start --cycle 1
    python3.12 cycle.py bundle --cycle 1 --role auditor
    python3.12 cycle.py ingest --cycle 1 --role auditor --vendor gemini \\
        --response cycles/001/auditor.reply.txt
    python3.12 cycle.py status --cycle 1

`start` assigns the objective and writes the generator's prompt. What happens
between `start` and `bundle` is the generator working — this module does not
run it, supervise it, or take its word for anything afterwards.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import bundle as bundle_mod
import check as check_mod
import claims as claims_mod
import ingest as ingest_mod
import machine as machine_mod
import state as state_mod
from claims import ClaimsError, repo_root

HERE = Path(__file__).resolve().parent
CYCLES = HERE / "cycles"
CLAIMS = HERE / "claims.json"
LOG = HERE / "CYCLE_LOG.jsonl"

# Always bundled alongside the claims' own subject files.
ALWAYS_INCLUDE = ("Documents/_PROJECTS/SOFTWARE/blacksmith/SPEC.md",)


def cycle_dir(n: int) -> Path:
    return CYCLES / f"{n:03d}"


def _log(record: dict) -> None:
    record["at"] = datetime.now(timezone.utc).isoformat()
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def start(n: int, since: str | None, budget: str) -> dict:
    """Regenerate STATE.md, assign the objective, write the generator prompt."""
    root = repo_root()

    # Every input read before a single byte is written. A half-built cycle
    # directory holding a STATE.md and no prompt reads to an operator as a
    # cycle that started.
    contract = (HERE / "roles" / "generator.md").read_text(encoding="utf-8")
    state_text = state_mod.render(root, since, CLAIMS)
    steps = state_mod.build_order()
    objective = state_mod.next_objective(steps, claims_mod.load(CLAIMS), root)

    out = cycle_dir(n)
    out.mkdir(parents=True, exist_ok=True)
    (out / "STATE.md").write_text(state_text, encoding="utf-8")

    # Recorded at assignment, not re-derived at load: between the two, the
    # build order may have moved, and the claims belong to the step that was
    # actually put in front of the generator.
    (out / "objective.json").write_text(
        json.dumps({"cycle": n,
                    "step": objective["step"] if objective else None,
                    "name": objective["name"] if objective else None},
                   indent=2) + "\n", encoding="utf-8")

    # A restarted cycle used to overwrite the prompt in place, so three starts
    # left one file and no way to say which one drove the session. Keep them
    # all: which bytes a model was given is the first thing an audit asks.
    prompt_path = out / "generator.prompt.md"
    if prompt_path.exists():
        seq = 2
        while (out / f"generator.prompt.{seq}.md").exists():
            seq += 1
        prompt_path = out / f"generator.prompt.{seq}.md"

    prompt = "\n".join([
        contract,
        "",
        "=" * 60,
        f"BUDGET CEILING THIS CYCLE: {budget}",
        "Stop when the objective is done or genuinely blocked, and say which.",
        "=" * 60,
        "",
        state_text,
        "",
        "=" * 60,
        "OPERATOR HANDOFF",
        "=" * 60,
        "",
        "Scott runs this cycle from RUNBOOK.md, which he has and you do not.",
        "Your deliverable is the work and CANDIDATE.json. When you are done,",
        "say so and stop; he takes it from there.",
        "",
        "Your work will be reviewed by parties whose identity, vendor, and",
        "method are deliberately withheld from you. Do not write for them, do",
        "not anticipate their checks, and do not shape CANDIDATE.json to pass",
        "anything. Write what is true about what you did.",
    ])
    prompt_path.write_text(prompt, encoding="utf-8")

    record = {"cycle": n, "step": "start",
              "objective": objective["name"] if objective else None,
              "objective_step": objective["step"] if objective else None,
              "budget": budget, "prompt_file": prompt_path.name}
    _log(record)
    return record | {"prompt": str(prompt_path)}


def _candidates(out: Path) -> list[Path]:
    """Every candidate in the cycle, oldest first. The last one is the live one.

    `start` never overwrites a prompt — it writes generator.prompt.2.md, then
    .3.md — and a generator that finds a CANDIDATE.json already there follows
    the same convention. Reading the unnumbered name unconditionally meant a
    restarted cycle loaded the stale file, matched every id against the ledger,
    and reported `added: 0` with exit 0: a silent pass over claims nothing had
    opened. Cycle 1 lost eight that way.

    Reading only the newest moves that silence rather than ending it — claims
    raised in an earlier candidate and absent from a later one would vanish
    unmentioned. Merging every file by id is the wrong correction: it would
    resurrect a claim the generator deliberately withdrew. So `load` reads the
    newest and *names* the ones it passed over, leaving the operator to judge.
    """
    numbered = []
    for p in out.glob("CANDIDATE.*.json"):
        seq = p.name[len("CANDIDATE."):-len(".json")]
        if seq.isascii() and seq.isdecimal():
            numbered.append((int(seq), p))
    found = [out / "CANDIDATE.json"] if (out / "CANDIDATE.json").is_file() else []
    return found + [p for _, p in sorted(numbered)]


def load_candidate(n: int) -> dict:
    """Move the generator's claims into the ledger.

    Without this the ledger stays empty and every downstream leg reviews
    ALWAYS_INCLUDE and nothing else — silently, with no error, which is how a
    full pipeline run can produce a review of the SPEC and read as a review of
    the work. Claims land as ASSERTED; nothing here is evidence of anything.

    Each claim is stamped with the build-order step it was raised under. That
    stamp is what lets a step close on evidence later — a claim naming no step
    can never close one, so a missing objective.json is refused here rather
    than producing claims that silently count towards nothing.
    """
    found = _candidates(cycle_dir(n))
    path = found[-1] if found else None
    if path is None:
        raise ClaimsError(f"no CANDIDATE.json for cycle {n} — the generator "
                          f"has not delivered, or delivered somewhere else")
    objective_path = cycle_dir(n) / "objective.json"
    if not objective_path.is_file():
        raise ClaimsError(
            f"no objective.json for cycle {n} — run `cycle.py start --cycle {n}` "
            f"first, so these claims are bound to the step they answer")
    step = json.loads(objective_path.read_text(encoding="utf-8")).get("step")
    if not isinstance(step, int):
        raise ClaimsError(
            f"cycle {n} was started with no objective assigned, so these claims "
            f"belong to no build-order step and could never close one")
    doc = json.loads(path.read_text(encoding="utf-8"))
    rows = doc.get("claims") if isinstance(doc, dict) else doc
    if not isinstance(rows, list) or not rows:
        raise ClaimsError(f"{path.name} carries no claims list")

    ledger = claims_mod.load(CLAIMS)
    by_id = {c["id"]: c for c in ledger}
    added, skipped = [], []
    for row in rows:
        claim = {k: row.get(k) for k in ("id", "text", "subject_files")}
        claim["raised_cycle"] = row.get("raised_cycle", n)
        claim["objective_step"] = step
        if row.get("how_i_tested"):
            claim["how_i_tested"] = row["how_i_tested"]
        if claim["id"] in by_id:
            # Re-raising an existing id must not silently drop the evidence
            # already attached to it.
            skipped.append(claim["id"])
            continue
        ledger.append(claim)
        added.append(claim["id"])

    claims_mod.validate(ledger)
    claims_mod.save(CLAIMS, ledger)
    record = {"cycle": n, "step": "load", "objective_step": step,
              "candidate_file": path.name,
              "superseded": [p.name for p in found[:-1]],
              "added": len(added), "already_present": skipped}
    _log(record)
    return record | {"claim_ids": added}


def _subject_files_present(root: Path) -> dict:
    """Which of the ledger's subject files exist in the tree about to be tested.

    Cycle 1's machine leg ran in the main tree while the generator worked in a
    worktree, twenty-four minutes before the candidate existed. It returned
    green — about code it had never seen. A green result over a tree missing the
    subject files is not weak evidence, it is evidence for a different claim, so
    the leg refuses rather than recording it.
    """
    rels = sorted({rel for claim in claims_mod.load(CLAIMS)
                   for rel in claim["subject_files"]})
    missing = [rel for rel in rels if not (root / rel).is_file()]
    return {"subject_files": rels, "missing": missing}


def machine_leg(n: int, git_range: str | None, skip_tests: bool) -> dict:
    root = repo_root()
    presence = _subject_files_present(root)
    # An empty ledger has no subject files, so the missing-files check below
    # has nothing to compare and waves the leg through — green, over a tree it
    # was never asked about. That is cycle 1's exact signature, so the guard
    # written for it must not depend on the ledger being populated.
    if not presence["subject_files"]:
        raise ClaimsError(
            "machine leg refused: the ledger is empty, so this run would "
            "report a pass that stands for nothing. Run `cycle.py load "
            f"--cycle {n}` first.")
    if presence["missing"]:
        raise ClaimsError(
            "machine leg refused: this tree is missing subject files the "
            "ledger names — " + ", ".join(presence["missing"][:5])
            + f"\nTree: {root}\nRun the machine leg in the tree the generator "
              "worked in, after it has finished writing.")

    results = [machine_mod.verify_manifest()]
    if not skip_tests:
        results.append(machine_mod.run_tests())
    if git_range:
        results.append(machine_mod.assay_range(git_range))
    written = machine_mod.record(CLAIMS, results)

    # The tree this ran over, recorded alongside the result. A pass is only
    # ever a pass about particular bytes.
    attested = {"tree": str(root),
                "subject_files": presence["subject_files"],
                "subject_digest": claims_mod.digest_files(
                    presence["subject_files"], root)}
    (cycle_dir(n) / "machine.json").write_text(
        json.dumps({"attested_over": attested, "results": results}, indent=2)
        + "\n", encoding="utf-8")
    record = {"cycle": n, "step": "machine", "rows_written": written,
              "tree": str(root), "subject_digest": attested["subject_digest"],
              "passed": all(r["passed"] is not False for r in results)}
    _log(record)
    return record


def make_bundle(n: int, role: str, no_canary: bool) -> dict:
    out = cycle_dir(n) / role
    meta = bundle_mod.build(CLAIMS, n, out, role, list(ALWAYS_INCLUDE),
                            with_canary=not no_canary)
    if role in ("checker", "tiebreak"):
        check_mod.emit(CLAIMS, out / "checker.prompt.txt")
    else:
        # The auditor's contract used to be emitted for nobody, so the operator
        # had to know to open roles/auditor.md and paste it himself. A leg whose
        # instructions arrive only if the operator remembers them is a leg that
        # returns REJECTED_SHAPE the first time he doesn't.
        (out / "auditor.prompt.txt").write_text(
            (HERE / "roles" / "auditor.md").read_text(encoding="utf-8"),
            encoding="utf-8")
    record = {"cycle": n, "step": "bundle", "role": role,
              "parts": len(meta["parts"]),
              "canary": bool(meta.get("canary"))}
    _log(record)
    return record | {"dir": str(out)}


def ingest_reply(n: int, role: str, vendor: str, response: Path,
                 transport: str) -> dict:
    out = cycle_dir(n) / role
    # Before parsing, because parsing writes verdict.<vendor>.json to disk and a
    # refused leg must leave nothing behind that a later reader could mistake
    # for a review that happened.
    ingest_mod.check_transport(transport, role)
    verdict = out / f"verdict.{vendor}.json"
    check_mod.parse(response, verdict)
    outcome = ingest_mod.ingest(verdict, out / "bundle.meta.json", CLAIMS,
                               vendor, role, out / "ingest.log.jsonl",
                               transport=transport)
    _log({"cycle": n, "step": "ingest", "role": role, "vendor": vendor,
          "transport": transport, "result": outcome["result"],
          "recorded": outcome["recorded"]})
    return outcome


def status(n: int, since: str | None) -> str:
    text = state_mod.render(repo_root(), since, CLAIMS)
    (cycle_dir(n) / "STATE.md").write_text(text, encoding="utf-8")
    return text


RULE = "=" * 62

_WINDOW = {"auditor": "AUDITOR window (gemini.google.com)",
           "checker": "CHECKER window (chatgpt.com)",
           "tiebreak": "TIEBREAK window (grok.com)"}
_VENDOR = {"auditor": "gemini-flash-lite", "checker": "chatgpt",
           "tiebreak": "grok"}


def _declare(command: str, rec: dict) -> str:
    """Say, in the terminal, whether this stage finished and what comes next.

    Four windows are open and only one of them is this one. Without a printed
    declaration the operator cannot tell a finished stage from one still
    waiting, so he waits on prose that may never arrive. Every stage ends
    either COMPLETE with the literal next command, or HALTED with the reason —
    no stage ends silently, and no stage ends with a model's opinion that it
    went well.
    """
    n = rec.get("cycle")
    py = "python3.12 -B cycle.py"
    head, lines = f"STAGE COMPLETE — {command} (cycle {n})", []

    if command == "start":
        if rec.get("objective") is None:
            head = f"STOP — {command} (cycle {n})"
            lines = ["No objective. Every build-order step is DONE or blocked",
                     "on you. Do not invent one — see STATE.md."]
        else:
            lines = ["NEXT · GENERATOR window — a new Claude Code session.",
                     f"  Paste: cycles/{n:03d}/{rec['prompt_file']}",
                     "  Add nothing else. Then run `load` here."]
    elif command == "load":
        lines = [f"Read {rec.get('candidate_file')} — {rec.get('added')} claim(s) added."]
        if rec.get("superseded"):
            lines += ["PASSED OVER, not read: " + ", ".join(rec["superseded"]),
                      "  Claims raised only in those files are NOT in the ledger."]
        lines += [f"NEXT · TERMINAL:  {py} machine --cycle {n}"]
    elif command == "machine":
        if rec.get("passed"):
            lines = [f"NEXT · TERMINAL:  {py} bundle --cycle {n} --role auditor"]
        else:
            head = f"STAGE COMPLETE — {command}, suite FAILED (cycle {n})"
            lines = ["Recorded, not refused: claims resting on it cannot rise",
                     "above ASSERTED. Fix, then re-run this stage."]
    elif command == "bundle":
        role = rec.get("role")
        parts = rec.get("parts") or 0
        lines = [f"NEXT · {_WINDOW.get(role, role)} — a NEW chat, paste in order:",
                 f"  1. cycles/{n:03d}/{role}/{role}.prompt.txt   (alone, first)"]
        lines += [f"  {i + 1}. cycles/{n:03d}/{role}/bundle.part{i}.txt"
                  for i in range(1, parts + 1)]
        lines += ["  then ask for the single JSON verdict block.",
                  "  NEVER paste bundle.meta.json — it is the answer key.",
                  f"Save the raw reply to cycles/{n:03d}/{role}/reply.txt, then:",
                  f"  {py} ingest --cycle {n} --role {role} \\",
                  f"    --vendor {_VENDOR.get(role, role)} --transport browser \\",
                  f"    --response cycles/{n:03d}/{role}/reply.txt"]
    elif command == "ingest":
        role, result = rec.get("role"), rec.get("result")
        if result == ingest_mod.ACCEPTED:
            nxt = {"auditor": f"{py} bundle --cycle {n} --role checker"}.get(
                role, f"{py} status --cycle {n}")
            lines = [f"NEXT · TERMINAL:  {nxt}"]
        else:
            head = f"STAGE HALTED — {command} (cycle {n})"
            lines = [f"{result} — the review is discarded whole, nothing recorded.",
                     "Do not keep its findings and do not reformat the reply.",
                     "Re-run the leg in a new chat, or fix the cause first."]
    elif command == "status":
        lines = [f"Read cycles/{n:03d}/STATE.md — FREEZE, provenance, contested.",
                 "A step closes when every claim stamped with it is CONFIRMED."]

    body = "\n".join(f"  {ln}" for ln in lines)
    return f"\n{RULE}\n  {head}\n{RULE}\n{body}\n{RULE}\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cycle", description="Drive one Blacksmith cycle.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start")
    p_start.add_argument("--cycle", required=True, type=int)
    p_start.add_argument("--since", default=None)
    p_start.add_argument("--budget", default="USD 25 / ~150 assistant turns")

    p_load = sub.add_parser("load")
    p_load.add_argument("--cycle", required=True, type=int)

    p_machine = sub.add_parser("machine")
    p_machine.add_argument("--cycle", required=True, type=int)
    p_machine.add_argument("--git-range", default=None)
    p_machine.add_argument("--skip-tests", action="store_true")

    p_bundle = sub.add_parser("bundle")
    p_bundle.add_argument("--cycle", required=True, type=int)
    p_bundle.add_argument("--role", default="auditor",
                          choices=("auditor", "checker", "tiebreak"))
    p_bundle.add_argument("--no-canary", action="store_true")

    p_ingest = sub.add_parser("ingest")
    p_ingest.add_argument("--cycle", required=True, type=int)
    p_ingest.add_argument("--role", required=True,
                          choices=("auditor", "checker", "tiebreak"))
    p_ingest.add_argument("--vendor", required=True)
    p_ingest.add_argument("--transport", required=True,
                          choices=ingest_mod.TRANSPORTS,
                          help="how the bytes reached the reviewer; 'agent' is "
                               "refused for every review role")
    p_ingest.add_argument("--response", required=True)

    p_status = sub.add_parser("status")
    p_status.add_argument("--cycle", required=True, type=int)
    p_status.add_argument("--since", default=None)

    args = parser.parse_args(argv)
    try:
        if args.command == "start":
            rec = start(args.cycle, args.since, args.budget)
        elif args.command == "load":
            rec = load_candidate(args.cycle)
        elif args.command == "machine":
            rec = machine_leg(args.cycle, args.git_range, args.skip_tests)
        elif args.command == "bundle":
            rec = make_bundle(args.cycle, args.role, args.no_canary)
        elif args.command == "ingest":
            rec = ingest_reply(args.cycle, args.role, args.vendor,
                               Path(args.response), args.transport)
        else:
            sys.stdout.write(status(args.cycle, args.since))
            sys.stdout.write(_declare("status", {"cycle": args.cycle}))
            return 0

        print(json.dumps(rec, indent=2))
        sys.stdout.write(_declare(args.command, rec))
        if args.command == "ingest":
            return 0 if rec["result"] == ingest_mod.ACCEPTED else 1
    except (ClaimsError, bundle_mod.BundleError, check_mod.CheckError,
            ingest_mod.TransportError, OSError) as exc:
        print(f"cycle: {exc}", file=sys.stderr)
        # A refusal is the one outcome the operator most needs declared: it
        # wrote nothing, and several of these never reach the rejection log,
        # so the terminal is the only place they exist.
        sys.stdout.write(
            f"\n{RULE}\n  STAGE REFUSED — {args.command} (cycle {args.cycle})\n"
            f"{RULE}\n  {exc}\n"
            "  Nothing was written. Fix the cause and re-run this stage.\n"
            f"{RULE}\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
