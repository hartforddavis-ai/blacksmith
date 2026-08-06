# JOB 12 — does 4-bit compression break instruction-following first?

Needs a platform with live web search.

---

## WHY

The models here are Q4_K_M — the weights are compressed to roughly four bits.
That is standard practice and it is why an 12-billion-parameter model fits on
this machine at all.

The usual defence of 4-bit quantisation is that perplexity barely moves. But
perplexity measures how well a model predicts ordinary text, and it is close to
irrelevant to what we need, which is: obey an exact output format, and stop.

Two failures on disk look like format failures rather than capability failures:
a model that left a required counts line as an unfilled template, and a model
that reasoned for two hours and emitted no answer at all. If 4-bit compression
degrades instruction-following disproportionately, both are explained by the
build rather than the model.

**This is distinct from Job 7.** That one is about compressing the cache during
a run. This one is about compressing the weights before it starts.

---

## PASTE THIS

```
I need published measurements, with links, on what 4-bit quantisation costs
in practice — specifically for instruction-following rather than perplexity.

Answer only from papers or benchmark results. Mark every claim QUOTED or
INFERRED — I discard everything INFERRED.

1. What published work measures quantised models on instruction-following
   benchmarks rather than perplexity? Name and link.

2. Is there evidence that quantisation degrades format adherence, structured
   output, or the ability to stop, more than it degrades general capability?
   Numbers, please.

3. How do the common llama.cpp quantisation levels compare — Q4_K_M, Q5_K_M,
   Q6_K, Q8_0 — on those instruction-following measures specifically?

4. Is there evidence that quantisation affects reasoning models differently
   from non-reasoning models? In particular, anything on quantised reasoning
   models failing to terminate their reasoning.

5. Is there any measurement of quantisation against verbatim quotation
   accuracy — reproducing exact text from a supplied document?

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- Say plainly which of the five questions the literature actually answers and
  which it does not.

Do not recommend a quantisation level. I am asking what has been measured.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

Questions 4 and 5 are the ones I expect to come back thin. If they do, that is
useful in itself: it means the properties this project depends on are ones
nobody publishes numbers for, and our own measurements are the only ones that
will ever exist for our case.

Question 3 is the practical one. If the cost between Q4 and Q5 is small on
format adherence and we have the memory headroom, that is a cheap experiment
worth running here later.

---

## BRING BACK

Numbers and links. And an honest list of which questions the literature simply
does not answer.
