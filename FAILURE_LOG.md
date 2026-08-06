# BLACKSMITH — FAILURE LOG

What was tried here and did not work. Kept so it is not tried again.
Nothing here is a design. Nothing here is to be followed.

---

## READ RULE

```
READ this file WHEN:
    a Law 1 verdict is about to be formed — BEFORE F is named.
    Not after Δ is formed. Read after, it justifies. Read before, it filters.

IT DECIDES two things, in this order:
    1  IS F DEMONSTRATED   F is what occurred. Absent here, and absent from a
                           reproduction on demand, F is theoretical → REJECT.
    2  IS Δ ALREADY DEAD   an entry naming this Δ is a REJECT at step 1.
                           Do not run a dead Δ through the four passes.

LIMIT — this rule binds the reader who opens the file. It cannot reach the
one who does not.
```

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

---

## 5 Aug 2026 — `runs/verify.qwen3.5-9b.20260805T103016.md`

```
BUILT      the only completed reading of the verify instrument. 37 rows,
           KERNEL 73a44a07e235.
BY         qwen3.5:9b, BOUND. Declared no tools; true, Ollama has none.
KILLED BY  Law 2 MATCHED — section 5 returned as the unfilled template,
           "VERIFIED n · MISQUOTED n · UNSUPPORTED n · MISSED n". Twelve
           rows carry a second, contradicting verdict inside the Evidence
           cell, against K2.
           Law 2 SHOWN — 14 rows VERIFIED, two ungrounded. "Step 0 is the
           one open step" cites SPEC §9 for the word OPEN; §9 has no status
           column and no OPEN. "Any fifth generator → verifier" is VERIFIED
           with no quote, on a paraphrase of the ruling.
CLAUSE     Assertion · Excess
STATUS     UNFIT. One fabricated VERIFIED is enough; there are two. Kept as
           the record of what the instrument produced. Its rows are not
           findings and nothing in it is to be acted on.
LESSON     The instrument asks a model with no file access to certify quotes
           against files it cannot open. Grep found both fabrications in
           minutes; the bound model could not have. The check lives with the
           operator, not in the paste.
           Nothing in the reply self-reports as incomplete. The counts line
           that would have exposed it was left as template.
```

---

## 5 Aug 2026 — gemma4:12b run 3

```
BUILT      the second reading the JOB requires.
           run_bound.py verify gemma4:12b, 40,878 chars, temperature 0.
BY         gemma4:12b, BOUND, run by the operator
KILLED BY  Law 2 SHOWN. TimeoutError at urlopen(req, timeout=1800) inside
           getresponse() — died waiting for the first byte, before any token
           streamed. Third attempt, third time zero tokens.
CLAUSE     none.
STATUS     FAILED RUN, no artifact. Raising the timeout is tuning a
           parameter to force a result, which the JOB forbids. A change here
           is a Δ under Law 1, not a patch.
LESSON     "Per read means stalled, not wall clock" holds for every read but
           the first, and the first is the whole of prompt-eval. A per-read
           timeout is not a stall detector until one byte has arrived.
           So the instrument has one reading, not two. Diverging means
           capacity, both failing the same way means the instrument —
           neither test is available. The UNFIT above rests on one model.
```

---

## 5 Aug 2026 — the verdict that would have cut `num_ctx`

A verdict, not a build. Nothing written, nothing run.

```
BUILT      a proposed one-line change: num_ctx 65536 down to about the
           prompt's token count, to get gemma4 past prompt-eval. Ruled
           APPROVE, then withdrawn.
BY         Opus, operator, at the owner's direction
KILLED BY  Law 1 ROBUST. num_ctx is not a performance knob. Ollama truncates
           silently when context is smaller than prompt, and a truncated
           prompt still carries correct digest stamps — the change would
           have let the stamps certify material the model never saw.
           Law 1 LEAN, on arithmetic: qwen used 11k prompt tokens and
           generated 18,919. 65536 covers both. Sizing to the prompt
           truncates the output.
CLAUSE     Assertion — the memory-pressure cause was never measured.
STATUS     WITHDRAWN before it touched a file. run_bound.py unchanged. The
           stall is undiagnosed; cutting sources does not fix it either,
           because Ollama sizes the KV cache from num_ctx, not prompt.
LESSON     Ask what a parameter holds up before calling it a tune. This one
           held the paste's integrity, and the instrument's claim rests on
           that. A probe proved gemma4 generates here — "alive" in 15.5s
           cold. Twice now this model has been blamed for something else.
```

---

## 5 Aug 2026 — "step 3 is untestable until the owner rules"

```
BUILT      a finding that SPEC §9 step 3 cannot run against the real
           runner: HOME locked 0o555 at step 1, child cannot write its
           state, require_sterile refuses the spawn. Stub-testable only,
           and blocked until the owner rules whether ~/.claude counts as
           contamination.
BY         provenance not stated; arrived as pasted text. The four turns
           built on it: Opus, UNBOUND, operator.
KILLED BY  Law 2 — returns a verdict Law 2 does not have. A step that
           cannot run fails BUILT. "Untestable pending a ruling" is a
           third state the filter does not define.
           Law 3 ORDERED — step 3 waits on a decision step 1 was to have
           made. Two steps that work only by adjusting each other are one
           decision split in two. That is the defect.
           Law 1 step 1 — F never occurred. Step 3 has never been run
           against the real runner.
CLAUSE     Assertion · Confabulation · Elaboration
STATUS     Nothing to keep; it was text. Its mechanism is wrong twice
           over: require_sterile is a census (cell.py:285), not a write
           test, and it runs at launch.py:186, before the spawn at :205 —
           a child failing to write cannot fail a check already passed.
           Do not revive the "owner must rule" framing.
LESSON     SPEC 119 already records this hole — UNPROVEN, gated on §8. A
           documented gap re-presented as a discovery adds nothing and
           costs a ruling slot. Ask whether a blocker is new before
           raising it.
           Four turns went on which ruling was needed, none on whether one
           was. The Laws closed it without the owner.
```

---

## 5 Aug 2026 — the redesign rulings

```
BUILT      Law 1 verdicts on twelve modules, two additions, a four-step
           design, a build order. Chat only. No file.
BY         Opus, UNBOUND, full tool set
KILLED BY  Law 2 SHOWN — approved `store` and `promote` without opening
           either file.
           Law 1 ROBUST — ten probes against no demonstrated failure.
           Seven duplicated the test file lying unopened beside them.
           Law 3 SCOPE — a build order on a design whose own §4 says
           "FROZEN: No".
CLAUSE     Confabulation · Assertion
           Five counts and citations stated without checking. The last,
           "nine of the ten duplicated" — seven — was written while
           confessing the defect.
STATUS     Read the design. Not the rulings: a verdict citing an unopened
           file is void.
LESSON     anneal built what it was not asked to. This ruled on what it
           had not read. Output is faster than reading, so reading goes.
           Every defect fell to one file read. None fell to the four
           passes, which ran on prose the session had just written.
```

---

## 6 Aug 2026 — `pipeline/`, deleted for real

```
BUILT      the eleven-stage cycle pipeline (generator → auditor → checker
           → tiebreak, provenance ledger, grounding gate)
BY         Sonnet, bound and unbound sessions, 31 Jul – 5 Aug
KILLED BY  Law 2 — Trim, not Accretion. Passed its own suite throughout;
           superseded by the 4 Aug freeze's leaner six-part Ring 0 (cell,
           attest, launch, collect, gauge, promote), which does the same
           job. The 6 Aug quarantine (move to anneal/pipeline/) was
           recorded as done and never was — it was a copy, not a move, so
           deleting anneal/ on Scott's ruling left the original pipeline/
           live and tracked, 20 files, untouched.
CLAUSE     none — Trim, not a Generator Clause failure
STATUS     Deleted (git rm), uncommitted — Scott's call to commit. Do not
           revive; the cloud vendor-review legs it depended on stay closed
           by CONSTRAINTS.md regardless of this entry.
LESSON     A FAILURE_LOG entry recording an action is not the action. The
           6 Aug dossier said "FAILURE_LOG.md entry added" for this
           quarantine and no such entry existed on disk when checked —
           check the file, not the claim about the file.
```
