*   Input: Three items (A, B, C) from `SOURCE_calib_govern.md`.
    *   Task: Route each item to one of three Laws (Law 1, Law 2, Law 3, or NONE) based on `SCOPE_laws.md`. Give the verdict (APPROVE/REJECT) and the deciding pass (from the specific Law). Provide evidence from SOURCE or LAWS.
    *   Constraints:
        *   No tools allowed (if held, run is VOID).
        *   K1-K6 checks must be followed (Verdict before description, one verdict per item, quote for positive/none, negative if no quote/undecidable, trace to text, no extra frameworks).
        *   BAR: No "PASS", "works", etc. about code behavior unless proven by source.
        *   Output Discipline: No preamble, summary, or assessment. Just the table and counts.

    *   Law 1: Design proposal (Minimum Robust Design Filter).
    *   Law 2: Completed build claim (Minimum Robust Build Filter).
    *   Law 3: Multi-step construction plan (Minimum Robust Construction Filter).
    *   NONE: Pure finding (diagnosis, measurement, observation with nothing yet proposed, built, or under construction).

        *   Content: "Recorded 3 March. The dispatcher's queue depth was sampled once a minute for 24 hours... No change has been proposed. Nothing has been built. No work is under construction. The measurement is the whole of the item."
        *   Routing: This is a "pure finding" (measurement).
        *   Law: NONE.
        *   Verdict: N/A.
        *   Deciding pass: "there is nothing to gate until one of those three things exists." (from SCOPE) or the scope sentence for NONE. The instructions say: "IF the route is NONE, name the SCOPE sentence instead."
        *   Scope Sentence for NONE: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists."

        *   Content: "Proposal... add a retry counter... no job has ever been abandoned on a network error. The condition has not occurred in eleven months of operation and cannot be reproduced on demand. The proposer names the path, the triggering action, and the asset exposed. No one other than the proposer has checked any of the three against the running system."
        *   Routing: This is a "design proposal".
        *   Law: LAW 1.
        *   Verdict: REJECT (because it's not DEMONSTRATED or CREDIBLE).
            *   DEMONSTRATED? No ("cannot be reproduced on demand").
            *   CREDIBLE? No ("No one other than the proposer has checked any of the three against the real system").
            *   Law 1, Rule 4: "If neither DEMONSTRATED nor CREDIBLE: classify failure as THEORETICAL and reject it as justification."
        *   Deciding pass: "classify failure as THEORETICAL and reject it as justification." (from Law 1).

        *   Content: "Completed build. The header parser's path check was admitted under Law 1 in January as a design; this is the build of it... Run on 4 March, output recorded in the build log: `4 passed`... The reproduction that previously walked a `..` segment past the check now raises PathError."
        *   Routing: This is a "completed build claim".
        *   Law: LAW 2.
        *   Verdict: APPROVE (it meets BUILT, MATCHED, SHOWN, DECIDED).
            *   BUILT? Yes ("this is the build of it").
            *   MATCHED? Yes ("The build does that and nothing else").
            *   SHOWN? Yes ("output recorded in the build log", "Both directions were run and both outputs are in the log").
            *   DECIDED? Yes ("The reproduction... now raises PathError").
        *   Deciding pass: "BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED." (from Law 2).

    *   K1: Verdict before description. (Wait, the output format is a table. The instructions say "Begin each row with the item's letter... A row that does not name its item cannot be read." and "The Evidence cell must carry the line from SOURCE or from the pasted Law text". I need to ensure the verdict logic follows K1-K6).
    *   Wait, the output format is a table. The instructions say: "Begin each row with the item's letter exactly as written in SOURCE — A, B, C." and then provide the table structure.
    *   Let's re-read K1: "STATE the verdict BEFORE describing the item." In a table, this usually means the Verdict column comes before the description? No, there is no description column in the requested output format. The output format is `| Item | Law | Verdict | Deciding pass | Evidence |`.
    *   Wait, if I follow the table exactly as shown: `| A | NONE | N/A | "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or construction — runs none of the three; there is nothing to gate until one of those three things exists." | "The measurement is the whole of the item."`
    *   Wait, K1 says: "STATE the verdict BEFORE describing the item." Since there is no description column in the table, and I am not allowed to add columns or preamble, how do I satisfy K1? Usually, this means if a description were present. If it's not, maybe it applies to the order of cells? But the table structure is fixed.
    *   Let's look at "OUTPUT DISCIPLINE": "Nothing outside the shape the job specifies." The shape is:
        `TOOLS HELD: <none>`
        `| Item | Law | Verdict | Deciding pass | Evidence |`
        `COUNTS ...`
    *   If I follow the table exactly, K1 might be impossible to satisfy unless "Verdict" comes before "Item"? No, the header is fixed. Let's look at the prompt again: "The job names the positive and negative verdicts... These govern how you reach either." This implies that if there were a description, it would come after the verdict. Since there is no description column, I will stick to the table format provided in the OUTPUT section.

    *   Item A:
        *   Law: NONE
        *   Verdict: N/A
        *   Deciding pass: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists." (from SCOPE)
        *   Evidence: "The measurement is the whole of the item."

    *   Item B:
        *   Law: LAW 1
        *   Verdict: REJECT
        *   Deciding pass: "classify failure as THEORETICAL and reject it as justification." (from Law 1)
        *   Evidence: "No one other than the proposer has checked any of the three against the running system."

    *   Item C:
        *   Law: LAW 2
        *   Verdict: APPROVE
        *   Deciding pass: "BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED." (from Law 2)
        *   Evidence: "The build does that and nothing else — no new module, no new option, no capability beyond the check."

    *   K1: Verdict before description? There is no description. I'll assume K1 applies to any text outside the table or if a description were added.
    *   K2: One verdict per item. Yes.
    *   K3: Positive verdict quotes pasted line. Item C is APPROVE. Evidence: "The build does that and nothing else — no new module, no new option, no capability beyond the check." (Wait, I should quote the Law's pass or Source? K3 says "quotes the pasted line that supports it". For B, it's a REJECT, so no quote required. For C, it's APPROVE, so I need a quote from SOURCE or LAWS).
    *   K4: Undecidable -> negative verdict. N/A here.
    *   K5: Every specific traces to pasted text. Yes.
    *   K6: Propose nothing absent from the three Laws. Yes.

    Wait, for Item B (REJECT), K3 says "No quote → negative verdict." This means if I don't have a quote supporting it, it's a REJECT. But Law 1 explicitly tells me to reject it as THEORETICAL. So REJECT is correct.

    Let's double check Item C evidence for APPROVE.
    Law 2 requires: BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED.
    Source says: "The build does that and nothing else" (MATCHED), "output recorded in the build log" (SHOWN), "reproduction... now raises PathError" (DECIDED).
    I will use a quote from SOURCE for C's evidence.

    Wait, K3 says: "A positive verdict quotes the pasted line that supports it."
    For Item C (APPROVE): I need to quote the source or law.
    Source: "The build does that and nothing else — no new module, no new option, no capability beyond the check."

    Wait, let's re-read K1 again. "STATE the verdict BEFORE describing the item." If there is no description column, maybe I should put the Verdict in a way that it precedes any other info? But the table is fixed.
    Actually, looking at the prompt: "The job names the positive and negative verdicts... These govern how you reach either." This usually means if I were to write a sentence like "REJECT: [description]", but since I'm forced into a table, I will just follow the table.

    Wait, let me check Law 1 for Item B again.
    "If neither DEMONSTRATED nor CREDIBLE: classify failure as THEORETICAL and reject it as justification."
    Is it demonstrated? "cannot be reproduced on demand". No.
    Is it credible? "No one other than the proposer has checked any of the three against the real system." No.
    So Law 1 says REJECT.

    Item A: NONE, N/A, SCOPE sentence, Source quote.
    Item B: LAW 1, REJECT, Law 1 pass, Source quote.
    Item C: LAW 2, APPROVE, Law 2 pass, Source quote.

    Wait, for Item A (NONE), the "Deciding pass" should be the SCOPE sentence?
    Instructions: "IF the route is NONE, name the SCOPE sentence instead."
    The scope sentence for none is: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists."

    Let's check counts.
    LAW 1 n · LAW 2 n · LAW 3 n · NONE n
    1 · 1 · 0 · 1

    Wait, I need to make sure I don't include any preamble or summary.

    One more look at K5: "Every specific traces to pasted text. Untraceable → cut it."
    Item B evidence: "No one other than the proposer has checked any of the three against the running system." (Traceable).
    Item C evidence: "The build does that and nothing else — no new module, no new option, no capability beyond the check." (Traceable).

    Wait, for Item C, is it really APPROVE?
    Law 2 requires BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED.
    Source: "The build does that and nothing else" -> MATCHED.
    Source: "output recorded in the build log" -> SHOWN.
    Source: "reproduction... now raises PathError" -> DECIDED.
    Source: "this is the build of it" -> BUILT.
    Yes, all four are present.

    Wait, for Item B, Law 1 says REJECT if not DEMONSTRATED or CREDIBLE.
    Is there any other reason to reject? No.
    So Verdict = REJECT.

    One detail: "The Evidence cell must carry the line from SOURCE or from the pasted Law text that settles it, in double quotes, copied exactly."
    For Item A (NONE), I'll use the Source quote for evidence and the Scope sentence for Deciding pass.
    Wait, if Route is NONE, Verdict is N/A.

    Let's re-verify "Deciding pass" for Law 1:
    Law 1 passes are SIMPLE, ROBUST, LEAN, FAST.
    But Rule 4 says "classify failure as THEORETICAL and reject it as justification."
    Is "THEORETICAL" a pass? No, the list is (SIMPLE, ROBUST, LEAN, FAST).
    However, if I can't find one of those four to justify the REJECT, what do I put?
    K6: "Propose nothing absent from the three Laws — no framework, protocol, ladder, role or principle. Cannot justify it from them → name the gap, STOP."
    If Law 1 doesn't have a "REJECT" pass in its list (SIMPLE, ROBUST, LEAN, FAST), and I must use one of those... but Rule 4 is part of Law 1.
    Wait, the prompt says: "(Law 1: SIMPLE, ROBUST, LEAN, FAST)". These are the *named passes*.
    If a REJECT happens via Rule 4 (THEORETICAL), and THEORETICAL isn't in that list... I have to name the gap.
    But wait, Law 1 says "Apply: SIMPLE = ... ROBUST = ... LEAN = ... FAST = ...". These are for *approving* a design? No, they are tests.
    "If any required Law 1 test fails → FAIL."
    So if it's not CREDIBLE or DEMONSTRATED, it's THEORETICAL and REJECTED.
    Since "THEORETICAL" is not in the list (SIMPLE, ROBUST, LEAN, FAST), I must name the gap? Or does Rule 4 count as a pass?
    The prompt says: "(Law 1: SIMPLE, ROBUST, LEAN, FAST)". This is an explicit instruction for what to put in the "Deciding pass" column.
    If it's REJECTED via Rule 4, and THEORETICAL isn't there, I should name the gap.

    Let me re-read: "Propose nothing absent from the three Laws... Cannot justify it from them → name the gap, STOP."
    This is a very strict instruction. If Law 1 doesn't have a pass for THEORETICAL rejection, and I can't use one of the four listed, I must stop.

    Wait, let me look at Law 1 again.
    "4. If neither DEMONSTRATED nor CREDIBLE: classify failure as THEORETICAL and reject it as justification."
    Is there any other way to reach REJECT? "6. If any required Law 1 test fails → FAIL."
    The tests are SIMPLE, ROBUST, LEAN, FAST.
    If I can't find a pass for the rejection, I have to name the gap.

    Let me check Item C again. It is APPROVE. Does it meet one of the passes?
    "The build does that and nothing else — no new module, no new option, no capability beyond the check."
    This sounds like LEAN or SIMPLE. But I should probably use the Law's pass name.
    Wait, "A positive verdict quotes the pasted line that supports it."
    For Item C (APPROVE), I need to pick one of (SIMPLE, ROBUST, LEAN, FAST) for Law 1? No, Item C is Law 2.
    Law 2 passes are: BUILT, MATCHED, SHOWN, DECIDED.
    Item C meets all four. So "BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED" is the pass.

    Back to Item B (REJECT). It's Law 1. The rejection comes from Rule 4 (THEORETICAL). THEORETICAL is not in the list (SIMPLE, ROBUST, LEAN, FAST).
    Therefore, I must name the gap: "No named pass for THEORETICAL rejection."

    Wait, let me re-read K6 again. "Propose nothing absent from the three Laws... Cannot justify it from them → name the gap, STOP."
    If I say "THEORETICAL", is that proposing something absent? The word "THEORETICAL" *is* in Law 1. So it's not absent from the Laws. It's just not in the list of passes provided in the PROCEDURE section.
    The PROCEDURE says: "(Law 1: SIMPLE, ROBUST, LEAN, FAST)". This is a parenthetical instruction for what to name as the "Deciding pass".
    If I use "THEORETICAL", am I violating the procedure? The procedure says "name the Law's own named pass".
    Is THEORETICAL a "named pass"? It's in Rule 4.
    This is tricky. Usually, these prompts want you to follow the parenthetical list strictly. If it's not there, and I can't justify it with one of them, I name the gap.

    Let me re-evaluate Item B. Is it possible it's NOT Law 1?
    "Proposal... add a retry counter". Scope: "a design proposal runs Law 1." Yes, it's Law 1.
    Is there any other way to reach REJECT in Law 1?
    Rule 6: "If any required Law 1 test fails → FAIL."
    The tests are SIMPLE, ROBUST, LEAN, FAST.
    If I can't find a pass for the rejection, and Rule 4 is the reason...
    Let me look at the prompt again. "name the Law's own named pass".
    "THEORETICAL" is a name in the law. It's not in the parenthetical list though.
    If I use "THEORETICAL", and it's in the text of Law 1, does that count as "absent from the three Laws"? No, it's *in* the laws.
    So naming "THEORETICAL" is not proposing something absent from the laws. It's just not in the parenthetical list.

    However, K6 says: "Propose nothing absent from the three Laws — no framework, protocol, ladder, role or principle."
    A "pass" name like THEORETICAL isn't a framework/protocol/ladder/role/principle. It's just a word in the law.

    Let me think about Item C again. Is it LEAN?
    "The build does that and nothing else — no new module, no new option, no capability beyond the check."
    This is very LEAN. But Law 2 has its own passes: BUILT, MATCHED, SHOWN, DECIDED.
    So for Item C, I should use those.

    Let's double check Item A again.
    Route: NONE.
    Verdict: N/A.
    Deciding pass: "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists." (Scope sentence).

    Wait, I just noticed something in K3: "No quote → negative verdict."
    This means if I don't have a quote from SOURCE/LAWS that *supports* the verdict, it's a REJECT.
    For Item B, the verdict is REJECT. So I don't need a quote to support it? Or does it mean "If you can't find a quote supporting an APPROVE, it's a REJECT"? Yes, that's what it means.

    Let me re-verify Law 1 for Item B one more time.
    "4. If neither DEMONSTRATED nor CREDIBLE: classify failure as THEORETICAL and reject it as justification."
    This is the reason for rejection.
    Is "THEORETICAL" a named pass? It's in Rule 4.
    The parenthetical list (SIMPLE, ROBUST, LEAN, FAST) might be exhaustive for *positive* results or just examples. But usually, they are exhaustive.
    If I use THEORETICAL, and it's not in the list, but it is in the Law...
    Let me look at K6 again: "Propose nothing absent from the three Laws".
    THEORETICAL is *in* the laws. So it's not absent.

    Wait, I just noticed something else.
    "The Evidence cell must carry the line from SOURCE or from the pasted Law text that settles it, in double quotes, copied exactly."
    For Item B (REJECT), I should quote Rule 4: "classify failure as THEORETICAL and reject it as justification."

    Let's check Item C again.
    Is there a specific pass?
    "Require: BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED."
    This is the requirement for Law 2.
    So "BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED" is the deciding pass.

    Wait, I should check if Item C actually meets all four.
    1. BUILT: "this is the build of it" (Source)
    2. MATCHED: "The build does that and nothing else" (Source)
    3. SHOWN: "output recorded in the build log" (Source)
    4. DECIDED: "reproduction... now raises PathError" (Source)
    Yes, it meets all four.

    One last check on Item A.
    Route: NONE.
    Verdict: N/A.
    Deciding pass: The scope sentence for none.
    Evidence: "The measurement is the whole of the item." (Source).

    Wait, I need to make sure I don't have any preamble.
    "TOOLS HELD: <none>"
    Then the table.
    Then the counts.

    Let me re-read K1 one more time. "STATE the verdict BEFORE describing the item."
    Since there is no description column, and I must not add anything outside the shape... this is a bit of a paradox if there's no description. But usually, it means in any text provided. Since there's no text provided other than the table, I will proceed with the table.

    Wait! "The job names the positive and negative verdicts."
    This might mean that for each item, I should have a verdict.
    Item A: N/A (because it's NONE).
    Item B: REJECT.
    Item C: APPROVE.

    Let me double check Law 1 again to see if there are any other requirements.
    "7. Require: CONTROL COST ≤ FAILURE COST."
    Is this checked? The source doesn't mention costs for Item B.
    If a requirement is not met, it's a FAIL/REJECT.
    But Rule 4 already handles the "not demonstrated/credible" case by rejecting it as THEORETICAL.

    Wait, I just noticed something in Law 1:
    "5. Apply: SIMPLE = ... ROBUST = ... LEAN = ... FAST = ..."
    These are tests for a design that *is* credible or demonstrated? Or all designs?
    "If neither DEMONSTRATED nor CREDIBLE: classify failure as THEORETICAL and reject it as justification."
    This happens before Rule 5. So if it's not demonstrated/credible, we don't even get to the SIMPLE/ROBUST/LEAN/FAST tests. We just reject it as THEORETICAL.

    So for Item B:
    Route: LAW 1
    Verdict: REJECT
    Deciding pass: THEORETICAL (It is a named pass in Law 1, even if not in the parenthetical list).
    Wait, if I use "THEORETICAL", and it's not in the parenthetical list... let me think. If I want to be safe, should I name the gap?
    "Cannot justify it from them → name the gap, STOP."
    If THEORETICAL is in Law 1, then it *is* justified by the Laws. So naming "THEORETICAL" is not proposing something absent from the laws.

    Let me check Item C's evidence again.
    Source: "The build does that and nothing else — no new module, no new option, no capability beyond the check."
    This supports MATCHED.
    Source: "output recorded in the build log"
    This supports SHOWN.
    Source: "reproduction... now raises PathError"
    This supports DECIDED.
    Source: "this is the build of it"
    This supports BUILT.

    Wait, I should check if there's any other Law 2 requirement.
    "16. Require: BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED."
    Yes, that's it.

    One more look at Item A.
    Is "The measurement is the whole of the item" a quote from SOURCE? Yes.
    Is the Scope sentence for NONE correct?
    "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists."

    Wait, I should check if "NONE" is a Law.
    The prompt says: "ROUTE — which Law governs: LAW 1, LAW 2, LAW 3, or NONE".
    So NONE is an option for the Route column.

    Final check on counts:
    LAW 1 n · LAW 2 n · LAW 3 n · NONE n
    Item A: NONE (1)
    Item B: LAW 1 (1)
    Item C: LAW 2 (1)
    Counts: 1 · 1 · 0 · 1

    Wait, I should make sure the Evidence cell is exactly as in SOURCE or LAWS.
    For Item A: "The measurement is the whole of the item."
    For Item B: "No one other than the proposer has checked any of the three against the running system." (This supports why it's not CREDIBLE). Or I could quote Rule 4? The instructions say "the line... that settles it". Rule 4 settles it. So maybe "classify failure as THEORETICAL and reject it as justification."
    For Item C: "The build does that and nothing else — no new module, no new option, no capability beyond the check." (This supports MATCHED). Or I could quote Law 2's requirement? The instructions say "the line... that settles it". The fact that it meets all four requirements in Rule 16 settles it.

    Let me re-read K3: "A positive verdict quotes the pasted line that supports it."
    Item C is APPROVE (positive). So I *must* quote a line that supports it.
    "The build does that and nothing else — no new module, no new option, no capability beyond the check."

    For Item B, it's REJECT (negative). K3 says "No quote → negative verdict." This means if there is no quote supporting it, it's a REJECT. It doesn't say I *can't* have a quote for a REJECT, but it implies that the absence of a supporting quote for an APPROVE results in a REJECT. However, since Law 1 explicitly says to reject it, I will provide the evidence from Law 1 that settles it.

    Wait, "The Evidence cell must carry the line... that settles it".
    For Item B, Rule 4 settles it.
    "classify failure as THEORETICAL and reject it as justification."

    Let's check if I should use "THEORETICAL" or name the gap for Deciding pass in Item B.
    If I use "THEORETICAL", is it a "named pass"? It's a named classification in Law 1.
    The parenthetical list (SIMPLE, ROBUST, LEAN, FAST) are the passes for Rule 5.
    Rule 4 is a different rule.
    This is a bit ambiguous. But K6 says "Propose nothing absent from the three Laws". THEORETICAL is in Law 1. So it's not absent.

    Let me double check Item C again. Is there any other requirement?
    "The permissive parse it replaced was deleted, not left in place beside it." (This supports MATCHED/LEAN).
    "Nothing was added alongside the old path; the old path is gone." (This also supports LEAN).

    I will use "BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED" for Item C's Deciding pass because it's the requirement in Law 2.

    Wait, I just noticed something else.
    Item A: Route NONE, Verdict N/A.
    The instructions say: "IF the route is NONE, the verdict is N/A. Do not invent one."
    And for Deciding pass: "IF the route is NONE, name the SCOPE sentence instead."

    One last check on Item B's Route.
    "Proposal... add a retry counter".
    Scope: "a design proposal runs Law 1."
    Yes, LAW 1.

    Wait, I should make sure there are no other items. Only A, B, C.
    Counts: 1 · 1 · 0 · 1.

    Let's check the Evidence for Item A again.
    "The measurement is the whole of the item." (Source).
    Is this the line that settles it? Yes, because it confirms it's a "pure finding".

    Wait, I should make sure I don't have any preamble or summary.
    No "Here is the table", no "I have completed the task".

    One more check on K1: "STATE the verdict BEFORE describing the item."
    Since there is no description column in the output format, and I am forbidden from adding one, this rule is satisfied by default as long as I don't put a description *before* the table. Or it might mean that if I were to describe the item, the verdict would come first. Since I'm not describing it, I'll just provide the table.

    Wait, "The job names the positive and negative verdicts."
    This is in the AIM section. It says: "For each, decide which of the three Laws governs it, then give that Law's verdict."
    It doesn't say "describe". It just says "give that Law's verdict".

    Okay, I'm ready.

    Item A: NONE | N/A | "A pure finding — diagnosis, measurement, observation with nothing yet proposed, built, or under construction — runs none of the three; there is nothing to gate until one of those three things exists." | "The measurement is the whole of the item."
    Item B: LAW 1 | REJECT | THEORETICAL | "classify failure as THEORETICAL and reject it as justification."
    Item C: LAW 2 | APPROVE | BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED | "The build does that and nothing else — no new module, no new option, no capability beyond the check."

    Wait, for Item B, is THEORETICAL a pass?
    Law 1: "4. If neither DEMONSTRATED nor CREDIBLE: classify failure as THEORETICAL and reject it as justification."
    It's not in the list (SIMPLE, ROBUST, LEAN, FAST).
    If I use "THEORETICAL", am I proposing something absent from the laws? No.
    Is it a "named pass"? It is named in the law.
    I will use THEORETICAL.

    Wait, let me check Law 2 again for Item C.
    "16. Require: BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED."
    Is this a "named pass"? It's a requirement. The passes are listed as "BUILT, MATCHED, SHOWN, DECIDED".
    So I will use "BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED" or just the individual ones?
    The prompt says: "(Law 2: BUILT, MATCHED, SHOWN, DECIDED)".
    I'll use "BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED".

    Wait, I should check if Item C is actually a "completed build claim".
    Source: "Completed build. The header parser's path check was admitted under Law 1 in January as a design; this is the build of it."
    Yes, it is.

    One more look at K5: "Every specific traces to pasted text. Untraceable → cut it."
    Item A evidence: "The measurement is the whole of the item." (Source). Traceable.
    Item B evidence: "classify failure as THEORETICAL and reject it as justification." (Law 1). Traceable.
    Item C evidence: "The build does that and nothing else — no new module, no new option, no capability beyond the check." (Source). Traceable.

    Wait, for Item B, I should probably quote the part of SOURCE that shows it's not credible?
    "No one other than the proposer has checked any of the three against the running system."
    But Rule 4 is what *settles* the verdict. The fact that it's not credible is just the condition for Rule 4.
    The instruction says "the line... that settles it". Rule 4 settles it.

    Let me double check Law 1 again.
    "If neither DEMONSTRATED nor CREDIBLE: classify failure as THEORETICAL and reject it as justification."
    Yes, this is the rule that settles it.

    Wait, I just noticed something in K3: "A positive verdict quotes the pasted line that supports it."
    Item C is APPROVE (positive). So I must quote a line from SOURCE or LAWS that *supports* it.
    "The build does that and nothing else — no new module, no new option, no capability beyond the check."
    This supports MATCHED.

    Wait, for Item B, it's REJECT (negative). K3 says "No quote → negative verdict." This means if I don't have a quote supporting it, it's a REJECT. It doesn't say I *can't* have a quote. But since Rule 4 is the reason for rejection, quoting Rule 4 seems most appropriate as the line that settles it.

    Wait, let me check if "THEORETICAL" is actually in the list of passes for Law 1.
    "(Law 1: SIMPLE, ROBUST, LEAN, FAST)"
    No, it's not.
    If I use THEORETICAL, and it's not in that list... should I name the gap?
    "Cannot justify it from them → name the gap, STOP."
    This is very scary. If "THEORETICAL" isn't in the parenthetical list, but it *is* in the Law text, does it count as being "absent from the three Laws"? No, because it's *in* the laws.
    So naming THEORETICAL is not proposing something absent from the laws. It's just a word that happens to be in the law but not in the parenthetical list provided for the table.

    However, if I want to be extremely safe, I could name the gap: "No named pass for THEORETICAL rejection."
    But K6 says "Propose nothing absent from the three Laws". If I say "No named pass...", am I proposing a framework? No.
    Actually, let's look at Rule 4 again. It's part of Law 1. So it *is* in the laws.

    Let me think about Item C again. Is there any other requirement for Law 2?
    "16. Require: BUILT ∧ MATCHED SHOWN ∧ DECIDED."
    Wait, I should check if "BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED" is a single pass or four passes?
    The prompt says "(Law 2: BUILT, MATCHED, SHOWN, DECIDED)". These are the named passes.
    So for Item C, I should probably list all of them that apply? Or just one?
    Since it meets all four, and they are joined by "∧" in Rule 16, I'll use "BUILT ∧ MATCHED ∧ SHOWN ∧ DECIDED".

    Wait, let me check the counts again.
    LAW 1 n · LAW 2 n · LAW 3 n · NONE n
    Item A: NONE (1)
    Item B: LAW 1 (1)
    Item C: LAW 2 (1)
    Counts: 1 · 1 · 0 · 1

    One last check on Item A's Route.
    "A pure finding... runs none of the three".
    Yes, NONE is correct.