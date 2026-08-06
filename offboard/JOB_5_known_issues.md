# JOB 5 — has someone already found and fixed this?

Needs a platform with live web search.

---

## WHY

The cheapest possible outcome of the whole four days is discovering that this
is a known bug with a known fix and a version number. Worth one search before
any more thinking is spent on it.

---

## PASTE THIS

```
Search GitHub issues and discussions on ollama/ollama and ggml-org/llama.cpp
for reports matching this behaviour:

A reasoning model produces a very long chain of thought and then returns an
empty final response. Reasoning tokens are present, the content field is
empty, and the request completes normally rather than erroring or timing out.

I am specifically interested in the qwen3 and qwen3.5 model families running
under Ollama with thinking enabled.

For each match give me: issue number, title, link, open or closed, the
version it was reported against, and the maintainer's explanation if there
is one. If it was fixed, give me the release that fixed it.

Also search for:
- reports of a model never emitting its end-of-thinking token
- reports of reasoning continuing until the context window is exhausted
- reports of empty content with non-empty reasoning on /api/generate

If there are no such reports, say so plainly. Do not describe what the cause
might be — I want issue links or nothing.
```

---

## SECOND SEARCH, IF THE FIRST COMES BACK EMPTY

```
What is the current recommended way to run qwen3.5 under Ollama with
reasoning enabled? Quote official model card guidance or maintainer comments,
with links — not community blog posts.

Specifically: which API endpoint, which sampling parameters, and whether the
model card names any parameter that must NOT be changed.

Mark every claim QUOTED or INFERRED. List anything you could not source as
NOT FOUND.
```

The second search is worth running even if the first succeeds. A model card
that says "do not set temperature to 0" would explain a great deal, given that
our runner sets temperature to 0 on every call.

---

## BRING BACK

Issue numbers and links, or a clear "nothing found". A clear nothing-found is
a real result — it means the behaviour is ours, not the stack's, and that
narrows the search here considerably.
