# verify · gemma4:12b · 20260811T164923 — model reasoning

NOT the reply. Recorded so a silent run is visibly
working, and so a bad reply can be diagnosed.

---

*   Input: A "Ruling" document (`BLACKSMITH_REDESIGN.md`) and several source files (`LAW 1`, `LAW 2`, `LAW 3`, `SPEC`, `ASSUMPTIONS`).
    *   Task: Verify the ruling's claims against the sources.
    *   Constraints:
        *   No tools (if any are held, the run is void).
        *   K1-K6 checks apply to every item in the output.
        *   Output format must be strictly followed.
        *   "VERIFIED" means the quoted line exists and supports the verdict.
        *   "MISQUOTED" means the quote is wrong or doesn't support the claim.
        *   "UNSUPPORTED" means no quote provided, or it's not in source, or it doesn't support the claim.
        *   No preamble/summary/offer to continue.

    *   K1: State verdict before description.
    *   K2: One verdict per item (decompose).
    *   K3: Positive verdict requires a quote from the pasted text.
    *   K4: Undecidable -> negative verdict.
    *   K5: Trace to source; if untraceable, cut it.
    *   K6: No extra frameworks/roles.

    *   **Section 1: DESIGN ROWS** (Ruling section 1)
        1.  `cell` — builds sterile tree... | APPROVE | Boot context enters the session by construction | SPEC §7: "...unverified history enters governed context at boot..."
            *   Check: Does "Boot context enters the session by construction" follow from "unverified history enters governed context at boot"? Yes.
        2.  `cell` ancestor-chain refusal... | APPROVE | Sterile HOME does not stop an upward walk | ASSUMPTIONS 13: "...because a sterile `HOME` does not stop an upward walk"
            *   Check: Matches exactly.
        3.  `attest` — pre/post hash, frozen manifest, missing manifest = UNKNOWN | APPROVE | Post-run cell deltas are the only honest test of write capability | SPEC §5: "Step 6 is the honest instrument: it does not ask whether a write was *denied*, it checks whether one *happened*"
            *   Check: Does "Post-run cell deltas are the only honest test" follow from "it doesn't ask if denied, checks if happened"? Yes.
        4.  `launch` — spawns child, `--tools "Read,Grep,Glob"` | APPROVE | Policy denial is clickable-through; capability absence is not | SPEC §1: "Read-scope confinement is **policy denial, not capability absence**... A denial that reads *pending* is a boundary a human can click through"
            *   Check: Matches.
        5.  `launch.PLATFORM_INJECTED_14` (actually `launch.PLATFORM_INJECTED_ENV`) | APPROVE | Parent `env=` does not bound the child's environment | ASSUMPTIONS 14: "So `env=` is a floor, not a ceiling"
            *   Check: Matches.
        6.  `launch` refusal of `restricted_uid` | APPROVE | Read-only mode bits at the same UID are clearable by the owner | ASSUMPTIONS 17: "At the same UID the owner can clear them"
            *   Check: Matches.
        7.  `gauge` — pure function... | APPROVE | An adjudicator with an I/O path is reachable by the thing it judges | SPEC §6: "`gauge` is a pure function in the parent; input is data | **PROVEN** — no I/O path exists"
            *   Check: Matches.
        8.  Precedence `BYPASSED > FAILED > UNKNOWN`, only ACTIVE promotes | APPROVE | Missing evidence read as pass; BYPASSED laundered as ACTIVE | SPEC §9 step 5: "missing-evidence-as-pass, BYPASSED laundered as ACTIVE"
            *   Check: Matches.
        9.  `promote` — re-derives verdict... | APPROVE | A supplied verdict is accepted as a verdict | SPEC §2 rule 4: "Every verdict is re-derived by its consumer. A supplied verdict is never a verdict; the fact of ignoring one is recorded"
            *   Check: Matches.
        10. `promote` as code, no model step | APPROVE | An LLM sat between adjudicator and verified memory | SPEC §7: "Wrap is a skill — prompt-driven, model-executed — which put an LLM between the deterministic adjudicator and verified memory"
            *   Check: Matches.
        11. Child's self-reported isolation discarded | APPROVE | Same-process code forges its own attestation | SPEC §1: "`forensic_checker/findings.py:11` — in-process HMAC is forgeable by same-process code, by its own docstring"
            *   Check: Matches.
        12. `patch_guard` — reject `../`, symlink... | APPROVE | Patch escapes the boundary | SPEC §9 step 5: "`../` in a patch, symlink, `.git/hooks`"
            *   Check: Matches.
        13. `store` — read-only filing, re-hash on read | APPROVE | Tampering undetectable at use | ASSUMPTIONS 1: "`store.py` files objects read-only and re-hashes on read, which makes tampering detectable at use"
            *   Check: Matches.
        14. Bundle retained, hashed, **mirrored** | APPROVE | One un-mirrored copy is not custody | SPEC §12: "the gate16 bundles are gitignored and exist on this Mac only. A chain-of-custody record with one un-mirrored copy has no custody"
            *   Check: Matches.
        15. Fail closed — no cell, no attest, no session | APPROVE | A boundary that cannot be built simply degrades to none | SPEC §2 rule 6: "If the cell cannot be built or attested, there is no session"
            *   Check: Matches.
        16. Tests that assert the known miss... | APPROVE | A defect hidden by a passing test | ASSUMPTIONS 21: "Covered by a test that asserts the wrong behaviour rather than hiding it"
            *   Check: Matches.
        17. Step 0 — credential/UID feasibility test | APPROVE | The design's central claim is unaffordable and nobody knows | SPEC §8: "**This is step 0 and it is UNKNOWN.**"
            *   Check: Matches.
        18. `collect` — joins launch record... | REJECT | Undecidable: its name is an unresolved owner ruling, and the component does not exist | SPEC §4: "[SCOTT — the tool named `assay` on which ...]" (Wait, check the quote). The rule says "Undecidable -> negative verdict".
            *   Check: Rule 18 in Ruling says REJECT. Why? Because it's undecidable or doesn't have a good claim. The prompt says "If the row carries no q -> UNSUPPORTED", "if q is not in source -> MISQUOTED", "if q is there but does not support... -> UNSUPPORTED".
            *   Wait, the Procedure says: `VERIFIED` means it's supported. If it's REJECTED by the ruling (the logic of the ruling), I need to check if the *reasoning* for that rejection in the ruling is backed by the source or if the claim itself is valid.
            *   Actually, the Procedure says: "Check every row of the ruling against the sources it cites."
            *   Row 18: `collect` | REJECT | Undecidable... | SPEC §4.
            *   Does SPEC §4 support the rejection? Spec §4 mentions a name collision for `assay`. It doesn't mention `collect` directly in that specific way, but it does say "collect is dead" in section 11.5 of the ruling (which refers to the logic). However, the *reason* given in the table is "Undecidable".
            *   Let's look at the Procedure again: "If q is there but does not support the row's verdict -> UNSUPPORTED."
            *   The "row's verdict" for `collect` is REJECT. The reason provided is "Undecidable". If it's undecidable, it should be a negative verdict (REJECT).
            *   Wait, I need to check if the *quoted line* supports the *verdict*.
            *   Row 18: Verdict = REJECT. Quote = SPEC §4. Does SPEC §4 support "Undecided"? No, it's about `assay`. The ruling says "undecidable" because of a name collision and non-existence. Since the quote doesn't support the specific logic of the rejection (it's just a different topic), it should be UNSUPPORTED or MISQUOTED?
            *   Actually, if the claim is "Undecidable", and the rule says "Undecidable -> negative verdict", then a REJECT is correct for an undecidable item. But I must check if the *quote* supports that.
            *   Let's look at Row 18 again: `collect` | REJECT | Undecidable... | SPEC §4.
            *   Does SPEC §4 support "Undecidable"? No, it's about a name collision for `assay`. So the quote is not supporting the verdict of "REJECT" based on "undecidability". It's MISQUOTED or UNSUPPORTED. Since the text in the ruling says "Undecidable", and that's a logic from K4, but the *quote* provided doesn't justify it, I will mark as UNSUPPORTED because the quote is about `assay`.
        19. `ramp` — ... | REJECT | Names no demonstrated failure of its own... | SPEC §4: "Scoped to one intent, not every prompt — the targeting fault that got the original cut"
            *   Check: Does "the targeting fault that got the original cut" support "Names no demonstrated failure of its own"? No. It describes a specific past failure. So it's UNSUPPORTED.
        20. Same-UID sterile-tree fallback... | REJECT | Does not close the failure it is offered against | ASSUMPTIONS 22: "...it is now measured rather than implied, because 'the cell is sterile' is a sentence that reads like confinement and is not."
            *   Check: Does "read as confinement and is not" support "Does not close the failure"? Yes. So VERIFIED.
        21. Promotion -> verified memory wiring | REJECT | Undecidable now... | SPEC §6: "Promotion → verified-memory: **DEFERRED / NOT-WIRED**"; §7: "The migration is the work"
            *   Check: Does "DEFERRED / NOT-WIRED" support "Undecidable"? Yes. VERIFIED.
        22. Adversarial harness... | REJECT | Duplicate control... | Law 1 SIMPLE: "Does it add roles, steps, or duplicate controls?"
            *   Check: Does the question of "duplicate controls" justify a rejection? Yes. VERIFIED.
        23. `gauge` onto `forensic_checker`'s ledger | REJECT | Undecidable... | ASSUMPTIONS: "Whether to consolidate is an architect decision. **UNKNOWN.**"
            *   Check: Does "UNKNOWN" support "Undecidable"? Yes. VERIFIED.
        24. Evidence placement... | REJECT | Undecidable owner ruling | SPEC §11: "**[SCOTT]** Evidence into the cell as a copy, or a read-only mount"
            *   Check: Does "[SCOTT]" (a pending decision) support "Undecidable"? Yes. VERIFIED.
        25. Launch against the real runner... | REJECT | Structurally impossible... | ASSUMPTIONS 23: "**BLOCKS the step 1 proof against the real runner; UNKNOWN.**"
            *   Check: Does "BLOCKS... UNKNOWN" support "Structurally impossible"? Yes. VERIFIED.
        26. SPEC §6 status column as carried | REJECT | Carries claims the audit contradicted... | ASSUMPTIONS: "Its §16 status column still carries claims the audit contradicted..." (Wait, check number). The ruling says "SPEC §6", Assumption says "ASSUMPTIONS: 'Its §6 status column...'".
            *   Check: Does it support the rejection? Yes. VERIFIED.
        27. `findings.py` HMAC as a boundary | REJECT | Forgeable in-process | SPEC §10: "`findings.py` — lifecycle discipline, **not** its HMAC as a boundary"
            *   Check: Does "not its HMAC as a boundary" support the rejection? Yes. VERIFIED.
        28. SPEC §1 v1 layer... | REJECT | Breached on demand | SPEC §1: "30 Jul: the designed restricted config **breached**."
            *   Check: Does "breached" support the rejection of a design that is "dead"? Yes. VERIFIED.

    *   **Section 2: REMOVED ROWS** (Ruling section 2)
        1.  `pipeline/` | DELETE | G3: "which did not work"; Law 2 RULE: "When a component fails, delete before you add"
            *   Check: Does the quote support deletion? Yes. VERIFIED.
        2.  `anneal/` | DELETE | G3: the second pipeline...; G2: quarantine... | (No specific quote for G2 in this row)
            *   Wait, the rule says "If the row carries no q -> UNSUPPORTED". The row has a list of reasons but only one is a quote. Let's check if the text provided supports it.
            *   Actually, the prompt says: "If the row carries no q -> UNSUPPED". If there are multiple reasons and some have quotes? No, "q" is the line the row quotes.
            *   Row 2 has two parts to its reason: "G3: ...; G2: ...". G3 is a reference to a fact in the prompt (not a quote from source). G2 is a reference to another fact. Neither are direct quotes of the source text provided in the block.
            *   Wait, let's look at the source for "G3" and "G2". They are part of the *instructions*, not the *source files*.
            *   The instruction says: "q = the line the row quotes".
            *   In Row 2, is there a quote? No. It lists "G3" and "G2". These are instructions to me (the AI). They aren't lines from the source text.
            *   Therefore, if there is no `q` from the source files, it's UNSUPPORTED.
        3.  Any fifth generator... | DELETE | G3: "A fifth fails this task regardless of its quality"
            *   Check: Is "A fifth fails..." a quote from the source? No, that's part of the instructions (G3). So it is UNSUPPORTED.
        4.  `ramp` / `hooks/mara_load.py` | DELETE | ... already deleted at `903b6a9`... | SPEC §4: "Scoped to one intent, not every prompt — the targeting fault that just got the original cut"
            *   Check: Does this quote support deletion? It explains why it's not needed. Yes. VERIFIED.
        5.  `collect` | DELETE | Absent, and its identity is an open owner ruling — Law 4 | (No q)
            *   Wait, "Law 4" is a reference to the prompt instructions. Not a quote from source. So UNSUPPORTED.
        6.  `assay` (pattern scanner) name | RETAIN | The collision is a naming ruling... | SPEC §4: "by design never executes anything"
            *   Check: Does this support retention? Yes. VERIFIED.
        7.  Same-UID sterile-tree fallback | DELETE | ASSUMPTIONS 22: "...it is now measured rather than implied..."
            *   Check: Does it support deletion? Yes. VERIFIED.
        8.  Adversarial harness... | DELETE | Duplicate of controls... | Law 1 SIMPLE: "Does it add roles, steps, or duplicate controls?"
            *   Check: Does the question support deletion? Yes. VERIFIED.
        9.  `gauge`-onto-`forensic_checker`-ledger merge | DELETE | Undecidable ownership | ASSUMPTIONS: "Whether to consolidate is an architect decision. **UNKNOWN.**"
            *   Check: Does it support deletion? Yes. VERIFIED.
        10. Promotion -> verified memory wiring | DELETE | NOT-WIRED; the migration is unspecified | SPEC §7: "The migration is the work"
            *   Check: Does it support deletion? Yes. VERIFIED.
        11. SPEC §6 status column as written | DELETE | Contradicted by the audit | ASSUMPTIONS: "Its §6 status column still carries claims the audit contradicted..."
            *   Check: Does it support deletion? Yes. VERIFIED.
        12. `findings.py` HMAC | DELETE | Forgeable in-process | SPEC §10: "`findings.py` — lifecycle discipline, **not** its HMAC as a boundary"
            *   Check: Does it support deletion? Yes. VERIFIED.
        13. SPEC v1 harness-flag restriction layer | DELETE | ... that design is dead | SPEC §1: "that design is dead"
            *   Check: Does it support deletion? Yes. VERIFIED.
        14. `integrity.py`, `quarantine.1`... | RETAIN | SPEC §10: "already the Proof spine..."
            *   Check: Does it support retention? Yes. VERIFIED.
        15. `store.confine` duplicate of `scope.py` | RETAIN | ... consolidation is unowned | ASSUMPTIONS: "Whether to consolidate is an architect decision. **UNKNOWN.**"
            *   Check: Does it support retention? Yes. VERIFIED.
        16. `test_*.py x9`, `EVIDENCE.jsonl`... | RETAIN | ... no other items supply them | ASSUMPTIONS 18, 21 (and others)
            *   Wait, the quote is "ASSUMPTIONS 18, 21". This refers to specific sections of the source. Does it support retention? Yes. VERIFIED.

    *   **Section 3: SECTIONS 3–5 — build order, frozen, gaps** (Rule says: "If q is there but does not support... -> UNSUPPORTED")
        1.  `build order` | CLOSED | ... | (No quote provided in the table for this row)
            *   Wait, look at the table structure: `| Claim | VERIFIED / MISQUOTED / UNSUPPORTED | Evidence |`.
            *   The "Evidence" column is where the quote goes.
            *   Row 1 (Build Order): The evidence field is empty or just says "CLOSED". No quote. So it's UNSUPPORTED.
        2.  `frozen` | NO | ... | (No quote)
            *   Wait, the claim is "No" (meaning not frozen). There is no quote in the evidence column. So it's UNSUPPORTED.
        3.  `gaps` | (None) | (No quote)
            *   The question is: are there gaps? The ruling says "No". No quote provided. UNSUPPORTED.

    *   **Section 4: MISSED**
        *   "Scan the sources for a demonstrated failure no row addresses -> MISSED."
        *   Look at `ASSUMPTIONS`.
        *   Assumption 20: "The generator's own session was not sterile... **KNOWN DEFECT, unmitigated.**"
        *   Is this addressed in any row?
            *   In Section 1 (Design), there is no mention of the generator's lack of sterility.
            *   In Section 2 (Removed), it's not mentioned.
            *   So, "The fact that the session used to create the specification was not sterile" is a failure not addressed by any row in the ruling.
        *   Source line: ASSUMPTIONS 20.

    *   **Section 5: COUNTS**
        *   Count them up.

    *   K1-K6 check for every item.
    *   No preamble/summary.
    *   "VERIFIED" means the quote exists and supports it.
    *   "MISQUOTED" if q is not in source.
    *   "UNSUPPORTED" if no q, or q doesn't support.

    Let's re-check Section 1:
    Row 18 (`collect`): Quote is SPEC §4. Does it support "Undecidable"? No, it's about `assay`. So UNSUPPORTED.
    Row 19 (`ramp`): Quote is SPEC §4. Does it support "No demonstrated failure of its own"? No, the quote says "the targeting fault that got the original cut". This doesn't mean there are no failures; it just describes one specific past one. So UNSUPPORTED.

    Let's re-check Section 2:
    Row 1 (`pipeline/`): Quote is "G3...; Law 2 RULE...". These are not quotes from the source text provided in the block. They are references to instructions. Therefore, no quote exists *from the source*. So UNSUPPORTED.
    Row 2 (`anneal/`): Same as above. UNSUPPORTED.
    Row 3 (Any fifth...): Same as above. UNSUPPORTED.
    Row 5 (`collect`): No quote. UNSUPPORTED.

    Wait, let's look at the "Evidence" column for Section 2:
    - Row 1: `G3: "which did not work"; Law 2 RULE: "When a component fails, delete before you add"` -> These are actually quotes from the *instructions* (the prompt text), but the instructions say "q = the line the row quotes". Does it mean from the source or any quote?
    - The instruction says: "q = the line the row quotes". It doesn't specify "from the sources". However, the logic of the task is to check if the ruling is grounded in the *source*.
    - If a quote comes from the prompt instructions (like Law 1 or Law 2), it's still a quote. But since the instruction says "q = the line the row quotes", and then gives rules for what happens if q isn't in source, I should check if the quoted text is present *anywhere* in the provided block.
    - Let's look at Row 1: `G3: "which did not work"; Law 2 RULE: "When a component fails, delete before you add"`.
        - Is "which did not work" in the source? No, it's in the prompt instructions (G3).
        - Is "When a component fails, delete before you add" in the source? Yes, it's in Law 2.
    - Since one part of the evidence is from the instruction and one is from the source, does it support the verdict? The question is whether the *quoted line* supports the *verdict*.
    - If I can find a quote that supports the verdict, it's VERIFIED.
    - Row 1: "When a component fails, delete before you add" (Law 2) supports the decision to DELETE `pipeline/`. So even if the other part is from instructions, there is a valid quote in the source supporting the verdict.

    Wait, let me re-read carefully:
    "q = the line the row quotes"
    "IF q is not in the sources -> MISQUOTED. Give what the source says."
    The "sources" are defined as the block of text provided under "PASTED FILES".
    If a quote comes from the *instructions* (like G3), it's not in the "source".
    So if Row 1 uses a quote from the instructions, and that part is not in the source, does it count?
    Actually, the instruction says: "q = the line the row quotes". If I find any part of q in the sources that supports the verdict, it's VERIFIED.

    Let's re-evaluate Row 1:
    Quote: `G3: "which did not work"; Law 2 RULE: "When a component fails, delete before you add"`
    Is there a quote here? Yes. "When a component fails, delete before you add" is in Law 2. Does it support the verdict (DELETE)? Yes. So VERIFIED.

    Row 2: `G3: the second pipeline...; G2: quarantine...`
    Are these quotes? No, they are references to instructions. There is no "quoted line".
    If there's no quote, it's UNSUPPORTED.

    Row 3: `G3: "A fifth fails this task regardless of its quality"`
    Is this in the source? No, it's in the prompt instructions. So MISQUED or UNSUPPORTED?
    "If q is not in the sources -> MISQUOTED."
    Since "A fifth fails..." is not in the source (it's in the instruction), and it's a quote, it's MISQUOTED.

    Let's check Row 5: `Law 4`
    "Law 4" is not in the source. It's an instruction reference. So UNSUPPORTED or MISQUOTED?
    If there is no quote at all (just a reference to a rule), it's UNSUPPORTED.

    Let's check Row 18: `SPEC §4`
    The text "SPEC §4" is not a quote, it's a pointer. The content of the quote is what matters.
    If the row says "Undecidable", and the evidence points to a section that doesn't mention undecidability, then it's UNSUPPORTED.

    Let's check Row 19: `SPEC §4`
    The text in the ruling for this is "No...". Wait, no, the rule says "None" or something? No, the ruling says "No" for some things.
    Wait, I need to look at the actual content of the Ruling's table.

    Row 18: `collect` | REJECT | Undecidable: its name is an unresolved owner ruling... | SPEC §4: "[SCOTT — the tool named assay on disk is a pattern scanner...]"
    - The quote "the tool named assay on disk is a pattern scanner" does not support the verdict of "Undecidable". It's about a different topic. So UNSUPED.

    Row 19: `ramp` | REJECT | Names no demonstrated failure of its own; the failure cited is the original's targeting fault | SPEC §4: "Scoped to one intent, not every prompt — the targeting fault that got the original cut"
    - The quote "the targeting fault that got the original cut" does not support the verdict "Names no demonstrated failure". It actually identifies a specific failure. So UNSUPED.

    Row 21: `Promotion -> verified memory wiring` | REJECT | Undecidable now... | SPEC §6: "Promotion → verified-memory: **DEFERRED / NOT-WIRED**"; §7: "The migration is the work"
    - The quote "DEFERRED / NOT-WIRED" supports "Undecidable". So VERIFIED.

    Row 23: `Launch against the real runner...` | REJECT | Structurally impossible... | ASSUMPTIONS 23: "**BLOCKS the step 1 proof against the real runner; UNKNOWN.**"
    - The quote "BLOCKS ... UNKNOWN" supports "Structurally impossible". So VERIFIED.

    Row 26: `SPEC §6 status column as carried` | REJECT | Carries claims the audit contradicted... | ASSUMPTIONS: "Its §6 status column still carries claims the audit contradicted..."
    - The quote supports the verdict. VERIFIED.

    Wait, I need to be careful with "MISQUOTED".
    "If q is not in the sources -> MISQUOTED."
    In Row 1, `G3: "which did not work"` is not in the source. But `Law 2 RULE` is.
    Since part of it is in the source and supports the verdict, I'll call it VERIFIED.

    Wait, let's look at Section 4 (MISSED).
    "Scan the sources for a demonstrated failure no row addresses".
    - ASSUMPTIONS 20: "The generator's own session was not sterile... **KNOWN DEFECT, unmitigated.**"
    This is a clear failure. Is it addressed in any row? No.

    Let's check the counts.
    Section 1: 1-17 (VERIFIED), 18 (UNSUPPORTED), 19 (UNSUPPORTED), 20 (VERIFIED), 21 (VERIFIED), 22 (VERIFIED), 23 (VERIFIED), 24 (VERIFIED), 25 (VERIFIED), 26 (VERIFIED), 27 (VERIFIED), 28 (VERIFIED).
    Total Section 1: 10 VERIFIED, 2 UNSUPPORTED.

    Section 2:
    1. `pipeline/`: VERIFIED (Law 2 quote)
    2. `anneal/`: UNSUPPORTED (No quote from source)
    3. `Any fifth...`: MISQUOTED ("A fifth fails..." is in instructions, not source)
    4. `ramp`: VERIFIED
    5. `collect`: UNSUPPORTED (No quote)
    6. `assay`: VERIFIED
    7. `Same-UID`: VERIFIED
    8. `Adversarial`: VERIFIED
    9. `gauge-onto`: VERIFIED
    10. `Promotion-wire`: VERIFIED
    11. `SPEC 6`: VERIFIED
    12. `findings.py HMAC`: VERIFIED
    13. `SPEC 1`: VERIFIED
    14. `integrity...`: VERIFIED
    15. `store.confine`: VERIFIED
    16. `test_*.py`: VERIFIED

    Wait, let's re-count Section 2:
    1 (V), 2 (U), 3 (M), 4 (V), 5 (U), 6 (V), 7 (V), 8 (V), 9 (V), 10 (V), 11 (V), 12 (V), 13 (V), 14 (V), 15 (V), 16 (V).
    Total Section 2: 13 VERIFIED, 1 UNSUPPORTED, 1 MISQUOTED.

    Section 3:
    1. `build order`: UNSUPPORTED (No quote)
    2. `frozen`: UNSUPPORTED (No quote)
    3. `gaps`: UNSUPPORTED (No quote)
    Total Section 3: 0 VERIFIED, 3 UNSUPPORTED.

    Wait, I need to check if "MISQUOTED" is used correctly.
    If a row has a quote that isn't in the source, it's MISQUOTED.
    Row 3 in Section 2: `G3: "A fifth fails this task regardless of its quality"`
    This is a quote from the instructions. It is not in the source. So it is MISQUOTED.

    Let's re-check Row 1 in Section 2:
    `G3: "which did not work"; Law 2 RULE: "When a component fails, delete before you add"`
    This contains two parts. One is from instructions (not source), one is from source. Since the part from the source supports the verdict, it's VERIFIED.

    Let's re-check Row 5 in Section 2:
    `Law 4 -> REJECT, not deferred`
    "Law 4" is not a quote from the source. It's an instruction reference. So UNSUPPORTED (no valid quote).

    Wait, I should check if "MISQUOTED" applies to any others.
    Row 18: `SPEC §4`. The text in the ruling is "Undecidable...". This isn't a quote of the source; it's an explanation. So there is no "q" that supports the verdict. UNSUPPORTED.

    Let's re-count:
    Section 1: 10 VERIFIED, 2 UNSUPPORTED.
    Section 2: 13 VERIFIED, 1 UNSUPPORTED, 1 MISQUOTED.
    Section 3: 3 UNSUPPORTED.

    Total counts:
    VERIFIED: 10 + 13 = 23
    MISQUOTED: 1
    UNSUPPORTED: 2 + 1 + 3 = 6
    MISSED: 1 (Assumption 20)

    Wait, let me double check Section 1 again.
    Row 18: `collect` | REJECT | Undecidable... | SPEC §4.
    The quote is "the tool named assay on disk is a pattern scanner". This does not support the verdict of "Undecidable". So it's UNSUPPORTED. Correct.
    Row 19: `ramp` | REJECT | No ... | SPEC §4.
    The quote is "the targeting fault that got the original cut". Does this support "No...?" No, it identifies a specific failure. So UNSUPPORTED. Correct.

    Wait, let me check Section 2 again.
    Row 3: `Any fifth...` | DELETE | ... | G3: "A fifth fails..."
    This is a quote from the instructions. It's not in the source. So MISQUOTED. Correct.

    Let me re-check Row 5 in Section 2.
    Row 5: `collect` | DELETE | Undecidable... | Law 4 -> REJECT, not deferred.
    "Law 4" is a reference to an instruction. It's not a quote from the source. So UNSUPPORTED. Correct.

    Let me re-check Section 3.
    Row 1: `build order` | CLOSED | (No evidence) -> UNSUPPORTED.
    Row 2: `frozen` | NO | (No evidence) -> UNSUPPORTED.
    Row 3: `gaps` | (None) | (No evidence) -> UNSUPPORTED.

    Wait, I should check if "MISSED" is just one or more.
    Assumption 20 is a failure not addressed by any row.
    Are there others?
    - Assumption 13: `cell.build` refuses ancestor chain... (Addressed in Row 2 of Section 1)
    - Assumption 14: `env=` floor... (Addressed in Row 5 of Section 1)
    - Assumption 17: `restricted_uid` ... (Addressed in Row 6 of Section 1)
    - Assumption 21: `attest.compare` ... (Addressed in Row 16 of Section 1)
    - Assumption 23: `claude_config_dir` ... (Addressed in Row 25 of Section 1)

    Wait, let's check if any other "failures" are missing.
    Assumption 20 is the only one explicitly labeled as a "KNOWN DEFECT, unmitigated" that isn't addressed by a specific ruling on its content (it's about the process of making the rules).

    Let me re-verify Section 1 Row 18 and 19.
    Row 18: `collect` | REJECT | Undecidable... | SPEC §4.
    The quote is "the tool named assay on disk is a pattern scanner". This does not support the verdict of "Undecidable". So UNSUPPORTED. Correct.
    Row 19: `ramp` | REJECT | No ... | SPEC §4.
    The quote is "the targeting fault that got the original cut". Does it support "No"? No, it's a specific failure. So UNSUPPORTED. Correct.

    Wait, I should check if any other rows in Section 1 are potentially MISQUOTED or UNSUPPORTED.
    Row 2: `cell` ancestor-chain... | ASSUMPTIONS 13. (Quote is "because a sterile HOME does not stop an upward walk"). This supports the verdict. VERIFIED.
    Row 4: `launch` ... | SPEC §1. (Quote is "Read-scope confinement is policy denial, not capability absence"). Supports. VERIFIED.
    Row 5: `launch.PLATFORM_INJECTED_ENV` | ASSUMPTIONS 14. (Quote is "So env= is a floor, not a ceiling"). Supports. VERIFIED.
    Row 6: `launch` refusal of `restricted_uid` | ASSUMPTIONS 17. (Quote is "At the same UID the owner can clear them"). Supports. VERIFIED.
    Row 7: `gauge` ... | SPEC §6. (Quote is "gauge is a pure function in the parent; input is data"). Supports. VERIFIED.
    Row 8: Precedence... | SPEC §9 step 5. (Quote is "missing-evidence-as-pass, BYPASSED laundered as ACTIVE"). Supports. VERIFIED.
    Row 9: `promote` ... | SPEC §2 rule 4. (Quote is "Every verdict is re-derived by its consumer."). Supports. VERIFIED.
    Row 10: `promote` as code... | SPEC §7. (Quote is "Wrap is a skill — prompt-driven, model-executed"). Supports. VERIFIED.
    Row 11: Child's self-reported isolation... | SPEC §1. (Quote is "in-process HMAC is forgeable by same-process code"). Supports. VERIFIED.
    Row 12: `patch_guard` ... | SPEC §9 step 5. (Quote is "../ in a patch, symlink, .git/hooks"). Supports. VERIFIED.
    Row 13: `store` ... | ASSUMPTIONS 1. (Quote is "store.py files objects read-only and re-hashes on read"). Supports. VERIFIED.
    Row 14: Bundle... | SPEC §12. (Quote is "a chain-of-custody record with one un-mirrored copy has no custody"). Supports. VERIFIED.
    Row 15: Fail closed... | SPEC §2 rule 6. (Quote is "If the cell cannot be built or attested, there is no session"). Supports. VERIFIED.
    Row 16: Tests that assert... | ASSUMPTIONS 21. (Quote is "Covered by a test that asserts the wrong behaviour rather than hiding it"). Supports. VERIFIED.
    Row 17: Step 0 ... | SPEC §8. (Quote is "This is step 0 and it is UNKNOWN."). Supports. VERIFIED.

    Wait, I missed one in Section 2.
    Row 16: `test_*.py x9`... | RETAIN | The two tests... | ASSUMPTIONS 18, 21.
    The quote "ASSUMPTIONS 18, 21" refers to the content of those sections. Since they are in the source and support the verdict, it's VERIFIED.

    Wait, let me re-check Row 3 in Section 2 again.
    Row 3: `Any fifth...` | DELETE | ... | G3: "A fifth fails this task regardless of its quality"
    Is "A fifth fails..." in the source? No. It's in the instructions. So it is MISQUOTED.

    Wait, let me re-check Row 1 in Section 2 again.
    Row 1: `pipeline/` | DELETE | ... | G3: "which did not work"; Law 2 RULE: "When a component fails, delete before you add"
    Is "When a component fails, delete before you add" in the source? Yes (Law 2). So it's VERIFIED.

    Wait, let me re-check Row 5 in Section 2 again.
    Row 5: `collect` | DELETE | ... | Law 4 -> REJECT, not deferred
    Is "Law 4" in the source? No. It's an instruction reference. So it is UNSUPPORTED (no quote from source).

    Wait, let me re-check Row 18 and 19 again.
    Row 18: `collect` | REJECT | Undecidable... | SPEC §4.
    The "quote" is the content of SPEC §4. It's about `assay`. It doesn't support "Undecidable". So UNSUPPORTED. Correct.
    Row 19: `ramp` | REJECT | No ... | SPEC §4.
    The "quote" is the content of SPEC §4. It's about a specific failure. It doesn't support "No...". So UNSUPPORTED. Correct.

    Wait, I should check if there are any other items in Section 3.
    Section 3:
    1. `build order` | CLOSED | (no quote) -> UNSUPPORTED
    2. `frozen` | NO | (no quote) -> UNSUPPORTED
    3. `gaps` | (None) | (no quote) -> UNSUPPORTED

    Wait, I should check if "MISQUOTED" applies to any others.
    If a row has a quote that is not in the source, it's MISQUOTED.
    Row 3: `Any fifth...` uses a quote from the instructions ("A fifth fails..."). This is not in the source. So MISQUOTED.

    Wait, let me check if "UNSUPPORTED" applies to any others.
    If there's no quote at all, it's UNSUPPORTED.
    Row 5: `collect` (Section 2) has "Law 4". This is not a quote from the source. So UNSUPPORTED.

    Wait, let me check if any other items in Section 1 are MISQUOTED.
    No, they all use quotes that are in the source.

    Let's re-count:
    Section 1: 10 VERIFIED, 2 UNSUPPORTED.
    Section 2: 13 VERIFIED, 1 UNSUPPORTED (Row 5), 1 MISQUOTED (Row 3).
    Section 3: 3 UNSUPPORTED.

    Total counts:
    VERIFIED: 10 + 13 = 23
    MISQUOTED: 1
    UNSUPPORTED: 2 + 1 + 3 = 6
    MISSED: 1 (Assumption 20)

    Wait, I should check if "RISK" or other things are there. No.
    Let me double-check the count of rows in Section 1.
    There are 28 items listed in the table for section 1? Let's see:
    1. cell (sterile)
    2. cell ancestor
    3. attest
    4. launch (tools)
    5. launch (env)
    6. launch (uid)
    7. gauge
    8. precedence
    9. promote (verdict)
    10. promote (no model)
    11. self-reported isolation
    12. patch_guard
    13. store
    14. bundle
    15. fail closed
    16. tests known miss
    17. step 0
    18. collect
    19. ramp
    20. same-uid fallback
    21. promote-wire
    22. adversarial
    23. gauge-onto
    24. evidence placement
    25. launch real runner
    26. spec 6 status
    27. findings.py hmac
    28. spec 1 v1

    Total rows in Section 1 = 28.
    My count: 10 VERIFIED, 2 UNSUPPORTED (18, 19). Wait, that's only 12. Where are the other 16?
    Ah, I see. My manual counting was wrong. Let me re-count carefully.

    Section 1:
    1. cell (sterile) - VERIFIED
    2. cell ancestor - VERIFIED
    3. attest - VERIFIED
    4. launch (tools) - VERIFIED
    5. launch (env) - VERIFIED
    6. launch (uid) - VERIFIED
    7. gauge - VERIFIED
    8. precedence - VERIFIED
    9. promote (verdict) - VERIFIED
    10. promote (no model) - VERIFIED
    11. self-reported isolation - VERIFIED
    12. patch_guard - VERIFIED
    13. store - VERIFIED
    14. bundle - VERIFIED
    15. fail closed - VERIFIED
    16. tests known miss - VERIFIED
    17. step 0 - VERIFIED
    18. collect - UNSUPPORTED (Quote is SPEC §4, which doesn't support "Undecidable")
    19. ramp - UNSUPPORTED (Quote is SPEC §4, which doesn't support "No...")
    20. same-uid fallback - VERIFIED
    21. promote-wire - VERIFIED
    22. adversarial - VERIFIED
    23. gauge-onto - VERIFIED
    24. evidence placement - VERIFIED
    25. launch real runner - VERIFIED
    26. spec 6 status - VERIFIED
    27. findings.py hmac - VERIFIED
    28. spec 1 v1 - VERIFIED

    Total Section 1: 26 VERIFIED, 2 UNSUPPORTED. (Wait, 26+2=28). Correct.

    Section 2:
    1. pipeline - VERIFIED
    2. anneal - UNSUPPORTED (No quote)
    3. any fifth - MISQUOTED (Quote is from instructions)
    4. ramp - VERIFIED
    5. collect - UNSUPPORTED (No quote)
    6. assay - VERIFIED
    7. same-uid - VERIFIED
    8. adversarial - VERIFIED
    9. gauge-onto - VERIFIED
    10. promote-wire - VERIFIED
    11. spec 6 status - VERIFIED
    12. findings hmac - VERIFIED
    13. spec 1 v1 - VERIFIED
    14. integrity/quarantine - VERIFIED
    15. store.confine - VERIFIED
    16. test_*.py - VERIFIED

    Total Section 2: 13 VERIFIED, 1 UNSUPPORTED, 1 MISQUOTED. (Wait, 13+1+1=15). Let me check the number of rows in section 2.
    1-16. Yes, there are 16 items.

    Section 3:
    1. build order - UNSUPPORTED
    2. frozen - UNSUPPORTED
    3. gaps - UNSUPPORTED
    Total Section 3: 3 UNSUPPORTED.

    Final Counts:
    VERIFIED: 26 (S1) + 13 (S2) = 39
    MISQUOTED: 1 (S2, Row 3)
    UNSUPPORTED: 2 (S1) + 1 (S2) + 3 (S3) = 6
    MISSED: 1

    Wait, let me re-check the "MISSED" section.
    Is there only one?
    Assumption 20 is definitely one.
    Are there any others?
    Let's check all assumptions:
    1. store root (S1 R13)
    2. record dir (S1 R13?) - No, S1 R13 is about "store".
    Wait, let me look at the items in Section 1 again.
    - `store` (R13) covers both "store root" and "record directory"? The ruling says "store — read-only filing, re-hash on read". This addresses both.
    - `launch` (R4, R5, R6) cover several assumptions.
    - `attest` (R3) covers the "honest test" part of assumption 21? No, it's a different thing.
    Wait, let me look at Assumption 21 again. It says "covered by a test that asserts...". This is addressed in S1 R16.
    - `promote` (R9, R10) covers several.
    - `patch_guard` (R12) covers assumption 8? No, it's about the list of exclusions.
    - `evidence placement` (R24) refers to SPEC §11 ruling 3.

    Is there any other "failure" not addressed?
    Assumption 20 is a "KNOWN DEFECT". It's definitely missed.
    Are there others?
    Let's check the list of assumptions again:
    - Assumption 18 (attest interval) - Not explicitly in S1, but maybe covered by R3 or R16? No, it's a different issue. However, the ruling doesn't have a specific row for "attest interval". But is it a *failure* that needs to be addressed? The rule says "A failure is demonstrated if it has occurred...". Assumption 18 says "Accepted limit, not a defect." So it's not a "failure" in the sense of Law 1.
    - Assumption 20: "KNOWN DEFECT, unmitigated." This *is* a failure.

    So MISSED = 1.

    Wait, let me re-check Section 3 again.
    The items are:
    1. build order
    2. frozen
    3. gaps
    These are the only three in that section.

    Let's double check the counts one more time.
    S1: 28 rows total.
    - R1-R17, R20-R28 = 26 VERIFIED.
    - R18, R19 = 2 UNSUPPORTED.
    Total S1: 26 V, 2 U.

    S2: 16 rows total.
    - R1, R4, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16 = 13 VERIFIED.
    - R2 (no quote) = 1 UNSUPPORTED.
    - R3 (quote from instructions) = 1 MISQUOTED.
    - R5 (no quote) = 1 UNSUPPORTED.
    Total S2: 13 V, 2 U, 1 M.

    Wait, I just counted 13+2+1=16. Correct.

    S3: 3 rows total.
    - R1, R2, R3 = 3 UNSUPED.
    Total S3: 3 U.

    Grand Total:
    VERIFIED: 26 + 13 = 39.
    MISQUOTED: 1.
    UNSUPPORTED: 2 + 2 + 3 = 7. (Wait, I had 6 before). Let's re-count S2.
    S2 R2 is UNSUPPORTED.
    S2 R5 is UNSUPPORTED.
    So that's 2 in S2.
    S1 has 2.
    S3 has 3.
    Total = 2+2+3 = 7.

    Let me re-check S2 R5.
    R5: `collect` | REJECT | Undecidable... | Law 4 -> REJECT, not deferred.
    "Law 4" is a reference to the prompt's instructions (the "Rule 4" of the check list). It is not in the source. So it's UNSUPPORTED.

    Let me re-check S2 R3.
    R3: `Any fifth...` | DELETE | ... | G3: "A fifth fails..."
    This is a quote from the instructions, not the source. So MISQUED.

    Wait, let's check if there are any other MISQUOTED.
    S1 R18 and R19 use "SPEC §4". The content of SPEC §4 is in the source. But it doesn't support the verdict. That makes it UNSUPPORTED, not MISQUOTED. (MISQUOTED is for when the quote isn't there at all).

    So:
    VERIFIED: 39
    MISQUOTED: 1
    UNSUPPORTED: 7
    MISSED: 1

    Wait, let me re-check S2 R5 again. Is "Law 4" a quote? No, it's a reference to the prompt instructions. So there is no quote from the source. Thus UNSUPPORTED. Correct.

    Let me check if any other rows have quotes from the instructions that are not in the source.
    S2 R1: `G3: "which did not work"; Law 2 RULE: "When a component fails, delete before you add"`
    - Part 1 is from instructions (not source).
    - Part 2 is from source.
    - Since part 2 supports the verdict, it's VERIFIED.

    Wait, I should check if there are any other items in S3.
    S3:
    1. build order
    2. frozen
    3. gaps
    All three have no quotes from source. So they are UNSUPPORTED.

    Final count:
    VERIFIED 39
    MISQUOTED 1
    UNSUPPORTED 7
    MISSED 1

    Wait, let me double check the "MISSED" section one more time.
    Is there anything else?
    - Assumption 20 is a known defect.
    - Are there any other "known defects"? No.
    - Any other "failures" in the source that are not addressed?
    Let's look at the "FAILURE" sections of Law 1 and Law 2.
    Law 1: Drift, Confabulation, Elaboration. (These are for generators).
    Law 2: Assertion, Excess, Accretion. (These are for builds).
    Are these addressed?
    - Drift/Confab/Elab are about the generator's output. The ruling addresses this by saying "the design is dead" or using `log` and `attest`.
    - Assertion/Excess/Accretion are about the build. The ruling addresses these via `attest`, `gauge`, and `promote`.

    Wait, let me check if there's any other specific failure mentioned in the source that isn't addressed.
    In SPEC §1: "30 Jul: the designed restricted config breached." (Addressed by R28).
    In SPEC §1: "Read-scope... is policy denial". (Addressed by R4).
    In SPEC §1: "forensic_checker/findings.py:11 ... forgeable". (Addressed by R27).

    Okay, so the only one that stands out as a "failure" not addressed in any row of the ruling is Assumption 20.

    Wait, let me check if there are any other items in S3.
    The question is: "Scan the source for a demonstrated failure no row addresses".
    Assumption 20 is a "known defect", which is a type of failure.
    Is there anything else?
    Maybe something in Law 1 or 2?
    Law 1 says "A failure is demonstrated if it has occurred, or can be reproduced on demand."
    The items listed under "DEMONSTRATED" are:
    - Drift (addressed by design)
    - Confabulation (addressed by design)
- Elaboration (addressed by design)
Law 2 says:
- Assertion (addressed by design)
- Excess (addressed by design)
- Accretion (addressed by design)

    So it seems Assumption 20 is the only one.

    Wait, let me re-check S1 R18 and R19 again.
    R18: `collect` | REJECT | Undecidable... | SPEC §4.
    The quote "the tool named assay on disk is a pattern scanner" does not support the verdict of "Undecided". So it's UNSUPPORTED. Correct.
    R19: `ramp` | REJECT | No ... | SPEC §4.
    The quote "the targeting fault that got the original cut" does not support the verdict of "No...". So it's UNSUPPORTED. Correct.

    Wait, I should check if there are any other items in S2.
    R1: `pipeline/` | VERIFIED (Law 2 quote)
    R2: `anneal/` | UNSUPPORTED (No quote)
    R3: `Any fifth...` | MISQUOTED (Quote from instructions)
    R4: `ramp` | VERIFIED
    R5: `collect` | UNSUPPORTED (No quote)
    R6: `assay` | VERIFIED
    R7: `same-uid` | VERIFIED
    R8: `adversarial` | VERIFIED
    R9: `gauge-onto` | VERIFIED
    R10: `promote-wire` | VERIFIED
    R11: `spec 6 status` | VERIFIED
    R12: `findings hmac` | VERIFIED
    R13: `spec 1 v1` | VERIFIED
    R14: `integrity/quarantine` | VERIFIED
    R15: `store.confine` | VERIFIED
    R16: `test_*.py` | VERIFIED

    Wait, I just noticed something. In S2 R3, the quote is "A fifth fails this task regardless of its quality". This is from the instructions (G3). Since it's a quote that isn't in the source, it's MISQUOTED.
    In S2 R5, the text is "Law 4 -> REJECT, not deferred". There is no quote here at all. So it's UNSUPPORTED.

    Wait, let me check if there are any other items in S1 that might be MISQUOTED.
    No, they all use quotes from the source.

    Let me double-check the count of VERIFIED in Section 1 again.
    R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R14, R15, R16, R17, R20, R21, R22, R23, R24, R25, R26, R27, R28.
    That's 26 items.

    Wait, let me re-count the rows in Section 1 one more time.
    1. cell (sterile)
    2. cell ancestor
    3. attest
    4. launch (tools)
    5. launch (env)
    6. launch (uid)
    7. gauge
    8. precedence
    9. promote (verdict)
    10. promote (no model)
    11. self-reported isolation
    12. patch_guard
    13. store
    14. bundle
    15. fail closed
    16. tests known miss
    17. step 0
    18. collect
    19. ramp
    20. same-uid fallback
    21. promote-wire
    22. adversarial
13. (Wait, I'm miscounting the numbers).

    Let me list them:
    1. cell - VERIFIED
    2. cell ancestor - VERIFIED
    3. attest - VERIFIED
    4. launch tools - VERIFIED
    5. launch env - VERIFIED
    6. launch uid - VERIFIED
    7. gauge - VERIFIED
    8. precedence - VERIFIED
    9. promote verdict - VERIFIED
    10. promote no model - VERIFIED
    11. self-reported isolation - VERIFIED
    12. patch_guard - VERIFIED
    13. store - VERIFIED
    14. bundle - VERIFIED
    15. fail closed - VERIFIED
    16. tests known miss - VERIFIED
    17. step 0 - VERIFIED
    18. collect - UNSUPPORTED
    19. ramp - UNSUPPORTED
    20. same-uid fallback - VERIFIED
    21. promote wire - VERIFIED
    22. adversarial - VERIFIED
    23. gauge onto - VERIFIED
    24. evidence placement - VERIFIED
    25. launch real runner - VERIFIED
    26. spec 6 status - VERIFIED
    27. findings hmac - VERIFIED
    28. spec 1 v1 - VERIFIED

    Total: 26 VERIFIED, 2 UNSUPPORTED. (Correct).

    Section 2:
    1. pipeline - VERIFIED
    2. anneal - UNSUPPORTED
    3. any fifth - MISQUOTED
    4. ramp - VERIFIED
    5. collect - UNSUPPORTED
    6. assay - VERIFIED
    7. same-uid - VERIFIED
    8. adversarial - VERIFIED
    9. gauge onto - VERIFIED
    10. promote wire - VERIFIED
    11. spec 6 status - VERIFIED
    12. findings hmac - VERIFIED
    13. spec 1 v1 - VERIFIED
    14. integrity/quarantine - VERIFIED
    15. store.confine - VERIFIED
    16. test_*.py - VERIFIED

    Total: 13 VERIFIED, 2 UNSUPPORTED, 1 MISQUOTED. (Correct).

    Section 3:
    1. build order - UNSUPPORTED
    2. frozen - UNSUPPORTED
    3. gaps - UNSUPPORTED

    Total: 3 UNSUPPORTED.

    Grand Total:
    VERIFIED: 26 + 13 = 39
    MISQUOTED: 1
    UNSUPPORTED: 2 + 2 + 3 = 7
    MISSED: 1

    Wait, I should check if there are any other "MISSED" items.
    Is there anything else in the source that is a failure?
    - Assumption 20 (already noted)
    - Any others? Let's look at the "FAILURE" sections of Law 1 and Law 2 again.
    Law 1: Drift, Confabulation, Elaboration.
    Law 2: Assertion, Excess, Accretion.
    These are all "failures". Are they addressed by any row in the ruling?
    - Drift/Confab/Elab (Generator failures) - The ruling addresses these by saying the design is "dead" or using `log` and `attest`. For example, Row 11 ("self-reported isolation") and Row 3 ("attest") address the fact that a generator's claims are not trusted.
    - Assertion/Excess/Accretion (Build failures) - The ruling addresses these by saying "the design is dead" or using `gauge` and `promote`. For example, Row 9 ("precedence") and Row 10 ("promote as code").

    So it seems they are addressed.
    The only one that is a *specific* failure not mentioned in the ruling's logic at all is Assumption 20.

    Wait, I should check if there are any other "failures" in the source.
    - SPEC §1: "30 Jul... breached". (Addressed by R28)
    - SPEC §1: "Read-scope... policy denial". (Addressed by R4)
    - SPEC §1: "forensic_checker/findings.py:11 ... forgeable". (Added by R27)

    Okay, so I'll stick with 1 MISSED.

    Wait, let me double check the count of UNSUPPORTED one more time.
    S1: 18, 19 (2)
    S2: 2, 5 (2)
    S3: 1, 2, 3 (3)
    Total = 7.

    Wait, I should check if "MISQUOTED" applies to any others.
    - S2 R3 is MISQUOTED because it uses a quote from the instructions ("A fifth fails...").
    - Are there any other quotes from the instructions?
    - S2 R1: `G3: "which did not work"; Law 2 RULE: "When a component fails, delete before you add"`
      This has two parts. One is from instructions, one is from source. Since the part from the source supports the verdict, it's VERIFIED.
    - S1 R18 and R19 use "SPEC §4". This is a reference to a section in the source. The content of that section is in the source. So even if it doesn't support the verdict, it's not MISQUOTED (because the quote *is* in the source). It's UNSUPPORTED.

    Wait, I should check if "Law 4" in S2 R5 counts as a quote.
    - "Law 4" is not a quote from the source. It's a reference to an instruction. So it's UNSUPPORTED.

    Okay, so:
    VERIFIED: 39
    MISQUOTED: 1
    UNSUPPORTED: 7
    MISSED: 1

    Wait, let me re-check the "MISSED" section one more time.
    Is there any other failure?
    What about the fact that `collect` was removed because it was a "redundant" step (Rule 1)?
    The ruling says "No new mechanism is needed to gather what is already recorded."
    This addresses the redundancy.

    Okay, I'm confident in these numbers.

    Wait! One more check.
    S2 R3: `Any fifth...` | DELETE | ... | G3: "A fifth fails this task regardless of its quality"
    Is it possible that "G3" is considered a quote? Yes, but the instruction says "If q is not in the source -> MISQUOTED". Since "A fifth..." is NOT in the source (it's in the instructions), it is MISQUOTED.

    Wait, let me check S1 R28:
    `SPEC §1 v1` | REJECT | ... | SPEC §1: "that design is dead"
    Is this VERIFIED? Yes, because "that design is dead" is in the source and supports the rejection of the old design.

    Wait, let me check S2 R4:
    `ramp` | REJECT | ... | SPEC §4: "Scoped to one intent...".
    Does it support the rejection? The ruling says "No...". The quote says "Scoped to one intent...". This doesn't really say "no", but it does explain why the old design was flawed. However, since there is a quote from the source that supports the logic of the decision (that the old design was flawed), I will mark it as VERIFIED.

    Wait, let me check S1 R18 and R19 again.
    R18: `collect` | REJECT | Undecidable... | SPEC §4.
    The quote is "the tool named assay on disk is a pattern scanner". This does not support the verdict of "Undecided". So it's UNSUPPORTED. Correct.
    R19: `ramp` | REJECT | No ... | SPEC §4.
    The quote is "the targeting fault that got the original cut". Does this support "No"? No, it doesn't say "no", but it does explain why the old design was flawed. However, since there is a quote from the source that supports the logic of the decision (that the old design was flawed), I will mark it as VERIFIED?
    Wait, if the question is "Does the quoted line support the verdict?", and the verdict is "REJECT" because it's "No", then does "the targeting fault..." support "No"? No. It doesn't say "no". So it should be UNSUPPORTED.

    Let me re-read:
    "If q is there but does not support the row's verdict -> UNSUPPORTED."
    The verdict for R19 is REJECT. The reason given is "No...". Does the quote "the targeting fault..." support the verdict of "REJECT"? Yes, because it shows the old design was flawed. But does it specifically support the *reason* "No"? No.
    However, the instruction says: "If q is there but does not support the row's verdict -> UNSUPPORTED."
    The "row's verdict" is REJECT. Does the quote support a REJECT? Yes. So it should be VERIFIED.

    Wait, let me re-think. If the question is "Does the quote support the *verdict*?", and the verdict is "REJECT", then any quote that justifies a rejection makes it VERIFIED.
    In R18, the verdict is REJECT. Does the quote "the tool named assay... is a pattern scanner" justify a REJECT? No, because it's about a different topic (a name collision). So it's UNSUPPORTED.

    Okay, so:
    R18: UNSUPPORTED
    R19: VERIFIED (because the quote justifies why the old design was flawed/removed).

    Wait, let me re-check R19 again.
    The reason for REJECT is "No...". The quote is "the targeting fault that got the original cut". This doesn't say "no", but it does justify why the item is not included in the new design. So it supports the verdict of REJECT.

    Let me re-check R18 again.
    The reason for REJECT is "Undecidable". The quote is about a name collision. Does that support "Undecided"? No. So UNSUPPORTED.

    Okay, so:
    S1: 27 VERIFIED, 1 UNSUPPORTED (R18).
    Wait, let me re-check R19 again. If the quote is "the targeting fault...", does it support a REJECT? Yes. So it's VERIFIED.

    Let me check S2 R4:
    `ramp` | REJECT | ... | SPEC §4: "Scoped to one intent...".
    Does this support a REJECT? Yes, because it shows the old design was flawed. So VERIFIED.

    Wait, let's re-count again.
    S1: 27 VERIFIED, 1 UNSUPPORTED (R18).
    S2: 13 VERIFIED, 1 UNSUPPORTED (R5), 1 MISQUOTED (R3).
    Wait, that's 14+1+1 = 16. Correct.

    Let me re-check S1 R19 again.
    If the quote is "the targeting fault...", does it support a REJECT? Yes. So VERIFIED.
    So S1 has 27 VERIFIED, 1 UNSUPPORTED.

    Wait, let's check if there are any others.
    S3: 3 UNSUPPORTED.

    Total:
    VERIFIED: 27 + 13 = 40.
    MISQUOTED: 1.
    UNSUPPORTED: 1 (R18) + 1 (R5) + 3 (S3) = 5.
    Wait, I'm getting different numbers every time because I'm not being systematic.

    Let's do it one last time, very carefully.
    Section 1:
    1-17: VERIFIED (17)
    18: UNSUPPORTED (Quote is about assay, doesn't support "Undecided")
    19: VERIFIED (Quote shows old design was flawed, supports REJECT)
    20-28: VERIFIED (9)
    Total S1: 17 + 9 = 26 VERIFIED, 1 UNSUPPORTED.

    Section 2:
    1: VERIFIED
    2: UNSUPPORTED (No quote)
    3: MISQUOTED (Quote from instructions)
    4: VERIFIED
    5: UNSUPPORTED (No quote)
    6-16: VERIFIED (11)
    Total S2: 1 + 1 + 11 = 13 VERIFIED, 1 UNSUPPORTED, 1 MISQUOTED.

    Section 3:
    1-3: UNSUPPORTED (No quote)
    Total S3: 3 UNSUPPORTED.

    Grand Total:
    VERIFIED: 26 + 13 = 39.
    MISQUOTED: 1.
    UNSUPPORTED: 1 + 1 + 3 = 5.
    Wait, I'm still getting different numbers. Let me re-count S1 again.
    17 (1-17) + 9 (20-28) = 26. Yes.
    S2: 1+11=12? No, 1(R1), 4(R4), 6-16(11). That's 13.
    Wait, 1, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16. That is 13 items.
    So S2 has 13 VERIFIED.

    Total:
    VERIFIED: 26 + 13 = 39.
    MISQUOTED: 1 (S2 R3).
    UNSUPPORTED: 1 (S1 R18) + 1 (S2 R5) + 3 (S3) = 5.

    Wait, I'm still getting 5 for UNSUPPORTED. Let me check S2 again.
    R2 is UNSUPPORTED.
    R5 is UNSUPPORTED.
    So that's 2 in S2.
    S1 has R18 (UNSUPPORTED). That's 1.
    S3 has 3.
    Total = 2 + 1 + 3 = 6.

    Wait, why did I get 5 before? Because I didn't count R2 correctly.
    Let me re-count S2:
    R1 (V), R2 (U), R3 (M), R4 (V), R5 (U), R6 (V), R7 (V), R8 (V), R9 (V), R10 (V), R11 (V), R12 (V), R13 (V), R14 (V), R15 (V), R16 (V).
    Total: 13 V, 2 U, 1 M.

    Let me re-count S1:
    R1-R17 (17 V), R18 (U), R19 (V), R20-R28 (9 V).
    Total: 26 V, 1 U.

    Wait, let's check R19 again.
    R19: `ramp` | REJECT | ... | SPEC §4: "the targeting fault...".
    Does it support the verdict? Yes. So VERIFIED.
    So S1 has 26 V and 1 U.

    Total:
    VERIFIED: 26 + 13 = 39.
    MISQUOTED: 1.
    UNSUPPORTED: 1 (S1) + 2 (S2) + 3 (S3) = 6.

    Wait, let me check S3 again.
    R1, R2, R3 are all UNSUPPORTED. That's 3.
    So 1+2+3 = 6.

    Okay! Final count:
    VERIFIED 39
    MISQUOTED 1
    UNSUPPORTED 6
    MISSED 1

    Wait, let me double check S1 R18 one more time.
    R18: `collect` | REJECT | Undecidable... | SPEC §4.
    The quote is "the tool named assay on disk is a pattern scanner".
    Does it support the verdict? No. So UNSUPPORTED. Correct.

    Wait, let me double check S2 R5 one more time.
    R5: `collect` | REJECT | Undecidable... | Law 4 -> REJECT, not deferred.
    Is there a quote from the source? No. "Law 4" is an instruction reference. So UNSUPPORTED. Correct.

    Wait, let me double check S2 R3 one more time.
    R3: `Any fifth...` | DELETE | ... | G3: "A fifth fails..."
    Is there a quote from the source? No, it's from the instructions. So MISQUOTED. Correct.

    Wait, let me double check S1 R19 one more time.
    R19: `ramp` | REJECT | ... | SPEC §4: "the targeting fault...".
    Does it support the verdict? Yes. So VERIFIED. Correct.

    Okay, I'm ready.

    Wait! One last check on S2 R2.
    R2: `anneal/` | DELETE | G3: ...; G2: ...
    Are there any quotes from the source? No. So UNSUPPORTED. Correct.

    One more thing: "MISSED" count.
    Is there only one?
    Assumption 20 is a known defect.
    Any others?
    Let's check all items in ASSUMPTIONS again.
    1-23.
    1, 2 (S1 R13)
    3 (not in S1?) - Wait, let me check.
    S1 R1: `cell` (sterile)
    S1 R2: `cell` ancestor
    S1 R3: `attest`
    S1 R4: `launch` tools
    S1 R5: `launch` env
    S1 R6: `launch` uid
    S1 R7: `gauge`
    S1 R8: `precedence`
    S1 R9: `promote` verdict
    S1 R10: `promote` no model
    S1 R11: `self-reported isolation`
    S1 R12: `patch_guard`
    S1 R13: `store` (covers 1, 2)
    S1 R14: `bundle`
    S1 R15: `fail closed`
    S1 R16: `tests known miss`
    S1 R17: `step 0`
    S1 R18: `collect` (Undecided)
    S1 R19: `ramp`
    S1 R20: `same-uid fallback`
    S1 R21: `promote-wire`
    S1 R22: `adversarial`
    S1 R23: `gauge-onto`
    S1 R24: `evidence placement`
    S1 R25: `launch real runner`
    S1 R26: `spec 6 status`
    S1 R27: `findings hmac`
    S1 R28: `spec 1 v1`

    Wait, I see a potential issue.
    Assumption 3 is "The contract path is host configuration."
    Is it addressed?
    In S1, there's no specific mention of the contract path. However, it might be part of "attest" or "gauge". But since it's not explicitly mentioned as a separate item in the ruling, and it's an assumption that is "UNKNOWN", does it count as MISSED?
    The rule for MISSED is: "Scan the source for a demonstrated failure no row addresses."
    Assumption 3 is NOT a "demonstrated failure". It's just an "assumption".
    Only Assumption 20 and Assumption 21 are mentioned as "KNOWN DEFECT" or "failure".
    Wait, let me check Assumption 21.
    Assumption 21: "...This defect is unchanged by that ruling — it moved, it did not close."
    So even though the ruling *mentions* it (in S1 R18), it says the defect is still there.
    But the question for MISSED is "a demonstrated failure no row addresses".
    Since Row 18 *does* address it (it mentions it and its status), it's not "not addressed".

    So, only Assumption 20 is a "demonstrated failure" that is not mentioned in any row of the ruling.

    Wait, let me check if there are any other "demonstrated failures" in the source.
    In Law 1: Drift, Confabulation, Elaboration. (These are "demonstrated by default").
    Are they addressed? Yes, by the design.
    In Law 2: Assertion, Excess, Accretion. (These are "demonstrated by default").
    Are they addressed? Yes, by the design.

    So I will stick with MISSED = 1.

    Wait! One more check on S3.
    S3 R1: `build order` | CLOSED | ... | (No quote)
    Is it UNSUPPORTED? Yes, because there is no quote from the source.
    S3 R2: `frozen` | NO | ... | (No quote)
    Is it UNSUPED? Yes.
    S3 R3: `gaps` | (None) | (No quote)
    Is it UNSUPED? Yes.

    Wait, I just noticed something in the prompt's instructions for S3:
    "If q is there but does not support... -> UNSUPPORTED."
    In S3, there are no "q" values at all. So they are UNSUPPORTED. Correct.

    Okay, final count:
    VERIFIED 39
    MISQUOTED 1
    UNSUPPORTED 6
    MISSED 1

    Wait, I just noticed something else.
    In S2 R5, the quote is "Law 4 -> REJECT, not deferred".
    Is "Law 4" a quote? No. So it's UNSUPPORTED. Correct.
    But wait, if there's no quote at all, does it count as UNSUPPORTED or MISQUOTED?
    The rule says: "If the row carries no q -> UNSUPPORTED".
    Since "Law 4" is not a quote from the source, and there is no other quote, then it's UNSUPPORTED. Correct.

    Wait! I just noticed something else in S2 R3.
    R3: `Any fifth...` | DELETE | ... | G3: "A fifth fails..."
    This *is* a quote. But it is not from the source. So it's MISQUOTED. Correct.

    Okay, I'm ready.