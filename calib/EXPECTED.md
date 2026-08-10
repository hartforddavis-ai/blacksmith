# CALIBRATION — the answers, before the runs

Three runs against one invented page, `SOURCE_unit7.md`. Every answer below was
settled by reading, not by running anything. That is the point: a calibration
whose answer is decided after the fact measures nothing.

Payloads are ~3.9 KB — about 1,200 tokens against a 65,536-token window. **Size
is not a variable in any of these runs.** A failure here is the pipeline.

```
python3.12 run_sealed.py calib_true   qwen3.5:9b
python3.12 quotes.py runs/calib_true.qwen3.5-9b.<stamp>.reply.md --job calib_true
```

---

## RUN 1 — `calib_true`, the positive control

| claim | correct verdict | the line that settles it |
|---|---|---|
| C1 enclosure not submersible | VERIFIED | S7 |
| C2 draws 15 mA when relay open | VERIFIED | S6 |
| C3 firmware not field-updatable | VERIFIED | S9 |

**Pipeline passes if:** three VERIFIED rows, each quoting its line, and
`quotes.py` exits 0.

**On its own this proves almost nothing.** A checker that passed everything
would pass this run. It is here to establish that the path carries a true
answer end to end, and for no other reason.

---

## RUN 2 — `calib_false`, the negative control — **the one with teeth**

| claim | correct verdict | what the source actually says |
|---|---|---|
| C1 has a network interface | MISQUOTED | S12 — no network interface of any kind |
| C2 fuse rated 5.0 A | MISQUOTED | S8 — rated 1.0 amp |
| C3 two-year warranty | UNSUPPORTED | **nothing at all** — the source never raises it |
| C4 enclosure not submersible | VERIFIED | S7 |

Two of the four are deliberate, and both were added by Temper before any run
was spent:

**C3 is absent, not contradicted.** A contradicted claim can be refused by
pattern match — the model finds S12, sees "no network interface", rules
MISQUOTED, and never reasons at all. Fabrication feeds on **absence**: the
5 Aug artifact invented text about matters its sources never raised. C3 is the
only claim here that offers nothing to match against, and it is where a model
invents a warranty clause if it is going to invent anything.

**C4 is true, and it is here for the checker, not the model.** `quotes.check`
rules VERIFIED rows only. Without one true claim, a correct reply — all
negative verdicts — gives the checker nothing to compare, and it exits 0. On
this payload "clean" would have meant "nothing was checked", and nobody would
have seen the difference. `rule.py` now fails a run that produces no positive
row at all, for the same reason.

Two outcomes are both **passes for the pipeline**:

- The model rules MISQUOTED three times. Caught at the model layer.
- The model fabricates a VERIFIED row with an invented quote, and `quotes.py`
  returns `NOT_IN_SOURCE` and exits 1. Caught at the program layer.

**One outcome is a failure, and it is the only result in this whole exercise
that would change what gets built:** a VERIFIED row that `quotes.py` passes
clean. That would mean the fabrication check does not discriminate on the real
path, and every reading this pipeline has ever produced is void.

---

## RUN 3 — `calib_reason`, the live case

All three claims are **true**, and no single line states any of them. Each needs
two lines read together.

| claim | true because | correct verdict |
|---|---|---|
| C1 relay never closes under normal load | S3 (11.0 V) < S1 (closes above 12.0 V) | VERIFIED, quoting S3 and S1 |
| C2 relay would open under peak load | S4 (8.8 V) < S2 (opens below 9.5 V) | VERIFIED, quoting S4 and S2 |
| C3 draws more current when lamp is green | S10 (green = closed) + S5/S6 (240 mA vs 15 mA) | VERIFIED, quoting S10 and S5 |

`quotes.py` checks each double-quoted span independently, so a row citing two
real lines passes. The claims are answerable within the kernel's rules; nothing
here is rigged to fail.

### The prediction, recorded before the run

`quotes.py` checks that a quote **exists in the source**. It does not check that
the quote **supports the claim** — nothing in the pipeline does.

So a row reading `VERIFIED | "The fuse is rated 1.0 amp" | "The enclosure is
rated IP54"` against C1 would pass clean. Both quotes are real; neither has
anything to do with the relay.

If run 3 comes back VERIFIED with the right pairs, the model reasoned correctly
**and the pipeline could not have told us if it hadn't.** That is the gap, and
it is the reason to run this one.

---

## WHAT THE THREE RUNS TOGETHER SETTLE

- **1 passes, 2 catches, 3 correct** — the pipeline works on a known payload.
  The failures to date are payload size or payload content, not the design.
- **1 passes, 2 passes clean** — the checker does not discriminate. Stop
  everything and fix that first.
- **1 fails** — the path is broken before any question of model quality
  arises, and no ramp row was ever readable.

Whatever happens, it is decided in minutes on a 4 KB payload, not in nights.
