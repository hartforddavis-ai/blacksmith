# calib_bind · gemma4:12b-it-qat · 20260812T072817

## Launch Record
- launched by: uid:503
- started at: 2026-08-11T21:39:20.443944+00:00
- kernel: sha256:56656c7f065f
- job: sha256:31a76adb0127
- evidence_mode: none

## Execution
- first token: 652.34s
- final token: 663.12s
- exit code: 0

## Integrity Report
- maker's mark, pre: 7cba2c2b4fa0d2e2aeb336cacbb38da5711b90efcf8e6e7e1f74cec3561854fa
- maker's mark, post: 6191ad39d94edcebb31ed105d496404fc8e1f31684e0f68da85caf828e042e32
- delta: CLEAN
- verdict: UNKNOWN

## Proof Chain
1. Launch-record proves session started (timestamp, who, what job)
2. Execution proves session ran (tokens arrived, exit status)
3. Integrity-report proves output wasn't tampered — the delta line is
   the evidence. The two hashes identify the measurements it compared;
   they are never equal to each other, because each covers its own
   phase name.
4. Verdict proves adjudication (ACTIVE/FAILED/UNKNOWN/BYPASSED)
5. **All four together = proof that session ran and output is credible**

## Lesson
Bound occupant over HTTP, no cell (dropped 11 Aug, TODO !55) — only the 6 real source files were watched. Integrity INTACT: no attested path changed between pre and post. Verdict UNKNOWN — gauge has no bundle or contract on this path and does not guess. Reply at calib_bind.gemma4-12b-it-qat.system.20260812T072817.reply.md, adjudicate with quotes.py before reading it. Binding variant: system, Laws in system field (4,187 chars).
