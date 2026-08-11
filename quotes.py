"""quotes — check a bound reply's quotes against the bytes it was given.

No security claim is made here, and no judgement of a review's content. This
answers one question per row: does the quote exist in the material that was
pasted? A reply that quotes something never sent has fabricated it, and that
is the failure this closes — qwen's 5 Aug verify reply carried two of them
(`FAILURE_LOG.md`), and the only thing that caught them was the operator
grepping by hand.

Only VERIFIED rows are checked. K3 says a positive verdict quotes the line
supporting it, so a VERIFIED row is the one place the reply commits to bytes
it claims to hold. Negative verdicts commit to nothing and are left alone.

Two ways a row fails, both taken from the real artifact:

    a VERIFIED row carrying no quote at all — K3 requires one, so its absence
    is the finding, not a reason to skip the row.

    a quote whose elided halves are real but come from different places. The
    reply's `"Step 0 ... OPEN"` is the case: `Step 0` and `OPEN` both occur in
    SPEC.md, hundreds of lines apart, and §9 contains neither the pairing nor
    the word OPEN. Checking segments independently passes this fabrication.

So an elision is treated as a gap inside one passage, not a licence to stitch:
the whole quote must match a contiguous window of a single source, segments in
order, gap bounded. That is one rule rather than two, and it is what makes the
check refuse the artifact it was written against.

This is deliberately NOT the old grounding gate. That one asked the model to
count line numbers, and Flash Lite failed it twice for being bad at counting
rather than for lying — a false negative on the property being measured. Here
the model is asked for nothing it does not already produce.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import build_paste

# An elision inside a quote: the reply writes `...` or a unicode ellipsis.
ELISION = re.compile(r"\s*(?:\.\.\.|…)\s*")

# Double-quoted spans in an evidence cell. Non-greedy, so adjacent quotes on
# one line stay separate rather than swallowing the text between them.
QUOTED = re.compile(r'"([^"]+)"')

# Markdown the model adds around quoted text; the source carries its own, and
# the two do not have to agree for the bytes to be the same bytes.
EMPHASIS = re.compile(r"[*`_]+")

# How far apart an elision may span inside one passage. An elision skips a
# clause or a sentence; it does not reach across a document. This bound is the
# whole mechanism — proven by widening it, which makes the 5 Aug fabrication
# pass again. A minimum segment length was tried alongside it and cut: it
# refused nothing the gap bound did not already refuse.
MAX_GAP = 400

VERDICT = "VERIFIED"

# K1 in KERNEL_bound.md: "DECLARE every tool you hold. First line, before
# anything else." Every real reply opens with this line; wording varies
# ("TOOLS HELD: none" vs "TOOLS HELD: <none>") but the phrase does not — it
# is fixed KERNEL text, not SOURCE, so checking for it cannot leak into what
# a VERIFIED row is judged against (!34: a cell where nothing ran is
# trivially delta-free upstream in attest.compare; this is the same gap
# closed for the reply itself — a reply with no first line to match never
# engaged with the protocol at all).
ENGAGEMENT_MARKER = "TOOLS HELD"


class QuoteError(ValueError):
    """The reply could not be read as a table of ruled rows."""


def normalise(text: str) -> str:
    """Strip emphasis and collapse whitespace, on both sides of the compare.

    Line wrapping and bold markers are the transport's, not the author's. What
    survives is the sequence of words, which is what a quote actually claims.
    """
    return re.sub(r"\s+", " ", EMPHASIS.sub("", text)).strip()


def sources(job: str = "verify") -> dict[str, str]:
    """Everything the paste carried, normalised, keyed by label.

    Read from `build_paste` rather than listed here, so the checker cannot
    drift from the assembler: a quote checked against material the model never
    saw proves nothing.

    KERNEL and JOB are in it because `build_paste.build` pastes them and
    `SOURCES` does not name them. Checking against `SOURCES` alone reported the
    reply's quote of the job's own GIVENs as fabricated — a false accusation
    against a reviewer quoting what it was handed. Found by running this
    against the real 5 Aug reply, not by reading it.
    """
    spec = build_paste.JOBS[job]
    paths = [("KERNEL", build_paste.KERNEL), ("JOB", spec["job"])]
    paths += spec["sources"]
    return {label: normalise(path.read_text(encoding="utf-8"))
            for label, path in paths}


def rows(reply: str) -> list[tuple[int, list[str], bool]]:
    """Every markdown table row, as (line number, cells, is_verified).

    Returns all ruled rows, not just the positive ones, so a caller can tell
    "no row claimed VERIFIED" from "there were no rows" — the first is an
    ordinary reply, the second is a reply that did not arrive.

    The evidence cell is the last one: the tables differ in width between
    sections of the same reply, and the last column is evidence in all of
    them. Keying on position from the left would break on section 3.
    """
    found = []
    for number, line in enumerate(reply.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 2 or set("".join(cells)) <= set("-: "):
            continue
        verified = VERDICT in [normalise(c).upper() for c in cells[:-1]]
        found.append((number, cells, verified))
    return found


def occurs(quote: str, corpus: str) -> bool:
    """Does this quote, elisions and all, match one contiguous run of `corpus`?

    Segments must appear in order with at most `MAX_GAP` between them. A quote
    with no elision is a plain substring test, which is the same rule with one
    segment.
    """
    segments = [s for s in ELISION.split(normalise(quote)) if s]
    if not segments:
        return False
    pattern = f".{{0,{MAX_GAP}}}".join(re.escape(s) for s in segments)
    return re.search(pattern, corpus, re.DOTALL) is not None


def engaged(reply_text: str) -> bool:
    """Does the reply's first non-blank line carry K1's required declaration?

    An inert cell — nothing ran, or the model never received the KERNEL — has
    no such line. This is a structural gate, same level as NO_ROWS below, and
    checked before any row is read: it answers "did this reply engage with
    the protocol at all", not "are its claims correct".
    """
    for line in reply_text.splitlines():
        stripped = line.strip()
        if stripped:
            # Same normalise() every other match in this module trusts —
            # markdown emphasis is the transport's, not the model's, and a
            # bolded "**TOOLS** **HELD**" must still match.
            return ENGAGEMENT_MARKER in normalise(stripped)
    return False


def check(reply_text: str, corpora: dict[str, str] | None = None,
          job: str = "verify") -> list[dict]:
    """Rule every VERIFIED row. Returns one finding per row that fails.

    An empty list means every VERIFIED row quoted something the model was
    actually given. It does not mean the review is right.

    A reply with no ruled rows at all is refused rather than passed. Nothing
    was compared, and a check that reports clean because it found nothing to
    check is not a check — the same defect this tree fixed in `tests_pass` on
    6 Aug, rebuilt here hours later and caught by running it on a header-only
    reply.
    """
    corpora = sources(job) if corpora is None else corpora
    if not engaged(reply_text):
        return [{"line": 0, "reason": "NO_ENGAGEMENT", "quote": "",
                 "detail": "first line does not carry K1's required "
                           f"{ENGAGEMENT_MARKER!r} declaration; nothing ran "
                           "or nothing was received"}]
    ruled = rows(reply_text)
    if not ruled:
        return [{"line": 0, "reason": "NO_ROWS", "quote": "",
                 "detail": "no ruled rows found; nothing was compared"}]
    findings = []
    for number, cells, verified in ruled:
        if not verified:
            continue
        evidence = cells[-1]
        quotes = QUOTED.findall(evidence)
        if not quotes:
            findings.append({"line": number, "reason": "NO_QUOTE",
                             "detail": "VERIFIED row carries no quoted span; "
                                       "K3 requires one",
                             "quote": ""})
            continue
        for quote in quotes:
            if not any(occurs(quote, c) for c in corpora.values()):
                findings.append({"line": number, "reason": "NOT_IN_SOURCE",
                                 "detail": "no source contains this as one "
                                           "passage",
                                 "quote": normalise(quote)})
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="quotes",
        description="Check a bound reply's VERIFIED rows against the paste.")
    parser.add_argument("reply", type=Path, help="a file under runs/")
    parser.add_argument("--job", default="verify", choices=sorted(build_paste.JOBS),
                        help="which paste this reply answered")
    args = parser.parse_args(argv)

    if not args.reply.is_file():
        print(f"no such reply: {args.reply}", file=sys.stderr)
        return 2

    findings = check(args.reply.read_text(encoding="utf-8"), job=args.job)
    if not findings:
        print(f"quotes clean: every {VERDICT} row quotes the pasted material")
        return 0
    for finding in findings:
        print(f"{args.reply.name}:{finding['line']}  {finding['reason']}  "
              f"{finding['detail']}")
        if finding["quote"]:
            print(f"    {finding['quote']!r}")
    print(f"\n{len(findings)} finding(s). "
          f"A rejected review is discarded whole.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
