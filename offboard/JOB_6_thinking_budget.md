# JOB 6 — does Ollama already have a thinking budget?

Needs a platform with live web search.

---

## WHY

We hold this problem back with a hand-rolled character ceiling: the runner
counts reasoning characters and gives up past a threshold. If Ollama exposes a
supported budget for the same thing, then ours is a duplicate control and the
Filter removes it — a control that duplicates an existing one fails on the
first pass, before anything else is considered.

There is a second reason. The run that started this went on for 8,412 seconds
and then **ended by itself**, normally, with an empty reply. Something stopped
it. If `num_predict` counts reasoning tokens, that is very likely what stopped
it, and the mystery dissolves.

---

## PASTE THIS

```
Questions about Ollama's generation limits. Answer from source code or
official documentation only, with links. Mark every claim QUOTED or
INFERRED — I discard everything INFERRED.

1. What is the default value of num_predict in Ollama when a request does
   not set it? Quote the source line that establishes the default.

2. Does num_predict count reasoning/thinking tokens, answer tokens, or the
   sum of both? Show me where this is decided in the code.

3. When num_predict is reached, how does the request end? Does the response
   carry a field naming the reason it stopped — and if so, what is that
   field called and what values can it take?

4. Is there any parameter in Ollama that limits reasoning specifically —
   a thinking budget, a reasoning-effort setting, a maximum thinking length,
   or anything equivalent? Which version introduced it?

5. If a generation ends because a limit was reached rather than because the
   model finished, is that distinguishable by a client reading the response?
   Name the exact field.

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- Name one observation that would prove your answer to question 5 wrong.

Do not recommend values or settings. I am not asking for a design.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

**Question 5 is the useful one.** Our failure record for the run says
`outcome: OK` — which is our own label, not the server's. If Ollama reports a
stop reason and we are throwing it away, then we have been recording "the model
finished" for runs where the model was cut off. That is a defect in our
instrument, and it is fixable in one line.

Questions 1 and 2 together may simply explain the 206,086 characters outright.

---

## BRING BACK

Quotes and links, and the name of the stop-reason field if one exists. That
field name is the single most actionable thing in this job.
