#!/usr/bin/env python3.12
"""Read-only progress monitor for a run_bound.py or run_sealed.py run. Never
opens the destination file for writing, never touches Ollama — it only
watches files those two scripts are already writing, so it cannot
contaminate a run. Writes nothing of its own.

Run in a second pane while the runner runs the same job/model:

    python3.12 run_bound.py   verify gemma4:12b
    python3.12 watch_bound.py verify gemma4:12b

Started after the run, add --attach to join the newest run already going.
Without it the watcher waits for a file that will never be created, which
is the state a run has to be restarted to escape.

Answers what run_bound.py's own output can't: during prompt-eval nothing
prints because nothing has arrived yet, and that silence is what got a
working gemma4:12b run killed by hand at 5m49s on 5 Aug (FAILURE_LOG.md).

13 Aug 2026 rebuild, on Scott's word: an earlier version of this file
computed elapsed time and a chars/s rate per phase. Reproduced live, that
rate was wrong the first time it was tried against a real run — it divided
by time elapsed since the watcher attached, not since the phase it was
describing actually started, silently folding a 44-second prompt-eval wait
into a "thinking" rate. Fixing the clock was the wrong fix. Scott's
correction: "clock is not a solution, state change is the trigger." This
version computes nothing from time.monotonic() and shows no rate, no
percentage, no predicted seconds, no bar. It prints one line each time the
files it watches actually change — a delta and a running total — and
nothing when they don't. Silence between lines is honest: it means nothing
has been observed, not that nothing is happening.

run_sealed.py's occupant (occupant_bound.run()) used to collect its whole
response in memory and write the reply file once, after the run was
already finished (verified 12 Aug reading occupant_bound.py) — so a
sealed run in progress had nothing on disk to watch. occupant_bound.run()
now streams each chunk to reply_path/think_path as it arrives (TODO !92's
runner half), and run_sealed.py passes those paths, so a sealed run's
reply file grows in real time the same as a bound run's. This file's
"sealed" handling already watches for that growth (see the main loop's
`kind == "sealed"` branch) rather than assuming a single write at the end.

run_bound.py already streams and flushes per chunk, and FAILURE_LOG's
5 Aug entry records that streaming was reverted once by a Law 2 call the
log itself rules wrong in fact, then RESTORED. So the precedent runs the
other way: the streaming runner is the only one that has ever completed a
run. This tool watches for a sealed run's reply file appearing and reports
it landed — it cannot show progress before that.
"""
import pathlib
import re
import sys
import time

import build_paste  # shared BS path constant only — no coupling to run_bound's request logic

OUT = pathlib.Path(build_paste.BS) / "runs"
DONE_MARKER = "\nprompt eval: "
STALL_MARKER = "STALLED:"
THINK_SUFFIX = ".thinking.md"

# The two shapes the runners actually write. run_bound.py's primary file is
# the bare stamped .md (header at open, footer at completion). run_sealed.py
# writes only a stamped .reply.md, never a bare .md — but run_bound.py ALSO
# writes a .reply.md sidecar alongside its primary file, so a bare .md
# sibling existing is what tells the two apart. Positive shape match plus
# one sibling check, not an exclusion list: nothing new added after this was
# written can be mistaken for either shape by accident.
STAMP = r"\d{8}T\d{6}"
BOUND_PRIMARY = re.compile(rf"^{STAMP}\.md$")
SEALED_REPLY = re.compile(rf"^{STAMP}\.reply\.md$")

# Printed before the wait, not buried in the docstring. occupant_bound.run()
# now streams to reply_path/think_path as tokens arrive, so a run_sealed.py
# run's reply file grows the same way a run_bound.py run's does — but there
# is still a real blind window before the first token, during prompt-eval,
# where nothing is on disk yet. That silence has been misread twice before:
# on 5 Aug a healthy gemma4:12b run was killed by hand at 5m49s
# (FAILURE_LOG.md), and on 12 Aug the watcher itself was read as not
# running. Saying so costs one line.
SEALED_BLIND_NOTE = (
    "note: if this is a run_sealed.py run, nothing appears here until the\n"
    "      first token arrives — prompt-eval is silent on disk for both\n"
    "      runners. Once generation starts, the reply file grows in real\n"
    "      time. Silence below is expected during prompt-eval, not a stall."
)

PROMPT_CHARS_RE = re.compile(r"prompt chars:\s*([\d,]+)")
FOOTER_RE = re.compile(
    r"prompt eval: ([\d,]+) tok in ([\d,]+)s\s*"
    r"generation:\s*([\d,]+) tok in ([\d,]+)s"
)


def _int(s):
    return int(s.replace(",", ""))


def classify(path, prefix):
    """"bound", "sealed", or None — never a set to exclude, only shapes to admit."""
    tail = path.name[len(prefix):]
    if BOUND_PRIMARY.match(tail):
        return "bound"
    m = SEALED_REPLY.match(tail)
    if m:
        stamp = tail[: -len(".reply.md")]
        sibling = path.parent / f"{prefix}{stamp}.md"
        if not sibling.exists():
            return "sealed"
    return None


def wait_for_new_file(prefix, already):
    while True:
        for p in OUT.glob(f"{prefix}*.md"):
            if p not in already:
                kind = classify(p, prefix)
                if kind:
                    return p, kind
        time.sleep(0.5)


def newest_existing(prefix):
    """Newest reply file already on disk, or None."""
    candidates = []
    for p in OUT.glob(f"{prefix}*.md"):
        kind = classify(p, prefix)
        if kind:
            candidates.append((p, kind))
    return max(candidates, key=lambda pk: pk[0].stat().st_mtime) if candidates else None


def _tail(path, size, window=4096):
    with path.open("rb") as f:
        f.seek(max(0, size - window))
        return f.read().decode(errors="ignore")


def _seal_path(path):
    return path.parent / (path.name + ".sha256")


def is_done(path, size):
    """True on either completion signal a primary .md file can carry:
    run_bound.py's own footer text, or a sibling `<name>.md.sha256` seal —
    evidence_log.write() (run_sealed.py's path, e.g. calib_bind) writes that
    seal only once, after the entry is fully rendered, so its mere presence
    is as reliable a completion signal as the footer text is for its own
    producer. Neither replaces the other: they come from different writers
    and a file only ever carries the one its own producer writes."""
    if _seal_path(path).exists():
        return True
    if size < len(DONE_MARKER):
        return False
    return DONE_MARKER in _tail(path, size)


def has_stalled(path, size):
    """run_bound.py's own failure marker: on a per-read timeout it appends
    "STALLED: ..." to this same file and returns WITHOUT ever writing the
    completion footer — so is_done() alone never fires, and the STALLED
    text's own bytes make the file grow, which without this check reads as
    a live "writing" state for a process that has already exited."""
    if size < len(STALL_MARKER):
        return False
    return STALL_MARKER in _tail(path, size)


def parse_header(text):
    m = PROMPT_CHARS_RE.search(text)
    return _int(m.group(1)) if m else None


def parse_footer(text):
    m = FOOTER_RE.search(text)
    if not m:
        return None
    return {
        "prompt_eval_tok": _int(m.group(1)),
        "prompt_eval_s": _int(m.group(2)),
        "eval_tok": _int(m.group(3)),
        "eval_s": _int(m.group(4)),
    }


def think_path_for(path):
    """The reasoning sidecar beside a run, under either runner's naming.

    run_bound.py writes `<stamp>.thinking.md` beside its bare `<stamp>.md`;
    run_sealed.py writes the same name beside `<stamp>.reply.md`, stripping
    `.reply` first. Taking `path.stem` alone gets bound right and sealed
    wrong — it looks for `<stamp>.reply.thinking.md`, which nothing writes,
    so a sealed run's reasoning file has never been found by this tool.
    """
    return path.parent / (path.stem.removesuffix(".reply") + THINK_SUFFIX)


def is_stable(path, interval=1.0):
    """True if the file has not grown across one interval.

    Read-only, and the only question that distinguishes a finished run from a
    live one without assuming which runner wrote it. Kept separate from the
    main loop so the attach path and a future streaming runner ask it the
    same way.
    """
    before = path.stat().st_size
    time.sleep(interval)
    return path.stat().st_size == before


def render_sealed_done(size):
    """The completion line for a sealed run, carrying no duration figure.

    A sealed reply is written once, after the run is over, so nothing this
    watcher observed brackets the run's actual start. Its own function so
    the no-duration property can be asserted.
    """
    return (f"✓ sealed reply landed, {size:,} chars · run duration not "
            f"observable from disk · no token counts for this runner")


def render_delta(label, delta, total):
    """One event line: what changed, and the running total. No rate, no
    percentage, no time figure of any kind — Scott's correction, 13 Aug:
    the state change is the signal, not a number derived from a clock."""
    return f"{label} · +{delta:,} chars · {total:,} total"


def render_done(grown, thought, footer):
    line = f"✓ done · {grown:,} reply chars · {thought:,} reasoning chars"
    if footer:
        # Ollama's own reported counts, not this watcher's clock — the model
        # measured its own prompt-eval and generation time; quoting that
        # back is not the rejected mechanism.
        line += (f" · Ollama reports prompt-eval {footer['prompt_eval_tok']:,} tok "
                 f"in {footer['prompt_eval_s']}s, generation {footer['eval_tok']:,} tok "
                 f"in {footer['eval_s']}s")
    return line


def main(job, model, attach=False):
    prefix = f"{job}.{model.replace(':', '-')}."

    if attach:
        found = newest_existing(prefix)
        if found is None:
            raise SystemExit(f"--attach: no {prefix}*.md in {OUT} to attach to")
        path, kind = found
        print(f"attaching to {path.relative_to(build_paste.BS)} [{kind}]", flush=True)
        # A sealed file that was already finished when this watcher arrived
        # belongs to a run it never observed, and saying "done" about it would
        # claim to have watched a run that finished before this process
        # existed.
        #
        # Tested by observation, not by assuming either runner buffers.
        # occupant_bound.run() now streams to reply_path (see this file's
        # header), so a live sealed run has a growing file here just like a
        # bound run — an existence check alone would wrongly call it
        # complete. Watching for growth is right under both runners.
        if kind == "sealed" and path.stat().st_size > 0 and is_stable(path):
            finished = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(path.stat().st_mtime))
            print(f"already complete when attached — finished {finished}, "
                  f"{path.stat().st_size:,} chars. Not watched by this process.",
                  flush=True)
            return
        print("counts below are from this moment, not from the start of the run",
              flush=True)
    else:
        already = set(OUT.glob(f"{prefix}*.md"))
        print(f"watching for a new {prefix}*.md in {OUT} …", flush=True)
        print(SEALED_BLIND_NOTE, flush=True)
        path, kind = wait_for_new_file(prefix, already)
        print(f"watching {path.relative_to(build_paste.BS)} [{kind}]", flush=True)

    think_path = think_path_for(path)
    baseline_size = path.stat().st_size
    last_grown = 0
    last_thought = 0
    writing = False
    last_sealed_size = None

    if kind == "bound":
        header = path.read_text(errors="ignore")[:1024]
        prompt_chars = parse_header(header)
        print("waiting for first token"
              + (f" ({prompt_chars:,} prompt chars sent)" if prompt_chars else "")
              + " — nothing is observable here; Ollama has the prompt and "
                "emits nothing until prompt-eval ends", flush=True)

    while True:
        time.sleep(1)
        size = path.stat().st_size
        grown = size - baseline_size
        thought = think_path.stat().st_size if think_path.exists() else 0

        if kind == "bound" and has_stalled(path, size):
            # Checked before WRITING latches: the STALLED note's own bytes
            # make this file grow, and without this check first, that growth
            # reads as a live "writing" state for a process that already exited.
            print("✗ STALLED — run_bound.py's own per-read timeout fired, "
                  "see the file", flush=True)
            return

        if kind == "bound" and is_done(path, size):
            footer = parse_footer(path.read_text(errors="ignore"))
            print(render_done(grown, thought, footer), flush=True)
            return

        if kind == "sealed":
            if last_sealed_size == size and size > 0:
                print(render_sealed_done(size), flush=True)
                return
            last_sealed_size = size

        # WRITING once the reply has started, and it stays WRITING — a pause
        # between reply tokens is not a return to thinking. Only one event
        # per poll: growth in the reply takes priority over a thinking
        # sidecar that (per the model's own behaviour) should have stopped
        # growing once the reply started.
        if grown > last_grown:
            writing = True
            print(render_delta("writing", grown - last_grown, grown), flush=True)
            last_grown = grown
        elif thought > last_thought and not writing:
            print(render_delta("thinking", thought - last_thought, thought), flush=True)
            last_thought = thought
        # else: nothing changed this poll. Silence, not a redraw — a state
        # change is the only thing that earns a line.


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--attach"]
    if len(args) != 2:
        raise SystemExit("usage: watch_bound.py <job> <model> [--attach]")
    try:
        main(args[0], args[1], attach="--attach" in sys.argv[1:])
    except KeyboardInterrupt:
        print()
