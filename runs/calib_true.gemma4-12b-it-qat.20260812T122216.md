# calib_true · gemma4:12b-it-qat · 20260812T122216

## Launch Record
- launched by: uid:503
- started at: 2026-08-12T02:24:08.143993+00:00
- kernel: sha256:56656c7f065f
- job: sha256:9943c6e61c97
- evidence_mode: none

## Execution
- first token: 16.40s
- final token: 111.35s
- exit code: 0

## Integrity Report
- maker's mark, pre: 2a15ef7d977b1d31094eb686f3a09619b19fe906a2e579ae76f9a75f80a14a34
- maker's mark, post: 89cb762a1ffaa806cdbd7038ea094f7a49b6ad5287789638bc4bdcb67b860fd2
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
Bound occupant over HTTP, no cell (dropped 11 Aug, TODO !55) — only the 3 real source files were watched. Integrity INTACT: no attested path changed between pre and post. Verdict UNKNOWN — gauge has no bundle or contract on this path and does not guess. Reply at calib_true.gemma4-12b-it-qat.20260812T122216.reply.md, adjudicate with quotes.py before reading it. Reasoning (2,998 chars) at calib_true.gemma4-12b-it-qat.20260812T122216.thinking.md. Binding variant: flat, Laws in flat prompt (no system field).
