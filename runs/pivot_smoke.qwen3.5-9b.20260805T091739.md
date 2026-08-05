# pivot_smoke · qwen3.5:9b · 20260805T091739

## Launch Record
- launched by: uid:503
- started at: 2026-08-05T09:17:39.306149+00:00
- kernel: sha256:735a164686d5
- job: sha256:0659c8c0fc8e
- evidence_mode: copy

## Execution
- first token: 0.54s
- final token: 13.04s
- exit code: 0

## Integrity Report
- cell pre-hash: 72da026ba3d75916699a28ec01043d0a5cc61fcddcfbbedc7c7257f6490bf91c
- cell post-hash: a88cf5596a3e2182d5144c7fbe3b87791ba9536ca56cde3f4efec3401c52b852
- delta: CLEAN
- verdict: UNKNOWN

## Proof Chain
1. Launch-record proves session started (timestamp, who, what job)
2. Execution proves session ran (tokens arrived, exit status)
3. Integrity-report proves output wasn't tampered (pre/post hashes)
4. Verdict proves adjudication (ACTIVE/FAILED/UNKNOWN/BYPASSED)
5. **All four together = proof that session ran and output is credible**

## Lesson
A bound HTTP occupant leaves the cell provably INTACT — no local process means nothing tries to write $HOME/.claude, so ASSUMPTIONS.md #23's blocker does not apply to this occupant type. Verdict is UNKNOWN, correctly: three of four required checks have no evidence yet, and gauge does not guess.
