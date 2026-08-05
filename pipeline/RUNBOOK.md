# RUNBOOK — the operator's page

Everything else in this directory addresses a model. This addresses you.

You are not supervising the pipeline; you are **part of it**. Both external review
legs cross a vendor boundary because *you* carry the bytes across it by hand. That
is the whole reason the boundary is real — an API key the generator could call is a
boundary the generator could route around.

Run every command from `blacksmith/pipeline/`. Everything lands in `cycles/NNN/`.

---

## Before you start: the four windows

Open these before step 1. Each stage below tells you which window it means.

| Window | What it actually is | What runs there |
|---|---|---|
| **TERMINAL** | Your shell, sitting in `blacksmith/pipeline/` | You, typing commands |
| **GENERATOR** | A brand-new Claude Code session — a new window, started from scratch | Claude Opus |
| **AUDITOR** | A browser tab at **gemini.google.com** | Gemini Flash Lite |
| **CHECKER** | A browser tab at **chatgpt.com** | ChatGPT |

There is a fifth, optional window — **TEMPER** — a second new Claude session. It is
cheap and carries no evidentiary weight. See step 5.

---

## ⛔ Do not use subagents for any of this

Not for the generator, and absolutely not for the auditor or checker. Three reasons,
plainest first:

1. **A subagent can read your hard drive.** The answer key is on your hard drive —
   `cycles/NNN/<role>/bundle.meta.json` holds the grounding answers and the exact
   location of the planted defect. An agent can open that file and score perfectly
   without reading one line of the code it is supposed to be reviewing. The grounding
   quiz and the planted defect are the *only* two things that catch a reviewer who
   didn't do the work. Against an agent they measure nothing. You, pasting into a
   browser tab, physically cannot do this.
2. **A subagent is Claude.** The generator is Claude. Claude reviewing Claude is one
   opinion delivered twice — same lineage, same blind spots. The pipeline records that
   as an independent review only because *you* typed a vendor name; it has no way to
   see what really produced the reply.
3. **A subagent inherits this machine's context** — `CLAUDE.md`, the `MEMORY.md` boot
   index, and everything the parent session already knows about Blacksmith. That is
   exactly the narrated prior-cycle state the generator contract forbids.

**A new Claude Code window is not a subagent.** The distinction is: did you open a new
window and paste, or did a model spawn it for you? Only the first one counts.

---

## Words used below

| Word | What it means here |
|---|---|
| **Claim** | One statement the generator wants to be true, e.g. "cell.py refuses a contaminated location". Claims live in `claims.json`. |
| **Provenance** | How well-evidenced a claim is. Weakest to strongest: `ASSERTED` → `STALE` → `MACHINE` → `REVIEWED` → `CONFIRMED`. Only `CONFIRMED` closes a gate. Nobody sets this by hand — it is recalculated from evidence every time anything is read. |
| **Machine leg** | The deterministic checks: run the tests, verify the manifest, optionally run assay. No model involved. |
| **Bundle** | The frozen source files sent out for review, split into **parts** small enough to paste without being truncated. |
| **Grounding question** | "Quote line 47 of cell.py verbatim." Trivial if you have the text, impossible if you don't. It proves the reviewer actually received the bytes. |
| **Canary** | A defect deliberately planted in the auditor's bundle. If the auditor doesn't spot it, the auditor wasn't looking. |
| **Temper** | A cheap in-family Claude pass that kills obvious defects before they cost you a paste round-trip. Commentary only, never evidence. |
| **`BLOCKED_OWNER`** | This step needs a decision from you. No cycle can unblock it. |
| **The four rulings** | Three `[SCOTT]` markers in SPEC.md plus the §8 step 0 design session. They reprint every cycle until you rule on them. |
| **Objective step** | The build-order step a claim was raised under, stamped at load from `objective.json`. A step closes when every claim carrying it reaches `CONFIRMED` — that is the only thing that advances the build order. |
| **The freeze** | The point where the spec stops moving. Four conditions, all derived: every claim `CONFIRMED`, no step blocked on you, no `[SCOTT]` ruling open, no claim contested. |

---

# The stages

---

## 1 — Start the cycle · TERMINAL

**What this is for.** Picks which objective this cycle works on, takes a fresh
snapshot of what the repository currently proves, and writes the generator's prompt.

**What you type.**

    python3.12 -B cycle.py start --cycle 1

**What you should see.** A JSON block naming the objective and the prompt it just
wrote, e.g.

    {
      "cycle": 1,
      "step": "start",
      "objective": "Cell + attest + sterile-launch proof",
      "objective_step": 1,
      "budget": "USD 25 / ~150 assistant turns",
      "prompt_file": "generator.prompt.md",
      "prompt": ".../cycles/001/generator.prompt.md"
    }

**Read `prompt_file`, every time.** A restart does not overwrite the prompt — it writes
`generator.prompt.2.md`, then `.3.md`. Which bytes drove a generator session is the first
thing an audit asks, so they are all kept. The consequence for you is that after any
restart, `generator.prompt.md` is the *stale* one. Step 2 means the file named here.

**If it looks wrong.** If `objective` comes back `null`, stop: every step is either done
or blocked on you, and the run below it prints "NONE — every step is DONE or BLOCKED. Do
not invent one." A step blocked on you never appears as the objective at all — the
assigner skips it and reports it separately, under *"Blocked on the owner"*.

**Before you move on.** The file named in `prompt_file` exists, and you have read the
objective line so you know what this cycle is about.

---

## 2 — Run the generator · GENERATOR window

**What this is for.** A model does the actual work of the objective — writes code,
writes tests, and writes down what it claims to have proved.

**What you paste.** Open a **brand-new Claude Code window** — not this session, not a
subagent, not a continued conversation. `cd` into the tree the work belongs in. Then
paste the entire contents of **the file step 1 named in `prompt_file`**:

    cycles/001/generator.prompt.md      ← first start
    cycles/001/generator.prompt.2.md    ← after one restart, and so on

**Add nothing.** No "here's what last cycle did", no "I think the problem is X", no "see
if you can find the bug in Y". Every word you add is a word it can anchor on, and the
whole value of this leg is that it arrived without a theory. The prompt is complete on
its own; that is what step 1 built it for.

**Which model.** Opus for boundary and security work. Sonnet is fine when the cycle is
following a pattern that already exists in the tree.

**What you should see.** It works the objective, then produces `cycles/001/CANDIDATE.json`
— its own written account of what it did, with one row per claim.

**If it looks wrong.** If the generator says something in its context looks like a summary
of a previous cycle, believe it and stop. Its contract tells it to report that, and a
contaminated generator run is worth more as a finding than as a cycle.

**Before you move on.** `cycles/001/CANDIDATE.json` exists, and you know which tree the
generator was working in — you need that for step 4.

---

## 3 — Load the claims · TERMINAL

**What this is for.** Moves the claims out of the generator's own account and into the
ledger, where the rest of the pipeline can see them.

**What you type.**

    python3.12 -B cycle.py load --cycle 1

**What you should see.** A count of rows written, matching the number of claims in
`CANDIDATE.json`, and the `objective_step` they were stamped with.

**Each claim is bound to the step it answers.** `load` reads `cycles/001/objective.json`
— written by step 1 — and stamps every claim with that build-order step. This is what
lets the step close later (stage 11). It refuses if you never ran step 1 for this cycle:
a claim that names no step can never close one, and a claim that counts towards nothing
is worse than no claim, because it looks like progress.

**If you skip this step** — and the old version of this runbook did not have it —
`claims.json` stays empty. The machine leg now refuses outright in that state, but
`bundle` does not: it will happily freeze `SPEC.md` alone and send it out, and an auditor
will review the spec while you read the result as a review of the work.

**Before you move on.** `claims.json` is no longer `[]`.

---

## 4 — Machine leg · TERMINAL

**What this is for.** The deterministic evidence. Tests, manifest, assay, git. No model
touches this, which is why it counts.

**What you type** — only after step 2 has finished, and after the generator's work has
been merged into this tree:

    python3.12 -B cycle.py machine --cycle 1 --git-range HEAD~1..HEAD

**Which tree this runs over is not your choice.** The leg finds the git root by walking
up from `pipeline/`'s own location — never from your cwd, deliberately. So "run it in the
worktree the generator used" is impossible: merge that work into this tree first. Cycle
1's had to be fast-forwarded before the leg would run at all.

**What you should see.** `"passed": true` and a `rows_written` count greater than zero.

**The two refusals, and what each means.** Both exit 2 and write nothing:

- *"the ledger is empty"* — you skipped step 3. A green result over a ledger with no
  claims stands for nothing, so the leg declines to record one.
- *"this tree is missing subject files the ledger names"* — the generator's work is not
  here. This is the guard for cycle 1's original failure: the leg ran in the main tree 24
  minutes before the candidate existed, went green, and that green was evidence about a
  different tree entirely.

**A failed suite is not a refusal.** It records, and the claims depending on it cannot
rise above `ASSERTED`. That is the system working, not a problem to route around.

**`--git-range` runs assay, and assay is informational only.** Without a record to gate
against it exits 10 and reports `"passed": null`, which `machine.record()` excludes from
evidence — it lands in `machine.json` and attaches to no claim. Useful to read, never
load-bearing. Drop the flag and it does not run at all.

**Before you move on.** `cycles/001/machine.json` records the same tree and git HEAD the
generator worked in.

---

## 5 — Temper (optional, cheap) · TEMPER window

**What this is for.** Killing obvious defects here costs one paste. Letting them reach
the auditor costs a whole round-trip and burns a review you can't un-burn.

**What you paste** into a second new Claude session, in this order:

1. `roles/temper.md`
2. the diff from this cycle

Nothing else. No claims list, no `CANDIDATE.json`, no context about what the fix was for.

**Haiku is fine here — and here is why that is safe.** Temper is Claude. So is the
generator. `claims.py` maps `haiku`, `sonnet`, `opus` and `claude` all to the same family:
`anthropic`. **In-family means Temper can never raise a claim's provenance, no matter
what it finds or how confident it sounds.** Because the leg carries no evidentiary weight
at all, spending Opus money on it buys you nothing. Use Haiku.

**Run it under `python3.12 -B`.** With bytecode caching on, a revert-and-prove pass can
report catching guards that were never actually exercised.

**What you should see.** A list of defects worth fixing, or nothing. Both are useful.

**Where its output goes.** Save it to `cycles/001/temper.md`. **Do not ingest it.** There
is no ingest command for Temper and adding one would be a mistake — the moment in-family
commentary enters the ledger as evidence, the ledger stops meaning anything.

**Before you move on.** Anything Temper found is either fixed (re-run step 4) or
consciously left.

---

## 6 — Build the auditor bundle · TERMINAL

**What this is for.** Freezes the exact bytes the auditor will see, binds them to a
digest, splits them for pasting, and plants the canary.

**What you type.**

    python3.12 -B cycle.py bundle --cycle 1 --role auditor

**What you should see.** A part count, and `"canary": true`. Files appear at
`cycles/001/auditor/auditor.prompt.txt` (the auditor's instructions) and
`bundle.part1.txt`, `part2.txt`, and so on.

**⛔ Never paste `bundle.meta.json`.** It holds the grounding answers and the canary's
location. Pasting it hands the reviewer the answer key. This is also the file that makes
a subagent auditor worthless — see the top of this page.

**Before you move on.** You know how many parts there are. You need that number in step 7.

---

## 7 — Auditor leg · AUDITOR window (gemini.google.com)

**What this is for.** The first genuinely independent look. Different vendor, different
lineage, no idea what the code was meant to do.

**What you paste, in this exact order, one message each:**

| # | Paste this | Why |
|---|---|---|
| 1 | `cycles/001/auditor/auditor.prompt.txt` — **by itself, first** | **The auditor's instructions.** Without them Gemini has no idea what output format to produce, which guarantees a `REJECTED_SHAPE`. Step 6 generates this file for you. |
| 2 | `cycles/001/auditor/bundle.part1.txt` | The source, verbatim |
| 3 | …`part2.txt`, `part3.txt`, … | **In order. All of them.** |
| 4 | Then ask: *"Return the single JSON verdict block described in your role contract."* | |

**Order is not cosmetic.** The grounding questions are written into the **last part**. If
you paste parts out of order, or drop one, the auditor answers quotation questions about
text it never received, and the whole review is discarded with `REJECTED_GROUNDING`.

**Don't help it.** No hints, no "check whether X is safe", no explanation of what the code
is for. Starving it is the entire value of this leg. Feeding it collapses it into agreement.

**Save the reply verbatim** — the whole reply, prose and all — to:

    cycles/001/auditor/reply.txt

Don't tidy it. Don't extract the JSON yourself. Don't fix its formatting. The parser does
that, and a reply you had to repair is a signal, not a nuisance.

**Before you move on.** `reply.txt` is the raw reply, unedited.

---

## 8 — Ingest the auditor · TERMINAL

**What you type.**

    python3.12 -B cycle.py ingest --cycle 1 --role auditor \
      --vendor gemini-flash-lite --transport browser \
      --response cycles/001/auditor/reply.txt

**`--vendor` is load-bearing and it is free text.** The pipeline decides whether a review
counts as independent by pattern-matching that string. A typo — `gemni`, `geminni` — matches
nothing, falls through to family `"unknown"`, and **unknown is treated as independent**. You
would be recording a review as independent on the strength of a typo. Use exactly:

- auditor → `gemini-flash-lite`
- checker → `chatgpt`
- tiebreak → `grok`

**`--transport browser`** is your attestation that you carried these bytes by hand. Say
`agent` and the pipeline will refuse the leg, by design.

**What you should see.** `"result": "ACCEPTED"` and a recorded count. Anything else, read
the rejection table below.

---

## 9 — Build the checker bundle and run the checker · TERMINAL, then CHECKER window

**What this is for.** A different question from the auditor's. The auditor asks "is this
code sound?" The checker asks one thing only: *does the test, as written, actually establish
the claim?*

**What you type.**

    python3.12 -B cycle.py bundle --cycle 1 --role checker

**What you paste into the CHECKER window (chatgpt.com), in this exact order:**

| # | Paste this | Why |
|---|---|---|
| 1 | `cycles/001/checker/checker.prompt.txt` — **by itself, first** | Unlike the auditor's, this file is generated for you, and it already contains the checker's role contract *plus* the claim list. You do not need to paste `roles/checker.md` separately. |
| 2 | `cycles/001/checker/bundle.part1.txt` | |
| 3 | …remaining parts, **in order** | |
| 4 | Then ask for the verdict | |

**⛔ Never paste `bundle.meta.json`.** Same reason as step 6.

**Save the reply verbatim** to `cycles/001/checker/reply.txt`, then:

    python3.12 -B cycle.py ingest --cycle 1 --role checker \
      --vendor chatgpt --transport browser \
      --response cycles/001/checker/reply.txt

**Grok is the tiebreak, not a third opinion.** Run `--role tiebreak` **only** when the
auditor and checker disagree about the same claim. You will find out that happened by
reading `STATE.md` after step 10 — look for the section headed *"Contested — recorded, not
resolved"*. Ingest records a disagreement; it never resolves one.

Two things about the tiebreak that are not obvious:

- Its prompt is written to `cycles/001/tiebreak/checker.prompt.txt` — the checker's
  contract, in the tiebreak's own directory. That filename is correct; paste it.
- **A tiebreak verdict never moves provenance.** `claims.provenance()` counts the auditor
  and the checker only. The tiebreak is recorded, and it informs *you*; it does not
  arithmetically break the tie, because a third model outvoting the second is not evidence
  about the code. A contested claim stays contested until the disagreement is resolved in
  the tree.

---

## 10 — Read the state · TERMINAL

**What you type.**

    python3.12 -B cycle.py status --cycle 1

**What you should see.** A rewritten `STATE.md`. Read four things in it:

- **FREEZE.** `NOT READY` now lists exactly which conditions failed — unconfirmed claims,
  steps blocked on you, open `[SCOTT]` rulings, contested claims. `READY` appears only when
  all four hold. It is computed each run; until 31 Jul 2026 it was the string `NOT READY`
  printed unconditionally under a sentence claiming it had been derived.
- **Each claim's provenance.** `CONFIRMED` means a machine leg *and* an independent review
  both re-derived the claim from the bytes currently on disk. Nothing else closes a gate.
- **"INDEPENDENT REVIEW"** — if it says `NONE ON RECORD`, no external verdict was ever
  ingested, whatever anyone claims happened.
- **"Contested"** — where the auditor and checker disagreed. That is your tiebreak list.

---

## 11 — How the cycle closes · TERMINAL

**What this is for.** Knowing whether this cycle finished its build-order step, or
whether the next one repeats it.

There is no command. The step closes on evidence: when **every claim stamped with that
step reaches `CONFIRMED`**, the next `cycle.py start` assigns the *following* step. You
will see it in the `objective` field, and in `STATE.md`'s "ASSIGNED OBJECTIVE" section.

**Read this as the answer to "did anything move?"** If `start` hands you the same step
again, the honest reading is that the step is not proved yet — find the claim that is
still short of `CONFIRMED` in the claim table and work out which leg it is missing.

**You do not edit `build_order.json` to advance it.** Its `status` field says `OPEN` or
`BLOCKED_OWNER` only; the `DONE` half is derived from the ledger. Before 31 Jul 2026
nothing wrote that field and this runbook never told you to, so the assigner returned
step 1 on every cycle no matter how much work landed — a whole cycle could complete and
change nothing about what the next one was asked to do.

**Evidence decays, so a closed step can reopen.** Edit a reviewed file and its claims
fall to `STALE`; the step stops being done and comes back as the objective. That is the
system working — the alternative is a step that stays closed over bytes nobody checked.

---

## What the rejections mean

A rejected review is discarded **whole**. Not partially kept, not weighed. That is
deliberate: keeping the plausible half of a review that failed its check is exactly how a
supplied verdict becomes a verdict.

| Result | What you'll see on screen | What actually happened | What you do |
|---|---|---|---|
| `REJECTED_SHAPE` | `response contains more than one JSON block` or `not valid JSON` | The reply wasn't one clean JSON block. Often because the role contract was never pasted. | Ask the same window for one JSON block and nothing else. **Never reformat it yourself, and never ask a model to repair it** — that puts a model between the reviewer and the ledger, which is the defect this pipeline exists to stop. |
| `REJECTED_UNBOUND` | The verdict names a different bundle digest | You pasted a stale bundle, or the tree changed mid-cycle | Rebuild the bundle and re-run that leg from scratch |
| `REJECTED_GROUNDING` | A quotation answer was wrong | It didn't have the bytes — a part was truncated, skipped, or pasted out of order, so it answered from memory | Check every part actually landed in the window, in order, then re-run the leg |
| `REJECTED_CITATION` | It cited a line number that doesn't exist | Fabrication | Note the vendor and move on. This is a fact about that model. |
| `REJECTED_INSENSITIVE` | It missed the planted defect | It didn't look | This is the only check that catches a reviewer who skimmed and returned nothing. Repeated misses mean the model is wrong for the role — that's a measurement, not an opinion. |
| Refused: `transport=agent` | The leg won't run at all | You told it a subagent produced the reply | Correct. Re-run the leg in a real browser tab. See the top of this page. |

**Two of these do not reach the rejection log, and you should know which.** A reply that
cannot be parsed at all, and a refused transport, both fail *before* `ingest` runs — they
print `cycle: <reason>`, exit 2, and write no row to `ingest.log.jsonl`. Everything from
`REJECTED_UNBOUND` down is logged, because by then the verdict exists as a file. So a
malformed reply leaves no trace but your terminal: if it matters that a vendor returned
something unparseable, keep the reply, because the ledger will not remember it for you.

---

## Your standing jobs, which no cycle can do

1. **The four rulings.** Three `[SCOTT]` markers in the SPEC, plus the §8 step 0 design
   session. `STATE.md` reprints them every cycle until you rule. Until then the freeze does
   not move, however many cycles run. Ruling on one in conversation does not clear it — the
   marker has to come out of `SPEC.md`.
2. **Never paste the meta file.** Worth saying twice.
3. **Don't help the reviewer.** No hints, no "check whether X is safe", no context about
   what the fix was meant to do. Starving it is the leg's entire value; feeding it collapses
   it into agreement.
4. **Real windows, never subagents, for every model leg.** The reason is at the top of this
   page and it is the most important paragraph in this file.
5. **Watch where the work goes.** Five self-directed cycles produced good hardening and never
   touched step 0, because work flows to whatever is reachable. If cycles keep landing on
   polish, the build order is being routed around.
