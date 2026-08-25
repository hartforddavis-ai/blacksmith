#!/usr/bin/env python3.12
"""Run a bound prompt against a clean local model. No tools reach the model.

Composes KERNEL + JOB + byte-exact sources, POSTs to Ollama with no system
prompt, writes the reply and a stamped record beside it.

Streamed, and the file opens before the request: a run that never finishes
still leaves what it got, and the first token marks where prompt-eval ended.

    python3.12 run_bound.py verify gemma4:12b
"""
import datetime
import hashlib
import json
import pathlib
import signal
import sys
import time
import urllib.request

import build_paste  # reuse the same composition, so what runs is what is stamped

OLLAMA = "http://localhost:11434/api/generate"
CLEAN = {"gemma4:12b", "gemma4:12b-it-qat", "qwen3.5:9b"}
OUT = pathlib.Path(build_paste.BS) / "runs"


def compose(job):
    """Same bytes build_paste writes, without touching the paste file."""
    spec = build_paste.JOBS[job]
    build_paste.build(job)
    return spec["out"].read_text(), spec


VARIANTS = build_paste.VARIANTS  # single source of what a variant means — build_paste.compose_variant


def secs(ns):
    return "?" if ns is None else f"{ns / 1e9:,.0f}s"


def unload(model):
    """Tell Ollama to drop this model's slot right now.

    13 Aug 2026: the actual cause of a session of slow/stuck runs was an
    orphaned llama-server subprocess from an earlier killed run_bound.py,
    still holding Ollama's one generation slot hours later — killing the
    client does not cancel the request server-side (dossier, 12 Aug).
    Ollama's own keep_alive default (5m) is exactly this gap: a client
    that dies without reading its response leaves the model loaded until
    that timer runs out on its own. Setting keep_alive:0 on a follow-up
    call unloads immediately instead of waiting on the timer — best
    effort, since a request already stuck mid-generation may not have a
    slot free to accept this one either, but every clean exit closes it.
    """
    try:
        req = urllib.request.Request(
            OLLAMA,
            data=json.dumps({"model": model, "keep_alive": 0}).encode(),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10).read()
    except OSError:
        pass


def _raise_on_term(signum, frame):
    # A plain `kill <pid>` sends SIGTERM, and Python's default disposition
    # for it is immediate termination with no exception raised — the
    # try/finally below never runs, unload() never fires. That's not a
    # theoretical gap: "killed by hand" is the literal, repeated failure
    # mode in the dossier (5 Aug, 12 Aug), and a plain kill is how it's
    # actually done. Turning SIGTERM into SystemExit is what makes
    # `finally: unload(model)` reachable for that case at all — SIGKILL
    # (kill -9) still can't be caught by anything, Python or otherwise.
    raise SystemExit(f"terminated by signal {signum}")


def main(job, model, variant="flat"):
    signal.signal(signal.SIGTERM, _raise_on_term)
    if model not in CLEAN:
        raise SystemExit(f"refusing {model!r}: not a clean base model. Use one of {sorted(CLEAN)}")
    if job not in build_paste.JOBS:
        raise SystemExit(f"unknown job {job!r}: {sorted(build_paste.JOBS)}")
    if variant not in VARIANTS:
        raise SystemExit(f"unknown variant {variant!r}: {sorted(VARIANTS)}")

    if variant == "flat":
        prompt, _ = compose(job)
        system = None
    else:
        prompt, system = build_paste.compose_variant(job, variant)
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        # These models reason before replying whether asked or not (59 tokens
        # to emit "OK"). Unasked, that stream is discarded and a working run
        # writes nothing — which is what got gemma4 killed by hand three times.
        "think": True,
        "options": {"temperature": 0, "num_ctx": 65536},
    }
    if system is not None:
        payload["system"] = system
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )

    OUT.mkdir(exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    tag = model.replace(":", "-") if variant == "flat" else f"{model.replace(':', '-')}.{variant}"
    dest = OUT / f"{job}.{tag}.{stamp}.md"
    print(f"{model} [{variant}]: sending {len(prompt):,} chars prompt"
          f"{f' + {len(system):,} chars system' if system else ''}, temperature 0 …",
          flush=True)
    # This goes quiet for minutes while the model reasons. Say so here, with the
    # command — the watcher existing was not enough to stop a working run being
    # killed by hand on 5 Aug (FAILURE_LOG.md).
    print(f"this stays silent while the model reasons. To watch it, in another pane:\n"
          f"    python3.12 watch_bound.py {job} {model}", flush=True)

    # Reasoning goes to its own file, never into the reply. The reply is what
    # gets adjudicated and what quotes.py scans; mixing the two would hand a
    # checker the model's self-persuasion as if it were the answer.
    think_path = dest.parent / (dest.stem + ".thinking.md")
    think_out = None

    # Bare reply, no stamp header — same naming convention run_sealed.py uses,
    # so quotes.py can be pointed at either pipeline's output without a manual
    # extraction step first.
    reply_path = dest.parent / (dest.stem + ".reply.md")
    reply_out = reply_path.open("w")

    start, first, chars, thought_chars, final = time.monotonic(), None, 0, 0, {}
    # Whatever happens inside — clean finish, STALLED, or an uncaught error —
    # the model's slot is freed on the way out. See unload()'s docstring.
    try:
        with dest.open("w") as out:
            out.write(
                f"# {job} · {model} · {stamp}\n\n"
                f"variant:       {variant}\n"
                f"prompt sha256: {hashlib.sha256(prompt.encode()).hexdigest()[:12]}\n"
                f"prompt chars:  {len(prompt):,}\n"
                f"system prompt: {'none' if system is None else f'{len(system):,} chars, sha256:{hashlib.sha256(system.encode()).hexdigest()[:12]}'}\n\n---\n\n"
            )
            out.flush()
            # Nothing arrives until prompt-eval ends, so the first line dates it.
            # The timeout is now per read: a stall between tokens, not a wall clock.
            try:
                with urllib.request.urlopen(req, timeout=1800) as r:
                    for line in r:
                        chunk = json.loads(line)
                        if first is None:
                            first = time.monotonic() - start
                            print(f"first token at {first:,.0f}s — prompt-eval done", flush=True)
                        thought = chunk.get("thinking") or ""
                        if thought:
                            if think_out is None:
                                think_out = think_path.open("w")
                                think_out.write(
                                    f"# {job} · {model} · {stamp} — model reasoning\n\n"
                                    "NOT the reply. Recorded so a silent run is visibly\n"
                                    "working, and so a bad reply can be diagnosed.\n\n---\n\n")
                            think_out.write(thought)
                            think_out.flush()
                            thought_chars += len(thought)
                        response = chunk.get("response", "")
                        out.write(response)
                        out.flush()
                        reply_out.write(response)
                        reply_out.flush()
                        chars += len(response)
                        if chunk.get("done"):
                            final = chunk
            except OSError as e:
                elapsed = time.monotonic() - start
                if think_out is not None:
                    think_out.close()
                reply_out.close()
                out.write(
                    f"\n\n---\n\n"
                    f"STALLED: read failed after {elapsed:,.0f}s "
                    f"(first token: {'never' if first is None else f'{first:,.0f}s'}, "
                    f"{chars:,} reply chars, {thought_chars:,} reasoning chars)\n"
                    f"error: {e!r}\n"
                )
                print(f"STALLED after {elapsed:,.0f}s — wrote partial + verdict to "
                      f"{dest.relative_to(build_paste.BS)}")
                return
            out.write(
                f"\n\n---\n\n"
                f"prompt eval: {final.get('prompt_eval_count')} tok in "
                f"{secs(final.get('prompt_eval_duration'))}\n"
                f"generation:  {final.get('eval_count')} tok in "
                f"{secs(final.get('eval_duration'))}\n"
                f"reasoning:   {thought_chars:,} chars (separate file)\n"
            )
        if think_out is not None:
            think_out.close()
        reply_out.close()
        print(f"wrote {dest.relative_to(build_paste.BS)}  "
              f"({chars:,} reply chars, {thought_chars:,} reasoning chars)  "
              f"reply: {reply_path.name}")
    finally:
        unload(model)


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        raise SystemExit(f"usage: run_bound.py <job> <model> [variant]  variants: {sorted(VARIANTS)}")
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else "flat")
