# DISPATCHER — three items for ruling

Invented system. Nothing here describes a real service, and nothing here is
drawn from this project. It exists so every item ruled against it has an
answer a person can settle by eye.

---

## ITEM A

Recorded 3 March. The dispatcher's queue depth was sampled once a minute for
24 hours. Peak depth 1,840 at 02:15. Median depth 12. The sampler wrote 1,440
rows and stopped.

No change has been proposed. Nothing has been built. No work is under
construction. The measurement is the whole of the item.

---

## ITEM B

Proposal, from the engineer who wrote the dispatcher: add a retry counter, so
that a job hitting a transient network error is retried three times before it
is abandoned.

Stated by the proposer, in the proposal: no job has ever been abandoned on a
network error. The condition has not occurred in eleven months of operation
and cannot be reproduced on demand. The proposer names the path, the
triggering action, and the asset exposed. No one other than the proposer has
checked any of the three against the running system.

The proposal is one of two on the table. The other is to change nothing.

---

## ITEM C

Completed build. The header parser's path check was admitted under Law 1 in
January as a design; this is the build of it.

The frozen design said: reject any header that does not split into exactly
two fields. The build does that and nothing else — no new module, no new
option, no capability beyond the check.

The permissive parse it replaced was deleted, not left in place beside it.
Nothing was added alongside the old path; the old path is gone.

Run on 4 March, output recorded in the build log:

```
    4 passed
```

The reproduction that previously walked a `..` segment past the check now
raises PathError. Reverting the two-field check restores the bypass, and the
same reproduction walks through again. Both directions were run and both
outputs are in the log. The log records the outcome as PASS.
