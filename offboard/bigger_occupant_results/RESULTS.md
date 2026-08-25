# RESULTS — JOB_bigger_occupant.md, run 20 Aug 2026

Answers `!95` (does a bigger occupant separate the semantic/algorithmic Law
representations, where the local model gemma4:12b-it-qat hit a 6/6 ceiling
on both). Run via Safari MCP. Panel: ChatGPT, Grok, Gemini, DeepSeek — Claude
dropped, matching `!91`'s 20 Aug precedent (Scott's call).

Two brand-new chats per site (never both pastes in one chat), tools left at
site defaults (no toggle exists to disable a browser chat's backend tools),
first reply taken as-is, graded by `calib/rule.py` against
`GOVERN2_ANSWERS` — not by eye.

**Correction, recorded because it matters more than the result:** the first
pass at this run recorded both Gemini arms as non-response after 45+ and 8+
minute waits with no visible streamed text, and I stopped the generation
manually in both chats. That was wrong — Scott went back to the same prompts
directly afterward and both arms answered cleanly. Gemini's Flash-Lite mode
gives no visible stream and appears empty right up until it finishes all at
once (the same behavior already on record from the 20 Aug `!91` run); an
empty read mid-generation is not evidence of a hang, and I acted on it as if
it were. The corrected results below are Scott's re-runs, graded the same
way as everything else here.

## Per-site outcome

| Site | Semantic | Algorithmic | Paired? |
|---|---|---|---|
| ChatGPT | VOID — self-declared holding tools (web, python, image_gen, etc.), stopped per kernel rule | VOID — same, confirmed twice (once here, once on Scott's independent retry) | No — site cannot host a sterile run |
| Grok | BOUND 6/6 | BOUND 6/6 | Yes — both arms usable, both correct |
| Gemini | BOUND 6/6 (Scott's re-run) | BOUND 6/6 (Scott's re-run) | Yes — both arms usable, both correct |
| DeepSeek | BOUND 6/6 | **NOT BOUND 3/6** — E, F, I misrouted to NONE | Yes — both arms usable, but disagree |

Raw replies: `reply_<site>_<arm>.md` in this folder. Graded via:
```
python3.12 calib/rule.py offboard/bigger_occupant_results/reply_grok_semantic.md calib_govern2
python3.12 calib/rule.py offboard/bigger_occupant_results/reply_grok_algorithmic.md calib_govern2_b
python3.12 calib/rule.py offboard/bigger_occupant_results/reply_deepseek_semantic.md calib_govern2
python3.12 calib/rule.py offboard/bigger_occupant_results/reply_deepseek_algorithmic.md calib_govern2_b
python3.12 calib/rule.py offboard/bigger_occupant_results/reply_gemini_semantic.md calib_govern2
python3.12 calib/rule.py offboard/bigger_occupant_results/reply_gemini_algorithmic.md calib_govern2_b
```
All six appended to `calib/LEDGER.md`.

## Verdict against the job's own pre-registered gate

`JOB_bigger_occupant.md`: "Minimum 3 sites where BOTH arms are usable. Below
3 paired sites, the comparison is inconclusive — say so and stop."

**3 paired sites (Grok, Gemini, DeepSeek) — the floor is met.** A comparison
can be reported. ChatGPT stays unpaired: confirmed twice now that it cannot
disable its backend tools well enough to run this job at all.

## What the data shows — sites mostly agree, one disagrees, and that split is the finding

The job doc names this explicitly as its own most-interesting outcome case:
*"Sites disagreeing with each other — also a finding, and a more interesting
one. Record it; do not average it away."*

- **Two of three paired sites (Grok, Gemini) held both representations
  perfectly** — 6/6 on both arms, identical routes and verdicts item for
  item. For these two sites, representation made no measurable difference.
- **DeepSeek's algorithmic arm broke on exactly the three items that require
  reading past a single labelled sentence** — E and I are completed-build
  claims where the SCOPE line for LAW 2 ("a completed build claim runs Law 2")
  sits right next to the SCOPE line for the "pure finding" NONE case, and F is
  the LAW 3 construction-plan item. DeepSeek's algorithmic reply quoted the
  SCOPE sentence itself as evidence for all three ("A completed build claim
  runs Law 2." / "A multi-step construction plan runs Law 3...") but then
  routed them to NONE anyway — it read the governing rule correctly and
  applied it wrong. Its semantic-arm reply on the same three items used
  claim-specific evidence (the RETRY_MAX line, the paired-steps line, the
  empty-queue log line) and routed all three correctly.
- **Reading across all three paired sites: representation does not matter
  most of the time, but when it fails, it fails toward the algorithmic
  form.** No site did the reverse (semantic breaking where algorithmic held).
  n=1 disagreement out of 3 paired sites is thin, but it is a real,
  consistent-direction defect, not noise — and the ceiling'd local run
  (both arms 6/6 on gemma4:12b-it-qat) could never have shown it.

## What this does not show

- Not evidence that algorithmic representation fails broadly — 2 of 3 paired
  sites show zero difference. This is a single-site defect, directionally
  consistent, not a general representation ranking.
- Not evidence ChatGPT "cannot" bind — its VOID outcome is a tool-declaration
  finding specific to this job's sterile-run requirement, not a claim about
  ChatGPT's ability to apply the Laws under other conditions.
- Not evidence about wording alone — per the job doc's standing caveat, the
  algorithmic form is also shorter and differently packaged; this run cannot
  separate wording from packaging even within the sites that answered.

## Next step, if `!95` reopens

The job's escape hatch — "both arms 6/6 everywhere, the next move is a
harder probe" — does not apply; DeepSeek's split shows this probe still has
headroom and found a real defect. The open thread is whether DeepSeek's
algorithmic failure replicates on a second fresh pair (n=1 today) or was a
one-off, and whether a fourth or fifth paired site (retrying ChatGPT with a
different tool-disable approach, or adding a site outside this panel) pushes
the "algorithmic fails toward NONE" pattern from suggestive to demonstrated.
