#!/usr/bin/env python3.12
"""Read-only progress monitor for a run_bound.py run. Never opens the
destination file for writing, never touches Ollama — it only watches the
file run_bound.py is already writing, so it cannot contaminate the run.

Run in a second pane while run_bound.py runs the same job/model:

    python3.12 run_bound.py   verify gemma4:12b
    python3.12 watch_bound.py verify gemma4:12b

Answers what run_bound.py's own output can't: during prompt-eval nothing
prints because nothing has arrived yet, and that silence is what got a
working gemma4:12b run killed by hand at 5m49s on 5 Aug (FAILURE_LOG.md).
This turns the silence into a visible elapsed-time heartbeat instead of a
guess.
"""
import itertools
import pathlib
import sys
import time

import build_paste  # shared BS path constant only — no coupling to run_bound's request logic

OUT = pathlib.Path(build_paste.BS) / "runs"
DONE_MARKER = "\nprompt eval: "
SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"


def wait_for_new_file(prefix, already):
    while True:
        for p in OUT.glob(f"{prefix}*.md"):
            if p not in already:
                return p
        time.sleep(0.5)


def is_done(path, size):
    if size < len(DONE_MARKER):
        return False
    with path.open("rb") as f:
        f.seek(max(0, size - 4096))
        tail = f.read().decode(errors="ignore")
    return DONE_MARKER in tail


def main(job, model):
    prefix = f"{job}.{model.replace(':', '-')}."
    already = set(OUT.glob(f"{prefix}*.md"))
    print(f"watching for a new {prefix}*.md in {OUT} …", flush=True)

    path = wait_for_new_file(prefix, already)
    print(f"watching {path.relative_to(build_paste.BS)}", flush=True)

    baseline = path.stat().st_size
    start = time.monotonic()
    generating = False
    spin = itertools.cycle(SPINNER)

    while True:
        time.sleep(1)
        size = path.stat().st_size
        grown = size - baseline
        elapsed = time.monotonic() - start
        generating = generating or grown > 0

        if is_done(path, size):
            print(f"\r✓ {elapsed:,.0f}s elapsed · done · {grown:,} chars written".ljust(78))
            return

        if not generating:
            line = f"\r{next(spin)} {elapsed:,.0f}s elapsed · prompt-eval · waiting on first byte"
        else:
            rate = grown / max(elapsed, 1e-9)
            line = f"\r{next(spin)} {elapsed:,.0f}s elapsed · generating · {grown:,} chars · {rate:,.0f} chars/s"
        print(line.ljust(78), end="", flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: watch_bound.py <job> <model>")
    try:
        main(sys.argv[1], sys.argv[2])
    except KeyboardInterrupt:
        print()
