# calib_reason · qwen3.5:9b · 20260807T073900

## Launch Record
- launched by: uid:503
- started at: 2026-08-06T21:43:50.160102+00:00
- kernel: sha256:56656c7f065f
- job: sha256:e47d975d9418
- evidence_mode: copy

## Execution
- first token: 9.63s
- final token: 289.87s
- exit code: 0

## Integrity Report
- cell pre-hash: 3268b33789063190a1b4a28ce00edd8d93a5dd06299fbe6f2aaf204ff916964c
- cell post-hash: 3825535826f5fbc46e8dac34239565483783397d50c1d47ce23c08a5aafdc029
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
Bound occupant over HTTP, sealed cell at /private/tmp/blacksmith-cells/calib_reason.qwen3.5-9b.20260807T073900, scratch declared empty. Integrity INTACT: no attested path changed between pre and post. Verdict UNKNOWN — gauge has no bundle or contract on this path and does not guess. Reply at calib_reason.qwen3.5-9b.20260807T073900.reply.md, adjudicate with quotes.py before reading it.
