# Spec 3: Bundle Mirroring — Redundant Custody

## Problem
Bundles (gitignored, stored on one Mac) are single-copy. Hardware failure = loss of custody chain. No redundancy.

## Solution
Create and maintain mirror copies of bundles in a separate location. Define location, sync mechanism, and verification.

---

## Locations

**Primary storage:** `/Users/Howard Scott/Documents/_PROJECTS/SOFTWARE/blacksmith/runs/` (gitignored)
- Contains: `<job>.<model>.<timestamp>.md` output files
- Ownership: Local; not synced to GitHub

**Mirror storage:** To be determined by Scott
- Options: External drive, network storage, second Mac, cloud sync
- Requirement: Not on the same machine as primary (hardware failure isolation)

---

## Sync Procedure

**Trigger:** After every run completes
- Source: Primary bundle (runs/*.md)
- Destination: Mirror storage
- Method: Copy (not move); primary and mirror both retain the file

**Verification:**
- Hash both files (sha256)
- Compare hashes
- Log result to evidence log
- Fail closed: if hashes don't match, raise error; do not mark run complete

**Cleanup:**
- Keep both primary and mirror indefinitely (no age-based deletion)
- Both must exist for a run to be considered complete

---

## Acceptance

1. Mirror location is specified
2. Copy operation is automated (runs after every completion)
3. Hash verification passes
4. Evidence log records both hashes
5. Both copies exist and are readable

---

## Notes

Scott decides mirror location. Once specified, this spec is complete.
