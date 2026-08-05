"""Content-addressed object store — the Ring 0 input/output boundary.

No security claim is made here. This module removes one class of defect: trusted
code selecting a file by a name that untrusted data supplied. Objects are named
by the SHA-256 of their contents, and every read re-hashes before returning.

Remediation:
  area 1 / area 4 — untrusted input crosses the boundary as bytes, never as a
  path. `get()` accepts a 64-hex object id only, so an object id cannot express
  traversal, and no caller can steer a read or a write outside the store root.
  area 1 — reads verify content, so a write-then-tamper window is detected at
  use rather than assumed away.

Assumption requiring runtime verification (see ASSUMPTIONS.md):
  the store root is not writable by the untrusted UID. This module cannot
  establish that; it must be checked by permission attestation before launch.
"""

from __future__ import annotations

import hashlib
import os
import re
import tempfile
from pathlib import Path


# \Z, not $ -- $ matches end-of-string OR just before a trailing "\n", so
# "a"*64 + "\n" (65 bytes) would satisfy this pattern under $ and carry a
# newline into the on-disk object filename: same logical id, two files.
OBJECT_ID = re.compile(r"^[0-9a-f]{64}\Z")


class StoreError(Exception):
    """The store could not satisfy the request."""


class IntegrityError(StoreError):
    """Stored bytes did not hash to the id they were filed under."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _valid_id(object_id) -> str:
    if not isinstance(object_id, str) or not OBJECT_ID.match(object_id):
        raise StoreError("object id is not a 64-character lowercase hex digest")
    return object_id


def confine(root: Path, candidate) -> Path:
    """Resolve `candidate` and require it to sit inside `root`.

    realpath before the prefix comparison, so a symlink cannot present an
    inside-looking path for an outside target. Same shape as
    forensic_checker/scope.py; duplicated rather than imported to avoid coupling
    this tree to that package's sealed integrity manifest (see ASSUMPTIONS.md).
    """
    real_root = Path(os.path.realpath(str(root)))
    real = Path(os.path.realpath(str(candidate)))
    if real != real_root and real_root not in real.parents:
        raise StoreError(f"path {str(candidate)!r} resolves outside {str(real_root)!r}")
    return real


class ObjectStore:
    def __init__(self, root):
        self._root = Path(os.path.realpath(str(root)))
        self._objects = self._root / "objects"
        self._objects.mkdir(parents=True, exist_ok=True)

    @property
    def root(self) -> Path:
        return self._root

    def _path_for(self, object_id: str) -> Path:
        _valid_id(object_id)
        return self._objects / object_id[:2] / object_id

    def put_bytes(self, data: bytes) -> str:
        """File `data` under its own digest. Returns the object id."""
        if not isinstance(data, (bytes, bytearray)):
            raise StoreError("only bytes may be filed")
        data = bytes(data)
        object_id = sha256_bytes(data)
        target = self._path_for(object_id)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            return object_id
        fd, tmp = tempfile.mkstemp(dir=str(target.parent))
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
            os.chmod(tmp, 0o444)
            os.replace(tmp, target)
        except BaseException:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise
        return object_id

    def get(self, object_id: str) -> bytes:
        """Return the object's bytes, re-hashed. Never accepts a path."""
        target = self._path_for(object_id)
        if not target.is_file():
            raise StoreError(f"object {object_id} is not in the store")
        data = target.read_bytes()
        actual = sha256_bytes(data)
        if actual != object_id:
            raise IntegrityError(f"object {object_id} hashes to {actual}")
        return data

    def has(self, object_id: str) -> bool:
        try:
            return self._path_for(object_id).is_file()
        except StoreError:
            return False

    def ingest_host_file(self, path, allowed_root) -> str:
        """Host-side only. `path` must come from host configuration, never from
        untrusted data; `allowed_root` confines it regardless."""
        real = confine(Path(allowed_root), path)
        if not real.is_file():
            raise StoreError(f"{str(real)!r} is not a regular file")
        return self.put_bytes(real.read_bytes())


def as_check(store: ObjectStore, object_id) -> dict:
    """Render a store lookup as a gauge check entry.

    Re-derivation, not duplication: `get()` already re-hashes on every read
    and raises `StoreError` (or its `IntegrityError` subclass) the moment the
    bytes on disk don't hash to the id they're filed under. This renders that
    existing outcome into gauge's CHECK_OUTCOMES rather than hashing a second
    time — a second hashing path is exactly what gauge's own docstring warns
    this tree against.
    """
    try:
        data = store.get(object_id)
    except StoreError as exc:
        return {"outcome": "FAIL", "detail": str(exc)}
    return {"outcome": "PASS",
            "detail": "artifact re-hashed to its declared id", "size": len(data)}
