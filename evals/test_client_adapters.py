"""Real-process client adapter checks; all installs and packages use temporary homes."""

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
NODE = shutil.which("node")
HOOK_COMMAND = 'python3 "${PLUGIN_ROOT}/hooks/codex-session-start.py"'
DIRECT_RUNTIME_FILES = {
    "sdc-cli.py", "scripts/sdc-runtime-context.py", "scripts/sdc_evidence.py",
    "scripts/sdc-task-brief.py", "scripts/sdc-review-package.py",
}


class ClientAdaptersTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sdc-adapters-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.home.mkdir()
        self.repo = self.base / "source"
        self.repo.mkdir()
        entries = [
            "bin", "scripts", "hooks", "skills", "sdc-references", "commands",
            ".claude-plugin", ".codex-plugin", ".agents", "docs", "evals",
            "package.json", "sdc-cli.py", ".npmignore", "README.md",
            "CHANGELOG.md", "SECURITY.md", "PRIVACY.md", "LICENSE",
        ]
        for name in entries:
            src, dest = ROOT / name, self.repo / name
            if src.is_dir():
                shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            else:
                shutil.copy2(src, dest)
        self.tools = self.base / "tools"
        self.tools.mkdir()
        # Never invoke a real Claude CLI, even if it ignores the fixture HOME.
        claude = self.tools / "claude"
        claude.write_text("#!/bin/sh\nexit 127\n")
        claude.chmod(0o755)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("SDC_")}
        self.env.update({
            "HOME": str(self.home), "USERPROFILE": str(self.home),
            "CODEX_HOME": str(self.home / ".codex"),
            "CLAUDE_CONFIG_DIR": str(self.home / ".claude"),
            "XDG_CONFIG_HOME": str(self.home / ".config"),
            "npm_config_cache": str(self.home / ".npm"),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PATH": str(self.tools) + os.pathsep + os.environ["PATH"],
        })
        self.run_process([NODE, "bin/install.js", "sync-public-skills"])
        self.marketplace = self.home / ".codex/local-marketplaces/sdc-local/plugins/sdc"
        version = json.loads((self.repo / "package.json").read_text())["version"]
        self.cache = self.home / ".codex/plugins/cache/sdc-local/sdc" / version

    def run_process(self, args, *, cwd=None, env=None, input="", success=True, timeout=30):
        result = subprocess.run(args, cwd=cwd or self.repo, env=env or self.env,
                                input=input, text=True, capture_output=True, timeout=timeout)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def install(self, value=None, claude=False, *, direct=False, hermes=False):
        env = dict(self.env)
        if value is not None:
            env["SDC_CODEX_HOOKS"] = value
        if direct:
            env["SDC_CODEX_DIRECT_SKILLS"] = "1"
        if claude:
            (self.home / ".claude/plugins").mkdir(parents=True, exist_ok=True)
        if hermes:
            (self.home / ".hermes/skills").mkdir(parents=True, exist_ok=True)
        return self.run_process([NODE, "bin/install.js"], env=env)

    def hook_payload(self, *, plugin=None, project=None, raw=None, env=None):
        plugin = plugin or self.repo
        script = plugin / "hooks/codex-session-start.py"
        self.assertTrue(script.is_file(), "native Codex hook adapter must exist")
        result = self.run_process([sys.executable, str(script)], cwd=project or self.base,
                                  env=env, input=raw if raw is not None else json.dumps({
                                      "hook_event_name": "SessionStart", "source": "compact",
                                      "session_id": "adapter-session",
                                  }), timeout=7)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(set(payload), {"hookSpecificOutput"})
        hook = payload["hookSpecificOutput"]
        self.assertEqual(set(hook), {"hookEventName", "additionalContext"})
        self.assertEqual(hook["hookEventName"], "SessionStart")
        self.assertIsInstance(hook["additionalContext"], str)
        self.assertLessEqual(len(hook["additionalContext"]), 4000)
        return hook["additionalContext"]

    def make_project(self):
        project = self.base / "project with spaces"
        project.mkdir()
        self.run_process([sys.executable, str(self.repo / "sdc-cli.py"), "init"], cwd=project)
        self.run_process([sys.executable, str(self.repo / "sdc-cli.py"), "change",
                          "adapter-context", "--confirmed-intake"], cwd=project)
        change = next((project / ".sdc/changes/active").iterdir())
        return project, change.name

    def assert_direct_runtime(self, root, client):
        project = self.base / f"{client} direct project with spaces"
        project.mkdir()
        self.run_process([sys.executable, str(root / "sdc-cli.py"), "init"], cwd=project)
        self.run_process([sys.executable, str(root / "sdc-cli.py"), "change",
                          "direct-context", "--confirmed-intake"], cwd=project)
        change = next((project / ".sdc/changes/active").iterdir())
        result = self.run_process([sys.executable, str(root / "scripts/sdc-runtime-context.py"),
                                   "session-context", "--client", client], cwd=project)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema"], "sdc.session-context/v1")
        self.assertIn(change.name, payload["additionalContext"])
        self.assertFalse((root / ".sdc").exists())
        self.assertEqual({p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()},
                         DIRECT_RUNTIME_FILES)

    def direct_layout_sentinels(self):
        sentinels = []
        for root in (self.home / ".agents", self.home / ".codex", self.home / ".hermes/skills"):
            for name in ("scripts/user-helper.py", "skills/user-skill/SKILL.md"):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("User-owned content\n")
                sentinels.append(path)
        return sentinels

    def test_hermes_direct_layout_runs_helpers_from_project_cwd(self):
        self.install(hermes=True)
        self.assert_direct_runtime(self.home / ".hermes/skills/sdc-runtime", "generic")

    def test_codex_direct_layout_runs_helpers_from_project_cwd(self):
        self.install(direct=True)
        self.assert_direct_runtime(self.home / ".agents/sdc-runtime", "codex")

    def test_direct_runtime_reinstall_replaces_only_owned_helpers(self):
        sentinels = self.direct_layout_sentinels()
        self.install(direct=True, hermes=True)
        roots = (self.home / ".agents/sdc-runtime", self.home / ".hermes/skills/sdc-runtime")
        for root in roots:
            (root / "scripts").mkdir(parents=True, exist_ok=True)
            (root / "scripts/obsolete-helper.py").write_text("stale\n")
            (root / "scripts/sdc_evidence.py").write_text("stale\n")
        self.install(direct=True, hermes=True)
        for root in roots:
            self.assertFalse((root / "scripts/obsolete-helper.py").exists())
            for name in DIRECT_RUNTIME_FILES:
                self.assertEqual((root / name).read_bytes(), (self.repo / name).read_bytes())
        for path in sentinels:
            self.assertEqual(path.read_text(), "User-owned content\n")

    def test_uninstall_removes_direct_runtimes_without_touching_user_files(self):
        sentinels = self.direct_layout_sentinels()
        self.install(direct=True, hermes=True)
        roots = (self.home / ".agents/sdc-runtime", self.home / ".codex/sdc-runtime",
                 self.home / ".hermes/skills/sdc-runtime")
        for root in roots:
            root.mkdir(parents=True, exist_ok=True)
            (root / "legacy-helper.py").write_text("stale runtime\n")
        self.run_process([NODE, "bin/install.js", "uninstall"])
        for root in roots:
            self.assertFalse(root.exists(), str(root))
        for path in sentinels:
            self.assertEqual(path.read_text(), "User-owned content\n")

    def test_codex_direct_to_plugin_removes_runtime_but_preserves_hermes(self):
        sentinels = self.direct_layout_sentinels()
        self.install(direct=True, hermes=True)
        roots = (self.home / ".agents/sdc-runtime", self.home / ".codex/sdc-runtime")
        for root in roots:
            root.mkdir(parents=True, exist_ok=True)
            (root / "legacy-helper.py").write_text("stale runtime\n")
        self.install()
        for root in roots:
            self.assertFalse(root.exists(), str(root))
        self.assertFalse((self.home / ".agents/skills/sdc-core").exists())
        self.assertTrue((self.cache / "scripts/sdc-runtime-context.py").is_file())
        self.assert_direct_runtime(self.home / ".hermes/skills/sdc-runtime", "generic")
        for path in sentinels:
            self.assertEqual(path.read_text(), "User-owned content\n")

    def test_source_manifest_disables_implicit_claude_hook_discovery(self):
        manifest = json.loads((self.repo / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest.get("hooks"), [], "source Codex manifest must override Claude autodiscovery")

    def test_workflow_helpers_resolve_from_plugin_not_target_project(self):
        paths = ["commands/" + name + ".md" for name in ("sdc", "change", "plan", "apply", "check")]
        paths += ["skills/sdc-spec/SKILL.md", "sdc-references/runtime-context.md"]
        for name in paths:
            with self.subTest(path=name):
                content = (self.repo / name).read_text()
                self.assertNotIn("python3 scripts/sdc-runtime-context.py", content)
                self.assertIn('python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py"', content)
                self.assertIn("target project", content)

    def test_default_and_nonliteral_opt_in_keep_portable_adapter(self):
        for value in (None, "0", "true", "yes"):
            with self.subTest(value=value):
                self.install(value)
                for plugin in (self.marketplace, self.cache):
                    self.assertFalse((plugin / "hooks").exists())
                    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
                    self.assertFalse(manifest.get("hooks"))
                    self.assertTrue((plugin / "scripts/sdc-runtime-context.py").is_file())
                    self.assertTrue((plugin / "skills/sdc-core/SKILL.md").is_file())

    def test_native_opt_in_uses_codex_config_and_preserves_trust_and_claude(self):
        config = self.home / ".codex/config.toml"
        config.parent.mkdir()
        original = '[features]\nhooks = false\n\n[projects."/fixture"]\ntrust_level = "untrusted"\n'
        config.write_text(original)
        result = self.install("1", claude=True)
        self.assertIn("/hooks", result.stdout)
        self.assertIn("trust", result.stdout.lower())
        self.assertTrue(config.read_text().startswith(original.rstrip()))
        for plugin in (self.marketplace, self.cache):
            manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
            self.assertEqual(manifest.get("hooks"), "./hooks/codex.json")
            self.assertEqual({p.name for p in (plugin / "hooks").iterdir()},
                             {"codex.json", "codex-session-start.py"})
            native = json.loads((plugin / "hooks/codex.json").read_text())
            self.assertEqual(set(native["hooks"]), {"SessionStart"})
            group = native["hooks"]["SessionStart"][0]
            for source in ("startup", "resume", "clear", "compact"):
                self.assertIsNotNone(re.fullmatch(group["matcher"], source))
            handler = group["hooks"][0]
            self.assertEqual(handler["command"], HOOK_COMMAND)
            self.assertEqual(handler["type"], "command")
            self.assertEqual(handler["timeout"], 5)
            self.assertEqual(handler["additionalContextLimit"], 4000)
            self.assertNotIn("shell", handler)
        claude = self.home / ".claude/plugins/marketplaces/sdc-local"
        self.assertEqual((claude / "hooks/hooks.json").read_bytes(), (self.repo / "hooks/hooks.json").read_bytes())
        self.assertEqual((claude / "hooks/session-start").read_bytes(), (self.repo / "hooks/session-start").read_bytes())
        self.install()
        self.assertFalse((self.cache / "hooks").exists(), "opting back out must remove stale native hooks")
        self.assertFalse((self.marketplace / "hooks").exists())

    def test_native_hook_wraps_portable_context_for_all_start_sources(self):
        self.install("1")
        project, change = self.make_project()
        runtime = self.cache / "scripts/sdc-runtime-context.py"
        portable = json.loads(self.run_process([sys.executable, str(runtime), "session-context",
                                               "--client", "codex", "--session-id", "adapter-session"],
                                              cwd=project).stdout)
        self.assertEqual(portable["schema"], "sdc.session-context/v1")
        self.assertNotIn("hookSpecificOutput", portable)
        for source in ("startup", "resume", "clear", "compact"):
            raw = json.dumps({"hook_event_name": "SessionStart", "source": source,
                              "session_id": "adapter-session"})
            context = self.hook_payload(plugin=self.cache, project=project, raw=raw)
            self.assertIn(change, context)
            self.assertEqual(context, portable["additionalContext"])
        claude = self.run_process(["bash", str(self.repo / "hooks/session-start")], cwd=project,
                                  input=json.dumps({"session_id": "adapter-session"}))
        self.assertEqual(json.loads(claude.stdout)["hookSpecificOutput"]["additionalContext"],
                         portable["additionalContext"])

    def test_native_command_from_config_runs_with_spaces_in_plugin_root(self):
        self.install("1")
        plugin = self.base / "plugin with spaces"
        shutil.copytree(self.cache, plugin)
        config = plugin / "hooks/codex.json"
        self.assertTrue(config.exists(), "opt-in must supply a native config")
        command = json.loads(config.read_text())["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        env = dict(self.env, PLUGIN_ROOT=str(plugin))
        result = self.run_process(["sh", "-c", command], env=env, cwd=self.base,
                                  input=json.dumps({"hook_event_name": "SessionStart", "source": "compact"}))
        self.assertIn("runtime context unavailable", json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"])

    def test_native_hook_invalid_input_and_no_project_fail_open(self):
        for raw in ("", "{", "[]", "null", '"text"', "x" * 65537,
                    '{"hook_event_name":"Stop"}', '{"source":"unknown"}'):
            with self.subTest(raw=raw[:40]):
                self.assertIn("runtime context unavailable", self.hook_payload(raw=raw))
        env = dict(self.env, SDC_RUNTIME_FORCE_HOOK_FAILURE="1")
        self.assertIn("manual fallback", self.hook_payload(env=env).lower())

    def test_native_identity_does_not_inherit_environment_without_opt_in(self):
        project, _ = self.make_project()
        env = dict(self.env, SDC_SESSION_ID="environment-session")
        raw = json.dumps({"hook_event_name": "SessionStart", "session_id": 7})
        self.assertNotIn("environment-session", self.hook_payload(project=project, raw=raw, env=env))
        env["SDC_ALLOW_ENV_SESSION_ID"] = "1"
        self.assertIn("Session id: environment-session", self.hook_payload(project=project, raw=raw, env=env))
        raw = json.dumps({"hook_event_name": "SessionStart", "session_id": "stdin-session"})
        self.assertIn("Session id: stdin-session", self.hook_payload(project=project, raw=raw, env=env))

    def test_compact_and_resume_reuse_only_the_event_session_selection(self):
        project, change = self.make_project()
        self.run_process([sys.executable, str(self.repo / "sdc-cli.py"), "change",
                          "other-context", "--confirmed-intake"], cwd=project)
        self.run_process([sys.executable, str(self.repo / "scripts/sdc-runtime-context.py"),
                          "select", "--change", change, "--session-id", "selected-session"], cwd=project)
        for source in ("compact", "resume"):
            raw = json.dumps({"hook_event_name": "SessionStart", "source": source,
                              "session_id": "selected-session"})
            self.assertIn(f"Active change: {change}", self.hook_payload(project=project, raw=raw))
        raw = json.dumps({"hook_event_name": "SessionStart", "source": "compact"})
        self.assertIn("runtime context unavailable", self.hook_payload(project=project, raw=raw))

    def test_native_hook_bounds_context_and_recovers_from_helper_failures(self):
        script = self.repo / "hooks/codex-session-start.py"
        self.assertTrue(script.is_file(), "native adapter must exist")
        helper = self.repo / "scripts/sdc-runtime-context.py"
        helper.write_text('import json\nprint(json.dumps({"additionalContext": "x" * 20000}))\n')
        self.assertEqual(len(self.hook_payload()), 4000)
        for body in ('print("not json")\n', 'print("[]")\n',
                     'print(\'{"additionalContext": []}\')\n', 'raise SystemExit(2)\n',
                     'import time\ntime.sleep(15)\n'):
            helper.write_text(body)
            self.assertIn("runtime context unavailable", self.hook_payload())
        helper.unlink()
        self.assertIn("runtime context unavailable", self.hook_payload())

    def test_audit_accepts_explicit_native_config_and_rejects_claude_payload(self):
        self.assertTrue((self.repo / "hooks/codex.json").exists(), "native config must exist")
        manifest_path = self.repo / ".codex-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text())
        native = json.loads((self.repo / "hooks/codex.json").read_text())
        for value in ([], "./hooks/codex.json", ["./hooks/codex.json"], native, [native]):
            manifest["hooks"] = value
            manifest_path.write_text(json.dumps(manifest))
            self.run_process([NODE, "scripts/audit-release.mjs"])
        for value in ("./hooks/hooks.json", "./../outside.json", {"hooks": {"Stop": []}}):
            manifest["hooks"] = value
            manifest_path.write_text(json.dumps(manifest))
            result = self.run_process([NODE, "scripts/audit-release.mjs"], success=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Codex", result.stderr)
        for field, value in (("shell", "bash"), ("timeout", 60), ("additionalContextLimit", 100000)):
            invalid = json.loads(json.dumps(native))
            invalid["hooks"]["SessionStart"][0]["hooks"][0][field] = value
            manifest["hooks"] = invalid
            manifest_path.write_text(json.dumps(manifest))
            result = self.run_process([NODE, "scripts/audit-release.mjs"], success=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("bounded native adapter", result.stderr)

    def test_packages_are_rootless_deterministic_and_mode_specific(self):
        project, change = self.make_project()
        for value in (None, "1"):
            env = dict(self.env)
            if value:
                env["SDC_CODEX_HOOKS"] = value
            outputs = [self.base / f"plugin-{value}-{i}.zip" for i in range(2)]
            for output in outputs:
                self.run_process([sys.executable, "scripts/package-codex-plugin.py", "--allow-dirty",
                                  "--output", str(output)], env=env, timeout=60)
                digest = hashlib.sha256(output.read_bytes()).hexdigest()
                self.assertEqual(output.with_suffix(".zip.sha256").read_text(), f"{digest}  {output.name}\n")
            self.assertEqual(outputs[0].read_bytes(), outputs[1].read_bytes())
            with zipfile.ZipFile(outputs[0]) as archive:
                names = archive.namelist()
                self.assertIn(".codex-plugin/plugin.json", names)
                self.assertIn("skills/sdc-core/SKILL.md", names)
                self.assertFalse(any(n.startswith(("sdc/", ".claude/", ".claude-plugin/", "commands/")) for n in names))
                manifest = json.loads(archive.read(".codex-plugin/plugin.json"))
                if value:
                    self.assertEqual(manifest.get("hooks"), "./hooks/codex.json")
                    self.assertEqual({n for n in names if n.startswith("hooks/")},
                                     {"hooks/codex.json", "hooks/codex-session-start.py"})
                else:
                    self.assertFalse(manifest.get("hooks"))
                    self.assertFalse(any(n.startswith("hooks/") for n in names))
                extracted = self.base / f"extracted-{value}"
                archive.extractall(extracted)
            runtime = extracted / "scripts/sdc-runtime-context.py"
            result = self.run_process([sys.executable, str(runtime), "session-context", "--client", "codex"],
                                      cwd=project)
            self.assertIn(change, json.loads(result.stdout)["additionalContext"])
            if value:
                self.assertIn(change, self.hook_payload(plugin=extracted, project=project))


if __name__ == "__main__":
    unittest.main()
