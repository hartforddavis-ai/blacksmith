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
