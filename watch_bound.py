#!/usr/bin/env python3.12
"""Read-only progress monitor for a run_bound.py or run_sealed.py run. Never
opens the destination file for writing, never touches Ollama — it only
watches files those two scripts are already writing, so it cannot
contaminate a run. The only thing it writes is its own baseline file,
outside runs/.

Run in a second pane while the runner runs the same job/model:

    python3.12 run_bound.py   verify gemma4:12b
    python3.12 watch_bound.py verify gemma4:12b

Started after the run, add --attach to join the newest run already going.
Without it the watcher waits for a file that will never be created, which
is the state a run has to be restarted to escape.

Answers what run_bound.py's own output can't: during prompt-eval nothing
prints because nothing has arrived yet, and that silence is what got a
working gemma4:12b run killed by hand at 5m49s on 5 Aug (FAILURE_LOG.md).
This turns the silence into a progress bar wherever there is a real
denominator to measure it against, and an honestly-labelled indeterminate
bar everywhere there is not — there is no tokenizer here and no invented
fraction. See watch_bound_baseline.jsonl for the one number this tool
measures and keeps: chars-per-second during prompt-eval, per model, taken
from run_bound.py's own completion footer.

run_sealed.py's occupant (occupant_bound.run()) collects its whole
response in memory and writes the reply file once, after the run is
already finished (verified 12 Aug reading occupant_bound.py) — so a
sealed run in progress has nothing on disk to watch at all. That is a
runner limitation, not a watcher bug, and no change to this file can
close it: fixing it means streaming tokens to disk from
occupant_bound.run(), a second build that needs its own verdict.

Two claims that stood here until 12 Aug and were wrong, corrected after
reading the sources rather than repeating them:

  - This file cited "run_sealed.py's docstring on what streaming means
    for its integrity check". run_sealed.py does not mention streaming
    anywhere. The citation had no source.
  - Streaming does not in fact conflict with that integrity check.
    originals_for() watches KERNEL, the job, and the sources, and
    excludes the reply file by design — so writing the reply
    incrementally touches nothing under watch.

run_bound.py already streams and flushes per chunk, and FAILURE_LOG's
5 Aug entry records that streaming was reverted once by a Law 2 call the
log itself rules wrong in fact, then RESTORED. So the precedent runs the
other way: the streaming runner is the only one that has ever completed a
run. This tool watches for a sealed run's reply file appearing and reports
it landed — it cannot show progress before that.
"""
import json
import pathlib
import re
import sys
import time

import build_paste  # shared BS path constant only — no coupling to run_bound's request logic

OUT = pathlib.Path(build_paste.BS) / "runs"
BASELINE_PATH = pathlib.Path(build_paste.BS) / "watch_bound_baseline.jsonl"
DONE_MARKER = "\nprompt eval: "
STALL_MARKER = "STALLED:"
THINK_SUFFIX = ".thinking.md"
BAR_WIDTH = 24

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

# Printed before the wait, not buried in the docstring. A run_sealed.py run
# has NOTHING on disk until it ends — occupant_bound.run() buffers the whole
# reply and writes once — so this tool legitimately shows no movement for the
# entire run. That silence has now been misread twice: on 5 Aug a healthy
# gemma4:12b run was killed by hand at 5m49s (FAILURE_LOG.md), and on 12 Aug
# the watcher itself was read as not running. Saying so costs one line.
SEALED_BLIND_NOTE = (
    "note: if this is a run_sealed.py run, nothing appears here until it\n"
    "      finishes — the runner buffers the whole reply and writes the file\n"
    "      once, at the end. Silence below is expected, not a stall."
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


def load_baseline(model):
    """Most recent measured prompt-eval chars/s for `model`, or None.

    Scans the whole file rather than seeking from the end: the file is one
    small row per completed bound run, nowhere near EVIDENCE.jsonl's size.
    """
    if not BASELINE_PATH.exists():
        return None
    row = None
    with BASELINE_PATH.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("model") == model and r.get("chars_per_s"):
                row = r
    return row


def record_baseline(model, prompt_chars, prompt_eval_tok, prompt_eval_s):
    """Append one calibration row. The only write this tool ever makes, and
    it lives outside runs/ so it can never be mistaken for run output."""
    if not prompt_chars or prompt_eval_s <= 0:
        return
    row = {
        "model": model,
        "prompt_chars": prompt_chars,
        "prompt_eval_tok": prompt_eval_tok,
        "prompt_eval_s": prompt_eval_s,
        "chars_per_s": prompt_chars / prompt_eval_s,
        "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    with BASELINE_PATH.open("a") as f:
        f.write(json.dumps(row) + "\n")


def render_bar(fraction, width=BAR_WIDTH):
    fraction = max(0.0, min(fraction, 1.0))
    filled = round(fraction * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def indeterminate_bar(tick, width=BAR_WIDTH):
    """A single marker sliding back and forth — visibly alive, claims no fraction."""
    span = max(width - 1, 1)
    pos = tick % (2 * span)
    pos = pos if pos <= span else 2 * span - pos
    cells = ["-"] * width
    cells[pos] = "?"
    return "[" + "".join(cells) + "]"


def predict_prompt_eval_seconds(prompt_chars, baseline):
    if not baseline or not baseline.get("chars_per_s") or prompt_chars is None:
        return None
    cps = baseline["chars_per_s"]
    if cps <= 0:
        return None
    return prompt_chars / cps


def render_prompt_eval(elapsed, predicted, tick, width=BAR_WIDTH):
    if predicted is None:
        return f"{indeterminate_bar(tick, width)} prompt-eval, indeterminate — no baseline yet"
    fraction = elapsed / predicted
    # Capped strictly below 1.0 by at least one cell: a full bar would read
    # as "done," which only the actual completion signal is allowed to say.
    cap = (width - 1) / width
    bar = render_bar(min(fraction, cap), width)
    tail = f"~{predicted:,.0f}s predicted"
    if fraction > 1.0:
        tail += ", past prediction"
    return f"{bar} prompt-eval, {tail}"


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
    """The completion line for a sealed run, carrying no elapsed figure.

    Deliberately quotes no duration: a sealed reply is written once, after the
    run is over, so this watcher's clock measures its own wait and nothing
    else. Its own function so the no-duration property can be asserted.
    """
    return (f"✓ sealed reply landed, {size:,} chars · run duration not "
            f"observable from disk · no token counts for this runner")


def render_generation(grown, elapsed):
    rate = grown / max(elapsed, 1e-9)
    return f"writing · {grown:,} chars · {rate:,.0f} chars/s"


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
        # report an outcome with an elapsed time measured from the attach —
        # which reads as a 2-second run.
        #
        # Tested by observation, not by assuming the runner buffers. Today
        # occupant_bound.run() writes the reply once at the end, so "exists"
        # and "finished" coincide; if that runner is ever changed to stream
        # (see this file's header), a live run would have a growing file here
        # and an existence check alone would call it complete. Watching for
        # growth is right under both runners.
        if kind == "sealed" and path.stat().st_size > 0 and is_stable(path):
            finished = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(path.stat().st_mtime))
            print(f"already complete when attached — finished {finished}, "
                  f"{path.stat().st_size:,} chars. Not watched by this process; "
                  f"no elapsed time is claimed.", flush=True)
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
    start = time.monotonic()
    writing = False
    tick = 0
    last_sealed_size = None

    prompt_chars = None
    predicted = None
    if kind == "bound":
        header = path.read_text(errors="ignore")[:1024]
        prompt_chars = parse_header(header)
        predicted = predict_prompt_eval_seconds(prompt_chars, load_baseline(model))

    while True:
        time.sleep(1)
        tick += 1
        size = path.stat().st_size
        grown = size - baseline_size
        thought = think_path.stat().st_size if think_path.exists() else 0
        elapsed = time.monotonic() - start

        if kind == "bound" and has_stalled(path, size):
            # Checked before WRITING latches: the STALLED note's own bytes
            # make this file grow, and without this check first, that growth
            # reads as a live "writing" state for a run that already exited.
            print(f"\r✗ {elapsed:,.0f}s elapsed · STALLED — run_bound.py's own "
                  f"per-read timeout fired, see the file".ljust(78))
            return

        writing = writing or grown > 0

        if kind == "bound" and is_done(path, size):
            footer = parse_footer(path.read_text(errors="ignore"))
            print(f"\r✓ {elapsed:,.0f}s elapsed · done · {grown:,} reply chars · "
                  f"{thought:,} reasoning chars".ljust(78))
            if footer:
                record_baseline(model, prompt_chars, footer["prompt_eval_tok"],
                                 footer["prompt_eval_s"])
            return

        if kind == "sealed":
            if last_sealed_size == size and size > 0:
                # No elapsed figure here on purpose. `start` is set when the
                # file was first seen, and a sealed file is only written once
                # the run is already over — so elapsed measures this watcher's
                # wait, not the run, and printing it as "elapsed" reads as a
                # two-second run.
                print("\r" + render_sealed_done(size).ljust(78))
                return
            last_sealed_size = size

        # WRITING once the reply has started, and it stays WRITING — a pause
        # between reply tokens is not a return to thinking.
        if writing:
            line = render_generation(grown, elapsed)
        elif thought:
            line = f"{indeterminate_bar(tick)} thinking · {thought:,} chars, no reply yet"
        elif kind == "bound":
            line = render_prompt_eval(elapsed, predicted, tick)
        else:
            line = f"{indeterminate_bar(tick)} sealed run — nothing observable until it finishes"
        print(f"\r{elapsed:,.0f}s elapsed · {line}".ljust(78), end="", flush=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--attach"]
    if len(args) != 2:
        raise SystemExit("usage: watch_bound.py <job> <model> [--attach]")
    try:
        main(args[0], args[1], attach="--attach" in sys.argv[1:])
    except KeyboardInterrupt:
        print()
