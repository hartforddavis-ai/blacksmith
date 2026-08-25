# TASK — rebuild the Blacksmith bound-run watcher with a real progress bar

Repo: `~/Documents/_PROJECTS/SOFTWARE/blacksmith`

## Read first, before proposing anything

- `watch_bound.py` — the thing you are rebuilding.
- `run_bound.py` and `run_sealed.py` — the two runners that write the files it
  watches. Note that they write DIFFERENT filename shapes.
- `occupant_bound.py` — the Ollama HTTP call. Read what the final streamed JSON
  object actually contains before you rely on any field of it.
- `FAILURE_LOG.md` — READ IT WHOLE, every entry, before you form a verdict.
  The 5 Aug entry is why this tool exists. Other entries may kill your design;
  you cannot search for a dead end you don't yet know you are walking into.

## The problem

During prompt-eval the model has received the prompt and is processing it, but
has emitted nothing. The reply file does not grow. The current watcher prints an
elapsed-seconds heartbeat and a spinner, which proves the watcher is alive but
says nothing about how far through the run is. On 5 Aug a healthy gemma4:12b run
was killed by hand at 5m49s inside exactly that silence.

Scott wants a visual progress bar of local-model run time.

## The constraint you must not paper over

There is no duration history on disk. I checked: `EVIDENCE.jsonl` is 2,256 lines
and contains zero bound-run timing records; `runs/` holds replies and thinking
sidecars with no timing file. So there is no denominator available today.

A bar with an invented denominator — a fake percentage, a fixed-guess ETA, an
animation that fills at a made-up rate — is forbidden. It looks like measurement
and is not. If you cannot ground the fraction in a measured number, render an
indeterminate indicator and say plainly that it is indeterminate.

## The design to implement (change it if you find it wrong — say so first)

1. **Measure, then predict.** When a run completes, Ollama's final streamed JSON
   carries prompt-eval and eval counts and durations. Verify the exact field
   names against `occupant_bound.py` and a real response — do not take my word
   for the names. Append them to a small local baseline file (one row per
   model), owned by this tool.

2. **Bar for prompt-eval.** Prompt token count is knowable before the run from
   the prompt the runner built. With a measured tokens-per-second for that model
   from the baseline file, prompt-eval progress is a real fraction: elapsed vs
   predicted. Render a bar for it.

3. **First run per model is honest about itself.** No baseline row yet means no
   fraction. Show an indeterminate bar labelled as such, and record the timings
   at the end so the next run has a denominator.

4. **Generation phase.** Once tokens arrive the reply file grows and rate is
   directly observable. Show throughput and elapsed. Do not show a percentage
   unless you can name what the total is — output length is not known ahead.

5. **There may be nothing on disk to watch — check this first.** Read how the
   runner writes the reply. If it buffers the whole stream in memory and writes
   the file only once the run has finished, then no file grows during the run
   and every file-growth signal in the watcher is dead, including the sticky
   WRITING state. Verified 12 Aug: `occupant_bound.run()` does exactly this, so
   a run in progress is invisible to any file watcher. Fixing the watcher alone
   does not fix that. Rule whether the runner should flush tokens to disk as
   they stream — and if you change the runner, that is a second build and needs
   its own Law 2 verdict, not a footnote to the watcher's.

6. **Watch both runners.** The current file only matches `run_bound.py`'s
   stamped `.md` shape and will wait forever on a `run_sealed.py` run that has
   already finished. Fix that, and keep the positive-match approach — an
   exclusion list is wrong for every sidecar added after it was written.

## Non-negotiable properties of the existing tool — preserve every one

- **Read-only. Never opens the run's files for writing. Never calls Ollama.**
  It must be impossible for the watcher to contaminate a run. Its own baseline
  file is the only thing it writes, and that file must live outside `runs/`.
- Positive filename matching, not exclusion lists.
- WRITING is sticky: a pause between reply tokens is not a return to thinking.
- `--attach` joins a run already in progress, and says out loud that its counts
  start from the moment of attach, not from the run's start.
- Terminal output only, single line redraw. No new dependencies — standard
  library only. Python 3.12.

## Deliverable

The rebuilt `watch_bound.py`, plus tests in the repo's existing style
(`test_*.py`, standard library). Prove the bar with a fake growing file, not by
description — a test that asserts on rendered output for a known baseline and a
known elapsed time.

## How to report

Before you write code, state your design and rule it against Claude's Law 1
(`~/Documents/_PROJECTS/SOFTWARE/Claudes Laws/claudes-law-1.md`): APPROVE or
REJECT per part, naming the failure each part closes. When the build is done,
rule it against Law 2. The verdict is the deliverable — do not skip it, and do
not certify your own work by assertion. Show the test output.

Do not commit or push.
