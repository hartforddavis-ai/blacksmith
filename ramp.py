#!/usr/bin/env python3.12
"""Ramp — find each clean model's largest working packet, and its speed there.

    python3.12 ramp.py            # all three models
    python3.12 ramp.py qwen3.5:9b # one model

RAMP ALGORITHM

  Purpose:
  Find, per model, the largest packet that still returns a correct answer,
  and the speed at that size.

  Input:
  Three clean models
  A doubling ladder of packet sizes
  Real source bytes, not filler

  Decision, per model, per size, smallest first:

      Warm the model with a throwaway shot.      Discard its timing.
      Send the packet. Time read; time write.
      Check the reply against the planted answer.

      IF the reply is wrong, or the cap is hit:
          STOP this model. Record the last good size.

      IF correct:
          Record. Double the size. Repeat.

  Output:
  Per model: last good size, and tokens/sec at each size.

WHY EACH GUARD IS HERE

One model at a time. Each is ~7.9 GB against 16 GB of memory; two resident
spills work onto the CPU and every number in the table becomes a measurement
of the spill instead of the model.

A discarded warm-up shot before each timed one. A cold model pulls 7.9 GB off
disk before the first token, and that load lands inside the read time. An
un-warmed first row overstates the read by roughly ten times — measured 6 Aug:
141s cold against 13.5s warm at the same token count.

Correctness, not just a stopwatch. Numbered markers are planted through the
packet and the model is asked to count them. It is checkable without a human,
and it degrades the way comprehension degrades: a model that has stopped
reading the middle of a long packet gets the count wrong while still answering
promptly. Speed on a wrong answer is not a result.

Every row is written the moment it lands. FAILURE_LOG.md records a run killed
by hand at 5m49s; a script that holds its results until the end loses all of
them to the same keystroke.
"""
import itertools
import json
import pathlib
import sys
import threading
import time
import urllib.request

import build_paste

SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

OLLAMA = "http://localhost:11434/api/generate"
MODELS = ("qwen3.5:9b", "gemma4:12b-it-qat", "gemma4:12b")

# Doubling. A doubling ladder finds the knee in five steps where a linear one
# needs thirty, and the knee is the only point being looked for.
#
# It stops at 8,000 because that is near the whole real job (~10,900 tokens)
# and the pool of real source bytes runs out there. A ladder rung the sources
# cannot fill would be measured against a short packet wearing a long label —
# reported as no slowdown at a size never actually sent. `packet` flags a short
# fill rather than letting it pass silently.
SIZES = (500, 1_000, 2_000, 4_000, 8_000)

# NOT a wall clock. A slow answer is still an answer, and a wall clock throws
# away a correct result for being late — which is how a working gemma4 run got
# killed by hand at 5m49s (FAILURE_LOG.md). This is silence between tokens: the
# model has sent nothing at all for this long, which is the only signal that
# distinguishes dead from slow. A run may take as long as it likes provided it
# is still saying something.
STALL_S = 420

# The other way a cell never ends. Silence is not the only failure: a model
# looping in its reasoning keeps emitting tokens, so it never trips the stall
# timeout, and with no wall clock and no stop-on-failure that cell runs until
# someone notices. This bounds the broken case only — it applies while the
# reply is still EMPTY, so a model that has started answering may take as long
# as it likes. The real verify run on 6 Aug sat at 38,000 characters of
# productive reasoning, so the ceiling is set well clear of working behaviour.
THINKING_CEILING = 400_000

# Roughly 4 chars/token for English prose. Only used to cut the packet to
# size; every reported token count comes from the model, not from this.
CHARS_PER_TOKEN = 4

# The SAME number of markers at every rung, spread evenly through whatever
# length the packet is. Planting one every N lines instead would mean 2 markers
# in the small packet and 19 in the large one — the counting task getting harder
# in step with the size, so a failure at the top could be "cannot count to 19"
# and would be recorded as "cannot read 32,000 characters". Fixed count, varying
# size: only one thing changes per rung, which is the whole point of a ladder.
MARKERS = 8
OUT = pathlib.Path(build_paste.BS) / "runs" / "RAMP.md"
FAILURES = pathlib.Path(build_paste.BS) / "runs" / "RAMP_FAILURES.md"


def source_text():
    """Real prose from the job's own sources, plus the kernel and the job itself.

    The same bytes the real run is composed from, so the ladder measures this
    model against this work rather than against generic text.
    """
    spec = build_paste.JOBS["verify"]
    paths = [build_paste.KERNEL, spec["job"]] + [p for _, p in spec["sources"]]
    return "\n\n".join(
        pathlib.Path(p).read_text(encoding="utf-8", errors="replace") for p in paths)


def packet(text, tokens):
    """Cut `text` to ~`tokens`, planting numbered markers as it goes.

    Markers are spread through the whole packet rather than gathered at one
    end, so a model that reads only the opening cannot score by position.

    Returns the packet, the number of markers planted, and whether the sources
    ran out before the budget was met. A short fill is reported, never hidden:
    a rung filled to 60% of its label would be recorded as that model coping
    with a size it was never sent.
    """
    budget = tokens * CHARS_PER_TOKEN

    # Fill to size first, then place the markers into what was filled — so the
    # count is the same at every rung and the spacing stretches with the packet.
    body_lines, used = [], 0
    for line in text.split("\n"):
        if used >= budget:
            break
        body_lines.append(line)
        used += len(line) + 1
    short = used < budget

    every = max(1, len(body_lines) // MARKERS)
    out, planted = [], 0
    for i, line in enumerate(body_lines):
        if i % every == 0 and planted < MARKERS:
            planted += 1
            out.append(f"[[MARKER {planted}]]")
        out.append(line)
    body = "\n".join(out)
    # The instruction must not contain the pattern it asks about. Spelling the
    # marker out here put a ninth match in an 8-marker packet, so a model
    # answering 9 was right and would have been scored wrong — an ambiguous
    # ground truth makes every failure in the table unreadable.
    task = (
        "\n\n---\n\nSome lines above consist only of a tag: two open square "
        "brackets, the word MARKER in capitals, a number, then two close "
        "square brackets.\n\nCount those lines. Reply with one line and "
        "nothing else, in this form, with the number substituted:\n\n"
        "COUNT: 42\n")
    return body + task, planted, short


def heartbeat(state, label):
    """Print one self-rewriting line a second until `state['done']`.

    The watcher, built in. `watch_bound.py` is a second command in a second
    pane, and this tree's own record is that a tool nobody is told to run does
    not get run — a working model was killed by hand during exactly this
    silence. An unattended ladder of fifteen cells cannot rely on someone
    remembering to open a watcher for each one, so the ramp carries its own.
    """
    spin = itertools.cycle(SPINNER)
    start = time.monotonic()
    while not state["done"]:
        elapsed = time.monotonic() - start
        quiet = time.monotonic() - state["last"]
        if state["reply"]:
            what = f"writing · {state['reply']:,} chars"
        elif state["thought"]:
            what = f"thinking · {state['thought']:,} chars"
        else:
            what = "reading the packet · nothing back yet"
        print(f"\r  {next(spin)} {label}  {elapsed:,.0f}s · {what}"
              f"{f' · quiet {quiet:,.0f}s' if quiet > 20 else ''}".ljust(96),
              end="", flush=True)
        time.sleep(1)


def ask(model, prompt, label="", stall=None):
    """One timed call, with a live heartbeat. Returns timings and the reply.

    `stall` is silence between tokens, never total elapsed. Passing None runs
    it unbounded-in-total: a model may take an hour provided it keeps talking.
    """
    stall = STALL_S if stall is None else stall
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({
            "model": model, "prompt": prompt, "stream": True, "think": True,
            "options": {"temperature": 0, "num_ctx": 65536},
        }).encode(),
        headers={"Content-Type": "application/json"},
    )
    start, first, reply, thought, final = time.monotonic(), None, [], 0, {}
    state = {"done": False, "last": start, "thought": 0, "reply": 0}
    beat = None
    if label:
        beat = threading.Thread(target=heartbeat, args=(state, label), daemon=True)
        beat.start()

    def result(outcome):
        state["done"] = True
        if beat:
            beat.join(timeout=2)
            print("\r".ljust(98) + "\r", end="", flush=True)
        return {"outcome": outcome, "elapsed": time.monotonic() - start,
                "first": first, "reply": "".join(reply),
                "thought_chars": thought, "final": final}

    try:
        # The socket timeout IS the stall timeout: urlopen's timeout applies to
        # each read, not to the whole response, so a model that keeps streaming
        # never trips it however long it runs.
        with urllib.request.urlopen(req, timeout=stall) as r:
            for line in r:
                chunk = json.loads(line)
                if first is None:
                    first = time.monotonic() - start
                thought += len(chunk.get("thinking") or "")
                reply.append(chunk.get("response", ""))
                written = sum(len(c) for c in reply)
                state.update(last=time.monotonic(), thought=thought, reply=written)
                if not written and thought > THINKING_CEILING:
                    return result(f"LOOPING — {thought:,} chars of reasoning, "
                                  f"no reply started")
                if chunk.get("done"):
                    final = chunk
    except Exception as exc:
        return result(f"STALLED after {stall}s of silence" if "timed out" in str(exc)
                      else f"ERROR {exc!r}")
    return result("OK")


def scored(reply, planted):
    """Did it get the count right? Last COUNT: line wins — models restate."""
    found = None
    for line in reply.splitlines():
        if "COUNT:" in line:
            digits = "".join(c for c in line.split("COUNT:", 1)[1] if c.isdigit())
            if digits:
                found = int(digits)
    return found, (found == planted)


def append(line):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("a") as f:
        f.write(line + "\n")


def log_failure(model, tokens, planted, got, r, attempt):
    """One entry per failed cell, with what would be needed to diagnose it.

    Its own file, not FAILURE_LOG.md. That file's ENTRY RULE admits a withdrawn
    design or a withdrawn verdict, in a fixed six-field form, and says plainly
    that nothing in it is to be followed. A model miscounting at one rung is a
    measurement, not a withdrawn design; filing it there would bury the entries
    that rule exists to protect. If a ramp result ever kills a design, that
    earns a FAILURE_LOG.md entry in the proper form, and this is its evidence.
    """
    FAILURES.parent.mkdir(parents=True, exist_ok=True)
    first = "never" if r["first"] is None else f"{r['first']:,.1f}s"
    new = not FAILURES.exists()
    with FAILURES.open("a") as f:
        if new:
            f.write("# RAMP — FAILED CELLS\n\nOne entry per cell that did not "
                    "return the right answer. Measurements, not design rulings: "
                    "see FAILURE_LOG.md for those.\n")
        f.write(
            f"\n---\n\n## {model} · {tokens:,} tok · attempt {attempt} · "
            f"{time.strftime('%Y-%m-%dT%H:%M:%S')}\n"
            f"- outcome: {r['outcome']}\n"
            f"- elapsed: {r['elapsed']:,.1f}s, first token {first}\n"
            f"- markers planted: {planted}, model said: {got}\n"
            f"- reasoning: {r['thought_chars']:,} chars, "
            f"reply: {len(r['reply']):,} chars\n"
            f"- reply verbatim:\n\n```\n{r['reply'][:1200] or '(empty)'}\n```\n")


def main(models):
    text = source_text()
    append(f"\n## ramp {time.strftime('%Y-%m-%dT%H:%M:%S')} — no wall clock, "
           f"stall at {STALL_S}s of silence, warm-up discarded, every rung fires\n")
    append("| model | tokens asked | prompt tok | read s | write s | tok/s | "
           "reasoning | markers | got | correct |")
    append("|---|---|---|---|---|---|---|---|---|---|")

    for model in models:
        print(f"\n=== {model} ===", flush=True)

        for tokens in SIZES:
            # Re-warmed before EVERY rung, not once per model. Ollama unloads an
            # idle model after about five minutes, and a rung may run far longer
            # than that — so warming once lets the model go cold partway down the
            # ladder and the next rung silently charges a 7.9 GB disk load to its
            # read time. That is the 141s-vs-13.5s confound, reappearing between
            # rows where it would look like a real slowdown with size.
            ask(model, "Reply with the single word: ready", stall=120)

            prompt, planted, short = packet(text, tokens)
            label = f"{model} {tokens:,} tok"
            print(f"  {tokens:>6,} tok ({len(prompt):>7,} chars"
                  f"{', SHORT — sources ran out' if short else ''})",
                  flush=True)
            r = ask(model, prompt, label=label)
            got, ok = scored(r["reply"], planted)
            if not (r["outcome"] == "OK" and ok):
                log_failure(model, tokens, planted, got, r, attempt=1)

            # One retry, only at a cell that failed. These models are not
            # deterministic even at temperature 0, and this tree has a logged
            # case of a single run being read as confirmation and later found
            # overstated (project_proof, 30 Jul). Two failures at one size is a
            # result; one is a coin toss.
            if not (r["outcome"] == "OK" and ok):
                first_got = got
                r = ask(model, prompt, label=label + " retry")
                got, ok = scored(r["reply"], planted)
                if not (r["outcome"] == "OK" and ok):
                    log_failure(model, tokens, planted, got, r, attempt=2)
                # Recorded either way. A rung that needed two attempts is not
                # the same result as one that passed first time, and a table
                # that hides the retry would read as if it were.
                append(f"| {model} | {tokens:,} retry | — | — | — | — | — | "
                       f"{planted} | {first_got} then {got} | "
                       f"{'passed on retry' if ok else 'failed twice'} |")

            f = r["final"] or {}
            ptok = f.get("prompt_eval_count")
            read_s = (f.get("prompt_eval_duration") or 0) / 1e9 or (r["first"] or 0)
            write_s = (f.get("eval_duration") or 0) / 1e9
            gen = f.get("eval_count") or 0
            rate = gen / write_s if write_s else 0
            append(f"| {model} | {tokens:,}{' (short)' if short else ''} | "
                   f"{ptok or '?'} | {read_s:,.1f} | "
                   f"{write_s:,.1f} | {rate:,.1f} | {r['thought_chars']:,} | "
                   f"{planted} | {got} | {'yes' if ok else 'NO'} |")
            print(f"    read {read_s:,.1f}s · write {write_s:,.1f}s · "
                  f"{rate:,.1f} tok/s · reasoning {r['thought_chars']:,} · "
                  f"markers {got}/{planted} · "
                  f"{'correct' if ok else r['outcome'] if r['outcome'] != 'OK' else 'WRONG'}",
                  flush=True)
            # No stop-on-failure. Every rung fires for every model, so the table
            # is complete and a model that dips at one size but recovers at the
            # next is visible as that, rather than as a ladder that ended early.

    print(f"\nwrote {OUT.relative_to(build_paste.BS)}")
    if FAILURES.exists():
        print(f"failed cells in {FAILURES.relative_to(build_paste.BS)}")


if __name__ == "__main__":
    chosen = tuple(sys.argv[1:]) or MODELS
    bad = [m for m in chosen if m not in MODELS]
    if bad:
        raise SystemExit(f"refusing {bad}: not clean base models. Use {list(MODELS)}")
    main(chosen)
