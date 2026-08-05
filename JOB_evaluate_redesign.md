# JOB — RULE THE BLACKSMITH REDESIGN UNDER LAW 1

## AIM

Every row of the ruling proposes a change. Rule each one APPROVE or REJECT.
Do not redesign it, extend it, repair it, or agree with it. Whether its
citations are accurate is a different job and is not asked here.

---

## PROCEDURE

```
FOR EACH row in the ruling's tables:
    Δ = the change the row proposes
    F = the failure it claims Δ addresses.
        For a removal, F is the failure the existing thing causes.

    IF the row names no F           → REJECT. Complexity without purpose.
    IF F is asserted, assumed or
       UNKNOWN in the sources       → REJECT. State what the source shows.

    ELSE test Δ against all four:
       SIMPLE  a new role, a new step, or a control duplicating one there?
       ROBUST  is the boundary against F direct, or does it rest on an
               assumption about how something behaves?
       LEAN    is Δ the smallest mechanism that blocks F?
       FAST    deterministic, no new overhead?

    IF any of the four fails        → REJECT. Name which.
    IF the complexity of Δ exceeds
       the criticality of F         → REJECT.
    ELSE                            → APPROVE

FOR EACH step in the ruling's build order, under Law 3:
    SINGLE   is one thing open at this step, or several?
    ORDERED  does it depend on a decision not yet made?
    Either fails                    → REJECT.

THEN ONCE:
    NAME any change the ruling makes that no row rules. Do not rule it.
```

REJECT is the default. Every verdict quotes the pasted line that shows F; no
quote is a REJECT.

---

## GIVEN — you cannot check these, and they are not open to ruling

```
G1  The ruling was produced by a session holding a full tool set — bash, file
    edit, memory read/write, browser, Gmail. It was not the bound venue its
    own prompt required. Its content is a claim, never a fact to inherit.

G2  The ruling cites "Law 4" twice. There is no Law 4. Do not report it, and
    do not treat a fourth Law as existing.

G3  The CORRECTION block at the top of the ruling was appended afterwards. It
    is not part of the ruling. Do not rule it.

G4  A row's citation may be wrong. That is the other job's finding, not
    yours, and it does not change your verdict. Rule the change, not the
    footnote.
```

---

## OUTPUT

```
TOOLS HELD: <none, or name any you hold>

## 1. ADDITIONS — ruling section 1
| Δ as ruled | F it claims | Which of SIMPLE/ROBUST/LEAN/FAST fails | APPROVE / REJECT | Quote showing F |

## 2. REMOVALS — ruling section 2
| Δ as ruled | F the existing thing causes | APPROVE / REJECT | Quote showing F |

## 3. BUILD ORDER — ruling section 3
| Step | SINGLE | ORDERED | APPROVE / REJECT | Quote |

## 4. UNRULED
| Change the ruling makes that no row rules | Source line |

## 5. COUNTS
Write APPROVE, REJECT and UNRULED as numbers, then the row count of
sections 1–3. The first two must sum to it.
```

A Quote column carries a quote and nothing else. A verdict written inside one
is not a verdict.
