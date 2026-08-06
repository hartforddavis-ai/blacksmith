"""Synthetic packets for the off-board task test. Generic filler only.

Nothing of ours goes into a free platform, so these are built from invented
weather-station prose and invented observation rows. The task wording is
copied verbatim from ramp.py.

    python3.12 make_packets.py

a  8 markers, no decoys, ~500 tok. Faithful replica of the local rung.
b  5 markers, no decoys, ~500 tok. Control — catches a model repeating a's
   answer instead of counting.
c  11 markers plus near-miss lines, ~500 tok. Precision. Every decoy fails the
   stated rule literally, so the ground truth stays unambiguous.
d  8 markers, no decoys, ~2,000 tok.
e  8 markers, no decoys, ~8,000 tok. Does the task survive scale.
"""
import pathlib

CHARS_PER_TOKEN = 4

PROSE = """The station records air temperature once every ten minutes.
Readings are written to a rolling file and rotated at midnight local time.
A reading that arrives out of order is kept, not discarded, and flagged.
Wind speed is sampled at one hertz and averaged over the reporting interval.
The gust value is the highest single sample within that same interval.
Humidity is measured by a capacitive element mounted inside the screen.
The screen is a louvred enclosure painted white to limit radiative heating.
Barometric pressure is corrected to sea level using the station elevation.
Elevation is surveyed once at installation and stored in the config file.
Rainfall is counted by a tipping bucket with a nominal resolution.
Each tip is timestamped so that intensity can be derived after the fact.
The bucket is inspected quarterly for debris and for insect nests.
Solar radiation is reported in watts per square metre over the interval.
The pyranometer dome is cleaned on the same schedule as the bucket.
Soil temperature probes sit at three depths below the undisturbed surface.
Depths are recorded in centimetres and are not adjusted after installation.
Battery voltage is logged alongside every observation for later diagnosis.
A voltage below the configured floor raises a maintenance flag in the record.
The logger keeps its own clock and disciplines it from a network time source.
If the time source is unreachable the logger continues on its internal clock.
Drift accumulated during an outage is reported but never silently corrected.
Data are transmitted in batches when the link is available and queued when not.
The queue is bounded and the oldest unsent batch is dropped when it overflows.
A dropped batch is counted so that gaps in the archive can be explained.
Quality control runs on receipt and marks values that fail a range check.
Range checks are seasonal and are held in a table separate from the code.
A value that fails a check is retained in the archive with its flag attached.
Nothing is deleted from the archive once written, only annotated.
Monthly summaries are computed from flagged data with the flags respected.
The summary states how many observations were excluded and on what grounds.
Station metadata changes are versioned with the date the change took effect.
A sensor swap is a metadata change and is recorded as one.
Calibration certificates are stored with the metadata and never in the archive.
The archive is copied nightly to a second site on separate power.
Restores are exercised twice a year against the second site, not the first.
An exercise that is not observed by a second person is not counted.
Retention is indefinite for observations and five years for diagnostics.
Diagnostics include voltage, clock discipline, and link availability.
The distinction matters because diagnostics are large and observations are not.
Access to the archive is read-only except through the ingest path.
The ingest path is the only writer and it is single-threaded by design.
Concurrency was tried once and produced interleaved records under load.
The single writer has held for eleven years without an ordering fault.
Reports are generated from the archive and never from the live logger.
A report that disagrees with the archive is a fault in the report."""

TASK = (
    "\n\n---\n\nSome lines above consist only of a tag: two open square "
    "brackets, the word MARKER in capitals, a number, then two close "
    "square brackets.\n\nCount those lines. Reply with one line and "
    "nothing else, in this form, with the number substituted:\n\n"
    "COUNT: 42\n")

# Each fails the stated rule literally — single brackets, lowercase, no number,
# prose. None is a line consisting only of the described tag.
DECOYS = ["[MARKER 9]", "[[marker 3]]", "[[MARKER]]",
          "The technician left a MARKER on the enclosure door."]


def filler(n_chars):
    """Prose first, then invented observation rows until the budget is met.

    The prose is cut to the budget rather than emitted whole, so a small rung
    is actually small. Emitting all of it made the ~500 tok packet 3,641 chars
    against the real rung's 2,367 — a size replica of the wrong size.
    """
    lines, used = [], 0
    for line in PROSE.split("\n"):
        if used >= n_chars:
            break
        lines.append(line)
        used += len(line) + 1
    i = 0
    while used < n_chars:
        i += 1
        line = (f"Observation {i:05d}: air {8 + (i % 210) / 10:.1f} C, "
                f"wind {(i % 87) / 10:.1f} m/s, pressure "
                f"{995 + (i % 380) / 10:.1f} hPa, battery "
                f"{11.4 + (i % 26) / 10:.1f} V.")
        lines.append(line)
        used += len(line) + 1
    return lines


def build(markers, tokens, decoys=False):
    lines = filler(tokens * CHARS_PER_TOKEN)
    every = max(1, len(lines) // markers)
    out, planted, dropped = [], 0, 0
    for i, line in enumerate(lines):
        if i % every == 0 and planted < markers:
            planted += 1
            out.append(f"[[MARKER {planted}]]")
        if decoys and dropped < len(DECOYS) and i and i % 9 == 0:
            out.append(DECOYS[dropped])
            dropped += 1
        out.append(line)
    return "\n".join(out) + TASK, planted, dropped


here = pathlib.Path(__file__).parent / "packets"
here.mkdir(exist_ok=True)

key = []
for name, markers, tokens, decoys in (("a", 8, 500, False),
                                      ("b", 5, 500, False),
                                      ("c", 11, 500, True),
                                      ("d", 8, 2_000, False),
                                      ("e", 8, 8_000, False)):
    text, planted, dropped = build(markers, tokens, decoys)
    (here / f"packet_{name}.txt").write_text(text, encoding="utf-8")
    key.append(f"packet_{name}.txt   COUNT: {planted:>2}   "
               f"({len(text):>6,} chars, ~{tokens:,} tok, {dropped} decoys)")
    print(f"packet_{name}: {planted} markers, {dropped} decoys, {len(text):,} chars")

(here / "ANSWERS.txt").write_text(
    "GROUND TRUTH — do not open until every model has replied.\n"
    "Counted by exact line match, not by eye. Re-check any time with:\n"
    "    grep -c -E '^\\[\\[MARKER [0-9]+\\]\\]$' packet_a.txt\n\n"
    + "\n".join(key) + "\n", encoding="utf-8")
print("wrote ANSWERS.txt")
