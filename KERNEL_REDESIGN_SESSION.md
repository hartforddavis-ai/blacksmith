# KERNEL — REDESIGN SESSION 2

Paste as the first message. Previous session ended 5 Aug 15:41. This file points forward; read it first.

---

## STATE

**Evaluation run died.** qwen3.5:9b hung at 61 minutes; zero output. Verify run (same model) returned UNFIT with fabricated verdicts. Both runs discarded.

**Hand ruling applied.** Scott read the 34-row BLACKSMITH_REDESIGN.md and applied Law 1:
- 4 APPROVE (bootstrap, evidentiary hole, no redundancy, naming collision)
- 2 FREEZE (interval blindness, memory migration)

**Findings 3 & 4 decided by Scott** (Law 1):
- **Finding 3 (interval blindness):** No live monitor. Record execution states in evidence log. Bound code logs what happens; all states captured deterministically.
- **Finding 4 (verified-memory migration):** No separate migration system. Migration is recorded in evidence log. Bound code performs it deterministically; all steps logged.

**Naming collision resolved.** Assay is now "one algorithm" per Scott; no renaming needed.

**Redundancy verified.** Bundles are triple-redundant: Git (remote) + local Mac + Time Capsule. Mirroring spec rejected under Law 1 (F not demonstrated).

---

## SPECIFICATIONS WRITTEN

All pass Law 1. Live and ready:

```
SPEC_STERILE_DERIVATION.md       4 gates (source, review, build, hash)
SPEC_EVIDENCE_LOG_SCHEMA.md      formal proof chain schema
SPEC_BUNDLE_MIRROR.md            (rejected under Law 1; redundancy exists)
```

---

## DECISION MAP — WHAT IS STILL OPEN

Nothing. All findings ruled. All specs written. All decisions made.

**Next action:** Execute the three approved fixes:
1. Re-derive cell.py through sterile gates (Spec 1)
2. Formalize evidence log as proof chain (Spec 2)
3. (Bundle mirror rejected; no action needed)

---

## BUILD ORDER

Per Scott's original ruling:
1. ✓ Freeze finding 4 (migration scope) — decided via evidence log
2. ✓ Rule finding 3 (monitor cost) — decided via evidence log
3. ⏳ Fix findings 1, 2, 5, 6 in parallel (pending execution)
4. Then proceed to construction

---

## OUTSTANDING — UNWRITTEN

None. All decisions logged. All specs written. No gaps remain.

---

## GIVEN

- CLEAN MODELS ONLY: gemma4:12b, gemma4:12b-it-qat, qwen3.5:9b
- Nothing from FAILURE_LOG is revived
- Verdict before edit, per part
- Do not tune parameters to force results
- Report what checks show; do not repair the ruling

---

## LESSONS FROM SESSION 1

- Bounded evaluation (verify + evaluate) both failed. Instrument is broken.
- Hand-reading of the ruling by Scott works and is faster.
- Evidence log is the answer to both findings 3 & 4.
- Redundancy was already solved (Git + Time Capsule); mirroring was unnecessary.

---

## SESSION 2 — CLOSED, 5 Aug 2026

Both approved fixes executed, Law 1 applied per part before each edit.

```
Spec 1 (cell.py, sterile derivation) — GATE_STERILE_DERIVATION_cell.md
  Gate 1  PASS  inline in cell.py's own docstring, no new file
  Gate 2  PASS  GATE2_CELL_REVIEW.md — 10 functions × SPEC §2 rules 1-6
  Gate 3  PASS  test_cell_sterility.py 28/28; full suite 152/152
  Gate 4  PASS  MANIFEST.sha256:cell.py, f8c82d38... (unchanged — cell.py
                itself was not edited, only verified)

Spec 2 (evidence log proof chain) — evidence_log.py, test_evidence_log.py
  Built as a schema-enforcing renderer: 5 required sections, every field
  mandatory, refuses a partial entry. Does not adjudicate — verdict field
  is gauge's, taken verbatim.
  NOT wired into run_bound.py. Law 1 REJECT on that wiring: run_bound.py's
  Ollama calls run with no cell around them, so three of the five required
  fields (evidence_mode, cell pre/post-hash, verdict) have no honest value
  to supply yet. Building the module was still APPROVE; connecting it to
  a runner that can't fill it honestly was not.

MANIFEST.sha256 regenerated twice this session (stale both times from new
Ring 0 files — build_paste.py/watch_bound.py first, then evidence_log.py).
16 files, current.

Bundle mirror — no action, per session 1's ruling.
```

**Next action:** None open from this kernel.

## SESSION 3 — bound-occupant pivot, 5 Aug 2026

The gap this file flagged above (evidence_log sits unused until a run goes
through a cell) is closed. Built `occupant_bound.py` — a Ring 1 occupant
that calls a local clean model over HTTP instead of spawning the `claude`
CLI, sidestepping ASSUMPTIONS.md #23 (the CLI's own startup writes to
`$HOME/.claude`, which a sealed cell refuses) because no local process is
spawned at all. SPEC §11 ruling 3 also reversed this session: evidence
into the cell is a copy, not a read-only mount — local execution is the
constraint, and a mount's `hdiutil` lifecycle is complexity against a
tampering failure never demonstrated in this tree.

Ran the pivot end-to-end: sterile cell (built outside the home tree —
`cell.py`'s ancestor-contamination check flags the home directory itself,
since `~/.claude` lives there) → pre-attest → real streamed call to
`qwen3.5:9b` → response staged into the content-addressed store →
post-attest → `attest.compare()` returned **INTACT**, zero deltas →
`gauge.adjudicate()` against an honestly partial bundle (3 of 4 required
checks and the pinned runner id left unmet on purpose) returned
**UNKNOWN**, not a fabricated ACTIVE → cell torn down → first real
`evidence_log.py` entry written: `runs/pivot_smoke.qwen3.5-9b.20260805T091739.md`.

MANIFEST.sha256 regenerated (17 files, current). Full suite 158/158.

**Next action, if scaling up:** wire one real check into the gauge bundle —
`artifact_hash_matches_manifest` is the cheapest to make honestly true
against what a run just staged — so a future run moves off UNKNOWN with
real evidence instead of more absence.

## SESSION 4 — first real check wired, 5 Aug 2026

`artifact_hash_matches_manifest` closed. Added `store.as_check(store,
object_id)`: renders `get()`'s existing re-hash-on-read into gauge's
CHECK_OUTCOMES rather than hashing a second time — the same shape as
`attest.as_check`, so the tree now has two I/O modules each rendering their
own guarantee into gauge's vocabulary instead of gauge doing any I/O itself.
PASS on an intact staged artifact; FAIL on missing, tampered-after-staging,
or malformed ids. No UNKNOWN branch — a store lookup only ever succeeds or
raises, so none was manufactured. Four tests, each tied to a named failure
(SPEC's adversarial-harness row 159 names "tampered manifest" and
"missing-evidence-as-pass" directly). MANIFEST.sha256 regenerated. Full
suite 162/162. Commit `c6fc723`.

No pivot-bundle driver was built — nothing in this tree yet assembles
`bundle["checks"]` for a live pivot run; `pivot_smoke....md` was hand-run.
`store.as_check` is ready for that driver whenever it's built; building the
driver itself was out of scope for this pass (Law 3: one step).

**Next action:** `runner_integrity_verified` — `manifest.py` already
re-derives the Ring 0 tree's hashes and compares them to `MANIFEST.sha256`
(the `--check` flag does exactly this today). That's a re-derivation path
to lean on, same shape as `artifact_hash_matches_manifest` leaning on
`store.get()`, rather than a new one — named as the likely candidate, not
pre-decided as the mechanism. Full detail in `KERNEL_WIRE_RUNNER_CHECK.md`.
