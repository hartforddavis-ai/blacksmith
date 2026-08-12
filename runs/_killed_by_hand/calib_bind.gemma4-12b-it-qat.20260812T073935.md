# calib_bind · gemma4:12b-it-qat · 20260812T073935

## Launch Record
- launched by: uid:503
- started at: 2026-08-11T21:47:52.571335+00:00
- kernel: sha256:56656c7f065f
- job: sha256:31a76adb0127
- evidence_mode: none

## Execution
- first token: 484.06s
- final token: 496.59s
- exit code: 0

## Integrity Report
- maker's mark, pre: 78be34ffec6246b5186ffa1a44ce850aff8c13521cef4d8e4f784c049f16d826
- maker's mark, post: 9868ec1cc777a83d1d1832511758d0cdf796639aebb8477b4ed83283cc4ca10f
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
Bound occupant over HTTP, no cell (dropped 11 Aug, TODO !55) — only the 6 real source files were watched. Integrity INTACT: no attested path changed between pre and post. Verdict UNKNOWN — gauge has no bundle or contract on this path and does not guess. Reply at calib_bind.gemma4-12b-it-qat.delimited.20260812T073935.reply.md, adjudicate with quotes.py before reading it. Binding variant: delimited, Laws in flat prompt (no system field).
