# WRAP/TEMPER FORENSIC CHECKER — PART 2 of 3 — baseline 2026-07-29

Continuation of the 3-part bundle. Same evidence rules and scope as part 1
apply here — do not restart the ruleset, just keep applying it. This part
covers the execution trace, the control-boundary classification, and the
state model.

## EXECUTION TRACE (one wrap cycle)

START → Scott says "wrap" this turn (prose gate, `wrap/SKILL.md`) →
`python3.12 ~/.claude/tools/memory.py wrap start`:
  - lists `project_*.md` changed since `.last_sweep` mtime (self-heals to epoch
    if marker absent — `memory.py:559-572`)
  - runs `cmd_lint` as a **preview only** (report, not gate)
  - `_boundary_check()`: probes ollama/brew/netstat/tailscale/ssh-keys, diffs
    against last snapshot, **unconditionally overwrites** `wrap_boundary.json`
    even if `wrap finish` never runs
  - truncates+rewrites `cache/wrap_claims.md` to just the header
  - writes `cache/wrap_started` (the pair-check anchor)
↓ AI judgement, no code enforcement: (1) Temper deep pass if a deliverable
  changed, (2) Save — edit TODO.md/MEMORY.md/project_*.md by hand, (3) Learn —
  optional floor.md/SKILL.md edit, gated only by the harness's normal
  permission prompt (Edit is allowlisted **only** under `.../memory/**`) →
  the AI free-writes STATE|what|evidence lines into `cache/wrap_claims.md`
  as it goes
↓ `python3.12 ~/.claude/tools/memory.py wrap finish [session-id]`:
  - refuses (exit 1) if `wrap_started` is missing or `.last_sweep`'s mtime
    moved since `start` (pair-check, `memory.py:756-771`)
  - `_check_claims`: refuses if claims file is missing/empty, has an
    unrecognized STATE, a CONFIRMED line with no 3rd field, or a tripwire
    boundary-move with no matching SECURITY line — **this validates FORMAT
    of the evidence field, never its truth**
  - `cmd_index` regenerates MEMORY.md/COLD.md; `cmd_lint` re-runs as a **gate**
    this time — dirty lint (any `✗`) stops everything, marker not advanced,
    transcript kept
  - on clean lint: advances `.last_sweep`, resolves session id from argv or
    `$CLAUDE_CODE_SESSION_ID`, deletes exactly that one `<id>.jsonl` (refuses
    glob/traversal/empty ids), removes `wrap_started`
↓ **No git action anywhere in this trace.** `wrap/SKILL.md` explicitly forbids
  `git add`/`commit`/`push` inside wrap — that happens only at true
  SessionEnd, via `hooks/brain_sync.py push()` (separate hook, separate
  process, runs after wrap's transcript delete).
SESSION END → `brain_sync.py push` (commit_local → `staged_is_safe()` allow/
  deny check → commit → rebase_pull → push) and `lean_spend_log.py`
  (independent), both fail-open.

## CONTROL BOUNDARY MAP

DETERMINISTIC (verify each still holds):
- wrap_finish's pair-check (start-before-finish, marker-unmoved)
- wrap_finish's claims-format gate (state keyword valid; CONFIRMED has *a*
  evidence string; SECURITY line count matches tripwire-moved count)
- wrap_finish's lint gate (structural drift only: orphans, dead/dangling
  links, missing frontmatter, floor schema/guard drift, duplicate `!N` ranks)
- transcript delete: single named file, id validated against `/`, `*`, `..`
- `brain_sync.staged_is_safe()`: independent allow/deny recheck of every
  staged path before auto-commit, regardless of `.gitignore` correctness
- `gate_check.py`'s two BLOCK paths (self-certification tells structurally
  tied to an unverified product edit; memory-drift once/session), capped at
  `BLOCK_CAP=3`, filesystem-persisted independent of the harness's own
  `stop_hook_active` flag
- harness permission gate: any Edit/Write outside
  `Edit(//…/memory/**)` requires interactive approval (covers floor.md/
  SKILL.md edits; does **not** cover project_*.md dossier edits, which sit
  inside the allowlist even though they can contain "content decisions")

ADVISORY (prose/discipline only — verify nothing has silently become code):
- whether "wrap" was genuinely Scott-triggered (no code check)
- whether Temper actually happened, and whether it was done well — pure
  self-report; per `project_assay.md`'s own "Durable design decision":
  *"Assay never executes anything, so it cannot verify the truth of a prose
  claim"* — i.e. the system's own docs state this is unverifiable by design,
  pending Assay's (still unwired) integration
- the "Learn" step's judgement of what's durable
- all of `gate_check.py`'s non-blocking nudges (Temper/memory/session/
  cache-miss/recap) — text the AI can read and ignore
- "ONE PASS, don't halt between steps" — prose, nothing prevents stopping

## STATE MODEL

Authoritative: TODO.md + project_*.md dossiers (git-tracked, hand-edited,
schema-checked only structurally by `lint`, never semantically).
Temporary: `cache/wrap_started`, `cache/wrap_boundary.json`,
`cache/wrap_claims.md`, `cache/gate_blocked/*` — all outside
`brain_sync.py`'s `ALLOW_PREFIXES`, so never auto-committed; confirm they're
still `.gitignore`d.
Generated: MEMORY.md catalog + WHERE-WE-ARE block, COLD.md — splice-regions
only, convention (not code) says "never hand-edit."
Human-controlled: skills/floor.md edits (code-gated via permissions);
"content decisions" more broadly (prose-gated only, per floor.md's
`alwayson` rule).
Recovery: git history only (`auto-sync <ts> (<host>)` commits at SessionEnd).
No Wrap-specific snapshot/backup mechanism found in scope.

[END PART 2 of 3 — paste part 3 next]
