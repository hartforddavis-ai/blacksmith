# KERNEL — TESTS_PASS INTEGRITY CHECK

Paste as the first message. Previous session ended 5 Aug 2026 (commit
4aadb3f). This file points forward; read it first. Nothing else carries
over — read the cited files, not this file's paraphrase of them, where
they differ.

---

## STATE

`runner_integrity_verified` is closed: `manifest.as_check()` renders
`manifest.py`'s existing `render()` vs `MANIFEST.sha256` comparison into
gauge's CHECK_OUTCOMES, mirroring `attest.as_check` and `store.as_check`.
Three tests, one per branch. Full suite 165/165. Full record:
`KERNEL_REDESIGN_SESSION.md`, SESSION 5.

Three of four required checks are now honestly wireable:
`no_generator_write_to_checker_tree` (via `attest.as_check`),
`artifact_hash_matches_manifest` (via `store.as_check`), and
`runner_integrity_verified` (via `manifest.as_check`). Neither the pinned
`runner_id` nor a bundle-assembly driver exists yet — nothing in this
tree builds `bundle["checks"]` for a live pivot run. That driver is a
separate, larger step than wiring a single check function, and Law 3
scopes to one step.

## GIVEN

```
G1  CLEAN MODELS ONLY: gemma4:12b, gemma4:12b-it-qat, qwen3.5:9b.
G2  Nothing in FAILURE_LOG.md is revived, restored, or extracted from.
G3  Verdict BEFORE the edit, per part — apply Law 1 to each check before
    wiring it, not after.
G4  gauge.py takes no I/O of its own (SPEC-stated constraint, see its own
    docstring). Whatever populates a check entry must do the file
    reading/hashing/subprocess work outside gauge and hand it a plain
    dict.
G5  Do not fabricate a check to move the verdict off UNKNOWN. An honest
    UNKNOWN is a valid outcome; a check that always reports PASS because
    nothing was actually compared is not a check.
```

## NEXT ACTION

Wire the last required check — `tests_pass` — into the gauge vocabulary.
Named as the likely candidate, not pre-decided as the mechanism:

- The first three checks each leaned on a function that already existed
  and already re-derived its guarantee (`store.get()`'s re-hash,
  `attest.compare()`'s delta walk, `manifest.render()`'s hash comparison).
  Nothing in this tree currently runs the test suite and reports the
  result as data — that has to be built, not just rendered, which makes
  this check a different shape from the last three.
- Decide what "the suite" means before writing anything. Candidates:
  this tree's own `test_*.py` files (would make `tests_pass` a
  self-referential claim about Blacksmith's own correctness, close in
  spirit to `runner_integrity_verified`'s Ring 0 sealing — check whether
  that makes the two checks redundant before wiring a second one that
  answers a question already answered); or a generated artifact's own
  tests, if SPEC anywhere names artifacts as carrying tests. Read SPEC.md
  and ASSUMPTIONS.md for "test" before assuming either.
- If the mechanism does need to invoke `python3 -m unittest` (or similar)
  as a subprocess, that is I/O gauge itself must never perform (G4) —
  the subprocess call belongs in the same kind of module-level
  `as_check()` function as the other three, run by whatever assembles the
  bundle, never inside gauge.py.
- Apply Law 1 to whatever mechanism you land on before writing it: what F
  does it close, is it the smallest of the alternatives, does a
  subprocess-based check introduce nondeterminism or environment
  sensitivity that the other three (pure hash/file comparisons) don't
  have — and if so, is that cost worth what it closes.

The pinned `runner_id` stays unmet — separate from `runner_integrity_verified`:
gauge already checks `bundle["runner"]["id"]` against `contract["runner_id"]`
independently of the `checks` dict (gauge.py lines 105-108), and nothing
populates `bundle["runner"]` yet. Do not wire it as part of closing
`tests_pass` — SPEC's own Law 3 (construction) scope is one step, ordered
on what already passed, not several at once. Note, but do not act on
without deciding fresh: once all four required checks are wireable, the
bundle-assembly driver becomes the natural next step — or `runner_id`
might be cheap to close first, since a `LaunchPlan`'s `runner` dict already
carries most of what an `id` would need. That is a separate call for the
session that reaches it.

## NOT YOURS

Do not revisit SPEC §11's rulings — they are DECIDED or DEFERRED, not
open. Do not re-run the bound-evaluation track (`CONTEXT_next_session.md`,
`KERNEL_execute.md`) from this file — that is a separate, parallel thread
in this project; this kernel is the redesign/pivot line only. Do not build
the pivot-bundle-assembly driver as part of closing this check — that is
the step after this one, not this one.
