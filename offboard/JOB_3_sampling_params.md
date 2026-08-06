# JOB 3 — is a sampling parameter stopping the model from ever finishing?

Needs a platform with live web search.

---

## WHY

`ollama show --modelfile qwen3.5:9b` reports, among others:

```
PARAMETER presence_penalty 1.5
PARAMETER top_k 20
PARAMETER top_p 0.95
PARAMETER temperature 1
```

Our runner overrides `temperature` and the context size and **nothing else**, so
`presence_penalty 1.5` is in force on every call we have ever made.

A presence penalty pushes the model away from any token it has already used.
Sustained across two hundred thousand characters of reasoning, that includes
the token that ends the reasoning block. If that token is being penalised, the
model is being actively discouraged from ever stopping — which is precisely the
behaviour we are seeing.

This is the cheapest possible explanation on the table and it has not been
checked. It is also a hypothesis, not a finding. This job tests it.

---

## PASTE THIS

```
Questions about sampling parameters in llama.cpp and Ollama. Answer from
source code or official documentation only, with links. Mark every claim
QUOTED or INFERRED — I discard everything INFERRED.

1. Does presence_penalty have any effect when temperature is 0 (greedy
   decoding)? Are penalties applied to the logits before the argmax is taken,
   or are they skipped on the greedy path? Show me where in the sampling
   code this is decided.

2. Does presence_penalty apply to special tokens and control tokens — end of
   turn, end of sequence, and any token marking the end of a reasoning or
   thinking block? Or are special tokens exempt from penalties?

3. In Ollama, when a request to /api/generate supplies an "options" object
   containing some parameters, what happens to the parameters set in the
   model's Modelfile that the request did not mention? Are they kept, reset
   to library defaults, or dropped?

4. What is the accepted range for presence_penalty, and is 1.5 considered
   high? Quote any documented guidance rather than giving me an opinion.

5. Is there any documented interaction between a repetition or presence
   penalty and a model failing to emit its stop token?

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- Name one observation that would prove your answer to question 2 wrong.

Do not suggest settings, fixes or improvements. I am not asking for a design.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

Question 2 is the one that decides it. If special tokens are exempt from
penalties, this hypothesis is dead and should be crossed off. If they are not
exempt, it moves to the front of the queue and is testable here in minutes.

Question 3 matters nearly as much: if supplying a partial `options` object
resets everything else to defaults, then `presence_penalty` is *not* in force
and the premise collapses. Either answer is worth having.

---

## BRING BACK

The quotes and links, plus a plain yes/no on questions 2 and 3. Those two
answers between them either promote this to the leading explanation or kill it
outright, and both outcomes are cheap wins.
