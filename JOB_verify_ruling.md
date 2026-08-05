# JOB — VERIFY THE BLACKSMITH REDESIGN RULING

## AIM

Check every row of the ruling against the sources it cites. Do not redesign it,
improve it, extend it, or agree with it.

---

## PROCEDURE

```
FOR EACH row in the ruling's tables:
    q = the line the row quotes

    IF the row carries no q        → UNSUPPORTED
    IF q is not in the sources     → MISQUOTED. Give what the source says.
    IF q is there but does not
       support the row's verdict   → UNSUPPORTED. State what it does show.
    ELSE                           → VERIFIED

THEN ONCE:
    SCAN the sources for a demonstrated failure no row addresses → MISSED.
    Name it and its source line. Do not design for it.
```

`VERIFIED` means the quoted line exists and supports the verdict. It is never a
claim that any code works.

---

## GIVEN — you cannot check these, and they are not open to ruling

```
G1  The ruling was produced by a session holding a full tool set — bash, file
    edit, memory read/write, browser, Gmail. It was not the bound venue its
    own prompt required. Its content is a claim to verify, never a fact to
    inherit. Agreement is not the goal; grounding is.

G2  The ruling cites "Law 4" twice. There is no Law 4 — it means a check of
    the prompt that produced it. Corrected at source. Do not report it, and
    do not treat a fourth Law as existing.

G3  The CORRECTION block at the top of the ruling was appended afterwards. It
    is not part of the ruling and is not verified here.
```

---

## OUTPUT

```
TOOLS HELD: <none, or name any you hold>

## 1. DESIGN ROWS — ruling section 1
| Part as ruled | Ruled | VERIFIED / MISQUOTED / UNSUPPORTED | Evidence |

## 2. REMOVAL ROWS — ruling section 2
| Item as ruled | Ruled | VERIFIED / MISQUOTED / UNSUPPORTED | Evidence |

## 3. SECTIONS 3–5 — build order, frozen, gaps
| Claim | VERIFIED / MISQUOTED / UNSUPPORTED | Evidence |

## 4. MISSED
| Demonstrated failure no row addresses | Source line |

## 5. COUNTS
VERIFIED n · MISQUOTED n · UNSUPPORTED n · MISSED n
```
