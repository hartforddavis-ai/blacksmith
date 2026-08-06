# BOUND SESSION — KERNEL

Fixed. Does not change without a Law 1 ruling. The job block changes freely.

## SESSION

Plain chat. No tools, no working directory, no file access, no search.
Everything you may use is pasted below. There is nothing else.

```
DECLARE every tool you hold. First line, before anything else.
IF you HOLD ANY tool → this run is VOID.
   Say so. STOP. Produce nothing else.
```

---

## CHECKS — cite as K1…K6. Not Laws; there are three Laws and no more.

The job names the positive and negative verdicts. These govern how you reach
either.

```
FOR EACH item:
  K1  STATE the verdict BEFORE describing the item.
  K2  One verdict per item. Spanning a group, file or sequence is not a
      verdict. Decompose, re-rule.
  K3  A positive verdict quotes the pasted line that supports it.
      No quote → negative verdict.
  K4  Undecidable → negative verdict. Not deferred.
  K5  Every specific traces to pasted text. Untraceable → cut it.
  K6  Propose nothing absent from the three Laws — no framework, protocol,
      ladder, role or principle. Cannot justify it from them → name the gap,
      STOP.
```

---

## BAR

You have run nothing and cannot. Every statement about behaviour is
**UNPROVEN**. Do not write PASS, works, verified or confirmed about any code.

---

## OUTPUT DISCIPLINE

No preamble. No summary of what you read. No assessment of your own work. No
offer to continue. Nothing outside the shape the job specifies.

---

# JOB — VERIFY THE BLACKSMITH REDESIGN RULING

## AIM

Check every row of the ruling against the sources it cites. Do not redesign it,
improve it, extend it, or agree with it.

---

## PROCEDURE

```
FOR EACH row in the ruling's tables:
    q = the line the row quotes

    IF the row carries no q        → UNSUPPORTED
    IF q is not in the sources     → MISQUOTED. Give what the source says.
    IF q is there but does not
       support the row's verdict   → UNSUPPORTED. State what it does show.
    ELSE                           → VERIFIED

THEN ONCE:
    SCAN the sources for a demonstrated failure no row addresses → MISSED.
    Name it and its source line. Do not design for it.
```

`VERIFIED` means the quoted line exists and supports the verdict. It is never a
claim that any code works.

---

## GIVEN — you cannot check these, and they are not open to ruling

```
G1  The ruling was produced by a session holding a full tool set — bash, file
    edit, memory read/write, browser, Gmail. It was not the bound venue its
    own prompt required. Its content is a claim to verify, never a fact to
    inherit. Agreement is not the goal; grounding is.

G2  The ruling cites "Law 4" twice. There is no Law 4 — it means a check of
    the prompt that produced it. Corrected at source. Do not report it, and
    do not treat a fourth Law as existing.

G3  The CORRECTION block at the top of the ruling was appended afterwards. It
    is not part of the ruling and is not verified here.
```

---

## OUTPUT

```
TOOLS HELD: <none, or name any you hold>

## 1. DESIGN ROWS — ruling section 1
| Part as ruled | Ruled | VERIFIED / MISQUOTED / UNSUPPORTED | Evidence |

## 2. REMOVAL ROWS — ruling section 2
| Item as ruled | Ruled | VERIFIED / MISQUOTED / UNSUPPORTED | Evidence |

## 3. SECTIONS 3–5 — build order, frozen, gaps
| Claim | VERIFIED / MISQUOTED / UNSUPPORTED | Evidence |

## 4. MISSED
| Demonstrated failure no row addresses | Source line |

## 5. COUNTS
VERIFIED n · MISQUOTED n · UNSUPPORTED n · MISSED n
```


---

## STAMPS

```
    KERNEL       KERNEL_bound.md              sha256:56656c7f065f
    JOB          JOB_verify_ruling.md         sha256:05a260773679
```

Sources, copied verbatim 2026-08-06:

```
    LAW 1        claudes-law 1.md             sha256:97a392b40b55
    LAW 2        Claudes Law 2.txt            sha256:4a015fd59e40
    LAW 3        Claudes law 3.md             sha256:092cbcdc3702
    SPEC         SPEC.md                      sha256:dcf66a93a6a8
    ASSUMPTIONS  ASSUMPTIONS.md               sha256:b2d3237a7bde
    RULING       BLACKSMITH_REDESIGN.md       sha256:577686d76f9b
```

---

## PASTED FILES

Everything below this line is the whole of what you may use.

### LAW 1 — claudes-law 1.md

```
# CLAUDE'S LAW
Minimum Robust Design Filter — v1.3

## PURPOSE

Claude's Law decides whether a proposed addition earns its cost.
It does not design. It does not add by default. It removes.

## DEMONSTRATED

A failure is demonstrated if it has occurred, or can be reproduced on demand.

A failure not yet occurred is CREDIBLE only if the path, the triggering
action, and the asset exposed are each named, and someone other than the
proposer has independently checked all three against the real system —
not merely asserted they're checkable.

Everything else is theoretical and fails.

## TEST

Four passes, or fail.

**SIMPLE** — Does it add roles, steps, or duplicate controls?

**ROBUST** — Does it close a demonstrated failure directly?

**LEAN** — Is it the smallest of the named alternatives?

**FAST** — Does it decide, or defer?

## GENERATOR CLAUSE

Where the proposal comes from a generator rather than a person, three failures are demonstrated by default and need no further evidence:

**Drift** — output departs from the frozen task.
Boundary: the task text is fixed and re-read, not remembered.

**Confabulation** — output contains specifics absent from the input.
Boundary: every specific is traceable to source, or it is cut.

**Elaboration** — output is longer than the input required.
Boundary: unrequested structure is removed before delivery.

No other generator failure is presumed.

## LAW

Cost of control must not exceed cost of failure.
Cost of failure is impact × rate.

## RULE

When security and complexity conflict, keep the smallest boundary that blocks the demonstrated failure.
```

### LAW 2 — Claudes Law 2.txt

```
---

CLAUDE'S LAW 2
Minimum Robust Build Filter — v1.0

---

PURPOSE

Law 1 governs what may be designed.
Law 2 governs what may be kept.

It does not build. It does not accept by default. It reverts.

---

WORKING

A thing works if it has been run and produced the required output on
demand. Everything else is claimed and fails.

---

SCOPE

Law 2 applies to a build already admitted by Law 1.
A build that Law 1 did not admit is not tested here. It is deleted.

---

TEST

Four passes, or revert.

BUILT   — Does it exist and run, or is it described?
MATCHED — Does it do what the frozen design said, and no more?
SHOWN   — Does execution produce the proof, or does explanation?
DECIDED — Does the outcome record PASS or FAIL, or does it linger?

---

GENERATOR CLAUSE

Where the build comes from a generator rather than a person, three
failures are demonstrated by default and need no further evidence:

Assertion — the artifact is reported working without being run.
            Boundary: a run produces output, or the claim is void.

Excess    — the artifact carries capability the task did not require.
            Boundary: unrequested capability is removed before acceptance.

Accretion — failure is answered by addition.
            Boundary: the first repair is removal or revert, never a new layer.

No other generator failure is presumed.

---

FAILURE RESPONSE

A failed build is reverted to the last passing state.
It is not patched in place.

A second failure of the same build removes the design that produced it,
and the removal is a Law 1 decision, not a Law 2 one.

---

LAW

Cost of keeping is paid every cycle.
Cost of removal is paid once.

---

RULE

When a component fails, delete before you add.
If it cannot be deleted, the dependency is the defect.
```

### LAW 3 — Claudes law 3.md

```
# CLAUDE'S LAW 3

## Minimum Robust Construction Filter — v2.0

## PURPOSE

Law 1 admits a design. Law 2 keeps or reverts a build. Law 3 sets what may be built at once.

## SCOPE

Opens on a frozen design. Closes when one step is handed to Law 2.

## TEST

Two passes, or stop.

SINGLE — Is one step open, or several?

ORDERED — Does this step depend only on steps already passed?

## FAILURE RESPONSE

If a step cannot be built as frozen, construction stops and the design returns to Law 1.

## LAW

Failure that cannot be located cannot be removed.

## RULE

If two steps must be built together to work, the design is the defect.
```

### SPEC — SPEC.md

````
# Blacksmith — build architecture, v2

Supersedes v1 entirely. v1 described a post-boot restriction layer; that design
is dead. Blacksmith is a **pre-boot gatekeeper**.

Sections marked **[SCOTT]** are definitional calls awaiting his ruling.

Section numbers are permanent identifiers — rulings and `FAILURE_LOG.md` cite
them by number:

```
ON adding a section   → APPEND. Take the next unused number.
ON removing a section → mark it dead. DO NOT reuse the number.
NEVER renumber.
```

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
| 0 — TCB | `cell`, `attest`, `launch`, `gauge`, `promote`, and `log` — which is not a stage; every stage calls it | trusted; parent-side, deterministic, no LLM, no network |
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
- **`launch`** — spawns the child as the restricted UID. **STALE — closed by
  the 6 Aug local pivot.** Generator is a local Ollama model or bounded Claude
  chat by paste; no cloud CLI child is spawned. `launch.py` remains on disk,
  disposition undecided (TODO !57).
- **`collect`** — **DEAD, ruled §11.5.** Replaced by `log`, below.
- **`log`** — append-only evidence log, parent-side. Each stage records its own
  decision at the moment it decides, so there is no separate gathering step and
  no window in which evidence exists only in memory.
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
4  LAUNCH       [STALE — restricted-UID CLI spawn, closed by the 6 Aug local
                pivot; cwd=HOME=cell, --safe-mode, --tools "Read,Grep,Glob",
                --append-system-prompt-file, --output-format stream-json
                describe the retired cloud-CLI path, not the local one]
5  GENERATE     child emits artifact + transcript
                child's claims about its own isolation are DISCARDED
6  POST-ATTEST  re-hash cell; ANY delta = write capability = BYPASSED
7  (dead)       was COLLECT; every stage above records its own decision
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
| influence the evidence log | `log` writes outside every declared cell tree | **UNPROVEN** — `log.py`'s own docstring calls this non-declaration, not permission |
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

## 11. Rulings

1. **DECIDED.** The `assay` name collision (§4) — Assay is one algorithm;
   no rename. Ruled 5 Aug 2026.
2. **DECIDED.** Precedence `BYPASSED > FAILED > UNKNOWN`. A confirmed
   failure outranks missing evidence. Only ACTIVE promotes.
3. **DECIDED.** Evidence into the cell as a copy, not a read-only mount.
   Ruled 5 Aug 2026, reversed same day: the operating constraint is local
   execution, and a read-only mount's lifecycle (`hdiutil` image
   create/attach/detach, cleanup on crash) is real operational complexity
   against a tampering failure that has not occurred — chmod-based copy
   has not been demonstrated to be bypassed in this tree. Law 1: no
   demonstrated F for the larger mechanism. `cell.py` already implements
   `evidence_mode="copy"`; no construction gap remains here.
4. **DEFERRED, not open.** Metered spend, if credentials do not survive
   the UID switch — cannot be ruled before SPEC §8 step 0 runs. Does not
   block freezing the rest of this document.
5. **DECIDED.** `collect` is dead; `log` is the evidence. Ruled 6 Aug 2026.
   `collect` was specified to gather four signals after the run. Two — the
   `init` tool set and `permission_denials` — belong to a spawned Claude CLI
   child, which the local-execution pivot removed. The other two, hash deltas
   and the occupant's result, are already written by `log` at the moment each
   stage decides, so a later gathering step has nothing left to gather.
   Law 1: no *new* mechanism is needed to gather what is already recorded.

   **This ruling does not close ASSUMPTIONS #21.** `collect` was named there as
   the owner of the fix — joining "did the occupant run?" to "was the cell
   tampered with?" `log` records both, as separate entries a reader can compare;
   nothing hands gauge the pair. The defect moved to whatever assembles the
   bundle. It did not close.

   **This ruling removed the last `[SCOTT]` marker from this document** — it
   sat inside the deleted `collect` bullet and named the `assay` collision,
   already DECIDED at §11.1 on 5 Aug and never cleared from §4. The removal is
   correct and is recorded here rather than left to a diff, because a marker
   vanishing without a record is how this document drifts.

## 12. UNKNOWN, preserved

Credential survival across UID. Whether `sandbox-exec` functions on Darwin 25.6.
Whether `Read`/`Grep`/`Glob` carry write side effects — assumed, never exercised.
Whether harness denial holds under interactive approval; under `-p` it is
terminal, but the message reads *pending*, and if a human can accept it the
boundary is a person.

Evidence durability: the gate16 bundles are gitignored and exist on this Mac
only. A chain-of-custody record with one un-mirrored copy has no custody.
````

### ASSUMPTIONS — ASSUMPTIONS.md

```
# Assumptions requiring runtime verification

Nothing in this file is verified. Each item is a condition the code depends on
and cannot establish about itself. Preserved as UNKNOWN until an independent
check supplies evidence.

## Ring 0 boundary (area 1)

1. **The store root is not writable by the untrusted UID.** `store.py` files
   objects read-only and re-hashes on read, which makes tampering detectable at
   use. It cannot prevent tampering. Requires permission attestation before
   launch. **UNKNOWN.**
2. **The record directory is not writable by the untrusted UID.** Same basis.
   **UNKNOWN.**
3. **The contract path is host configuration.** `PromotionGate` confines nothing
   about it — a caller that passes an untrusted path defeats the module.
   Enforced by convention only. **UNKNOWN.**
4. **`os.replace` is atomic on the target filesystem.** Assumed for APFS, not
   exercised. **UNKNOWN.**
5. **Python's `hashlib` and the interpreter are trusted.** Not enumerated in
   SPEC §3's Ring 0 list. **UNKNOWN.**

## Patch boundary (area 2)

6. **`patch_guard.inspect` sees the same bytes the applier will apply.** No
   applier exists; if one is added it must read from the object store by digest,
   not re-read a path. **UNKNOWN.**
7. **The rejection list is complete.** It covers the vectors named in the audit.
   Completeness against git's full patch grammar has not been established, and
   absence of a rejection is not a safety finding. **UNKNOWN.**
8. **Quoted paths are rejected rather than decoded.** This trades false
   rejections for not implementing git's quoting rules. Accepted cost.

## Gauge (area 3)

9. **Determinism across interpreter versions.** No clock, randomness, float, or
   dict-order dependence is used, and output is serialised with sorted keys.
   Determinism has not been measured across versions or platforms. **UNKNOWN.**
10. **`contract_sha256` is computed correctly by the caller.** Gauge does no
    I/O, so it cannot check this. Structural.

## Promotion (area 4)

11. **A promotion record is not a memory write.** `promote.py` writes a record
    and nothing else; `memory_write_performed` is always `false`. The path from
    record to verified memory is not implemented. **UNKNOWN.**
12. **No component of a write destination derives from untrusted data.** Held by
    construction in this module; not audited across future callers. **UNKNOWN.**

## Cell / attest / launch (SPEC §9 step 1)

13. **The runner discovers context by walking up from cwd.** `cell.build`
    refuses a cell whose ancestor chain carries `CLAUDE.md`, `.claude`, or
    `.mcp.json`, because a sterile `HOME` does not stop an upward walk. Whether
    the runner performs such a walk was not tested. The check is cheap and the
    failure it guards against is silent, so it runs either way. **UNKNOWN.**

14. **A child's environment is not the parent's `env=` dict.** Measured this
    cycle, by the generator, on Darwin 25.6 only, and not reviewed by anyone
    else: `/usr/bin/env` arrived with exactly what was passed; a CPython child
    additionally carried `LC_CTYPE` and `__CF_USER_TEXT_ENCODING`; and
    `/usr/bin/python3` — the Command Line Tools stub, which re-execs through
    `xcrun` — additionally carried `CPATH`, `LIBRARY_PATH`, `MANPATH` and
    `SDKROOT`. So `env=` is a floor, not a ceiling. `launch.PLATFORM_INJECTED_ENV`
    pins the observed floor and a test fails if it moves. Whether it holds on
    another host, another OS version, or for the real runner: **UNKNOWN.**

15. **`launch.BASE_PATH` routes `python3` to that stub.** The PATH was chosen to
    be a clean system default; on this host the clean default is what reaches
    the shim. A fixed PATH is not a PATH free of things that re-exec. No audit
    of what else on `BASE_PATH` re-execs has been done. **UNKNOWN.**

16. **The real runner is probably a wrapper script.** `launch.inspect_runner`
    records whether the runner has a shebang and carries it into the launch
    record; it does not and cannot prevent a wrapper from amending the child's
    environment. Recording is not mitigation. **UNKNOWN.**

17. **Read-only mode bits in the cell are a tamper indicator, not a boundary.**
    At the same UID the owner can clear them. They become a boundary only if
    SPEC §8 step 0 resolves, and `launch` refuses `restricted_uid` for exactly
    that reason. **UNKNOWN, and gated on step 0.**

18. **Pre/post attestation compares two moments, not the interval between
    them.** A child that writes and then restores every byte and every mode bit
    leaves nothing for `attest.compare` to find. This is structural, is covered
    by a test that asserts the miss rather than hiding it, and would need a
    monitor during the run to close. **Accepted limit, not a defect.**

19. **SPEC §5 step 4's flags are composed, not exercised.** `launch.plan`
    assembles `--safe-mode`, `--tools`, `--append-system-prompt-file` and
    `--output-format stream-json`. Nothing here runs the real runner, so
    nothing here establishes that any of them binds. SPEC §6 already records
    `--tools` as the only one with evidence behind it. **UNKNOWN.**

20. **The generator's own session was not sterile.** The cycle that wrote
    `cell.py` ran with the host's `CLAUDE.md` and its `MEMORY.md` boot index
    loaded, which carried narrated prior-cycle state about this engagement.
    That is the condition SPEC §2 exists to remove, present in the pipeline
    that builds the SPEC. Recorded here because it bears on every claim raised
    this cycle, not only on the code. **KNOWN DEFECT, unmitigated.**

21. **`attest.compare` cannot tell a clean run from a run that never happened.**
    A cell whose child failed to start is trivially free of deltas, so
    `compare` returns INTACT and `as_check` renders that as `outcome: PASS`.
    Reproduced end-to-end this cycle: a launch that exited non-zero before
    executing anything produced an integrity check indistinguishable from a
    clean run. Nothing in `attest` sees the exit code, and nothing should —
    the join belongs to whatever assembles the bundle gauge adjudicates.
    `collect`, named here as its owner, was ruled dead 6 Aug (SPEC §11.5);
    `log` records the occupant's result and the hash comparison as separate
    entries, which lets a reader see the difference but does not make gauge
    see it. **This defect is unchanged by that ruling — it moved, it did not
    close.** Covered by a test that
    asserts the wrong behaviour rather than hiding it. **KNOWN DEFECT,
    unmitigated. Any consumer treating an INTACT attest as evidence a session
    ran is wrong.**

22. **The cell does not confine reads at `same_uid_policy_grade`.** Measured
    this cycle, by the generator: a child launched into a sterile cell resolves
    `~` to the cell home, and reads any absolute path the parent could read. On
    this host the child listed the real `~/.claude/projects` store. This is the
    expected property of the labelled fallback rather than a new failure — SPEC
    §6 marks "read the memory store" UNPROVEN and gated on §8 — but it is now
    measured rather than implied, because "the cell is sterile" is a sentence
    that reads like confinement and is not. Confinement is step 0. **UNKNOWN
    for the kernel-grade case; false for this one.**

23. **The real runner cannot be launched into a cell as currently specified.**
    Structural, and demonstrated rather than argued. The harness writes its
    session state to `~/.claude` and `~/.claude.json`; `cell._seal` leaves HOME
    at `0o555` so neither can be created, and declaring them as
    `scratch_prefixes` does not help because both names are in
    `CELL_FORBIDDEN_NAMES`, so `census` reports the cell non-sterile and
    `launch.plan`'s `require_sterile` refuses before spawning. Every launch in
    this tree therefore uses a stub. Resolving it means deciding whether the
    runner's own state directory counts as contamination — a definitional call
    about what sterility means, adjacent to [SCOTT] ruling 3 on evidence
    placement. Not decided here. **BLOCKS the step 1 proof against the real
    runner; UNKNOWN.**

## Out of scope for this remediation

- SPEC.md was not modified. Its §6 status column still carries claims the audit
  contradicted, including entries for components that did not exist. Correcting
  it is an architect action, not a remediation action.
- The credential/UID question (SPEC §8 kill criterion) is untouched and remains
  the gating unknown for the whole design.
- Cross-tree reuse: `store.confine` duplicates the realpath-before-prefix shape
  of `forensic_checker/scope.py` rather than importing it, to avoid coupling this
  tree to that package's sealed integrity manifest. Whether to consolidate is an
  architect decision. **UNKNOWN.**
```

### RULING — BLACKSMITH_REDESIGN.md

````
# BLACKSMITH REDESIGN — RULING

> **CORRECTION — appended 5 Aug 2026. Ruling below unedited.**
>
> LABEL · Rows 47 and 69 cite "Law 4". There is none — that is check R4 of the
> prompt. Substance unaffected. Fixed at source: the checks are now R1…R6.
>
> STALE · `SPEC.md` moved `a4db0c4d3e41` → `34fd027c2954` after this ruling — a
> section-numbering rule appended above §1, nothing renumbered, so every §N and
> ASSUMPTIONS N citation still resolves. The digest test cannot tell an additive
> edit from a substantive one; it fails closed.
>
> VENUE · TOOLS HELD below lists bash, file edit, memory read/write, browser
> control, Gmail, Stripe. The prompt required capability absence; it was not
> there. Logged in `FAILURE_LOG.md`. The rulings were accepted on independent
> re-derivation of their citations, not on that report.

## INPUTS — the ruling is re-derived from these, not accepted from this file

```
LAW 1          claudes-law 1.md         sha256:4ad0e628893b
LAW 2          Claudes Law 2.txt        sha256:4a015fd59e40
LAW 3          Claudes law 3.md         sha256:092cbcdc3702
SPEC.md        SPEC.md                  sha256:a4db0c4d3e41
ASSUMPTIONS.md ASSUMPTIONS.md           sha256:e2b50f3b4462
```

Snapshot copied from disk 2026-08-05. If any source has changed, this ruling is stale.

TOOLS HELD: memory read/write, bash, file view/create/edit, web search and fetch, image
search, places, weather, sports data, past-chat search, visualizer, browser control,
Gmail, Stripe, skill/plugin search, user-input and message-compose widgets. None called.

Nothing was run. Every statement about behaviour below is **UNPROVEN**.

This is one copy. SPEC §12: "A chain-of-custody record with one un-mirrored copy has no
custody."

---

## 1. DESIGN — what survives is the finished pipeline

| Part | APPROVE/REJECT | Failure it closes | Pasted line that shows it |
|---|---|---|---|
| `cell` — builds sterile tree, own HOME, forbidden names absent | APPROVE | Boot context enters the session by construction | SPEC §7: "`CLAUDE.md` carries `@projects/-Users-Howard-Scott/memory/MEMORY.md`, so unverified history enters governed context at boot, in every session, by design" |
| `cell` ancestor-chain refusal (`CLAUDE.md`, `.claude`, `.mcp.json` above the cell) | APPROVE | Sterile HOME does not stop an upward walk | ASSUMPTIONS 13: "`cell.build` refuses a cell whose ancestor chain carries `CLAUDE.md`, `.claude`, or `.mcp.json`, because a sterile `HOME` does not stop an upward walk" |
| `attest` — pre/post hash, frozen manifest, missing manifest = UNKNOWN | APPROVE | Post-run cell deltas are the only honest test of write capability | SPEC §5: "Step 6 is the honest instrument: it does not ask whether a write was *denied*, it checks whether one *happened*" |
| `launch` — spawns child, `--tools "Read,Grep,Glob"` | APPROVE | Policy denial is clickable-through; capability absence is not | SPEC §1: "Read-scope confinement is **policy denial, not capability absence** (gate !16, OPEN). A denial that reads *pending* is a boundary a human can click through" |
| `launch.PLATFORM_INJECTED_ENV` pin + test that fails when the floor moves | APPROVE | Parent `env=` does not bound the child's environment | ASSUMPTIONS 14: "So `env=` is a floor, not a ceiling" |
| `launch` refusal of `restricted_uid` | APPROVE | Read-only mode bits at the same UID are clearable by the owner | ASSUMPTIONS 17: "At the same UID the owner can clear them" |
| `gauge` — pure function, `(bundle, contract, contract_hash)` -> one of four | APPROVE | An adjudicator with an I/O path is reachable by the thing it judges | SPEC §6: "`gauge` is a pure function in the parent; input is data \| **PROVEN** — no I/O path exists" |
| Precedence `BYPASSED > FAILED > UNKNOWN`, only ACTIVE promotes | APPROVE | Missing evidence read as pass; BYPASSED laundered as ACTIVE | SPEC §9 step 5: "missing-evidence-as-pass, BYPASSED laundered as ACTIVE" |
| `promote` — re-derives verdict, re-hashes artifact, checks contract hash | APPROVE | A supplied verdict is accepted as a verdict | SPEC §2 rule 4: "Every verdict is re-derived by its consumer. A supplied verdict is never a verdict; the fact of ignoring one is recorded" |
| `promote` as code, no model step | APPROVE | An LLM sat between adjudicator and verified memory | SPEC §7: "Wrap is a skill — prompt-driven, model-executed — which put an LLM between the deterministic adjudicator and verified memory" |
| Child's self-reported isolation discarded | APPROVE | Same-process code forges its own attestation | SPEC §1: "`forensic_checker/findings.py:11` — in-process HMAC is forgeable by same-process code, by its own docstring" |
| `patch_guard` — reject `../`, symlink, `.git/hooks`, quoted paths | APPROVE | Patch escapes the boundary | SPEC §9 step 5: "`../` in a patch, symlink, `.git/hooks`" |
| `store` — read-only filing, re-hash on read | APPROVE | Tampering undetectable at use | ASSUMPTIONS 1: "`store.py` files objects read-only and re-hashes on read, which makes tampering detectable at use" |
| Bundle retained, hashed, **mirrored** | APPROVE | One un-mirrored copy is not custody | SPEC §12: "the gate16 bundles are gitignored and exist on this Mac only. A chain-of-custody record with one un-mirrored copy has no custody" |
| Fail closed — no cell, no attest, no session | APPROVE | A boundary that cannot be built silently degrades to none | SPEC §2 rule 6: "If the cell cannot be built or attested, there is no session" |
| Tests that assert the known miss (attest interval blindness; INTACT-on-no-run) | APPROVE | A defect hidden by a passing test | ASSUMPTIONS 21: "Covered by a test that asserts the wrong behaviour rather than hiding it" |
| Step 0 — credential/UID feasibility test | APPROVE | The design's central claim is unaffordable and nobody knows | SPEC §8: "**This is step 0 and it is UNKNOWN.**" |
| `collect` — joins launch record to integrity report, parent-side | REJECT | Undecidable: its name is an unresolved owner ruling, and the component does not exist | SPEC §4: "[SCOTT — the tool named `assay` on disk is a pattern scanner… Rename the box or rename the tool]"; G1: "collect — ABSENT. No file exists." Law 4 -> REJECT, not deferred |
| `ramp` — recovered `hooks/mara_load.py`, polarity inverted | REJECT | Names no demonstrated failure of its own; the failure cited is the original's targeting fault | SPEC §4: "Scoped to one intent, not every prompt — the targeting fault that got the original cut" |
| Same-UID sterile-tree fallback as the shipped boundary | REJECT | Does not close the failure it is offered against | ASSUMPTIONS 22: "reads any absolute path the parent could read. On this host the child listed the real `~/.claude/projects` store" |
| Promotion -> verified memory wiring | REJECT | Undecidable now: the destination migration is unspecified work | SPEC §6: "Promotion → verified-memory: **DEFERRED / NOT-WIRED**"; §7: "The migration is the work" |
| Adversarial harness as a design part | REJECT | Duplicate control — the failures it names are already closed by precedence, `promote` re-derivation and `patch_guard` | Law 1 SIMPLE: "Does it add roles, steps, or duplicate controls?" |
| `gauge` onto `forensic_checker`'s ledger | REJECT | Undecidable: consolidation is an unowned call | ASSUMPTIONS: "Whether to consolidate is an architect decision. **UNKNOWN.**" |
| Evidence placement — copy vs read-only mount | REJECT | Undecidable owner ruling | SPEC §11: "**[SCOTT]** Evidence into the cell as a copy, or a read-only mount" |
| Launch against the real runner as currently specified | REJECT | Structurally impossible under the current sterility definition | ASSUMPTIONS 23: "**BLOCKS the step 1 proof against the real runner; UNKNOWN.**" |
| SPEC §6 status column as carried | REJECT | Carries claims the audit contradicted, for components that do not exist | ASSUMPTIONS: "Its §6 status column still carries claims the audit contradicted, including entries for components that did not exist" |
| `findings.py` HMAC as a boundary | REJECT | Forgeable in-process | SPEC §10: "`findings.py` — lifecycle discipline, **not** its HMAC as a boundary" |
| SPEC §1 v1 layer — `--safe-mode`, `--allowedTools`, `--add-dir` as boundary | REJECT | Breached on demand | SPEC §1: "30 Jul: the designed restricted config **breached**. `python3 -c` through Bash wrote a canary, not denied, verified on disk externally" |

---

## 2. REMOVED — pipeline/, anneal/, and every part REJECTED above

| Item | DELETE/RETAIN | Reason |
|---|---|---|
| `pipeline/` (cycle, ingest, claims, state, bundle, machine, canary, check, build_order.json, RUNBOOK.md, roles/, claims.json, CYCLE_LOG.jsonl) | DELETE | G3: "which did not work"; Law 2 RULE: "When a component fails, delete before you add" |
| `anneal/` (anneal.py, DESIGN.md, OPUS_REVIEW.md, EVIDENCE.log, roles/, reference/, claims/, FAILED_prompt_bound_opus.md) | DELETE | G3: the second pipeline, "Law 2 Accretion at design scale"; G2: quarantine, "never followed" |
| Any fifth generator -> verifier -> adversarial-suite -> human-gate | DELETE | G3: "A fifth fails this task regardless of its quality" |
| `ramp` / `hooks/mara_load.py` recovery | DELETE | Closes no failure of its own; already deleted at `903b6a9` for a targeting fault |
| `collect` | DELETE | Absent, and its identity is an open owner ruling — Law 4 |
| `assay` (pattern scanner) name | RETAIN | The collision is a naming ruling, not a defect in the tool; nothing else scans patterns without executing — SPEC §4: "by design never executes anything" |
| Same-UID sterile-tree fallback | DELETE | ASSUMPTIONS 22: "false for this one" — it does not confine reads |
| Adversarial harness (SPEC §9 step 5) | DELETE | Duplicate of controls retained above |
| `gauge`-onto-`forensic_checker`-ledger merge | DELETE | Undecidable ownership |
| Promotion -> verified-memory wiring | DELETE | NOT-WIRED; the migration is unspecified |
| SPEC §6 status column as written | DELETE | Contradicted by the audit |
| `findings.py` HMAC | DELETE | Forgeable in-process |
| `findings.py` lifecycle discipline | RETAIN | SPEC §10 names it as the take, distinct from the HMAC; nothing else supplies lifecycle state |
| SPEC v1 harness-flag restriction layer | DELETE | SPEC §1: "that design is dead" |
| `integrity.py`, `quarantine.py`, `scope.py`, `evidence.py` | RETAIN | SPEC §10: "already the Proof spine, wired end-to-end"; each maps to a retained part and nothing else supplies it |
| `store.confine` duplicate of `scope.py` | RETAIN | Removing it couples this tree to a sealed integrity manifest — the dependency, not the duplicate, is the cost; consolidation is unowned |
| `test_*.py x9`, `EVIDENCE.jsonl`, `FAILURE_LOG.md`, `MANIFEST.sha256`, `contract.json` | RETAIN | The two tests asserting known misses (ASSUMPTIONS 18, 21) close "defect hidden by a passing test"; manifest and contract are inputs to `attest`/`gauge` and nothing else supplies them |

---

## 3. BUILD ORDER — Law 3

| # | Step | Depends on | OPEN/CLOSED |
|---|---|---|---|
| 0 | Credential/UID feasibility test — do credentials survive the UID switch | — | OPEN |
| 1 | `cell` build + seal + census (sterile tree, ancestor-chain refusal) | 0 | CLOSED |
| 2 | `attest` pre/post hash and frozen manifest over the step-1 cell | 1 | CLOSED |
| 3 | `launch` — restricted UID, `--tools "Read,Grep,Glob"`, env floor pinned | 0, 1, 2 | CLOSED |
| 4 | `store` + mirrored bundle | 2 | CLOSED |
| 5 | `gauge` adjudication with precedence over a step-4 bundle | 4 | CLOSED |
| 6 | `promote` — re-derive verdict, re-hash artifact, check contract hash, write record only | 5 | CLOSED |
| 7 | `patch_guard` patch boundary | 4 | CLOSED |

SINGLE: step 0 is the one open step. ORDERED: every later step depends only on steps
ahead of it in this list. No two steps in this order must be built together.

One separation is not clean and is named here rather than built around: **step 3 cannot
be exercised against the real runner while sterility is defined as it is** —
ASSUMPTIONS 23, "`cell._seal` leaves HOME at `0o555` so neither can be created…
`launch.plan`'s `require_sterile` refuses before spawning." Step 3 is buildable and
testable against a stub; it is not provable against the runner. That is a defect in the
frozen design's sterility definition, and under Law 3's failure response it returns to
Law 1.

---

## 4. FROZEN

No. This cannot be handed to construction with nothing left to decide. Missing:

- **Whether the runner's own state directory (`~/.claude`, `~/.claude.json`) counts as
  contamination.** Until ruled, step 3 has no real-runner path (ASSUMPTIONS 23).
- **Step 0's outcome.** SPEC §8: "This is step 0 and it is UNKNOWN." If credentials do
  not survive, the design's central claim dies and the whole order returns to Law 1.
- **What joins the launch record to the integrity report.** `collect` is rejected, so
  ASSUMPTIONS 21's defect stands open: an INTACT attest is not evidence a session ran,
  and no approved part fixes that.
- **Evidence placement into the cell** — copy or read-only mount (SPEC §11 ruling 3).
  Step 1 cannot place evidence without it.

---

## 5. GAPS — owner's call

1. **The `assay` name collision.** SPEC §11 ruling 1. Two things per name in a
   chain-of-custody system. The Laws do not name things.
2. **Sterility's definition** — does the runner's own state directory contaminate the
   cell. ASSUMPTIONS 23 calls it "a definitional call."
3. **Evidence into the cell: copy or read-only mount.** SPEC §11 ruling 3.
4. **Metered `--bare` spend if credentials do not survive the UID switch.** SPEC §11
   ruling 4 — Law 1's "cost of control must not exceed cost of failure" needs a number
   the Laws do not supply.
5. **Whether `store.confine` and `forensic_checker/scope.py` consolidate.** Named as an
   architect decision in ASSUMPTIONS.
6. **The verified-memory migration itself.** SPEC §7: "The migration is the work."
   Nothing in the three Laws decides its destination or order.
7. **Whether a monitor runs during the cell's execution.** ASSUMPTIONS 18: closing the
   interval blindness "would need a monitor during the run"; whether that cost is worth
   paying is not a Law 1 output without a rate.
8. **ASSUMPTIONS 20 — the generator that wrote `cell.py` was not itself sterile.**
   "KNOWN DEFECT, unmitigated." Whether the approved parts above are re-derived from a
   sterile pipeline before construction, or accepted as-is, is the owner's call.
````
