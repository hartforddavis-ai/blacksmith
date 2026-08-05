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


def secs(ns):
    return "?" if ns is None else f"{ns / 1e9:,.0f}s"


def main(job, model):
    if model not in CLEAN:
        raise SystemExit(f"refusing {model!r}: not a clean base model. Use one of {sorted(CLEAN)}")
    if job not in build_paste.JOBS:
        raise SystemExit(f"unknown job {job!r}: {sorted(build_paste.JOBS)}")

    prompt, _ = compose(job)
    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": {"temperature": 0, "num_ctx": 65536},
        }).encode(),
        headers={"Content-Type": "application/json"},
    )

    OUT.mkdir(exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    dest = OUT / f"{job}.{model.replace(':', '-')}.{stamp}.md"
    print(f"{model}: sending {len(prompt):,} chars, temperature 0 …", flush=True)

    start, first, chars, final = time.monotonic(), None, 0, {}
    with dest.open("w") as out:
        out.write(
            f"# {job} · {model} · {stamp}\n\n"
            f"prompt sha256: {hashlib.sha256(prompt.encode()).hexdigest()[:12]}\n"
            f"prompt chars:  {len(prompt):,}\n"
            f"system prompt: none\n\n---\n\n"
        )
        out.flush()
        # Nothing arrives until prompt-eval ends, so the first line dates it.
        # The timeout is now per read: a stall between tokens, not a wall clock.
        with urllib.request.urlopen(req, timeout=1800) as r:
            for line in r:
                chunk = json.loads(line)
                if first is None:
                    first = time.monotonic() - start
                    print(f"first token at {first:,.0f}s — prompt-eval done", flush=True)
                out.write(chunk.get("response", ""))
                out.flush()
                chars += len(chunk.get("response", ""))
                if chunk.get("done"):
                    final = chunk
        out.write(
            f"\n\n---\n\n"
            f"prompt eval: {final.get('prompt_eval_count')} tok in "
            f"{secs(final.get('prompt_eval_duration'))}\n"
            f"generation:  {final.get('eval_count')} tok in "
            f"{secs(final.get('eval_duration'))}\n"
        )
    print(f"wrote {dest.relative_to(build_paste.BS)}  ({chars:,} chars)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: run_bound.py <job> <model>")
    main(sys.argv[1], sys.argv[2])
