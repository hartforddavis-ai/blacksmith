# KERNEL — WIRE ONE GAUGE CHECK

Paste as the first message. Previous session ended 5 Aug 2026 (commit
756f2e6). This file points forward; read it first. Nothing else carries
over — read the cited files, not this file's paraphrase of them, where
they differ.

---

## STATE

SPEC.md is frozen — §11 has no open rulings, only DECIDED/DEFERRED. The
bound-occupant pivot works end to end: `occupant_bound.py` calls a local
clean model over HTTP (no `claude` CLI spawn, so ASSUMPTIONS.md #23 does
not apply to it), the response is staged into the content-addressed store,
and a real run produced `attest.compare()` = **INTACT** with zero deltas.

That proves the pipe is clean. It does not prove the pipe is checked.
`gauge.adjudicate()` on that run returned **UNKNOWN** — correctly: the
smoke test populated only one of `contract.json`'s four required checks
(`no_generator_write_to_checker_tree`, via `attest.as_check`). The other
three, and the pinned `runner_id`, were left genuinely unmet rather than
faked. Full record: `runs/pivot_smoke.qwen3.5-9b.20260805T091739.md`.

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

Wire **one** required check — `artifact_hash_matches_manifest` — into a
future pivot run's evidence bundle. Named as the cheapest of the four to
make honestly true, not pre-decided as the mechanism:

- `store.py`'s `ObjectStore` is content-addressed: an object's id *is* its
  sha256, and the store re-hashes on every `get()`. Read `store.py` before
  assuming what "matches manifest" should mean here — there may already be
  a re-derivation path this check can lean on rather than duplicate.
- Apply Law 1 to whatever mechanism you land on before writing it: what F
  does it close, is it the smallest of the alternatives, does it introduce
  a second hashing path gauge's own docstring warns against.

The other three required checks (`runner_integrity_verified`, `tests_pass`,
and the pinned `runner_id`) stay unmet. Do not wire more than one in this
pass — SPEC's own Law 3 (construction) scope is one step, ordered on what
already passed, not several at once.

## NOT YOURS

Do not revisit SPEC §11's rulings — they are DECIDED or DEFERRED, not
open. Do not re-run the bound-evaluation track (`CONTEXT_next_session.md`,
`KERNEL_execute.md`) from this file — that is a separate, parallel thread
in this project; this kernel is the redesign/pivot line only.
