# BLACKSMITH — FAILURE LOG

What was tried here and did not work. Kept so it is not tried again.
Nothing here is a design. Nothing here is to be followed.

---

## ENTRY RULE

```
ADD an entry WHEN:
    a build fails Law 2,  OR  a design is withdrawn,
    OR  a verdict is withdrawn — the build passed and the ruling was wrong.

THEN:
    KEEP the artifact. MARK it failed. DO NOT revive it.

FIELDS — all required. An entry missing one is not an entry.
    BUILT      what it was
    BY         which generator, bound or unbound
    KILLED BY  Law + pass that failed
    CLAUSE     which Generator Clause failures fired
    STATUS     what a reader may do with it
    LESSON     the finding that outlives the artifact
```

---

## 5 Aug 2026 — `anneal/`

```
BUILT      a second review pipeline, with design doc, review prompt,
           role documents, reference material
BY         Sonnet, UNBOUND, human-overseen
KILLED BY  Law 2 — Accretion. Handed pipeline/, which did not work, it
           built a replacement instead of removing the original.
           Fourth reinvention of generator → verifier → adversarial-suite
           → human-gate here, after Loop Protocol, Foundry, FRAM.
CLAUSE     Accretion
STATUS     SUSPECT INPUT. Direction never checked. Any statement it makes
           about Blacksmith is a claim to verify, never a fact to inherit,
           including any count, size or history. Its DESIGN.md request for
           approve/reject/send-back is VOID — written for an unbound
           reviewer, and an unbound reviewer is the defect under test.
LESSON     An unbound generator handed a broken thing builds a new thing.
           Removal is not its instinct. Bind it, or it accretes.
```

---

## 5 Aug 2026 — `anneal/FAILED_prompt_bound_opus.md`

```
BUILT      a prompt to bind Opus to redesign Blacksmith under the three
           Laws. Six versions in one session.
BY         Opus, at the owner's direction
KILLED BY  Law 2 BUILT    — never run
           Law 2 MATCHED  — no frozen design to match; re-opened each pass
           Law 2 SHOWN    — six versions, five verdict tables, zero runs
           Law 2 DECIDED  — no PASS or FAIL recorded on any version
           Law 3 SINGLE   — five steps open at once
           Law 3 ORDERED  — depended on two decisions never made: the
                            target, and where the session would run
           Law 1 LEAN     — the tool floor was the only non-assumptive
                            boundary in it
CLAUSE     Assertion · Excess · Accretion
STATUS     FAILED EXAMPLE. Not an instrument. Do not run it, do not
           extract from it.
LESSON     A prompt is not a boundary. Capability absence is. The document
           was elaboration around four lines of session configuration, and
           writing more of it felt like progress every time.
           Owner's rule, broken twice inside a document written to enforce
           it: the verdict goes before the edit, per part. Written after,
           it is a justification, not a filter.
```

---

## 5 Aug 2026 — `anneal/FAILED_prompt_paste.md`, first run: wrong venue

```
BUILT      bound-Opus chat prompt. Run once, produced
           Blacksmith Pipeline Redesign/Bound redesign and prompt/
           BLACKSMITH_REDESIGN.md
BY         Opus, UNBOUND — full tool set held
KILLED BY  Law 2 SHOWN. The prompt's only boundary is capability absence.
           The run held bash, file edit, memory read/write, browser, Gmail,
           Stripe. "None called" is a model certifying its own isolation.
           BUILT, MATCHED, DECIDED passed.
CLAUSE     Assertion
STATUS     FIRST failure. Nothing to revert to — it never passed — so the
           corrections are a new Δ under Law 1: VOID on tools held, checks
           renamed, three-stamp digests. Superseded 5 Aug by the
           KERNEL_bound.md / JOB_*.md split and quarantined here with its
           template; the design job it existed for is finished, so no
           regeneration path is kept. Do not run it.
LESSON     The tool declaration worked; the consequence was missing. It
           declared and continued, and the output read as authoritative.
           A detector without a halt is a footnote.
           The ruling was accepted on re-derivation of its citations,
           never on the run's own report.
```

---

## 5 Aug 2026 — the ruling that reverted streaming from `run_bound.py`

The failure here is a VERDICT, not a build. The build passed. Kept because
the wrong call is the thing worth not repeating.

```
BUILT      run_bound.py with streaming: tokens written as they arrive, file
           opened before the request, prompt-eval dated by the first token.
BY         Opus, at the owner's direction
KILLED BY  A Law 2 reading that was correct in form and wrong in fact. The
           previous run had failed BUILT, and Law 2 says a failed build
           reverts rather than being patched — so the streaming change was
           called a patch in place and quarantined.
           It was not a patch. The single-read 1800s timeout WAS the defect.
           qwen3.5:9b returned in ~39 minutes; the reverted runner gives up
           at 30 and writes nothing. The reverted file has never completed a
           run. The quarantined one is the only version that ever has.
CLAUSE     none. Nothing was asserted, padded or accreted.
STATUS     RESTORED to run_bound.py, 5 Aug. The quarantine copy is deleted —
           keeping a byte-identical twin would be the accretion this entry
           wrongly accused it of.
LESSON     "Revert, do not patch" assumes a last passing state exists. Here
           there was none, and that absence was read as proof the change was
           illegitimate. It was the opposite: nothing had ever passed because
           the timeout was wrong, and the change was the fix.
           Before calling an edit a patch, ask what the last passing state
           actually was. If the answer is "there isn't one", the edit may be
           the first real attempt, not a repair of a failed one.
           Cost of the wrong call: gemma4:12b was written off as too slow at
           30 minutes when the timeout, not the model, was the limit.
```
