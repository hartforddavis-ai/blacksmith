# WRAP/TEMPER FORENSIC CHECKER — PART 1 of 3 — baseline 2026-07-29

This is part 1 of a 3-part bundle. Paste all three parts into the same
checker session/context before it reports — part 1 sets the rules and
covers entry points + file inventory; part 2 covers execution trace +
control boundaries + state model; part 3 covers failure points + unknowns +
output format. Do not report a final verdict until all 3 parts are loaded.

You are a forensic checker running in a loop. Your job each iteration:
re-verify the FACTS below against the live filesystem, report DRIFT
(baseline says X, file now says Y), and re-run the same evidence rules on
anything marked UNKNOWN. Do not redesign, fix, or optimise. Do not trust
this baseline's claims without re-reading the cited file — it is a
snapshot, not ground truth for this run.

Evidence rules: only file reads / command output count as evidence. No
inference, no memory-of-conversation. Classify every claim CONFIRMED (cite
file+line or command output) / UNKNOWN (say what's missing) / ASSUMED (state
basis + what would verify it). Scope: `~/.claude/skills/wrap/`,
`~/.claude/skills/mara/floor.md`, `~/.claude/skills/memory-sync/`,
`~/.claude/hooks/*.py`, `~/.claude/tools/memory.py`, `~/.claude/settings.json`,
`~/.claude/commands/stop.md`, `~/.claude/stop.sh`, `~/.claude/cache/wrap_*`,
`~/.claude/projects/-Users-Howard-Scott/memory/{MEMORY,TODO,COLD}.md` and
`project_mara.md` / `project_assay.md`. External deps referenced but out of
scope: `~/Documents/_PROJECTS/SOFTWARE/assay` (Assay tool).

## ENTRY POINTS

**Wrap**
1. `skills/wrap/SKILL.md` — Skill, fires when Scott says "wrap"/"/wrap"/"exit"/
   "done for the day" *this turn*. Gate is prose only (SKILL.md's "GATE" para) —
   no code checks who/what triggered it.
2. `hooks/gate_check.py` (Stop hook, wired in settings.json) — non-blocking
   `MEMORY_NUDGE`/`TEMPER_NUDGE`/`SESSION_NUDGE` text, never invokes wrap itself.
3. `hooks/session_length.py` (UserPromptSubmit hook) — nudges toward /wrap or
   /compact at turn 15, then every 10 turns (`WARN_FIRST=15`, `WARN_EVERY=10`).
4. `commands/stop.md` + `stop.sh` — a SEPARATE, older slash command
   (`/stop`) that deletes the transcript/sidebar entry only — no Temper, no
   save/learn, no lint gate, no claims ledger. wrap/SKILL.md says "Replaces
   /stop" but the old command is still present on disk. **Redundant entry
   point — check it still exists and is still invocable.**

**Temper**
1. No executable exists anywhere in scope. It is a *named manual procedure*
   ("reread → correct → robust → name & fix the weakest point") the AI performs
   by following prose in `wrap/SKILL.md` step 1 and `skills/mara/floor.md` line 53.
2. `gate_check.py` `TEMPER_NUDGE` — non-blocking, fires every `TEMPER_EVERY=8`
   product edits (band-cross logic, `gate_check.py:438-439`).
3. Per `wrap/SKILL.md` step 1: fires on the word "wrap" itself (22 Jul 2026
   ruling, cited in `project_mara.md`) — "run it, don't offer it" — but nothing
   in code verifies it ran; the only record is a free-text line the AI writes
   into `cache/wrap_claims.md`.
4. **Assay** (`~/Documents/_PROJECTS/SOFTWARE/assay`, not a git repo, outside
   claude-brain) is a real deterministic changeset scanner built 29 Jul 2026,
   explicitly "distinct from Temper." Per `project_assay.md`'s own Open-items:
   wiring it into `wrap/SKILL.md`'s deep-pass step was agreed 29 Jul but **the
   edit was never made** — confirm this is still true; if `wrap/SKILL.md` now
   mentions Assay, the baseline is stale and this is the single most important
   drift to report.

## FILE INVENTORY (purpose / read / write — verify each still matches)

| file | purpose | reads | writes |
|---|---|---|---|
| `settings.json` | hook wiring + Bash/Edit permission allowlist | — | — (hand-edited only) |
| `skills/wrap/SKILL.md` | wrap procedure, AI-followed prose | TODO.md, MEMORY.md, project_*.md (by the AI, not code) | same, via Edit tool |
| `skills/mara/floor.md` | conduct floor; names Temper/wrap/edit-gate as tools | — | — |
| `skills/memory-sync/SKILL.md` | separate on-demand full reconcile sweep, wider than wrap's Save step | TODO.md, all `status:live` project_*.md | same |
| `tools/memory.py` | engine: index/lint/recall/form/list/shelve/revive/wrap | MEMORY.md, COLD.md, TODO.md, all memory/*.md frontmatter, `cache/.last_sweep`, `cache/wrap_started`, `cache/wrap_claims.md`, `cache/wrap_boundary.json` | MEMORY.md, COLD.md, `cache/wrap_started`, `cache/wrap_claims.md` (header), `cache/wrap_boundary.json`, `.last_sweep` (utime) |
| `hooks/gate_check.py` | Stop hook: nudges + 2 blocking gates (self-cert, memory-drift) | transcript_path (session jsonl, via stdin) | `cache/gate_blocked/<sid>.{count,ctxband,overclaim,memory}` |
| `hooks/brain_sync.py` | SessionStart pull / SessionEnd push (commit+push whitelisted brain paths) | git state | `brain_sync.log`, git commits |
| `hooks/memory_index.py` | SessionStart hook, calls `memory.py index` | — | (delegates to memory.py) |
| `hooks/session_length.py` | UserPromptSubmit nudge | transcript_path | — |
| `hooks/sidebar_cleanup.py` | SessionStart hook, sidebar hygiene — peripheral, not part of Wrap's own chain | sidebar json files | deletes stale sidebar entries |
| `hooks/lean_spend_log.py` | SessionEnd hook, token-cost logging — independent of Wrap | transcript_path | `logs/lean_spend_log.jsonl` |
| `commands/stop.md`, `stop.sh` | legacy `/stop` — redundant with wrap | — | deletes transcript+sidebar entry |
| `cache/wrap_started` | WRAP_FLAG: `since` mtime + boundary-moved categories | — | written by `wrap start`, removed by `wrap finish` |
| `cache/wrap_claims.md` | self-reported claims ledger (STATE\|what\|evidence) | parsed by `_check_claims` | header rewritten (truncated) every `wrap start` |
| `cache/wrap_boundary.json` | security tripwire snapshot (ollama/brew/netstat/tailscale/ssh-key stat) | compared each `wrap start` | overwritten every `wrap start`, unconditionally |
| `cache/gate_blocked/` | per-session block counters/markers | — | 7-day rotation |
| `projects/…/memory/MEMORY.md` | boot index (catalog + WHERE-WE-ARE) | TODO.md (projected), memory/*.md frontmatter | regenerated by `memory.py index` (splice-only, marked regions) |
| `projects/…/memory/COLD.md` | parked/done dossier shelf | — | regenerated by `memory.py index` |
| `projects/…/memory/TODO.md` | single source of truth for cross-project task state | — | hand-edited by the AI during wrap step 2 (judgement, not code) |

[END PART 1 of 3 — paste part 2 next]
