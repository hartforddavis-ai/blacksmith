# JOB 14 — is 65,536 a real number or an advertised one?

Optional. Supports Job 11 — run it after, if the earlier answers leave the
question open. Needs a platform with live web search.

> **The Filter rejected this job on LEAN, 6 Aug.** Job 11 is smaller and covers
> the same ground: advertised-versus-effective context is a subset of the
> question of how recall degrades with length. Kept because it names the three
> quantities this project keeps conflating, and naming them is worth something
> on its own — but Job 11 first, and drop this one if Job 11 answers it.

---

## WHY

`ollama show gemma4:12b` reports a context length of 262,144. We run at 65,536.
Neither number has been tested here.

There are three different quantities being conflated across this project, and
they are routinely treated as one:

1. **What the model was trained to handle** — the architectural window.
2. **What we allocate** — `num_ctx`, which sizes the cache and the memory bill.
3. **What the model still uses well** — the length past which recall degrades.

Only the third one matters for whether a run can be trusted, and it is the only
one nobody publishes on the model card.

---

## PASTE THIS

```
I need published evidence, with links, on the gap between advertised and
usable context length.

Answer from papers, benchmark results, or model cards. Mark every claim
QUOTED or INFERRED — I discard everything INFERRED.

1. For open models advertising very long context windows — 128k tokens and
   above — what measurements exist of performance at those lengths versus
   at shorter lengths? Numbers and links.

2. Are there benchmarks designed specifically to expose the difference
   between advertised and effective context? Name them.

3. What techniques extend a model's advertised window after training, and do
   published results show quality falling off in the extended range?

4. Does allocating a larger context window than the prompt needs cost
   anything in output quality, as distinct from memory? Any measurement?

5. For the Qwen 3.x and Gemma model families specifically: what does
   published work say about effective context length?

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- Say plainly whether question 4 has an evidence-based answer or only
  folklore.

Do not recommend a context size. I am asking what is measured.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

Question 4 is the one with direct consequences here. This project has already
ruled once — correctly — that shrinking `num_ctx` to fit the prompt was a bad
idea, because Ollama truncates silently when the window is smaller than the
input and the truncated prompt still carries correct digest stamps. That ruling
stands regardless of what comes back.

What is still open is the other direction: whether allocating a large window
costs anything beyond memory. If the honest answer is folklore rather than
evidence, that is worth knowing before anybody tunes it again.

---

## BRING BACK

Numbers and links, and a clear statement of whether question 4 is answered by
evidence or by folklore.
