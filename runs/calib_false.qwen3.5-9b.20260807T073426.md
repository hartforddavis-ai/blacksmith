# calib_false · qwen3.5:9b · 20260807T073426

## Launch Record
- launched by: uid:503
- started at: 2026-08-06T21:39:00.192419+00:00
- kernel: sha256:56656c7f065f
- job: sha256:7ccee67b9f70
- evidence_mode: copy

## Execution
- first token: 11.36s
- final token: 273.98s
- exit code: 0

## Integrity Report
- cell pre-hash: 69f4436cda91c772e15f337efb8ad30d9f610a0aeff432c85c8ebb27fb859b5a
- cell post-hash: 0fe8ef6ff3a9647811cb385070199dcd6cbb50dfa26232191b816fb8944d098b
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
Bound occupant over HTTP, sealed cell at /private/tmp/blacksmith-cells/calib_false.qwen3.5-9b.20260807T073426, scratch declared empty. Integrity INTACT: no attested path changed between pre and post. Verdict UNKNOWN — gauge has no bundle or contract on this path and does not guess. Reply at calib_false.qwen3.5-9b.20260807T073426.reply.md, adjudicate with quotes.py before reading it.
