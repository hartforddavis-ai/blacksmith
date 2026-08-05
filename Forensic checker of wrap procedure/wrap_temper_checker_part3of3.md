# WRAP/TEMPER FORENSIC CHECKER — PART 3 of 3 — baseline 2026-07-29

Final part of the 3-part bundle. Same evidence rules and scope as part 1
apply. This part covers known failure points, open unknowns, and the
required output format — produce your report only after this part.

## KNOWN FAILURE POINTS AS OF BASELINE (re-verify each)

F1 [enforcement-gap, OPEN] — claims-gate checks evidence-field FORMAT, never
  truth (`memory.py` `_check_claims`, ~L706-749). A fabricated CONFIRMED line
  passes identically to a real one.
F2 [bypass-path, OPEN] — `git add/commit/push` remain allowlisted Bash
  commands in settings.json; nothing code-level stops mid-session commits
  despite wrap's prose "NO COMMITS" rule. `project_mara.md` (22 Jul) names
  this explicitly as undefended ("nothing external stops this — the
  discipline is the stop").
F3 [dead code, CONFIRMED] — `brain_sync.py`'s `checkpoint()` (docstring:
  "every turn boundary, Stop hook") is only reachable via CLI arg
  `checkpoint`; settings.json's Stop hook array contains only
  `gate_check.py`. **Confirmed unwired** — re-check settings.json hasn't
  changed.
F4 [redundant entry point, OPEN] — `commands/stop.md`/`stop.sh` still
  implement a materially weaker session-end path alongside wrap.
F5 [Wrap/Temper separation gap, OPEN] — Temper has zero executable form;
  enforcement is a nudge + a self-written claims line. Violates the
  project's own stated principle ("anything that must hold regardless runs
  as a tool, not a line").
F6 [in-progress mitigation, NOT A BLOCKER] — Assay exists and targets F1/F5
  directly but is confirmed NOT wired into wrap yet (`project_assay.md` Open
  items). **This is the field most likely to have changed — check first.**
F7 [sweep accuracy, NOT A BLOCKER, edge-case] — mtime-based `.last_sweep`
  sweep misreports inside a git worktree checkout (documented incident, 21
  Jul, not fixed at the mechanism level).
F8 [config drift, ASSUMED, low severity] — `MARA_FLOOR` env var / old
  `floor_terminal.md` / `mara_load.py` machinery referenced in TODO.md's 10
  Jul entry; `mara_load.py` confirmed deleted 12 Jul per `project_mara.md`.
  Current live use of `MARA_FLOOR` is unconfirmed — grep `skills/`, `hooks/`,
  `settings.json` for it each run.

## UNKNOWN AT BASELINE (close these if you can)

- Role of `cache/changelog.md` (474KB) and `cache/my-closed-issues.json`
  relative to Wrap/Temper — grep hit only ("temper" mentioned), never opened.
- Whether `~/.claude/backups/` relates to Wrap/Temper recovery — no
  reference found tying it in; likely unrelated but not confirmed.
- Whether the historical 3-redundant-commit incident's hashes
  (`a6d24bb`/`0bbab00`/`c4ee8d2`) are still present in `git log` or were
  rebased away — not checked against current history.
- Full top-to-bottom TODO.md "Marrow / Mara consolidation" section — only
  grep hits and one excerpt were reviewed, not the whole file.

## OUTPUT FORMAT

Reuse these headings only: SYSTEM MAP, EVIDENCE INVENTORY, EXECUTION TRACE,
TEMPER DISCIPLINE MAP, TEMPER IMPLEMENTATION GAP, CONTROL BOUNDARY MAP, STATE
MODEL, LOOP MODEL, DEPENDENCIES, FAILURE POINTS, UNKNOWN ITEMS, NEXT EVIDENCE
REQUIRED, then a FINAL MACHINE RECORD block:
EXTRACTION_STATUS / FILES_INSPECTED / COMMANDS_RUN / UNKNOWN_COUNT /
TEMPER_STATUS / READY_FOR_TEMPER_REVIEW. Lead every section with **DRIFT:**
lines for anything that no longer matches this baseline, before restating
what's unchanged. A missing fact is better than a plausible answer — do not
carry a baseline claim forward without re-reading its cited file this run.

[END PART 3 of 3 — all parts loaded, produce the report now]
