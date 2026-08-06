# ALL JOBS — one file

Everything in this folder concatenated in the recommended order, for carrying on
a phone. This is a COPY. The separate files are the originals, and this one does
not update itself — rebuild it with `python3.12 export_all.py` after any edit.

The packets are NOT in here. Paste them whole and unaltered from
`packets/packet_a.txt` and the rest; a partial paste changes the task being
measured and nothing will tell you it happened.


========================================================================
FILE: README.md
========================================================================
# OFF-BOARD JOBS — four days

Fourteen jobs to run on free AI platforms while local capacity is spent. Each is
a single file. Open it, paste the block it gives you, bring the answer back.

**Where everything is:** `~/Documents/_PROJECTS/SOFTWARE/blacksmith/offboard/`

| what | where |
|---|---|
| the jobs | `JOB_1` … `JOB_14`, one file each |
| all of it in one file, for a phone | `ALL_JOBS.md` — a copy, rebuilt by the export, not a source |
| text to paste into a model | `packets/packet_a.txt` … `packet_e.txt` |
| the right answers | `packets/ANSWERS.txt` — **keep it shut until the packets are done** |
| where answers go | `RESULTS.md` |
| rebuild the packets | `python3.12 make_packets.py` |
| why any of this | **A NOTE ON THE PIPELINE**, at the bottom of this file |

The job numbers are labels, not an order. **The order is below.**

Disposable. Delete the whole directory once the answers are recorded and acted
on — it is a set of questions, not a part of the pipeline.

---

## THE THREE RULES

**1. Paste nothing of ours.** No file contents, no paths, no project name, no
kernel or job text. Every prompt in here is deliberately generic, and the
packets are invented weather-station prose. Free platforms train on what you
give them.

**2. Ask for quotes and links, never summaries.** A platform's paraphrase of a
document is exactly the kind of confident, unsourced output this project keeps
getting caught by. If it cannot quote a source, the honest answer is NOT FOUND,
and that is what should come back.

**3. Open every link before you write it down.** This is the one that will
actually bite. Asking a chat model for published citations is the single most
reliable way to get invented ones — plausible paper titles, real-looking arXiv
numbers that resolve to nothing or to something unrelated. The QUOTED/INFERRED
discipline in these prompts catches reasoning dressed up as fact; it does
nothing against a link that simply does not exist.

So: click it. If it 404s, if the paper is real but says something else, if the
quote is not on the page — **that citation is not evidence, and it goes into
`RESULTS.md` marked UNVERIFIED rather than being dropped.** A platform that
produced one invented citation has told you what the rest of its answer is
worth.

This project has already paid for this lesson once. The failure log, 5 Aug:
*"The ruling was accepted on re-derivation of its citations, never on the run's
own report."*

**Hard exclusion: do not ask any platform to design, fix, or improve anything.**
The failure log holds two entries where an unbound model was handed a broken
thing and built a replacement instead of removing it. These are fact-finding
and measurement jobs only. Every prompt already ends by saying so — leave that
line in.

---

## THE ORDER

### Day 1 — is the instrument even sound?

**`JOB_2_packet_test.md`** — packets a, b, c.
The only job here that produces a measurement rather than a fact, and the only
one that cannot be done on our own machine at any price. It asks whether the
counting task is well-formed, or whether the local models are simply failing
something that is broken to begin with. Do this first even if nothing else gets
done. Turn chat memory off before you start — the file explains why.

**`JOB_3_sampling_params.md`** — the cheapest explanation on the table.
A sampling penalty left in force by the model's own config may be actively
discouraging the model from ever stopping. Two of the five questions can kill
this idea outright, which is a good day's work either way.

### Day 2 — is the runner using the wrong door?

**`JOB_4_generate_vs_chat.md`** — potentially the largest mechanical finding.
If chat formatting only applies on the endpoint we are *not* using, then every
run in `runs/` was produced under conditions nobody intended.

**`JOB_5_known_issues.md`** — has somebody already found this and fixed it.
Half an hour of searching that could make several other jobs unnecessary.

### Day 3 — is the job we are asking even possible?

**`JOB_10_verification_ceiling.md`** — **the deepest question in the folder.**
Can a model this size verify quotes against a document at all? Every serious
entry in the failure log is that task going wrong. If the published answer is
no, then no amount of plumbing repair helps, and that reframes everything else
here.

**`JOB_11_retrieval_vs_length.md`** — how fast exact recall falls off with
length. The ramp is measuring this at four and a half hours per data point.
The literature may already have the curve, which would tell us which rungs are
worth measuring at all.

### Day 4 — the settings on the live server

**`JOB_1_context_shift.md`** — `--context-shift --keep 4`. Whether the model
quietly loses the question mid-answer.

**`JOB_6_thinking_budget.md`** — what actually stopped the run. It ended by
itself after 8,412 seconds, and our record calls that `OK` on our own authority
rather than the server's.

**`JOB_12_quantisation_and_format.md`** — whether 4-bit compression breaks
instruction-following before it breaks anything else.

### If there is time left

- **`JOB_7_kv_quantisation.md`** — the compressed cache and exact recall.
- **`JOB_13_determinism.md`** — does temperature 0 give the same answer twice.
  Rejected by the Filter as a forecast, kept because if it comes back badly it
  is the most serious finding here.
- **`JOB_14_effective_context.md`** — is 65,536 a real number or an advertised
  one.
- **`JOB_8_scale_test.md`** — packets d and e. Rejected by the Filter; drop
  this first.
- **`JOB_9_model_shortlist.md`** — what evidence exists about which models hold
  a strict output format.

---

## IF THERE IS TIME FOR ONLY ONE

**Job 2.** Everything else is a fact that can be looked up later, by anyone, at
any time. Job 2 is a measurement, and it is the only thing on this list that can
tell us the difference between a bad model and a bad question.

**If there is time for two, add Job 10** — for the reason in the note below.

---

## WHAT THE FILTER SAID ABOUT THIS FOLDER

Run 6 Aug, per part, so you know what to drop when time runs short.

- **Earned** — Job 2 (packets a and b), Job 3, Job 4, Job 5, Job 10, Job 11,
  Job 12. Each closes something that has actually failed here.
- **Not earned, kept anyway** — packet c, packets d and e, Job 8, Job 13.
  These answer questions where nothing has gone wrong yet. That is a forecast,
  not a failure, and the log has an entry about the cost of confusing the two.
- **Elaboration fired.** The demonstrated failures are closed by about half of
  this folder. The other half exists because a four-day budget was set, which
  is a legitimate reason to keep it and not a reason to pretend it was earned.

---

## WHY ANY OF THIS — where things stood, 6 Aug 2026

- `qwen3.5:9b`, on the **smallest** rung of the ramp, returned an empty reply
  after 8,412 seconds and 206,086 characters of reasoning. The retry did the
  same.
- Our own record of that run says `outcome: OK`.
- The live server runs with `--context-shift --keep 4` and an 8-bit key/value
  cache.
- The model's own config carries a presence penalty of 1.5, which our runner
  does not override.
- The model's template is `{{ .Prompt }}` — it wraps nothing — and formatting is
  delegated to machinery that may not apply to the endpoint we call.

Four candidate causes, none proven, all checkable by reading rather than by
burning another night of local compute. That is what makes them good off-board
work.

---

## A NOTE ON THE PIPELINE

Written 6 Aug, at the end of a long night. This is an observation about a
pattern in the failure log, not a proposal. What to do about it is Scott's call.

**The pipeline does two different kinds of checking, and only one of them has
ever failed.**

The first kind: a program works the answer out from the source itself. `quotes.py`
re-derives what the quotes actually are and compares. `cell` and `attest` count
bytes and hash them. These do not ask a model anything. **Nothing in this
category has ever produced a wrong answer.** They are also the parts that
survive a model being swapped for a better one, because they never depended on
the model in the first place.

The second kind: a model is handed a document and asked to say whether something
is true about it. **Every serious entry in `FAILURE_LOG.md` is this kind.** The
verify instrument ruled UNFIT for two fabricated VERIFIED rows. Nine quotes that
were not in the source. A counts line left as an unfilled template. Tonight, a
model that thought for two hours and answered nothing.

In every one of those cases the fabrication was caught in minutes by a plain
text search. It was never caught by the model, and in the UNFIT case the model's
own summary line — the one that would have exposed the problem — was the field
it left blank.

**That is the pattern, and it has been consistent since 5 August.** Programs
that re-derive: no failures. Models that certify: nothing but.

Most of the jobs in this folder ask *why the model is misbehaving tonight* —
which setting, which endpoint, which penalty. Those are worth answering and some
of them may well explain everything. But Jobs 10 and 11 ask the question
underneath: **is certifying quotes against a supplied document something a model
of this size can do reliably at all?**

If the published evidence says no, then tonight's investigation has been
diagnosing a symptom of a limit rather than a fault. The response would not be
to fix the model. It would be to know where the line is, and to stop treating a
model's verdict as evidence on its own — which the pipeline already half does,
in the parts that never fail.

If the evidence says yes, that is equally useful: it means the failures are ours
and there is something here to repair.

Either answer is worth more than another night of watching a spinner. That is
the whole argument for spending four days on reading instead of running.


========================================================================
FILE: JOB_2_packet_test.md
========================================================================
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


========================================================================
FILE: JOB_3_sampling_params.md
========================================================================
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


========================================================================
FILE: JOB_4_generate_vs_chat.md
========================================================================
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


========================================================================
FILE: JOB_5_known_issues.md
========================================================================
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


========================================================================
FILE: JOB_10_verification_ceiling.md
========================================================================
# JOB 10 — can a model of this size verify quotes at all?

**The deepest question in the set.** Needs a platform with live web search.

---

## WHY

The pipeline asks a local model to read a document it has been handed and
certify whether specific claims are supported by it. Every serious failure in
`FAILURE_LOG.md` is a version of that task going wrong:

- 5 Aug — the only completed reading of the verify instrument returned two
  VERIFIED rows that cite text which does not exist. Ruled UNFIT.
- 6 Aug — a run produced nine quotes not present anywhere in its source.

Both were caught by grep in minutes. Neither was caught by the model.

Every job in this folder up to now assumes the task is sound and something in
the plumbing is breaking it. This one asks the question underneath: **is
verifying quotes against a pasted document something a 9-to-12 billion
parameter model can do reliably at all?**

If the published answer is no, then no amount of context-shift fixing, penalty
tuning or endpoint correction will help, and the finding is worth more than
every other job here combined.

---

## PASTE THIS

```
I need published evidence, with links, about a specific capability: a
language model reading a document supplied in its prompt and correctly
judging whether a given quotation appears in that document verbatim.

Answer only from published papers, benchmarks, or model cards. Mark every
claim QUOTED or INFERRED — I discard everything INFERRED.

1. What benchmarks measure attributed or grounded generation — checking a
   claim against a supplied source rather than against world knowledge?
   Name them, link them.

2. What error rates do open models under roughly 15 billion parameters
   achieve on those benchmarks? Give numbers and sources.

3. Is there published evidence on models producing fabricated verbatim
   quotations attributed to a supplied source? What rates are reported, and
   does the rate change with document length?

4. Is there evidence that a model asked to verify its own or another model's
   citations performs better or worse than a simple string search?

5. Does asking a model to output a structured verdict per claim — verified,
   unsupported, misquoted — change its error rate compared with asking for
   free text? Any published comparison?

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- State plainly whether the published evidence supports or contradicts the
  idea that a sub-15B model can do this reliably.

Do not propose a system, a prompt, or an improvement. I am asking what is
known.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

Named benchmarks with numbers. Question 4 is the sharpest: if published work
finds that a model verifying citations is worse than a string search, then this
project has already built the right answer — `quotes.py` re-derives from source
and does not ask the model anything — and the model's role should be understood
in that light.

---

## BRING BACK

The benchmark names, the numbers, and the links. And the plain answer to the
final question, because it decides whether the rest of this investigation is
about repairing an instrument or about accepting a limit.


========================================================================
FILE: JOB_11_retrieval_vs_length.md
========================================================================
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


========================================================================
FILE: JOB_1_context_shift.md
========================================================================
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


========================================================================
FILE: JOB_6_thinking_budget.md
========================================================================
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


========================================================================
FILE: JOB_12_quantisation_and_format.md
========================================================================
# JOB 12 — does 4-bit compression break instruction-following first?

Needs a platform with live web search.

---

## WHY

The models here are Q4_K_M — the weights are compressed to roughly four bits.
That is standard practice and it is why an 12-billion-parameter model fits on
this machine at all.

The usual defence of 4-bit quantisation is that perplexity barely moves. But
perplexity measures how well a model predicts ordinary text, and it is close to
irrelevant to what we need, which is: obey an exact output format, and stop.

Two failures on disk look like format failures rather than capability failures:
a model that left a required counts line as an unfilled template, and a model
that reasoned for two hours and emitted no answer at all. If 4-bit compression
degrades instruction-following disproportionately, both are explained by the
build rather than the model.

**This is distinct from Job 7.** That one is about compressing the cache during
a run. This one is about compressing the weights before it starts.

---

## PASTE THIS

```
I need published measurements, with links, on what 4-bit quantisation costs
in practice — specifically for instruction-following rather than perplexity.

Answer only from papers or benchmark results. Mark every claim QUOTED or
INFERRED — I discard everything INFERRED.

1. What published work measures quantised models on instruction-following
   benchmarks rather than perplexity? Name and link.

2. Is there evidence that quantisation degrades format adherence, structured
   output, or the ability to stop, more than it degrades general capability?
   Numbers, please.

3. How do the common llama.cpp quantisation levels compare — Q4_K_M, Q5_K_M,
   Q6_K, Q8_0 — on those instruction-following measures specifically?

4. Is there evidence that quantisation affects reasoning models differently
   from non-reasoning models? In particular, anything on quantised reasoning
   models failing to terminate their reasoning.

5. Is there any measurement of quantisation against verbatim quotation
   accuracy — reproducing exact text from a supplied document?

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- Say plainly which of the five questions the literature actually answers and
  which it does not.

Do not recommend a quantisation level. I am asking what has been measured.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

Questions 4 and 5 are the ones I expect to come back thin. If they do, that is
useful in itself: it means the properties this project depends on are ones
nobody publishes numbers for, and our own measurements are the only ones that
will ever exist for our case.

Question 3 is the practical one. If the cost between Q4 and Q5 is small on
format adherence and we have the memory headroom, that is a cheap experiment
worth running here later.

---

## BRING BACK

Numbers and links. And an honest list of which questions the literature simply
does not answer.


========================================================================
FILE: JOB_7_kv_quantisation.md
========================================================================
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


========================================================================
FILE: JOB_13_determinism.md
========================================================================
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


========================================================================
FILE: JOB_14_effective_context.md
========================================================================
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


========================================================================
FILE: JOB_8_scale_test.md
========================================================================
# JOB 8 — does the task survive being made bigger?

Run this **only after Job 2**, and only if Job 2 came back clean.

> **The Filter rejected this job on 6 Aug, on ROBUST.** No rung above 500 tokens
> has ever run here, so nothing has failed at scale, and "it might break when
> bigger" is a forecast rather than a demonstrated failure. Kept because the
> owner set a four-day budget and it is cheap to run — but it is optional work,
> and it should be the first thing dropped if time runs short.

---

## WHY

The ramp climbs 500 → 1,000 → 2,000 → 4,000 → 8,000 tokens, on the assumption
that the task stays constant and only the size changes. That assumption has
never been checked.

If a strong model counts eight markers perfectly in a small packet and starts
missing them in a large one, then size alone breaks the task, and the ramp is
measuring the wrong thing — it would be recording "this model cannot handle
8,000 tokens" when the truth is "nobody can do this task at 8,000 tokens".

This is the same question Job 2 asks, asked at the top of the ladder instead of
the bottom.

---

## HOW TO RUN IT

Two packets in `packets/`:

| packet | size | markers |
|---|---|---|
| `packet_d.txt` | ~2,000 tokens (8,411 chars) | 8 |
| `packet_e.txt` | ~8,000 tokens (32,417 chars) | 8 |

Same rules as Job 2, and they matter more here because the packets are long
enough that a platform may quietly truncate them:

- **Paste the whole file. Add nothing.** Each ends with its own instruction.
- **Fresh chat for every packet on every platform.**
- **Check the paste actually went through.** Some free platforms silently cut
  long pastes or convert them to an attachment. If the platform shows an
  attachment rather than text in the message, that is a different experiment —
  note it, and try another platform.
- Both packets contain **the same number of markers**. Do not tell the model
  that. If a model returns the same number for both, that is either two correct
  answers or one habit, and only the wrong ones tell them apart.

Run `packet_d.txt` on every platform first, then `packet_e.txt`. Same models as
Job 2 if possible — a comparison across sizes is only readable if the model is
held constant.

---

## WHAT TO BRING BACK

Per platform, per packet:

1. Platform and model name.
2. The reply, verbatim.
3. Did it obey "one line and nothing else"?
4. Any sign the paste was truncated, attached, or summarised rather than read.

Point 4 is not housekeeping. A model answering from a truncated paste will give
a confident wrong number and nothing will indicate why, and that is the exact
failure mode this whole investigation is circling.

---

## WHAT IT DECIDES

- **Correct at both sizes** → the task holds at scale, the ladder is sound, and
  local failures at the top are real model limits.
- **Correct small, wrong large** → the ladder's upper rungs are unreadable, and
  the ramp should be cut back to the sizes where the task is known to work.
- **Wrong at both** → go back to Job 2; something is wrong with the task, not
  with the size.


========================================================================
FILE: JOB_9_model_shortlist.md
========================================================================
# JOB 9 — which local models actually hold a strict output format?

Lowest priority. Do this only if the earlier jobs are done and there is time
left. Needs a platform with live web search.

---

## WHY

The pipeline has to survive models being swapped as better ones arrive. What it
needs from a model is narrow and unusual: read a large block of text, obey an
exact one-line output format, and **stop**. Raw capability is close to
irrelevant — a brilliant model that answers in three paragraphs is useless
here, and a modest one that answers in the required form is not.

Nobody benchmarks that property directly, so this job is a search for the
nearest available evidence, and a NOT FOUND is an acceptable outcome.

---

## PASTE THIS

```
I run local language models under Ollama on a machine with 16 GB of unified
memory, so a model plus its context has to fit in roughly 10 GB. I need
models that reliably obey a strict output format — for example, replying
with exactly one line in a fixed shape and nothing else — over inputs of a
few thousand tokens.

Answer with links. Mark every claim QUOTED or INFERRED.

1. Which published benchmarks measure instruction-following and output-format
   adherence specifically, as opposed to general capability? Name them and
   link them.

2. On those benchmarks, which openly available models under about 15 billion
   parameters score best? Give me the numbers and the source, not a ranking
   you assembled yourself.

3. Which of those models have a non-reasoning mode, or can have reasoning
   disabled? Quote the model card.

4. For each model you name: parameter count, the licence, and whether a
   quantised build is published on Ollama.

5. Is there published evidence that reasoning models are worse at strict
   output formats than non-reasoning models of similar size? Links, please.

Then:
- List anything you could NOT source. Write NOT FOUND against each.
- Say plainly which of your answers rest on a benchmark and which rest on
  reputation. I will discard the reputation ones.

Do not tell me which model to choose. I am asking what the evidence is.
```

---

## WHAT A GOOD ANSWER LOOKS LIKE

Benchmark names with links and actual scores. Question 5 is the interesting
one: if there is evidence that reasoning models are systematically worse at
strict formats, then the model that has been burning our evenings was the wrong
class of model from the start, and that is a finding about how to choose, not
about which to choose.

---

## BRING BACK

The benchmark links and the numbers. **Not a recommendation.** A shortlist
assembled by a chat model from reputation is worth nothing here, and the
project's own failure log has entries about exactly that kind of confident,
unsourced output.


========================================================================
FILE: RESULTS.md
========================================================================
# RESULTS — paste answers in here as they come back

One section per job, in the order the README recommends. Paste raw. Do not tidy,
do not summarise, do not correct a model's spelling. The raw reply is the
evidence; anything else is a report about the evidence.

If a job produced nothing useful, write that. A recorded nothing is worth more
than a gap, because a gap looks like work not yet done.

**Every citation gets a verdict before it counts.** Open the link. Mark it
CHECKED if it resolves and says what the platform claimed, UNVERIFIED if it does
not. An unopened link is not evidence, and a platform that produced one invented
citation has told you what the rest of its answer is worth.

---

## JOB 2 — packet test

| platform / model | packet | reply verbatim | one line only? | memory off? |
|---|---|---|---|---|
| | a | | | |
| | b | | | |
| | c | | | |

Ground truth is in `packets/ANSWERS.txt`. **Do not open it until this table is
full.**

---

## JOB 3 — sampling parameters

Q2 — are special tokens exempt from presence_penalty? **YES / NO / NOT FOUND:**

Q3 — does a partial options object reset the rest? **KEPT / RESET / NOT FOUND:**

Quotes and links (CHECKED / UNVERIFIED):

---

## JOB 4 — generate vs chat

Q2 — does RENDERER apply to /api/generate? **YES / NO / NOT FOUND:**

Quotes and links (CHECKED / UNVERIFIED):

---

## JOB 5 — known issues

Issue links found, or NOTHING FOUND (CHECKED / UNVERIFIED):

Model card guidance on sampling parameters:

---

## JOB 10 — verification ceiling

Does the published evidence support or contradict a sub-15B model doing this
reliably? **SUPPORTS / CONTRADICTS / NOT FOUND:**

Q4 — model verifying citations versus a plain string search:

Benchmarks and numbers (CHECKED / UNVERIFIED):

---

## JOB 11 — retrieval versus length

Q4 — gap between advertised and reliable context, with numbers:

Q5 — is counting measured anywhere against length? **YES / NOT FOUND:**

Benchmarks and numbers (CHECKED / UNVERIFIED):

---

## JOB 1 — context shift

Q4 — is a context shift visible to a client? **YES (field: ) / NO / NOT FOUND:**

Quotes and links (CHECKED / UNVERIFIED):

---

## JOB 6 — thinking budget

Q5 — name of the stop-reason field, if any:

Q2 — does num_predict count reasoning tokens? **YES / NO / NOT FOUND:**

Quotes and links (CHECKED / UNVERIFIED):

---

## JOB 12 — quantisation and format

Q2 — does quantisation hit format adherence harder than capability?

Q4/Q5 — reasoning termination, verbatim quotation: answered or NOT FOUND?

Numbers and links (CHECKED / UNVERIFIED):

---

## JOB 7 — KV cache quantisation

Q4 — any measurement against verbatim quotation?

Numbers and links (CHECKED / UNVERIFIED):

---

## JOB 13 — determinism

Q1 — is temperature-0 output bit-identical across runs? **YES / NO / NOT FOUND:**

The local experiment it named, if any:

---

## JOB 14 — effective context

Q4 — evidence or folklore?

Numbers and links (CHECKED / UNVERIFIED):

---

## JOB 8 — scale test

| platform / model | packet | reply verbatim | one line only? | paste intact? |
|---|---|---|---|---|
| | d | | | |
| | e | | | |

---

## JOB 9 — model shortlist

Benchmarks found, with links (CHECKED / UNVERIFIED):

Which answers rest on a benchmark, and which on reputation:

---

## RUNNING COUNT — invented citations

Tally them here as you go. Platform, what it claimed, what the link actually
was. This is its own finding: it measures how much any of these answers can be
trusted, and it is the same measurement the pipeline exists to make.

| platform | claimed | what was actually there |
|---|---|---|
| | | |
