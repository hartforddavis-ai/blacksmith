# Adversarial review request — forensic-checker v2.4, round 6

## Your role

You are an independent adversarial security reviewer. A different AI model
(the "generator") built the Python library below and has already run five
rounds against it. You are being brought in as a second, independent set of
eyes specifically because the generator cannot fully audit its own work —
you have no stake in the code looking good.

Your job: **find real authority-boundary or verification-boundary gaps that
the existing 94-test suite does not already cover**, and prove each one with
a runnable Python 3.12 stdlib-only test or PoC script. Do not just theorize —
every claim you make must be backed by code that actually demonstrates the
failure when run.

If you look hard and find nothing beyond what's already documented, say so
plainly. A false "I found more gaps" claim is worse than an honest "I didn't
find anything new" — this project's own discipline (quoted from its source)
is: **"report the failure instead of creating a false guarantee."** Hold
yourself to that same standard when reporting results, in both directions.

## What this system is

A deterministic, stdlib-only Python verification boundary meant to gate an AI
generator's own output: untrusted claims go in, checker-verified evidence and
findings come out. It is NOT a linter or prose scanner — it's closer to a
capability-based authorization layer, structured as a pipeline:

`integrity → quarantine → scope → execution → evidence → findings → loop`

Full source for all 9 modules + the CLI entry point is in the Appendix below
— that's the entire system, ~1220 lines, nothing else exists outside it.

## History — five rounds so far

- **v2.0** shipped with 27 unit tests, all green.
- **Round 1 (internal adversarial pass):** 27 more tests, found 8 real
  authority-leak gaps (forged findings via `dataclasses.replace()`/direct
  construction, a launcher-binary argument escape, wholesale in-memory
  evidence-ledger replacement, forged findings entering loop history, an
  HMAC key as a plain readable attribute, plus variants).
- **v2.1 remediation:** closed 6 of the 8 with real code changes, kept 2 as
  honestly-documented residual limits (see below).
- **Round 2/3:** found 3 further gaps: (a) `LoopEngine` took a fresh
  `os.urandom(32)` key every run with no persistence, so the "loop" never
  chained across process invocations; (b)
  `quarantine.quarantine_claim()`'s return value was computed and then
  discarded in `engine.py`, decoupling the checked operation from the claim
  it was supposedly checking; (c) `ScopeGuard.validate_path` allowed
  `real == root`, letting a directory pass validation as a validated
  executable path.
- **v2.2 remediation:** closed all 3 (`loop.py` persistence, `execution.py`
  requiring a valid-format `claim_ingestion_hash`, `scope.py` requiring
  `os.path.isfile()`).
- **Round 4 (external adversarial pass):** found 2 further gaps: (a) the
  v2.2 quarantine-binding fix (`is_valid_ingestion_hash()`) was a *format*
  check only — any well-formed sha256 hex string, never actually produced by
  `quarantine_claim()`, satisfied it; (b) neither `EvidenceLedger` nor
  `LoopEngine` locked their append-only storage files, so concurrent writers
  (separate process/thread instances backed by the same `storage_path`)
  could each compute a hash/HMAC chain link from a `prev_hash`/`prev_digest`
  read before another writer's write landed, diverging the chain without any
  single write being physically torn.
- **v2.3 remediation:** closed both. `quarantine.QuarantineRegistry` now
  tracks hashes actually issued by `quarantine_claim()`; `AuthorisedExecutor`
  accepts an optional registry and requires `claim_ingestion_hash` to have
  been genuinely issued against it, not merely well-formed (`quarantine.py`,
  `execution.py`). `EvidenceLedger` and `LoopEngine` now perform
  read-current-tail → compute-next-link → write inside one `flock`-held
  critical section (`_filelock.py`, `evidence.py`, `loop.py`) instead of
  appending from a possibly-stale in-memory cache. Building the concurrency
  regression test surfaced a related bug along the way — `LoopEngine`'s
  `loop_secret.key` trust-on-first-use write had the identical
  unsynchronized-check-then-write race — closed the same way. Also found
  and closed in passing: `integrity.py`'s `PACKAGE_FILES` list never
  included the new `_filelock.py` module, so the checker's own
  self-integrity manifest silently didn't cover it — added.
- **Round 5 (external adversarial pass):** found 2 further gaps, both
  confirmed real: (a) `QuarantineRegistry` indexed issued claims by
  `ingestion_hash` alone, in a flat set — since `ingestion_hash =
  sha256(raw_payload)` carries no per-claim salt, two distinct claims
  (different `claim_id`) quarantining identical payload text produced the
  identical hash, making claim A's hash and claim B's hash mutually
  substitutable under `is_registered()`'s hash-only membership check; (b)
  neither `EvidenceLedger` nor `LoopEngine` synchronized their **in-memory**
  (no `storage_path`) append/record path at all — v2.3's locking only
  protected the file-backed branch, so a single instance shared across
  threads with no `storage_path` configured could still race two
  `append()`/`record()` calls against a stale `self._records`/`self._history`
  tail.
- **v2.4 remediation (just completed):** closed both.
  `QuarantineRegistry.register()`/`is_registered()` now track the exact
  `(claim_id, ingestion_hash)` pair rather than hash membership alone;
  `AuthorisedExecutor.run()` and `is_registered()` accept an optional
  `claim_id` — passing it requires the exact claim-to-hash binding, omitting
  it preserves the v2.3 hash-only fallback (`quarantine.py`, `execution.py`).
  `engine.py`'s real pipeline now passes the claim's own `claim_id`, fully
  closing the binding on the production path. `EvidenceLedger` and
  `LoopEngine` each gained a `threading.Lock` guarding their in-memory
  append/record branch specifically — the file-backed branch was already
  safe via `flock` and is untouched (`evidence.py`, `loop.py`).
- **Current state: 94/94 tests pass** (`python3 -m unittest discover -v`
  from the project root; stdlib `unittest` only, no pytest, no external
  packages — that constraint is load-bearing, don't suggest packages that
  violate it). New in v2.4: `TestQuarantineClaimIdBinding` (5 tests) in
  `tests/test_quarantine.py`, including the exact round-5 attack
  reproduced and now rejected; `TestInMemoryEvidenceLedgerThreadSafety` and
  `TestInMemoryLoopEngineThreadSafety` (2 tests) in `tests/test_concurrency.py`
  — 8 threads × 20 ops against one shared in-memory instance, asserting no
  errors and an unbroken chain/hmac with no duplicate or skipped sequence
  numbers.

**Do not re-report anything from rounds 1–5 above** (fixed with a regression
test) **or the residual limits below** (already documented as open). Your
value is in finding a **sixth thing** nobody has looked for yet.

## Known residual limits (already documented, NOT new findings)

1. **Integrity manifest is unsigned local JSON, trust-on-first-use.** An
   attacker who can write both source and manifest rebases trust onto
   tampered source. No external root of trust. (`integrity.py`)
2. **Secrets are same-process-introspectable.**
   `FindingAuthority._secret` is a plain attribute; `LoopEngine`'s HMAC key
   (in a closure) is still extractable via `__closure__` introspection.
   Inherent to a single-process, stdlib-only, no-external-secrets-store
   design.
3. **Filesystem-write-access forgery is out of scope for all four
   append-only/state files** (`evidence_ledger.jsonl`, `loop_history.jsonl`,
   `integrity_manifest.json`, `loop_secret.key`): `reload_and_verify()`
   defeats in-memory tampering, not a compromised disk.
4. **`flock` is advisory and local-filesystem-only.** It only serializes
   code paths that go through `_filelock.locked_open()`. Anything that opens
   `storage_path`/`key_path` directly (bypassing that helper) is not
   blocked, and advisory locks are not reliably enforced over network
   filesystems (NFS etc.). This build assumes a local disk and cooperating
   code — both stated design constraints, not new gaps.
5. **`QuarantineRegistry` is per-process and unpersisted**, unlike
   `loop_history.jsonl`/`evidence_ledger.jsonl`. It only provides a real
   guarantee because `engine.py` always quarantines and executes within the
   same process invocation. A caller wiring quarantine in one process and
   execution in another (nothing in this codebase does that today) would
   find every registry check trivially fails closed — safe by omission,
   not by design that's been exercised.
6. **The v2.4 claim-identity guarantee is opt-in at the call site, not
   structurally enforced.** `AuthorisedExecutor.run()`'s `claim_id`
   parameter defaults to `None`; a registry-configured executor called
   without it silently falls back to the weaker v2.3 hash-only check that
   round 5 demonstrated is insufficient against payload-collision. Nothing
   in `AuthorisedExecutor.__init__` requires that a registry-bearing
   executor's callers *always* supply `claim_id` — the strength of the
   guarantee depends entirely on every call site remembering to pass it
   (which `engine.py` does, but the API doesn't enforce it).

## Investigation leads (unconfirmed — verify, don't assume)

These are things I noticed reading the v2.4 diff that are **not** already
documented above and **not** covered by an existing test name I could find.
Treat each as a hypothesis to test, not a confirmed finding.

- **The new `threading.Lock` in `EvidenceLedger`/`LoopEngine` guards writers
  against each other, but the reader methods do not acquire it.**
  `EvidenceLedger.records()`, `.root_hash`, `.verify_chain()`,
  `.verify_against_checkpoint()`, and `LoopEngine.history()`/`.verify()` all
  read `self._records`/`self._history` without taking `self._lock`, even on
  the in-memory (no `storage_path`) path. In CPython 3.12 the GIL makes
  `list.append()` and reference reassignment atomic, so a reader almost
  certainly never observes a torn list — but does it ever observe a
  **stale-but-internally-consistent** snapshot mid-append in a way that
  could make `verify_chain()`/`verify()` race against `_append_unchecked()`/
  `record()` and produce a spurious pass or fail? Construct a concrete
  interleaving (one thread appending in a loop, another concurrently calling
  `verify_chain()`/`verify()` in a loop) and see if you can produce anything
  other than "always valid, sees old or new state, never in between." If you
  can't break it, say so explicitly — this is exactly the kind of "GIL saves
  us" reasoning the project has been asked to verify empirically rather than
  assume, both here and elsewhere.
- **`EvidenceLedger.from_dict()` mutates `self._records` directly, bypassing
  both `_append_unchecked()` and the new lock entirely** (see
  `evidence.py`, the `from_dict` classmethod: `ledger._records.append(...)`
  in a loop, no lock, no chain-hash recomputation — it trusts the dicts it's
  given were already a valid chain). Is there any realistic path where
  `from_dict()` runs concurrently with `append()`/`record_execution()` on
  the *same* ledger instance (e.g., a caller reconstructing from a
  checkpoint while another thread is still appending)? If so, does the
  unlocked, unchained mutation in `from_dict()` reopen the exact race v2.4
  just closed for the "normal" append path? Note `LoopEngine` has no
  equivalent `from_dict()` — confirm that asymmetry and whether it matters.
- **`claim_id` is an unvalidated, caller-supplied string with no uniqueness
  constraint anywhere in `quarantine.py`.** Two separate `quarantine_claim()`
  calls with the *same* `claim_id` but *different* `raw_payload` each
  register their own `(claim_id, ingestion_hash)` pair into the registry
  without conflict or warning — `QuarantineRegistry` never asserts a
  `claim_id` maps to exactly one payload/hash. Does anything downstream
  assume `claim_id` uniqueness that this could violate, or is `is_registered()`'s
  exact-pair check sufficient regardless of how many hashes end up
  associated with one `claim_id`? Try to construct a scenario where
  `claim_id` reuse across different payloads causes an executor to accept a
  `claim_ingestion_hash` for the "wrong" semantic claim despite the exact-pair
  check passing.
- **Exercise the residual limit #6 above rather than just accepting it as
  documented.** Build a concrete PoC: a registry-configured
  `AuthorisedExecutor` where the calling code (imagine it's some future
  caller, not `engine.py`) simply forgets to pass `claim_id`. Confirm the
  round-5 payload-collision attack (residual limit #6 describes it, round 5
  found it, v2.4 fixed it only when `claim_id` is actually passed) still
  succeeds against that caller. This isn't asking you to "find" the gap —
  it's already named above — it's asking whether there's a *design* fix
  (e.g., making the executor refuse to omit `claim_id` once a registry is
  configured) that would close it structurally instead of by caller
  discipline, and whether that fix would break any existing test if you
  sketched it.
- Anything else that jumps out to you in a fresh read — the four above are
  starting points, not the whole assignment.

## Ground rules

- Python 3.12, standard library only. No `pip install` suggestions.
- Every finding needs: **exact file:line**, a **minimal runnable PoC or
  unittest-style test** that demonstrates it (not pseudocode), and your own
  honest call on **severity** and on whether it's closable within this
  design or inherent to the single-process/stdlib constraint.
- If a "gap" you find is actually already caught by the existing test suite
  or already listed as a known residual limit above, don't report it —
  that's not new signal.
- Existing test files, for reference (don't re-derive what they already
  cover): `tests/test_quarantine.py`, `tests/test_integrity.py`,
  `tests/test_scope.py`, `tests/test_execution.py`, `tests/test_evidence.py`,
  `tests/test_findings.py`, `tests/test_loop.py`, `tests/test_adversarial.py`
  (the round-1, 27-test adversarial file), `tests/test_concurrency.py`
  (file-locking tests from v2.3, in-memory thread-safety tests new in v2.4).

## Output format

For each finding:

```
### Finding N: <one-line name>
- Location: <file:line>
- Class: <new gap | already-covered (name the test) | non-issue (say why)>
- Attack: <what an adversary does>
- PoC: <runnable code>
- Severity: <your call>
- Closable-in-design?: <yes, here's the fix | no, inherent, here's why>
```

Close with a one-paragraph honest summary: how many *new* gaps you actually
found, and how confident you are that you've covered the surface — not a
certification, just your best honest read.

---

## Appendix: full source

### `forensic_checker/__init__.py`

```python
CHECKER_VERSION = "2.4"
```

### `forensic_checker/_filelock.py`

```python
"""Cross-process locking for the append-only .jsonl storage files shared by
evidence.py's EvidenceLedger and loop.py's LoopEngine.

v2.3: remediation for the round-4 finding that _append_unchecked() (evidence)
and record() (loop) performed raw, unsynchronized open() calls against
storage_path. Concurrent writers could interleave writes and, more
fundamentally, could each compute a hash/HMAC chain link from a stale
prev_hash/prev_digest read before the other's write landed -- corrupting the
chain even without any single write being physically torn. locked_open()
holds an OS-level advisory lock (fcntl.flock) for the entire duration its
caller has the file open; both ledger.py and loop.py use it to read the
current on-disk tail and append the next record in one lock-held critical
section, closing both the physical-corruption and the stale-prev-hash race
at once.

POSIX-only (fcntl). On a platform without fcntl, locking is skipped rather
than raising -- single-process/single-host correctness (everything the
existing test suite exercises) is unaffected; only the concurrent-writer
guarantee is unavailable on that platform. That trade-off is deliberate and
reported via HAVE_FLOCK, not silent.
"""

from __future__ import annotations

from contextlib import contextmanager

try:
    import fcntl
    HAVE_FLOCK = True
except ImportError:  # pragma: no cover - exercised only on non-POSIX platforms
    fcntl = None
    HAVE_FLOCK = False


@contextmanager
def locked_open(path, mode: str, exclusive: bool):
    """Open path in mode, holding a shared (exclusive=False) or exclusive
    (exclusive=True) flock for the lifetime of the context. mode "a+" is
    used by writers that need to read the current tail before appending;
    mode "r" is used by pure readers."""
    fh = open(path, mode, encoding="utf-8")
    try:
        if HAVE_FLOCK:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
        yield fh
    finally:
        if HAVE_FLOCK:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        fh.close()
```

### `forensic_checker/quarantine.py`

```python
"""Claim quarantine: generator input enters the system only through this module.

v2.2: adds is_valid_ingestion_hash(), a structural check used by execution.py
to require that every authorised execution is bound to a real quarantine
ingestion_hash (remediation for the v2.1 finding that quarantine_claim()'s
return value was computed and then discarded in engine.py, leaving the
checked operation entirely decoupled from the claim that was supposedly
being checked).

v2.3: adds QuarantineRegistry. Round-4 audit found that is_valid_ingestion_hash()
is a format check only -- any well-formed sha256 hex string, never actually
issued by quarantine_claim(), satisfied it. quarantine_claim() now accepts an
optional registry and, when given one, records the hash it issued.
AuthorisedExecutor (execution.py) can be constructed with the same registry
to require that a claim_ingestion_hash was really issued, not merely
well-formed. The registry is opt-in: passing none preserves the v2.2
format-only behaviour, which is what the existing test suite's many
directly-constructed hashes rely on. engine.py's real pipeline always wires
a registry, so the production path is fully closed even though the format-
only fallback remains available for callers that don't need it.

v2.4: round-5 audit found that QuarantineRegistry indexed issued claims by
ingestion_hash alone, in a flat set. Since ingestion_hash is just
sha256(raw_payload), two distinct claims (different claim_id) that happen to
quarantine identical payload text produce the identical hash -- so a hash
issued for claim_id "A" was silently interchangeable with one issued for
claim_id "B" in is_registered()'s hash-only membership check. register() now
tracks the exact (claim_id, ingestion_hash) pair, and is_registered() accepts
an optional claim_id to check that exact pair rather than hash membership
alone. claim_id is opt-in on the caller's side too: omitting it preserves the
v2.3 hash-only check (any claim_id that was ever paired with this hash
suffices), which is what execution.py's default call and the existing test
suite rely on.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone

_SHA256_HEX_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class ClaimPackage:
    claim_id: str
    ingestion_hash: str
    raw_payload: str
    timestamp_utc: str


class QuarantineRegistry:
    """Tracks ingestion hashes actually issued by quarantine_claim() in this
    process. Constructing AuthorisedExecutor with a registry requires that a
    claim_ingestion_hash passed to run() was really issued against that
    registry, not merely well-formed -- closing the round-4 gap where a
    synthesized (but correctly-shaped) hash, never produced by
    quarantine_claim(), passed is_valid_ingestion_hash() and was accepted."""

    def __init__(self):
        self._issued: set = set()  # set of (claim_id, ingestion_hash) pairs

    def register(self, claim: "ClaimPackage") -> None:
        self._issued.add((claim.claim_id, claim.ingestion_hash))

    def is_registered(self, ingestion_hash, claim_id=None) -> bool:
        """With claim_id given, requires the exact (claim_id, ingestion_hash)
        pair to have been issued together -- closing the round-5 gap where
        two claims sharing a payload (and therefore a hash) were mutually
        substitutable. With claim_id omitted, falls back to the v2.3
        hash-only membership check (any issued claim_id paired with this
        hash suffices)."""
        if not is_valid_ingestion_hash(ingestion_hash):
            return False
        if claim_id is not None:
            return (claim_id, ingestion_hash) in self._issued
        return any(issued_hash == ingestion_hash for _, issued_hash in self._issued)


def quarantine_claim(claim_id: str, raw_payload: str, registry: QuarantineRegistry = None) -> ClaimPackage:
    ingestion_hash = hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()
    timestamp_utc = datetime.now(timezone.utc).isoformat()
    claim = ClaimPackage(
        claim_id=claim_id,
        ingestion_hash=ingestion_hash,
        raw_payload=raw_payload,
        timestamp_utc=timestamp_utc,
    )
    if registry is not None:
        registry.register(claim)
    return claim


def is_valid_ingestion_hash(value) -> bool:
    """Structural check only: is this a well-formed sha256 hex digest? It
    does not re-verify that the hash matches any particular raw_payload --
    that equality holds by construction for any hash produced by
    quarantine_claim() above, since ClaimPackage is frozen/immutable. It also
    does not prove the hash was ever actually issued -- see QuarantineRegistry
    for that stronger, opt-in guarantee."""
    return isinstance(value, str) and bool(_SHA256_HEX_RE.match(value))
```

### `forensic_checker/integrity.py`

```python
"""Checker self-integrity: hash checker source files, detect modification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

PACKAGE_FILES = (
    "__init__.py",
    "_filelock.py",
    "integrity.py",
    "quarantine.py",
    "scope.py",
    "execution.py",
    "evidence.py",
    "findings.py",
    "loop.py",
    "engine.py",
)


class IntegrityFailure(Exception):
    """STATUS: CHECKER_INTEGRITY_FAILURE"""


def compute_manifest(package_dir: Path) -> dict:
    manifest = {}
    for name in PACKAGE_FILES:
        data = (package_dir / name).read_bytes()
        manifest[name] = hashlib.sha256(data).hexdigest()
    return manifest


def manifest_root_hash(manifest: dict) -> str:
    canonical = json.dumps(manifest, sort_keys=True).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def verify_integrity(package_dir: Path, manifest_path: Path) -> dict:
    """Trust-on-first-use: if no manifest exists yet, this run's hashes become
    the baseline. A manifest tampered with or replaced before the first
    legitimate run is a security assumption this module cannot close -- see
    build report."""
    current = compute_manifest(package_dir)

    if not manifest_path.exists():
        manifest_path.write_text(
            json.dumps(current, indent=2, sort_keys=True), encoding="utf-8"
        )
        return current

    expected = json.loads(manifest_path.read_text(encoding="utf-8"))
    if current != expected:
        raise IntegrityFailure("CHECKER_INTEGRITY_FAILURE: source manifest mismatch")
    return current


def describe_trust_model(manifest_path: Path) -> dict:
    """v2.1 remediation 7: report what integrity verification actually
    guarantees, rather than let a caller assume more than trust-on-first-use
    provides. This does not close the trust-on-first-use gap -- it makes it
    visible in every run's output instead of leaving it undocumented."""
    return {
        "trust_root": "local-trust-on-first-use",
        "external_root_configured": False,
        "manifest_signed": False,
        "manifest_path": str(manifest_path),
        "limitation": (
            "the manifest is an unsigned local file; an attacker able to "
            "write both the source tree and this manifest can rebase trust "
            "onto tampered source. No external root of trust is configured."
        ),
    }
```

### `forensic_checker/scope.py`

```python
"""Scope authority: checker-controlled path validation.

v2.2: validate_path() now also requires the resolved path to be a regular
file (remediation for the v2.1 finding that `real == root` let a directory
-- including an allowed root itself -- pass validation and be handed to
callers such as AuthorisedExecutor as if it were a validated executable).
"""

from __future__ import annotations

import os


class ScopeViolation(Exception):
    """STATUS: SCOPE_VIOLATION"""


class ScopeGuard:
    def __init__(self, allowed_roots):
        self._roots = tuple(os.path.realpath(str(r)) for r in allowed_roots)

    @property
    def roots(self) -> tuple:
        return self._roots

    def validate_path(self, path) -> str:
        real = os.path.realpath(str(path))
        for root in self._roots:
            if real == root or real.startswith(root + os.sep):
                if not os.path.isfile(real):
                    raise ScopeViolation(
                        f"SCOPE_VIOLATION: {path!r} resolves to a non-file "
                        f"path ({real!r}); directories cannot satisfy scope "
                        "validation"
                    )
                return real
        raise ScopeViolation(
            f"SCOPE_VIOLATION: {path!r} escapes allowed roots {self._roots!r}"
        )
```

### `forensic_checker/execution.py`

```python
"""Execution authority: checker-controlled, allowlisted command execution.

v2.1: command authorisation now validates argument FORM, not just
executable identity (remediation for the v2.0 finding that allowlisting a
launcher-style binary let caller-controlled args execute unauthorised
programs). A capability sentinel (_EXECUTION_CAPABILITY) gates the creation
of COMMAND_EXECUTION evidence in evidence.py -- see that module for the
honest limits of that gate.

v2.2: AuthorisedExecutor.run() now requires a claim_ingestion_hash bound
from quarantine.quarantine_claim() (remediation for the v2.1 finding that
the quarantined claim was never actually wired to the checked operation).
This is a structural/format check only -- it does not re-derive the hash
from a raw payload, since ClaimPackage's immutability already guarantees
ingestion_hash == sha256(raw_payload) for anything quarantine_claim()
produced. The hash flows into ExecutionRecord and, via evidence.py, into
the hash-chained evidence payload -- once recorded, altering it breaks
the chain like any other payload field.

v2.3: AuthorisedExecutor accepts an optional quarantine.QuarantineRegistry.
When given one, run() requires claim_ingestion_hash to have actually been
issued by quarantine_claim() against that registry, not merely be
well-formed -- remediation for the round-4 finding that the v2.2 format-only
check accepted any synthesized sha256-shaped string. The registry is
opt-in: an executor with none falls back to the v2.2 format-only check,
which the existing test suite's directly-constructed hashes rely on.
engine.py's real pipeline always wires a registry.

v2.4: run() accepts an optional claim_id, forwarded to
QuarantineRegistry.is_registered() -- remediation for the round-5 finding
that a hash shared by two distinct claims (same payload, different
claim_id) was accepted regardless of which claim it was actually being
checked against. Passing claim_id requires the exact claim -> hash binding;
omitting it preserves the v2.3 hash-only check. engine.py's real pipeline
now passes the claim's own claim_id, fully closing the binding for the
production path.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
from dataclasses import dataclass

from .quarantine import is_valid_ingestion_hash
from .scope import ScopeGuard

EXECUTION_ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C.UTF-8"}
ENVIRONMENT_FINGERPRINT = hashlib.sha256(
    json.dumps(EXECUTION_ENV, sort_keys=True).encode("utf-8")
).hexdigest()

# Possessing this object is required to mint COMMAND_EXECUTION evidence
# (see evidence.EvidenceLedger.record_execution). It is a private module
# singleton, not part of the public API -- but Python cannot make it
# unreachable to same-process code that deliberately imports the
# underscore-prefixed name. That is a known, documented limitation, not a
# cryptographic guarantee.
_EXECUTION_CAPABILITY = object()


class ExecutionDenied(Exception):
    """Raised when a command, or its argument form, is not authorised."""


@dataclass(frozen=True)
class ExecutionRecord:
    command: tuple
    executable: str
    stdout: str
    stderr: str
    exit_code: int
    runtime_seconds: float
    environment_fingerprint: str
    claim_ingestion_hash: str


class CommandPolicy:
    """Binds an allowlisted command name to one executable AND a closed set
    of approved argument tuples. An argument tuple not in the approved set
    is refused outright -- executable identity alone is not authority."""

    def __init__(self, executable: str, allowed_argument_forms=((),)):
        self.executable = executable
        self.allowed_argument_forms = frozenset(tuple(form) for form in allowed_argument_forms)

    def permits(self, args) -> bool:
        return tuple(args) in self.allowed_argument_forms


class AuthorisedExecutor:
    def __init__(self, scope_guard: ScopeGuard, allowlist: dict, registry=None):
        self._scope = scope_guard
        self._registry = registry
        self._policies = {}
        for name, entry in allowlist.items():
            if isinstance(entry, CommandPolicy):
                self._policies[name] = entry
            else:
                # A bare executable-path string is the strictest possible
                # policy: no arguments permitted at all.
                self._policies[name] = CommandPolicy(entry, allowed_argument_forms=((),))

    def run(self, command_name: str, *, claim_ingestion_hash: str, claim_id: str = None, args=()) -> ExecutionRecord:
        if not is_valid_ingestion_hash(claim_ingestion_hash):
            raise ExecutionDenied(
                "execution requires a valid sha256 claim_ingestion_hash bound "
                "from quarantine.quarantine_claim(); none or a malformed hash "
                "was given"
            )

        if self._registry is not None and not self._registry.is_registered(claim_ingestion_hash, claim_id=claim_id):
            raise ExecutionDenied(
                "claim_ingestion_hash is well-formed but was never issued by "
                "quarantine.quarantine_claim() against this executor's configured "
                "registry" + (f" for claim_id {claim_id!r}" if claim_id is not None else "")
            )

        if command_name not in self._policies:
            raise ExecutionDenied(f"command not allowlisted: {command_name!r}")

        policy = self._policies[command_name]
        args = tuple(args)
        if not policy.permits(args):
            raise ExecutionDenied(
                f"argument form {args!r} is not an approved form for {command_name!r}"
            )

        validated_executable = self._scope.validate_path(policy.executable)

        start = time.monotonic()
        result = subprocess.run(
            [validated_executable, *args],
            capture_output=True,
            text=True,
            env=dict(EXECUTION_ENV),
            timeout=30,
        )
        runtime_seconds = time.monotonic() - start

        return ExecutionRecord(
            command=tuple([validated_executable, *args]),
            executable=validated_executable,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode,
            runtime_seconds=runtime_seconds,
            environment_fingerprint=ENVIRONMENT_FINGERPRINT,
            claim_ingestion_hash=claim_ingestion_hash,
        )


def is_authorised_execution_payload(payload) -> bool:
    """Schema check used by findings.resolve_finding(): does this payload
    structurally match what AuthorisedExecutor.run() produces? This is a
    shape/constant check, not authentication -- an attacker who reads this
    source can replicate the shape exactly. Real provenance enforcement is
    EvidenceLedger's reserved-operation guard in evidence.py."""
    if not isinstance(payload, dict):
        return False
    required_keys = {
        "exit_code", "stdout", "stderr", "executable",
        "environment_fingerprint", "claim_ingestion_hash",
    }
    if set(payload.keys()) != required_keys:
        return False
    if payload.get("environment_fingerprint") != ENVIRONMENT_FINGERPRINT:
        return False
    return is_valid_ingestion_hash(payload.get("claim_ingestion_hash"))
```

### `forensic_checker/evidence.py`

```python
"""Evidence ledger: checker-generated, hash-chained, append-only, tamper-detectable.

v2.1: adds record_execution() as the only way to create COMMAND_EXECUTION
evidence (gated by a capability object from execution.py and a real
ExecutionRecord instance), and optional append-only file-backed storage so
resolve_finding()/engine.py can reload_and_verify() instead of trusting
whatever is currently sitting in this process's memory.

v2.2: record_execution()'s payload now also carries the execution's
claim_ingestion_hash, so the quarantine-to-execution binding (see
quarantine.py, execution.py) is itself hash-chained -- altering it after
the fact breaks verify_chain() exactly like tampering with any other
payload field.

Known limitation (documented, not solved -- stdlib-only, single-process
constraints): an attacker with filesystem write access to the storage file
itself can still replace it wholesale with a different, internally
self-consistent forged file. reload_and_verify() defeats in-memory
mutation; it does not defeat a compromised disk. See
tests/test_adversarial.py::TestEvidenceTampering for a test that
demonstrates this residual gap directly.

v2.3: _append_unchecked() now performs its read-current-tail /
compute-next-chain-link / write steps inside one flock-held critical
section (see _filelock.py) when storage_path is configured, instead of
appending to disk from a possibly-stale in-memory self._records. Round-4
audit found that two concurrent EvidenceLedger instances backed by the same
storage_path could each compute chain_hash from a prev_hash read before the
other's write landed, corrupting the chain even though neither write was
physically torn. Reads (_load_from_storage / reload_and_verify) take a
shared lock; appends take an exclusive one.

v2.4: adds a threading.Lock guarding the in-memory (no storage_path)
append path. Round-5 audit found that a single EvidenceLedger instance
shared across threads -- unlike the file-backed case, which flock already
serialises -- had no synchronization at all: concurrent _append_unchecked()
calls could each read self._records's stale tail before either appended,
computing duplicate/diverging chain_hash values. The lock is only taken on
the in-memory branch; the file-backed branch's correctness already comes
from locked_open() and is unaffected.
"""

from __future__ import annotations

import hashlib
import json
import threading
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from . import execution as _execution
from ._filelock import locked_open

GENESIS_HASH = "0" * 64
COMMAND_EXECUTION_OPERATION = "COMMAND_EXECUTION"


class EvidenceIntegrityFailure(Exception):
    """STATUS: EVIDENCE_INTEGRITY_FAILURE"""


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    run_id: str
    timestamp_utc: str
    checker_version: str
    operation: str
    target: str
    payload: str
    sha256: str
    chain_hash: str


def _canonical_payload(payload) -> str:
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, sort_keys=True)


def _parse_evidence_lines(fh) -> list:
    records = []
    for line in fh:
        line = line.strip()
        if not line:
            continue
        records.append(EvidenceRecord(**json.loads(line)))
    return records


class EvidenceLedger:
    RESERVED_OPERATIONS = frozenset({COMMAND_EXECUTION_OPERATION})

    def __init__(self, storage_path=None):
        self._records: list = []
        self._storage_path = Path(storage_path) if storage_path else None
        self._lock = threading.Lock()
        if self._storage_path and self._storage_path.exists():
            self._load_from_storage()

    def _load_from_storage(self):
        with locked_open(self._storage_path, "r", exclusive=False) as fh:
            self._records = _parse_evidence_lines(fh)
        self.verify_chain()

    def reload_and_verify(self) -> bool:
        """Discard in-memory state and rebuild strictly from append-only
        storage, verifying the chain. This is what defeats in-process
        mutation of _records -- it is only authoritative if a storage_path
        was actually configured."""
        if not self._storage_path:
            raise EvidenceIntegrityFailure(
                "EVIDENCE_INTEGRITY_FAILURE: no append-only storage configured; "
                "in-memory ledger state cannot be treated as authoritative"
            )
        self._load_from_storage()
        return True

    def _append_unchecked(self, run_id, checker_version, operation, target, payload) -> EvidenceRecord:
        payload_str = _canonical_payload(payload)
        payload_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

        if self._storage_path:
            # Read the current on-disk tail, compute the next chain link, and
            # write it, all inside one exclusive-lock critical section -- so
            # a concurrent writer can't cause this record's prev_hash to go
            # stale between when it's read and when this record lands.
            with locked_open(self._storage_path, "a+", exclusive=True) as fh:
                fh.seek(0)
                records_on_disk = _parse_evidence_lines(fh)
                prev_hash = records_on_disk[-1].chain_hash if records_on_disk else GENESIS_HASH
                chain_hash = hashlib.sha256((prev_hash + payload_hash).encode("utf-8")).hexdigest()
                record = EvidenceRecord(
                    evidence_id=str(uuid.uuid4()),
                    run_id=run_id,
                    timestamp_utc=datetime.now(timezone.utc).isoformat(),
                    checker_version=checker_version,
                    operation=operation,
                    target=target,
                    payload=payload_str,
                    sha256=payload_hash,
                    chain_hash=chain_hash,
                )
                fh.write(json.dumps(asdict(record), sort_keys=True) + "\n")
                fh.flush()
                self._records = records_on_disk + [record]
            return record

        # No storage_path: this instance's self._records is the only shared
        # state, and unlike the file-backed branch above (serialised by
        # locked_open) it has no OS-level lock protecting it -- a plain
        # in-process threading.Lock stands in for that here.
        with self._lock:
            prev_hash = self._records[-1].chain_hash if self._records else GENESIS_HASH
            chain_hash = hashlib.sha256((prev_hash + payload_hash).encode("utf-8")).hexdigest()
            record = EvidenceRecord(
                evidence_id=str(uuid.uuid4()),
                run_id=run_id,
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
                checker_version=checker_version,
                operation=operation,
                target=target,
                payload=payload_str,
                sha256=payload_hash,
                chain_hash=chain_hash,
            )
            self._records.append(record)
            return record

    def append(self, run_id: str, checker_version: str, operation: str, target: str, payload) -> EvidenceRecord:
        if operation in self.RESERVED_OPERATIONS:
            raise EvidenceIntegrityFailure(
                f"EVIDENCE_INTEGRITY_FAILURE: operation {operation!r} is reserved; "
                "use record_execution() with a valid execution capability"
            )
        return self._append_unchecked(run_id, checker_version, operation, target, payload)

    def record_execution(self, capability, run_id: str, checker_version: str, target: str, execution_record) -> EvidenceRecord:
        if capability is not _execution._EXECUTION_CAPABILITY:
            raise EvidenceIntegrityFailure(
                "EVIDENCE_INTEGRITY_FAILURE: execution evidence requires the execution capability"
            )
        if not isinstance(execution_record, _execution.ExecutionRecord):
            raise EvidenceIntegrityFailure(
                "EVIDENCE_INTEGRITY_FAILURE: execution evidence must wrap a real ExecutionRecord"
            )
        payload = {
            "exit_code": execution_record.exit_code,
            "stdout": execution_record.stdout,
            "stderr": execution_record.stderr,
            "executable": execution_record.executable,
            "environment_fingerprint": execution_record.environment_fingerprint,
            "claim_ingestion_hash": execution_record.claim_ingestion_hash,
        }
        return self._append_unchecked(run_id, checker_version, COMMAND_EXECUTION_OPERATION, target, payload)

    def records(self) -> tuple:
        return tuple(self._records)

    @property
    def root_hash(self) -> str:
        return self._records[-1].chain_hash if self._records else GENESIS_HASH

    def verify_chain(self) -> bool:
        prev_hash = GENESIS_HASH
        for record in self._records:
            expected_payload_hash = hashlib.sha256(record.payload.encode("utf-8")).hexdigest()
            if expected_payload_hash != record.sha256:
                raise EvidenceIntegrityFailure(
                    f"EVIDENCE_INTEGRITY_FAILURE: payload hash mismatch for {record.evidence_id}"
                )
            expected_chain_hash = hashlib.sha256(
                (prev_hash + expected_payload_hash).encode("utf-8")
            ).hexdigest()
            if expected_chain_hash != record.chain_hash:
                raise EvidenceIntegrityFailure(
                    f"EVIDENCE_INTEGRITY_FAILURE: chain hash mismatch for {record.evidence_id}"
                )
            prev_hash = record.chain_hash
        return True

    def verify_against_checkpoint(self, expected_root_hash: str) -> bool:
        self.verify_chain()
        if self.root_hash != expected_root_hash:
            raise EvidenceIntegrityFailure(
                "EVIDENCE_INTEGRITY_FAILURE: root hash mismatch (possible truncation)"
            )
        return True

    def to_dict(self) -> dict:
        return {"records": [asdict(r) for r in self._records]}

    @classmethod
    def from_dict(cls, data: dict) -> "EvidenceLedger":
        ledger = cls()
        for rec in data["records"]:
            ledger._records.append(EvidenceRecord(**rec))
        return ledger
```

### `forensic_checker/findings.py`

```python
"""Finding authority: only FindingAuthority may mint or resolve findings.

v2.1: VerifiedFinding now carries an HMAC signature over its own fields.
create_finding()/resolve_finding() (thin wrappers around a module-level
FindingAuthority) are the only paths that produce a *validly signed*
finding. Direct construction or dataclasses.replace() still succeed as
Python operations (nothing can prevent instantiating a public frozen
dataclass) but produce an object that is_valid_finding() rejects, because
its signature won't match its (possibly altered) field values.

Known limitation (documented, not solved): the signing secret lives on the
default FindingAuthority instance. Same-process code that goes looking for
it (e.g. _DEFAULT_AUTHORITY._secret) can still forge a valid signature.
This is the same class of limitation as loop.py's HMAC key handling.
"""

from __future__ import annotations

import dataclasses
import hashlib
import hmac
import json
import secrets
import uuid
from dataclasses import dataclass

from . import evidence as _evidence
from . import execution as _execution

CREATED_BY = "CHECKER"


class FindingViolation(Exception):
    """Raised when a finding lifecycle rule is violated."""


@dataclass(frozen=True)
class VerifiedFinding:
    finding_id: str
    run_id: str
    created_by: str
    evidence_id: str
    description: str
    status: str  # "OPEN" | "RESOLVED"
    signature: str = ""


class FindingAuthority:
    """The sole intended issuer of VerifiedFinding objects."""

    def __init__(self, secret: bytes = None):
        self._secret = secret if secret is not None else secrets.token_bytes(32)

    def _sign(self, finding_id, run_id, created_by, evidence_id, description, status) -> str:
        message = json.dumps(
            {
                "finding_id": finding_id,
                "run_id": run_id,
                "created_by": created_by,
                "evidence_id": evidence_id,
                "description": description,
                "status": status,
            },
            sort_keys=True,
        ).encode("utf-8")
        return hmac.new(self._secret, message, hashlib.sha256).hexdigest()

    def create_finding(self, run_id: str, evidence_id: str, description: str) -> VerifiedFinding:
        finding_id = str(uuid.uuid4())
        status = "OPEN"
        signature = self._sign(finding_id, run_id, CREATED_BY, evidence_id, description, status)
        return VerifiedFinding(
            finding_id=finding_id,
            run_id=run_id,
            created_by=CREATED_BY,
            evidence_id=evidence_id,
            description=description,
            status=status,
            signature=signature,
        )

    def is_valid(self, finding) -> bool:
        if not isinstance(finding, VerifiedFinding):
            return False
        if finding.created_by != CREATED_BY:
            return False
        expected = self._sign(
            finding.finding_id, finding.run_id, finding.created_by,
            finding.evidence_id, finding.description, finding.status,
        )
        return hmac.compare_digest(expected, finding.signature)

    def resolve_finding(self, finding: VerifiedFinding, ledger: "_evidence.EvidenceLedger", run_id: str) -> VerifiedFinding:
        if not self.is_valid(finding):
            raise FindingViolation("finding signature is invalid or was not issued by this authority")

        matching = [r for r in ledger.records() if r.evidence_id == finding.evidence_id]
        if not matching:
            raise FindingViolation("evidence_id does not exist in ledger")

        record = matching[0]
        if record.run_id != run_id:
            raise FindingViolation("evidence does not belong to the current run")

        if record.operation != _evidence.COMMAND_EXECUTION_OPERATION:
            raise FindingViolation("evidence was not produced by authorised command execution")

        ledger.verify_chain()

        try:
            payload = json.loads(record.payload)
        except (json.JSONDecodeError, TypeError):
            raise FindingViolation("evidence payload is not valid execution evidence")

        if not _execution.is_authorised_execution_payload(payload):
            raise FindingViolation("evidence payload does not match the authorised execution schema")

        if payload["exit_code"] != 0:
            raise FindingViolation("evidence does not prove successful execution (exit_code != 0)")

        new_signature = self._sign(
            finding.finding_id, finding.run_id, finding.created_by,
            finding.evidence_id, finding.description, "RESOLVED",
        )
        return dataclasses.replace(finding, status="RESOLVED", signature=new_signature)


_DEFAULT_AUTHORITY = FindingAuthority()


def create_finding(run_id: str, evidence_id: str, description: str) -> VerifiedFinding:
    return _DEFAULT_AUTHORITY.create_finding(run_id, evidence_id, description)


def resolve_finding(finding: VerifiedFinding, ledger, run_id: str) -> VerifiedFinding:
    return _DEFAULT_AUTHORITY.resolve_finding(finding, ledger, run_id)


def is_valid_finding(finding) -> bool:
    return _DEFAULT_AUTHORITY.is_valid(finding)
```

### `forensic_checker/loop.py`

```python
"""Loop authority: HMAC-protected, append-only, replay-resistant history of
verified findings.

v2.1: LoopEngine.record() now requires findings.is_valid_finding() to pass,
not just isinstance() -- a forged VerifiedFinding (wrong signature) is
rejected here even though nothing can prevent it from being constructed in
the first place (see findings.py). The HMAC secret is no longer stored as a
plain instance attribute (self._key is gone); it lives only inside a
closure. That raises the bar over simple attribute access, but Python
closures remain introspectable via __closure__ -- see
tests/test_adversarial.py::TestHistoryTampering for a test that
demonstrates this residual route still works.

v2.2: adds optional append-only file-backed storage (storage_path) and a
persisted HMAC key (key_path), mirroring evidence.py's EvidenceLedger --
remediation for the v2.1 finding that engine.py instantiated a fresh
os.urandom(32) key on every run with nowhere for history to persist, so the
"loop" never actually chained across process invocations. On construction,
an existing key_path is reused as-is (trust-on-first-use, same pattern as
integrity.py's manifest) and an existing storage_path is reloaded and
verified immediately -- a tampered or truncated persisted history raises
HistoryTamperDetected at load time, before any new event is recorded.
Known limitation (same class as evidence.py's, documented not solved): an
attacker with filesystem write access to key_path or storage_path can
still replace either wholesale with an internally self-consistent forgery.

v2.3: record() now performs its read-current-tail / compute-next-hmac-link /
write steps inside one flock-held critical section (see _filelock.py) when
storage_path is configured, instead of appending from possibly-stale
in-memory self._history. Round-4 audit found that two concurrent LoopEngine
instances backed by the same storage_path could each compute an hmac_digest
from a prev_digest/sequence read before the other's write landed, diverging
the chain even though neither write was physically torn. Reads
(_load_from_storage / reload_and_verify) take a shared lock; record() takes
an exclusive one for its whole read-compute-write span.

v2.4: adds a threading.Lock guarding the in-memory (no storage_path) record
path. Round-5 audit found that a single LoopEngine instance shared across
threads had no synchronization protecting self._history/self._seen_sequences:
concurrent record() calls could each read a stale sequence/prev_digest tail
before either appended, producing duplicate sequence numbers and diverging
hmac chains. The file-backed branch is unaffected -- its correctness already
comes from locked_open().
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from ._filelock import locked_open
from .findings import VerifiedFinding, is_valid_finding

GENESIS_DIGEST = "GENESIS"


class HistoryTamperDetected(Exception):
    """STATUS: HISTORY_TAMPER_DETECTED"""


@dataclass(frozen=True)
class LoopEvent:
    sequence: int
    run_id: str
    finding_ids: tuple
    timestamp_utc: str
    hmac_digest: str


def _make_signer(secret_key: bytes):
    def sign(message: bytes) -> str:
        return hmac.new(secret_key, message, hashlib.sha256).hexdigest()
    return sign


def _parse_loop_lines(fh) -> list:
    events = []
    for line in fh:
        line = line.strip()
        if not line:
            continue
        data = json.loads(line)
        events.append(LoopEvent(
            sequence=data["sequence"],
            run_id=data["run_id"],
            finding_ids=tuple(data["finding_ids"]),
            timestamp_utc=data["timestamp_utc"],
            hmac_digest=data["hmac_digest"],
        ))
    return events


class LoopEngine:
    def __init__(self, secret_key: bytes = None, storage_path=None, key_path=None):
        self._storage_path = Path(storage_path) if storage_path else None
        self._key_path = Path(key_path) if key_path else None
        self._history: list = []
        self._seen_sequences: set = set()
        self._lock = threading.Lock()

        self._sign = _make_signer(self._resolve_key(secret_key))

        if self._storage_path and self._storage_path.exists():
            self._load_from_storage()

    def _resolve_key(self, secret_key) -> bytes:
        """Trust-on-first-use, same pattern as integrity.py's manifest: if
        key_path doesn't exist yet, this call's key (explicit or freshly
        random) becomes the persisted baseline. If it does exist, the file
        is authoritative -- an explicitly-passed secret_key is ignored so a
        caller can't silently rotate the key out from under existing
        persisted history.

        v2.3: the check-then-write is now one flock-held critical section
        (mode "a+" creates the file if missing). Without this, concurrent
        first-time construction of separate LoopEngine instances against the
        same key_path could each observe "file doesn't exist yet", generate
        a different random key, and race to write it -- leaving different
        instances holding different secret keys despite sharing a key_path."""
        if self._key_path is None:
            return secret_key if secret_key is not None else secrets.token_bytes(32)
        with locked_open(self._key_path, "a+", exclusive=True) as fh:
            fh.seek(0)
            existing = fh.read().strip()
            if existing:
                return bytes.fromhex(existing)
            key = secret_key if secret_key is not None else secrets.token_bytes(32)
            fh.write(key.hex())
            fh.flush()
            return key

    def _load_from_storage(self):
        with locked_open(self._storage_path, "r", exclusive=False) as fh:
            self._history = _parse_loop_lines(fh)
        self._seen_sequences = {event.sequence for event in self._history}
        self.verify()

    def reload_and_verify(self) -> bool:
        """Discard in-memory state and rebuild strictly from append-only
        storage, verifying the chain -- same role as
        EvidenceLedger.reload_and_verify(). Only authoritative if a
        storage_path was actually configured."""
        if not self._storage_path:
            raise HistoryTamperDetected(
                "HISTORY_TAMPER_DETECTED: no append-only storage configured; "
                "in-memory loop history cannot be treated as authoritative"
            )
        self._load_from_storage()
        return True

    def _compute_hmac(self, sequence, run_id, finding_ids, timestamp_utc, prev_digest) -> str:
        message = json.dumps(
            {
                "sequence": sequence,
                "run_id": run_id,
                "finding_ids": list(finding_ids),
                "timestamp_utc": timestamp_utc,
                "prev_digest": prev_digest,
            },
            sort_keys=True,
        ).encode("utf-8")
        return self._sign(message)

    def record(self, run_id: str, findings) -> LoopEvent:
        findings = list(findings)
        if not all(isinstance(f, VerifiedFinding) and is_valid_finding(f) for f in findings):
            raise TypeError("loop state may only be derived from checker-signed VerifiedFinding objects")

        finding_ids = tuple(f.finding_id for f in findings)
        timestamp_utc = datetime.now(timezone.utc).isoformat()

        if self._storage_path:
            # Read the current on-disk tail, compute the next hmac link, and
            # write it, all inside one exclusive-lock critical section -- so
            # a concurrent writer can't cause this event's sequence/prev_digest
            # to go stale between when it's read and when this event lands.
            with locked_open(self._storage_path, "a+", exclusive=True) as fh:
                fh.seek(0)
                events_on_disk = _parse_loop_lines(fh)
                sequence = len(events_on_disk)
                prev_digest = events_on_disk[-1].hmac_digest if events_on_disk else GENESIS_DIGEST
                digest = self._compute_hmac(sequence, run_id, finding_ids, timestamp_utc, prev_digest)
                event = LoopEvent(
                    sequence=sequence,
                    run_id=run_id,
                    finding_ids=finding_ids,
                    timestamp_utc=timestamp_utc,
                    hmac_digest=digest,
                )
                fh.write(json.dumps({
                    "sequence": event.sequence,
                    "run_id": event.run_id,
                    "finding_ids": list(event.finding_ids),
                    "timestamp_utc": event.timestamp_utc,
                    "hmac_digest": event.hmac_digest,
                }, sort_keys=True) + "\n")
                fh.flush()
                self._history = events_on_disk + [event]
                self._seen_sequences = {e.sequence for e in self._history}
            return event

        # No storage_path: self._history/self._seen_sequences are the only
        # shared state, and unlike the file-backed branch above (serialised
        # by locked_open) nothing else protects them -- a plain in-process
        # threading.Lock stands in for that here.
        with self._lock:
            sequence = len(self._history)
            if sequence in self._seen_sequences:
                raise HistoryTamperDetected("HISTORY_TAMPER_DETECTED: replay detected")

            prev_digest = self._history[-1].hmac_digest if self._history else GENESIS_DIGEST
            digest = self._compute_hmac(sequence, run_id, finding_ids, timestamp_utc, prev_digest)
            event = LoopEvent(
                sequence=sequence,
                run_id=run_id,
                finding_ids=finding_ids,
                timestamp_utc=timestamp_utc,
                hmac_digest=digest,
            )
            self._history.append(event)
            self._seen_sequences.add(sequence)
            return event

    def history(self) -> tuple:
        return tuple(self._history)

    def verify(self) -> bool:
        prev_digest = GENESIS_DIGEST
        for index, event in enumerate(self._history):
            if event.sequence != index:
                raise HistoryTamperDetected("HISTORY_TAMPER_DETECTED: sequence gap or replay")
            expected_digest = self._compute_hmac(
                event.sequence, event.run_id, event.finding_ids, event.timestamp_utc, prev_digest
            )
            if not hmac.compare_digest(expected_digest, event.hmac_digest):
                raise HistoryTamperDetected("HISTORY_TAMPER_DETECTED: hmac mismatch")
            prev_digest = event.hmac_digest
        return True

    @staticmethod
    def converged(findings) -> bool:
        findings = list(findings)
        if not findings:
            return False
        return all(f.status == "RESOLVED" for f in findings)
```

### `forensic_checker/engine.py`

```python
"""CLI entry point: python -m forensic_checker.engine

v2.4 pipeline order:
  1. Checker integrity verification
  2. Claim quarantine                (registers (claim_id, ingestion_hash) in a QuarantineRegistry)
  3. Scope validation
  4. Authorised execution            (requires that exact claim_id/hash pair registered)
  5. Evidence creation      (via record_execution(), capability-gated; lock-protected append)
  6. Evidence verification  (reload_and_verify() against append-only storage)
  7. Finding evaluation
  8. Loop analysis          (persisted; lock-protected append; reload_and_verify() across runs)

Any evidence verification failure halts with STATUS: EVIDENCE_INTEGRITY_FAILURE.
Any loop-history verification failure halts with STATUS: HISTORY_TAMPER_DETECTED.

NOTE: no concrete generator-claim format has ever been specified for this
build. This engine demonstrates the verification boundary end-to-end using
a single allowlisted no-op command ("true") as the checked operation -- it
proves the pipeline's mechanics are wired correctly. It does not check real
generator output, because no real check content was ever given.
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path

from . import CHECKER_VERSION, evidence, execution, findings, integrity, loop, quarantine, scope


def _find_true_binary() -> str:
    for candidate in ("/usr/bin/true", "/bin/true"):
        if os.path.exists(candidate):
            return candidate
    raise execution.ExecutionDenied("no allowlisted 'true' binary found on this system")


def main(argv=None) -> int:
    argv = list(argv) if argv is not None else sys.argv[1:]
    run_id = str(uuid.uuid4())
    package_dir = Path(__file__).resolve().parent
    build_dir = package_dir.parent
    manifest_path = build_dir / "integrity_manifest.json"
    ledger_path = build_dir / "evidence_ledger.jsonl"
    loop_history_path = build_dir / "loop_history.jsonl"
    loop_key_path = build_dir / "loop_secret.key"

    result = {
        "status": "UNKNOWN",
        "run_id": run_id,
        "sha256_root": None,
        "converged": False,
        "error": None,
        "integrity": integrity.describe_trust_model(manifest_path),
    }

    try:
        integrity.verify_integrity(package_dir, manifest_path)

        raw_payload = argv[0] if argv else sys.stdin.read()
        registry = quarantine.QuarantineRegistry()
        claim = quarantine.quarantine_claim(run_id, raw_payload, registry=registry)

        exec_guard = scope.ScopeGuard(["/usr/bin", "/bin"])
        true_binary = _find_true_binary()
        executor = execution.AuthorisedExecutor(exec_guard, {"true": true_binary}, registry=registry)
        exec_record = executor.run("true", claim_ingestion_hash=claim.ingestion_hash, claim_id=claim.claim_id)

        ledger = evidence.EvidenceLedger(storage_path=ledger_path)
        ev = ledger.record_execution(
            execution._EXECUTION_CAPABILITY, run_id, CHECKER_VERSION, "true", exec_record
        )

        ledger.reload_and_verify()

        finding = findings.create_finding(run_id, ev.evidence_id, "baseline authorised-execution check")
        finding = findings.resolve_finding(finding, ledger, run_id)

        loop_engine = loop.LoopEngine(storage_path=loop_history_path, key_path=loop_key_path)
        loop_engine.record(run_id, [finding])
        loop_engine.reload_and_verify()

        result.update(
            {
                "status": "OK",
                "sha256_root": ledger.root_hash,
                "converged": loop.LoopEngine.converged([finding]),
                "error": None,
            }
        )
        print(json.dumps(result))
        return 0

    except integrity.IntegrityFailure as exc:
        result.update({"status": "CHECKER_INTEGRITY_FAILURE", "error": str(exc)})
        print(json.dumps(result))
        return 1
    except scope.ScopeViolation as exc:
        result.update({"status": "SCOPE_VIOLATION", "error": str(exc)})
        print(json.dumps(result))
        return 1
    except evidence.EvidenceIntegrityFailure as exc:
        result.update({"status": "EVIDENCE_INTEGRITY_FAILURE", "error": str(exc)})
        print(json.dumps(result))
        return 1
    except loop.HistoryTamperDetected as exc:
        result.update({"status": "HISTORY_TAMPER_DETECTED", "error": str(exc)})
        print(json.dumps(result))
        return 1
    except (execution.ExecutionDenied, findings.FindingViolation) as exc:
        result.update({"status": "FAIL_CLOSED", "error": str(exc)})
        print(json.dumps(result))
        return 1


if __name__ == "__main__":
    sys.exit(main())
```
