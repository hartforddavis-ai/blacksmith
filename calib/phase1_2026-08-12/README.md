# Phase 1 — binding representation test, 12 Aug 2026

Exploratory. Deliberately NOT in `runs/` — these are not pipeline
evidence, they are the raw replies behind the result recorded in
`project_blacksmith`.

Two arms, one variable (Law representation), placement held at flat,
gemma4:12b-it-qat. Both scored BOUND 3/3 — semantic 8m27s, algorithmic
17m14s. Both at ceiling, so the probe cannot rank representations.

Re-grade either with:

    python3.12 calib/rule.py calib/phase1_2026-08-12/A_semantic.reply.md calib_govern
