# JOB 7 — is the compressed cache destroying long-range recall?

Needs a platform with live web search.

---

## WHY

The live server runs with:

```
--cache-type-k q8_0 --cache-type-v q8_0 --flash-attn on
```

The key/value cache is being stored at 8-bit rather than full precision. That
halves memory, which is why it is on — this machine has 16 GB and the model
wants roughly 8 GB of it.

The cost is accuracy of recall over long contexts. If quantising the cache
degrades a model's ability to retrieve exact detail from far back in its input,
that is a direct candidate for a run this project already has on disk: a model
that produced nine quotes which do not appear anywhere in the source it was
given. A degraded cache does not make a model refuse — it makes it approximate,
and an approximated quote is a fabricated quote.

---

## PASTE THIS

```
Questions about KV cache quantisation in llama.cpp. Answer from source,
official documentation, or published measurements with links. Mark every
claim QUOTED or INFERRED — I discard everything INFERRED.

1. What do --cache-type-k and --cache-type-v do, and what does q8_0 mean in
   this context? What is the default when neither flag is given?

2. What published measurements exist of the accuracy cost of q8_0 KV cache
   quantisation? I want benchmark numbers with links, not general statements
   that it is "usually fine".

3. Is the accuracy cost uniform across context length, or does it grow with
   distance? Specifically: is exact retrieval of detail from early in a long
   context affected more than nearby detail?

4. Is there any measurement of KV quantisation and verbatim quotation or
   exact-copy tasks, as opposed to perplexity? Perplexity is not the property
   I care about.

5. Are K and V equally sensitive to quantisation, or is one worse? Quote the
   measurements.

6. Does --flash-attn change any of the above?

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- Name one measurement that would prove your answer to question 3 wrong.

Do not recommend settings. I am not asking for a design.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

Numbers with links. Question 4 is the one I expect to come back NOT FOUND —
almost everything published measures perplexity, and perplexity is close to
useless for the property that matters here, which is whether a quote came out
of the text or out of the model.

A well-sourced NOT FOUND on question 4 is a genuine result: it means nobody has
measured the thing we care about, and we would have to measure it ourselves.

---

## BRING BACK

The benchmark numbers and links. And note honestly whether question 4 came back
empty, because that changes what we would need to build here.
