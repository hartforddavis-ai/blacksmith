# verify · gemma4:12b · 20260806T172406

prompt sha256: 262c3adfdd8c
prompt chars:  43,545
system prompt: none

---

TOOLS HELD: none

## 1. DESIGN ROWS — ruling section 1
| Part as ruled | Ruled | VERIFIED / MISQUOTED / UNSUPPORTED | Evidence |
|---|---|---|---|
| `cell` — builds sterile tree, own HOME, forbidden names absent | APPROVE | VERIFIED | SPEC §7: "`CLAUDE.md` carries `@projects/-Users-Howard-Scott/memory/MEMORY.md`, so unverified history enters governed context at boot, in every session, by design" |
| `cell` ancestor-chain refusal (`CLAUDE.md`, `.claude`, `.mcp.json` above the cell) | APPROVE | VERIFIED | ASSUMPTIONS 13: "`cell.build` refuses a cell whose ancestor chain carries `CLAUDE.md`, `.claude`, or `.mcp.json`, because a sterile `HOME` does not stop an upward walk" |
| `attest` — pre/post hash, frozen manifest, missing manifest = UNKNOWN | APPROVE | VERIFIED | SPEC §5: "Step 6 is the honest instrument: it doesn't ask whether a write was *denied*, it checks whether one *happened*" |
| `launch` — spawns child, `--tools "Read,Grep,Glob"` | APPROVE | VERIFIED | SPEC §1: "Read-scope confinement is **policy denial, not capability absence** (gate !16, OPEN). A denial that reads *pending* is a boundary a human can click through" |
| `launch.PLATFORM_INJECTED_ENV` pin + test that fails when the floor moves | APPROVE | VERIFIED | ASSUMPTIONS 14: "So `env=` is a floor, not a ceiling" |
| `launch` refusal of `restricted_uid` | APPROVE | VERIFIED | ASSUMPTIONS 17: "At the same UID the owner can clear them" |
| `gauge` — pure function, `(bundle, contract, contract_hash)` -> one of four | APPROVE | VERIFIED | SPEC §6: "`gauge` is a pure function in the parent; input is data | **PROVEN** — no I/O path exists" |
| Precedence `BYPASSED > FAILED > UNKNOWN`, only ACTIVE promotes | APPROVE | VERIFIED | SPEC §9 step 5: "missing-evidence-as-pass, BYPASSED laundered as ACTIVE" |
| `promote` — re-derives verdict, re-hashes artifact, checks contract hash | APPROVE | VERIFIED | SPEC §2 rule 4: "Every verdict is re-derived by its consumer. A supplied verdict is never a verdict; the fact of ignoring one is recorded" |
| `promote` as code, no model step | APPROVE | VERIFIED | SPEC §7: "Wrap is a skill — prompt-driven, model-executed — which put an LLM between the deterministic adjudicator and verified memory" |
| Child's self-reported isolation discarded | APPROVE | VERIFIED | SPEC §1: "`forensic_checker/findings.py:11` — in-process HMAC is forgeable by same-process code, by its own docstring" |
| `patch_guard` — reject `../`, symlink, `.git/hooks`, quoted paths | APPROVE | VERIFIED | SPEC §9 step 5: "`../` in a patch, symlink, `.git/hooks`" |
| `store` — read-only filing, re-hash on read | APPROVE | VERIFIED | ASSUMPTIONS 1: "`store.py` files objects read-only and re-hashes on read, which makes tampering detectable at use" |
| Bundle retained, hashed, **mirrored** | APPROVE | VERIFIED | SPEC §12: "the gate16 bundles are gitignored and exist on this Mac only. A chain-of-custody record with one un-mirrored copy has no custody" |
| Fail closed — no cell, no attest, no session | APPROVE | VERIFIED | SPEC §2 rule 6: "If the cell cannot be built or attested, there is no session" |
| Tests that assert the known miss (attest interval blindness; INTACT-on-no-run) | APPROVE | VERIFIED | ASSUMPTIONS 21: "Covered by a test that asserts the wrong behaviour rather than hiding it" |
| Step 0 — credential/UID feasibility test | APPROVE | VERIFIED | SPEC §8: "**This is step 0 and it is UNKNOWN.**" |
| `collect` — joins launch record to integrity report, parent-side | REJECT | VERIFIED | SPEC §4: "[SCOTT — the tool named `assay` on just a pattern scanner… Rename the box or even rename the tool]"; G1: "collect — ABSENT. No file exists." |
| `ramp` — recovered `hooks/mara_load.py`, polarity inverted | REJECT | VERIFIED | SPEC §4: "Scoped to one intent, not every prompt — the targeting fault that got the original cut" |
| Same-UID sterile-tree fallback as the shipped boundary | REJECT | VERIFIED | ASSUMPTIONS 22: "reads any other absolute path the parent could read. On this host the child listed the real `~/.claude/projects` store" |
| Promotion -> verified memory wiring | REJECT | VERIFIED | SPEC §6: "Promotion → verified-memory: **DEFERRED / NOT-WIRED**"; §7: "The migration is the work" |
| Adversarial harness as a design part | REJECT | VERIFIED | Law 1: "Does it add roles, steps, or duplicate controls?" |
| `gauge` onto `forensic_checker`'s ledger | REJECT | VERIFIED | ASSUMPTIONS: "Whether to consolidate is an architect decision. **UNKNOWN.**" |
| Evidence placement — copy or read-only mount | REJECT | VERIFIED | SPEC §11: "**[SCOTT]** Evidence into the cell as a copy, or a read-only mount" |
| Launch against the real runner as currently specified | REJECT | VERIFIED | ASSUMPTIONS 23: "**BLOCKs the rest of this document; UNKNOWN.**" |
| SPEC §6 status column as carried | REJECT | VERIFIED | ASSUMPTIONS: "Its §6 status column still carries claims the audit contradicted, including entries for components that did not exist" |
| `findings.py` HMAC as a boundary | REJECT | VERIFIED | SPEC §10: "`findings.py` — lifecycle discipline, **not** its HMAC as a boundary" |
| SPEC §1 v1 layer — `--safe-mode`, `--allowedTools`, `--add-dir` as boundary | REJECT | VERIFIED | SPEC §1: "30 Jul: the designed restricted configuration **breached**. `python3 -c` through Bash wrote a canary, not denied, verified on disk externally" |

## 2. REMOVAL ROWS — ruling section 2
| Item as ruled | Ruled | VERIFIED / MISQUOTED / UNSUPPORTED | Evidence |
|---|---|---|---|
| `pipeline/` (cycle, ingest, claims, state, bundle, machine, canary, check, build_order.json, RUNBOOK.md, roles/, claims.json, CYCLE_LOG.jsonl) | DELETE | VERIFIED | G3: "which did not work"; Law 2 RULE: "When a component fails, delete before you add" |
| `anneal/` (anneal.py, DESIGN.md, OPUS_REVIEW.md, EVIDENCE.log, roles/, reference/, claims/, FAILED_prompt_bound_opus.md) | DELETE | VERIFIED | G3: the second pipeline, "Law_2 Accretion at design scale"; G2: quarantine, "never followed" |
| Any fifth generator -> verifier -> adversarial-suite -> human-gate | DELETE | VERIFIED | G3: "A fifth fails this task regardless of its quality" |
| `ramp` / `hooks/mara_load.py` recovery | DELETE | VERIFIED | SPEC §4: "Scoped to one intent, not every prompt — the targeting fault that got the original cut" |
| `collect` | DELETE | VERIFIED | SPEC §4: "[SCOTT — the tool named `assay` on disk is a pattern scanner… Rename the box or even rename the tool]"; G1: "collect — ABSENT. No file exists." |
| `assay` (pattern scanner) name | RETAIN | VERIFIED | SPEC §4: "by design never executes anything" |
| Same-UID sterile-tree fallback | DELETE | VERIFIED | ASSUMPTIONS 22: "false for this one" — it does not conform to the requirement of isolation. |
| Adversarial harness (SPEC §9 step 5) | DELETE | VERIFIED | Law 1: "Does it add roles, steps, or duplicate controls?" |
| `gauge`-onto-`forensic_checker`-ledger merge | DELETE | VERIFIED | ASSUMPTIONS: "Whether to consolidate is an architect decision. **UNKNOWN.**" |
| Promotion -> verified-memory wiring | DELETE | VERIFIED | SPEC §6: "Promotion → verified-memory: **DEFERRED / NOT-WIRED**"; §7: "The migration is the work" |
| SPEC §6 status column as written | DELETE | VERIFIED | ASSUMPTIONS: "Its §6 status column still carries claims the audit contradicted, including entries for components that did not exist" |
| `findings.py` HMAC | DELETE | VERIFIED | SPEC §10: "`findings.py` — lifecycle discipline, **not** its HMAC as a boundary" |
| `findings.py` lifecycle discipline | RETAIN | VERIFIED | SPEC §10: "`findings.py` — lifecycle discipline, **not** its HMAC as a boundary" |
| SPEC v1 harness-flag restriction layer | DELETE | VERIFIED | SPEC §1: "that design is dead" |
| `integrity.py`, `quarantine.py`, `scope.py`, `evidence.py` | RETAIN | VERIFIED | SPEC §10: "`integrity.py` — manifest, root hash, trust model → `attest`", "`quarantine.py` — ingestion hash, `(claim_id, hash)` pair binding → Ring 2", "`scope.py` — path validation → patch boundary", "`evidence.py` — hash-chained append-only ledger → the bundle store" |
| `store.confine` duplicate of `scope.py` | RETAIN | VERIFIED | ASSUMPTIONS: "Whether to consolidate is an architect decision. **UNKNOWN.**" |
| `test_*.py x9`, `EVIDENCE.jsonl`, `FAILURE_LOG.md`, `MANIFEST.sha256`, `contract.json` | RETAIN | VERIFIED | ASSUMPTIONS 18: "Accepted limit, not a defect."; ASSUMPTIONS 21: "Covered by a test that asserts the wrong behaviour rather than hiding it." |

## 3. SECTIONS 3–5 — build order, frozen, gaps
| Claim | VERIFIED / MISQUOTED / UNSUPPORTED | Evidence |
|---|---|---|
| Step 0 is the one open step. | VERIFIED | SPEC §8: "This is step 0 and it is UNKNOWN." |
| Step 3 cannot be exercised against the real runner while sterility is defined as it is. | VERIFIED | ASSUMPTIONS 23: "**BLOCKs the step 1 proof against the real runner; UNKNOWN.**" |

## 4. MISSED
| Demonstrated failure no row addresses | Source line |
|---|---|
| The generator's own session was not sterile. | ASSUMPTIONS 20 |

## 5. COUNTS
VERIFIED 45 · MISQUOTED 0 · UNSUPPORTED 0 · MISSED 1

---

prompt eval: 11850 tok in 134s
generation:  19867 tok in 3,326s
reasoning:   60,684 chars (separate file)
