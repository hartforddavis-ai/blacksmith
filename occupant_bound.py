"""Bound occupant — Ring 1, run as a direct HTTP call, not a spawned process.

`launch.py` spawns the `claude` CLI as Ring 1's occupant. That CLI writes its
own session state to `$HOME/.claude` and `$HOME/.claude.json` on startup,
which a sealed cell (mode 0o555) refuses, and `CELL_FORBIDDEN_NAMES` flags as
contamination regardless of scratch declaration (ASSUMPTIONS.md #23). This
module is a different occupant for the same Ring 1 slot: a bound call to a
local model over HTTP. No local process is spawned, so there is nothing that
could write `$HOME/.claude` in the first place — #23's cause does not exist
here, so it does not need to be patched here.

CLEAN MODELS ONLY, the same list `run_bound.py` enforces. There is no tool
surface to restrict, because there is no tool surface: the model receives a
prompt string and returns a completion, and nothing it says is executed.

Streamed, per-read timeout — a stall between tokens, not a wall clock. Same
shape as `run_bound.py`, for the same reason: the failure FAILURE_LOG records
against a single-read timeout (dying at prompt-eval, not generation) applies
here too.
"""

from __future__ import annotations

import json
import time
import urllib.request
from dataclasses import dataclass

import store as store_mod

OLLAMA = "http://localhost:11434/api/generate"
CLEAN_MODELS = frozenset({"gemma4:12b", "gemma4:12b-it-qat", "qwen3.5:9b"})


class OccupantError(Exception):
    """The bound call could not be completed, or its output could not be staged."""


@dataclass(frozen=True)
class BoundRun:
    model: str
    prompt: str
    response: str
    first_token_s: float
    final_token_s: float
    exit_code: str


def run(model: str, prompt: str, timeout: float = 1800) -> BoundRun:
    """POST `prompt` to a local, clean model and collect the full response."""
    if model not in CLEAN_MODELS:
        raise OccupantError(
            f"refusing {model!r}: not a clean base model. Use one of {sorted(CLEAN_MODELS)}")
    if not isinstance(prompt, str) or not prompt.strip():
        raise OccupantError("prompt must be a non-empty string")

    req = urllib.request.Request(
        OLLAMA,
        data=json.dumps({
            "model": model, "prompt": prompt, "stream": True,
            "options": {"temperature": 0},
        }).encode(),
        headers={"Content-Type": "application/json"},
    )

    start = time.monotonic()
    first_token = None
    chunks = []
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            for line in r:
                chunk = json.loads(line)
                if first_token is None:
                    first_token = time.monotonic() - start
                chunks.append(chunk.get("response", ""))
                if chunk.get("done"):
                    break
    except OccupantError:
        raise
    except Exception as exc:
        raise OccupantError(f"bound call failed: {exc}") from exc

    if first_token is None:
        raise OccupantError("no tokens received before the connection closed")

    return BoundRun(
        model=model, prompt=prompt, response="".join(chunks),
        first_token_s=first_token, final_token_s=time.monotonic() - start,
        exit_code="0",
    )


def stage_artifact(store: store_mod.ObjectStore, response: str) -> str:
    """Bridge a bound run's raw text into the content-addressed store.

    Returns the object id `gauge`/`promote` expect at `bundle["artifact"]["sha256"]`.
    This is the whole of the output module: encode, then let `store.py` do the
    hashing it already does. No second hashing path is introduced here.
    """
    if not isinstance(response, str):
        raise OccupantError("response must be a string")
    return store.put_bytes(response.encode("utf-8"))
