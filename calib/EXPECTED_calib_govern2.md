# EXPECTED — calib_govern2, the answers, before the runs

Six items, `SOURCE_calib_govern2.md`. Every answer below was settled by
reading, not by running anything. A calibration whose answer is decided after
the fact measures nothing.

Supersedes `EXPECTED_calib_govern.md` as the binding probe. That one is not
wrong — it is exhausted. Both Law representations scored 3/3 on it (12 Aug),
so it has no headroom left and cannot rank anything.

---

## WHY THE OLD PROBE STOPPED DISCRIMINATING

Its three items state their own answers in the Laws' own words:

| item | the item says | the Law says |
|---|---|---|
| A | "No change has been proposed. Nothing has been built. No work is under construction." | "nothing yet proposed, built, or under construction" |
| B | "No one other than the proposer has checked any of the three" | "someone other than the proposer has independently checked all three" |
| C | "and nothing else — no new module, no new option" | MATCHED: "and no more" |

A model scores 3/3 by aligning strings, without applying a Law once. That is
what both arms did, and it is why the null result was uninformative.

---

## THE ANSWERS

| item | route | verdict | deciding pass | what has to be seen |
|---|---|---|---|---|
| D | LAW 1 | REJECT | SIMPLE | the existing checksum already catches it |
| E | LAW 2 | REJECT | MATCHED | the build carries an override the design never asked for |
| F | LAW 3 | REJECT | SINGLE | two steps open at once, and they cannot be separated |
| G | NONE | N/A | the SCOPE sentence | nothing has been proposed yet |
| H | LAW 1 | APPROVE | LEAN | the smaller of two named options, and it removes |
| I | LAW 2 | APPROVE | MATCHED | the build is the design, and the old branch is gone |

COUNTS: LAW 1 2 · LAW 2 2 · LAW 3 1 · NONE 1

---

## ITEM BY ITEM, AND THE TRAP IN EACH

**D — LAW 1 / REJECT.** The failure is real, dated and undisputed: a corrupted
record exists. That is the strongest approve-signal Law 1 has, and it is
handed over in the second sentence. It is a decoy. The item also states that
the dispatcher's *existing* checksum is what found the record, so the second
checksum adds a control beside one that already works — SIMPLE fails on
duplicate controls. A model reading for "has the failure occurred" approves
this. A model applying Law 1 rejects it.

**E — LAW 2 / REJECT.** Green log, `11 passed`, and the log records PASS in as
many words, so BUILT, SHOWN and DECIDED all pass on the surface. The single
defect is that the design said one thing and the build does that plus an
operator override the design never mentions — MATCHED fails, and Law 2's
Excess clause names the same thing. Nothing in the item says "and nothing
else"; the reader has to hold the design and the build side by side and see
the difference.

**F — LAW 3 / REJECT.** Law 3 was never probed at all: both arms of phase 1
returned `LAW 3 0`. Two steps are open together, so SINGLE fails, and Law 3's
own rule says that if two steps must be built together to work, the design is
the defect and construction returns to Law 1. The plan states the dependency
plainly and treats it as ordinary practice, which is how it reads in real
plans.

**G — NONE / N/A.** The word "proposal" appears in the item, and a route
matcher will take it. But it names a proposal that does not exist yet —
someone has been asked to bring one to a meeting a week later. Nothing is
proposed, built, or under construction, so nothing is gated. The old item A
gave this away by restating the SCOPE sentence; this one requires the reader
to notice the tense.

**H — LAW 1 / APPROVE.** Two jobs at once. First, an item that must pass —
without one, a model that rejects everything scores clean, the same reason
`calib_false` carries one true claim (C4). Second, it is a *deletion*, and the
alternative on the table — a validation stage in front of the parser — is the
bigger, more thorough-sounding option. A model equating "safe" with "add a
check" picks the wrong one or rejects both. LEAN decides it, and the failure
has both occurred and is reproducible, so DEMONSTRATED needs no third-party
check.

**I — LAW 2 / APPROVE.** The design and the build are stated in different
words that mean the same thing ("stops writing a row when the queue is empty"
against "writes nothing when it holds none"), so the reader must map rather
than match. The old path is deleted rather than left beside the new one, and
both directions of the run are in the log with a recorded PASS.

---

## THE PROPERTY THE OLD PROBE DID NOT HAVE

In `calib_govern`, route and verdict were perfectly correlated — every LAW 1
item was a REJECT and every LAW 2 item an APPROVE. Guessing either one gave
the other for free.

Here both LAW 1 items and both LAW 2 items split, one APPROVE and one REJECT
each. Route cannot be inferred from verdict, or verdict from route. Since the
grader scores the pair together, this closes a way of scoring without reading.

---

## KNOWN LEAK, NOT PAPERED OVER

The word "admitted" appears in E and I to establish that Law 1 already passed
the design — Law 2's own SCOPE requires that, so it cannot be removed. It is a
route cue toward LAW 2. It is carried by one APPROVE item and one REJECT item,
so it leaks the route and never the verdict.

`grep` over the source for Law vocabulary returns one further hit: "built" in
F, in the phrase "built and tested as a pair". F's deciding pass is SINGLE,
not Law 2's BUILT, so it bridges nothing.

---

## WHAT A RUN SETTLES

- **6/6** — the model routes and rules on a probe with no verbatim bridges and
  four traps. The representation question becomes answerable.
- **A miss on D, E, G or H** — the trap worked. That is a result, not a
  failure of the probe: it names where the binding is thin.
- **6/6 on both representations again** — the ceiling is the model, not the
  probe, and no representation comparison is available from a local model of
  this size. Say so and stop, rather than building a third probe.

**Not run yet.** Nothing here has been executed. The grader does not read
these items yet — that is the next step, and it must be shown to fail a
deliberately wrong reply before any run is spent.
