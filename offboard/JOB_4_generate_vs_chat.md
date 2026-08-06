# JOB 4 — is the model being handed raw text with no instruction turn?

Needs a platform with live web search.

---

## WHY

`ollama show --modelfile qwen3.5:9b` reports:

```
TEMPLATE {{ .Prompt }}
RENDERER qwen3.5
PARSER qwen3.5
```

The template wraps nothing at all — it emits the prompt unchanged. The
formatting a chat model needs (system turn, user turn, the marker that tells it
to begin answering) is delegated to `RENDERER` and `PARSER`, which are newer
Ollama machinery.

Our runner calls **`/api/generate`** with a raw `prompt` string, not
`/api/chat` with messages.

If `RENDERER` only engages on the chat path, then every call this project has
made has handed the model a wall of unformatted text with no instruction turn
and no cue to begin answering. A reasoning model given that may simply
ruminate — which is what we are watching it do.

---

## PASTE THIS

```
Questions about Ollama's API. Answer from source code or official
documentation only, with links. Mark every claim QUOTED or INFERRED — I
discard everything INFERRED.

1. What are RENDERER and PARSER in an Ollama Modelfile? Which version
   introduced them, and what do they do?

2. Does RENDERER apply to requests sent to /api/generate, or only to
   /api/chat? Show me where in the source this is decided.

3. If a Modelfile's TEMPLATE is exactly "{{ .Prompt }}" and the request goes
   to /api/generate with a raw prompt string, what does the model actually
   receive? Does anything add chat control tokens, a system turn, or a
   generation prompt?

4. What does the "think" option do on /api/generate specifically? Is it
   supported on that endpoint, or only on /api/chat?

5. For a reasoning model, what tells it to stop reasoning and start
   answering? Is that a token the template supplies, something the renderer
   supplies, or something the model produces on its own?

6. Is there any documented case of a reasoning model producing unbounded
   reasoning and no answer when given an unformatted prompt?

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- Name one observation that would prove your answer to question 2 wrong.

Do not suggest fixes, endpoints to switch to, or improvements. I am not
asking for a design.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

**Question 2 decides it.** If `RENDERER` is chat-only, then our runner has been
using the wrong endpoint since the beginning, and every result on disk was
produced under conditions nobody intended.

That would be the largest finding of the four days — larger than any tuning
question — because it reaches backwards over every run in `runs/`, including
the one committed this afternoon.

---

## BRING BACK

The quotes and links. And a plain answer to question 2 in one word, because
that word decides whether the rest of the week's work is about tuning a model
or about repairing an instrument.
