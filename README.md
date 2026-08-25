# Blacksmith

A build system for working with a generator (an AI model or agent) in a loop,
designed so the loop can't drift off the task, can't invent facts, and can't
carry state it wasn't given — governed by the
[PRIME AI Operating Laws](https://github.com/hartforddavis-ai/prime-ai-operating-laws).

## Why this exists

Narrow-AI generators in a build loop fail in three specific ways: they drift
from the frozen task, they confabulate specifics the input never gave them,
and they add more than the task required. Blacksmith's answer isn't a prompt
telling the generator to behave — a boundary enforced from inside the thing
being bounded doesn't hold. It's a small, deterministic, non-LLM core (Ring
0: `cell`, `attest`, `launch`, `gauge`, `promote`, `log`) that builds a
sterile environment *before* the generator runs, and re-derives every verdict
on the far side rather than trusting one the generator reports about itself.

## How it's structured

- **Ring 0 — the trusted core.** Deterministic, no LLM, no network. Builds
  the sterile working tree, hashes it before and after, and is the only
  thing that can promote output into kept state.
- **Ring 1 — the cell.** The generator runs here, contained: own `HOME`, no
  memory files, no skills, no hooks. Untrusted by design.
- **Ring 2 — output.** Transcript, artifacts, patches. Untrusted until Ring
  0 promotes it.

Independence is the OS process, filesystem, and UID boundary — not a prompt,
not a signature, not a flag the generator could be talked past. See `SPEC.md`
for the full architecture and the reasoning behind each rule.

## Status

Research build, actively developed, not a packaged product. `calib/LEDGER.md`
records every calibration run against it. `FAILURE_LOG.md` records what was
tried and didn't work, kept so it isn't retried. Read both before assuming
a design choice here is arbitrary — most of them are the losing side of a
real attempt.

## Running it

Local only, by design (see "Why this exists" above — the sterility guarantee
depends on it). No pip install, no third-party packages — Python 3.12 stdlib
only. The one external dependency is [Ollama](https://ollama.com), running
locally with a model pulled.

```bash
# 1. Install Ollama and pull one of the three models this repo trusts
ollama pull gemma4:12b        # or gemma4:12b-it-qat, or qwen3.5:9b

# 2. Run a job against it — writes the reply + a stamped record to runs/
python3.12 run_bound.py verify gemma4:12b

# 3. (optional) watch it in another pane while it reasons — it goes
#    silent for minutes between the request and the first token
python3.12 watch_bound.py verify gemma4:12b
```

Valid job names: `calib_bind`, `calib_false`, `calib_govern`, `calib_govern2`,
`calib_govern2_b`, `calib_govern_b`, `calib_reason`, `calib_true`, `evaluate`,
`verify` (defined in `build_paste.py`'s `JOBS`). An unrecognised job or model
name refuses immediately rather than running — `run_bound.py` will list the
valid set back at you.

`run_sealed.py` takes the same two arguments and does the same call, plus a
source-file integrity measurement around it (see its own docstring for what
that does and doesn't prove — it's narrower than the name suggests).

There's a second, non-scripted generator path — a bounded Claude chat, prompt
built by `build_paste.py` and pasted in by hand — for when the job calls for
a model this repo doesn't have local weights for. No single command for that
one; `SPEC.md` and `CONTEXT_next_session.md` are the fuller orientation on
both paths and the reasoning behind each design choice.

## License

Not yet decided — treat as all-rights-reserved until this section says
otherwise.
