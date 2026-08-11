#!/usr/bin/env python3.12
"""What does the stream actually carry? Same call as occupant_bound, all fields kept.

Three calibration runs returned zero-character replies on a ~1,200-token payload.
`occupant_bound.run` keeps `chunk["response"]` and nothing else, so an empty
reply has two possible causes and the record cannot tell them apart:

    the model produced no answer                         — a model finding
    the model's output arrived under a different key     — a runner defect

This distinguishes them. It counts every key the stream uses and the characters
under each, and prints the done_reason the server gives. It does not change
occupant_bound; it reads the same endpoint the same way and keeps what that
module throws away.

    python3.12 calib/probe_fields.py
"""
import collections
import json
import pathlib
import time
import urllib.request

PASTE = pathlib.Path(__file__).parent / "PASTE_calib_true.md"
prompt = PASTE.read_text(encoding="utf-8")

req = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=json.dumps({
        "model": "qwen3.5:9b", "prompt": prompt, "stream": True,
        "options": {"temperature": 0},
    }).encode(),
    headers={"Content-Type": "application/json"},
)

chars = collections.Counter()
last = {}
start = time.monotonic()
n = 0

print(f"prompt {len(prompt):,} chars — same paste, same options, all fields kept",
      flush=True)
with urllib.request.urlopen(req, timeout=1800) as r:
    for line in r:
        chunk = json.loads(line)
        n += 1
        for k, v in chunk.items():
            if isinstance(v, str) and v:
                chars[k] += len(v)
        if chunk.get("done"):
            last = chunk
            break

print(f"\n{n:,} chunks in {time.monotonic() - start:,.1f}s")
print("\ncharacters carried, per field:")
for k, v in chars.most_common():
    print(f"    {k:<16} {v:>10,}")
if not chars:
    print("    (nothing — every chunk was empty)")

print("\nfinal chunk, non-text fields:")
for k, v in sorted(last.items()):
    if not isinstance(v, str) or len(v) < 80:
        print(f"    {k:<20} {v!r}")

print("\nVERDICT")
kept = chars.get("response", 0)
other = sum(v for k, v in chars.items() if k != "response")
if kept:
    print(f"    occupant_bound would keep {kept:,} chars — reply not empty.")
elif other:
    print(f"    RUNNER DEFECT. {other:,} chars arrived, none under 'response'.")
    print(f"    occupant_bound discards all of it and records an empty reply.")
else:
    print("    MODEL FINDING. The stream carried no text under any key.")
