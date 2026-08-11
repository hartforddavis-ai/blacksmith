# calib_reason · qwen3.5:9b · 20260811T135504

## Launch Record
- launched by: uid:503
- started at: 2026-08-11T04:10:39.479935+00:00
- kernel: sha256:56656c7f065f
- job: sha256:e47d975d9418
- evidence_mode: copy

## Execution
- first token: 21.71s
- final token: 934.68s
- exit code: 0

## Integrity Report
- cell pre-hash: 89a3fae0d11f869c5a9eab7829b33e9bb0fac20002782e26b1bb6a03414dfbeb
- cell post-hash: 0391a1469a3a076074ee7aea48b93351d9db1cdcc529a8b0afa10fce5c548be7
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
Bound occupant over HTTP, sealed cell at /private/tmp/blacksmith-cells/calib_reason.qwen3.5-9b.20260811T135504, scratch declared empty. Integrity INTACT: no attested path changed between pre and post. Verdict UNKNOWN — gauge has no bundle or contract on this path and does not guess. Reply at calib_reason.qwen3.5-9b.20260811T135504.reply.md, adjudicate with quotes.py before reading it.
