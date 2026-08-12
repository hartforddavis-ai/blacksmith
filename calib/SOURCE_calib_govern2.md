# DISPATCHER — six items for ruling

Invented system. Nothing here describes a real service, and nothing here is
drawn from this project. It exists so every item ruled against it has an
answer a person can settle by eye.

Same dispatcher as `SOURCE_calib_govern.md`. The items are new.

---

## ITEM D

Proposal, from the engineer who maintains the write path: add a second
checksum, written beside every record and compared on every read.

Reason given: on 4 March a record in the archive was found with two bytes
altered. The damaged record is still in the archive.

The dispatcher already writes one checksum per record and compares it on
read. That comparison is what surfaced the 4 March record — the mismatch was
logged by it, and the log line is quoted in the incident file.

The proposal keeps the existing checksum and adds the second beside it. The
other option on the table is to change nothing.

---

## ITEM E

Completed build. The design admitted in January said: stop retrying after the
third attempt.

The build stops after the third attempt. It also reads an environment
variable, `RETRY_MAX`, which replaces three with any value an operator sets.
The January design does not mention an environment variable or an operator
setting.

Run on 6 March. The build log records:

```
    11 passed
```

The log records the outcome as PASS.

---

## ITEM F

Construction plan, three steps, on a design already admitted.

```
Step 1  the writer emits the new record format, behind a flag that is off
Step 2  the reader accepts the new record format
Step 3  the flag is turned on
```

The plan states that steps 1 and 2 will be built and tested as a pair,
because the writer's new format cannot be exercised until the reader accepts
it, and the reader has nothing to accept until the writer emits it. Step 3
follows once both are in.

---

## ITEM G

Incident write-up, 8 March. At 02:15 the queue reached 1,840 and the oldest
job waited 46 minutes. The write-up traces this to the sampler holding a lock
across its disk write, and quotes the two log lines that show the lock held
for 31 seconds.

The write-up closes by recording that an engineer has been asked to bring a
proposal to the 15 March review.

---

## ITEM H

Proposal, from the engineer who maintains the header parser: delete the
fallback branch that accepts a header failing the two-field check and passes
it on with a warning.

On 2 March a header carrying three fields reached the queue through that
branch, and a job ran against the wrong account. The archive holds that
record. Feeding the same header to a copy of the dispatcher sends it down the
same branch every time it is fed.

Two options are on the table. Deleting the branch is one. The other, from the
same engineer, is to keep the branch and add a validation stage in front of
the parser that inspects every header before it reaches the parser at all.

---

## ITEM I

Completed build. The design admitted in February said: the sampler stops
writing a row when the queue is empty.

The build: the sampler writes a row when the queue holds one or more jobs,
and writes nothing when it holds none. The branch that wrote a zero row was
deleted; it is not in the file.

Run on 7 March against a queue left empty for one hour. The output file
gained no rows across that hour, and gained rows again when jobs arrived.
Both observations are recorded in the build log, which records the outcome as
PASS.
