# JOB 9 — which local models actually hold a strict output format?

Lowest priority. Do this only if the earlier jobs are done and there is time
left. Needs a platform with live web search.

---

## WHY

The pipeline has to survive models being swapped as better ones arrive. What it
needs from a model is narrow and unusual: read a large block of text, obey an
exact one-line output format, and **stop**. Raw capability is close to
irrelevant — a brilliant model that answers in three paragraphs is useless
here, and a modest one that answers in the required form is not.

Nobody benchmarks that property directly, so this job is a search for the
nearest available evidence, and a NOT FOUND is an acceptable outcome.

---

## PASTE THIS

```
I run local language models under Ollama on a machine with 16 GB of unified
memory, so a model plus its context has to fit in roughly 10 GB. I need
models that reliably obey a strict output format — for example, replying
with exactly one line in a fixed shape and nothing else — over inputs of a
few thousand tokens.

Answer with links. Mark every claim QUOTED or INFERRED.

1. Which published benchmarks measure instruction-following and output-format
   adherence specifically, as opposed to general capability? Name them and
   link them.

2. On those benchmarks, which openly available models under about 15 billion
   parameters score best? Give me the numbers and the source, not a ranking
   you assembled yourself.

3. Which of those models have a non-reasoning mode, or can have reasoning
   disabled? Quote the model card.

4. For each model you name: parameter count, the licence, and whether a
   quantised build is published on Ollama.

5. Is there published evidence that reasoning models are worse at strict
   output formats than non-reasoning models of similar size? Links, please.

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- Say plainly which of your answers rest on a benchmark and which rest on
  reputation. I will discard the reputation ones.

Do not tell me which model to choose. I am asking what the evidence is.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

Benchmark names with links and actual scores. Question 5 is the interesting
one: if there is evidence that reasoning models are systematically worse at
strict formats, then the model that has been burning our evenings was the wrong
class of model from the start, and that is a finding about how to choose, not
about which to choose.

---

## BRING BACK

The benchmark links and the numbers. **Not a recommendation.** A shortlist
assembled by a chat model from reputation is worth nothing here, and the
project's own failure log has entries about exactly that kind of confident,
unsourced output.
