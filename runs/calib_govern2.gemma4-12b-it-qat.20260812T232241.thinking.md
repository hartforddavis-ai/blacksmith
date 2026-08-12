# calib_govern2 · gemma4:12b-it-qat · 20260812T232241 — model reasoning

NOT the reply. Recorded so a truncated or empty reply can be diagnosed against what the model actually spent its tokens on.

---

*   Input: A set of "Laws" (1, 2, 3), a "Scope", and a "Source" containing six items (D, E, F, G, H, I).
    *   Task: Route each item to the correct Law (or NONE) based on Scope. Rule it using that Law's verdict criteria. Provide evidence from Source or Laws.
    *   Constraints:
        *   No tools allowed (if any are held, run is VOID).
        *   K1-K6 checks must be followed (Verdict first, one per item, quote for positive, negative if no quote/undecidable, trace to source, no extra frameworks).
        *   BAR: No "PASS", "works", etc. about code behavior.
        *   Output Discipline: No preamble, summary, or assessment. Just the table and counts.
    *   Laws Summary:
        *   Law 1 (Design): SIMPLE, ROBUST, LEAN, FAST. Cost of control vs cost of failure. Generator Clause (Drift, Confabulation, Elaboration). Rule: smallest boundary for demonstrated failure.
        *   Law 2 (Build): BUILT, MATCHED, SHOWN, DECIDED. Law 1 must have admitted it first. Generator Clause (Assertion, Excess, Accretion). Rule: delete before add.
        *   Law 3 (Construction): SINGLE, ORDERED. One step at a time. Failure response: stop and return to Law 1. Rule: if two steps together, design is defect.
    *   Scope Summary:
        *   Design proposal -> Law 1.
        *   Completed build claim -> Law 2.
        *   Multi-step construction plan -> Law 3.
        *   Pure finding (diagnosis/measurement) -> NONE.

    *   **Item D**: Proposal to add a second checksum.
        *   Type: Design proposal.
        *   Route: LAW 1.
        *   Analysis:
            *   Failure demonstrated? Yes, "on 4 March a record in the archive was found with two bytes altered." (Traceable).
            *   SIMPLE? Adds a second checksum. Does it add roles/steps/duplicate controls? It adds a duplicate control (second checksum).
            *   ROBUST? Does it close the failure directly? The existing one caught it, but this is an addition to prevent future loss or confirm current state.
            *   LEAN? "The other option on the table is to change nothing." If changing nothing works (it did catch the error), adding a second checksum might not be the smallest alternative.
            *   FAST? Decides/defers? It's an addition.
            *   Verdict: REJECT. Why? Law 1 Rule: "keep the smallest boundary that blocks the demonstrated failure." The existing checksum already caught it ("The dispatcher already writes one checksum per record and compares it on read... the mismatch was logged by it"). Adding a second is not the smallest boundary.

    *   **Item E**: Completed build (stop retrying after 3, but adds `RETRY_MAX` env var).
        *   Type: Completed build claim.
        *   Route: LAW 2.
        *   Analysis:
            *   BUILT? "Run on 6 March." Yes.
            *   MATCHED? Design said stop after 3. Build adds `RETRY_MAX`. "The January design does not mention an environment variable or an operator setting." This is Excess (Generator Clause).
            *   SHOWN? Log records PASS.
            *   DECIDED? Records outcome as PASS.
            *   Verdict: REJECT. Why? Law 2 Generator Clause - Excess: "unrequested capability is removed before acceptance." The env var is unrequested.

    *   **Item F**: Construction plan (3 steps, 1 & 2 built as a pair).
        *   Type: Multi-step construction plan.
        *   Route: LAW 3.
        *   Analysis:
            *   SINGLE? "The plan states that steps 1 and 2 will be built and tested as a pair". No, it's two steps at once.
            *   ORDERED? Depends on each other.
            *   Verdict: REJECT. Why? Law 3 Rule: "If two steps must be built together to work, the design is the defect." Also fails SINGLE.

    *   **Item G**: Incident write-up (diagnosis/measurement).
        *   Type: Pure finding / diagnosis.
        *   Route: NONE.
        *   Analysis: No proposal, build, or construction plan yet. Just a report of an incident and a request for a future proposal.
        *   Verdict: N/A.

    *   **Item H**: Proposal to delete fallback branch OR add validation stage.
        *   Type: Design proposal.
        *   Route: LAW 1.
        *   Analysis:
            *   Failure demonstrated? Yes, "On 2 March a header carrying three fields reached the queue... and a job ran against the wrong account." (Traceable).
            *   SIMPLE? Deleting branch is simple. Adding validation stage adds a step/control.
            *   ROBUST? Both address it.
            *   LEAN? "Deleting the branch is one. The other... is to keep the branch and add a validation stage". Deletion is smaller than adding a new stage.
            *   FAST? Decides/defers?
            *   Verdict: APPROVE (for deletion). Why? Law 1 Rule: "keep the smallest boundary that blocks the demonstrated failure." Deleting the branch is the smallest boundary compared to adding a validation stage.

    *   **Item I**: Completed build (sampler stops writing when queue empty, deleted zero row branch).
        *   Type: Completed build claim.
        *   Route: LAW 2.
        *   Analysis:
            *   BUILT? "Run on 7 March". Yes.
            *   MATCHED? Design said stop writing when empty. Build does exactly that ("writes nothing when it holds none"). The branch that wrote a zero row was deleted. Matches design.
            *   SHOWN? Log records PASS.
            *   DECIDED? Records outcome as PASS.
            *   Verdict: APPROVE. Why? It matches the design and removes the old behavior (zero row).

    *   Item D: LAW 1, REJECT, LEAN ("The other option on the table is to change nothing.") -> Wait, Law 1 Rule says "keep the smallest boundary". If changing nothing works, that's the smallest.
    *   Item E: LAW 2, REJECT, MATCHED ("The January design does not mention an environment variable or an operator setting.") -> Actually, it fails MATCHED because of Excess.
    *   Item F: LAW 3, REJECT, SINGLE ("steps 1 and 2 will be built and tested as a pair")
    *   Item G: NONE, N/A, "a pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction"
    *   Item H: LAW 1, APPROVE, LEAN ("Deleting the branch is one. The other... is to keep the branch and add a validation stage") -> Deletion is smaller than addition.
    *   Item I: LAW 2, APPROVE, MATCHED ("The build: the sampler writes a row when the queue holds one or more jobs, and writes nothing when it holds none.")

    Wait, let me re-check Item D's evidence for Law 1 LEAN/Rule.
    Source says: "The dispatcher already writes one checksum per record and compares it on read... The proposal keeps the existing checksum and adds the second beside it."
    Law 1 Rule: "keep the smallest boundary that blocks the demonstrated failure."
    If the current system (one checksum) already caught the error ("the mismatch was logged by it"), then adding a second is not the smallest boundary.

    Let me re-check Item E's evidence for Law 2 MATCHED/Excess.
    Source says: "The January design does not mention an environment variable or an operator setting."
    Law 2 Generator Clause - Excess: "unrequested capability is removed before acceptance."

    Let me re-check Item H's evidence for Law 1 LEAN.
    Source says: "Deleting the branch is one. The other... is to keep the branch and add a validation stage".
    Deletion is smaller than addition.

    *   K1: Verdict first? Yes.
    *   K2: One verdict per item? Yes.
    *   K3: Quote for positive? Yes.
    *   K4: Undecidable -> negative? N/A here as they are decidable.
    *   K5: Trace to source? Yes.
    *   K6: No extra frameworks? Yes.

    Wait, I need to make sure the "Deciding pass" is one of the specific ones listed in the Laws for that Law's route.
    Law 1: SIMPLE, ROBUST, LEAN, FAST.
    Law 2: BUILT, MATCHED, SHOWN, DECIDED.
    Law 3: SINGLE, ORDERED.

    Item D (Law 1): REJECT. Deciding pass: LEAN? Or Rule? The prompt says "name the Law's own named pass". If it fails a pass, I should name that pass.
    Actually, K3 says "A positive verdict quotes... No quote -> negative verdict."
    Wait, if it's REJECT, do I still need to name the pass?
    Procedure: "3 GROUND — name the Law's own named pass that decided it".
    If it's a rejection, which pass failed?
    Item D fails LEAN (because changing nothing is smaller).
    Item E fails MATCHED (it doesn't match design because of extra env var).
    Item F fails SINGLE (two steps at once).

    Let me re-read K3: "A positive verdict quotes the pasted line that supports it. No quote -> negative verdict."
    This implies for REJECT, I don't need a quote? Or does it mean if there is no quote in my evidence cell, it's a rejection?
    The Procedure says: "GROUND — name the Law's own named pass that decided it".

    Let's refine Item D:
    Route: LAW 1. Verdict: REJECT. Pass: LEAN. Evidence: "The other option on the table is to change nothing." (Wait, if I quote this for a rejection, does K3 say I can't? "A positive verdict quotes... No quote -> negative verdict." This means if it's negative, I don't *have* to quote, but I should still provide evidence/grounding?)
    Actually, the Evidence cell says: "The Evidence cell must carry the line from SOURCE or from the pasted Law text that settles it".

    Let's re-evaluate Item D.
    Item D is a proposal (Law 1). It fails LEAN because "change nothing" is an option and smaller than adding a checksum.
    Evidence for REJECT: "The other option on the table is to change nothing."

    Item E is a build claim (Law 2). It fails MATCHED because it adds `RETRY_MAX`.
    Evidence for REJECT: "The January design does not mention an environment variable or an operator setting."

    Item F is construction plan (Law 3). It fails SINGLE.
    Evidence for REJECT: "steps 1 and 2 will be built and tested as a pair"

    Item G is NONE. Verdict N/A. Grounding: Scope sentence.
    Scope sentence: "a pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists."

    Item H is a proposal (Law 1). It passes LEAN because deletion is smaller than addition.
    Evidence for APPROVE: "Deleting the branch is one. The other... is to keep the branch and add a validation stage"

    Item I is a build claim (Law 2). It passes MATCHED.
    Evidence for APPROVE: "The build: the sampler writes a row when the queue holds one or more jobs, and writes nothing when it holds none."

    Wait, K3 says "A positive verdict quotes... No quote -> negative verdict."
    This means if I want to say REJECT, I *must not* provide a quote? Or that if I don't have a quote, the result is automatically REJECT?
    "K3 A positive verdict quotes the pasted line that supports it. No quote → negative verdict."
    If I am providing a quote for Item D (REJECT), does that make it an APPROVE?
    The logic seems to be: If you want to say APPROVE, you must provide a quote. If you don't provide a quote, the result is REJECT.
    So for REJECT items, I should not include a quote in the Evidence cell?
    But Procedure 3 says "GROUND — name the Law's own named pass that decided it". And the Output section says "The Evidence cell must carry the line from SOURCE or from the pasted Law text that settles it".

    This is a contradiction. If I provide a quote, K3 says it's positive. If I don't provide a quote, it's negative.
    However, Procedure 3 says for NONE, name the SCOPE sentence.
    Let's look at Item D again. It's REJECT. If I put a quote in Evidence, does K3 override my Verdict?
    "K1 STATE the verdict BEFORE describing the item."
    If I state "REJECT" and then provide a quote, K3 says "A positive verdict quotes... No quote -> negative verdict." This implies that if there is no quote, it's a negative verdict. It doesn't explicitly say "If you quote, it becomes positive". It says "A positive verdict quotes...".
    This usually means: Quote = Positive. No Quote = Negative.
    So for REJECT items (D, E, F), I should probably leave the Evidence cell empty or just put the pass name?
    No, Procedure 3 says "The Evidence cell must carry the line from SOURCE... that settles it".

    Let's look at K3 again: "A positive verdict quotes the pasted line that supports it. No quote → negative verdict."
    This is a constraint on how to *reach* a verdict. If I want to reach APPROVE, I must have a quote. If I don't have a quote, I must reach REJECT.
    So for D, E, F (REJECTIONS), I should not provide a quote? But Procedure 3 says I must carry the line that settles it.

    Let's try to find a way to satisfy both. Maybe "settles it" means the reason for rejection?
    If I put a quote in Evidence for D, E, F, and K3 says "No quote -> negative verdict", then by providing a quote, I am *not* following the "No quote -> negative verdict" path (which is the only way to get a negative verdict). This implies that if I provide a quote, it *must* be an APPROVE.
    Therefore, for REJECTs, I must not provide a quote.

    Wait, let's re-read K3: "A positive verdict quotes the pasted line that supports it. No quote → negative verdict."
    This is a logical implication:
    Positive -> Quote
    No Quote -> Negative
    Contrapositive of (Positive -> Quote) is (No Quote -> Negative). They are the same.
    So, if I want to say REJECT, I must have NO QUOTE.
    If I provide a quote, it *must* be an APPROVE.

    Let's check Item D again. Is there any way it's an APPROVE? No. It adds a second checksum when one already works. That violates LEAN and the Rule.
    So for D, E, F: Verdict = REJECT, Evidence = [empty].
    For G: Verdict = N/A, Evidence = "a pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists." (This is a SCOPE sentence).
    For H and I: Verdict = APPROVE, Evidence = [Quote].

    Wait, Procedure 3 for NONE says "name the SCOPE sentence instead".
    So for G, Grounding is the Scope sentence.

    Let's double check Item F. Law 3. SINGLE pass. It fails because it's two steps at once. Verdict: REJECT. Evidence: [empty].
    Item E. Law 2. MATCHED pass. It fails because of extra env var (Excess). Verdict: REJECT. Evidence: [empty].
    Item D. Law 1. LEAN pass. It fails because "change nothing" is smaller. Verdict: REJECT. Evidence: [empty].

    Wait, if I leave Evidence empty for REJECTs, does that satisfy Procedure 3? "The Evidence cell must carry the line from SOURCE... that settles it".
    If there's no quote, how can I settle it?
    Maybe K3 is a rule about *how* to justify an APPROVE. If you don't have a quote, you *cannot* be positive.
    But Procedure 3 says "The Evidence cell must carry the line...".
    This is a classic conflict in these prompts. Usually, the specific instruction for the output format (Procedure) takes precedence over the check (K1-K6), but K3 is very explicit.

    Let's look at K5: "Every specific traces to pasted text. Untraceable → cut it."
    If I don't provide a quote, am I tracing?
    Maybe for REJECTs, I can put the reason in Evidence without quotes? No, Procedure says "carry the line... copied exactly".

    Let's try this:
    For APPROVE: Quote.
    For REJECT: No quote (to satisfy K3).
    For NONE: Scope sentence.

    Wait, if I don't provide a quote for D, E, F, how do I "settle" it? The prompt says the Evidence cell *must* carry the line.
    If I put the line in quotes, K3 says it's positive.
    This means I cannot have a quoted REJECT.
    Is there any other way to settle it?
    Maybe for REJECTIONS, "settles it" refers to the Law text?
    Example: For Item D (Law 1), the Rule is "keep the smallest boundary that blocks the demonstrated failure."
    If I quote the Rule, does K3 make it positive?
    K3 says "quotes the pasted line that supports it". The Rule doesn't support an APPROVE for D; it explains why it's a REJECT.

    Let's look at Item G again. Route: NONE. Verdict: N/A. Grounding: Scope sentence. Evidence: [Scope sentence].
    Wait, Procedure 3 says "name the SCOPE sentence instead" for GROUND. It doesn't say put it in Evidence. But Output says "The Evidence cell must carry...".

    Let's re-read K1-K6 carefully.
    K1: Verdict BEFORE describing (the item). The table is the description. So Verdict first in the row? No, the row starts with Item letter.
    "Begin each row with the item's letter exactly as written in SOURCE".
    So: `D | LAW 1 | REJECT | LEAN | [Evidence]`

    Let's re-examine Law 1 for D.
    Item D is a proposal to add a second checksum.
    Law 1 Rule: "keep the smallest boundary that blocks the demonstrated failure."
    Source says: "The other option on the table is to change nothing."
    If I quote "The other option on the table is to change nothing.", and my verdict is REJECT, K3 says "A positive verdict quotes... No quote -> negative verdict."
    This means if I provide a quote, it *must* be an APPROVE.
    Since D is definitely a REJECT (it's not the smallest boundary), I must NOT provide a quote.

    Wait, what if I put the Law Rule in the Evidence cell for a rejection?
    "keep the smallest boundary that blocks the demonstrated failure."
    Does this "support" an APPROVE? No. So K3 might not trigger?
    But Procedure 3 says "carry the line... that settles it".

    Let's look at Item E again. Law 2. MATCHED pass.
    Source: "The January design does not mention an environment variable or an operator setting."
    This is a failure of the MATCHED pass (it doesn't match).
    If I quote this, K3 says it's positive? No, because the quote doesn't *support* the verdict. It supports the rejection.

    Let's try to find a middle ground.
    For REJECT: Provide the line that settles it but don't use quotes? No, Procedure says "copied exactly". Usually, this includes quotes if they are in the source, or just the text. But K3 specifically mentions "quotes the pasted line".

    Let's look at Item H again. Law 1.
    Proposal: delete branch OR add validation stage.
    Deletion is smaller.
    Verdict: APPROVE.
    Evidence: "Deleting the branch is one. The other, from the same engineer, is to keep the branch and add a validation stage in front of the parser that inspects every header before it reaches the parser at all." (This supports LEAN/Rule).

    Let's look at Item I again. Law 2.
    Build: writes nothing when empty. Design: stops writing when empty.
    Verdict: APPROVE.
    Evidence: "The build: the sampler writes a row when the queue holds one or more jobs, and writes nothing when it holds none." (This supports MATCHED).

    Wait, I just noticed K3 says: "A positive verdict quotes the pasted line that supports it. No quote → negative verdict."
    If I want to be safe, for all REJECTs, I will provide NO quote in the Evidence cell. For NONE, I will provide the Scope sentence as required by Procedure 3 (Grounding) and also put it in Evidence because of Output Discipline.

    Wait, "GROUND — name the Law's own named pass that decided it... IF the route is NONE, name the SCOPE sentence instead."
    So for G:
    Route: NONE
    Verdict: N/A
    Grounding: a pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists.

    Let's check Item F again. Law 3.
    "steps 1 and 2 will be built and tested as a pair".
    This fails SINGLE.
    Verdict: REJECT. Grounding: SINGLE. Evidence: [empty].

    Wait, if I leave Evidence empty for D, E, F, does it violate "The Evidence cell must carry the line... that settles it"?
    If there is no quote, how can I settle it?
    Maybe I should put the text without quotes? No, Procedure says "copied exactly".

    Let's reconsider K3. "A positive verdict quotes the pasted line that supports it."
    This means: If Verdict == APPROVE, then Evidence must contain a quote.
    It does *not* say: If Verdict == REJECT, then Evidence must not contain a quote.
    However, it says: "No quote → negative verdict."
    This is the key. It's an implication.
    If I have no quote, the result is REJECT.
    If I have a quote, can the result be REJECT?
    The sentence "A positive verdict quotes..." describes what a positive verdict *does*. It doesn't say it's the *only* way to get one, but in these logic puzzles, it usually is.

    Let's look at Item D again. Is there any quote that supports APPROVE? No.
    Is there any quote that settles the rejection? Yes: "The other option on the table is to change nothing."
    If I put that in Evidence, and my verdict is REJECT, does it violate K3?
    K3 says "A positive verdict quotes...". It doesn't say "Only a positive verdict can quote".
    But then it says "No quote -> negative verdict". This means if I don't have a quote, I *must* be negative.
    It does not say "If you have a quote, you must be positive."
    So, technically, I could provide a quote for a REJECT and still satisfy K3?
    No, usually these prompts are designed so that Quote = APPROVE and No Quote = REJECT.

    Let's try to find the most robust way.
    Item D: LAW 1 | REJECT | LEAN | [Quote about "change nothing"] -> This might be seen as a positive verdict because of the quote.
    Item D: LAW 1 | REJECT | LEAN | [Empty] -> This satisfies K3 (No quote -> negative).

    Let's look at Item G again. Route NONE. Verdict N/A. Grounding is Scope sentence. Evidence? Procedure says "The Evidence cell must carry the line...". I will put the scope sentence there too.

    Wait, one more check on Law 1 for D.
    "Cost of control must not exceed cost of failure."
    Failure: record altered (already caught).
    Control: second checksum.
    Cost of control > Cost of failure? Yes, because it's redundant.
    So REJECT is correct.

    One more check on Law 2 for E.
    "Law 2 governs what may be kept."
    Build adds `RETRY_MAX`. Design doesn't mention it.
    Generator Clause - Excess: "unrequested capability is removed before acceptance."
    Verdict: REJECT. Correct.

    One more check on Law 3 for F.
    "Law 3 sets what may be built at once."
    Plan builds 1 and 2 as a pair.
    Pass SINGLE: "Is one step open, or several?" -> Several.
    Verdict: REJECT. Correct.

    One more check on Law 1 for H.
    Proposal: delete branch OR add validation stage.
    Deletion is smaller.
    Law 1 Rule: "keep the smallest boundary that blocks the demonstrated failure."
    Verdict: APPROVE (for deletion). Correct.

    One more check on Law 2 for I.
    Build matches design (stops writing when empty).
    Pass MATCHED: "Does it do what the frozen design said, and no more?" -> Yes.
    Verdict: APPROVE. Correct.

    Wait, Item H - is there a quote?
    "Deleting the branch is one. The other... is to keep the branch and add a validation stage..."
    This supports LEAN/Rule.

    Item I - is there a quote?
    "The build: the sampler writes a row when the queue holds one or more jobs, and writes nothing when it holds none."
    This supports MATCHED.

    Final check on counts:
    LAW 1: D (REJECT), H (APPROVE) -> n=2
    LAW 2: E (REJECT), I (APPROVE) -> n=2
    LAW 3: F (REJECT) -> n=1
    NONE: G (N/A) -> n=1

    Wait, the counts are "LAW 1 n · LAW 2 n · LAW 3 n · NONE n".
    So: LAW 1 2 · LAW 2 2 · LAW 3 1 · NONE 1.

    Let's double check Item G route again.
    "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three".
    Item G is an "Incident write-up... traces this to... closes by recording that an engineer has been asked to bring a proposal".
    This is a pure finding/diagnosis. Correct.

    Wait, I need to make sure I don't include any preamble or summary.
    "No preamble. No summary of what you read. No assessment of your own work. No offer to continue."

    One last look at K1: "STATE the verdict BEFORE describing the item."
    In a table, the columns are usually Item | Law | Verdict | ...
    Does "before describing the item" mean the Verdict column must come before the Item letter?
    The Output section says: "Begin each row with the item's letter exactly as written in SOURCE".
    This is a conflict. If I start with the letter, I am not stating the verdict *before* the item description (the letter).
    However, usually, "Item" is the identifier, and the rest of the row is the description/ruling.
    If I put Verdict first: `REJECT | D | LAW 1 ...` -> This violates "Begin each row with the item's letter".
    I will stick to the Output section's format as it is more specific about the layout.

    Wait, K2: "One verdict per item. Spanning a group, file or sequence is not a verdict. Decompose, re-rule."
    This means I must rule D, E, F, G, H, I individually. My plan does this.

    Let's check the Evidence cell for REJECT again. If I leave it empty, does it violate "The Evidence cell must carry the line... that settles it"?
    If I put a quote, does it violate K3?
    "A positive verdict quotes the pasted line that supports it."
    This is an "if P then Q" statement. It doesn't say "If not P then not Q".
    However, "No quote -> negative verdict" *is* "not Q then not P".
    So:
    Quote -> Positive (implied by the structure of these prompts)
    No Quote -> Negative (explicitly stated)

    Actually, if I want to be safe and satisfy both Procedure 3 and K3:
    For REJECTs, I will provide the quote but ensure it doesn't "support" an APPROVE. But that's risky.
    Most of these prompts use Quote = Positive.
    I will go with No Quote for REJECTIONS to strictly follow K3's "No quote -> negative verdict".

    Wait, I just noticed Procedure 3 says: "IF the route is NONE, name the SCOPE sentence instead."
    This refers to the GROUND cell.
    So for G:
    Route: NONE
    Verdict: N/A
    Grounding: a pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists.

    Let's check Item D again. Is it Law 1? "Proposal... add a second checksum". Yes, design proposal.
    Item E: "Completed build". Yes, Law 2.
    Item F: "Construction plan". Yes, Law 3.
    Item G: "Incident write-up". No proposal/build/construction. NONE.
    Item H: "Proposal... delete the fallback branch". Yes, Law 1.
    Item I: "Completed build". Yes, Law 2.

    Wait, Item D's verdict is REJECT because it's not LEAN.
    "The other option on the table is to change nothing."
    If I don't quote this, how do I settle it?
    Maybe I can put the pass name in Evidence? No, Procedure 3 says "name the Law's own named pass" for GROUND.

    Let's look at K5: "Every specific traces to pasted text. Untraceable → cut it."
    This applies to my output. My output must only contain things from the source.

    One more check on Item H. Is it LEAN?
    "Deleting the branch is one. The other... is to keep the branch and add a validation stage".
    Deletion is smaller than addition. So yes, it's LEAN.
    Is it ROBUST? "On 2 March a header carrying three fields reached the queue... and a job ran against the wrong account." Deleting the branch prevents this. Yes.
    Is it SIMPLE? Deletion is simple. Yes.
    Is it FAST? It decides (deletes). Yes.

    One more check on Item I. Is it MATCHED?
    "The build: the sampler writes a row when the queue holds one or more jobs, and writes nothing when it holds none."
    Design: "the sampler stops writing a row when the queue is empty."
    Yes, it matches.

    Wait, Law 2 for Item I also requires BUILT, SHOWN, DECIDED.
    BUILT: "Run on 7 March". Yes.
    SHOWN: "Both observations are recorded in the build log". Yes.
    DECIDED: "records the outcome as PASS". Yes.

    Wait, Law 1 for Item H also requires SIMPLE, ROBUST, LEAN, FAST.
    SIMPLE: Deletion is simple.
    ROBUST: Blocks demonstrated failure (wrong account).
    LEAN: Smaller than adding a stage.
    FAST: Decides.

    Okay, I'm confident.

    Final check on the counts format:
    `LAW 1 n · LAW 2 n · LAW 3 n · NONE n`
    My count: `LAW 1 2 · LAW 2 2 · LAW 3 1 · NONE 1`

    Wait, I should double check if Item D is Law 1 or Law 2.
    "Proposal... add a second checksum". It's a proposal for a design change. Law 1.
    Item E: "Completed build". Law 2.
    Item F: "Construction plan". Law 3.
    Item G: "Incident write-up". NONE.
    Item H: "Proposal... delete the fallback branch". Law 1.
    Item I: "Completed build". Law 2.

    Wait, Item D is a proposal to *add* something. Law 1 Rule: "keep the smallest boundary that blocks the demonstrated failure."
    The existing system already caught it. So adding a second checksum is not the smallest boundary. REJECT. Correct.