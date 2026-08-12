#!/usr/bin/env python3.12
"""Phase 1 — find the binding. Local, no pipeline, disposable.

Two arms, identical in every respect but the Law representation:
    calib_govern    A — semantic (the current production form)
    calib_govern_b  B — algorithmic (PRIME's frozen Candidate B)

Placement held at flat for both — the current production shape, and the one
PRIME's Stage 2 failed from. One variable.

Reuses build_paste.compose_variant and occupant_bound.run so what runs here
is what the pipeline would run in phase 2. No attest, no evidence_log: these
are exploratory runs and must not enter the evidence set.
"""
import pathlib
import sys
import time

BS = pathlib.Path.home() / "Documents/_PROJECTS/SOFTWARE/blacksmith"
sys.path.insert(0, str(BS))

import build_paste          # noqa: E402
import occupant_bound       # noqa: E402

MODEL = "gemma4:12b-it-qat"
OUT = pathlib.Path(__file__).parent / "phase1"
ARMS = [("A_semantic", "calib_govern"), ("B_algorithmic", "calib_govern_b")]


def main():
    OUT.mkdir(exist_ok=True)
    for label, job in ARMS:
        prompt, system = build_paste.compose_variant(job, "flat")
        print(f"\n=== {label} ({job}) — {len(prompt):,} chars ===", flush=True)
        start = time.monotonic()
        try:
            run = occupant_bound.run(MODEL, prompt, system=system)
        except occupant_bound.OccupantError as exc:
            print(f"{label}: FAILED — {exc}", flush=True)
            (OUT / f"{label}.error.txt").write_text(str(exc))
            continue
        (OUT / f"{label}.reply.md").write_text(run.response, encoding="utf-8")
        if run.thinking:
            (OUT / f"{label}.thinking.md").write_text(run.thinking, encoding="utf-8")
        print(f"{label}: first {run.first_token_s:,.0f}s  total "
              f"{time.monotonic() - start:,.0f}s  "
              f"{len(run.response):,} reply chars  "
              f"{len(run.thinking):,} reasoning chars  "
              f"done_reason={run.done_reason!r}", flush=True)
    print("\nphase 1 runs complete", flush=True)


if __name__ == "__main__":
    main()
