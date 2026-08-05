"""Coverage for launch.py.

Written this cycle, by the generator, in the same session as launch.py. These
tests are evidence that the launcher composes the environment and argv its
author intended, and that it refuses what its author intended it to refuse.

They establish nothing at all about isolation. No test here runs a real runner,
switches UID, or observes what a child can reach; the one test that spawns a
process spawns a script the test wrote, to read back the environment it was
given. Whether a Claude session in this environment is contained is SPEC §8
step 0, and step 0 is UNKNOWN.
"""

from __future__ import annotations

import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

import cell as cell_mod
import launch


def build_cell(root, **kwargs):
    kwargs.setdefault("evidence_mode", "copy")
    return cell_mod.build(cell_mod.CellSpec(root=Path(root), **kwargs))


def fake_runner(directory: Path, body: str = "import sys\n") -> Path:
    path = directory / "runner"
    path.write_text("#!/usr/bin/env python3\n" + body, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IRUSR)
    return path


class GradeTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.cells = self.tmp / "cells"
        self.cells.mkdir()
        self.cell = build_cell(self.cells / "c1")
        self.runner = fake_runner(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def test_restricted_uid_raises_the_kill_criterion(self):
        with self.assertRaises(launch.KillCriterionUnresolved) as caught:
            launch.plan(self.cell, self.runner, launch.RESTRICTED_UID)
        self.assertIn("step 0", str(caught.exception))

    def test_grade_has_no_default(self):
        with self.assertRaises(TypeError):
            launch.plan(self.cell, self.runner)

    def test_unknown_grade_is_refused(self):
        with self.assertRaises(launch.LaunchError):
            launch.plan(self.cell, self.runner, "sandboxed")

    def test_same_uid_plan_records_that_isolation_is_not_established(self):
        record = launch.plan(self.cell, self.runner, launch.SAME_UID).as_record()
        self.assertFalse(record["isolation_established"])
        self.assertEqual(record["isolation_grade"], launch.SAME_UID)
        self.assertIn("UNKNOWN", record["isolation_note"])


class SterileEnvTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.home = Path(self._tmp.name) / "home"
        self.home.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def test_environment_holds_only_home_and_path(self):
        env = launch.sterile_env(self.home)
        self.assertEqual(set(env), {"HOME", "PATH"})
        self.assertEqual(env["HOME"], str(self.home))

    def test_path_is_the_fixed_default_not_the_parents(self):
        self.assertEqual(launch.sterile_env(self.home)["PATH"], launch.BASE_PATH)
        self.assertNotEqual(launch.sterile_env(self.home)["PATH"],
                            os.environ.get("PATH"))

    def test_parent_environment_is_not_inherited(self):
        os.environ["BLACKSMITH_TEST_LEAK"] = "present"
        try:
            self.assertNotIn("BLACKSMITH_TEST_LEAK", launch.sterile_env(self.home))
        finally:
            del os.environ["BLACKSMITH_TEST_LEAK"]

    def test_context_and_credential_names_cannot_be_smuggled_in(self):
        for name in ("CLAUDE_CONFIG_DIR", "ANTHROPIC_API_KEY", "XDG_CONFIG_HOME",
                     "GITHUB_TOKEN", "anthropic_api_key"):
            with self.subTest(name=name):
                with self.assertRaises(launch.LaunchError):
                    launch.sterile_env(self.home, {name: "x"})

    def test_declared_extra_is_admitted(self):
        env = launch.sterile_env(self.home, {"TERM": "dumb"})
        self.assertEqual(env["TERM"], "dumb")

    def test_extra_may_not_override_home(self):
        with self.assertRaises(launch.LaunchError):
            launch.sterile_env(self.home, {"HOME": "/etc"})


class PlanRefusalTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.cells = self.tmp / "cells"
        self.cells.mkdir()
        self.cell = build_cell(self.cells / "c1")
        self.runner = fake_runner(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def test_non_sterile_cell_blocks_the_launch(self):
        os.chmod(self.cell.home, 0o755)
        (self.cell.home / "CLAUDE.md").write_text("inject", encoding="utf-8")
        with self.assertRaises(cell_mod.CellError):
            launch.plan(self.cell, self.runner, launch.SAME_UID)

    def test_missing_runner_is_refused(self):
        with self.assertRaises(launch.LaunchError):
            launch.plan(self.cell, self.tmp / "nope", launch.SAME_UID)

    def test_non_executable_runner_is_refused(self):
        plain = self.tmp / "plain.py"
        plain.write_text("print()", encoding="utf-8")
        plain.chmod(0o644)
        with self.assertRaises(launch.LaunchError):
            launch.plan(self.cell, plain, launch.SAME_UID)

    def test_missing_system_prompt_file_is_refused(self):
        with self.assertRaises(launch.LaunchError):
            launch.plan(self.cell, self.runner, launch.SAME_UID,
                        system_prompt_file=self.tmp / "absent.md")

    def test_argv_carries_the_spec_flags(self):
        prompt = self.tmp / "prompt.md"
        prompt.write_text("system", encoding="utf-8")
        argv = launch.plan(self.cell, self.runner, launch.SAME_UID,
                           system_prompt_file=prompt).argv
        self.assertIn("--safe-mode", argv)
        self.assertEqual(argv[argv.index("--tools") + 1], "Read,Grep,Glob")
        self.assertEqual(argv[argv.index("--output-format") + 1], "stream-json")
        self.assertEqual(argv[argv.index("--append-system-prompt-file") + 1],
                         str(prompt.resolve()))

    def test_cwd_is_the_cell_home(self):
        self.assertEqual(launch.plan(self.cell, self.runner, launch.SAME_UID).cwd,
                         str(self.cell.home))

    def test_run_refuses_anything_that_is_not_a_plan(self):
        with self.assertRaises(launch.LaunchError):
            launch.run({"argv": ["/bin/echo"]})


class SpawnedChildTests(unittest.TestCase):
    """One real spawn, of a script this test wrote, to read back its own env."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.cells = self.tmp / "cells"
        self.cells.mkdir()
        self.cell = build_cell(self.cells / "c1")

    def tearDown(self):
        self._tmp.cleanup()

    def test_child_sees_the_sterile_environment_and_cwd(self):
        os.environ["BLACKSMITH_TEST_LEAK"] = "present"
        runner = fake_runner(self.tmp, body=(
            "import json, os, sys\n"
            "sys.stdout.write(json.dumps("
            "{'env': sorted(os.environ), 'cwd': os.getcwd()}))\n"))
        try:
            plan = launch.plan(self.cell, runner, launch.SAME_UID)
            # argv[0] is this interpreter by absolute path, deliberately not
            # `/usr/bin/env python3`: under the module's own BASE_PATH, `python3`
            # resolves to Apple's Command Line Tools stub, which is the shim the
            # next test is about. Routing the baseline through it would measure
            # the shim and call the result the platform floor.
            plan = launch.LaunchPlan(
                argv=(sys.executable, str(runner)),
                env=plan.env, cwd=plan.cwd, isolation_grade=plan.isolation_grade)
            result = launch.run(plan, timeout=30)
        finally:
            del os.environ["BLACKSMITH_TEST_LEAK"]

        self.assertEqual(result["exit_code"], 0, result["stderr"])
        import json
        seen = json.loads(result["stdout"])
        self.assertNotIn("BLACKSMITH_TEST_LEAK", seen["env"])
        self.assertEqual(os.path.realpath(seen["cwd"]), str(self.cell.home))

        # Not {"HOME", "PATH"}. Even execing the interpreter directly, the child
        # carries names the parent never passed, added by the platform after
        # exec. Pinning the observed set here means a platform that starts
        # adding a *different* name fails this test rather than passing quietly
        # — which is the only way the assumption gets re-measured rather than
        # inherited.
        self.assertEqual(set(seen["env"]) - {"HOME", "PATH"},
                         set(launch.PLATFORM_INJECTED_ENV))

    @unittest.skipUnless(sys.platform == "darwin", "Darwin toolchain shim")
    @unittest.skipUnless(Path("/usr/bin/python3").exists(), "no CLT stub present")
    def test_the_modules_own_base_path_resolves_python3_to_the_shim(self):
        # BASE_PATH was chosen to be a clean system PATH. On this host that
        # clean PATH is exactly what routes to the injecting stub. A fixed PATH
        # is not the same thing as a PATH with nothing on it that re-execs.
        import shutil
        resolved = shutil.which("python3", path=launch.BASE_PATH)
        self.assertEqual(resolved, "/usr/bin/python3")

    @unittest.skipUnless(sys.platform == "darwin", "Darwin toolchain shim")
    @unittest.skipUnless(Path("/usr/bin/python3").exists(), "no CLT stub present")
    def test_a_shim_on_the_exec_path_adds_more_than_the_platform_does(self):
        # The finding this pins: `env=` governs what crosses the exec, not what
        # the child ends up with. Apple's Command Line Tools stub re-execs
        # through xcrun and arrives with SDKROOT, CPATH, LIBRARY_PATH and
        # MANPATH set — none supplied by the parent. A `claude` binary that is
        # an npm or version-manager wrapper script has the same shape.
        script = self.tmp / "dump.py"
        script.write_text("import json, os, sys\n"
                          "sys.stdout.write(json.dumps(sorted(os.environ)))\n",
                          encoding="utf-8")
        plan = launch.LaunchPlan(
            argv=("/usr/bin/python3", str(script)),
            env=launch.sterile_env(self.cell.home), cwd=str(self.cell.home),
            isolation_grade=launch.SAME_UID)
        result = launch.run(plan, timeout=120)
        self.assertEqual(result["exit_code"], 0, result["stderr"])

        import json
        added = (set(json.loads(result["stdout"]))
                 - {"HOME", "PATH"} - set(launch.PLATFORM_INJECTED_ENV))
        self.assertTrue(added, "expected the shim to add environment; it added none")


class RunnerInspectionTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_script_runner_is_flagged_as_able_to_amend_the_environment(self):
        report = launch.inspect_runner(fake_runner(self.tmp))
        self.assertTrue(report["is_script"])
        self.assertTrue(report["may_amend_child_environment"])
        self.assertEqual(report["shebang"], "#!/usr/bin/env python3")

    def test_binary_runner_is_not_flagged(self):
        report = launch.inspect_runner("/bin/echo")
        self.assertFalse(report["is_script"])
        self.assertFalse(report["may_amend_child_environment"])
        self.assertIsNone(report["shebang"])

    def test_symlinked_runner_is_reported_by_its_real_path(self):
        target = fake_runner(self.tmp)
        link = self.tmp / "claude"
        link.symlink_to(target)
        report = launch.inspect_runner(link)
        self.assertEqual(report["path"], str(target.resolve()))
        self.assertEqual(report["path_as_given"], str(link))

    def test_the_plan_carries_the_runner_report(self):
        cells = self.tmp / "cells"
        cells.mkdir()
        built = build_cell(cells / "c1")
        record = launch.plan(built, fake_runner(self.tmp),
                             launch.SAME_UID).as_record()
        self.assertTrue(record["runner"]["may_amend_child_environment"])
        self.assertTrue(record["env_is_a_floor_not_a_ceiling"])

    def test_result_record_still_says_isolation_is_not_established(self):
        cells = self.tmp / "cells"
        cells.mkdir()
        built = build_cell(cells / "c1")
        runner = fake_runner(self.tmp, body="import sys\nsys.exit(0)\n")
        plan = launch.plan(built, runner, launch.SAME_UID)
        plan = launch.LaunchPlan(argv=(sys.executable, str(runner)),
                                 env=plan.env, cwd=plan.cwd,
                                 isolation_grade=plan.isolation_grade)
        result = launch.run(plan, timeout=30)
        self.assertFalse(result["isolation_established"])


if __name__ == "__main__":
    unittest.main()
