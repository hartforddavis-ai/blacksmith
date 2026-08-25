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
depends on it). Generator is a local model (Ollama) or a chat you paste into
by hand; there is no cloud-CLI child process and no API key involved.
`run_sealed.py` / `run_bound.py` are the entry points; `SPEC.md` and
`CONTEXT_next_session.md` are the fuller orientation.

## License

Not yet decided — treat as all-rights-reserved until this section says
otherwise.
