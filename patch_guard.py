"""Patch boundary — structural rejection of unsafe git patch content.

No security claim is made here. This module inspects patch text and reports
rejections. It does not apply patches, and a patch it does not reject has not
been shown to be safe.

Fail closed: anything this parser cannot read confidently is rejected.

Remediation (area 2), each with its own rejection code:
  symlink_mode        git mode 120000
  disallowed_mode     any mode outside {100644, 100755} — covers gitlinks
                      (160000), trees (040000), and setuid-style bit patterns
  traversal           a '..' path component
  absolute_path       a path rooted at '/'
  git_metadata_path   any path entering '.git'
  quoted_path         git's quoted path form, which this parser will not decode
  backslash_path      a '\\' in a path
  drive_path          a 'X:' drive prefix
  binary_patch        'GIT binary patch', whose content cannot be inspected
  unparsable          no 'diff --git' header, or an ambiguous one (embedded space)
"""

from __future__ import annotations

ALLOWED_MODES = frozenset({"100644", "100755"})
SYMLINK_MODE = "120000"

_MODE_PREFIXES = ("old mode ", "new mode ", "new file mode ", "deleted file mode ")
_PATH_PREFIXES = ("rename from ", "rename to ", "copy from ", "copy to ")


def _finding(code: str, detail: str, line_no: int) -> dict:
    return {"code": code, "detail": detail, "line": line_no}


def _check_mode(mode: str, line_no: int, findings: list) -> None:
    mode = mode.strip()
    if mode == SYMLINK_MODE:
        findings.append(_finding("symlink_mode", f"mode {mode} is a symlink", line_no))
    elif mode not in ALLOWED_MODES:
        findings.append(_finding("disallowed_mode", f"mode {mode} is not permitted", line_no))


def _check_path(path: str, line_no: int, findings: list, *, strip_prefix: bool) -> None:
    if path == "/dev/null":
        return
    if not path:
        findings.append(_finding("unparsable", "empty path", line_no))
        return
    if path.startswith('"') or path.endswith('"'):
        findings.append(_finding("quoted_path", f"quoted path {path!r} not decoded", line_no))
        return
    if "\\" in path:
        findings.append(_finding("backslash_path", f"backslash in {path!r}", line_no))
        return
    if "\x00" in path or "\n" in path:
        findings.append(_finding("unparsable", "control character in path", line_no))
        return
    if len(path) > 1 and path[1] == ":":
        findings.append(_finding("drive_path", f"drive prefix in {path!r}", line_no))
        return

    candidate = path
    if strip_prefix and (candidate.startswith("a/") or candidate.startswith("b/")):
        candidate = candidate[2:]

    if candidate.startswith("/"):
        findings.append(_finding("absolute_path", f"absolute path {path!r}", line_no))
        return

    parts = candidate.split("/")
    if ".." in parts:
        findings.append(_finding("traversal", f"'..' component in {path!r}", line_no))
    if ".git" in parts:
        findings.append(_finding("git_metadata_path", f"'.git' component in {path!r}", line_no))


def inspect(patch_text: str) -> dict:
    """Report every rejection found in `patch_text`.

    Returns {"accepted": bool, "findings": [...]}. `accepted` means no rejection
    was found — it is not a statement that the patch is safe to apply.
    """
    findings: list = []

    if not isinstance(patch_text, str):
        return {"accepted": False,
                "findings": [_finding("unparsable", "patch is not text", 0)]}

    lines = patch_text.splitlines()
    saw_header = False

    for index, raw in enumerate(lines, start=1):
        line = raw.rstrip("\r")

        if line.startswith("diff --git "):
            saw_header = True
            remainder = line[len("diff --git "):]
            if '"' in remainder:
                findings.append(_finding("quoted_path", "quoted path in diff header", index))
                continue
            fields = remainder.split(" ")
            if len(fields) != 2:
                # >2 fields means an embedded space in a path -- ambiguous;
                # fail closed instead of silently dropping middle tokens.
                findings.append(_finding("unparsable", "ambiguous diff header (embedded space in path)", index))
                continue
            for field in fields:
                _check_path(field, index, findings, strip_prefix=True)
            continue

        if line.startswith("--- ") or line.startswith("+++ "):
            _check_path(line[4:].split("\t")[0], index, findings, strip_prefix=True)
            continue

        matched_mode = False
        for prefix in _MODE_PREFIXES:
            if line.startswith(prefix):
                _check_mode(line[len(prefix):], index, findings)
                matched_mode = True
                break
        if matched_mode:
            continue

        if line.startswith("index "):
            fields = line.split(" ")
            if len(fields) >= 3:
                _check_mode(fields[2], index, findings)
            continue

        matched_path = False
        for prefix in _PATH_PREFIXES:
            if line.startswith(prefix):
                _check_path(line[len(prefix):], index, findings, strip_prefix=False)
                matched_path = True
                break
        if matched_path:
            continue

        if line.startswith("GIT binary patch"):
            findings.append(_finding("binary_patch", "binary patch cannot be inspected", index))

    if not saw_header:
        findings.append(_finding("unparsable", "no 'diff --git' header found", 0))

    return {
        "accepted": not findings,
        "findings": sorted(findings, key=lambda f: (f["line"], f["code"], f["detail"])),
    }
