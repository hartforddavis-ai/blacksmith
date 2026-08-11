# Spec 2: Evidence Log Schema — Formal Proof Chain

## Problem
Evidence exists (FAILURE_LOG pattern) but is informal. Launch-record and integrity-report are two independent assertions with no explicit join. No formal proof that a session ran and its output is credible.

## Solution
Define evidence log schema as the formal proof chain that joins:
- Launch-record (session started, when, by whom)
- Execution (what the bound code did, what states it recorded)
- Integrity-report (output wasn't tampered, verdict is valid)

---

## Evidence Log Schema

**Filename:** `<job>.<model>.<timestamp>.md`

**Required Fields:**

```
# <job> · <model> · <timestamp>

## Launch Record
- launched by: <UID/process>
- started at: <ISO timestamp>
- kernel: <kernel digest>
- job: <job digest>
- evidence_mode: <"copy" or "mount">

## Execution
- first token: <time offset from launch>
- final token: <time offset from launch>
- exit code: <code or timeout>

## Integrity Report
- maker's mark, pre: <sha256>
- maker's mark, post: <sha256>
- delta: <"CLEAN" or "MODIFIED">
- verdict: <ACTIVE|FAILED|UNKNOWN|BYPASSED>

## Proof Chain
1. Launch-record proves session started (timestamp, who, what job)
2. Execution proves session ran (tokens arrived, exit status)
3. Integrity-report proves output wasn't tampered — the delta line is the
   evidence. The two hashes identify the measurements it compared; they are
   never equal to each other, because each covers its own phase name.
4. Verdict proves adjudication (ACTIVE/FAILED/UNKNOWN/BYPASSED)
5. **All four together = proof that session ran and output is credible**

## Lesson
[Single sentence summarizing what this run teaches about Blacksmith]
```

---

## Required Outputs

Every run produces one evidence log entry with all fields. No field is optional. No entry is filled partially.

**Pre-run:** Launch-record exists before first byte.
**Post-run:** Integrity-report and verdict written before process exits.
**Chain:** All four sections present and timestamped.

---

## Acceptance
Evidence log exists for every run. All required fields present. Proof chain is explicit and unambiguous.
