"""Local harness tests with fake agents and real source helpers, NOT model evidence."""

import importlib
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import time
import unittest
from unittest.mock import patch


HARNESS = Path(__file__).resolve().parent / "sdc-agent"
sys.path.insert(0, str(HARNESS))


class HarnessUnitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="sdc-agent-unit-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def runner(self):
        self.assertTrue((HARNESS / "run_agent_evals.py").exists(), "runner not implemented")
        return importlib.import_module("run_agent_evals")

    def invoke_fake(self, code, **kwargs):
        runner = self.runner()
        return runner.run_process(
            [sys.executable, "-c", code], self.root, os.environ.copy(), "",
            self.root / "transcript", timeout=kwargs.pop("timeout", 2),
            max_output_bytes=kwargs.pop("max_output_bytes", 100_000), **kwargs,
        )

    def test_fake_process_nonzero_is_not_retried(self):
        result = self.invoke_fake("from pathlib import Path; Path('once').write_text('1'); raise SystemExit(7)")
        self.assertEqual(result["exit_code"], 7)
        self.assertEqual(result["attempts"], 1)
        self.assertEqual(result["status"], "process_failed")

    def test_fake_timeout_preserves_partial_transcript(self):
        result = self.invoke_fake("import time; print('partial', flush=True); time.sleep(10)", timeout=0.15)
        self.assertTrue(result["timed_out"])
        self.assertEqual(result["status"], "timeout")
        self.assertLess(result["elapsed_seconds"], 2)
        self.assertIn("partial", (self.root / "transcript.stdout.jsonl").read_text())

    def test_fake_output_limit_is_failure(self):
        result = self.invoke_fake("import sys; sys.stdout.write('x'*200000)", max_output_bytes=100)
        self.assertEqual(result["status"], "output_limit")
        self.assertLessEqual((self.root / "transcript.stdout.jsonl").stat().st_size, 100)

    def test_missing_executable_recorded(self):
        runner = self.runner()
        result = runner.run_process(
            [str(self.root / "does-not-exist")], self.root, {}, "", self.root / "missing",
            timeout=1, max_output_bytes=1000,
        )
        self.assertEqual(result["status"], "launch_error")
        self.assertIsNone(result["exit_code"])

    def test_isolated_environment_drops_secrets_and_autoload(self):
        runner = self.runner()
        env = runner.isolated_env(self.root, {
            "PATH": "/usr/bin", "HOME": "/real/home", "CODEX_HOME": "/real/codex",
            "OPENAI_API_KEY": "do-not-inherit", "ANTHROPIC_API_KEY": "do-not-inherit",
            "CLAUDE_PLUGIN_ROOT": "/plugins", "SDC_ACTIVE_CHANGE": "stale",
            "PYTHONPATH": "/injected", "NODE_OPTIONS": "--require injected.js",
        }, "isolated")
        for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "CLAUDE_PLUGIN_ROOT", "SDC_ACTIVE_CHANGE", "PYTHONPATH", "NODE_OPTIONS"):
            self.assertNotIn(key, env)
        self.assertEqual(env["HOME"], str(self.root / "home"))
        self.assertEqual(env["CODEX_HOME"], str(self.root / "home" / ".codex"))

    def make_source(self):
        source = self.root / "source"
        for relative in ("sdc-cli.py", "skills/sdc-core/SKILL.md", "scripts/sdc-runtime-context.py", "commands/sdc.md", "sdc-references/runtime-context.md"):
            file = source / relative
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text("selected source\n")
        (source / "secret.txt").write_text("not selected")
        return source

    def test_baseline_has_no_sdc_source_and_snapshot_is_copied(self):
        runner = self.runner()
        baseline = self.root / "baseline"
        baseline.mkdir()
        self.assertEqual(runner.install_source(None, baseline)["files"], {})
        self.assertEqual(list(baseline.iterdir()), [])
        source = self.make_source()
        selected = self.root / "selected"
        selected.mkdir()
        manifest = runner.install_source(source, selected)
        self.assertIn("sdc-cli.py", manifest["files"])
        self.assertFalse((selected / "secret.txt").exists())
        (source / "sdc-cli.py").write_text("changed later")
        self.assertEqual((selected / "sdc-cli.py").read_text(), "selected source\n")

    def test_source_symlink_is_rejected(self):
        runner = self.runner()
        source = self.make_source()
        (source / "commands" / "leak.md").symlink_to(source / "secret.txt")
        target = self.root / "target"
        target.mkdir()
        with self.assertRaises(ValueError):
            runner.install_source(source, target)

    def test_false_pass_and_missing_events_are_unknown(self):
        self.runner()
        grading = importlib.import_module("grading")
        events = grading.parse_transcript("codex", "RESULT: PASS\n")
        self.assertEqual(events["model_status"], "unknown")
        self.assertIsNone(events["usage"]["input_tokens"])
        result = grading.aggregate_outcome("completed", events["model_status"], [{"status": "pass"}])
        self.assertEqual(result, "unknown")

    def test_codex_events_keep_tool_failure_and_usage_separate(self):
        self.runner()
        grading = importlib.import_module("grading")
        raw = "\n".join(json.dumps(item) for item in [
            {"type": "item.completed", "item": {"type": "command_execution", "command": "test", "exit_code": 1, "status": "completed"}},
            {"type": "turn.completed", "usage": {"input_tokens": 40, "cached_input_tokens": 10, "output_tokens": 4}},
        ])
        result = grading.parse_transcript("codex", raw)
        self.assertEqual(result["model_status"], "completed")
        self.assertEqual(result["tool_exits"][0]["exit_code"], 1)
        self.assertEqual(result["usage"]["input_tokens"], 40)
        self.assertIsNone(result["usage"]["cost_usd"])

    def test_claude_error_even_zero_process_exit_is_not_pass(self):
        self.runner()
        grading = importlib.import_module("grading")
        result = grading.parse_transcript("claude", json.dumps({"type": "result", "is_error": True, "subtype": "error_max_turns"}))
        self.assertEqual(result["model_status"], "failed")
        self.assertEqual(grading.aggregate_outcome("completed", "failed", [{"status": "pass"}]), "unknown")

    def test_all_six_scenarios_have_semantic_rubrics(self):
        self.runner()
        scenarios = importlib.import_module("scenarios").SCENARIOS
        self.assertEqual(set(scenarios), {"vague-intake", "authorized-maintenance", "brownfield-conflict", "failed-test-delivery", "revision-invalidation", "interruption-resume"})
        for name, scenario in scenarios.items():
            self.assertTrue(scenario["semantic_rubric"], name)
            self.assertTrue(scenario["prompts"], name)

    def test_vague_intake_does_not_pass_when_agent_creates_code(self):
        runner = self.runner()
        grading = importlib.import_module("grading")
        scenarios = importlib.import_module("scenarios")
        scenarios.seed_project(self.root, "vague-intake")
        before = runner.file_manifest(self.root)
        (self.root / "app.py").write_text("print('unauthorized')\n")
        checks = grading.structural_checks("vague-intake", self.root, before, [])
        self.assertIn("fail", [check["status"] for check in checks])

    def test_codex_does_not_override_reserved_provider(self):
        self.runner()
        adapters = importlib.import_module("agent_adapters")
        command = adapters.agent_command("codex", "/bin/codex")
        self.assertFalse(any(value.startswith("model_providers.openai.") for value in command))
        self.assertIn("skip_host_skill_discovery", command)
        self.assertIn("--ignore-user-config", command)

    def test_runtime_support_modules_are_staged(self):
        runner = self.runner()
        source = self.make_source()
        helpers = ("scripts/sdc_evidence.py", "scripts/sdc_compact.py",
                   "scripts/sdc_findings.py", "scripts/sdc-doctor.mjs")
        for name in helpers:
            (source / name).write_text("# runtime dependency\n")
        target = self.root / "target"
        target.mkdir()
        manifest = runner.install_source(source, target)
        for name in helpers:
            with self.subTest(helper=name):
                self.assertIn(name, manifest["files"])

    def freeze_source_twice(self, source):
        runner = self.runner()
        frozen = self.root / "frozen"
        project = self.root / "project"
        frozen.mkdir()
        project.mkdir()
        # main freezes the source, then run_trial copies it into its fresh project.
        first = runner.install_source(source, frozen)
        second = runner.install_source(frozen, project)
        self.assertEqual(first["files"], second["files"])
        self.assertEqual(first["sha256"], second["sha256"])
        return project

    def invoke_snapshot_helper(self, project, command):
        runner = self.runner()
        env = runner.isolated_env(self.root, os.environ, "isolated")
        self.assertNotIn("PYTHONPATH", env)
        result = runner.run_process(command, project, env, "", self.root / "helper",
                                    timeout=5, max_output_bytes=100_000)
        stdout = (self.root / result["stdout_ref"]).read_text()
        stderr = (self.root / result["stderr_ref"]).read_text()
        return result, stdout, stderr

    def test_current_source_helpers_survive_double_snapshot(self):
        project = self.freeze_source_twice(HARNESS.parent.parent)
        commands = (
            ("sdc-cli.py",),
            ("scripts/sdc-runtime-context.py", "--help"),
            ("scripts/sdc-task-brief.py", "--help"),
            ("scripts/sdc-review-package.py", "--help"),
            ("scripts/sdc_findings.py", "--help"),
        )
        for command in commands:
            with self.subTest(helper=command[0]):
                result, stdout, stderr = self.invoke_snapshot_helper(
                    project, [sys.executable, "-B", *command])
                self.assertEqual(result["exit_code"], 0, stderr)
                self.assertEqual(result["status"], "completed", stderr)
                self.assertTrue(stdout.strip())
                self.assertEqual(stderr, "")

    @unittest.skipUnless(shutil.which("node"), "Node.js is required for the doctor sidecar")
    def test_current_source_doctor_survives_double_snapshot(self):
        project = self.freeze_source_twice(HARNESS.parent.parent)
        for command in ([shutil.which("node"), "scripts/sdc-doctor.mjs"],
                        [sys.executable, "-B", "sdc-cli.py", "check", "installation"]):
            with self.subTest(command=command):
                result, stdout, stderr = self.invoke_snapshot_helper(
                    project, command + ["--json", "--home", str(self.root / "home"),
                                        "--source", str(project)])
                self.assertEqual(stderr, "")
                self.assertEqual(result["exit_code"], 1)
                self.assertEqual(result["status"], "process_failed")
                report = json.loads(stdout)
                self.assertEqual(report["schema"], "sdc.install-diagnostics/v1")
                self.assertFalse(report["ok"])
                self.assertEqual(report["installations"], [])
                self.assertEqual([issue["code"] for issue in report["issues"]], ["NO_INSTALLATIONS"])

    def test_older_source_without_new_helpers_survives_double_snapshot(self):
        source = self.make_source()
        for name in ("sdc-cli.py", "scripts/sdc-runtime-context.py"):
            (source / name).write_text("print('older snapshot')\n")
        project = self.freeze_source_twice(source)
        for name in ("scripts/sdc_compact.py", "scripts/sdc_findings.py", "scripts/sdc-doctor.mjs"):
            self.assertFalse((project / name).exists())
        for name in ("sdc-cli.py", "scripts/sdc-runtime-context.py"):
            result, stdout, stderr = self.invoke_snapshot_helper(project, [sys.executable, "-B", name])
            self.assertEqual(result["status"], "completed", stderr)
            self.assertEqual(stdout, "older snapshot\n")

    def test_new_source_helpers_obey_byte_bound(self):
        runner = self.runner()
        source = self.make_source()
        for index, name in enumerate(("scripts/sdc_compact.py", "scripts/sdc_findings.py", "scripts/sdc-doctor.mjs")):
            with self.subTest(helper=name):
                (source / name).write_text("x" * 1025)
                target = self.root / str(index)
                target.mkdir()
                with patch.object(runner, "MAX_SOURCE_BYTES", 1024):
                    with self.assertRaisesRegex(ValueError, "bounded file/byte limit"):
                        runner.install_source(source, target)
                (source / name).unlink()

    def test_new_source_helpers_reject_symlinks(self):
        runner = self.runner()
        source = self.make_source()
        for index, name in enumerate(("scripts/sdc_compact.py", "scripts/sdc_findings.py", "scripts/sdc-doctor.mjs")):
            with self.subTest(helper=name):
                (source / name).symlink_to(source / "secret.txt")
                target = self.root / str(index)
                target.mkdir()
                with self.assertRaisesRegex(ValueError, "Symlinks are not allowed"):
                    runner.install_source(source, target)
                (source / name).unlink()

    def test_source_helpers_reject_symlinked_directory(self):
        runner = self.runner()
        source = self.make_source()
        outside = self.root / "outside-scripts"
        (source / "scripts").rename(outside)
        (source / "scripts").symlink_to(outside, target_is_directory=True)
        target = self.root / "target"
        target.mkdir()
        with self.assertRaisesRegex(ValueError, "Symlinks are not allowed"):
            runner.install_source(source, target)

    def test_snapshot_excludes_installers_hooks_and_unlisted_javascript(self):
        source = self.make_source()
        excluded = ("bin/install.js", "hooks/hooks.json", "hooks/session-start.sh",
                    ".codex-plugin/plugin.json", ".claude-plugin/plugin.json",
                    "skills/sdc-core/SKILL.md", ".sdc/state.json", "scripts/unlisted.py",
                    "scripts/unlisted.mjs", "commands/unlisted.mjs", "sdc-references/unlisted.mjs")
        for name in excluded:
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("must not be copied\n")
        project = self.freeze_source_twice(source)
        for name in excluded:
            with self.subTest(path=name):
                self.assertFalse((project / name).exists())

    def test_grading_never_reads_symlinked_ancestors(self):
        self.runner()
        grading = importlib.import_module("grading")
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "labels.py").write_text("def normalize(value):\n    return value.strip().lower()\n")
        project = self.root / "project"
        project.mkdir()
        (project / "src").symlink_to(outside, target_is_directory=True)
        self.assertEqual(grading.normalize_behavior(project)["status"], "fail")

    def test_fake_end_to_end_trials_get_fresh_projects(self):
        runner = self.runner()
        import argparse
        args = argparse.Namespace(model="default", timeout=2, max_output_bytes=100000, auth_mode="isolated")
        output = self.root / "artifacts"
        output.mkdir()
        fake = [sys.executable, "-c", "import json; print(json.dumps({'type':'turn.completed','usage':{'input_tokens':1,'output_tokens':1}}))"]
        preflight = {"ready": True, "executable": sys.executable}
        with patch.object(runner, "probe_agent", return_value=preflight), patch.object(runner, "agent_command", return_value=fake):
            one = runner.run_trial("codex", None, "baseline", "vague-intake", 1, args, output)
            two = runner.run_trial("codex", None, "baseline", "vague-intake", 2, args, output)
        self.assertNotEqual(one["temporary_project"], two["temporary_project"])
        self.assertFalse(Path(one["temporary_project"]).exists())
        self.assertEqual(one["objective_outcome"], "pass")
        self.assertEqual(one["outcome"], "unknown")
        self.assertEqual(one["fixture_sha256"], two["fixture_sha256"])

    def test_cli_retry_event_stops_fake_agent_without_retry(self):
        result = self.invoke_fake("import json,time; print(json.dumps({'type':'error','message':'Reconnecting... 1/5'}), flush=True); time.sleep(10)", stop_on_agent_error=True)
        self.assertEqual(result["status"], "client_retry_detected")
        self.assertFalse(result["timed_out"])
        self.assertEqual(result["attempts"], 1)

    def test_fake_timeout_kills_descendants(self):
        code = "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',\"import time; from pathlib import Path; time.sleep(.6); Path('leaked-child').touch()\"]); time.sleep(10)"
        result = self.invoke_fake(code, timeout=0.15)
        self.assertEqual(result["status"], "timeout")
        time.sleep(0.65)
        self.assertFalse((self.root / "leaked-child").exists())

    def test_static_grader_never_executes_module(self):
        self.runner()
        grading = importlib.import_module("grading")
        (self.root / "src").mkdir()
        (self.root / "src/labels.py").write_text("from pathlib import Path\nPath('should-not-exist').touch()\ndef normalize(value):\n    return value.strip().lower()\n")
        self.assertEqual(grading.normalize_behavior(self.root)["status"], "unknown")
        self.assertFalse((self.root / "should-not-exist").exists())

    def test_malformed_event_shapes_do_not_crash_or_pass(self):
        self.runner()
        grading = importlib.import_module("grading")
        for raw in ('{"type":"turn.completed","usage":[]}', '{"type":"item.completed","item":42}', '{"type":"result","usage":4}', '[1,2]'):
            with self.subTest(raw=raw):
                result = grading.parse_transcript("codex" if "turn." in raw or "item." in raw else "claude", raw)
                self.assertNotEqual(result["model_status"], "completed")

    def test_model_failure_is_not_erased_by_later_completed_event(self):
        self.runner()
        grading = importlib.import_module("grading")
        result = grading.parse_transcript("codex", '{"type":"turn.failed"}\n{"type":"turn.completed","usage":{"input_tokens":1}}')
        self.assertEqual(result["model_status"], "failed")

    def test_failed_test_delivery_requires_observed_failure(self):
        runner = self.runner()
        grading = importlib.import_module("grading")
        scenarios = importlib.import_module("scenarios")
        scenarios.seed_project(self.root, "failed-test-delivery")
        before = runner.file_manifest(self.root)
        checks = grading.structural_checks("failed-test-delivery", self.root, before, [])
        self.assertEqual(next(c for c in checks if c["name"] == "observed_failed_test")["status"], "unknown")

    def test_comparison_matrix_budget_cannot_silently_expand(self):
        runner = self.runner()
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            runner.main(["--trials", "10", "--max-total-trials", "1"])
        self.assertEqual(error.exception.code, 2)

    def test_selected_instructions_use_commands_not_stale_generated_skills(self):
        runner = self.runner()
        import argparse
        source = self.make_source()
        (source / "commands/sdc.md").write_text("REVISED LOCAL COMMAND SENTINEL\n")
        (source / "skills/sdc-core/SKILL.md").write_text("STALE GENERATED SKILL SENTINEL\n")
        output = self.root / "artifacts"
        output.mkdir()
        args = argparse.Namespace(model="default", timeout=1, max_output_bytes=10000, auth_mode="isolated")
        fake = [sys.executable, "-c", "print('{\"type\":\"turn.completed\"}')"]
        with patch.object(runner, "probe_agent", return_value={"ready": True, "executable": sys.executable}), patch.object(runner, "agent_command", return_value=fake):
            result = runner.run_trial("codex", source, "current", "vague-intake", 1, args, output)
        prompt = (output / "current--vague-intake--1/phase-1.prompt.txt").read_text()
        self.assertIn("REVISED LOCAL COMMAND SENTINEL", prompt)
        self.assertNotIn("STALE GENERATED SKILL SENTINEL", prompt)
        self.assertFalse(any(name.startswith("skills/") for name in result["source"]["files"]))

    def test_source_without_generated_skills_is_supported(self):
        runner = self.runner()
        source = self.make_source()
        (source / "skills/sdc-core/SKILL.md").unlink()
        target = self.root / "target"
        target.mkdir()
        manifest = runner.install_source(source, target)
        self.assertIn("commands/sdc.md", manifest["files"])
        self.assertFalse((target / "skills").exists())

    def test_claude_synthetic_auth_error_is_not_a_successful_model(self):
        self.runner()
        grading = importlib.import_module("grading")
        events = [
            {"type": "assistant", "error": "authentication_failed",
             "message": {"role": "assistant", "model": "<synthetic>", "content": [{"type": "text", "text": "Not logged in"}]}},
            {"type": "result", "subtype": "success", "is_error": True, "result": "Not logged in"},
        ]
        parsed = grading.parse_transcript("claude", "\n".join(json.dumps(event) for event in events))
        self.assertEqual(parsed["model_status"], "failed")
        self.assertEqual(parsed["infrastructure_failure"], "authentication")
        self.assertNotIn("<synthetic>", parsed["observed_models"])
        execution = grading.classify_execution({"status": "process_failed"}, parsed)
        self.assertEqual(execution, {"status": "blocked", "failure_category": "authentication"})
        self.assertEqual(grading.aggregate_outcome(execution["status"], parsed["model_status"], [{"status": "pass"}]), "unknown")

    def test_claude_success_subtype_without_explicit_error_flag_is_unknown(self):
        self.runner()
        grading = importlib.import_module("grading")
        parsed = grading.parse_transcript("claude", '{"type":"result","subtype":"success"}')
        self.assertEqual(parsed["model_status"], "unknown")

    def test_auth_error_cannot_be_erased_by_later_success(self):
        self.runner()
        grading = importlib.import_module("grading")
        parsed = grading.parse_transcript("claude", '{"type":"assistant","error":"authentication_failed","message":{}}\n{"type":"result","subtype":"success","is_error":false}')
        self.assertEqual(parsed["model_status"], "failed")
        self.assertEqual(parsed["infrastructure_failure"], "authentication")

    def test_service_and_network_failures_are_blocked(self):
        self.runner()
        grading = importlib.import_module("grading")
        for message, category in (("tls handshake eof", "network"), ("rate_limit_error", "service"), ("service_unavailable", "service")):
            with self.subTest(category=category, message=message):
                parsed = grading.parse_transcript("codex", json.dumps({"type": "turn.failed", "error": {"message": message}}))
                execution = grading.classify_execution({"status": "timeout"}, parsed)
                self.assertEqual(execution, {"status": "blocked", "failure_category": category})

    def test_stderr_network_setup_failure_without_model_events_is_blocked(self):
        self.runner()
        grading = importlib.import_module("grading")
        parsed = grading.parse_transcript("codex", "")
        execution = grading.classify_execution({"status": "timeout"}, parsed, "failed to connect to websocket: tls handshake eof")
        self.assertEqual(execution, {"status": "blocked", "failure_category": "network"})

    def test_incomplete_execution_does_not_grade_unmodified_fixture_as_failure(self):
        self.runner()
        grading = importlib.import_module("grading")
        for status in ("unavailable", "blocked", "process_failed", "timeout", "launch_error", "output_limit"):
            with self.subTest(status=status):
                self.assertEqual(grading.aggregate_outcome(status, "unknown", [{"status": "fail"}]), "unknown")
        self.assertEqual(grading.aggregate_outcome("completed", "completed", [{"status": "fail"}]), "fail")

    def test_normal_assistant_prose_cannot_spoof_an_auth_failure(self):
        self.runner()
        grading = importlib.import_module("grading")
        parsed = grading.parse_transcript("claude", '{"type":"result","subtype":"success","is_error":false,"result":"Not logged in is the expected UI message."}')
        self.assertIsNone(parsed["infrastructure_failure"])
        self.assertEqual(parsed["model_status"], "completed")

    def test_ready_probe_then_fake_claude_auth_failure_is_unknown_not_task_fail(self):
        runner = self.runner()
        import argparse
        output = self.root / "artifacts"
        output.mkdir()
        args = argparse.Namespace(model="default", timeout=1, max_output_bytes=10000, auth_mode="isolated")
        raw = json.dumps({"type": "result", "subtype": "success", "is_error": True, "result": "Not logged in"})
        fake = [sys.executable, "-c", "print(" + repr(raw) + "); raise SystemExit(1)"]
        with patch.object(runner, "probe_agent", return_value={"ready": True, "executable": sys.executable}), patch.object(runner, "agent_command", return_value=fake):
            result = runner.run_trial("claude", None, "baseline", "authorized-maintenance", 1, args, output)
        self.assertEqual(result["phases"][0]["process"]["status"], "process_failed")
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["execution"]["failure_category"], "authentication")
        self.assertEqual(result["objective_outcome"], "unknown")
        self.assertEqual(result["outcome"], "unknown")

    def test_missing_readiness_never_launches_fake_model_or_passes(self):
        runner = self.runner()
        import argparse
        args = argparse.Namespace(model="default", timeout=1, max_output_bytes=10000, auth_mode="isolated")
        output = self.root / "artifacts"
        output.mkdir()
        with patch.object(runner, "probe_agent", return_value={"installed": True}), patch.object(runner, "run_process") as fake:
            result = runner.run_trial("codex", None, "baseline", "vague-intake", 1, args, output)
        fake.assert_not_called()
        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["objective_outcome"], "unknown")


if __name__ == "__main__":
    unittest.main()
