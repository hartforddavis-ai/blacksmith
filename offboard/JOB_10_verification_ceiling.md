# JOB 10 — can a model of this size verify quotes at all?

**The deepest question in the set.** Needs a platform with live web search.

---

## WHY

The pipeline asks a local model to read a document it has been handed and
certify whether specific claims are supported by it. Every serious failure in
`FAILURE_LOG.md` is a version of that task going wrong:

- 5 Aug — the only completed reading of the verify instrument returned two
  VERIFIED rows that cite text which does not exist. Ruled UNFIT.
- 6 Aug — a run produced nine quotes not present anywhere in its source.

Both were caught by grep in minutes. Neither was caught by the model.

Every job in this folder up to now assumes the task is sound and something in
the plumbing is breaking it. This one asks the question underneath: **is
verifying quotes against a pasted document something a 9-to-12 billion
parameter model can do reliably at all?**

If the published answer is no, then no amount of context-shift fixing, penalty
tuning or endpoint correction will help, and the finding is worth more than
every other job here combined.

---

## PASTE THIS

```
I need published evidence, with links, about a specific capability: a
language model reading a document supplied in its prompt and correctly
judging whether a given quotation appears in that document verbatim.

Answer only from published papers, benchmarks, or model cards. Mark every
claim QUOTED or INFERRED — I discard everything INFERRED.

1. What benchmarks measure attributed or grounded generation — checking a
   claim against a supplied source rather than against world knowledge?
   Name them, link them.

2. What error rates do open models under roughly 15 billion parameters
   achieve on those benchmarks? Give numbers and sources.

3. Is there published evidence on models producing fabricated verbatim
   quotations attributed to a supplied source? What rates are reported, and
   does the rate change with document length?

4. Is there evidence that a model asked to verify its own or another model's
   citations performs better or worse than a simple string search?

5. Does asking a model to output a structured verdict per claim — verified,
   unsupported, misquoted — change its error rate compared with asking for
   free text? Any published comparison?

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- State plainly whether the published evidence supports or contradicts the
  idea that a sub-15B model can do this reliably.

Do not propose a system, a prompt, or an improvement. I am asking what is
known.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

Named benchmarks with numbers. Question 4 is the sharpest: if published work
finds that a model verifying citations is worse than a string search, then this
project has already built the right answer — `quotes.py` re-derives from source
and does not ask the model anything — and the model's role should be understood
in that light.

---

## BRING BACK

The benchmark names, the numbers, and the links. And the plain answer to the
final question, because it decides whether the rest of this investigation is
about repairing an instrument or about accepting a limit.
