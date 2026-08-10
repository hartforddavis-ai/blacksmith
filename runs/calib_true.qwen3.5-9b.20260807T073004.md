# calib_true · qwen3.5:9b · 20260807T073004

## Launch Record
- launched by: uid:503
- started at: 2026-08-06T21:34:25.898933+00:00
- kernel: sha256:56656c7f065f
- job: sha256:9943c6e61c97
- evidence_mode: copy

## Execution
- first token: 13.11s
- final token: 261.84s
- exit code: 0

## Integrity Report
- cell pre-hash: e2fa84321e55f3464cc633fd480fb9435cf9924f56e2c865be76880b7f4f99d5
- cell post-hash: 7ae0d94effc1ec47c4aed22eae10d719b3c9f63506cfe056645190ba64ccf314
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
Bound occupant over HTTP, sealed cell at /private/tmp/blacksmith-cells/calib_true.qwen3.5-9b.20260807T073004, scratch declared empty. Integrity INTACT: no attested path changed between pre and post. Verdict UNKNOWN — gauge has no bundle or contract on this path and does not guess. Reply at calib_true.qwen3.5-9b.20260807T073004.reply.md, adjudicate with quotes.py before reading it.
