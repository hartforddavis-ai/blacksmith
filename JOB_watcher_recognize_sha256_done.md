# Job — teach the watcher a second completion signal

## Context
`watch_bound.py` (repo: `~/Documents/_PROJECTS/SOFTWARE/blacksmith`) and the
SwiftBar plugin layered on it (`~/.swiftbar/plugins/blacksmith_bound.1s.py`,
its own separate git repo) both call `wb.is_done(path, size)` to decide
whether a run has finished. `is_done()` only recognizes one completion
signal: `run_bound.py`'s own footer text, `"\nprompt eval: "`, appended to
the primary `.md` file when a bound run completes.

Not every script that writes into `runs/` is `run_bound.py`. `calib_bind`'s
runner (find the actual script — grep `runs/` for where `calib_bind.*.md.sha256`
gets written, don't assume) writes its own primary `.md` file, but signals
completion with a **sibling `.md.sha256` file** instead — no footer text ever
lands in the primary file for that path.

## The concrete failure this caused (12 Aug 2026, live, twice)
`calib_bind.gemma4-12b-it-qat.20260812T073935.md` finished for real at
07:47. Because `is_done()` never recognized it as done, and because it kept
legitimately being the newest file in `runs/` (real git-commit timestamp
10:16:57, not a display bug — confirmed by rereading `git log` on the file),
the SwiftBar indicator stuck on "loading …" indefinitely, with nothing
actually running (`ollama ps` empty, no `llama-server` process). This
recurred after being manually cleared once already, since clearing it
without fixing the underlying cause is not a fix.

## What's already been ruled out / already done
- The done-state **label** was already fixed on Scott's direct instruction:
  both `sealed`-done and `bound`-done branches in the SwiftBar plugin now
  print a fixed `"Local run done"` instead of trying to parse a job/model
  name (that parsing had its own separate bug — see
  `project_blacksmith.md`'s 12 Aug entries on the "delimited" mislabel,
  a different root cause, already closed).
- That label fix does nothing for *this* gap — `is_done()` still returns
  `False` for this file, so the done branch is never reached at all; it's
  stuck in the loading/thinking/writing branch instead.
- Linking the indicator to the Ollama daemon itself was proposed and
  REJECTED under Law 1 this session (see `project_blacksmith.md`) — not a
  candidate fix for this, out of scope here.

## Task
Read `watch_bound.py`'s `is_done()` (and `has_stalled()` right above it, for
the pattern to follow) before changing anything. Add a second completion
check: if a sibling `<stem>.md.sha256` file exists next to the primary `.md`,
that also counts as done — alongside the existing footer-text check, not
replacing it (both signals are real and come from different producers).
Read whatever script actually writes `calib_bind`'s `.md.sha256` sidecar
first, to confirm it's written only once, after the run is genuinely
finished (the same "only appears on success" property the `sealed` kind
already relies on) — don't assume, verify.

State a Law 1 design verdict before writing code (this is DEMONSTRATED —
named failure, recurred twice live — and should be SIMPLE: one more check
in one function, no new process, no new dependency). Then a Law 2 build
verdict after, with real test output — extend `test_watch_bound.py`
(`HeaderFooterParsingTests`/a new small class) rather than asserting it
works. Verify live against the actual `calib_bind.gemma4-12b-it-qat.
20260812T073935.md` file (or its `_killed_by_hand` copy if it's been moved)
— confirm `is_done()` now returns `True` for it and the SwiftBar plugin's
`render()` shows `"Local run done"` for it, not "loading".

Do not touch the loading/thinking/writing labels' own parsing bug (the
`STAMP_RE` 3-vs-4-segment issue) — that's separate, named, not this job.
