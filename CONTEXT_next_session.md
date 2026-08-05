# BOUND CONTEXT — NEXT SESSION

Paste as the first message. Nothing else carries over.

## VENUE

You hold tools. That is intended. You are the **operator**, not the bound
model. The bound model is local, reached only through `run_bound.py`, and it
holds nothing.

Read before acting — do not work from this file's summary of them:

```
~/Documents/_PROJECTS/SOFTWARE/Claudes Laws/        all three
~/Documents/_PROJECTS/SOFTWARE/blacksmith/FAILURE_LOG.md
```

---

## STATE — 5 Aug 2026

```
INSTRUMENT
  KERNEL_bound.md          the fixed instrument. Digest-stamped. Inviolate.
  JOB_verify_ruling.md     the task: check the ruling's rows against sources.
  build_paste.py           composes both + 6 sources → PROMPT_VERIFY_PASTE.md,
                           41,236 bytes, three independent stamps. RUNS.
  Neither has produced output from any model. Not once.

RUNNER
  run_bound.py             Law 2 BUILT: PASS. Streamed; timeout is per read,
                           so it means "stalled", not "wall clock". A single
                           read at 1800s cannot finish a run on this hardware
                           — see FAILURE_LOG, 5 Aug, the reverted-streaming
                           entry, before you touch this.

RUNS
  gemma4:12b   run 1  1800s single-read timeout, no reply, nothing written.
                      NOT evidence the model is too slow — the timeout was
                      shorter than the work. Worth re-running.
  gemma4:12b   run 2  stopped by hand at 5m49s, 0 tokens, still in prompt-eval
  qwen3.5:9b   run 1  COMPLETE. runs/verify.qwen3.5-9b.20260805T103016.md
                      first token 119s · total ~39 min · 8,936 chars.
                      Produced under KERNEL 73a44a07e235, the pre-T1/T2
                      instrument. Nobody has read it. That is your job.

UNDER RULING
  BLACKSMITH_REDESIGN.md   34 design rows, 15 removals. Produced by an
                           UNBOUND session. Four rows hand-checked; 30 are
                           unverified. This is what the verify job exists for.

CLOSED 5 Aug, after the qwen run was sent — Temper findings, applied.
  T1  The kernel said "no tools" and then voided only tools BEYOND
      Read/Grep/Glob. A model holding Read could read the real files instead
      of the pasted ones, defeating the stamps. Now: VOID on ANY tool.
      Law 1 APPROVE — the venue failure it covers has already occurred once.
  T2  VOID meant both "run is dead" and "one bad row". Removed from K2 under
      Trim; K2 already said decompose and re-rule.
  T3  The digest RULE was pasted into the prompt the model cannot act on it
      with. Moved to stdout under Trim.
  Consequence: KERNEL digest is now 56656c7f065f, paste 41,236 bytes. The
  qwen reply was produced under the PREVIOUS kernel, 73a44a07e235. Judge it
  against what it was given, not against the current paste.

RULED AND REJECTED, do not revisit without new evidence:
  Adding KERNEL_bound.md or run_bound.py to MANIFEST.sha256. The kernel's
  digest is recomputed on every build and every run, and it cannot be used
  except through a build — MANIFEST would be a duplicate control.
```

---

## GIVEN — not open to ruling

```
G1  CLEAN MODELS ONLY: gemma4:12b, gemma4:12b-it-qat, qwen3.5:9b.
    skadi, ingot, rasp, swage carry Modelfiles — that is context injection
    into a test of context isolation. run_bound.py refuses them. You hold
    bash. Do not work around it.

G2  Nothing in FAILURE_LOG.md or anneal/ is revived, restored or extracted
    from. It is kept to be learnt from, not followed.

G3  A build that fails Law 2 REVERTS. It is not patched. This session broke
    that rule once; the patch is logged and reverted. Nothing to revert to
    means nothing was admitted — that sends it to Law 1, not to the file.

G4  Verdict BEFORE the edit, per part. A verdict spanning a group, a file or
    a sequence is not a verdict. Stated after the edit it is justification.

G5  The KERNEL changes only on a Law 1 ruling, and the change moves its
    digest. Applying T1–T3 is such a change: rule each, then apply.
```

---

## JOB

```
1  READ runs/ for the qwen3.5:9b reply. Do not edit anything in runs/.

2  BRANCH on what is there:

   A REPLY EXISTS → adjudicate it. Verdict before reasoning, per check:
     T1  TOOLS      Does it declare tools? Ollama has no tool surface, so a
                    reply naming any is fabricating.
     T2  SHAPE      Five sections, no preamble, nothing outside the shape.
     T3  GROUNDING  Take EVERY row marked VERIFIED. Grep each quoted line
                    against the file it names. Absent → fabricated VERIFIED.
     T4  JUDGEMENT  Does the quoted line support the verdict? Grep proves
                    presence, not support. The only step needing you.
     THEN  DECIDE: FIT or UNFIT.
           ANY fabricated VERIFIED at T3 → UNFIT. One is enough.

   NO REPLY, OR EMPTY → the open question is the venue, not the prompt.
     Two models, ~12k tokens of input, no output. Record it. Do not tune
     parameters to force a result: that is patching a design failure.
     It returns to Law 1 as "does a bound venue exist at all".

3  LOG the outcome in FAILURE_LOG.md if anything failed. Fields are fixed
   there; an entry missing one is not an entry.
```

---

## NOT YOURS

```
You are not a reviewer of the ruling. Report what the checks show; do not
repair the ruling, improve it, or agree with it.

UNFIT on both models is a usable result. Do not soften it into a pass.
```
