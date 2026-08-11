# calib_true · qwen3.5:9b · 20260811T141759

## Launch Record
- launched by: uid:503
- started at: 2026-08-11T04:25:27.910620+00:00
- kernel: sha256:56656c7f065f
- job: sha256:9943c6e61c97
- evidence_mode: copy

## Execution
- first token: 13.19s
- final token: 448.70s
- exit code: 0

## Integrity Report
- cell pre-hash: 8c0d1e3e3c9dba749ff025a18ffcafcad369ad59dd0e19d8d4b25a78467dcefc
- cell post-hash: 546da41759f6e7d8c6cb52d3f1993b00fe7323f7a2ec30396d13ee32e604ddb2
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
Bound occupant over HTTP, sealed cell at /private/tmp/blacksmith-cells/calib_true.qwen3.5-9b.20260811T141759, scratch declared empty. Integrity INTACT: no attested path changed between pre and post. Verdict UNKNOWN — gauge has no bundle or contract on this path and does not guess. Reply at calib_true.qwen3.5-9b.20260811T141759.reply.md, adjudicate with quotes.py before reading it. Reasoning (16,906 chars) at calib_true.qwen3.5-9b.20260811T141759.thinking.md.
