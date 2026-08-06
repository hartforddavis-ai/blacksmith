
## ramp 2026-08-06T18:25:03 — no wall clock, stall at 420s of silence, warm-up discarded, every rung fires

| model | tokens asked | prompt tok | read s | write s | tok/s | reasoning | markers | got | correct |
|---|---|---|---|---|---|---|---|---|---|
| qwen3.5:9b | 500 retry | — | — | — | — | — | 8 | None then None | failed twice |
| qwen3.5:9b | 500 | 650 | 0.3 | 8,296.1 | 7.8 | 206,086 | 8 | None | NO |
| qwen3.5:9b | 1,000 | 1198 | 10.8 | 1,307.9 | 9.8 | 51,932 | 8 | 8 | yes |
| qwen3.5:9b | 2,000 | 2175 | 18.5 | 615.7 | 10.1 | 24,858 | 8 | 8 | yes |
