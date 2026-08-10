# TEST — is `evidence_log.py` actually wired into the pipeline?

Written 11 Aug 2026, answering Scott's question about !55 (attestation is not
the evidence log — separate stages, checked against `run_local.py`'s own
order). The dossier's 6 Aug note that nothing calls `evidence_log.py` is
**already stale** — `run_sealed.py`, committed the same evening, is the
caller (verified 11 Aug by the grep below). Kept as a standing regression
test: this stage has gone silently uncalled once before.

## WHAT IT DECIDES

- **A caller is found** (currently `run_sealed.py`) → wiring holds, nothing
  to do.
- **No caller is found** → the evidence-log stage in the pipeline diagram has
  gone aspirational again. That's a Law 1 ROBUST failure waiting to happen: a
  run can complete, print "evidence log" in the stage list, and never
  actually write one — it happened once already (5 Aug `pivot_smoke`).

## RUN

```
cd ~/Documents/_PROJECTS/SOFTWARE/blacksmith
grep -rn "evidence_log\|root_hash(\|canonical(" --include="*.py" . \
  | grep -v "^./evidence_log.py\|test_"
```

Empty output (besides the module's own definition and its tests) = confirmed
gap, matching what the dossier already found. Any real hit = the finding is
stale, update `project_blacksmith.md`.

## IF THE GAP IS CONFIRMED

Not this session's call to fix — SPEC-level (Law 1: does closing it need a
new caller site named in the frozen design, or does `run_local.py` already
have the hook and just isn't using it?). Read `run_local.py`'s bundle/gauge
step before writing the call; don't add a second evidence-writing path next
to whatever's already there.
