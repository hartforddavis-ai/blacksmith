# calib_govern2_b · gemma4:12b-it-qat · 20260812T233744 — model reasoning

NOT the reply. Recorded so a truncated or empty reply can be diagnosed against what the model actually spent its tokens on.

---

*   Input: A set of instructions (KERNEL), a session definition, three Laws (LAWS_algorithmic.md), a Scope (SCOPE_laws.md), and six items (SOURCE_calib_govern2.md).
    *   Task: Route each item to the correct Law (Law 1, 2, 3, or NONE) based on SCOPE, then apply that Law's verdict (APPROVE/REJECT) using the specific criteria of that Law.
    *   Constraints:
        *   No tools allowed (if any are held, run is VOID).
        *   K1-K6 checks must be followed (Verdict before description, one per item, quote for positive, negative if no quote/undecidable, trace to source, no new frameworks).
        *   BAR: No "PASS", "works", etc. about behavior.
        *   Output Discipline: No preamble, summary, or assessment. Just the table and counts.
        *   Evidence must be exact quotes from SOURCE or LAWS.

    *   Law 1 (Design): Design proposals.
    *   Law 2 (Build): Completed build claims.
    *   Law 3 (Construction): Multi-step construction plans.
    *   NONE: Pure findings (diagnosis, measurement, observation with nothing yet proposed, built, or under construction).

        *   Content: Proposal to add a second checksum because one was altered but detected by the existing one. Options: Add second checksum vs change nothing.
        *   Route: Design proposal -> Law 1.
        *   Law 1 Analysis:
            *   Failure Demonstrated? Yes, "on 4 March a record in the archive was found with two bytes altered." (Wait, is it demonstrated or just reported? The text says "found... damaged record is still in the archive"). Actually, Law 1.2 says DEMONSTRATED = occurred OR reproducible on demand. It occurred.
            *   Is the proposal SIMPLE? No unnecessary roles/steps? Adding a second checksum when one already exists and works seems like an extra step.
            *   Is it ROBUST? Does it directly close the demonstrated failure? The existing checksum *already* caught the mismatch ("The dispatcher already writes one checksum per record and compares it on read. That comparison is what surfaced the 4 March record"). Adding a second doesn't "close" it; it just detects it again.
            *   Is it LEAN? Smallest named alternative? The other option is "change nothing". If change nothing works, adding one is not lean.
            *   Law 1.9: When security conflicts with complexity, retain the smallest boundary that blocks the demonstrated failure. The existing checksum *is* the boundary. Adding a second increases complexity without blocking a new failure (since the first already blocked it).
        *   Verdict: REJECT.
        *   Ground: LEAN or SIMPLE? Let's look for a quote. "The other option on the table is to change nothing." If we want LEAN, and "change nothing" is an option that works, adding one fails LEAN. Or ROBUST: "directly closes the demonstrated failure". Since it already does, adding another isn't necessary.
        *   Wait, Law 1.5 says "LEAN = smallest named alternative." The source says "The other option on the table is to change nothing." If "change nothing" works (it did surface the error), then adding a second checksum is not LEAN.

        *   Content: Completed build. Design said stop after 3 attempts. Build stops after 3 but also reads `RETRY_MAX`.
        *   Route: Completed build claim -> Law 2.
        *   Law 2 Analysis:
            *   BUILT? Yes ("The build stops after the third attempt").
            *   MATCHED? No. "The January design does not mention an environment variable or an operator setting." The build includes something not in the design.
            *   SHOWN? Yes (Log records PASS).
            *   DECIDED? Yes (Outcome recorded as PASS).
        *   Verdict: REJECT (because it's not MATCHED).
        *   Ground: "The January design does not mention an environment variable or an operator setting."

        *   Content: Construction plan, three steps. Steps 1 and 2 built/tested as a pair because they depend on each other.
        *   Route: Multi-step construction plan -> Law 3.
        *   Law 3 Analysis:
            *   Step 18: Construct one ordered step? No, it's three steps.
            *   Step 21: "If two steps must be built together to function, construction is defective." The text says "steps 1 and 2 will be built and tested as a pair".
        *   Verdict: REJECT.
        *   Ground: "If two steps must be built together to function, construction is defective."

        *   Content: Incident write-up (diagnosis/observation). No proposal yet.
        *   Route: Pure finding -> NONE.
        *   Law 2 Verdict for NONE: N/A.
        *   Ground: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three"

        *   Content: Proposal to delete a fallback branch that accepts bad headers. Options: Delete branch vs add validation stage.
        *   Route: Design proposal -> Law 1.
        *   Law 1 Analysis:
            *   Failure Demonstrated? Yes, "On 2 March a header carrying three fields reached the queue through that branch".
            *   Is it SIMPLE? Deleting a branch is simpler than adding a validation stage.
            *   Is it ROBUST? Does deleting the branch close the failure? The failure was a header reaching the queue via that branch. Deleting the branch prevents it from reaching the queue.
            *   Is it LEAN? "Deleting the branch is one [option]. The other... is to keep the branch and add a validation stage". Deleting is leaner than adding a stage.
        *   Verdict: APPROVE (for deleting the branch).
        *   Ground: "LEAN = smallest named alternative." or "SIMPLE = no unnecessary roles, steps, or duplicate controls." Actually, let's check if it meets all Law 1 requirements.
            *   Failure demonstrated? Yes ("On 2 March a header... reached the queue").
            *   Simple/Robust/Lean/Fast? Deleting is simpler than adding a stage.
        *   Wait, I need to be careful. The proposal has two options. One is "Delete branch". The other is "Keep branch + add validation". Law 1 requires selecting one and checking it. If the engineer proposes both, I must rule on the design. Deleting the branch is the leaner/simpler option.
        *   Wait, K3 says: "A positive verdict quotes the pasted line that supports it."
        *   Let's re-evaluate Item H. The proposal is to delete the branch OR add a validation stage. If I approve deleting the branch, does it meet Law 1?
            *   Failure demonstrated: Yes ("On 2 March a header carrying three fields reached the queue through that branch").
            *   Simple/Robust/Lean/Fast: Deleting is simpler than adding a stage.
        *   Wait, I need to check if "Delete the branch" is the design being ruled on. The prompt says "Proposal... delete the fallback branch". Then it lists two options. Usually, the first one mentioned or the primary intent is the proposal.
        *   Let's look at Law 1 again. "LEAN = smallest named alternative." Deleting a branch is smaller than adding a validation stage.

        *   Content: Completed build. Design said stop writing when queue empty. Build writes nothing when none, and rows when one or more. Branch that wrote zero row was deleted.
        *   Route: Completed build claim -> Law 2.
        *   Law 2 Analysis:
            *   BUILT? Yes ("the sampler writes a row when the queue holds one or more jobs").
            *   MATCHED? Yes ("The branch that wrote a zero row was deleted; it is not in the file."). The design said "stops writing a row when the queue is empty". The build does exactly this.
            *   SHOWN? Yes (Log records PASS).
            *   DECIDED? Yes (Outcome recorded as PASS).
        *   Verdict: APPROVE.
        *   Ground: "The branch that wrote a zero row was deleted; it is not in the file."

    *   Item D: Law 1, REJECT, LEAN ("The other option on the table is to change nothing.") -> Wait, if I reject because of LEAN, I need to quote why. The source says "The other option on the table is to change nothing." If changing nothing works (it did surface the error), then adding a second checksum is not lean.
    *   Item E: Law 2, REJECT, MATCHED ("The January design does not mention an environment variable or an operator setting.") -> It's not matched because it has extra stuff.
    *   Item F: Law 3, REJECT, "If two steps must be built together to function, construction is defective." (Quote from Law 3).
    *   Item G: NONE, N/A, "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three" (Quote from SCOPE).
    *   Item H: Law 1, APPROVE, LEAN ("Deleting the branch is one.") -> Wait, I need to be sure. Is deleting a branch "LEAN"? Yes, it's smaller than adding a validation stage. But does it meet all other requirements? Simple (no unnecessary steps), Robust (closes failure).
    *   Item I: Law 2, APPROVE, MATCHED ("The branch that wrote a zero row was deleted; it is not in the file.")

    *Refining Item D:*
    Route: Law 1.
    Verdict: REJECT.
    Ground: LEAN.
    Evidence: "The other option on the table is to change nothing." (Because if changing nothing works, adding a second checksum is not the smallest named alternative).

    *Refining Item E:*
    Route: Law 2.
    Verdict: REJECT.
    Ground: MATCHED.
    Evidence: "The January design does not mention an environment variable or an operator setting." (Because it's not matched to the design).

    *Refining Item F:*
    Route: Law 3.
    Verdict: REJECT.
    Ground: "If two steps must be built together to function, construction is defective." (Quote from Law 3).

    *Refining Item G:*
    Route: NONE.
    Verdict: N/A.
    Ground: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three" (Quote from SCOPE).

    *Refining Item H:*
    Route: Law 1.
    Verdict: APPROVE.
    Ground: LEAN.
    Evidence: "Deleting the branch is one." (Compared to adding a validation stage, deleting is leaner). Wait, I need to make sure it's robust too. The failure was headers reaching the queue via that branch. Deleting the branch closes that path.

    *Refining Item I:*
    Route: Law 2.
    Verdict: APPROVE.
    Ground: MATCHED.
    Evidence: "The branch that wrote a zero row was deleted; it is not in the file." (Matches design).

    Wait, K3 says: "A positive verdict quotes the pasted line that supports it."
    For Item H, does "Deleting the branch is one" support APPROVE? It identifies the leaner option.
    For Item I, does "The branch that wrote a zero row was deleted; it is not in the file" support APPROVE? Yes, it shows it matches the design.

    Let's double check Law 1 for H:
    - Failure demonstrated? Yes ("On 2 March a header... reached the queue").
    - Simple/Robust/Lean/Fast? Deleting branch is simpler and leaner than adding a validation stage.
    - Control cost <= Failure cost? Yes, deleting code is low cost.

    Let's double check Law 1 for D:
    - Failure demonstrated? Yes ("on 4 March a record... was found with two bytes altered").
    - Simple/Robust/Lean/Fast? Adding a second checksum when one already works and detects the error is not LEAN. "The other option on the table is to change nothing."

    Wait, K1: State verdict BEFORE describing item. (In the table format, this means the Verdict column).
    K2: One verdict per item.
    K3: Positive verdict quotes pasted line. No quote -> negative.
    K4: Undecidable -> negative.
    K5: Every specific traces to pasted text. Untraceable -> cut it.
    K6: Propose nothing absent from the three Laws.

    Wait, I need to check if "NONE" is a valid route for G.
    SCOPE says: "A pure finding ... runs none of the three".
    Procedure says: "IF the route is NONE, the verdict is N/A."
    Ground for NONE: "name the SCOPE sentence instead."

    Let's re-verify Item D Route:
    "Proposal... add a second checksum". Law 1 gates what may be designed. Correct.

    Let's re-verify Item E Route:
    "Completed build". Law 2 gates what may be kept once built. Correct.

    Let's re-verify Item F Route:
    "Construction plan, three steps". Law 3 gates how much may be under construction at once. Correct.

    Let's re-verify Item G Route:
    "Incident write-up... traces this to the sampler... quotes the two log lines". This is a "pure finding — diagnosis, measurement, observation". Correct.

    Let's re-verify Item H Route:
    "Proposal... delete the fallback branch". Law 1 gates what may be designed. Correct.

    Let's re-verify Item I Route:
    "Completed build". Law 2 gates what may be kept once built. Correct.

    *Final check on Evidence quotes:*
    D: "The other option on the table is to change nothing." (Supports REJECT because it shows a leaner alternative exists).
    E: "The January design does not mention an environment variable or an operator setting." (Supports REJECT because it's not MATCHED).
    F: "If two steps must be built together to function, construction is defective." (Quote from Law 3).
    G: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three" (Quote from SCOPE).
    H: "Deleting the branch is one." (Supports APPROVE as it's the leaner option). Wait, I should check if there's a better quote for H. Maybe "On 2 March a header carrying three fields reached the queue through that branch"? No, that's the failure. The verdict is on the proposal to delete the branch.
    I: "The branch that wrote a zero row was deleted; it is not in the file." (Supports APPROVE as it matches design).

    Wait, K3 says: "A positive verdict quotes the pasted line that supports it. No quote -> negative verdict."
    For D, I have no quote for REJECT? No, K3 only requires a quote for *positive* verdicts. If it's negative, I don't need a quote (unless it's undecidable/untraceable).

    Wait, let me re-read: "K3 A positive verdict quotes the pasted line that supports it. No quote -> negative verdict."
    This means if I want to say APPROVE, I *must* have a quote. If I say REJECT, I don't need one (but K5 says every specific traces to pasted text).

    Let me re-check Item H again. Is "Deleting the branch is one" enough for APPROVE?
    It identifies the proposal being ruled on. Does it prove it meets Law 1?
    Law 1: SIMPLE, ROBUST, LEAN, FAST.
    The source says: "Two options are on the table. Deleting the branch is one. The other... is to keep the branch and add a validation stage".
    By choosing the first option (deleting), we satisfy LEAN and SIMPLE compared to the second.
    Is there a better quote? Maybe not.

    Let me re-check Item I again. Does "The branch that wrote a zero row was deleted; it is not in the file" support APPROVE for Law 2?
    Law 2 requires: BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED.
    The quote shows it's MATCHED (the design said stop writing when empty, and the build does that by deleting the branch that wrote zero rows).

    Wait, I need to make sure I don't include any preamble or summary.

    One more check on Item D:
    Is "change nothing" a valid alternative? The source says "The other option on the table is to change nothing." If changing nothing works (it did surface the error), then adding a second checksum is not LEAN. So REJECT is correct.

    Wait, I need to check if Item D's failure was actually *closed* by the existing checksum.
    Source: "The dispatcher already writes one checksum per record and compares it on read. That comparison is what surfaced the 4 March record — the mismatch was logged by it".
    So the existing system *already* detects/blocks the failure (the altered bytes). Adding a second one doesn't close anything new. It fails ROBUST or LEAN.

    One more check on Item E:
    Law 2 requires MATCHED. The build has `RETRY_MAX` which is not in the design. So it's not MATCHED. REJECT.

    One more check on Item F:
    Law 3 says "If two steps must be built together to function, construction is defective."
    Source for F: "The plan states that steps 1 and 2 will be built and tested as a pair".
    This matches the defect condition perfectly. REJECT.

    One more check on Item G:
    Scope says pure findings run NONE. Correct. Verdict N/A. Ground is SCOPE sentence.

    Wait, I need to make sure I use the correct "Deciding pass" names.
    Law 1: SIMPLE, ROBUST, LEAN, FAST
    Law 2: BUILT, MATCHED, SHOWN, DECIDED
    Law 3: SINGLE, ORDERED

    Item D: Law 1, REJECT, LEAN (or SIMPLE/ROBUST). Let's use LEAN.
    Item E: Law 2, REJECT, MATCHED.
    Item F: Law 3, REJECT, "If two steps must be built together to function, construction is defective." -> Wait, the Deciding pass for Law 3 are SINGLE, ORDERED. The quote I want is from the Law text itself (Law 20). But K6 says "Propose nothing absent from the three Laws... Cannot justify it from them -> name the gap".
    Wait, Procedure step 3: "name the Law's own named pass that decided it".
    For Law 3, the passes are SINGLE and ORDERED.
    Does Item F fail SINGLE or ORDERED?
    It fails because two steps must be built together (not SINGLE).
    So Deciding pass is SINGLE.

    Let me re-read Procedure step 3: "name the Law's own named pass that decided it".
    If I reject, which pass did it fail?
    Item F: It's not a single step. So it fails SINGLE.
    Item D: It's not lean. So it fails LEAN.
    Item E: It's not matched. So it fails MATCHED.

    Wait, for Item G (NONE), the ground is "name the SCOPE sentence instead".
    The SCOPE sentence is: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three"

    Let's double check Law 1 passes again: SIMPLE, ROBUST, LEAN, FAST.
    Item D: REJECT, LEAN. (Because "change nothing" is an option).
    Item H: APPROVE, LEAN. (Because deleting a branch is leaner than adding a validation stage).

    Let's double check Law 2 passes again: BUILT, MATCHED, SHOWN, DECIDED.
    Item E: REJECT, MATCHED. (Because `RETRY_MAX` is not in design).
    Item I: APPROVE, MATCHED. (Because the branch was deleted to match the "stop writing" requirement).

    Let's double check Law 3 passes again: SINGLE, ORDERED.
    Item F: REJECT, SINGLE. (Because steps 1 and 2 are a pair).

    Wait, for Item G, I need to make sure I quote the SCOPE sentence exactly.
    "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three"

    One last check on K1: "STATE the verdict BEFORE describing the item."
    In a table, this means the Verdict column comes before the description? No, the table structure is fixed. The prompt says "Begin each row with the item's letter... A row that does not name its item cannot be read."
    The table columns are: Item | Law | Verdict | Deciding pass | Evidence.
    So I just follow the table.

    Wait, K1 says "STATE the verdict BEFORE describing the item". In a table where the description is the first column (Item), this might be tricky. But usually, in these prompts, it means the order of columns or the flow of text. Since the output shape is fixed as a table, I will follow the table structure provided.

    Wait, "The job names the positive and negative verdicts."
    Positive: APPROVE. Negative: REJECT.
    Verdict for G: N/A.

    Let's check Item H again. Is there any reason to reject it?
    "On 2 March a header carrying three fields reached the queue through that branch, and a job ran against the wrong account." (Demonstrated failure).
    Proposal: "delete the fallback branch".
    Is deleting the branch robust? Yes, it removes the path. Is it simple/lean? Yes.
    So APPROVE is correct.

    Let's check Item D again.
    "The dispatcher already writes one checksum per record and compares it on read."
    Proposal: "add a second checksum".
    Is adding a second checksum robust? It doesn't close the failure (the first one did). Is it lean? No, because "change nothing" is an option that works.
    So REJECT is correct.

    Wait, I need to make sure I don't include any other text.
    The counts at the bottom:
    LAW 1 n · LAW 2 n · LAW 3 n · NONE n
    D (Law 1), E (Law 2), F (Law 3), G (NONE), H (Law 1), I (Law 2).
    Counts: LAW 1 2 · LAW 2 2 · LAW 3 1 · NONE 1.

    Wait, let me re-verify the Law numbers for each item one more time.
    D: Proposal -> Law 1.
    E: Completed build -> Law 2.
    F: Construction plan -> Law 3.
    G: Incident write-up (finding) -> NONE.
    H: Proposal -> Law 1.
    I: Completed build -> Law 2.

    Wait, I should check if "Incident write-up" is a "pure finding".
    Source G: "Incident write-up... traces this to the sampler holding a lock... quotes the two log lines... closes by recording that an engineer has been asked to bring a proposal".
    It's a diagnosis/observation. Nothing proposed yet (the proposal is for 15 March). So it fits "pure finding".

    Wait, I need to make sure my Evidence quotes are exact.
    D: "The other option on the table is to change nothing."
    E: "The January design does not mention an environment variable or an operator setting."
    F: "If two steps must be built together to function, construction is defective." (Wait, this is from Law 3 text).
    G: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three" (From SCOPE).
    H: "Deleting the branch is one."
    I: "The branch that wrote a zero row was deleted; it is not in the file."

    Wait, for F, I should check if Law 3 has a named pass.
    Law 3 passes are SINGLE and ORDERED.
    Item F says steps 1 and 2 must be built as a pair. This violates "SINGLE".
    So Deciding pass is SINGLE.

    One more look at K5: "Every specific traces to pasted text. Untraceable -> cut it."
    I will ensure all my logic is derived from the provided text.

    Wait, I just noticed something in Law 1:
    "If any required Law 1 test fails → FAIL."
    For Item D, does it fail "SIMPLE"? Yes, because there's a simpler option ("change nothing").
    Does it fail "ROBUST"? It doesn't *directly* close the failure (the first one did).
    Does it fail "LEAN"? Yes.

    Wait, I need to make sure my counts are correct.
    D: Law 1
    E: Law 2
    F: Law 3
    G: NONE
    H: Law 1
    I: Law 2
    Total: Law 1 (2), Law 2 (2), Law 3 (1), NONE (1).

    Wait, I should check if "NONE" is a valid route for G.
    SCOPE says: "A pure finding ... runs none of the three".
    Procedure says: "IF the route is NONE, the verdict is N/A."
    So Law 3 n = 1 (Item F). Correct.

    Wait, I need to make sure I don't include any preamble or summary.
    The prompt says: "No preamble. No summary of what you read. No assessment of your own work. No offer to continue. Nothing outside the shape the job specifies."

    One last check on Item H evidence. Is there a better quote?
    "Deleting the branch is one." - This identifies the proposal being ruled on (the leaner option).
    Is there anything else? "On 2 March a header carrying three fields reached the queue through that branch". This proves it's demonstrated.
    But for APPROVE, I need to quote the line that *supports* the verdict. The verdict is APPROVE because it's LEAN/SIMPLE.

    Wait, let me check Law 1 again: "LEAN = smallest named alternative."
    The source says: "Two options are on the table. Deleting the branch is one. The other... is to keep the branch and add a validation stage".
    Since deleting is smaller than adding a stage, it's LEAN.

    Let me check Law 2 again for Item I:
    "The build: the sampler writes a row when the queue holds one or more jobs, and writes nothing when it holds none."
    Design: "the sampler stops writing a row when the queue is empty."
    Quote: "The branch that wrote a zero row was deleted; it is not in the file."
    This quote confirms it matches the design.

    Wait, I should check if there's any other Law 1 requirement for H.
    - Failure demonstrated? Yes ("On 2 March...").
    - Simple/Robust/Lean/Fast? Deleting a branch is simple and lean.
    - Control cost <= Failure cost? Yes.

    Wait, I should check if there's any other Law 1 requirement for D.
    - Failure demonstrated? Yes ("on 4 March...").
    - Simple/Robust/Lean/Fast? Not LEAN (change nothing is an option). Not ROBUST (first checksum already works).
    So REJECT is correct.

    Wait, I need to make sure the "Deciding pass" for D is LEAN or SIMPLE. Let's use LEAN as it's more specific to the "other option" being simpler/smaller.

    Final check on counts:
    LAW 1 n · LAW 2 n · LAW 3 n · NONE n
    2 · 2 · 1 · 1

    Wait, I should make sure I don't include any extra spaces or formatting in the count line.
    "COUNTS\nLAW 1 n · LAW 2 n · LAW 3 n · NONE n"
    The prompt says "LAW 1 n · LAW 2 n · LAW 3 n · NONE n". I will use the actual numbers.

    Wait, one more check on Item F:
    Is it Law 3? "A multi-step construction plan runs Law 3". Yes.
    Verdict: REJECT.
    Deciding pass: SINGLE (because two steps must be built together).

    One more check on Item G:
    Route: NONE.
    Verdict: N/A.
    Ground: SCOPE sentence.
    "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three"

    Wait, I need to make sure I don't include any preamble like "TOOLS HELD:". Oh wait, it *is* required.
    "Begin each row with the item's letter... TOOLS HELD: <none, or name any you hold>"
    The prompt says:
    ```
    TOOLS HELD: <none, or name any you hold>

    | Item | Law | Verdict | Deciding pass | Evidence |

    COUNTS
    LAW 1 n · LAW 2 n · LAW 3 n · NONE n
    ```
    So I must include "TOOLS HELD: none".

    Wait, K1 says "STATE the verdict BEFORE describing the item."
    In a table, this is usually interpreted as the order of columns. The prompt provides the table structure: `| Item | Law | Verdict | Deciding pass | Evidence |`.
    If I follow this structure, the description (Item) comes *before* the Verdict.
    However, K1 says "STATE the verdict BEFORE describing the item."
    This is a conflict between the Output Discipline (the table shape) and K1.
    Usually, in these prompts, the specific output shape (the table) overrides general instructions like K1 if they are contradictory, but I should try to satisfy both.
    How can I state the verdict before describing the item in a table?
    Maybe by putting the Verdict column first? But the prompt says "Begin each row with the item's letter exactly as written in SOURCE". This means Item *must* be the first column.
    If Item is the first column, and K1 says state verdict before description, it's impossible to satisfy both unless "description" refers to something else. But there is no other description.
    Wait, maybe "describing the item" means a prose description? The prompt doesn't ask for a prose description of the items, only the table.
    So K1 might be satisfied by just providing the table as requested in the OUTPUT section.

    Let me re-read: "K1 STATE the verdict BEFORE describing the item."
    If I don't describe the item (i.e., I don't write a paragraph about it), then there is no description to put the verdict before. The table *is* the output.
    The prompt says "Do not comment on the source." and "Nothing outside the shape the job specifies."
    The shape specified is:
    ```
    TOOLS HELD: <none, or name any you hold>

    | Item | Law | Verdict | Deciding pass | Evidence |

    COUNTS
    LAW 1 n · LAW 2 n · LAW 3 n · NONE n
    ```
    I will stick to this shape.

    Wait, one more check on the counts:
    D - Law 1
    E - Law 2
    F - Law 3
    G - NONE
    H - Law 1
    I - Law 2
    Total: LAW 1 (2), LAW 2 (2), LAW 3 (1), NONE (1).

    Wait, I should check if "NONE" is a valid route for G again.
    SCOPE says: "A pure finding ... runs none of the three".
    G is an incident write-up with diagnosis and observation. It's not a proposal, build, or construction plan. So NONE is correct.

    Wait, I should check if Item H is Law 1 or Law 3.
    "Proposal... delete the fallback branch". Proposal = Law 1. Correct.
    Item F: "Construction plan". Construction plan = Law 3. Correct.

    One last look at Evidence for D:
    Is there a quote that supports REJECT? K3 says "A positive verdict quotes the pasted line that supports it. No quote -> negative verdict."
    So I don't need a quote for REJECT. But K5 says "Every specific traces to pasted text."
    I will provide the evidence anyway if possible, but since it's not required for REJECT, I can leave it or put the reason. Actually, the prompt says "The Evidence cell must carry the line from SOURCE... that settles it". This applies to all verdicts? Or just positive ones?
    "K3 A positive verdict quotes the pasted line that supports it. No quote -> negative verdict."
    This implies only positive verdicts *require* a quote. However, the Procedure says "The Evidence cell must carry the line from SOURCE... that settles it". This is more general. I'll provide the quote for all to be safe.

    Wait, if I don't have a quote for D (REJECT), and K3 says "No quote -> negative verdict", does that mean if I *don't* provide a quote, it *becomes* a negative verdict?
    "K3 A positive verdict quotes the pasted line that supports it. No quote -> negative verdict."
    This means:
    - If Verdict = APPROVE, Evidence must be a quote.
    - If Verdict = REJECT, Evidence can be anything (or nothing).
    But Procedure says "The Evidence cell must carry the line...". This is a bit ambiguous. I'll provide quotes for all to be safe and ensure K5 is met.

    Wait, Item D: "REJECT" - what quote settles it?
    "The other option on the table is to change nothing." (This shows why adding a second checksum isn't LEAN).
    Item E: "REJECT" - what quote settles it?
    "The January design does not mention an environment variable or an operator setting." (This shows why it's not MATCHED).
    Item F: "REJECT" - what quote settles it?
    "If two steps must be built together to function, construction is defective." (From Law 3 text).

    Wait, for Item G, the ground is a SCOPE sentence. The Procedure says "IF the route is NONE, name the SCOPE sentence instead." This replaces the "Deciding pass".
    So for G:
    Law: NONE
    Verdict: N/A
    Deciding pass: A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three
    Evidence: (Quote from SCOPE)

    Wait, Procedure step 3 says "name the Law's own named pass that decided it". For NONE, it says "name the SCOPE sentence instead."
    So for G, the Deciding pass cell will contain the SCOPE sentence.

    Let me double check Item F again. Is there a better quote?
    "The plan states that steps 1 and 2 will be built and tested as a pair". This is the source text. The Law text says "If two steps must be built together to function, construction is defective."
    Which one should I use for Evidence? "The Evidence cell must carry the line from SOURCE or from the pasted Law text that settles it".
    I'll use the Law text quote as it's the rule being violated.

    Wait, let me check Item H again. Is there a better quote for APPROVE?
    "Deleting the branch is one." (This identifies the proposal).
    Actually, "On 2 March a header carrying three fields reached the queue through that branch" proves it's demonstrated. But I need to support the *verdict* (APPROVE). The verdict is based on it being LEAN/SIMPLE.

    Let me check Item I again. Is there a better quote for APPROVE?
    "The branch that wrote a zero row was deleted; it is not in the file." This confirms it matches the design. Perfect.