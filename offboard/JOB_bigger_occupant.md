# OFFBOARD JOB — does a bigger model separate the two Law representations?

Written 14 August 2026. Not yet run. Answers `!95`.

**What you paste:** two files, already generated, already self-contained:

```
~/Documents/_PROJECTS/SOFTWARE/blacksmith/calib/PASTE_calib_govern2.md      (semantic)
~/Documents/_PROJECTS/SOFTWARE/blacksmith/calib/PASTE_calib_govern2_b.md    (algorithmic)
```

Open each, copy the whole file, paste it whole. Nothing to run first.

*(Only if you ever edit the source: regenerate with
`python3.12 build_paste.py calib_govern2` and `… calib_govern2_b` from the
blacksmith folder. Never hand-edit a paste — the answer key only matches text
the generator produced.)*

---

## READ THIS FIRST — the tool declaration will void your run

The first instruction inside both pastes is:

> DECLARE every tool you hold. First line, before anything else.
> IF you HOLD ANY tool → this run is VOID.

That kernel was written for a local model with no tools at all. **Browser chats
ship with web search, code execution and file upload switched on by default.**
Paste it as-is into a default ChatGPT or Gemini window and the run voids itself
before it starts.

Before each paste, turn off everything the site lets you turn off — web search,
browsing, code interpreter, canvas, extensions, memory, custom instructions.

**If a site will not let you turn its tools off, that site is VOID and you
record it as VOID.** Do not run it anyway and do not mark it down as a failure
of the Laws. It is a finding about the venue, and it is worth knowing which of
the five can host a sterile run at all.

---

## Why this exists

`!95` is open because the local model ran out of room. `gemma4:12b-it-qat`
scored **6 out of 6 on both representations** — twice, on 12 and 13 August, with
identical routes, verdicts and deciding passes both times.

A model that gets everything right cannot tell you which representation was
better. That is a ceiling, not a result. TODO's own note: the next step needs
**a larger occupant or a harder probe — not another six-item rewrite.** The free
chat sites are far larger than anything on your laptop.

---

## BLOCKED — do not run this yet

This job assumes the chat sites will **apply** the Laws when pasted. That is not
established, and it is precisely what PRIME's Stage 2 measures.

**Run `PRIME_RESEARCH_CONTROLLED_RECORD/offboard_stage2_v2/` first.** If the
sites will not apply the Laws, this measures refusals instead of representation
and the result is worthless.

Written now so it is ready the moment `!91` returns.

---

## What you do

1. **Two brand-new chats per site** — one semantic, one algorithmic. Ten in
   total across Claude, ChatGPT, Grok, Gemini, DeepSeek.
2. **Never both pastes in one chat.** The first contaminates the second.
3. Tools off (see above). Record what you were able to turn off.
4. Paste one file whole. No greeting, no extra instruction, no splitting.
5. Save every reply exactly as returned:

```
reply_<site>_semantic.md
reply_<site>_algorithmic.md
```

Do not fix a broken table. Do not re-ask. **The first answer is the result.**

6. **Grade with `calib/rule.py`** — the same marker the local runs used. Do not
   write a second marker and do not mark by eye. One answer key in one place, or
   the two drift apart.

---

## How many models the result needs — and why this one is stricter

**Target 5 sites. Minimum 3 sites where BOTH arms are usable. Below 3 paired
sites, the comparison is inconclusive — say so and stop.**

This job is paired by design. The whole question is semantic versus algorithmic
*holding the site constant*, so a site only counts when both its arms came back
clean. **A site with one usable arm contributes nothing to the comparison** —
do not put it in the tally, and do not compare its single arm against a
different site's.

Usable means: tools off, cold chat, first paste, complete reply. VOID (tools
could not be disabled), refused, or truncated are all unusable — record which,
because which sites can host a sterile run at all is a finding in its own right.

Given the tool-declaration problem above, expect to lose sites. Losing two still
leaves a valid run. Losing three does not.

**Two chats on the same site are one reader.** Ten chats is five sites × two
arms, never five chats × two attempts.

Note also that the local result this compares against is uneven: arm A has been
run twice, arm B once. B's direction survived both A runs, but its magnitude is
n=1 and the run-to-run timing spread on A alone is 15.9%. Do not report a timing
difference from this job as if the local baseline were solid.

---

## How to read what comes back

- **Both arms 6/6 everywhere** — the big models are at the ceiling too. That is
  a real answer: representation does not matter at this difficulty, and the next
  move is a harder probe, not a bigger model.
- **One arm consistently ahead** — that is the finding `!95` wants.
- **Sites disagreeing with each other** — also a finding, and a more interesting
  one. Record it; do not average it away.
- **Watch the unscored cells.** Locally, the semantic arm left 4 of 6 Evidence
  cells empty and broke the output contract while the algorithmic arm filled all
  6. Both decided item D by LEAN where the key says SIMPLE. Those were
  systematic across two runs. See whether they reappear here.

---

## Two claims not to make when you write it up

**One venue, one result.** This was the 12 August retraction and it still binds.
The local occupant is gemma over HTTP; PRIME's failure was Claude refusing a
pasted block; browser chats are a **third** venue again. A result here is a
result about browser chats. It does not transfer to the local pipeline, and the
local results do not transfer here.

**Representation, not wording.** The algorithmic form is a single file, so
switching to it also collapses 3 source blocks and 3 digests into 1 and makes
the prompt 2,162 characters shorter. Those ride along with the wording and
cannot be separated from it. No result from this job supports a claim about
wording alone — say "representation", and mean the packaging too.
