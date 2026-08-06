# JOB 1 — what `--context-shift` and `--keep` actually do in llama.cpp

Needs a platform with live web search: Gemini, ChatGPT search, or Perplexity.

---

## WHY

Our local server is running with `--context-shift --keep 4`. If a context shift
silently discards the prompt mid-generation, it explains two separate things at
once: a model reasoning for two hours and returning nothing, and an earlier run
that produced nine quotes which do not exist in the source. Both would be a
model answering a question it can no longer see.

This is one of three untested explanations, not the leading one. The other two
are a sampling penalty that may be preventing the model from ever stopping
(Job 3) and a template that may never format the prompt as a question at all
(Job 4). All three are cheap to check and any of them could be the whole
answer. This job settles this one.

---

## PASTE THIS

```
In llama.cpp's llama-server, what do the flags --context-shift and --keep do?

Answer only from source code or official documentation, with links. For every
claim, mark it QUOTED (you are reproducing text you found) or INFERRED (you
are reasoning about it). I will discard everything marked INFERRED.

1. When the KV cache fills during generation with --context-shift enabled,
   precisely which tokens are discarded and which are retained?
2. What is the unit of --keep? Tokens, messages, or something else? What does
   --keep 4 retain in practice?
3. After a shift, does generation continue or stop?
4. Is there ANY signal that a shift occurred — in the HTTP response body, in
   the SSE stream, in a field of the final JSON, or only in the server log at
   some verbosity? Name the field or log line.
5. Has the default for --context-shift changed between releases? Which release,
   and in which direction?
6. What happens with --context-shift disabled and the cache full?

Then, separately:
- List anything above you could NOT find a source for. Write NOT FOUND against
  each. A plausible description is worse than nothing to me.
- Name one thing that would prove your answer to question 4 wrong.

Do not suggest fixes, settings, or improvements. I am not asking for a design.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

- File and line references in the `llama.cpp` repository, not blog posts.
- A link to the flag documentation or the argument parser itself.
- At least one honest NOT FOUND. An answer with six confident sources and no
  gaps is the answer to be most suspicious of.

**Question 4 is the one that matters.** If a context shift is silent, then no
run this project has ever done can be trusted to have seen its own prompt, and
that reaches back over every result on disk.

---

## BRING BACK

The verbatim quotes and the links. Not the platform's summary of them — the
quotes themselves, so they can be checked against the repository here.
