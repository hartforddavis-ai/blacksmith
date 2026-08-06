"""Concatenate the folder into ALL_JOBS.md, in the order the README recommends.

    python3.12 export_all.py

ALL_JOBS.md is a copy for carrying on a phone, not a source. Edit the separate
files and re-run this; editing ALL_JOBS.md directly loses the change on the next
export. Re-run it after ANY edit to a job or to the README, or the copy quietly
disagrees with the originals — which is the failure this project keeps finding
in other forms.

The packets are deliberately not included. They must be pasted whole and
unaltered from packets/, and burying them in a 58 KB file invites a partial
copy-paste, which would silently change the task being measured.
"""
import pathlib

ORDER = [
    "README.md",
    # Day 1 — is the instrument sound
    "JOB_2_packet_test.md", "JOB_3_sampling_params.md",
    # Day 2 — is the runner using the wrong door
    "JOB_4_generate_vs_chat.md", "JOB_5_known_issues.md",
    # Day 3 — is the job we are asking even possible
    "JOB_10_verification_ceiling.md", "JOB_11_retrieval_vs_length.md",
    # Day 4 — the settings on the live server
    "JOB_1_context_shift.md", "JOB_6_thinking_budget.md",
    "JOB_12_quantisation_and_format.md",
    # If there is time left
    "JOB_7_kv_quantisation.md", "JOB_13_determinism.md",
    "JOB_14_effective_context.md", "JOB_8_scale_test.md",
    "JOB_9_model_shortlist.md",
    "RESULTS.md",
]

HEAD = """# ALL JOBS — one file

Everything in this folder concatenated in the recommended order, for carrying on
a phone. This is a COPY. The separate files are the originals, and this one does
not update itself — rebuild it with `python3.12 export_all.py` after any edit.

The packets are NOT in here. Paste them whole and unaltered from
`packets/packet_a.txt` and the rest; a partial paste changes the task being
measured and nothing will tell you it happened.
"""


def main():
    here = pathlib.Path(__file__).parent
    missing = [n for n in ORDER if not (here / n).exists()]
    if missing:
        raise SystemExit("MISSING: " + ", ".join(missing))

    # Anything not in ORDER is reported rather than silently dropped — a job
    # written and never added to the list would be invisible in the copy.
    listed = set(ORDER) | {"ALL_JOBS.md", "export_all.py", "make_packets.py"}
    stray = sorted(p.name for p in here.glob("*.md") if p.name not in listed)
    if stray:
        print("NOT IN THE EXPORT (add them to ORDER):", ", ".join(stray))

    parts = [HEAD]
    for name in ORDER:
        parts.append("\n\n" + "=" * 72 + f"\nFILE: {name}\n" + "=" * 72 + "\n")
        parts.append((here / name).read_text(encoding="utf-8"))

    out = here / "ALL_JOBS.md"
    out.write_text("".join(parts), encoding="utf-8")
    print(f"{out.name} — {len(ORDER)} files, {out.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
