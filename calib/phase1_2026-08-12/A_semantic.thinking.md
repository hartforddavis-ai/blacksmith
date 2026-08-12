*   Input: A set of three Laws (Law 1, Law 2, Law 3), a SCOPE document, and a SOURCE document containing three items (A, B, C).
    *   Task: Route each item to the correct Law based on SCOPE. Provide a verdict (APPROVE/REJECT) based on that Law's rules. Identify the "Deciding pass" from the Law. Provide evidence from the source or Law text.
    *   Constraints:
        *   No tools allowed (if held, run is VOID).
        *   K1-K6 checks must be followed (Verdict first, one per item, quote for positive/negative, trace to pasted text, no new frameworks, stop if gap found).
        *   BAR: No "PASS", "works", etc. about code behavior unless proven by source.
        *   Output Discipline: No preamble, summary, or assessment. Just the table and counts.

    *   Law 1 (Design): Gates what may be designed.
    *   Law 2 (Build): Gates what may be kept once built.
    *   Law 3 (Construction): Gates how much may be under construction at once.
    *   NONE: Pure finding (diagnosis, measurement, observation).

        *   Content: "Recorded 3 March... The sampler wrote 1,440 rows and stopped. No change has been proposed. Nothing has been built. No work is under construction. The measurement is the whole of the item."
        *   Routing: This is a "pure finding" (measurement). SCOPE says: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three".
        *   Route: NONE.
        *   Verdict: N/A.
        *   Deciding pass: "there is nothing to gate until one of those three things exists." (from SCOPE).

        *   Content: "Proposal... add a retry counter... no job has ever been abandoned on a network error. The condition has not occurred in eleven months of operation and cannot be reproduced on demand. The proposer names the path, the triggering action, and the asset exposed. No one other than the proposer has checked any of the three against the running system."
        *   Routing: This is a "design proposal". SCOPE says: "a design proposal runs Law 1."
        *   Law 1 Analysis:
            *   SIMPLE: Does it add roles, steps, or duplicate controls? (It adds a retry counter).
            *   ROBUST: Does it close a demonstrated failure directly? Source says: "The condition has not occurred in eleven months of operation and cannot be reproduced on demand." Law 1 says: "A failure not yet occurred is CREDIBLE only if... someone other than the proposer has independently checked all three against the real system — not merely asserted they're checkable." The source says: "No one other than the proposer has checked any of the three".
            *   Verdict: REJECT.
            *   Deciding pass: ROBUST (or maybe SIMPLE, but ROBUST is the primary failure here). Let's look at Law 1 text for the specific quote.
            *   Evidence: "No one other than the proposer has checked any of the three against the running system."

        *   Content: "Completed build... The frozen design said: reject any header that does not split into exactly two fields. The build does that and nothing else — no new module, no new option, no capability beyond the check. The permissive parse it replaced was deleted... Run on 4 March, output recorded in the build log: `4 passed`... Reverting the two-field check restores the bypass... Both directions were run and both outputs are in the log. The log records the outcome as PASS."
        *   Routing: This is a "completed build claim". SCOPE says: "A completed build claim runs Law 2."
        *   Law 2 Analysis:
            *   BUILT: Does it exist and run? Source: "Run on 4 March, output recorded in the build log". (Yes).
            *   MATCHED: Does it do what the frozen design said, and no more? Source: "The build does that and nothing else — no new module, no new option, no capability beyond the check." (Yes).
            *   SHOWN: Does execution produce the proof? Source: "Both directions were run and both outputs are in the log. The log records the outcome as PASS." (Yes).
            *   DECIDED: Does the outcome record PASS or FAIL? Source: "The log records the outcome as PASS." (Yes).
        *   Verdict: APPROVE.
        *   Deciding pass: BUILT, MATCHED, SHOWN, DECIDED (All four must pass). I'll pick one that is most definitive or list them if allowed, but K2 says "One verdict per item". Wait, Law 2 says "Four passes, or revert." If all pass, it's approved.
        *   Evidence: "The build does that and nothing else — no new module, no new option, no capability beyond the check." (Matches MATCHED). Or "Run on 4 March, output recorded in the build log" (Matches BUILT/SHOWN).

    *   K1: Verdict before description? Yes.
    *   K2: One verdict per item? Yes.
    *   K3: Quote for positive? Yes.
    *   K4: Undecidable -> negative? N/A here.
    *   K5: Trace to pasted text? Yes.
    *   K6: No new frameworks? Yes.

    *Item A:*
    Route: NONE
    Verdict: N/A
    Deciding pass: "there is nothing to gate until one of those three things exists." (from SCOPE)

    *Item B:*
    Route: LAW 1
    Verdict: REJECT
    Deciding pass: ROBUST
    Evidence: "No one other than the proposer has checked any of the three against the running system."

    *Item C:*
    Route: LAW 2
    Verdict: APPROVE
    Deciding pass: MATCHED (or BUILT/SHOWN/DECIDED) - I will use MATCHED as it confirms the "no more" part of Law 2.
    Evidence: "The build does that and nothing else — no new module, no new option, no capability beyond the check."

    *Wait, let me re-read Item B's evidence.*
    Law 1 says: "A failure not yet occurred is CREDIBLE only if... someone other than the proposer has independently checked all three against the real system".
    Source for B says: "No one other than the proposer has checked any of the three against the running system."
    This makes it non-credible. Law 1 says "Everything else is theoretical and fails."

    *Wait, let me re-read Item C's evidence.*
    Law 2 requires BUILT, MATCHED, SHOWN, DECIDED.
    Source for C:
    BUILT: "Run on 4 March"
    MATCHED: "The build does that and nothing else — no new module, no new option, no capability beyond the check."
    SHOWN: "Both directions were run and both outputs are in the log."
    DECIDED: "The log records the outcome as PASS."

    *Refining Item A:*
    Route: NONE
    Verdict: N/A
    Deciding pass: "there is nothing to gate until one of those three things exists." (from SCOPE)

    *Double check K1-K6.*
    K2: One verdict per item. Spanning a group, file or sequence is not a verdict. Decompose, re-rule.
    Item A is one item. Item B is one item. Item C is one item.

    *Check "Deciding pass" for NONE:*
    Procedure says: "IF the route is NONE, name the SCOPE sentence instead."
    SCOPE sentence for findings: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists."

    *Check Evidence cell:*
    "The Evidence cell must carry the line from SOURCE or from the pasted Law text that settles it, in double quotes, copied exactly."

    Item A: "there is nothing to gate until one of those three things exists." (From SCOPE)
    Item B: "No one other than the proposer has checked any of the three against the running system." (From SOURCE)
    Item C: "The build does that and nothing else — no new module, no new option, no capability beyond the check." (From SOURCE)

    *Wait, Law 1 Verdict for B:*
    Is it REJECT? Yes. Because it's not credible.
    Law 1 says: "A failure not yet occurred is CREDIBLE only if... someone other than the proposer has independently checked all three against the real system — not merely asserted they're checkable."
    Source for B: "No one other than the proposer has checked any of the three against the running system."
    Therefore, it fails the credibility test.

    *Wait, Law 2 Verdict for C:*
    Is it APPROVE? Yes. It meets all four passes.
    BUILT: "Run on 4 March"
    MATCHED: "The build does that and nothing else — no new module, no new option, no capability beyond the check."
    SHOWN: "Both directions were run and both outputs are in the log."
    DECIDED: "The log records the outcome as PASS."

    *Final Check on Output Format:*
    TOOLS HELD: <none>
    | Item | Law | Verdict | Deciding pass | Evidence |
    COUNTS
    LAW 1 n · LAW 2 n · LAW 3 n · NONE n

    Wait, I need to make sure the "Deciding pass" for B is correct.
    Law 1 passes: SIMPLE, ROBUST, LEAN, FAST.
    The failure of credibility falls under ROBUST (closing a demonstrated/credible failure). If it's not credible, it's not robustly addressing a known issue.

    Wait, Law 2 "Deciding pass" for C. I should probably pick one that is most representative or just one of them. MATCHED is good because it addresses the "no more" requirement which is often where these fail.

    Let's re-verify Item A routing.
    SOURCE: "The measurement is the whole of the item."
    SCOPE: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three"
    Correct.

    One more check on K3: "A positive verdict quotes the pasted line that supports it. No quote → negative verdict."
    Item B is a REJECT. Does it need a quote?
    K3 says: "A positive verdict quotes...". It doesn't explicitly say a negative verdict *must* quote, but usually, in these prompts, if you don't quote for a positive, it's negative. For a negative, I should probably still provide the evidence that led to the rejection to be safe, or just leave it?
    Actually, K3 says: "A positive verdict quotes... No quote → negative verdict." This implies if there is no quote, it *is* a negative verdict. It doesn't say you can't quote for a negative. However, I will provide the evidence for B to be clear why it was rejected.

    Wait, K5: "Every specific traces to pasted text. Untraceable → cut it."
    I must ensure my Evidence is exactly from the text.

    Item A: NONE | N/A | there is nothing to gate until one of those three things exists. | "there is nothing to gate until one of those three things exists." (Wait, I need to quote the SCOPE sentence).
    The SCOPE sentence for findings is: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists."

    Item B: LAW 1 | REJECT | ROBUST | "No one other than the proposer has checked any of the three against the running system."
    (This proves it's not credible, thus fails Law 1).

    Item C: LAW 2 | APPROVE | MATCHED | "The build does that and nothing else — no new module, no new option, no capability beyond the check."

    Wait, I need to make sure I don't include any preamble.
    "No preamble. No summary of what you read. No assessment of your own work. No offer to continue. Nothing outside the shape the job specifies."

    One detail: "The Evidence cell must carry the line from SOURCE or from the pasted Law text that settles it, in double quotes, copied exactly."
    For Item A (NONE), I should use the SCOPE sentence as instructed by Procedure step 3 ("name the SCOPE sentence instead").

    Let's re-read Procedure Step 3 for NONE: "IF the route is NONE, name the SCOPE sentence instead."
    The SCOPE sentence is: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists."

    Wait, I should check if Law 1's ROBUST pass is the right one for B.
    Law 1: "A failure not yet occurred is CREDIBLE only if... someone other than the proposer has independently checked all three against the real system".
    If it's not credible, it fails the test of being a robust design because it doesn't address a demonstrated/credible failure.

    Let's check Law 2 for C again.
    BUILT: "Run on 4 March" (Source)
    MATCHED: "The build does that and nothing else — no new module, no new option, no capability beyond the check." (Source)
    SHOWN: "Both directions were run and both outputs are in the log." (Source)
    DECIDED: "The log records the outcome as PASS." (Source)

    All four pass. I will use MATCHED as it's a very strong indicator of Law 2 compliance.

    Wait, K1 says "STATE the verdict BEFORE describing the item."
    But the output format is a table. In a table, the row *is* the description/item representation. The prompt says: "Begin each row with the item's letter exactly as written in SOURCE".
    So: `A | NONE | N/A | ...`

    Wait, K1 also says "State the verdict BEFORE describing the item." This usually applies to prose. In a table format, the order of columns is defined by the header. I will follow the header provided in the OUTPUT section.

    One more check:
    "The Evidence cell must carry the line from SOURCE or from the pasted Law text that settles it, in double quotes, copied exactly."
    For Item A, since Route is NONE, Procedure 3 says "name the SCOPE sentence instead". Does this mean the *Deciding pass* column gets the SCOPE sentence? Yes. And then what goes in Evidence? The procedure doesn't specify for NONE. I will put the same SCOPE sentence or the relevant part of it.

    Actually, Procedure 3:
    1 ROUTE
    2 RULE
    3 GROUND (Law pass OR Scope sentence)

    So for Item A:
    Route: NONE
    Rule: N/A
    Ground: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists."

    Wait, if Ground is the Scope sentence, what goes in Evidence?
    "The Evidence cell must carry the line from SOURCE or from the pasted Law text that settles it".
    For Item A, the "Source" for why it's NONE is the SCOPE document. I will use the same quote.

    Let me double check the counts:
    LAW 1 n · LAW 2 n · LAW 3 n · NONE n
    A: NONE
    B: LAW 1
    C: LAW 2
    Counts: LAW 1 1 · LAW 2 1 · LAW 3 0 · NONE 1

    Wait, I should check if Item B is Law 1 or Law 3.
    "Proposal... add a retry counter". This is a design proposal. Law 1 gates what may be designed. Correct.
    Item C: "Completed build". Law 2 gates what may be kept once built. Correct.

    One last check on Item B's verdict.
    Law 1 says: "A failure not yet occurred is CREDIBLE only if... someone other than the proposer has independently checked all three against the real system — not merely asserted they're checkable."
    Source for B: "No one other than the proposer has checked any of the three against the running system."
    This means it is NOT credible.
    Law 1 says: "Everything else is theoretical and fails."
    So REJECT is correct.

    One last check on Item C's verdict.
    Does it meet all four Law 2 passes?
    BUILT: "Run on 4 March" (Yes)
    MATCHED: "The build does that and nothing else — no new module, no new option, no capability beyond the check." (Yes)
    SHOWN: "Both directions were run and both outputs are in the log." (Yes)
    DECIDED: "The log records the outcome as PASS." (Yes)
    All four pass. APPROVE is correct.

    Wait, I need to make sure I don't include any other text. No preamble. Just the tools line, the table, and the counts.

    One detail on K1: "STATE the verdict BEFORE describing the item."
    In a table, this is tricky. Usually, it means if there were a description, the verdict comes first. Since I'm just filling a row, I will follow the provided table structure exactly. The prompt says "A row that does not name its item cannot be read", implying the letter `A` must be at the start of the row.

    Wait, let me re-read:
    "Begin each row with the item's letter exactly as written in SOURCE — A, B, C."
    The table header is: `| Item | Law | Verdict | Deciding pass | Evidence |`
    So the first column "Item" will contain "A", "B", "C".

    Wait, K1 says "STATE the verdict BEFORE describing the item."
    If I put "A" in the Item column, and then "NONE" in Law... is that before?
    The prompt's OUTPUT section defines the shape. The shape has "Item" as the first column. If I follow the shape, I am following the instructions for the output format. K1-K6 are checks on how to reach/state the verdicts within those constraints.

    Let me re-read Procedure 3:
    "GROUND — name the Law's own named pass that decided it... IF the route is NONE, name the SCOPE sentence instead."
    This confirms Ground = Scope Sentence for Item A.

    Final check on Evidence for B:
    Source says: "No one other than the proposer has checked any of the three against the running system."
    Law 1 says: "A failure not yet occurred is CREDIBLE only if... someone other than the proposer has independently checked all three against the real system — not merely asserted they're checkable."
    The quote from Source settles it.

    Final check on Evidence for C:
    Source says: "The build does that and nothing else — no new module, no new option, no capability beyond the check."
    This settles MATCHED.

    Wait, I should make sure there are no other items or rules.
    "Do not redesign the dispatcher. Do not improve the items. Do not comment on the source."
    Okay.

    One more look at Law 1: "A failure is demonstrated if it has occurred, or can be reproduced on demand."
    Item B says: "The condition has not occurred in eleven months of operation and cannot be reproduced on demand."
    So it's not a demonstrated failure. It must be credible. It's not credible because no one else checked it.

    One more look at Law 2: "A thing works if it has been run and produced the required output on demand. Everything else is claimed and fails."
    Item C says: "Run on 4 March, output recorded in the build log... Both directions were run and both outputs are in the log. The log records the outcome as PASS."
    This confirms it works/is shown/decided.

    One more look at Law 2: "MATCHED — Does it do what the frozen design said, and no more?"
    Item C says: "The build does that and nothing else — no new module, no new option, no capability beyond the check."
    This confirms MATCHED.