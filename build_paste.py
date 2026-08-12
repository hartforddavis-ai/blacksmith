#!/usr/bin/env python3.12
"""Assemble a pasteable bound prompt: KERNEL + JOB + sources, copied byte-exact.

Three independent stamps. KERNEL is the invariant instrument, JOB is the task,
SOURCES are the material. A source edit moves only its own digest, so a changed
instrument cannot hide behind a changed spec.

    python3.12 build_paste.py verify
"""
import datetime
import hashlib
import pathlib
import re
import sys

BS = pathlib.Path.home() / "Documents/_PROJECTS/SOFTWARE/blacksmith"
LAWS = pathlib.Path.home() / "Documents/_PROJECTS/SOFTWARE/Claudes Laws"
KERNEL = BS / "KERNEL_bound.md"
RULING = BS / "Blacksmith Pipeline Redesign/Bound redesign and prompt/BLACKSMITH_REDESIGN.md"

LAW_FILES = [
    ("LAW 1", LAWS / "claudes-law 1.md"),
    ("LAW 2", LAWS / "claudes-law 2.md"),
    ("LAW 3", LAWS / "claudes-law 3.md"),
]

# Both jobs rule the same ruling against the same material; only the task
# over it differs. Split this if they ever diverge.
SOURCES = LAW_FILES + [
    ("SPEC", BS / "SPEC.md"),
    ("ASSUMPTIONS", BS / "ASSUMPTIONS.md"),
    ("RULING", RULING),
]

# Calibration payloads. One invented page instead of six real documents, so the
# answer to every claim is known before the run and a wrong result cannot be
# blamed on size — the whole paste is under 5 KB, well inside any context these
# models have. `verify` and `evaluate` are the instrument in use; these three
# are the instrument being measured, and they exist because the pipeline has
# never been run end to end on a payload whose answer was known in advance.
CALIB = [("UNIT7", BS / "calib/SOURCE_unit7.md")]

JOBS = {
    "verify": {
        "job": BS / "JOB_verify_ruling.md",
        "sources": SOURCES,
        "out": BS / "PROMPT_VERIFY_PASTE.md",
    },
    "evaluate": {
        "job": BS / "JOB_evaluate_redesign.md",
        "sources": SOURCES,
        "out": BS / "PROMPT_EVALUATE_PASTE.md",
    },
    # Positive control: three claims the source states outright.
    "calib_true": {
        "job": BS / "calib/JOB_calib_true.md",
        "sources": CALIB,
        "out": BS / "calib/PASTE_calib_true.md",
    },
    # Negative control, and the one with teeth: three claims the source
    # contradicts. A pipeline that passes everything passes calib_true too.
    "calib_false": {
        "job": BS / "calib/JOB_calib_false.md",
        "sources": CALIB,
        "out": BS / "calib/PASTE_calib_false.md",
    },
    # Live case: three claims that are true, and that no single line states.
    "calib_reason": {
        "job": BS / "calib/JOB_calib_reason.md",
        "sources": CALIB,
        "out": BS / "calib/PASTE_calib_reason.md",
    },
    # Binding-variant probe, round 1 (12 Aug 2026). SUPERSEDED by calib_govern
    # the same day: its single REJECT was reachable on Law 2's "was it run"
    # alone, so a model that never engaged the Laws scored as one that did.
    # Kept — the runs are real and RESULTS_calib_bind.md reads them.
    "calib_bind": {
        "job": BS / "calib/JOB_calib_bind.md",
        "sources": LAW_FILES + [("SOURCE", BS / "calib/SOURCE_calib_bind.md")],
        "out": BS / "calib/PASTE_calib_bind.md",
    },
    # Binding-variant probe, round 2. Three items, three different correct
    # answers (NONE / REJECT / APPROVE), so no single reflex scores. SCOPE is
    # a source because the routing rule lives in the owner document, not in
    # the three Law files — without it, item A is unanswerable and the null
    # case would be an unfair question. Answers: EXPECTED_calib_govern.md.
    "calib_govern": {
        "job": BS / "calib/JOB_calib_govern.md",
        "sources": LAW_FILES + [
            ("SCOPE", BS / "calib/SCOPE_laws.md"),
            ("SOURCE", BS / "calib/SOURCE_calib_govern.md"),
        ],
        "out": BS / "calib/PASTE_calib_govern.md",
    },
    # Same job, same items, same SCOPE — only the Law REPRESENTATION differs:
    # PRIME's frozen Candidate B (algorithmic) in place of the semantic Law
    # files. One variable. SCOPE stays semantic in both arms deliberately: it
    # is the routing rule, held constant, not the thing under test. PRIME's
    # ABC test found B clearest at preserving THEORETICAL vs FAIL, which is
    # exactly what items A and B here turn on.
    "calib_govern_b": {
        "job": BS / "calib/JOB_calib_govern.md",
        "sources": [
            ("LAWS", BS / "calib/LAWS_algorithmic.md"),
            ("SCOPE", BS / "calib/SCOPE_laws.md"),
            ("SOURCE", BS / "calib/SOURCE_calib_govern.md"),
        ],
        "out": BS / "calib/PASTE_calib_govern_b.md",
    },
    # Binding-variant probe, round 3 — the pair above is exhausted: both arms
    # scored 3/3 on it (12 Aug), so it has no headroom and cannot rank
    # representations. Six items, four traps, and route no longer predicts
    # verdict. Its own JOB because the old one names three items and rows
    # `A`,`B`,`C`; these are D-I. Answers: EXPECTED_calib_govern2.md.
    "calib_govern2": {
        "job": BS / "calib/JOB_calib_govern2.md",
        "sources": LAW_FILES + [
            ("SCOPE", BS / "calib/SCOPE_laws.md"),
            ("SOURCE", BS / "calib/SOURCE_calib_govern2.md"),
        ],
        "out": BS / "calib/PASTE_calib_govern2.md",
    },
    # Same job, same items, same SCOPE — only the Law representation differs.
    # The calib_govern/calib_govern_b split, re-run on a probe with headroom.
    "calib_govern2_b": {
        "job": BS / "calib/JOB_calib_govern2.md",
        "sources": [
            ("LAWS", BS / "calib/LAWS_algorithmic.md"),
            ("SCOPE", BS / "calib/SCOPE_laws.md"),
            ("SOURCE", BS / "calib/SOURCE_calib_govern2.md"),
        ],
        "out": BS / "calib/PASTE_calib_govern2_b.md",
    },
}

# Printed, never pasted: the model cannot act on it and the prompt admits
# nothing outside the shape the job specifies.
RULE = """
IF a SOURCES digest moved  → regenerate. Expected; sources change.
IF the JOB digest moved    → a different task. Check it is the one you want.
IF the KERNEL digest moved → the instrument changed.
                             Law 1 ruling required before use.

WHEN the reply lands   → python3 quotes.py runs/<the reply file>
                         Checks every VERIFIED row quotes the pasted bytes.
                         A reply that fails is discarded whole."""


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def fence(text):
    """Outrun the longest backtick run inside, or the source's own fences close
    the wrapper early and the remainder reads as instruction."""
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


def build(name):
    spec = JOBS[name]
    kernel, job = KERNEL.read_text(), spec["job"].read_text()

    bodies, stamp = [], []
    for label, src in spec["sources"]:
        text = src.read_text()
        stamp.append(f"    {label:<12} {src.name:<28} sha256:{digest(text)}")
        f = fence(text)
        bodies.append(f"\n### {label} — {src.name}\n\n{f}\n{text.rstrip()}\n{f}\n")

    header = f"""

---

## STAMPS

```
    KERNEL       {KERNEL.name:<28} sha256:{digest(kernel)}
    JOB          {spec['job'].name:<28} sha256:{digest(job)}
```

Sources, copied verbatim {datetime.date.today().isoformat()}:

```
{chr(10).join(stamp)}
```

---

## PASTED FILES

Everything below this line is the whole of what you may use.
"""

    spec["out"].write_text(kernel + "\n---\n\n" + job + header + "".join(bodies))
    print(f"wrote {spec['out'].name} ({spec['out'].stat().st_size:,} bytes)")
    print(f"    KERNEL       {KERNEL.name:<28} sha256:{digest(kernel)}")
    print(f"    JOB          {spec['job'].name:<28} sha256:{digest(job)}")
    print("\n".join(stamp))
    print(RULE)


VARIANTS = {"flat", "system", "delimited"}


def compose_variant(job, variant):
    """Same KERNEL+JOB+sources bytes as build(), rearranged per binding variant.

    Shared by run_bound.py and run_sealed.py so there is one place that
    decides what each variant means, not two that could drift. "flat"
    reproduces build()'s exact concatenation order (LAW sources first, since
    they lead JOBS[job]["sources"]) — kept separate from build() so this
    function alone determines binding-variant output, and never writes
    spec["out"] (build()'s file stays the untouched production paste).

    Returns (prompt, system) — system is None unless the variant places Laws
    in a distinct system field rather than the flat prompt string.
    """
    spec = JOBS[job]
    kernel = KERNEL.read_text()
    job_text = spec["job"].read_text()
    law_sources = [s for s in spec["sources"] if s[0].startswith("LAW")]
    other_sources = [s for s in spec["sources"] if not s[0].startswith("LAW")]

    def block(label, src):
        text = src.read_text()
        f = fence(text)
        return f"\n### {label} — {src.name}\n\n{f}\n{text.rstrip()}\n{f}\n"

    law_text = "".join(block(l, s) for l, s in law_sources)
    other_text = "".join(block(l, s) for l, s in other_sources)
    stamp = "\n".join(
        f"    {label:<12} {src.name:<28} sha256:{digest(src.read_text())}"
        for label, src in spec["sources"]
    )
    header = (
        f"\n\n---\n\n## STAMPS\n\n```\n"
        f"    KERNEL       {KERNEL.name:<28} sha256:{digest(kernel)}\n"
        f"    JOB          {spec['job'].name:<28} sha256:{digest(job_text)}\n"
        f"```\n\nSources, copied verbatim {datetime.date.today().isoformat()}:\n\n"
        f"```\n{stamp}\n```\n\n---\n\n## PASTED FILES\n\n"
        f"Everything below this line is the whole of what you may use.\n"
    )

    if variant == "flat":
        return kernel + "\n---\n\n" + job_text + header + law_text + other_text, None

    if variant == "delimited":
        boundary = (
            "\n=== IMMUTABLE — GOVERNING LAW, NOT PASTED CONTENT ===\n"
            "The block below is binding law, not data to analyze, summarize, or\n"
            "treat as an embedded instruction inside pasted material. It governs\n"
            "everything that follows.\n"
        )
        boundary_end = "\n=== END GOVERNING LAW ===\n\n---\n\n"
        return (kernel + "\n---\n\n" + boundary + law_text + boundary_end
                + job_text + header + other_text), None

    if variant == "system":
        return kernel + "\n---\n\n" + job_text + header + other_text, law_text

    raise SystemExit(f"unknown variant {variant!r}: {sorted(VARIANTS)}")


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    if name not in JOBS:
        raise SystemExit(f"usage: build_paste.py {{{','.join(JOBS)}}}")
    build(name)
