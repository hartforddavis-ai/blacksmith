#!/usr/bin/env python3.12
"""Read-only progress monitor for a run_bound.py run. Never opens the
destination file for writing, never touches Ollama — it only watches the
file run_bound.py is already writing, so it cannot contaminate the run.

Run in a second pane while run_bound.py runs the same job/model:

    python3.12 run_bound.py   verify gemma4:12b
    python3.12 watch_bound.py verify gemma4:12b

Started after the run, add --attach to join the newest run already going.
Without it the watcher waits for a file that will never be created, which
is the state a run has to be restarted to escape.

Answers what run_bound.py's own output can't: during prompt-eval nothing
prints because nothing has arrived yet, and that silence is what got a
working gemma4:12b run killed by hand at 5m49s on 5 Aug (FAILURE_LOG.md).
This turns the silence into a visible elapsed-time heartbeat instead of a
guess.
"""
import itertools
import pathlib
import re
import sys
import time

import build_paste  # shared BS path constant only — no coupling to run_bound's request logic

OUT = pathlib.Path(build_paste.BS) / "runs"
DONE_MARKER = "\nprompt eval: "
THINK_SUFFIX = ".thinking.md"
SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

# The exact shape run_bound.py writes: prefix, timestamp, .md — nothing else.
# Matching what a reply IS beats excluding each sidecar as it appears: the
# reasoning sidecar and run_sealed's .reply.md both share the prefix and both
# lack the end marker, so a watcher pointed at either waits forever for a run
# that already finished. An exclusion list would have to grow with every new
# sidecar and would be wrong for the stretch between adding one and remembering
# this file. A positive match is wrong about nothing it was never shown.
STAMPED_REPLY = re.compile(r"^\d{8}T\d{6}\.md$")


def is_reply(path, prefix):
    return bool(STAMPED_REPLY.match(path.name[len(prefix):]))


def wait_for_new_file(prefix, already):
    while True:
        for p in OUT.glob(f"{prefix}*.md"):
            if p not in already and is_reply(p, prefix):
                return p
        time.sleep(0.5)


def is_done(path, size):
    if size < len(DONE_MARKER):
        return False
    with path.open("rb") as f:
        f.seek(max(0, size - 4096))
        tail = f.read().decode(errors="ignore")
    return DONE_MARKER in tail


def newest_existing(prefix):
    """Newest reply file already on disk, or None."""
    files = [p for p in OUT.glob(f"{prefix}*.md") if is_reply(p, prefix)]
    return max(files, key=lambda p: p.stat().st_mtime) if files else None


def main(job, model, attach=False):
    prefix = f"{job}.{model.replace(':', '-')}."

    if attach:
        path = newest_existing(prefix)
        if path is None:
            raise SystemExit(f"--attach: no {prefix}*.md in {OUT} to attach to")
        print(f"attaching to {path.relative_to(build_paste.BS)} — counts below "
              f"are from this moment, not from the start of the run", flush=True)
    else:
        already = set(OUT.glob(f"{prefix}*.md"))
        print(f"watching for a new {prefix}*.md in {OUT} …", flush=True)
        path = wait_for_new_file(prefix, already)
        print(f"watching {path.relative_to(build_paste.BS)}", flush=True)

    think_path = path.parent / (path.stem + THINK_SUFFIX)
    baseline = path.stat().st_size
    start = time.monotonic()
    writing = False
    spin = itertools.cycle(SPINNER)

    while True:
        time.sleep(1)
        size = path.stat().st_size
        grown = size - baseline
        thought = think_path.stat().st_size if think_path.exists() else 0
        elapsed = time.monotonic() - start
        writing = writing or grown > 0

        if is_done(path, size):
            print(f"\r✓ {elapsed:,.0f}s elapsed · done · {grown:,} reply chars · "
                  f"{thought:,} reasoning chars".ljust(78))
            return

        # WRITING once the reply has started, and it stays WRITING — a pause
        # between reply tokens is not a return to thinking.
        if writing:
            rate = grown / max(elapsed, 1e-9)
            state = f"writing · {grown:,} chars · {rate:,.0f} chars/s"
        elif thought:
            state = f"thinking · {thought:,} chars, no reply yet"
        else:
            state = "waiting · nothing received yet"
        print(f"\r{next(spin)} {elapsed:,.0f}s elapsed · {state}".ljust(78),
              end="", flush=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--attach"]
    if len(args) != 2:
        raise SystemExit("usage: watch_bound.py <job> <model> [--attach]")
    try:
        main(args[0], args[1], attach="--attach" in sys.argv[1:])
    except KeyboardInterrupt:
        print()
