# JOB 8 — does the task survive being made bigger?

Run this **only after Job 2**, and only if Job 2 came back clean.

> **The Filter rejected this job on 6 Aug, on ROBUST.** No rung above 500 tokens
> has ever run here, so nothing has failed at scale, and "it might break when
> bigger" is a forecast rather than a demonstrated failure. Kept because the
> owner set a four-day budget and it is cheap to run — but it is optional work,
> and it should be the first thing dropped if time runs short.

---

## WHY

The ramp climbs 500 → 1,000 → 2,000 → 4,000 → 8,000 tokens, on the assumption
that the task stays constant and only the size changes. That assumption has
never been checked.

If a strong model counts eight markers perfectly in a small packet and starts
missing them in a large one, then size alone breaks the task, and the ramp is
measuring the wrong thing — it would be recording "this model cannot handle
8,000 tokens" when the truth is "nobody can do this task at 8,000 tokens".

This is the same question Job 2 asks, asked at the top of the ladder instead of
the bottom.

---

## HOW TO RUN IT

Two packets in `packets/`:

| packet | size | markers |
|---|---|---|
| `packet_d.txt` | ~2,000 tokens (8,411 chars) | 8 |
| `packet_e.txt` | ~8,000 tokens (32,417 chars) | 8 |

Same rules as Job 2, and they matter more here because the packets are long
enough that a platform may quietly truncate them:

- **Paste the whole file. Add nothing.** Each ends with its own instruction.
- **Fresh chat for every packet on every platform.**
- **Check the paste actually went through.** Some free platforms silently cut
  long pastes or convert them to an attachment. If the platform shows an
  attachment rather than text in the message, that is a different experiment —
  note it, and try another platform.
- Both packets contain **the same number of markers**. Do not tell the model
  that. If a model returns the same number for both, that is either two correct
  answers or one habit, and only the wrong ones tell them apart.

Run `packet_d.txt` on every platform first, then `packet_e.txt`. Same models as
Job 2 if possible — a comparison across sizes is only readable if the model is
held constant.

---

## WHAT TO BRING BACK

Per platform, per packet:

1. Platform and model name.
2. The reply, verbatim.
3. Did it obey "one line and nothing else"?
4. Any sign the paste was truncated, attached, or summarised rather than read.

Point 4 is not housekeeping. A model answering from a truncated paste will give
a confident wrong number and nothing will indicate why, and that is the exact
failure mode this whole investigation is circling.

---

## WHAT IT DECIDES

- **Correct at both sizes** → the task holds at scale, the ladder is sound, and
  local failures at the top are real model limits.
- **Correct small, wrong large** → the ladder's upper rungs are unreadable, and
  the ramp should be cut back to the sizes where the task is known to work.
- **Wrong at both** → go back to Job 2; something is wrong with the task, not
  with the size.
