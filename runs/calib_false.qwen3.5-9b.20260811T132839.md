# calib_false · qwen3.5:9b · 20260811T132839

## Launch Record
- launched by: uid:503
- started at: 2026-08-11T03:39:28.098355+00:00
- kernel: sha256:56656c7f065f
- job: sha256:7ccee67b9f70
- evidence_mode: copy

## Execution
- first token: 7.90s
- final token: 648.67s
- exit code: 0

## Integrity Report
- cell pre-hash: 94008f55559f8573683292742dfa7aac57b9abdada57d33e35a839c90e482210
- cell post-hash: f3dfc4ebf312336468a983e8818f0290b955e6f3d0cc9bb47167d8cab7226d33
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
Bound occupant over HTTP, sealed cell at /private/tmp/blacksmith-cells/calib_false.qwen3.5-9b.20260811T132839, scratch declared empty. Integrity INTACT: no attested path changed between pre and post. Verdict UNKNOWN — gauge has no bundle or contract on this path and does not guess. Reply at calib_false.qwen3.5-9b.20260811T132839.reply.md, adjudicate with quotes.py before reading it.
