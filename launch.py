"""Launch — spawn the cell's occupant. Ring 0, parent-side.

No security claim is made here, and one specific claim is refused outright:
this module does not establish that the child is contained. Containment is the
UID boundary, the UID boundary is SPEC §8 step 0, and step 0 is UNKNOWN. A
launcher that ran the child under the parent's own UID and reported success
would be reporting that the process started, which nobody doubted.

So `isolation_grade` is a required argument with no default and exactly two
legal values:

  "same_uid_policy_grade"  — the child runs as the parent's UID. Everything the
      parent can reach, the child can reach; the cell's read-only bits are
      owner-settable and therefore owner-clearable. Evidence gathered under this
      grade is policy-grade, which SPEC §8 names as the fallback that kills the
      design's central claim. It is legal here because measuring the fallback is
      how you learn what it costs, and it is *labelled* so no result gathered
      under it can later be read as the kernel-grade one.

  "restricted_uid"         — raises. Implementing it is step 0.

The environment is built from `{}`, not from `os.environ` with entries removed.
SPEC §2 rule 3: absent, not disabled. A filter has to enumerate every bad name
and is wrong the day a new one appears; an allowlist starting from nothing is
wrong only about names it was never given, which is the failure that shows up
as the child not working rather than as the child seeing too much.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import cell as cell_mod

SAME_UID = "same_uid_policy_grade"
RESTRICTED_UID = "restricted_uid"
GRADES = (SAME_UID, RESTRICTED_UID)

# The child gets these and nothing else. PATH is a fixed system default rather
# than the parent's, which on a developer machine carries toolchain shims,
# version-manager hooks, and per-project directories.
BASE_PATH = "/usr/bin:/bin:/usr/sbin:/sbin"

# Names that reintroduce host context or host credentials. A caller may not
# smuggle one through `extra_env`. Credential variables are refused for a
# separate reason from the context ones: whether a credential should cross into
# the cell at all is SPEC §8 step 0 and SPEC §11 ruling 4, both open.
BLOCKED_ENV_PREFIXES = (
    "CLAUDE", "ANTHROPIC", "XDG_", "OPENAI", "GOOGLE", "AWS_", "GH_", "GITHUB_",
    "NPM_", "NODE_", "PYTHON",
)

DEFAULT_TOOLS = "Read,Grep,Glob"

# Measured on Darwin 25.6 this cycle, by the generator, by spawning a script
# with env={"HOME":..., "PATH":...} and reading back os.environ. Not reviewed by
# anyone else, and not measured on any other platform.
#
# The result that matters is not this list, it is what producing it showed:
# `env=` controls what crosses the exec, and does not control what the child
# ends up with. `/usr/bin/env` arrived clean; a CPython process additionally
# carried LC_CTYPE and __CF_USER_TEXT_ENCODING, added by the platform after
# exec; and `/usr/bin/python3` — Apple's Command Line Tools stub, which re-execs
# through xcrun — additionally carried CPATH, LIBRARY_PATH, MANPATH and SDKROOT,
# none of which the parent supplied.
#
# So the parent's environment dict is a floor, not a ceiling. The names below
# are benign. The vector is not: any runner that is a wrapper script re-execs,
# and a re-exec can add anything the wrapper's own startup puts there. That is
# why `inspect_runner` records whether the runner is a script, rather than this
# module pretending it can prevent the amendment.
PLATFORM_INJECTED_ENV = frozenset({"LC_CTYPE", "__CF_USER_TEXT_ENCODING"})


class LaunchError(Exception):
    """The child could not be launched to specification."""


class KillCriterionUnresolved(LaunchError):
    """The requested grade depends on a SPEC §8 kill criterion that is open."""


def inspect_runner(path) -> dict:
    """Report whether the runner re-execs, which is the environment-injection vector.

    A runner with a shebang is a script: it execs an interpreter, and that
    interpreter's startup can add environment the parent never passed. The npm
    and version-manager shims that a `claude` on the PATH is most likely to be
    are exactly this shape.

    This records the fact rather than refusing it — refusing every script would
    refuse the real runner on most installations. What must not happen is the
    fact going unrecorded, so a later reading of the evidence can assume the
    child's environment was the one the parent composed.
    """
    real = Path(os.path.realpath(str(path)))
    head = b""
    try:
        with open(real, "rb") as handle:
            head = handle.read(256)
    except OSError:
        pass
    is_script = head.startswith(b"#!")
    shebang = None
    if is_script:
        shebang = head.split(b"\n", 1)[0].decode("utf-8", "replace").strip()
    return {
        "path": str(real),
        "path_as_given": str(path),
        "is_script": is_script,
        "shebang": shebang,
        "may_amend_child_environment": is_script,
    }


@dataclass(frozen=True)
class LaunchPlan:
    """Everything about the launch, decided before anything is spawned."""

    argv: tuple
    env: dict
    cwd: str
    isolation_grade: str
    runner: dict = field(default_factory=dict)

    def as_record(self) -> dict:
        return {
            "argv": list(self.argv),
            "env_names": sorted(self.env),
            "cwd": self.cwd,
            "isolation_grade": self.isolation_grade,
            "runner": dict(self.runner),
            # The parent composed `env_names`. It did not necessarily deliver
            # exactly that set — see PLATFORM_INJECTED_ENV. Stated here so a
            # reader of the record does not have to know the module to know it.
            "env_is_a_floor_not_a_ceiling": True,
            "platform_injected_env": sorted(PLATFORM_INJECTED_ENV),
            # Restated in the record rather than left to the reader, because
            # this is the field a later summary is most likely to drop.
            "isolation_established": False,
            "isolation_note": (
                "the child ran under the parent's UID; nothing here establishes "
                "that it could not reach the host. SPEC §8 step 0 is UNKNOWN."
            ),
        }


def sterile_env(home: Path, extra_env=None) -> dict:
    """Build the child's environment from nothing.

    `extra_env` is for what the runner genuinely needs and the caller can name.
    Every entry is checked against BLOCKED_ENV_PREFIXES, so the allowlist cannot
    be used to reintroduce the very thing the cell removed.
    """
    env = {"HOME": str(home), "PATH": BASE_PATH}
    for name, value in (extra_env or {}).items():
        upper = str(name).upper()
        if any(upper.startswith(prefix) for prefix in BLOCKED_ENV_PREFIXES):
            raise LaunchError(
                f"environment variable {name!r} reintroduces host context or a "
                "host credential into the cell; refused")
        if name in env:
            raise LaunchError(f"environment variable {name!r} is set by the cell")
        env[str(name)] = str(value)
    return env


def plan(built_cell, runner, isolation_grade: str, system_prompt_file=None,
         prompt_args=(), tools: str = DEFAULT_TOOLS, extra_env=None) -> LaunchPlan:
    """Compose the launch. Nothing is spawned; this is the decision, written down.

    The flags follow SPEC §5 step 4. Their *semantics* are the runner's, not
    this module's, and are unverified here — SPEC §6 records `--tools` as the
    one harness restriction with evidence behind it and the rest as unproven.
    Composing a flag is not evidence the flag binds.
    """
    if isolation_grade not in GRADES:
        raise LaunchError(
            f"isolation_grade must be one of {GRADES}, got {isolation_grade!r}")
    if isolation_grade == RESTRICTED_UID:
        raise KillCriterionUnresolved(
            "launching as a restricted UID is SPEC §8 step 0 — whether "
            "credentials survive the switch is the design's kill criterion and "
            "is UNKNOWN. Running it wrong and reading the result as a PASS "
            "would validate the central claim falsely, so it is not implemented "
            "here")

    # Fail closed before composing anything: a launch into a cell that is not
    # sterile is a session SPEC §2 rule 6 says does not happen.
    cell_mod.require_sterile(built_cell)

    runner_path = Path(os.path.realpath(str(runner)))
    if not runner_path.is_file():
        raise LaunchError(f"runner {str(runner_path)!r} is not a regular file")
    if not os.access(runner_path, os.X_OK):
        raise LaunchError(f"runner {str(runner_path)!r} is not executable")

    argv = [str(runner_path), "--safe-mode", "--tools", tools,
            "--output-format", "stream-json"]
    if system_prompt_file is not None:
        prompt_path = Path(os.path.realpath(str(system_prompt_file)))
        if not prompt_path.is_file():
            raise LaunchError(f"system prompt file {str(prompt_path)!r} is not a file")
        argv += ["--append-system-prompt-file", str(prompt_path)]
    argv += [str(a) for a in prompt_args]

    return LaunchPlan(
        argv=tuple(argv),
        env=sterile_env(built_cell.home, extra_env),
        cwd=str(built_cell.home),
        isolation_grade=isolation_grade,
        runner=inspect_runner(runner_path),
    )


def run(launch_plan: LaunchPlan, timeout: float | None = None) -> dict:
    """Spawn the child and capture its streams in the parent.

    The transcript is captured here rather than written by the child, so the
    cell needs no writable directory for it. That is not a convenience: a cell
    with a writable output directory cannot distinguish the child writing its
    artifact from the child writing anything else, and post-attest would have to
    excuse a whole directory to stay quiet.
    """
    if not isinstance(launch_plan, LaunchPlan):
        raise LaunchError("run() takes a LaunchPlan built by plan()")
    try:
        proc = subprocess.run(
            list(launch_plan.argv), env=dict(launch_plan.env),
            cwd=launch_plan.cwd, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        return dict(launch_plan.as_record(), exit_code=None, timed_out=True,
                    stdout=(exc.stdout or b"").decode("utf-8", "replace"),
                    stderr=(exc.stderr or b"").decode("utf-8", "replace"))
    return dict(launch_plan.as_record(), exit_code=proc.returncode, timed_out=False,
                stdout=proc.stdout.decode("utf-8", "replace"),
                stderr=proc.stderr.decode("utf-8", "replace"))
