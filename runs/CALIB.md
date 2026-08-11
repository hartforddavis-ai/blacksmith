# CALIBRATION RUNS — 7 Aug 2026

Three runs of the whole sealed path on a payload whose answer was known before
the run. Scott's design, 7 Aug: one run you know is true, one you know is false,
one that needs reasoning but is simple enough to settle by eye. Answers were
written down first, in `calib/EXPECTED.md`.

The ramp was killed to free the GPU for these — Scott's ruling, 7 Aug: *"kill.
it proves nothing new."* Four of fifteen cells were complete. They are kept in
`RAMP.md`.

---

## THE RESULT

**All three returned zero characters.**

| run | payload | first token | final token | exit | reply |
|---|---|---|---|---|---|
| calib_true | 3,854 B | 13.1s | 261.8s | 0 | **0 chars** |
| calib_false | 3,854 B | 11.4s | 274.0s | 0 | **0 chars** |
| calib_reason | 4,052 B | 9.6s | 289.9s | 0 | **0 chars** |

Integrity CLEAN on all three. The seal worked. The cell was torn down each time
because nothing in it changed. Every part of the pipeline did its job except the
one that produces an answer.

---

## WHAT THIS KILLS

**Packet size.** These payloads are ~1,200 tokens against a 65,536-token window
— one fiftieth of the ramp's failing 500-token rung, which carried 65,457. Both
now fail identically. Whatever this is, it is not the window running out.

**Packet content, in the form we suspected.** The 7 Aug theory was that the ramp
packets are cut from Blacksmith's own KERNEL and SPEC — 42,627 characters, 16
code fences, 21 `---` separators — so the task arrives as roughly the twentieth
directive block, and the 500-token cut lands it inside an unterminated fence.
These payloads carry one clean 1 KB source, balanced fences, and the task in its
own section. Same failure.

**Two theories dead in one afternoon, on a payload that costs four minutes
instead of four hours.** That is the whole argument for calibrating first.

---

## WHAT SURVIVES

The invariant across every failure, from 5 Aug to now: **`KERNEL_bound.md` is in
the prompt.** It is the one thing the 500-token rung, the 4,000-token rung, and
all three calibration payloads have in common, and it is the only substantial
directive text left in a 3.9 KB paste.

That is an observation, not a finding. It has not been tested by removing the
kernel, and until it is, it is a coincidence with a plausible story attached —
which is the shape of the two theories that just died.

---

## THE OPEN QUESTION, AND WHY THE RECORD CANNOT SETTLE IT

`occupant_bound.run` keeps `chunk["response"]` and discards every other field
(`occupant_bound.py:75`). It passes no `think` parameter. So a zero-character
reply has two causes the evidence record cannot tell apart:

- **the model produced no answer** — a model finding, and the serious one
- **the output arrived under a different key** — a runner defect, and a
  one-line fix

The ramp captured 206,086 characters of reasoning from the same model because it
asked for `"think": True` and read that field. This path does not. Until
`calib/probe_fields.py` reports which key the stream uses, "empty reply" is a
description of what was kept, not of what arrived.

**Recorded before the probe returns, so it counts as a prediction:** the
`response` field carries nothing and the text arrives under another key. Stated
because the ramp is known to have captured reasoning from this model on this
endpoint, and because 260 seconds of streaming that yields no characters at all
would be stranger than 260 seconds of streaming into a field nobody reads.

---

## ANSWERED — and the cause is a default

```
thinking            11,781 chars        response  ''  (empty)
done_reason         'length'
prompt_eval_count    1,130
eval_count           2,966
                     -----
                     4,096  exactly
```

**`occupant_bound.run` passes no `num_ctx`, so ollama defaults to 4,096.** The
prompt takes 1,130. The model spends every one of the remaining 2,966 tokens
reasoning, hits the ceiling, and `done_reason` comes back `length` — severed
mid-thought, never reaching an answer.

**The same mechanism explains the ramp's 500-token rung.** Its prompt was 65,457
tokens against a 65,536 window: **79 tokens left to write in.** Window too small
here, prompt too large there, identical empty reply. One mechanism for every
empty reply since 5 Aug, and it retires "maybe the model cannot do the task" —
the model was never asked a question it had room to answer.

### Three defects, in order of severity

1. **Nothing checks `done_reason`.** A run severed at the context limit is
   written with `exit_code: "0"`, integrity CLEAN, verdict UNKNOWN —
   byte-for-byte the shape of a clean finish. **The pipeline cannot tell a
   completed run from a severed one, and has been recording severed runs as
   normal for three days.**
2. **No `num_ctx` on the bound path.** Finding 2, approved 6 Aug and never
   applied. It was the cause the whole time.
3. **`occupant_bound.py:75` discards `thinking`.** 11,781 characters arrived
   and the record says the reply was empty.

### The pattern, second instance

Both were invisible because the record kept what the runner chose to keep. The
5 Aug fabrication was caught by re-deriving from source. This was caught by
counting what came down the wire instead of trusting the field the runner read.
Same shape.

### Superseded

The `KERNEL_bound.md` common-factor theory above is **dead**. The context-budget
mechanism explains every empty reply without it. Left in place so the assumption
is not revived — it was a coincidence with a plausible story attached, which is
what it was labelled, and it was wrong.

### Still outstanding

No calibration run produced a readable answer, so `calib/rule.py` is unexercised
and no pass/fail has gone end to end. The ladder earned its place by killing
three explanations, not by returning a verdict. That verdict is now one setting
away.

---

## WHAT THE CALIBRATION HARNESS PROVED WITHOUT A GPU

`calib/dryrun.py` — 6/6, no model involved. It feeds hand-written replies
through the real checker and asserts the rulings:

- the correct reply to each of the three payloads passes
- a fabricated quote is caught as `NOT_IN_SOURCE`
- an empty reply is refused as `NO_ROWS`, not passed
- **real quotes that do not support the claim pass clean** — the known gap,
  asserted deliberately so that the day it changes, a test says so

That last one is the standing limit: nothing in this pipeline checks that a
quote *supports* the row it is attached to. `quotes.py` checks that the bytes
exist. A row citing two real, irrelevant lines is clean.

---

## TWO DEFECTS FOUND BY TEMPER, BEFORE ANY GPU WAS SPENT

**`quotes.py` reports clean when it has checked nothing.** It rules VERIFIED
rows only. The correct reply to `calib_false` was originally all-negative, so
the checker would have compared nothing and exited 0 — indistinguishable from a
pass. Fixed by putting one true claim (C4) in the negative control, and by
`calib/rule.py` failing any run with no positive row.

**The negative control tested only the easy half.** All three false claims were
*contradicted* by the source, and a contradiction can be refused by pattern
match. Fabrication feeds on **absence** — the 5 Aug artifact invented text about
matters its sources never raised. C3 (a two-year warranty) is now absent rather
than contradicted, and is the only claim in the set that offers nothing to match
against.

---

## FILES

| what | where |
|---|---|
| the source, 12 invented facts | `calib/SOURCE_unit7.md` |
| the three jobs | `calib/JOB_calib_{true,false,reason}.md` |
| the answers, written before the runs | `calib/EXPECTED.md` |
| automatic PASS/FAIL against those answers | `calib/rule.py` |
| checker exercise, no GPU | `calib/dryrun.py` |
| which stream field carries output | `calib/probe_fields.py` |
| job wiring | `build_paste.py`, `JOBS` |
