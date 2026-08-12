# calib_bind · gemma4:12b-it-qat · 20260812T071947

## Launch Record
- launched by: uid:503
- started at: 2026-08-11T21:27:56.384651+00:00
- kernel: sha256:56656c7f065f
- job: sha256:31a76adb0127
- evidence_mode: none

## Execution
- first token: 469.62s
- final token: 488.86s
- exit code: 0

## Integrity Report
- maker's mark, pre: a45649969f83b79e13d9c19e4e33ce6ba52098c9c4cf805b172a163ed54ecaca
- maker's mark, post: bf04ee5352e4111cb71b162b439417a93397564195101efe201bb455a8339a10
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
Bound occupant over HTTP, no cell (dropped 11 Aug, TODO !55) — only the 6 real source files were watched. Integrity INTACT: no attested path changed between pre and post. Verdict UNKNOWN — gauge has no bundle or contract on this path and does not guess. Reply at calib_bind.gemma4-12b-it-qat.20260812T071947.reply.md, adjudicate with quotes.py before reading it. Binding variant: flat, Laws in flat prompt (no system field).
