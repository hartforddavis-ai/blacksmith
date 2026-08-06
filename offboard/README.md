# OFF-BOARD JOBS — four days

Fourteen jobs to run on free AI platforms while local capacity is spent. Each is
a single file. Open it, paste the block it gives you, bring the answer back.

**Where everything is:** `~/Documents/_PROJECTS/SOFTWARE/blacksmith/offboard/`

| what | where |
|---|---|
| the jobs | `JOB_1` … `JOB_14`, one file each |
| all of it in one file, for a phone | `ALL_JOBS.md` — a copy, rebuilt by the export, not a source |
| text to paste into a model | `packets/packet_a.txt` … `packet_e.txt` |
| the right answers | `packets/ANSWERS.txt` — **keep it shut until the packets are done** |
| where answers go | `RESULTS.md` |
| rebuild the packets | `python3.12 make_packets.py` |
| why any of this | **A NOTE ON THE PIPELINE**, at the bottom of this file |

The job numbers are labels, not an order. **The order is below.**

Disposable. Delete the whole directory once the answers are recorded and acted
on — it is a set of questions, not a part of the pipeline.

---

## THE THREE RULES

**1. Paste nothing of ours.** No file contents, no paths, no project name, no
kernel or job text. Every prompt in here is deliberately generic, and the
packets are invented weather-station prose. Free platforms train on what you
give them.

**2. Ask for quotes and links, never summaries.** A platform's paraphrase of a
document is exactly the kind of confident, unsourced output this project keeps
getting caught by. If it cannot quote a source, the honest answer is NOT FOUND,
and that is what should come back.

**3. Open every link before you write it down.** This is the one that will
actually bite. Asking a chat model for published citations is the single most
reliable way to get invented ones — plausible paper titles, real-looking arXiv
numbers that resolve to nothing or to something unrelated. The QUOTED/INFERRED
discipline in these prompts catches reasoning dressed up as fact; it does
nothing against a link that simply does not exist.

So: click it. If it 404s, if the paper is real but says something else, if the
quote is not on the page — **that citation is not evidence, and it goes into
`RESULTS.md` marked UNVERIFIED rather than being dropped.** A platform that
produced one invented citation has told you what the rest of its answer is
worth.

This project has already paid for this lesson once. The failure log, 5 Aug:
*"The ruling was accepted on re-derivation of its citations, never on the run's
own report."*

**Hard exclusion: do not ask any platform to design, fix, or improve anything.**
The failure log holds two entries where an unbound model was handed a broken
thing and built a replacement instead of removing it. These are fact-finding
and measurement jobs only. Every prompt already ends by saying so — leave that
line in.

---

## THE ORDER

### Day 1 — is the instrument even sound?

**`JOB_2_packet_test.md`** — packets a, b, c.
The only job here that produces a measurement rather than a fact, and the only
one that cannot be done on our own machine at any price. It asks whether the
counting task is well-formed, or whether the local models are simply failing
something that is broken to begin with. Do this first even if nothing else gets
done. Turn chat memory off before you start — the file explains why.

**`JOB_3_sampling_params.md`** — the cheapest explanation on the table.
A sampling penalty left in force by the model's own config may be actively
discouraging the model from ever stopping. Two of the five questions can kill
this idea outright, which is a good day's work either way.

### Day 2 — is the runner using the wrong door?

**`JOB_4_generate_vs_chat.md`** — potentially the largest mechanical finding.
If chat formatting only applies on the endpoint we are *not* using, then every
run in `runs/` was produced under conditions nobody intended.

**`JOB_5_known_issues.md`** — has somebody already found this and fixed it.
Half an hour of searching that could make several other jobs unnecessary.

### Day 3 — is the job we are asking even possible?

**`JOB_10_verification_ceiling.md`** — **the deepest question in the folder.**
Can a model this size verify quotes against a document at all? Every serious
entry in the failure log is that task going wrong. If the published answer is
no, then no amount of plumbing repair helps, and that reframes everything else
here.

**`JOB_11_retrieval_vs_length.md`** — how fast exact recall falls off with
length. The ramp is measuring this at four and a half hours per data point.
The literature may already have the curve, which would tell us which rungs are
worth measuring at all.

### Day 4 — the settings on the live server

**`JOB_1_context_shift.md`** — `--context-shift --keep 4`. Whether the model
quietly loses the question mid-answer.

**`JOB_6_thinking_budget.md`** — what actually stopped the run. It ended by
itself after 8,412 seconds, and our record calls that `OK` on our own authority
rather than the server's.

**`JOB_12_quantisation_and_format.md`** — whether 4-bit compression breaks
instruction-following before it breaks anything else.

### If there is time left

- **`JOB_7_kv_quantisation.md`** — the compressed cache and exact recall.
- **`JOB_13_determinism.md`** — does temperature 0 give the same answer twice.
  Rejected by the Filter as a forecast, kept because if it comes back badly it
  is the most serious finding here.
- **`JOB_14_effective_context.md`** — is 65,536 a real number or an advertised
  one.
- **`JOB_8_scale_test.md`** — packets d and e. Rejected by the Filter; drop
  this first.
- **`JOB_9_model_shortlist.md`** — what evidence exists about which models hold
  a strict output format.

---

## IF THERE IS TIME FOR ONLY ONE

**Job 2.** Everything else is a fact that can be looked up later, by anyone, at
any time. Job 2 is a measurement, and it is the only thing on this list that can
tell us the difference between a bad model and a bad question.

**If there is time for two, add Job 10** — for the reason in the note below.

---

## WHAT THE FILTER SAID ABOUT THIS FOLDER

Run 6 Aug, per part, so you know what to drop when time runs short.

- **Earned** — Job 2 (packets a and b), Job 3, Job 4, Job 5, Job 10, Job 11,
  Job 12. Each closes something that has actually failed here.
- **Not earned, kept anyway** — packet c, packets d and e, Job 8, Job 13.
  These answer questions where nothing has gone wrong yet. That is a forecast,
  not a failure, and the log has an entry about the cost of confusing the two.
- **Elaboration fired.** The demonstrated failures are closed by about half of
  this folder. The other half exists because a four-day budget was set, which
  is a legitimate reason to keep it and not a reason to pretend it was earned.

---

## WHY ANY OF THIS — where things stood, 6 Aug 2026

- `qwen3.5:9b`, on the **smallest** rung of the ramp, returned an empty reply
  after 8,412 seconds and 206,086 characters of reasoning. The retry did the
  same.
- Our own record of that run says `outcome: OK`.
- The live server runs with `--context-shift --keep 4` and an 8-bit key/value
  cache.
- The model's own config carries a presence penalty of 1.5, which our runner
  does not override.
- The model's template is `{{ .Prompt }}` — it wraps nothing — and formatting is
  delegated to machinery that may not apply to the endpoint we call.

Four candidate causes, none proven, all checkable by reading rather than by
burning another night of local compute. That is what makes them good off-board
work.

---

## A NOTE ON THE PIPELINE

Written 6 Aug, at the end of a long night. This is an observation about a
pattern in the failure log, not a proposal. What to do about it is Scott's call.

**The pipeline does two different kinds of checking, and only one of them has
ever failed.**

The first kind: a program works the answer out from the source itself. `quotes.py`
re-derives what the quotes actually are and compares. `cell` and `attest` count
bytes and hash them. These do not ask a model anything. **Nothing in this
category has ever produced a wrong answer.** They are also the parts that
survive a model being swapped for a better one, because they never depended on
the model in the first place.

The second kind: a model is handed a document and asked to say whether something
is true about it. **Every serious entry in `FAILURE_LOG.md` is this kind.** The
verify instrument ruled UNFIT for two fabricated VERIFIED rows. Nine quotes that
were not in the source. A counts line left as an unfilled template. Tonight, a
model that thought for two hours and answered nothing.

In every one of those cases the fabrication was caught in minutes by a plain
text search. It was never caught by the model, and in the UNFIT case the model's
own summary line — the one that would have exposed the problem — was the field
it left blank.

**That is the pattern, and it has been consistent since 5 August.** Programs
that re-derive: no failures. Models that certify: nothing but.

Most of the jobs in this folder ask *why the model is misbehaving tonight* —
which setting, which endpoint, which penalty. Those are worth answering and some
of them may well explain everything. But Jobs 10 and 11 ask the question
underneath: **is certifying quotes against a supplied document something a model
of this size can do reliably at all?**

If the published evidence says no, then tonight's investigation has been
diagnosing a symptom of a limit rather than a fault. The response would not be
to fix the model. It would be to know where the line is, and to stop treating a
model's verdict as evidence on its own — which the pipeline already half does,
in the parts that never fail.

If the evidence says yes, that is equally useful: it means the failures are ours
and there is something here to repair.

Either answer is worth more than another night of watching a spinner. That is
the whole argument for spending four days on reading instead of running.
