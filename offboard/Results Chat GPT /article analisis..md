I accessed the article. ([Jeremy Tian][1])

I will separate **what the article states** from **analysis against your supplied framework**.

## Evidence from article

Source:
Jeremy Tian, **“A Data-Driven Explanation: Why Do AI Agents Still Fail”**, published Aug 4, 2026. ([Jeremy Tian][1])

The article identifies four causes for AI agent underperformance:

1. **Variance / reliability**

   * It argues that multi-step agent workflows compound failure probability.
   * Example given:

     * 90% success per step:

       * 10 steps → 34% end-to-end success
       * 20 steps → 12%
       * 30 steps → 4.2%
         ([Jeremy Tian][1])
   * It distinguishes:

     * **pass@k** = whether the model can succeed at least once
     * **pass^k** = whether it succeeds consistently across repeated runs
       ([Jeremy Tian][1])

2. **Benchmark / dataset quality**

   * It argues evaluations can be misleading if datasets contain bad tasks, incorrect expectations, or poor evaluators.
   * It cites examples where benchmark tasks required repair. ([Jeremy Tian][1])

3. **Agent-specific errors**

   * The article states that agent mistakes have moved “up the stack” rather than disappeared. ([Jeremy Tian][1])

4. **Alignment**

   * The article introduces alignment as another factor affecting reliability. ([Jeremy Tian][1])

---

# Analysis against supplied criteria

## DEMONSTRATED

### Claim:

“AI agents fail because multi-step reliability decreases.”

**Status: DEMONSTRATED within the article's model only.**

Evidence:

* The article provides a mathematical model showing compounded probability loss. ([Jeremy Tian][1])

Limit:

* The model assumes independent step probabilities.
* The article itself notes real agents are more complex because errors can compound or recover. ([Jeremy Tian][1])

Therefore:

* Demonstrated: **the probability model**
* Not demonstrated from this article alone: **that every production agent behaves exactly this way**

---

### Claim:

“Agents are inconsistent across runs.”

**Status: DEMONSTRATED within cited benchmark examples.**

Evidence:

* Article discusses pass^k measurements and reports performance drops when requiring repeated success. ([Jeremy Tian][1])

---

### Claim:

“Benchmarks can mislead.”

**Status: DEMONSTRATED by cited examples in the article.**

Evidence:

* Article reports benchmark datasets requiring corrections. ([Jeremy Tian][1])

---

## TEST

### SIMPLE

Question:
Does the article add roles, steps, or duplicate controls?

**Result: UNKNOWN**

Reason:
The article analyses failures. It does not specify an implementation control architecture.

---

### ROBUST

Question:
Does it close a demonstrated failure directly?

**Result: UNKNOWN**

Reason:
The article identifies failure modes but does not propose or test a control boundary.

---

### LEAN

Question:
Is it the smallest alternative?

**Result: UNKNOWN**

No alternatives are evaluated.

---

### FAST

Question:
Does it decide or defer?

**Result: UNKNOWN**

The article is explanatory, not a decision procedure.

---

## GENERATOR CLAUSE

Applying only the supplied generator criteria:

### Drift

UNKNOWN.

The article is not presented as generator output.

### Confabulation

UNKNOWN.

No generated artifact is being evaluated.

### Elaboration

UNKNOWN.

No frozen task length requirement is supplied.

---

# Comparison with evidence-first principle

Observed:

The article's central problem is that **capability measurement ≠ reliable execution**.

That aligns with:

> A single successful run does not prove dependable behaviour.

Evidence:

* The article explicitly distinguishes best-case capability (pass@k) from repeatable reliability (pass^k). ([Jeremy Tian][1])

Inference:

This supports the general need to measure repeatability, but the article alone does **not** establish any specific architecture or control mechanism.

Status:
**SUPPORTED CONCEPT**

Not:
**PROVEN DESIGN REQUIREMENT**

---

## Unknowns

The article does not provide evidence for:

* whether independent verification solves these failures
* whether human gates improve reliability
* whether external execution boundaries prevent failure
* whether local models differ from hosted models
* whether quantisation affects these failures
* whether a particular architecture is optimal

All are **UNKNOWN from this source**.

[1]: https://jeremytian.substack.com/p/a-data-driven-explanation-why-do "A Data-Driven Explanation: Why Do AI Agents Still Fail"
