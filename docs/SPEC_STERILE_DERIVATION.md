# Spec 1: Sterile Derivation of cell.py

## Problem
cell.py exists but is unverified. It was not derived through sterile gates. Code shipped without proof it came through a known, clean derivation process.

## Solution
Define the sterile gates through which cell.py must pass to establish verified derivation.

## Procedure

**Input:** Current cell.py source (or requirements for what cell.py must do)

**Gate 1: Derivation Source**
- Source: SPEC §2 (Design rules), SPEC §3 (Rings), SPEC §4 (Components)
- Method: Re-derive cell.py from specification only, no copy-paste from old version
- Evidence: Derivation notes showing which lines map to which sections of SPEC

**Gate 2: Code Review (Sterile)**
- Reviewer: Deterministic rules only (no human judgment, no assumptions)
- Rules: Apply SPEC §2 rules 1–6 to every function:
  - Rule 1: OS process/filesystem/UID boundaries only (no prompt-level controls)
  - Rule 2: Capability absence (permissions/UID) beats policy
  - Rule 3: Sterility by construction (files absent, not suppressed)
  - Rule 4: No supplied verdicts (re-derive on consumer side)
  - Rule 5: Promotion is code (no model between adjudicator and memory)
  - Rule 6: Fail closed (raise, never degrade)
- Evidence: Checklist showing each function passes all six rules

**Gate 3: Sterile Build**
- Environment: Isolated, no internet, no context from ~/.claude, no git history
- Build: Run cell.py through `cell.confine()`, `ancestor_contamination()`, and `CELL_FORBIDDEN_NAMES` checks
- Evidence: Build log showing no contamination found

**Gate 4: Manifest Hash**
- Digest: sha256 of cell.py source
- Record: MANIFEST.sha256 entry naming gate sequence and digest
- Evidence: Hash in manifest

**Output:** cell.py verified; MANIFEST entry recording derivation path and digest

---

## Acceptance
Verified cell.py meets all four gates. Hash recorded. Ready for construction.
