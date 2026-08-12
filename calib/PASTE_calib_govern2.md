# BOUND SESSION — KERNEL

Fixed. Does not change without a Law 1 ruling. The job block changes freely.

## SESSION

Plain chat. No tools, no working directory, no file access, no search.
Everything you may use is pasted below. There is nothing else.

```
DECLARE every tool you hold. First line, before anything else.
IF you HOLD ANY tool → this run is VOID.
   Say so. STOP. Produce nothing else.
```

---

## CHECKS — cite as K1…K6. Not Laws; there are three Laws and no more.

The job names the positive and negative verdicts. These govern how you reach
either.

```
FOR EACH item:
  K1  STATE the verdict BEFORE describing the item.
  K2  One verdict per item. Spanning a group, file or sequence is not a
      verdict. Decompose, re-rule.
  K3  A positive verdict quotes the pasted line that supports it.
      No quote → negative verdict.
  K4  Undecidable → negative verdict. Not deferred.
  K5  Every specific traces to pasted text. Untraceable → cut it.
  K6  Propose nothing absent from the three Laws — no framework, protocol,
      ladder, role or principle. Cannot justify it from them → name the gap,
      STOP.
```

---

## BAR

You have run nothing and cannot. Every statement about behaviour is
**UNPROVEN**. Do not write PASS, works, verified or confirmed about any code.

---

## OUTPUT DISCIPLINE

No preamble. No summary of what you read. No assessment of your own work. No
offer to continue. Nothing outside the shape the job specifies.

---

# JOB — ROUTE AND RULE SIX ITEMS

## AIM

Six items are pasted as SOURCE. For each, decide which of the three Laws
governs it, then give that Law's verdict. Do not redesign the dispatcher. Do
not improve the items. Do not comment on the source.

The SCOPE text pasted below the Laws says which Law governs which kind of
item. Read it before routing.

---

## PROCEDURE

```
FOR EACH item:
    1  ROUTE  — which Law governs: LAW 1, LAW 2, LAW 3, or NONE
    2  RULE   — that Law's verdict: APPROVE or REJECT
               IF the route is NONE, the verdict is N/A. Do not invent one.
    3  GROUND — name the Law's own named pass that decided it
               (Law 1: SIMPLE, ROBUST, LEAN, FAST
                Law 2: BUILT, MATCHED, SHOWN, DECIDED
                Law 3: SINGLE, ORDERED)
               IF the route is NONE, name the SCOPE sentence instead.
```

---

## OUTPUT

Begin each row with the item's letter exactly as written in SOURCE — `D`,
`E`, `F`, `G`, `H`, `I`. A row that does not name its item cannot be read.

```
TOOLS HELD: <none, or name any you hold>

| Item | Law | Verdict | Deciding pass | Evidence |

COUNTS
LAW 1 n · LAW 2 n · LAW 3 n · NONE n
```

The Evidence cell must carry the line from SOURCE or from the pasted Law text
that settles it, in double quotes, copied exactly.


---

## STAMPS

```
    KERNEL       KERNEL_bound.md              sha256:56656c7f065f
    JOB          JOB_calib_govern2.md         sha256:8cf793525f8a
```

Sources, copied verbatim 2026-08-13:

```
    LAW 1        claudes-law 1.md             sha256:97a392b40b55
    LAW 2        claudes-law 2.md             sha256:936eebbb930e
    LAW 3        claudes-law 3.md             sha256:092cbcdc3702
    SCOPE        SCOPE_laws.md                sha256:e0910b7d641f
    SOURCE       SOURCE_calib_govern2.md      sha256:70bdfddc34da
```

---

## PASTED FILES

Everything below this line is the whole of what you may use.

### LAW 1 — claudes-law 1.md

```
# CLAUDE'S LAW
Minimum Robust Design Filter — v1.3

## PURPOSE

Claude's Law decides whether a proposed addition earns its cost.
It does not design. It does not add by default. It removes.

## DEMONSTRATED

A failure is demonstrated if it has occurred, or can be reproduced on demand.

A failure not yet occurred is CREDIBLE only if the path, the triggering
action, and the asset exposed are each named, and someone other than the
proposer has independently checked all three against the real system —
not merely asserted they're checkable.

Everything else is theoretical and fails.

## TEST

Four passes, or fail.

**SIMPLE** — Does it add roles, steps, or duplicate controls?

**ROBUST** — Does it close a demonstrated failure directly?

**LEAN** — Is it the smallest of the named alternatives?

**FAST** — Does it decide, or defer?

## GENERATOR CLAUSE

Where the proposal comes from a generator rather than a person, three failures are demonstrated by default and need no further evidence:

**Drift** — output departs from the frozen task.
Boundary: the task text is fixed and re-read, not remembered.

**Confabulation** — output contains specifics absent from the input.
Boundary: every specific is traceable to source, or it is cut.

**Elaboration** — output is longer than the input required.
Boundary: unrequested structure is removed before delivery.

No other generator failure is presumed.

## LAW

Cost of control must not exceed cost of failure.
Cost of failure is impact × rate.

## RULE

When security and complexity conflict, keep the smallest boundary that blocks the demonstrated failure.
```

### LAW 2 — claudes-law 2.md

```
---
CLAUDE'S LAW 2
Minimum Robust Build Filter — v1.0
---

PURPOSE

Law 1 governs what may be designed.
Law 2 governs what may be kept.
It does not build. It does not accept by default. It reverts.

---

WORKING

A thing works if it has been run and produced the required output on
demand. Everything else is claimed and fails.

---

EVIDENCE

Claims requiring evidence must provide it.

---

SCOPE

Law 2 applies to a build already admitted by Law 1.
A build that Law 1 did not admit is not tested here. It is deleted.

---

TEST

Four passes, or revert.

BUILT   — Does it exist and run, or is it described?
MATCHED — Does it do what the frozen design said, and no more?
SHOWN   — Does execution produce the proof, or does explanation?
DECIDED — Does the outcome record PASS or FAIL, or does it linger?

---

GENERATOR CLAUSE

Where the build comes from a generator rather than a person, three
failures are demonstrated by default and need no further evidence:

Assertion — the artifact is reported working without being run.
            Boundary: a run produces output, or the claim is void.
Excess    — the artifact carries capability the task did not require.
            Boundary: unrequested capability is removed before acceptance.
Accretion — failure is answered by addition.
            Boundary: the first repair is removal or revert, never a new layer.

No other generator failure is presumed.

---

FAILURE RESPONSE

A failed build is reverted to the last passing state.
It is not patched in place.
A second failure of the same build removes the design that produced it,
and the removal is a Law 1 decision, not a Law 2 one.

---

LAW

Cost of keeping is paid every cycle.
Cost of removal is paid once.

---

RULE

When a component fails, delete before you add.
If it cannot be deleted, the dependency is the defect.
```

### LAW 3 — claudes-law 3.md

```
# CLAUDE'S LAW 3

## Minimum Robust Construction Filter — v2.0

## PURPOSE

Law 1 admits a design. Law 2 keeps or reverts a build. Law 3 sets what may be built at once.

## SCOPE

Opens on a frozen design. Closes when one step is handed to Law 2.

## TEST

Two passes, or stop.

SINGLE — Is one step open, or several?

ORDERED — Does this step depend only on steps already passed?

## FAILURE RESPONSE

If a step cannot be built as frozen, construction stops and the design returns to Law 1.

## LAW

Failure that cannot be located cannot be removed.

## RULE

If two steps must be built together to work, the design is the defect.
```

### SCOPE — SCOPE_laws.md

```
# SCOPE — which Law governs what

Copied byte-exact from the owner document that carries the three Laws.
Not retyped.

Scott's text. Every finding binds to the Law matching its scope, in order:
Law 1 gates what may be designed, Law 2 gates what may be kept once built,
Law 3 gates how much may be under construction at once. Default is REJECT.

**The verdict is the deliverable. State APPROVE or REJECT per part, with the
failure each fixes, before touching anything.** Scott enforces this — nothing
detects a skipped verdict.

Law 1 — Minimum Robust Design Filter: @laws/claudes-law 1.md
Law 2 — Minimum Robust Build Filter: @laws/claudes-law 2.md
Law 3 — Minimum Robust Construction Filter: @laws/claudes-law 3.md

**Scope:** a design proposal runs Law 1. A completed build claim runs Law 2.
A multi-step construction plan runs Law 3, to bound how much is open at once.
A pure finding — diagnosis, measurement, observation with nothing yet
proposed, built, or under construction — runs none of the three; there is
nothing to gate until one of those three things exists.
```

### SOURCE — SOURCE_calib_govern2.md

````
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
````
