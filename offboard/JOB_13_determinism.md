# JOB 13 — does temperature 0 actually mean the same answer twice?

Optional. Needs a platform with live web search.

> **The Filter rejected this job on ROBUST.** No run here has ever been repeated
> on identical input, so nothing has been observed to differ, and "it might not
> reproduce" is a forecast rather than a demonstrated failure. Kept because the
> whole pipeline stamps digests on its runs, and a digest asserts something
> about reproducibility that has never been tested. Optional work — but if it
> comes back badly, it is the most serious finding in the folder.

---

## WHY

The pipeline runs everything at temperature 0 and stamps digests on the result.
The unstated assumption is that identical bytes in produce identical bytes out,
which is what makes a digest worth stamping.

Temperature 0 removes sampling randomness. It does not by itself guarantee
bit-identical output: floating-point reduction order can vary with batching,
with thread count, and with how work is scheduled onto the GPU. If two runs of
the same prompt can diverge, then a digest proves what was *sent*, not what
would happen again — and that is a much weaker claim than the one the pipeline
appears to make.

---

## PASTE THIS

```
I need documented evidence, with links, on whether local language model
inference is reproducible.

Answer from source code, issue trackers, or published measurements. Mark
every claim QUOTED or INFERRED — I discard everything INFERRED.

1. With temperature 0 and a fixed seed, is llama.cpp inference bit-identical
   across repeated runs on the same machine and same build? Where is this
   stated or demonstrated?

2. Does batch size, thread count, or GPU backend affect the output for an
   otherwise identical request? Any documented cases?

3. Specifically on Apple Metal: are there known reports of non-deterministic
   output from identical inputs?

4. Does Ollama pass a seed by default? What happens if a request does not
   set one, at temperature 0?

5. Are there open issues about non-reproducible output in llama.cpp or
   Ollama? Issue numbers and links.

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- Name one experiment that would settle question 1 on my own machine.

Do not suggest fixes. I am asking what is known.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

The last line matters more than usual here. If the platform names a clean local
experiment — run the same short prompt N times, compare the bytes — that is a
test worth running here in minutes, and it settles the question directly
without trusting anybody's documentation.

**If output is not reproducible**, then every digest this project stamps needs
its claim restated: it certifies what went in, not that the same thing comes
out. That is a documentation change, not a code change, but it is a change to
what the pipeline says about itself.

---

## BRING BACK

The answer to question 1, and the local experiment if one is named.
