# JOB 11 — how fast does exact recall fall off as the document gets longer?

Needs a platform with live web search. Run after Job 10 — same territory,
narrower question.

---

## WHY

The run that fabricated nine quotes was given 40,878 characters. The ramp
climbs to 8,000 tokens for the same reason: to find where a model stops coping.

But the ramp measures one model on one machine, slowly, and there is a large
published literature on exactly this. If effective recall collapses well below
the advertised window — and the phrase "lost in the middle" exists because it
does — then the ramp is rediscovering a known curve at a cost of roughly four
and a half hours per data point.

Knowing the published curve does not replace measuring our own. It tells us
which rungs are worth measuring.

---

## PASTE THIS

```
I need published evidence, with links, on how exact retrieval from a prompt
degrades as the prompt gets longer.

Answer only from papers or benchmark results. Mark every claim QUOTED or
INFERRED — I discard everything INFERRED.

1. What is the "lost in the middle" effect? Link the original work and any
   replication. Does it apply to current models or was it specific to older
   ones?

2. What benchmarks measure long-context retrieval beyond simple
   needle-in-a-haystack? Name and link them. What do they add?

3. For open models around 9 to 14 billion parameters: at what input length
   does exact retrieval accuracy begin to fall measurably? Give numbers with
   sources.

4. Is there a documented gap between a model's advertised context window and
   the length at which it still retrieves reliably? How large, for which
   models?

5. Does counting or enumerating items scattered through a long document
   behave like retrieval, or is it a separate and harder task? Any published
   measurement of counting accuracy against document length?

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- Name one result that would prove your answer to question 4 wrong.

Do not recommend context sizes or models. I am asking what is measured.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

Question 5 is the one that matters most and the one most likely to come back
NOT FOUND. Counting markers is not the same task as finding one needle: a
needle can be found by attending to one region, while counting requires
attending to all of them at once and keeping a running total. If nobody has
measured counting against length, that is a genuine gap, and it means our ramp
is measuring something the literature does not cover — which makes it more
valuable, not less.

Question 4 tells us whether running at a 65,536-token window is meaningful or
whether the model stopped retrieving reliably long before that.

---

## BRING BACK

Numbers and links, and an honest note on whether question 5 came back empty.
