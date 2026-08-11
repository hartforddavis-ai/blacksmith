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
    this tree therefore uses a stub.

    **PARTIALLY RESOLVED 11 Aug 2026 (TODO !57).** Not by ruling on whether
    `.claude`/`.claude.json` count as contamination — `FAILURE_LOG.md`'s
    "step 3 is untestable until the owner rules" entry killed that framing
    outright (Law 2: a step that can't run fails BUILT; Law 3: a fix
    depending on someone else's ruling is one decision split into two
    dependent steps). Instead: `launch.plan()` gained a `claude_config_dir`
    argument, confined to the cell and checked against the built cell's own
    declared `scratch_prefixes` before spawn. Set as `CLAUDE_CONFIG_DIR` in
    the child's environment, it redirects a real Claude Code runner's startup
    writes away from the forbidden literal path entirely — `CELL_FORBIDDEN_
    NAMES` is untouched, and the collision this item names simply never
    happens. Proven against a real spawned child in `test_lifecycle_proof.py`
    (`ClaudeConfigDirTests`): a write under the redirected path lands as a
    declared scratch delta and reads INTACT; the literal `~/.claude.json`
    write is still refused, unchanged.

    **What this does not prove.** No test here has ever run the actual
    `claude` binary — every launch, including this one, uses a stub script
    (see `test_lifecycle_proof.py`'s own module docstring). Whether the real
    CLI honours `CLAUDE_CONFIG_DIR` as expected, and whether SPEC §5 step 4's
    flags (`--safe-mode`, `--tools`) bind, are unproven — ASSUMPTIONS #19,
    untouched by this fix. The kernel-grade contamination question for the
    real runner also stays open on its own terms; this item only closes the
    same-UID structural collision.**

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
