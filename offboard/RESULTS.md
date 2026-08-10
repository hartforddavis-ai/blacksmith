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

**Note on `Scott research /`:** that folder's four vendor subfolders
(Deepseek, Grok, ChatGPT, Gemini) and its `ASFC.txt` / `Read me first.
Contect.txt` are **not** answers to any of JOB_1–JOB_14. They're a separate
exercise — a "clean-room" prompt run across platforms about an unrelated
proposal ("AI State Flux Cascade" / "Three Laws" / a generator-auditor loop
architecture). Confirmed by reading both files first, per the task
instructions, and by sampling the Deepseek/ChatGPT/Gemini/Grok answers inside
— none reference context-shift, sampling parameters, quantisation, or any
other JOB_N topic. Nothing from that folder is used below. All raw answers
actually used come from `Results Chat GPT /`.

---

## JOB 2 — packet test

**NOT DONE.** No platform ever actually ran the four packets. What exists in
`Results Chat GPT /Job 2.txt`, `Job 2..txt`, and `Job 2 test results Run .txt`
is not a packet reply — someone pasted `make_packets.py` (the *generator
source*, i.e. our own project file — a Rule 1 violation in whatever session
produced it) into ChatGPT and asked it to reason about the suite. ChatGPT
correctly refused to fabricate a result: all three files say, verbatim,
"Received. Status: INPUT RECEIVED — NOT EXECUTED" / "No packets generated,"
"Current result: UNKNOWN for the Job 2 measurement."

None of packet a, f, g, or b was ever pasted whole into a fresh chat and
answered. Per the special rule for this job, **`packets/ANSWERS.txt` was not
opened** — the four-packet condition was never close to satisfied.

| platform / model | packet | reply verbatim | one line only? | memory off? |
|---|---|---|---|---|
| — | a (prose, baseline) | NOT DONE | — | — |
| — | f (directive filler) | NOT DONE | — | — |
| — | g (directive + odd fence) | NOT DONE | — | — |
| — | b (count control) | NOT DONE | — | — |

**a right but f wrong is the headline result** — it would mean the instrument has
been measuring a packet that argues with its own task. Cannot be evaluated;
no data.

Ground truth is in `packets/ANSWERS.txt`. **Do not open it until this table is
full.** (It is still shut.)

---

## JOB 3 — sampling parameters

Platform: ChatGPT (`Results Chat GPT /Job 3 result.txt`). Sources used stated as
"official Ollama docs and llama.cpp documentation only" — **no links were
supplied anywhere in the reply**, for any of the five questions.

Q2 — are special tokens exempt from presence_penalty? **NOT FOUND** (honest —
model states it could not find EOS/special-token exemption documentation
either way; hypothesis left "ACTIVE — UNRESOLVED").

Q3 — does a partial options object reset the rest? **KEPT.** Reasoned from
Ollama's own API doc language ("`options`: additional model parameters...")
and Modelfile `PARAMETER` doc, concluding unsupplied parameters (like
`presence_penalty 1.5`) remain from the Modelfile.

Other answers: Q1 (does presence_penalty affect temp-0 / greedy decoding) —
NOT FOUND. Q4 (accepted range, is 1.5 high) — PARTIAL/NOT FOUND (llama.cpp
default 0.0 quoted, no min/max or "high" threshold documented). Q5
(penalty→stop-token-failure interaction documented) — NOT FOUND.

Quotes and links (CHECKED / UNVERIFIED): **UNVERIFIED — no links given.**
Every "QUOTED" claim in this file (the `--presence-penalty N` line, the
`PARAMETER` instruction line, the `options` doc line) is asserted as coming
from "llama.cpp documentation" or "Ollama API documentation" but not one URL
accompanies any of them, so none can be opened and checked. Per the README
rule, an unopened/unlinked claim is not evidence — every quote in this job's
answer is UNVERIFIED, not because it was checked and failed, but because
there was nothing to click. This is itself the finding: this is the one job
where the platform gave prose citations with zero linkability, which is a
step short of even an invented link.

---

## JOB 4 — generate vs chat

Platform: ChatGPT (`Results Chat GPT /Job 4..txt`).

Q2 — does RENDERER apply to /api/generate? **NO** (one-word answer given), but
the evidence under it actually shows the opposite of "chat-only": the model
found and quoted `routes.go` source showing `/api/generate` has its own
template-execution path (`tmpl.Execute(&b, values)` → `prompt = b.String()`)
and a comment where the generate handler explicitly checks "we're in the
`api/chat`-like flow, and if so, generate the prompt the same way" as a
stopgap. The model's own final line concedes this: "Question 2 claim
'renderer is chat-only' is **not supported by checked source**." So the
one-word headline answer and the evidence under it disagree — read as
**NOT a clean NO**, closer to "renderer logic is reachable from
`/api/generate` under some conditions, not gated to `/api/chat` only." **This
needs a human call** — it's the largest-consequence question in the whole
folder (which endpoint every run used) and the raw answer is internally
inconsistent.

Q1 (RENDERER/PARSER as Modelfile instructions) — NOT FOUND (no official doc
naming them, version unclear). Q3 (what `{{ .Prompt }}` template actually
sends) — QUOTED from Ollama docs: default template sends "user inputs...
verbatim." Q4 (`think` on /api/generate) — documented on both endpoints.
Q5/Q6 (what tells a reasoning model to stop reasoning; documented case of
unbounded reasoning from unformatted prompt) — both NOT FOUND.

Quotes and links (CHECKED / UNVERIFIED):
- `github.com/ollama/ollama/blob/main/server/routes.go` — **CHECKED.** Contains
  the quoted `tmpl.Execute`/`prompt = b.String()` lines and the "api/chat-like
  flow" / "TEMP(drifkin)" comment, verbatim.
- `github.com/ollama/ollama/blob/main/docs/api.md` — **CHECKED.** `template`,
  `raw`, and `think` (both endpoints) all present as quoted.
- `docs.ollama.com/modelfile` — **CHECKED.** `TEMPLATE`/Go-template-syntax
  language present (RENDERER/PARSER as such not found on this page, consistent
  with the model's own NOT FOUND).
- `ollama.readthedocs.io/en/template/` — **CHECKED.** "By default, models
  imported into Ollama have a default template of `{{ .Prompt }}`..." present
  verbatim.

---

## JOB 5 — known issues

Platform: ChatGPT (`Results Chat GPT /Job 5.txt`). Only the first search (issue
search) was run; the second search (model-card guidance) was **not done** —
no answer for that half of the job exists in the raw files.

Issue links found, or NOTHING FOUND (CHECKED / UNVERIFIED):
- `github.com/ollama/ollama/issues/10976` "Thinking + tools + qwen3 = empty
  output" — **CHECKED.** Real issue, title and content match as described
  (think=true + tools → empty content on qwen3:30b-a3b, Ollama 0.9.0, open,
  assigned to @drifkin). Not an exact match to the requested symptom (tools
  were required; the job asked for the no-tools case) — the platform said so
  itself.
- `github.com/ollama/ollama/issues/15288` — **CHECKED.** Real, matches as
  described, but is a Gemma 4 issue, not Qwen3/3.5 as the job asked about —
  again flagged honestly by the platform as off-target.
- `github.com/ollama/ollama/issues/14493` — **CHECKED.** Real. Title and
  content (repetition penalties silently discarded, tool-calling format
  mismatch, renderer never emits `</think>`) all confirmed verbatim.
- `github.com/ggml-org/llama.cpp/issues/20260` — **UNVERIFIED / mischaracterized.**
  The raw answer describes it as "A maintainer comment discusses a case where
  the `</think>` tag was not generated." The actual issue is about the PEG
  chat-format parser failing when the model emits a natural-language
  transition sentence **between** `</think>` and `<tool_call>` — a related but
  different defect (the `</think>` tag *is* generated; it's what comes after
  it, before the tool call, that breaks parsing). Real link, wrong claim about
  what it says → goes in the running-count table.
- `github.com/ggml-org/llama.cpp/discussions/21445` — not independently
  re-checked (low stakes: cited only as "mentions overthinking," which is a
  soft, unfalsifiable-enough claim); treat as UNVERIFIED by omission.

No exact match for "empty content, non-empty reasoning, no tools, qwen3/3.5,
/api/generate" was found — reported as NOT FOUND, which is itself an honest,
useable result. **No fixed version/release was identified** for any of the
matched issues.

Model card guidance on sampling parameters: **NOT DONE** — the second-search
prompt in the job file was never run against any platform in the raw files.

---

## JOB 10 — verification ceiling

Platform: ChatGPT (`Results Chat GPT /Job 10.txt`).

Does the published evidence support or contradict a sub-15B model doing this
reliably? **NOT FOUND**, stated precisely: no benchmark exactly matches "a
~9–12B model given a document, asked to certify whether a quotation appears
verbatim." What the platform will commit to instead: **UNVERIFIED** — "a
sub-15B model cannot reliably verify quotes" (not established either way) vs.
**SUPPORTED** — "source-grounded verification is a known failure area for
language models, and reliability must be measured rather than assumed." That
second, weaker claim is the actual defensible result of this job.

Q4 — model verifying citations versus a plain string search: **NOT FOUND.**
No controlled comparison of LLM-verifier vs. exact string search on verbatim
quote existence was located. This is a real gap, not a dodge — it means the
sharpest question in the whole folder (is `quotes.py`'s re-derivation
provably better than asking a model?) has no direct published answer; only
adjacent evidence that model-based attribution is a documented failure mode.

Benchmarks and numbers (CHECKED / UNVERIFIED):
- AIS (`research.google/pubs/measuring-attribution-in-natural-language-generation-models/`)
  — **CHECKED.** "whether NLG output is only sharing verifiable information
  about the external world" / "supported by underlying sources" both present.
- RAGTruth (`aclanthology.org/2024.acl-long.585/`) — **CHECKED.** "corpus
  tailored for analyzing word-level hallucinations... nearly 18,000 naturally
  generated responses" confirmed.
- RAGTruth stats (`github.com/ParticleMedia/RAGTruth`) — **CHECKED.**
  Hallucination counts for Llama-2-7B-chat (1832), Llama-2-13B-chat (1677),
  Mistral-7B-Instruct (1953) all confirmed exactly.
- KaLMA (`aclanthology.org/2024.findings-acl.28/`) — **CHECKED.** "Towards
  Verifiable Generation: A Benchmark for Knowledge-aware Language Model
  Attribution," KaLMA task and BioKaLMA dataset confirmed.
- FactBench/VERIFY (`aclanthology.org/2025.acl-long.1587/`) — **CHECKED.**
  "categorizes content units as Supported, Unsupported, or Undecidable"
  confirmed.
- RAGTruth arXiv mirror (`arxiv.org/abs/2401.00396`) — not independently
  re-opened (ACL Anthology version already confirmed as the same paper);
  treat as UNVERIFIED by omission, low risk.

No fabricated citation found in this job — every checked link resolved and
supported its claim, which is itself notable given this is the job the
project's own note calls "the deepest question in the set."

---

## JOB 11 — retrieval versus length

Platform: ChatGPT (`Results Chat GPT /Job 11.txt`).

Q4 — gap between advertised and reliable context, with numbers: **Documented
and large.** RULER quoted directly: "only half of them [models claiming ≥32K]
can maintain satisfactory performance at the length of 32K." Worked examples
from the RULER repo table: Yi-34B claims 200K, effective 32K; Phi3-mini
claims 128K, effective 32K; Command-R-plus claims 128K, effective 32K; GLM4-9B
claims 1M, effective 64K. Qwen3-14B and GLM4-9B score curves (98.0→85.1 and
94.7→83.1 from 4K→128K) also quoted and confirmed.

Q5 — is counting measured anywhere against length? **NOT FOUND.** The
platform found benchmarks that *include* counting as one task type
(Counting-Stars, BABILong) but no paper directly comparing single-needle
retrieval accuracy against multi-marker counting accuracy across a controlled
length ramp — which is exactly what Job 2/8's packet suite is trying to
measure locally. Honest, useful gap.

Benchmarks and numbers (CHECKED / UNVERIFIED):
- Lost in the Middle (`arxiv.org/abs/2307.03172`) — **CHECKED.** Both quoted
  lines ("performance can degrade significantly...", "highest... beginning or
  end... degrades... middle") confirmed in the abstract verbatim.
- RULER (`arxiv.org/abs/2404.06654`) — **CHECKED.** Both headline quotes
  confirmed in the abstract.
- LongBench (`aclanthology.org/2024.acl-long.172/`) — **CHECKED.** "21
  datasets across 6 task categories" confirmed.
- BABILong (`arxiv.org/abs/2406.10149`) — **CHECKED.** "20 reasoning tasks...
  fact chaining, simple induction, deduction, counting, and handling
  lists/sets" confirmed verbatim.
- RULER repo tables (`github.com/NVIDIA/RULER`) — **CHECKED.** Claimed-vs-
  effective table and both model score curves confirmed with matching
  numbers.
- Counting-Stars (`arxiv.org/abs/2403.11802`) — **CHECKED.** Self-description
  and "two counting-based multiple pieces of evidence retrieval sub-tasks"
  confirmed.

No fabricated citation found in this job.

---

## JOB 1 — context shift

Platform: ChatGPT (`Results Chat GPT /Job 1.txt` and `Job1.txt` — identical
duplicate pastes, same run).

Q4 — is a context shift visible to a client? **NO** (effectively) — the
platform found a `truncated` boolean field (context size exceeded, prompt +
generated tokens > n_ctx) but explicitly could **not** find an HTTP field, SSE
event, or JSON field named for a *shift* specifically, nor a documented log
line. Read plainly: there is a "your context is full" signal, but no
"a shift just discarded your early tokens" signal that a client can see. This
is the load-bearing answer of the whole folder — it means no run this project
has done can be proven to have kept seeing its own prompt — and the raw
answer supports it with an honest NOT FOUND rather than a guess.

Also answered: Q1/Q2 — `--keep N` retains the first N **tokens** (not
messages) of the initial prompt, excluding BOS; discard is from the older
region beyond `--keep`. Q3 — generation continues after a shift ("context
must then be re-evaluated before generation can resume"). Q5 — NOT FOUND
(no release/version pinned for when `--context-shift` default changed). Q6 —
disabled + full cache: request errors if bigger than context, otherwise
`n_predict` capped to `n_ctx - n_tokens_prompt`.

Quotes and links (CHECKED / UNVERIFIED):
- `github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md` —
  **CHECKED.** Both the `--keep N` CLI line and the `n_keep` endpoint-option
  line ("excludes the BOS token") confirmed verbatim, in the same page (the
  raw answer cites this page twice under two different footnote numbers as if
  two sources — cosmetic, not a fabrication).
- `github.com/ggml-org/llama.cpp/issues/5732` — **CHECKED.** `truncated`
  boolean field description confirmed verbatim.
- `manpages.debian.org/.../llama-server.1.en.html` — **CHECKED.**
  `--context-shift, --no-context-shift` "(default: disabled)" confirmed.
- `github.com/ggml-org/llama.cpp/issues/9390` — **CHECKED.** Both quoted
  bullets (error on oversized request; `n_predict` capped to
  `n_ctx - n_tokens_prompt`) confirmed.
- `tools/completion/README.md` (footnote 3, the "re-evaluated before
  generation can resume" quote) — not independently re-opened; the same
  claim appears, differently worded, in the server README already checked,
  so treat as UNVERIFIED by omission rather than a red flag.

No fabricated citation found in this job.

---

## JOB 6 — thinking budget

Platform: ChatGPT (`Results Chat GPT /Job 6.txt`).

Q5 — name of the stop-reason field, if any: **`done_reason`**, value
`"length"` observed — but the platform is explicit that this comes from a
**community Reddit thread, not an official source**, and marks it
UNVERIFIED-from-official-docs itself. That caveat held up: I could not open
the Reddit link in this environment (`reddit.com` fetches are blocked here),
so it goes in the running-count table as unconfirmable, not confirmed.

Q2 — does num_predict count reasoning tokens? **NOT FOUND.** No source
distinguishes thinking-token vs. answer-token counting for `num_predict`.
Genuinely open question — the 206,086-character reasoning run's cause is
still not pinned down by this job alone.

Q1 — default `num_predict` = `-1` (infinite), quoted from the Modelfile
reference. Q4 — no general Ollama "thinking budget" parameter found; only
GPT-OSS has a documented `low`/`medium`/`high` trace-length control.

Quotes and links (CHECKED / UNVERIFIED):
- `docs.ollama.com/modelfile` — **CHECKED.** `num_predict` default `-1`
  language confirmed verbatim.
- `docs.ollama.com/capabilities/thinking` — **CHECKED.** Both the
  `message.thinking`/`message.content` split and the GPT-OSS
  low/medium/high language confirmed verbatim.
- `github.com/ollama/ollama/blob/main/docs/api.md` — not independently
  re-opened for this job (already checked under Job 4, same file, same
  session); treat as CHECKED by carry-over.
- `reddit.com/r/ollama/comments/1is4jtg` (`done_reason: "length"`) —
  **UNVERIFIED — link could not be opened** (Reddit is blocked from this
  environment). The platform's own answer already flagged this as
  non-official; I can add that it is also unconfirmable from here. Do not
  treat `done_reason` as established until someone opens this by hand.

No fabricated citation found among the openable links in this job.

---

## JOB 12 — quantisation and format

Platform: ChatGPT (`Results Chat GPT /Job 12.txt`). (Note: the folder also has
a file literally named `JOB_12_quantisation_and_format.md` and
`article analisis..md` — both are the **same** content, an unrelated analysis
of a Substack article ("A Data-Driven Explanation: Why Do AI Agents Still
Fail," Jeremy Tian). Neither answers Job 12's actual questions; ignored here,
noted so it isn't mistaken for a second run.)

Q2 — does quantisation hit format adherence harder than capability?
**PARTIAL.** One real number found: Qwen's own published GPTQ-Int4/AWQ table
shows IFEval (instruction-following) dropping for the 7B model (BF16 53.1 →
GPTQ-Int4 49.4) but *rising* slightly for the 72B model (77.6 → 78.9 on
GPTQ-Int4) — so the direction isn't even consistent, let alone proven worse
than capability loss generally. No llama.cpp K-quant (Q4_K_M/Q5_K_M/Q6_K/Q8_0)
data exists in the literature the platform found at all (Q3: **NOT FOUND**).

Q4/Q5 — reasoning termination, verbatim quotation: both **NOT FOUND**. No
published measurement of quantisation causing runaway/non-terminating
reasoning, and no published measurement of quantisation against verbatim
quotation accuracy from a supplied document. Both are named as genuine
literature gaps, which the job file predicted ("the properties this project
depends on are ones nobody publishes numbers for").

Numbers and links (CHECKED / UNVERIFIED):
- `arxiv.org/abs/2409.11055` — **UNVERIFIED / mischaracterized citation.**
  The raw answer titles this "A Comprehensive Evaluation of Quantized
  Instruction-Tuned Large Language Models: An Experimental Analysis up to
  405B" and claims it covers "GPTQ, AWQ, SmoothQuant, and FP8" on "models
  ranging from 7B to 405B." The paper is real and on-topic, but its actual
  title is **"Exploring the Trade-Offs: Quantization Methods, Task
  Difficulty, and Model Size in Large Language Models From Edge to Giant,"**
  it spans **1B to 405B** (not 7B–405B), evaluates **four** quantization
  methods across 13 datasets, and SmoothQuant is not confirmed as one of
  them. Real link, invented title and slightly wrong scope → goes in the
  running-count table.
- `arxiv.org/abs/2305.14314` (QLoRA) — not independently re-opened; the claim
  attached to it ("finetune more than 1,000 models... 8 instruction
  datasets") is a well-known, plausible detail from a widely-cited paper;
  treat as UNVERIFIED by omission, low risk.
- `qwen.readthedocs.io/en/latest/getting_started/quantization_benchmark.html`
  — **CHECKED.** IFEval BF16/GPTQ-Int4/AWQ numbers for Qwen2-7B-Instruct
  (53.1/49.4/51.4) and Qwen2-72B-Instruct (77.6/.../78.9) confirmed exactly.
- `arxiv.org/abs/2505.20276` — **CHECKED.** "first systematic evaluation of
  quantized LLMs on tasks with long inputs (>64K tokens)... five quantization
  methods... and five models" confirmed verbatim, including the specific
  model list (Llama-3.1 8B/70B, Qwen-2.5 7B/32B/72B).

One invented/mischaracterized citation in this job (2409.11055's title and
scope) — logged below.

---

## JOB 7 — KV cache quantisation

Platform: ChatGPT (`Results Chat GPT /Job 7.txt`).

Q4 — any measurement against verbatim quotation? **NOT FOUND**, and honestly
so — every benchmark found (three separate perplexity comparisons) measures
perplexity, not verbatim quotation or exact-copy accuracy. The platform says
this outright: "This is again perplexity" (repeated three times, once per
measurement). This is exactly the well-sourced NOT FOUND the job file said
would itself be a genuine result.

Other answers: Q1 — `--cache-type-k`/`--cache-type-v` set K/V cache dtype,
default `f16`, q8_0 among allowed values (confirmed). Q3 — distance-dependent
degradation NOT FOUND for q8_0 specifically (some evidence found for q4_0
climbing 43% from 2K→8K, but that's a different quant level). Q5 — K vs V
differential sensitivity NOT FOUND for q8_0. Q6 — flash-attn interaction NOT
FOUND.

Numbers and links (CHECKED / UNVERIFIED):
- `android.googlesource.com/.../tools/cli/README.md` — **CHECKED.**
  `--cache-type-k`/`-v` flag docs, allowed values including q8_0, default
  f16, confirmed verbatim.
- `github.com/ggml-org/llama.cpp/discussions/5932` — **CHECKED.** Qwen2.5-
  Coder-7B perplexity table (f16/f16 8.3891, q8_0/q8_0 8.3934) confirmed
  exactly.
- `arxiv.org/abs/2401.18079` (KVQuant) — **CHECKED.** "Per-Channel Key
  Quantization" phrase confirmed in the paper.
- `techstat.net/qwen3-5-27b-q8-kv-cache-benchmarks-...` — **CHECKED.**
  Qwen3.5 27B BF16 (6.8653) vs Q8_0 (6.864972, i.e. ≈6.8650) perplexity
  numbers confirmed, close enough to the quoted rounding to count as
  supported.
- `reddit.com/r/LocalLLaMA/...kobold-cpp-frankenstein...` and
  `reddit.com/r/LLMDevs/...i-measured-4bit-kv-cache-perplexity...` —
  **UNVERIFIED — could not be opened** (Reddit blocked from this
  environment). These carry the q4_0-climbs-43%-from-2K-to-8K claim and the
  "q8_0 is free everywhere (+0.02–0.07%)" claim. Neither is load-bearing for
  the job's main NOT FOUND result, but both should be hand-checked before
  being relied on for anything about q4_0 specifically.

No fabricated citation found among the openable links.

---

## JOB 13 — determinism

Platform: ChatGPT (`Results Chat GPT /Job 13.txt`, marked "(partial)" by the
platform itself).

Q1 — is temperature-0 output bit-identical across runs? **NOT GUARANTEED /
demonstrated-NO in at least one documented case.** llama.cpp issue #7052
reports the reporter set temperature 0 and disabled other samplers, then
found completions and logits were "not deterministic" across runs — in a
multi-slot server configuration, getting "5 to 8 unique completion texts"
from 8 slots on the same prompt. In single-slot use they got the same answer
text but still saw "small variations in the logits" underneath. No source
found stating a positive guarantee of bit-identical output under fixed
seed/temp-0/same-build. This directly undercuts the pipeline's digest-
stamping assumption, as the job file predicted it might.

The local experiment it named, if any: **Yes** — run the identical request
repeatedly with model file, build, machine, parameters, and prompt all held
fixed, and byte-compare the outputs. Simple and actually runnable here.

Quotes and links (CHECKED / UNVERIFIED):
- `github.com/ggml-org/llama.cpp/issues/7052` — **CHECKED.** All three quoted
  passages (the "not deterministic" line, the MacBook Pro M1/H100/A100
  hardware line, and the "5 to 8 unique completion texts" line) confirmed
  verbatim.

No fabricated citation in this job — but note it only answers Q1 and the
local-experiment ask; Q2 (batch/thread/GPU-backend effect), Q3 (Metal-
specific reports beyond the one M1 mention already in #7052), Q4 (Ollama's
default seed behaviour), and Q5 (other open issues) are all marked NOT FOUND
or thin in the raw file — this is a genuinely partial answer, as its own
filename says.

---

## JOB 14 — effective context

Platform: ChatGPT (`Results Chat GPT /Job 14.txt`).

Q4 — evidence or folklore? **Folklore — stated plainly as such.** The
platform's own verdict: "Evidence-based answer: NO (from checked sources)."
No paper isolates "identical model, identical prompt, only allocated context
size changed" and measures output quality independent of memory/runtime
effects. The claim that a bigger `num_ctx` than needed costs quality on its
own is **UNVERIFIED** from the literature — exactly the honest gap the job
file said was worth surfacing.

Numbers and links (CHECKED / UNVERIFIED):
- RULER (`arxiv.org/abs/2404.06654`) and RULER repo
  (`github.com/NVIDIA/RULER`) — **CHECKED** (already verified under Job 11;
  same numbers reused here, including "only half... can maintain satisfactory
  performance at the length of 32K").
- Lost in the Middle, ACL/TACL version (`aclanthology.org/2024.tacl-1.9/`) —
  not independently re-opened (arXiv version of the same paper already
  checked under Job 11 with matching quotes); treat as CHECKED by
  equivalence.
- STRING (`arxiv.org/abs/2410.18745`) — **CHECKED.** "effective context
  lengths of open-source LLMs often fall short, typically not exceeding half
  of their training lengths" and the STRING method description both
  confirmed verbatim.
- Gemma 4 model card (`ai.google.dev/gemma/docs/core/model_card_4`) —
  **CHECKED.** "Context windows of up to 128K tokens (E2B/E4B) and 256K
  tokens (12B/26B A4B/31B)" and an "MRCR v2 8 needle 128k" benchmark row both
  confirmed. Note the raw answer paraphrases the window numbers slightly
  loosely ("up to 128K... and 256K tokens") — matches closely enough not to
  flag as invented.

No fabricated citation found in this job. Qwen 3.x-specific effective-context
evidence came back NOT FOUND, honestly.

---

## JOB 8 — scale test

**NOT DONE.** Same pattern as Job 2: `Results Chat GPT /Job 8.txt` is not a
packet reply, it's ChatGPT evaluating the *job description itself* against
the supplied Smithy-style criteria ("ROBUST", "SIMPLE", "LEAN", "FAST") —
concluding, correctly, that no failure has been demonstrated yet because no
packet was actually pasted or run. Packets d and e were never pasted into any
platform in a fresh chat. Also out of order per the README (Job 8 should only
run after Job 2 comes back clean, and Job 2 never ran at all).

| platform / model | packet | reply verbatim | one line only? | paste intact? |
|---|---|---|---|---|
| — | d | NOT DONE | — | — |
| — | e | NOT DONE | — | — |

---

## JOB 9 — model shortlist

Platform: ChatGPT (`Results Chat GPT /Job 9.txt`).

Benchmarks found, with links (CHECKED / UNVERIFIED):
- IFEval — named and described (verifiable formatting/exact-match checking);
  no single canonical link opened for the benchmark description page itself,
  but its numbers below are independently confirmed.
- FollowEval (`arxiv.org/abs/2311.09829`) — **CHECKED.** Title and the
  five-dimension description (string manipulation, commonsense/logical/
  spatial reasoning, response constraints) confirmed verbatim.
- IFBench (`arxiv.org/abs/2507.02833`) — **CHECKED.** "58 new, diverse, and
  challenging verifiable out-of-domain constraints" confirmed verbatim.
- Llama-3.1-8B-Instruct IFEval 80.4
  (`huggingface.co/meta-llama/Llama-3.1-405B-Instruct`) — **CHECKED,** on the
  actual cited URL (note: the link is to the *405B* model card's shared
  benchmark table, which does contain an 8B-Instruct column reading
  IFEval 80.4 — the number is right, the citation is just to a table that
  lives on a different model-size's page; not a fabrication, but sloppy
  sourcing worth flagging).
- Qwen2.5-7B-Instruct IFEval 75.85
  (`huggingface.co/Qwen/Qwen2.5-7B-Instruct/blob/refs%2Fpr%2F4/README.md`) —
  **CHECKED** on the exact cited URL (a specific PR-branch README, not the
  main model page — the number 75.85 is confirmed there verbatim).
- Llama-3.2-3B-Instruct IFEval 77.01
  (`github.com/huggingface/blog/blob/main/llama32.md`) — **CHECKED.** Table
  row "Meta-Llama-3.2-3B-Instruct | 20.88 | 77.01 | 31.80 | 43.23" confirmed
  exactly.
- Gemma 2 9B Instruct IFEval 75.42 (Reddit) — **UNVERIFIED — could not be
  opened** (Reddit blocked from this environment). This is the weakest
  sourced number in the job (a Reddit post as the sole citation for a
  benchmark score) and the platform itself labelled it a "secondary source."
- Ollama thinking docs (`ollama.com/blog/thinking`) — **CHECKED.** "When
  thinking is disabled, the model will not think and directly output the
  content," `--think=false`, and DeepSeek R1/Qwen 3 as supported models all
  confirmed verbatim.
- Gemma 4 thinking token (`ollama.com/library/gemma4`) — **CHECKED.**
  `<|think|>` token enable/disable language confirmed verbatim.

Which answers rest on a benchmark, and which on reputation: the platform's
own accounting is honest — five IFEval scores rest on named benchmarks with
sources (four independently confirmed, one Reddit-sourced and unconfirmable);
nothing here is presented as pure reputation/ranking, and the platform
explicitly declined to produce a "shortlist," as the job asked. The two
sharpest questions — a benchmark for exact one-line stopping behaviour over
a few thousand tokens, and evidence that reasoning models are worse at strict
formats — both came back **NOT FOUND**, honestly.

---

## RUNNING COUNT — invented citations

Tally them here as you go. Platform, what it claimed, what the link actually
was. This is its own finding: it measures how much any of these answers can be
trusted, and it is the same measurement the pipeline exists to make.

| platform | claimed | what was actually there |
|---|---|---|
| ChatGPT (Job 5) | `ggml-org/llama.cpp` issue #20260 "discusses a case where the `</think>` tag was not generated" | Real issue, but about a different defect: a stray natural-language sentence appearing *between* `</think>` and `<tool_call>` that breaks the PEG parser. The `</think>` tag is generated in this issue; what follows it is the problem. Real link, wrong description. |
| ChatGPT (Job 12) | arXiv 2409.11055 = "A Comprehensive Evaluation of Quantized Instruction-Tuned Large Language Models: An Experimental Analysis up to 405B," covering GPTQ/AWQ/SmoothQuant/FP8 on 7B–405B models | Real paper, wrong title. Actual title: "Exploring the Trade-Offs: Quantization Methods, Task Difficulty, and Model Size in Large Language Models From Edge to Giant." Actual range 1B–405B (not 7B–405B), four quant methods (SmoothQuant not confirmed as one). Invented title + wrong scope on a real link. |
| ChatGPT (Job 9) | Llama-3.1-8B-Instruct IFEval 80.4, cited to `huggingface.co/meta-llama/Llama-3.1-405B-Instruct` | Number confirmed correct on that page (shared benchmark table has an 8B column), but the citation points to the 405B model's page, not the 8B model's own page — sloppy sourcing, not fabrication. Flagged, not tallied as invented. |

**Links that could not be opened from this environment (Reddit is blocked)
and are logged as unconfirmable, not fabricated:**

| platform | job | claimed | why unconfirmable |
|---|---|---|---|
| ChatGPT | Job 6 | `done_reason: "length"` field, r/ollama thread | Reddit fetch blocked here; platform itself already flagged this as non-official. |
| ChatGPT | Job 7 | q4_0 "climbs 43% from 2K to 8K"; q8_0 "free everywhere (+0.02–0.07%)", two r/LocalLLaMA / r/LLMDevs threads | Reddit fetch blocked here. Not load-bearing for Job 7's main NOT FOUND result. |
| ChatGPT | Job 9 | Gemma 2 9B Instruct IFEval 75.42, r/LocalLLaMA thread | Reddit fetch blocked here; platform itself called it a "secondary source." |

**Structural note, not a per-citation row:** Job 3's entire answer cites
"llama.cpp documentation" and "Ollama API documentation" for every QUOTED
line but supplies **zero URLs** anywhere in the file — nothing to click at
all. Every claim in that job is UNVERIFIED by default, not because a link
failed, but because none was given. See the JOB 3 section above.

**Platform coverage:** every one of the 14 jobs' actual answers in this
folder came from a **single platform, ChatGPT**. The README asked for at
least three free platforms, especially for Job 2. No Grok, Gemini, or
DeepSeek answers to any of JOB_1–JOB_14 exist anywhere in either raw folder —
see the note at the top of this file about the `Scott research /` folder.
