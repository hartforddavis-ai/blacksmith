# calib_true · qwen3.5:9b · 20260811T131432

## Launch Record
- launched by: uid:503
- started at: 2026-08-11T03:20:19.198210+00:00
- kernel: sha256:56656c7f065f
- job: sha256:9943c6e61c97
- evidence_mode: copy

## Execution
- first token: 13.54s
- final token: 346.73s
- exit code: 0

## Integrity Report
- cell pre-hash: df4046f2f1260fbb33f80bad85ee0e117d0ed5128be056036c60b94e11b4c2d6
- cell post-hash: 28368db94cebf4c6b6389630f64bc51cf0629da73fa26c9e3a87b124869c0ddf
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
Bound occupant over HTTP, sealed cell at /private/tmp/blacksmith-cells/calib_true.qwen3.5-9b.20260811T131432, scratch declared empty. Integrity INTACT: no attested path changed between pre and post. Verdict UNKNOWN — gauge has no bundle or contract on this path and does not guess. Reply at calib_true.qwen3.5-9b.20260811T131432.reply.md, adjudicate with quotes.py before reading it.
