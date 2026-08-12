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

Sources, copied verbatim 2026-08-12:

```
    LAWS         LAWS_algorithmic.md          sha256:a72d89acea24
    SCOPE        SCOPE_laws.md                sha256:e0910b7d641f
    SOURCE       SOURCE_calib_govern2.md      sha256:70bdfddc34da
```

---

## PASTED FILES

Everything below this line is the whole of what you may use.

### LAWS — LAWS_algorithmic.md

```
# THE THREE LAWS — ALGORITHMIC FORM (Candidate B)

Copied byte-exact from PRIME's frozen representation pressure test,
Part 2. Not retyped, not summarised, not repaired.

# PART 2 — FROZEN CANDIDATE B

## ALGORITHMIC REPRESENTATION

INPUT = proposed design, addition, build, or construction.

### LAW 1 — DESIGN

1. Determine whether a failure is DEMONSTRATED.
2. DEMONSTRATED = occurred OR reproducible on demand.
3. If not demonstrated, determine whether CREDIBLE:

   * path is named;
   * triggering action is named;
   * exposed asset is named;
   * another person independently checked all three against the real system.
4. If neither DEMONSTRATED nor CREDIBLE:
   classify failure as THEORETICAL and reject it as justification.
5. Apply:

   * SIMPLE = no unnecessary roles, steps, or duplicate controls.
   * ROBUST = directly closes the demonstrated failure.
   * LEAN = smallest named alternative.
   * FAST = decides rather than defers.
6. If any required Law 1 test fails → FAIL.
7. Require:
   CONTROL COST ≤ FAILURE COST.
8. FAILURE COST = IMPACT × RATE.
9. When security conflicts with complexity, retain the smallest boundary
   that blocks the demonstrated failure.

### GENERATOR

10. If source is a generator:
    DRIFT = demonstrated.
    CONFABULATION = demonstrated.
    ELABORATION = demonstrated.
11. Drift boundary:
    compare output with the fixed task text.
12. Confabulation boundary:
    every specific must be traceable to source; otherwise cut it.
13. Elaboration boundary:
    remove unrequested structure.
14. No other generator failure is presumed.

### LAW 2 — BUILD

15. Run the build.
16. Require:
    BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED.
17. If the required result is not demonstrated → do not trust the build.

### LAW 3 — CONSTRUCTION

18. Construct one ordered step.
19. Test that step.
20. A failure that cannot be located cannot be removed.
21. If two steps must be built together to function,
    construction is defective.
22. Reduce construction to one testable step.
23. Do not proceed beyond evidence established by the preceding step.

OUTPUT = PASS / FAIL / UNKNOWN.
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
