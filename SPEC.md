# Blacksmith — build architecture, v2

Supersedes v1 entirely. v1 described a post-boot restriction layer; that design
is dead. Blacksmith is a **pre-boot gatekeeper**.

Sections marked **[SCOTT]** are definitional calls awaiting his ruling.

---

## 1. Why v1 died

The old approach fought context injection with prompt text and harness flags —
`--safe-mode` to suppress memory, `--allowedTools` to restrict, `--add-dir` to
fence reads. All of it is the harness policing itself.

- 30 Jul: the designed restricted config **breached**. `python3 -c` through Bash
  wrote a canary, not denied, verified on disk externally.
- Read-scope confinement is **policy denial, not capability absence** (gate !16,
  OPEN). A denial that reads *pending* is a boundary a human can click through.
- `forensic_checker/findings.py:11` — in-process HMAC is forgeable by
  same-process code, by its own docstring.

**Deleted assumption:** that a boundary can be enforced from inside the thing
being bounded.

## 2. The correction

You cannot un-inject context from inside a prompt. You *can* arrange that there
was never anything to inject. Sterility is a property of the environment the
host builds, and the host builds it before the model exists.

Six rules, binding on every component:

1. **Independence is the OS process, filesystem, and UID boundary.** Not
   signatures, not prompts, not self-policing flags.
2. **Capability absence beats policy denial.** `--tools` is the only harness
   restriction proven to hold; prefer kernel permissions over all of them.
3. **Sterility by construction, not suppression.** Files absent, not disabled.
4. **Every verdict is re-derived by its consumer.** A supplied verdict is never
   a verdict; the fact of ignoring one is recorded.
5. **Promotion is code.** No model-driven step between adjudication and verified
   memory.
6. **Fail closed.** If the cell cannot be built or attested, there is no session.

## 3. Rings

| Ring | Contents | Trust |
|---|---|---|
| 0 — TCB | `cell`, `attest`, `launch`, `collect`, `gauge`, `promote` | trusted; parent-side, deterministic, no LLM, no network |
| 1 — cell | the generator session | untrusted, contained |
| 2 — output | transcript, artifacts, patches | untrusted until promoted |

Ring 0 stays small enough to read in one sitting. That is the point of it.

## 4. Components

All parent-side except the cell's occupant.

- **`ramp`** — entry point. Recovered from `hooks/mara_load.py` (deleted
  `903b6a9`, 12 Jul), **polarity inverted**: it does not inject context, it
  execs Blacksmith. Fails closed. Scoped to one intent, not every prompt — the
  targeting fault that got the original cut.
- **`cell`** — builds and destroys the sterile tree. Own `HOME`, no `CLAUDE.md`,
  no `MEMORY.md`, no skills, no hooks. Evidence placed read-only.
- **`attest`** — hashes cell, contract, runner, and evidence before launch;
  re-hashes after. Freezes a manifest. A missing manifest reports integrity
  UNKNOWN and is never filled in later.
- **`launch`** — spawns the child as the restricted UID.
- **`collect`** — deterministic evidence from outside the cell: the `init` tool
  set, `permission_denials`, hash deltas, exit code. **This is the box the old
  diagram called Assay.** [SCOTT — the tool named `assay` on disk is a pattern
  scanner that by design never executes anything. It is not this component.
  Rename the box or rename the tool; a chain-of-custody system cannot have two
  things per name.]
- **`gauge`** — pure adjudicator. `(bundle, contract, contract_hash)` → exactly
  one of `ACTIVE` / `FAILED` / `UNKNOWN` / `BYPASSED`. No I/O, no clock, no
  randomness, no float. Built.
- **`promote`** — the air gap. Re-derives the verdict, re-hashes the artifact,
  checks the contract hash. Only `ACTIVE` promotes.

## 5. Lifecycle

```
1  RAMP         trigger; fail closed
2  CELL BUILD   sterile tree, own HOME, evidence read-only
3  PRE-ATTEST   hash cell + contract + runner + evidence; freeze manifest
4  LAUNCH       restricted UID, cwd=HOME=cell, --safe-mode,
                --tools "Read,Grep,Glob", --append-system-prompt-file,
                --output-format stream-json
5  GENERATE     child emits artifact + transcript
                child's claims about its own isolation are DISCARDED
6  POST-ATTEST  re-hash cell; ANY delta = write capability = BYPASSED
7  COLLECT      parent-side deterministic evidence only
8  GAUGE        pure adjudication -> one of four
9  PROMOTE      ACTIVE only, verdict re-derived, artifact re-hashed
10 TEARDOWN     cell destroyed; bundle retained, hashed, mirrored
```

Step 6 is the honest instrument: it does not ask whether a write was *denied*,
it checks whether one *happened*.

## 6. Trust boundary table

Every prohibition gets a mechanism and an evidence state. A prohibition without
a mechanism is a wish.

| The generator cannot… | Mechanism | Status |
|---|---|---|
| write anything | `--tools "Read,Grep,Glob"` — Bash/Write/Edit genuinely absent | **PROVEN** — `init` reports the resulting set |
| read the memory store | restricted UID holds no read right on `~/.claude`; kernel `EACCES` | **UNPROVEN** — gated on §8 |
| see boot memory | sterile `HOME`; files absent, not suppressed | **UNPROVEN** — cheap to test |
| influence the collector | collector runs in parent, different UID, tree not child-writable | **UNPROVEN** |
| influence the adjudicator | `gauge` is a pure function in the parent; input is data | **PROVEN** — no I/O path exists |
| validate itself | `promote` re-derives; supplied verdicts ignored and recorded | **PROVEN** in slice |
| write verified memory | promotion is parent code; child has no channel to it | Promotion → verified-memory: **DEFERRED / NOT-WIRED** |

## 7. Two corrections to the old Proof path

**Wrap cannot promote.** The old path ran `… → Gauge → Wrap → verified memory`.
Wrap is a skill — prompt-driven, model-executed — which put an LLM between the
deterministic adjudicator and verified memory, contradicting "no LLM authority."
Wrap may **request** promotion. `promote` performs it.

**The air gap is not a wall to maintain; it is a wall to build.** Today
`CLAUDE.md` carries `@projects/-Users-Howard-Scott/memory/MEMORY.md`, so
unverified history enters governed context at boot, in every session, by design.
`UNVERIFIED` is the current state of the entire store. The migration is the work.

## 8. Kill criteria

State these before building, so no result can be fitted to a story afterwards.

- **Credentials do not survive the UID switch** and metered `--bare` spend is
  unacceptable → the kernel-grade gate is unaffordable → fall back to a
  same-UID sterile tree, which is policy-grade only, and this design's central
  claim dies with it. **This is step 0 and it is UNKNOWN.**
- **Post-attest shows cell deltas with Bash absent** → capability absence is not
  real → the harness is untrustworthy for any forensic purpose, and Blacksmith
  needs a VM, not a UID.

## 9. Build order

| # | Step | Why here |
|---|---|---|
| 0 | Credential/UID feasibility | Decides affordability of everything. One test. |
| 1 | Cell + attest + sterile-launch proof | The real Blacksmith boundary test. Does **not** wait on gate !16 — the boundary moved to the OS. |
| 2 | `promote` wired to Marrow | Hardest proof point; pure host code, no model, no rate limits. |
| 3 | Patch boundary / clean room | `scope.ScopeGuard` is the seed: realpath before prefix compare, regular-file requirement. |
| 4 | `gauge` onto `forensic_checker`'s ledger | Reuse the hash-chained ledger; do not rewrite it. |
| 5 | Adversarial harness | Forged verdict, replayed verdict, tampered manifest, missing-evidence-as-pass, BYPASSED laundered as ACTIVE, `../` in a patch, symlink, `.git/hooks`. |

**Board consequence:** gate !16 demotes from blocker to defence-in-depth, which
unblocks !15 (`proof-verify`). Step 1 needs `proof-verify` as its external
re-hash source.

## 10. Reuse, not rebuild

`forensic_checker` v2.4 is already the Proof spine, wired end-to-end and proven
on a no-op. `engine.py`'s docstring names the only gap: no generator-claim
format was ever specified. Take from it:

- `integrity.py` — manifest, root hash, trust model → `attest`
- `quarantine.py` — ingestion hash, `(claim_id, hash)` pair binding → Ring 2
- `scope.py` — path validation → patch boundary
- `evidence.py` — hash-chained append-only ledger → the bundle store
- `findings.py` — lifecycle discipline, **not** its HMAC as a boundary

## 11. Open rulings

1. **[SCOTT]** The `assay` name collision (§4).
2. Precedence `BYPASSED > FAILED > UNKNOWN`. A confirmed failure outranks
   missing evidence. Only ACTIVE promotes.
3. **[SCOTT]** Evidence into the cell as a copy, or a read-only mount.
4. **[SCOTT]** Metered spend, if credentials do not survive the UID switch.

## 12. UNKNOWN, preserved

Credential survival across UID. Whether `sandbox-exec` functions on Darwin 25.6.
Whether `Read`/`Grep`/`Glob` carry write side effects — assumed, never exercised.
Whether harness denial holds under interactive approval; under `-p` it is
terminal, but the message reads *pending*, and if a human can accept it the
boundary is a person.

Evidence durability: the gate16 bundles are gitignored and exist on this Mac
only. A chain-of-custody record with one un-mirrored copy has no custody.
