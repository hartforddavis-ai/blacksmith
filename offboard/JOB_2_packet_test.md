# JOB 2 — is the task well-formed, or are the local models just failing it?

**Run this one first.** It produces a measurement, not a fact, and it is the
only job here that cannot be done on our own machine at any price.

---

## WHAT IT DECIDES

Locally, two models have now failed a counting task. We do not know whether
that is the models or the task. This tells us.

- **Strong models all count correctly** → the task is clean, and the local
  models are failing something frontier models find trivial. That is a
  model-selection finding, and the ramp is measuring what it claims to.
- **Strong models miscount or waffle** → the task is ambiguous, and every row
  the ramp ever produces is unreadable. That kills the ramp, not the models,
  and it is the more valuable answer of the two.

---

## HOW TO RUN IT

Three of the five packets in `packets/` belong to this job — a, b and c. The
other two are for Job 8. Each is a complete prompt: it ends with its own
instruction, so **paste the whole file and add nothing**. Not a word of
framing, no "please", no "this is a test". Added words are a different
experiment.

Use at least three different free platforms. Suggested: ChatGPT, Gemini,
Claude, DeepSeek, Qwen, Mistral — whichever are reachable.

**Fresh chat for every single packet — and turn persistent memory OFF.** A new
chat is not a clean room on platforms that remember across conversations.
ChatGPT, Gemini and others carry memory between chats by default, so a model
can see what it answered an hour ago and repeat it. Use a temporary or
incognito chat, or switch memory off in settings, before the first packet.

Without that, packet B measures nothing: its whole purpose is to catch a model
repeating A's answer, and a model with memory has a legitimate route to A's
answer that has nothing to do with counting.

Run them in this order: **A, then C, then B.**

**If a packet fails and you are unsure whether the model saw an earlier one,
record that doubt in `RESULTS.md`.** A result with a known hole in it is usable.
A result with an unrecorded hole is worse than no result.

| packet | what it is |
|---|---|
| `packet_a.txt` | Faithful replica of the local rung — plain markers, no traps. The direct comparison. |
| `packet_c.txt` | Same idea plus near-miss lines: single brackets, lowercase, a tag with no number. Every one of them fails the stated rule literally, so the right answer is not a judgement call. Tests precision. |
| `packet_b.txt` | A different number of markers, no traps. **The control.** Anything that answered A confidently and returns the same number here was pattern-matching, not counting. |

`ANSWERS.txt` holds the ground truth, verified by exact-match line count and
not by eye. **Do not open it until every model has replied.** Knowing the
number changes how you read a wrong answer.

---

## WHAT TO BRING BACK

Per platform, per packet, four things:

1. Platform and model name, with version if shown.
2. The reply, **verbatim** — including anything before or after the count.
3. Did it obey *"Reply with one line and nothing else"*? Yes or no.
4. Roughly how long it took, and whether it visibly showed reasoning.

Point 3 matters as much as the number. A model that counts correctly but
buries it in three paragraphs of explanation fails the format the pipeline
depends on, and that is a finding in its own right.

---

## WHAT NOT TO DO

- **Do not tell it the answer, or that markers were "planted", or that this
  is a test.** It will count more carefully than it otherwise would, and the
  measurement is then worthless.
- **Do not re-ask a model that got it wrong.** A second attempt after an
  implied correction measures nothing. One shot each, recorded as it fell.
- **Do not ask it to explain its count** until after it has answered and you
  have recorded the answer. If you want the reasoning, ask in a follow-up
  message, and note that the first reply was already recorded.
