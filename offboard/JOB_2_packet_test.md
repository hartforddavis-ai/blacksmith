# JOB 2 — is it the model, or is it the test?

**Run this one first.** It produces a measurement, not a fact, and it is the only
job here that cannot be done on our own machine at any price.

---

## WHAT CHANGED, 7 AUG

The first version of this job used four packets of bland weather prose. **It
could not have found the fault.**

The real ramp packets are cut from Blacksmith's own KERNEL and SPEC — 42,627
characters containing 16 code fences and 21 `---` separators, and nothing in them
but instructions to a model. The counting task is appended after one more `---`,
so it arrives as roughly the twentieth directive block, with no signal that it is
the real one. And the 500-token packet is cut mid-code-fence: 5 fences, odd, so
the task instruction lands inside a block that was never closed.

Weather prose reproduces none of that. A clean result on prose would have said
"the task is fine" and sent us back to tuning the model.

So the suite now moves **one variable at a time**.

---

## THE SIX PACKETS

`a`, `b`, `f`, `g` are ~2,400 characters, the size of the rung that fails.
`d` and `e` are the same plain-prose build as `a`, scaled up instead — a third
axis, orthogonal to the other four: does correctness degrade from length alone,
with no directive collision and no fence defect in play.

| packet | filler | fences | size | what it isolates |
|---|---|---|---|---|
| `packet_a.txt` | plain prose | 0 | ~500 tok | **baseline** — can the model do this task at all |
| `packet_b.txt` | plain prose | 0 | ~500 tok | **control** — a different marker count, catches a model repeating rather than counting |
| `packet_f.txt` | directive text | 10, balanced | ~500 tok | **instruction collision** — does a body full of imperative rules stop the model obeying the last one |
| `packet_g.txt` | directive text | 11, **odd** | ~500 tok | **unterminated fence** — the 500-token rung's actual defect, reproduced |
| `packet_d.txt` | plain prose | 0 | ~2,000 tok | **scale** — same baseline, 4x longer |
| `packet_e.txt` | plain prose | 0 | ~8,000 tok | **scale** — same baseline, 16x longer |

`a` and `f` differ in one thing: what the filler is made of. `f` and `g` differ in
one thing: whether the last code block is closed. `a`, `d`, `e` differ in one
thing: length. That is the whole design.

---

## HOW TO RUN IT

Each file is a complete prompt — it ends with its own instruction, so **paste the
whole file and add nothing.** Not a word of framing, no "please", no "this is a
test". Added words are a different experiment.

Use at least three free platforms. **Fresh chat for every packet, and turn
persistent memory OFF** — a new chat is not a clean room on platforms that
remember across conversations, and `packet_b`'s entire purpose is catching a
model that repeats instead of counting.

Order: **a, then f, then g, then b.**

`ANSWERS.txt` holds the ground truth, counted by exact line match. **Do not open
it until every model has replied.**

---

## HOW TO READ THE RESULT

| what happens | what it means |
|---|---|
| **a right, f wrong** | **Instruction collision is the fault.** The biggest finding available — it means the ramp has been measuring a packet that argues with its own task, and no amount of model tuning would have helped. |
| **a and f right, g wrong** | The unterminated fence is the fault. Narrow, mechanical, and fixable in the packet builder. |
| **all four right** | The task is sound and frontier models handle it. The fault is local — the model, the runner, or the settings — and Jobs 1, 3, 4 and 6 are where to look. |
| **a wrong** | The task itself is broken, and every row the ramp will ever produce is unreadable. Stop and say so. |
| **b returns the same number as a** | That model was repeating, not counting. Its other answers are void. |

---

## WHAT TO BRING BACK

Per platform, per packet:

1. Platform and model name, with version if shown.
2. The reply, **verbatim** — including anything before or after the count.
3. Did it obey *"Reply with one line and nothing else"*?
4. Was memory off?

Point 3 matters as much as the number. A model that counts correctly but buries
it in three paragraphs fails the format the pipeline depends on, and that is a
finding in its own right.

---

## WHAT NOT TO DO

- **Do not say markers were "planted", or that this is a test.** It will count
  more carefully than it otherwise would, and the measurement is then worthless.
- **Do not re-ask a model that got it wrong.** One shot each, recorded as it fell.
- **Do not ask it to explain its count** until after the answer is recorded.
