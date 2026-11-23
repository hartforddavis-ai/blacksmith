# Sterile Derivation of cell.py — Gate Record

Per SPEC_STERILE_DERIVATION.md. Cross-referenced, not duplicated into
MANIFEST.sha256 — see Law 1 note at the foot of this file for why.

## Gate 1 — Derivation Source

PASS. Derivation notes are inline in cell.py's own module docstring
(lines 11–32): explicit citation of SPEC §2 rules 3 and 6, SPEC §8 step 0,
and SPEC §11 ruling 3, with the design consequence of each stated next to
the citation. A separate derivation-notes file would restate this without
adding anything checkable.

## Gate 2 — Code Review (Sterile)

PASS. Full function-by-function checklist against SPEC §2 rules 1–6:
[GATE2_CELL_REVIEW.md](GATE2_CELL_REVIEW.md). 10 functions reviewed, 0
violations of a rule that applies. One disclosed (not concealed) gap in
`_seal`, tracked at SPEC §8/§12, not a defect in this derivation.

## Gate 3 — Sterile Build

PASS. `test_cell_sterility.py`: 28/28, isolated tempdirs, no internet, no
`~/.claude` context, no git history reachable from the test roots — run
2026-08-05, `python3.12 -m unittest test_cell_sterility -v`. Full repo
suite re-run after: 152/152, `python3.12 -m unittest discover -p
"test_*.py"`.

Limit carried forward, not hidden: this exercises `confine`,
`ancestor_contamination`, and `CELL_FORBIDDEN_NAMES` census logic. It does
not touch the UID boundary — the test file's own docstring says so — so it
is evidence for Gates 1–3 only, not for SPEC §8 step 0.

## Gate 4 — Manifest Hash

PASS by cross-reference. MANIFEST.sha256, line 6:
`f8c82d38defaee20547567d079522faf7050a57d3313f579e9ec4cce6d2dcfef  cell.py`
— regenerated this session via `python3.12 manifest.py`, confirmed current
via `python3.12 manifest.py --check` and `test_manifest.py`'s own
round-trip check.

**Law 1 note on this gate's wording:** SPEC_STERILE_DERIVATION.md asks for
a manifest entry "naming gate sequence and digest." Adding gate-sequence
metadata to MANIFEST.sha256 itself was run through Law 1 and rejected —
no demonstrated need for that fact to live in *that* file rather than
here, and `manifest.py`'s stated design (a hand-free glob, uniform across
every Ring 0 file) would have to special-case one entry to carry it. This
file is the gate-sequence record; the digest it cites is the one
MANIFEST.sha256 already carries.

---

## Acceptance

All four gates pass. cell.py is verified per SPEC_STERILE_DERIVATION.md.
Ready for construction.
