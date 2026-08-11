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

CLAUDE_CONFIG_DIR — added 11 Aug 2026 (TODO !57, ASSUMPTIONS.md #23). A real
`claude` runner writes its session state to `~/.claude`/`~/.claude.json` on
startup; both names are in `cell.CELL_FORBIDDEN_NAMES` and refused however
they're declared, so every launch in this tree used a stub until now. The
fix does not loosen that refusal — `CELL_FORBIDDEN_NAMES` is untouched. It
tells the runner to write its state somewhere else: a scratch-declared
directory inside the cell, via the one env var Claude Code already honours
for this. `plan()`'s `claude_config_dir` argument is confined to the cell's
home and checked against the built cell's own declared `scratch_prefixes`
before it is ever handed to the child — a value outside the cell, or inside
it but undeclared, is refused before spawn. `BLOCKED_ENV_PREFIXES` still
refuses `CLAUDE_CONFIG_DIR` (and everything else `CLAUDE*`) when offered
through `extra_env`; the dedicated argument is the only path in, because it
is the only path that gets the confinement check.
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
# with env={"HOME":..., "PATH":...} and reading back os.environ. Unreviewed, and
# not measured on any other platform. `/usr/bin/env` arrived clean; CPython also
# carried LC_CTYPE and __CF_USER_TEXT_ENCODING; `/usr/bin/python3` — Apple's
# stub, which re-execs through xcrun — also carried CPATH, LIBRARY_PATH, MANPATH
# and SDKROOT, none of them supplied by the parent.
#
# So `env=` controls what crosses the exec, not what the child ends up with: the
# parent's dict is a floor, not a ceiling. These names are benign, the vector is
# not — any wrapper-script runner re-execs, and a re-exec adds whatever its own
# startup puts there. Hence `inspect_runner` records whether the runner is a
# script, rather than pretending to prevent the amendment.
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

    Recorded rather than refused: refusing every script would refuse the real
    runner on most installations. Going unrecorded is the failure — a later
    reading would assume the child's environment was the one the parent composed.
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
            # The parent composed `env_names`; it did not necessarily deliver
            # exactly that set — see PLATFORM_INJECTED_ENV.
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


def sterile_env(home: Path, extra_env=None, claude_config_dir: Path | None = None) -> dict:
    """Build the child's environment from nothing.

    `claude_config_dir`, when given, is set as CLAUDE_CONFIG_DIR so a real
    Claude Code runner writes its startup session state there instead of the
    forbidden literal `~/.claude`/`~/.claude.json` (ASSUMPTIONS.md #23). Not
    validated here — `plan` has already confined it to the cell and checked
    it against the built cell's declared scratch before calling this.

    `extra_env` is for what the runner genuinely needs and the caller can
    name. Every entry is checked against BLOCKED_ENV_PREFIXES, so the
    allowlist cannot be used to reintroduce the very thing the cell removed.
    CLAUDE_CONFIG_DIR specifically must go through the dedicated argument
    above, never here — that argument is what gets the confinement check.
    """
    env = {"HOME": str(home), "PATH": BASE_PATH}
    if claude_config_dir is not None:
        env["CLAUDE_CONFIG_DIR"] = str(claude_config_dir)
    for name, value in (extra_env or {}).items():
        upper = str(name).upper()
        if upper == "CLAUDE_CONFIG_DIR":
            raise LaunchError(
                "CLAUDE_CONFIG_DIR must be passed as plan()'s/sterile_env()'s "
                "claude_config_dir argument, not via extra_env — only that "
                "argument gets the inside-the-cell confinement check")
        if any(upper.startswith(prefix) for prefix in BLOCKED_ENV_PREFIXES):
            raise LaunchError(
                f"environment variable {name!r} reintroduces host context or a "
                "host credential into the cell; refused")
        if name in env:
            raise LaunchError(f"environment variable {name!r} is set by the cell")
        env[str(name)] = str(value)
    return env


def plan(built_cell, runner, isolation_grade: str, system_prompt_file=None,
         prompt_args=(), tools: str = DEFAULT_TOOLS, extra_env=None,
         claude_config_dir=None) -> LaunchPlan:
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

    resolved_config_dir = None
    if claude_config_dir is not None:
        # Must resolve inside the cell and be declared scratch — the point is
        # the runner's own startup write lands somewhere the seal already
        # expects a write, not somewhere new that reads as BYPASSED tampering.
        resolved_config_dir = cell_mod.confine(built_cell.home, claude_config_dir)
        rel = resolved_config_dir.relative_to(built_cell.home)
        declared = built_cell.spec.scratch_prefixes
        if not any(rel == Path(p) or Path(p) in rel.parents for p in declared):
            raise LaunchError(
                f"claude_config_dir {str(rel)!r} is not declared as scratch in "
                f"the cell spec {declared!r}; build the cell with it declared "
                "first, or the runner's own write will read as tampering")

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
        env=sterile_env(built_cell.home, extra_env,
                        claude_config_dir=resolved_config_dir),
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
