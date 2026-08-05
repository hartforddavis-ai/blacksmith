# KERNEL — WIRE RUNNER INTEGRITY CHECK

Paste as the first message. Previous session ended 5 Aug 2026 (commit
c6fc723). This file points forward; read it first. Nothing else carries
over — read the cited files, not this file's paraphrase of them, where
they differ.

---

## STATE

`artifact_hash_matches_manifest` is closed: `store.as_check()` renders
`ObjectStore.get()`'s existing re-hash-on-read into gauge's CHECK_OUTCOMES,
mirroring `attest.as_check`. Four tests, each tied to a named failure. Full
suite 162/162. Full record: `KERNEL_REDESIGN_SESSION.md`, SESSION 4.

Two of four required checks are now honestly wireable:
`no_generator_write_to_checker_tree` (via `attest.as_check`) and
`artifact_hash_matches_manifest` (via `store.as_check`). Neither is
currently called from a committed bundle-assembly path — nothing in this
tree yet builds `bundle["checks"]` for a live pivot run. That driver does
not exist and was not built this pass; building it is a separate, larger
step than wiring a single check function, and Law 3 scopes to one step.

## GIVEN

```
G1  CLEAN MODELS ONLY: gemma4:12b, gemma4:12b-it-qat, qwen3.5:9b.
G2  Nothing in FAILURE_LOG.md is revived, restored, or extracted from.
G3  Verdict BEFORE the edit, per part — apply Law 1 to each check before
    wiring it, not after.
G4  gauge.py takes no I/O of its own (SPEC-stated constraint, see its own
    docstring). Whatever populates a check entry must do the file
    reading/hashing outside gauge and hand it a plain dict.
G5  Do not fabricate a check to move the verdict off UNKNOWN. An honest
    UNKNOWN is a valid outcome; a check that always reports PASS because
    nothing was actually compared is not a check.
```

## NEXT ACTION

Wire **one** required check — `runner_integrity_verified` — into the
gauge vocabulary. Named as the likely candidate, not pre-decided as the
mechanism:

- `manifest.py` already re-derives the Ring 0 source tree's hashes and
  compares them against `MANIFEST.sha256` — the `--check` flag does this
  today (`manifest.render(root) == MANIFEST.read_text()`). Read
  `manifest.py` before assuming this check should duplicate that logic
  rather than call it: the same "render an existing guarantee into
  gauge's vocabulary" shape that `attest.as_check` and `store.as_check`
  already use is the pattern to look for here first.
- "Runner" in SPEC and in contract.json's `runner_id` may or may not turn
  out to be the same thing `manifest.py` measures (the Ring 0 TCB:
  `cell`, `attest`, `launch`, `collect`, `gauge`, `promote` — SPEC §3).
  Confirm what "runner" denotes in this tree before wiring; do not assume
  it from this file's paraphrase.
- Apply Law 1 to whatever mechanism you land on before writing it: what F
  does it close, is it the smallest of the alternatives, does it
  introduce a second hashing path (`manifest.py`'s own docstring warns
  against a hand-maintained list going stale silently — check whether a
  new mechanism would reintroduce that class of drift).

The pinned `runner_id` and `tests_pass` stay unmet. Do not wire more than
one in this pass — SPEC's own Law 3 (construction) scope is one step,
ordered on what already passed, not several at once. Note, but do not act
on without deciding fresh: `runner_id` may turn out to be cheap once
`runner_integrity_verified`'s mechanism is chosen (e.g. a root hash
derived from the same re-derivation path) — or may not. That is a
separate call for the session that reaches it.

## NOT YOURS

Do not revisit SPEC §11's rulings — they are DECIDED or DEFERRED, not
open. Do not re-run the bound-evaluation track (`CONTEXT_next_session.md`,
`KERNEL_execute.md`) from this file — that is a separate, parallel thread
in this project; this kernel is the redesign/pivot line only. Do not build
the pivot-bundle-assembly driver as part of closing this check — that is
the step after this one, not this one.
