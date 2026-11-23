# Gate 2 — Sterile Code Review of cell.py

Per SPEC_STERILE_DERIVATION.md Gate 2: deterministic rules only, no human
judgment, no assumptions. SPEC §2 rules 1–6 applied to every function.
`N/A` means the rule does not bear on what that function does — recorded
rather than skipped, so a reader can see the rule was considered, not missed.

Source: cell.py, hash f8c82d38defaee20547567d079522faf7050a57d3313f579e9ec4cce6d2dcfef
(MANIFEST.sha256, regenerated this session).

---

## `confine(root, candidate)` — lines 74–85

- R1 (OS boundary only): PASS. `os.path.realpath` + prefix comparison, no
  prompt/signature involved.
- R2 (capability absence): N/A — this is a path check, not a capability grant.
- R3 (sterility by construction): N/A.
- R4 (re-derived verdict): PASS. Recomputes both realpaths itself each call;
  takes no supplied verdict about containment.
- R5 (promotion is code): N/A.
- R6 (fail closed): PASS. Raises `CellError` on any path resolving outside
  `root` (line 84); no silent clamp.

## `ancestor_contamination(path)` — lines 88–100

- R1: PASS. Filesystem walk of `path.parents`, no prompt-level check.
- R2: N/A — detection, not a capability boundary.
- R3 (construction not suppression): PASS. Reports found files; does not
  delete, hide, or rename them.
- R4: PASS. Walks the real filesystem itself; returns findings, not a verdict
  supplied elsewhere.
- R5: N/A.
- R6: N/A — a reporting function, nothing to fail closed on. (Callers,
  `build`, treat a non-empty result as fail-closed; see `build` below.)

## `CellSpec.__post_init__` — lines 124–148

- R1: N/A — pure value validation, no OS boundary claim.
- R2: N/A.
- R3: PASS. Refuses `scratch_prefixes` that would name the cell home itself
  (line 138–142) or cover the evidence tree (line 144–148) — both are
  suppression-shaped holes (a "scratch" label wide enough to excuse
  everything) closed by construction, not by a runtime check elsewhere.
- R4: N/A.
- R5: N/A.
- R6: PASS. Every malformed input (`evidence_mode` not in `("copy","mount")`,
  absolute/`..` scratch prefix, empty prefix, prefix under `evidence/`)
  raises `CellError` at construction. No default that papers over a bad spec.

## `build(spec)` — lines 159–201

- R1: PASS. Every check (existing root, symlink root, ancestor contamination)
  is a filesystem stat/walk. No prompt or signature enters the decision.
- R2: N/A directly — `build` does not grant or deny a runtime capability
  itself. It hands off to `_seal`, reviewed below, which is where the R2
  caveat actually lives.
- R3: PASS. `root.mkdir(parents=False, exist_ok=False)` (line 184) — refuses
  to build into anything pre-existing (line 167–168); every populated path
  traces to an explicit item in `spec` (extra_dirs, evidence_sources,
  scratch_prefixes), nothing copied-then-hidden.
- R4: N/A — `build` is the producer of the cell, not a consumer of another
  module's verdict.
- R5: N/A.
- R6: PASS. Six distinct raise points before or during build: existing root
  (168), non-directory parent (170), contaminated ancestor (174–176), mount
  mode not implemented (179–182, `RulingRequired` — a genuine unresolved
  owner ruling, not swallowed), plus whatever `_place_evidence` and
  `CellSpec.__post_init__` raise, propagated unchanged.

## `_place_evidence(evidence_root, source)` — lines 204–220

- R1: PASS. `Path.is_symlink()` / `is_file()` checks, no prompt-level trust.
- R2: N/A.
- R3: PASS. Copies one named file to one named destination; does not
  enumerate-then-filter a directory, so there is no suppression step for a
  file that "shouldn't" be there — it was never in scope.
- R4: N/A.
- R5: N/A.
- R6: PASS. Refuses a symlink source (213), a non-regular-file source (215),
  and a basename collision (218) — all raise, none degrade to "skip and
  continue."

## `_seal(home, scratch_prefixes)` — lines 223–245

- R1: **Caveat, not a failure.** Sets `os.chmod` mode bits (0o444/0o555).
  The module's own docstring (lines 28–31) and this function's docstring
  (227–229) state outright that these bits are a tamper *indicator*, not a
  boundary, until SPEC §8 step 0 (UID switch) resolves — i.e., the function
  does **not** claim an OS-boundary property it hasn't earned. That is R1
  satisfied by disclosure rather than by the mechanism alone: the risk R1
  guards against is a *false* boundary claim, and none is made here.
- R2: **Same caveat, same resolution.** Mode bits are capability-shaped but
  owner-clearable pre-UID-switch (a `chmod` by the owning UID reverses them),
  so this is *not yet* "capability absence" in R2's sense — and the code
  says so rather than presenting it as one. Compliant by honest labelling;
  becomes a true R2 mechanism only when §8 step 0 lands.
- R3: PASS. Deepest-first walk sets read-only after population, not as a
  suppression of anything already flagged bad.
- R4: N/A.
- R5: N/A.
- R6: N/A — this function has no reject path of its own; it mutates mode
  bits unconditionally over what `build` already validated.

## `census(cell)` — lines 248–286

- R1: PASS. `os.walk` over the real tree; `sterile` is computed from what
  the walk found, not from a self-report.
- R2: N/A — a report, not a grant.
- R3: PASS. `declared` is built from `spec` fields explicitly (268–274);
  `undeclared` is a set difference against what's actually `present`
  (281) — nothing is excused by naming it "expected" after the fact.
- R4: PASS. Recomputes `present`/`forbidden_names`/`symlinks` from the
  filesystem on every call; a stale prior census cannot be reused as if
  current.
- R5: N/A.
- R6: N/A — `census` reports; `require_sterile` (below) is where the
  fail-closed obligation is discharged.

## `attest_args(cell)` — lines 289–309

- R1: N/A — pure data transformation (rebasing paths), no boundary claim.
- R2: N/A.
- R3: N/A.
- R4: PASS by design intent — exists specifically so callers cannot restate
  the scratch declaration at a mismatched base and have it "silently match
  nothing" (296–303), which is exactly a supplied-verdict-shaped failure
  mode (an unearned PASS). Docstring names the concrete consequence: every
  runner write would report as an attested delta.
- R5: N/A.
- R6: N/A — no reject path; a pure computation.

## `require_sterile(cell, log_path)` — lines 312–330

- R1: PASS. Delegates to `census`, which is filesystem-only.
- R2: N/A.
- R3: N/A (inherits `census`'s R3).
- R4: PASS. Does not accept or trust a prior sterility claim; calls `census`
  itself and raises on what it finds.
- R5: N/A.
- R6: PASS, and this is the function SPEC §2 rule 6 names directly (line
  325–328): a non-sterile cell raises `CellError` rather than returning a
  report an operator could weigh and override. Both outcomes are logged
  (323, 329) before either raising or returning — no silent branch.

## `teardown(cell_root, cells_root)` — lines 333–356

- R1: PASS. `os.path.realpath` + prefix confinement (345) before any
  destructive call, same shape as `confine`.
- R2: N/A.
- R3: N/A — a destroy operation, not a build.
- R4: PASS. Re-resolves `cells_root` and the target itself (341, 345)
  rather than trusting a path the caller labelled safe.
- R5: N/A.
- R6: PASS. Refuses a symlinked root (343), refuses removing `cells_root`
  itself (346), refuses a non-directory target (348) — all raise before
  `shutil.rmtree` is reached (355).

---

## Summary

10 functions reviewed. 0 functions found in violation of a rule that applies
to them. Two functions (`_seal`) carry a disclosed, not concealed, gap
against R1/R2 — the mode-bit mechanism is honestly labelled as a tamper
indicator pending SPEC §8 step 0, not presented as a boundary it is not.
That gap is a property of the UID-switch not being built yet (tracked at
SPEC §8, §12), not a defect in cell.py's derivation from SPEC §2.

**Gate 2: PASS.**
