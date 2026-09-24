"""Read-only installation diagnostics, exercised through real Node processes."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCTOR = ROOT / "scripts/sdc-doctor.mjs"
NODE = shutil.which("node")
PUBLIC = ("core", "init", "change", "plan", "apply", "check", "archive", "harness")
ADVANCED = ("spec", "implement", "review", "test", "quality", "validate")
HELPERS = ("sdc-cli.py", "scripts/sdc-runtime-context.py", "scripts/sdc_evidence.py",
           "scripts/sdc-task-brief.py", "scripts/sdc-review-package.py",
           "scripts/sdc_compact.py", "scripts/sdc_findings.py")


@unittest.skipUnless(NODE, "Node.js is required")
class InstallDiagnosticsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="sdc doctor spaces-")
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.home = self.base / "home"
        self.source = self.base / "source"
        self.home.mkdir()
        self.source.mkdir()
        self.env = {k: v for k, v in os.environ.items()
                    if not k.startswith(("SDC_", "NODE_"))}
        self.env.update(HOME=str(self.home), USERPROFILE=str(self.home),
                        CODEX_HOME=str(self.home / ".codex"),
                        CLAUDE_CONFIG_DIR=str(self.home / ".claude"),
                        PYTHONDONTWRITEBYTECODE="1")
        self.put_json(self.source / "package.json", {"name": "sdc-spec", "version": "1.3.0",
                                                     "type": "module"})
        self.put_json(self.source / ".codex-plugin/plugin.json",
                      {"name": "sdc", "version": "1.3.0", "skills": "./skills/", "hooks": []})
        self.put_json(self.source / ".claude-plugin/plugin.json",
                      {"name": "sdc", "version": "1.3.0", "commands": "./commands/",
                       "skills": [f"./skills/sdc-{x}" for x in ADVANCED]})
        for name in HELPERS:
            self.put(self.source / name, f"# fixture {name}\n")
        self.put(self.source / "sdc-references/runtime-context.md", "Runtime contract\n")
        for name in PUBLIC + ADVANCED:
            capability = "sdc" if name == "core" else f"sdc-{name}"
            self.put(self.source / f"skills/sdc-{name}/SKILL.md",
                     f"---\nname: {capability}\ndescription: fixture\n---\n{capability}\n")
        for name in PUBLIC:
            name = "sdc" if name == "core" else name
            self.put(self.source / f"commands/{name}.md", f"---\ndescription: {name}\n---\n{name}\n")

    def put(self, path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def put_json(self, path, value):
        self.put(path, json.dumps(value))

    def snapshot(self):
        result = {}
        for path in sorted(self.base.rglob("*")):
            if path.is_symlink():
                result[str(path)] = ("link", os.readlink(path))
            elif path.is_file():
                result[str(path)] = (path.stat().st_mtime_ns,
                                     hashlib.sha256(path.read_bytes()).hexdigest())
            else:
                result[str(path)] = "directory"
        return result

    def run_doctor(self, *args, success=True, defaults=False, api=False, script=DOCTOR):
        self.assertTrue(script.is_file(), "missing read-only scripts/sdc-doctor.mjs sidecar")
        command = [NODE, str(script), "--json"]
        if not defaults:
            command += ["--home", str(self.home), "--source", str(self.source)]
        command += list(args)
        if api:
            command = [NODE, "--input-type=module", "-e",
                       "const {diagnose}=await import(process.argv[1]);"
                       "const r=diagnose(JSON.parse(process.argv[2]));"
                       "console.log(JSON.stringify(r));process.exitCode=r.ok?0:1;",
                       DOCTOR.as_uri(), json.dumps({"home": str(self.home),
                                                   "sourceRoot": str(self.source)})]
        before = self.snapshot()
        result = subprocess.run(command, cwd=self.base, env=self.env, text=True,
                                capture_output=True, timeout=15)
        self.assertEqual(self.snapshot(), before, "doctor must not modify source or home")
        self.assertEqual(result.stderr, "", result.stderr)
        self.assertEqual(result.returncode, 0 if success else 1, result.stdout)
        self.assertTrue(result.stdout.startswith("{"), result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(set(payload), {"schema", "ok", "issues", "installations"})
        self.assertEqual(payload["schema"], "sdc.install-diagnostics/v1")
        self.assertEqual(payload["ok"], success)
        self.assertEqual(payload["ok"], not any(i["severity"] == "error" for i in payload["issues"]))
        for issue in payload["issues"]:
            self.assertTrue(issue["code"])
            self.assertTrue(issue["message"])
            self.assertTrue(issue["action"])
        return payload

    def codes(self, payload):
        return {issue["code"] for issue in payload["issues"]}

    def test_existing_check_router_forwards_arguments_and_exit_status(self):
        self.codex()
        command = [NODE, str(ROOT / "bin/sdc.js"), "check", "installation", "--json",
                   "--home", str(self.home), "--source", str(self.source)]
        before = self.snapshot()
        for client, expected in (("codex", 0), ("claude", 1)):
            result = subprocess.run([*command, "--client", client], cwd=self.base,
                                    env=self.env, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, expected, result.stdout)
            self.assertEqual(result.stderr, "")
            self.assertEqual(json.loads(result.stdout)["ok"], expected == 0)
        self.assertEqual(self.snapshot(), before)

    def codex(self, market="team-local", enabled=True):
        marketplace = self.home / f".codex/local-marketplaces/{market}"
        plugin = marketplace / "plugins/sdc"
        cache = self.home / f".codex/plugins/cache/{market}/sdc/1.3.0"
        shutil.copytree(self.source, plugin)
        shutil.copytree(self.source, cache)
        self.put_json(marketplace / ".agents/plugins/marketplace.json", {
            "name": market, "plugins": [{"name": "sdc", "source": {
                "source": "local", "path": "./plugins/sdc"}}]})
        self.put(self.home / ".codex/config.toml",
                 f'[marketplaces.{market}]\nsource_type = "local"\n'
                 f'source = {json.dumps(str(marketplace))}\n'
                 f'[plugins."sdc@{market}"]\nenabled = {str(enabled).lower()}\n')
        return plugin, cache

    def claude(self, *, public_skills=False, marketplace_source="./"):
        market = self.home / ".claude/plugins/marketplaces/team-local"
        plugin = market / marketplace_source
        cache = self.home / ".claude/plugins/cache/team-local/sdc/1.3.0"
        for root in (plugin, cache):
            shutil.copytree(self.source, root)
            if not public_skills:
                for name in PUBLIC:
                    shutil.rmtree(root / f"skills/sdc-{name}")
        self.put_json(market / ".claude-plugin/marketplace.json", {
            "name": "team-local", "plugins": [{"name": "sdc", "source": marketplace_source}]})
        self.put_json(self.home / ".claude/settings.json", {
            "enabledPlugins": {"sdc@team-local": True, "unrelated@elsewhere": True},
            "env": {"SECRET": "NEVER_PRINT_SETTINGS_VALUE"}})
        self.put_json(self.home / ".claude/plugins/known_marketplaces.json", {
            "team-local": {"source": {"source": "directory", "path": str(market)},
                           "installLocation": str(market)},
            "elsewhere": {"installLocation": "/not/a/plugin"}})
        self.put_json(self.home / ".claude/plugins/installed_plugins.json", {
            "version": 2, "plugins": {"sdc@team-local": [
                {"scope": "user", "installPath": str(cache), "version": "1.3.0"}],
                "unrelated@elsewhere": [{"installPath": "/not/a/plugin"}]}})
        return plugin, cache

    def direct(self, client="hermes", legacy=False):
        if client == "hermes":
            parent = self.home / ".hermes/skills"
            skills = parent / ("sdc-spec" if legacy else "sdc")
        else:
            parent = self.home / (".codex" if legacy else ".agents")
            skills = parent / "skills"
        shutil.copytree(self.source / "skills", skills)
        shutil.copytree(self.source / "sdc-references", parent / "sdc-references")
        for name in HELPERS:
            target = parent / "sdc-runtime" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.source / name, target)
        return skills, parent / "sdc-runtime"

    def test_healthy_codex_follows_enabled_marketplace_and_exports_api(self):
        self.codex()
        cli = self.run_doctor()
        self.assertEqual(cli, self.run_doctor(api=True))
        self.assertEqual({x["client"] for x in cli["installations"]}, {"codex"})
        self.assertEqual({x["kind"] for x in cli["installations"]}, {"marketplace", "cache"})
        for item in cli["installations"]:
            self.assertEqual(item["fingerprint"], item["sourceFingerprint"])
            self.assertEqual(len(item["fingerprint"]), 64)

    def test_same_version_runtime_drift_is_blocking(self):
        _, cache = self.codex()
        self.put(cache / HELPERS[1], "# stale at same version\n")
        payload = self.run_doctor(success=False)
        self.assertIn("PAYLOAD_DRIFT", self.codes(payload))
        self.assertNotEqual(payload["installations"][-1]["fingerprint"],
                            payload["installations"][-1]["sourceFingerprint"])

    def test_reference_and_skill_drift_are_blocking(self):
        plugin, cache = self.codex()
        self.put(plugin / "sdc-references/runtime-context.md", "stale reference\n")
        self.put(cache / "skills/sdc-check/SKILL.md", "stale skill\n")
        payload = self.run_doctor(success=False)
        self.assertGreaterEqual(sum(i["code"] == "PAYLOAD_DRIFT" for i in payload["issues"]), 2)

    def test_missing_helper_is_actionable(self):
        _, cache = self.codex()
        (cache / HELPERS[2]).unlink()
        self.assertIn("MISSING_HELPER", self.codes(self.run_doctor(success=False)))

    def test_missing_enabled_cache_root_is_blocking(self):
        _, cache = self.codex()
        shutil.rmtree(cache)
        self.assertIn("MISSING_INSTALLATION", self.codes(self.run_doctor(success=False)))

    def test_ambiguous_cache_versions_are_not_silently_selected(self):
        _, cache = self.codex()
        shutil.copytree(cache, cache.parent / "0.9.0")
        self.assertIn("AMBIGUOUS_CACHE", self.codes(self.run_doctor(success=False)))

    def test_direct_codex_plus_plugin_is_duplicate(self):
        self.codex()
        self.direct("codex")
        self.assertIn("DUPLICATE_CAPABILITY", self.codes(self.run_doctor(success=False)))

    def test_old_codex_direct_skill_directory_is_inspected(self):
        self.direct("codex", legacy=True)
        payload = self.run_doctor()
        self.assertIn("LEGACY_LAYOUT", self.codes(payload))
        self.assertTrue(any(x["active"] for x in payload["installations"]))

    def test_hermes_sibling_runtime_and_references_are_supported(self):
        self.direct()
        payload = self.run_doctor("--client", "hermes")
        self.assertEqual({x["client"] for x in payload["installations"]}, {"hermes"})

    def test_hermes_missing_helper_is_blocking(self):
        _, runtime = self.direct()
        (runtime / HELPERS[-1]).unlink()
        self.assertIn("MISSING_HELPER", self.codes(self.run_doctor(success=False)))

    def test_hermes_old_and_current_direct_skills_are_duplicate(self):
        skills, _ = self.direct()
        shutil.copytree(skills, skills.parent / "sdc-spec")
        self.assertIn("DUPLICATE_CAPABILITY", self.codes(self.run_doctor(success=False)))

    def test_hermes_legacy_single_skill_is_not_overlooked(self):
        self.direct()
        self.put(self.home / ".hermes/skills/sdc-spec/SKILL.md",
                 (self.source / "skills/sdc-spec/SKILL.md").read_text())
        self.assertIn("DUPLICATE_CAPABILITY", self.codes(self.run_doctor(success=False)))

    def test_claude_enabled_registry_is_authoritative(self):
        _, cache = self.claude()
        payload = self.run_doctor("--client", "claude")
        self.assertNotIn("NEVER_PRINT_SETTINGS_VALUE", json.dumps(payload))
        self.assertTrue(any(x["path"] == str(cache.resolve()) and x["active"] for x in payload["installations"]))

    def test_claude_nonroot_commands_and_public_skills_are_duplicate(self):
        self.claude(public_skills=True, marketplace_source="./plugins/sdc")
        payload = self.run_doctor(success=False)
        duplicates = [i for i in payload["issues"] if i["code"] == "DUPLICATE_CAPABILITY"]
        self.assertEqual({i["capability"] for i in duplicates},
                         {"sdc" if name == "core" else f"sdc-{name}" for name in PUBLIC})

    def test_claude_additive_scan_deduplicates_the_same_skill_file(self):
        self.claude(marketplace_source="./plugins/sdc")
        self.run_doctor("--client", "claude")

    def test_claude_root_exception_allows_shared_codex_public_skills(self):
        self.claude(public_skills=True)
        self.run_doctor("--client", "claude")

    def test_claude_root_exception_compares_resolved_source_not_literal(self):
        self.claude(public_skills=True, marketplace_source="./.")
        self.run_doctor("--client", "claude")

    def test_claude_root_subset_selection_is_configuration_drift(self):
        plugin, cache = self.claude(public_skills=True)
        for folder in (cache, plugin):
            manifest = folder / ".claude-plugin/plugin.json"
            original = json.loads(manifest.read_text())
            for skills, selected in ((["./skills/sdc-spec"], {"spec"}),
                                     ("./skills/sdc-spec/", {"spec"}),
                                     ([f"./skills/sdc-{x}" for x in ADVANCED[:-1]],
                                      set(ADVANCED[:-1]))):
                with self.subTest(kind=folder.name, skills=skills):
                    self.put_json(manifest, {**original, "skills": skills})
                    payload = self.run_doctor("--client", "claude", success=False)
                    self.assertEqual(self.codes(payload), {"CONFIGURATION_DRIFT"})
                    drift, = payload["issues"]
                    self.assertEqual(drift["path"], str(manifest.resolve()))
                    self.assertEqual(drift["client"], "claude")
                    self.assertEqual(drift["missing"], sorted(
                        f"skills/sdc-{name}/SKILL.md" for name in set(ADVANCED) - selected))
                    self.assertEqual(drift["missingCount"], len(ADVANCED) - len(selected))
                    for item in payload["installations"]:
                        self.assertEqual(item["fingerprint"], item["sourceFingerprint"])
            self.put_json(manifest, original)

    def test_claude_root_selection_checks_additional_source_skills(self):
        self.put(self.source / "skills/sdc-extra/SKILL.md",
                 "---\nname: sdc-extra\n---\nAdditional source capability\n")
        manifest = self.source / ".claude-plugin/plugin.json"
        intended = json.loads(manifest.read_text())
        intended["skills"].append("./skills/sdc-extra")
        self.put_json(manifest, intended)
        _, cache = self.claude(public_skills=True)
        self.run_doctor("--client", "claude")
        self.put_json(cache / ".claude-plugin/plugin.json",
                      {**intended, "skills": [f"./skills/sdc-{x}" for x in ADVANCED]})
        payload = self.run_doctor("--client", "claude", success=False)
        self.assertEqual(self.codes(payload), {"CONFIGURATION_DRIFT"})
        drift, = payload["issues"]
        self.assertEqual(drift["missing"], ["skills/sdc-extra/SKILL.md"])
        self.assertEqual(drift["missingCount"], 1)

    def test_claude_root_equivalent_selection_is_not_drift_or_duplicate(self):
        _, cache = self.claude(public_skills=True)
        manifest = cache / ".claude-plugin/plugin.json"
        data = json.loads(manifest.read_text())
        data["skills"] = [f"./skills/sdc-{x}/" for x in reversed(ADVANCED)]
        data["skills"].append("./skills/sdc-spec")
        data["description"] = "Metadata is not loading configuration"
        self.put_json(manifest, data)
        self.run_doctor("--client", "claude")

    def test_claude_root_default_selection_still_loads_advanced_only_payload(self):
        _, cache = self.claude()
        manifest = cache / ".claude-plugin/plugin.json"
        original = json.loads(manifest.read_text())
        for value in (None, [], ["./skills/"], "./skills/"):
            with self.subTest(skills=value):
                data = {**original, "skills": value}
                if value is None:
                    data.pop("skills")
                self.put_json(manifest, data)
                self.run_doctor("--client", "claude")

    def test_claude_nonroot_subset_selection_remains_additive(self):
        _, cache = self.claude(marketplace_source="./plugins/sdc")
        manifest = cache / ".claude-plugin/plugin.json"
        original = json.loads(manifest.read_text())
        for value in (["./skills/sdc-spec"], "./skills/sdc-spec", []):
            with self.subTest(skills=value):
                self.put_json(manifest, {**original, "skills": value})
                self.run_doctor("--client", "claude")

    def test_claude_nonroot_subset_selection_keeps_public_duplicates(self):
        _, cache = self.claude(public_skills=True, marketplace_source="./plugins/sdc")
        manifest = cache / ".claude-plugin/plugin.json"
        data = json.loads(manifest.read_text())
        data["skills"] = ["./skills/sdc-spec"]
        self.put_json(manifest, data)
        payload = self.run_doctor("--client", "claude", success=False)
        self.assertEqual(self.codes(payload), {"DUPLICATE_CAPABILITY"})
        self.assertEqual({i["capability"] for i in payload["issues"]},
                         {"sdc" if name == "core" else f"sdc-{name}" for name in PUBLIC})
        self.assertTrue(all(i["count"] == 2 for i in payload["issues"]))

    def test_claude_root_explicit_public_skill_still_duplicates_command(self):
        plugin, cache = self.claude(public_skills=True)
        for folder in (plugin, cache):
            manifest = folder / ".claude-plugin/plugin.json"
            data = json.loads(manifest.read_text())
            data["skills"].append("./skills/sdc-init")
            self.put_json(manifest, data)
        payload = self.run_doctor("--client", "claude", success=False)
        self.assertEqual({i["capability"] for i in payload["issues"]
                          if i["code"] == "DUPLICATE_CAPABILITY"}, {"sdc-init"})

    def test_claude_root_without_specific_directories_keeps_default_scan(self):
        plugin, cache = self.claude(public_skills=True)
        for value in (None, [], ["./skills/"], "./skills/"):
            with self.subTest(skills=value):
                for folder in (plugin, cache):
                    manifest = folder / ".claude-plugin/plugin.json"
                    data = json.loads(manifest.read_text())
                    if value is None:
                        data.pop("skills", None)
                    else:
                        data["skills"] = value
                    self.put_json(manifest, data)
                payload = self.run_doctor("--client", "claude", success=False)
                self.assertIn("DUPLICATE_CAPABILITY", self.codes(payload))
                self.assertNotIn("INVALID_REGISTRY", self.codes(payload))

    def test_claude_malformed_skill_path_field_cannot_claim_root_exception(self):
        plugin, cache = self.claude(public_skills=True)
        for value in (None, False, {}):
            with self.subTest(skills=value):
                for folder in (plugin, cache):
                    manifest = folder / ".claude-plugin/plugin.json"
                    data = json.loads(manifest.read_text())
                    data["skills"] = value
                    self.put_json(manifest, data)
                self.assertIn("INVALID_REGISTRY", self.codes(
                    self.run_doctor("--client", "claude", success=False)))

    def test_claude_cached_marketplace_cannot_forge_root_provenance(self):
        _, cache = self.claude(public_skills=True, marketplace_source="./plugins/sdc")
        self.put_json(cache / ".claude-plugin/marketplace.json", {
            "name": "team-local", "plugins": [{"name": "sdc", "source": "./"}]})
        self.assertIn("DUPLICATE_CAPABILITY", self.codes(self.run_doctor(success=False)))

    def test_claude_root_exception_is_not_inherited_by_legacy_copy(self):
        _, cache = self.claude(public_skills=True)
        legacy = self.home / ".claude/plugins/sdc-spec"
        shutil.copytree(cache, legacy)
        payload = self.run_doctor("--client", "claude", success=False)
        duplicate = next(i for i in payload["issues"]
                         if i["code"] == "DUPLICATE_CAPABILITY" and i["capability"] == "sdc-init")
        self.assertEqual(set(duplicate["paths"]), {
            str((cache / "commands/init.md").resolve()),
            str((legacy / "commands/init.md").resolve()),
            str((legacy / "skills/sdc-init/SKILL.md").resolve())})

    def test_claude_root_exception_does_not_hide_direct_skill_duplicate(self):
        self.claude(public_skills=True)
        self.put(self.home / ".claude/skills/sdc-init/SKILL.md",
                 (self.source / "skills/sdc-init/SKILL.md").read_text())
        payload = self.run_doctor("--client", "claude", success=False)
        duplicate = next(i for i in payload["issues"]
                         if i["code"] == "DUPLICATE_CAPABILITY" and i["capability"] == "sdc-init")
        self.assertEqual(duplicate["count"], 2)

    def test_claude_legacy_plugin_is_duplicate(self):
        _, cache = self.claude()
        shutil.copytree(cache, self.home / ".claude/plugins/sdc-spec")
        self.assertIn("DUPLICATE_CAPABILITY", self.codes(self.run_doctor(success=False)))

    def test_claude_missing_registry_install_path_does_not_fall_back_to_cache(self):
        self.claude()
        self.put_json(self.home / ".claude/plugins/installed_plugins.json", {
            "version": 2, "plugins": {"sdc@team-local": [{"scope": "user", "installPath":
                                                         str(self.home / "missing")}]}})
        self.assertIn("MISSING_INSTALLATION", self.codes(self.run_doctor(success=False)))

    def test_none_diagnosed_is_an_error_even_if_other_plugins_exist(self):
        self.put(self.home / ".codex/config.toml", '[plugins."other@example"]\nenabled = true\n')
        self.put_json(self.home / ".claude/settings.json", {"enabledPlugins": {"other@x": True}})
        self.assertIn("NO_INSTALLATIONS", self.codes(self.run_doctor(success=False)))

    def test_explicit_missing_client_errors_without_requiring_all_clients(self):
        self.codex()
        self.run_doctor()
        self.assertIn("CLIENT_MISSING", self.codes(self.run_doctor("--client", "hermes", success=False)))

    def test_disabled_plugin_does_not_count_as_active(self):
        self.codex(enabled=False)
        self.assertIn("NO_INSTALLATIONS", self.codes(self.run_doctor(success=False)))

    def test_invalid_json_is_structured_and_does_not_leak_contents(self):
        self.claude()
        self.put(self.home / ".claude/settings.json", '{"SECRET":"NEVER_PRINT_SETTINGS_VALUE",')
        payload = self.run_doctor(success=False)
        self.assertIn("INVALID_JSON", self.codes(payload))
        self.assertNotIn("NEVER_PRINT_SETTINGS_VALUE", json.dumps(payload))

    def test_invalid_json_shape_is_blocking(self):
        self.claude()
        self.put_json(self.home / ".claude/plugins/installed_plugins.json", [])
        self.assertIn("INVALID_REGISTRY", self.codes(self.run_doctor(success=False)))

    def test_missing_source_is_structured(self):
        self.codex()
        shutil.rmtree(self.source)
        self.assertIn("MISSING_ROOT", self.codes(self.run_doctor(success=False)))

    def test_missing_home_is_structured(self):
        shutil.rmtree(self.home)
        self.assertIn("MISSING_ROOT", self.codes(self.run_doctor(success=False)))

    def test_broken_symlink_in_payload_is_actionable(self):
        _, cache = self.codex()
        target = cache / HELPERS[1]
        target.unlink()
        target.symlink_to(self.base / "missing helper")
        self.assertIn("UNSAFE_PATH", self.codes(self.run_doctor(success=False)))

    def test_escaping_symlink_is_not_followed(self):
        _, cache = self.codex()
        target = cache / "sdc-references"
        shutil.rmtree(target)
        secret = self.base / "outside"
        self.put(secret / "secret.md", "NEVER_PRINT_SETTINGS_VALUE")
        target.symlink_to(secret, target_is_directory=True)
        payload = self.run_doctor(success=False)
        self.assertIn("UNSAFE_PATH", self.codes(payload))
        self.assertNotIn("NEVER_PRINT_SETTINGS_VALUE", json.dumps(payload))

    def test_marketplace_relative_path_escape_is_rejected(self):
        plugin, _ = self.codex()
        manifest = plugin.parent.parent / ".agents/plugins/marketplace.json"
        data = json.loads(manifest.read_text())
        data["plugins"][0]["source"]["path"] = "../../../../outside"
        self.put_json(manifest, data)
        self.assertIn("UNSAFE_PATH", self.codes(self.run_doctor(success=False)))

    def test_symlink_loop_is_bounded(self):
        _, cache = self.codex()
        (cache / "skills/sdc-check/loop").symlink_to(cache / "skills", target_is_directory=True)
        self.assertIn("UNSAFE_PATH", self.codes(self.run_doctor(success=False)))

    def test_oversized_configuration_is_bounded(self):
        self.claude()
        self.put(self.home / ".claude/settings.json", " " * (4 * 1024 * 1024 + 1))
        self.assertIn("SCAN_LIMIT", self.codes(self.run_doctor(success=False)))

    def test_codex_toml_quoted_names_comments_and_unrelated_settings(self):
        self.codex()
        config = self.home / ".codex/config.toml"
        text = config.read_text().replace("[marketplaces.team-local]", "[marketplaces.'team-local']")
        self.put(config, 'secret = "NEVER_PRINT_SETTINGS_VALUE"\n' + text.replace(
            "enabled = true", "enabled = true # intentional comment"))
        self.assertNotIn("NEVER_PRINT_SETTINGS_VALUE", json.dumps(self.run_doctor()))

    def test_codex_malformed_relevant_toml_is_not_silently_ignored(self):
        self.codex()
        config = self.home / ".codex/config.toml"
        self.put(config, config.read_text().replace("enabled = true", 'enabled = "true"'))
        self.assertIn("INVALID_REGISTRY", self.codes(self.run_doctor(success=False)))

    def test_default_home_is_environment_and_default_source_is_package_root(self):
        # Default source must be the doctor's package, not cwd or a fixture source.
        shutil.rmtree(self.source)
        shutil.copytree(ROOT, self.source, ignore=shutil.ignore_patterns(
            ".git", "node_modules", "__pycache__", ".sdc", "dist"))
        self.codex()
        self.run_doctor(defaults=True)

    def test_invalid_cli_arguments_are_json_errors(self):
        for args in (("--client", "unknown"), ("--home",), ("--unexpected",)):
            with self.subTest(args=args):
                self.assertIn("INVALID_ARGUMENT", self.codes(self.run_doctor(*args, success=False)))

    def test_real_installer_codex_and_hermes_layouts(self):
        shutil.rmtree(self.source)
        shutil.copytree(ROOT, self.source, ignore=shutil.ignore_patterns(
            ".git", "node_modules", "__pycache__", ".sdc", "dist"))
        (self.home / ".hermes/skills").mkdir(parents=True)
        for command in ([NODE, "bin/install.js", "sync-public-skills"], [NODE, "bin/install.js"]):
            result = subprocess.run(command, cwd=self.source, env=self.env, capture_output=True,
                                    text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = self.run_doctor()
        self.assertEqual({x["client"] for x in payload["installations"]}, {"codex", "hermes"})

    def test_required_runtime_modules_participate_in_fingerprint(self):
        for name in ("sdc_compact.py", "sdc_findings.py"):
            self.put(self.source / "scripts" / name, "# new runtime module\n")
        _, cache = self.codex()
        self.put(cache / "scripts/sdc_compact.py", "# stale compact module\n")
        payload = self.run_doctor(success=False)
        self.assertIn("PAYLOAD_DRIFT", self.codes(payload))
        (cache / "scripts/sdc_findings.py").unlink()
        self.assertIn("MISSING_HELPER", self.codes(self.run_doctor(success=False)))

    def test_minimal_runtime_source_is_actionably_unavailable(self):
        self.direct()
        shutil.rmtree(self.source / "skills")
        shutil.rmtree(self.source / "sdc-references")
        (self.source / "package.json").unlink()
        payload = self.run_doctor(success=False)
        self.assertIn("SOURCE_UNAVAILABLE", self.codes(payload))
        self.assertTrue(any("--source" in x["action"] for x in payload["issues"]))

    def test_standalone_mjs_runs_without_package_json(self):
        self.codex()
        self.assertTrue(DOCTOR.is_file(), "missing standalone doctor module")
        script = self.base / "portable/scripts/sdc-doctor.mjs"
        script.parent.mkdir(parents=True)
        shutil.copy2(DOCTOR, script)
        result = subprocess.run([NODE, str(script), "--json", "--home", str(self.home),
                                 "--source", str(self.source)], env=self.env,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(result.stdout.startswith("{"), "standalone entrypoint did not produce JSON")
        self.assertTrue(json.loads(result.stdout)["ok"])

    def test_portal_source_without_package_json_can_compare_skills(self):
        self.codex()
        (self.source / "package.json").unlink()
        shutil.rmtree(self.source / "commands")
        self.run_doctor()

    def test_partial_legacy_skill_still_reports_duplicate_capability(self):
        self.codex()
        self.put(self.home / ".agents/skills/sdc-core/SKILL.md",
                 (self.source / "skills/sdc-core/SKILL.md").read_text())
        payload = self.run_doctor(success=False)
        self.assertIn("MISSING_HELPER", self.codes(payload))
        self.assertIn("DUPLICATE_CAPABILITY", self.codes(payload))

    def test_unrelated_direct_skill_and_file_do_not_affect_hermes(self):
        skills, _ = self.direct()
        self.put(skills / "unrelated/SKILL.md", "---\nname: other\n---\nUnrelated\n")
        self.put(skills / "unrelated-file.txt", "unrelated")
        self.run_doctor()

    def test_extra_owned_skill_payload_is_drift(self):
        _, cache = self.codex()
        self.put(cache / "skills/sdc-obsolete/SKILL.md", "---\nname: sdc-obsolete\n---\nObsolete\n")
        self.assertIn("PAYLOAD_DRIFT", self.codes(self.run_doctor(success=False)))

    def test_new_source_skill_payload_is_in_fingerprint(self):
        self.put(self.source / "skills/sdc-new/SKILL.md", "---\nname: sdc-new\n---\nNew\n")
        _, cache = self.codex()
        self.put(cache / "skills/sdc-new/SKILL.md", "---\nname: sdc-new\n---\nStale\n")
        self.assertIn("PAYLOAD_DRIFT", self.codes(self.run_doctor(success=False)))

    def test_command_drift_is_detected_for_claude(self):
        _, cache = self.claude()
        self.put(cache / "commands/init.md", "stale command")
        self.assertIn("PAYLOAD_DRIFT", self.codes(self.run_doctor(success=False)))

    def test_claude_source_requires_each_public_command(self):
        self.claude(public_skills=True)
        commands = {p.name: p.read_text() for p in (self.source / "commands").glob("*.md")}
        for missing in [(name,) for name in commands] + [tuple(commands)]:
            with self.subTest(missing=missing):
                try:
                    for name in missing:
                        (self.source / "commands" / name).unlink()
                    payload = self.run_doctor("--client", "claude", success=False)
                    self.assertEqual(self.codes(payload), {"SOURCE_UNAVAILABLE"})
                    self.assertTrue(all("--source" in i["action"] for i in payload["issues"]))
                finally:
                    for name in missing:
                        self.put(self.source / "commands" / name, commands[name])

    def test_claude_installed_profile_requires_each_public_command(self):
        plugin, cache = self.claude(public_skills=True)
        commands = {p.name: p.read_text() for p in (self.source / "commands").glob("*.md")}
        for folder in (plugin, cache):
            for missing in [(name,) for name in commands] + [tuple(commands)]:
                with self.subTest(folder=folder, missing=missing):
                    try:
                        for name in missing:
                            (folder / "commands" / name).unlink()
                        payload = self.run_doctor("--client", "claude", success=False)
                        self.assertEqual(self.codes(payload), {"MISSING_PAYLOAD"})
                        issue, = payload["issues"]
                        self.assertIn(issue["path"], [str((folder / "commands" / name).resolve())
                                                      for name in missing])
                    finally:
                        for name in missing:
                            self.put(folder / "commands" / name, commands[name])

    def test_claude_matching_sources_require_public_commands_even_in_default_cache(self):
        shutil.copy2(DOCTOR, self.source / "scripts/sdc-doctor.mjs")
        plugin, cache = self.claude(public_skills=True)
        commands = {p.name: p.read_text() for p in (self.source / "commands").glob("*.md")}
        for missing in [(name,) for name in commands] + [tuple(commands)]:
            for mode in ("selected-source", "selected-cache", "default-cache"):
                with self.subTest(missing=missing, mode=mode):
                    try:
                        # Equal damaged trees must not certify absent command entrypoints.
                        for folder in (self.source, plugin, cache):
                            for name in missing:
                                (folder / "commands" / name).unlink()
                        args = ["--client", "claude"]
                        if mode == "selected-cache":
                            args += ["--source", str(cache)]
                        payload = self.run_doctor(
                            *args, defaults=mode == "default-cache", success=False,
                            script=cache / "scripts/sdc-doctor.mjs")
                        self.assertEqual(self.codes(payload), {"SOURCE_UNAVAILABLE"})
                        self.assertTrue(all(i["fingerprint"] is None for i in payload["installations"]))
                    finally:
                        for folder in (self.source, plugin, cache):
                            for name in missing:
                                self.put(folder / "commands" / name, commands[name])

    def test_repeated_explicit_clients_can_be_selected(self):
        self.codex()
        self.direct()
        self.run_doctor("--client", "codex", "--client", "hermes")

    def test_toml_multiline_unrelated_string_does_not_fake_registration(self):
        self.codex(enabled=False)
        config = self.home / ".codex/config.toml"
        self.put(config, 'note = """\n[plugins."sdc@fake"]\nenabled = true\n"""\n' + config.read_text())
        payload = self.run_doctor(success=False)
        self.assertEqual(self.codes(payload), {"NO_INSTALLATIONS"})

    def test_unrelated_codex_nested_plugin_tables_are_ignored(self):
        self.codex()
        config = self.home / ".codex/config.toml"
        self.put(config, config.read_text() + '\n[plugins."other@market".settings]\nsecret = "NEVER_PRINT_SETTINGS_VALUE"\n')
        self.assertNotIn("NEVER_PRINT_SETTINGS_VALUE", json.dumps(self.run_doctor()))

    def test_array_form_sdc_toml_is_actionable_not_ignored(self):
        self.put(self.home / ".codex/config.toml", '[[plugins."sdc@team-local"]]\nenabled = true\n')
        self.assertIn("INVALID_REGISTRY", self.codes(self.run_doctor(success=False)))

    def test_quoted_codex_inline_and_dotted_keys_fail_closed_with_healthy_hermes(self):
        self.direct()
        config = self.home / ".codex/config.toml"
        statements = (
            'plugins = {"sdc@team-local" = {enabled = true}}',
            '"plugins" = {"sdc@team-local" = {enabled = true}}',
            "'plugins' = {'sdc@team-local' = {enabled = true}}",
            r'"\u0070lugins" = {"sdc@team-local" = {enabled = true}}',
            r'"\U00000070lugins" = {"sdc@team-local" = {enabled = true}}',
            '\"\"\"plugins\"\"\" = {"sdc@team-local" = {enabled = true}}',
            "'''plugins''' = {'sdc@team-local' = {enabled = true}}",
            '"plugins"."sdc@team-local" = {enabled = true}',
            "'plugins'.'sdc@team-local'.enabled = true",
            '"marketplaces" = {"team-local" = {source_type = "local"}}',
            "'marketplaces'.'team-local'.source_type = 'local'",
            r'"\u006darketplaces"."team-local" = {source_type = "local"}',
        )
        for statement in statements:
            with self.subTest(statement=statement):
                self.put(config, statement + "\n")
                payload = self.run_doctor(success=False)
                self.assertEqual(self.codes(payload), {"INVALID_REGISTRY"})
                issue, = payload["issues"]
                self.assertEqual(issue["client"], "codex")
                self.assertEqual(issue["path"], str(config.resolve()))
                self.assertEqual({i["client"] for i in payload["installations"]}, {"hermes"})
                self.assertEqual(payload["installations"][0]["fingerprint"],
                                 payload["installations"][0]["sourceFingerprint"])

    def test_quoted_codex_table_first_keys_remain_supported(self):
        self.codex()
        config = self.home / ".codex/config.toml"
        original = config.read_text()
        for plugins, marketplaces in (("'plugins'", '"marketplaces"'),
                                      ('"plugins"', "'marketplaces'"),
                                      (r'"\u0070lugins"', r'"\u006darketplaces"')):
            with self.subTest(plugins=plugins, marketplaces=marketplaces):
                self.put(config, original.replace("[plugins.", f"[{plugins}.").replace(
                    "[marketplaces.", f"[{marketplaces}."))
                self.run_doctor("--client", "codex")

    def test_unrelated_quoted_codex_keys_and_multiline_values_remain_opaque(self):
        self.direct()
        self.put(self.home / ".codex/config.toml", '''"other" = {enabled = true}
"plugins.sdc@not-a-table" = {enabled = true}
'note' = """
"plugins" = {"sdc@fake" = {enabled = true}}
"""
"notes" = [
  '"marketplaces" = {"fake" = {source_type = "local"}}',
]
''')
        self.run_doctor()

    def test_registered_cache_symlink_is_rejected(self):
        _, cache = self.codex()
        outside = self.base / "cache copy"
        shutil.move(cache, outside)
        cache.symlink_to(outside, target_is_directory=True)
        self.assertIn("UNSAFE_PATH", self.codes(self.run_doctor(success=False)))

    def test_optional_native_hook_payload_is_fingerprinted(self):
        self.put_json(self.source / "hooks/codex.json", {"hooks": {"SessionStart": []}})
        self.put(self.source / "hooks/codex-session-start.py", "# native helper\n")
        plugin, cache = self.codex()
        for folder in (plugin, cache):
            manifest = folder / ".codex-plugin/plugin.json"
            data = json.loads(manifest.read_text())
            data["hooks"] = "./hooks/codex.json"
            self.put_json(manifest, data)
        self.run_doctor()
        self.put(cache / "hooks/codex-session-start.py", "# stale native helper\n")
        self.assertIn("PAYLOAD_DRIFT", self.codes(self.run_doctor(success=False)))

    def test_unsupported_manifest_hook_forms_fail_closed(self):
        for client in ("codex", "claude"):
            plugin, cache = getattr(self, client)()
            conventional = "./hooks/codex.json" if client == "codex" else "./hooks/hooks.json"
            values = ([conventional], ["./hooks/missing.json"],
                      ["../../NEVER_PRINT_SETTINGS_VALUE.json"],
                      [str(self.base / "NEVER_PRINT_SETTINGS_VALUE.json")],
                      [{"hooks": {"SessionStart": []}}],
                      {"hooks": {"SessionStart": []}}, {}, None, False, True, 0, "")
            if client == "claude":
                values += ([],)
            for folder in (plugin, cache):
                manifest = folder / f".{client}-plugin/plugin.json"
                original = json.loads(manifest.read_text())
                for value in values:
                    with self.subTest(client=client, folder=folder, hooks=value):
                        try:
                            self.put_json(manifest, {**original, "hooks": value})
                            payload = self.run_doctor("--client", client, success=False)
                            self.assertEqual(self.codes(payload), {"INVALID_REGISTRY"})
                            issue, = payload["issues"]
                            self.assertEqual(issue["path"], str(manifest.resolve()))
                            self.assertEqual(issue["client"], client)
                            self.assertNotIn("NEVER_PRINT_SETTINGS_VALUE", json.dumps(payload))
                        finally:
                            self.put_json(manifest, original)

    def test_absent_hooks_and_codex_explicit_empty_hooks_remain_supported(self):
        for client in ("codex", "claude"):
            plugin, cache = getattr(self, client)()
            for folder in (plugin, cache):
                manifest = folder / f".{client}-plugin/plugin.json"
                data = json.loads(manifest.read_text())
                data.pop("hooks", None)
                self.put_json(manifest, data)
            self.run_doctor("--client", client)
            if client == "codex":
                for folder in (plugin, cache):
                    manifest = folder / ".codex-plugin/plugin.json"
                    self.put_json(manifest, {**json.loads(manifest.read_text()), "hooks": []})
                self.run_doctor("--client", client)

    def test_array_hooks_cannot_hide_a_missing_helper(self):
        for client, config, helper in (("codex", "codex.json", "codex-session-start.py"),
                                       ("claude", "hooks.json", "session-start")):
            _, cache = getattr(self, client)()
            self.put_json(cache / "hooks" / config, {"hooks": {"SessionStart": []}})
            self.assertFalse((cache / "hooks" / helper).exists())
            manifest = cache / f".{client}-plugin/plugin.json"
            self.put_json(manifest, {**json.loads(manifest.read_text()),
                                     "hooks": [f"./hooks/{config}"]})
            with self.subTest(client=client):
                payload = self.run_doctor("--client", client, success=False)
                self.assertEqual(self.codes(payload), {"INVALID_REGISTRY"})
                self.assertEqual(payload["issues"][0]["path"], str(manifest.resolve()))

    def test_explicit_string_hooks_require_the_client_helper(self):
        for client, config, helper in (("codex", "codex.json", "codex-session-start.py"),
                                       ("claude", "hooks.json", "session-start")):
            self.put_json(self.source / "hooks" / config, {"hooks": {"SessionStart": []}})
            self.put(self.source / "hooks" / helper, "# fixture hook helper\n")
            source_manifest = self.source / f".{client}-plugin/plugin.json"
            data = json.loads(source_manifest.read_text())
            self.put_json(source_manifest, {**data, "hooks": f"./hooks/{config}"})
            plugin, cache = getattr(self, client)()
            self.run_doctor("--client", client)
            for folder in (plugin, cache):
                with self.subTest(client=client, folder=folder):
                    target = folder / "hooks" / helper
                    original = target.read_text()
                    try:
                        target.unlink()
                        payload = self.run_doctor("--client", client, success=False)
                        self.assertEqual(self.codes(payload), {"MISSING_HELPER"})
                        self.assertEqual(payload["issues"][0]["path"], str(target.resolve()))
                    finally:
                        self.put(target, original)

    def test_claude_implicit_hook_payload_is_fingerprinted(self):
        self.put_json(self.source / "hooks/hooks.json", {"hooks": {"SessionStart": []}})
        self.put(self.source / "hooks/session-start", "#!/bin/sh\nexit 0\n")
        _, cache = self.claude()
        self.put(cache / "hooks/session-start", "#!/bin/sh\nexit 1\n")
        self.assertIn("PAYLOAD_DRIFT", self.codes(self.run_doctor(success=False)))

    def test_unrelated_plugin_directories_and_registrations_are_not_inspected(self):
        self.codex()
        self.put(self.home / ".codex/plugins/cache/other/plugin/1/secret.json", "malformed-secret")
        self.put(self.home / ".codex/plugins/other/.codex-plugin/plugin.json", "malformed-secret")
        self.put_json(self.home / ".claude/settings.json", {"enabledPlugins": {"other@market": True}})
        self.run_doctor()

    def test_source_missing_core_helper_is_unavailable(self):
        self.codex()
        (self.source / HELPERS[0]).unlink()
        self.assertIn("SOURCE_UNAVAILABLE", self.codes(self.run_doctor(success=False)))

    def test_source_missing_imported_runtime_module_is_unavailable(self):
        self.codex()
        for name in ("scripts/sdc_compact.py", "scripts/sdc_findings.py"):
            with self.subTest(module=name):
                content = (self.source / name).read_text()
                (self.source / name).unlink()
                self.assertIn("SOURCE_UNAVAILABLE", self.codes(self.run_doctor(success=False)))
                self.put(self.source / name, content)

    def test_claude_only_source_does_not_require_public_generated_skills(self):
        self.claude()
        for name in PUBLIC:
            shutil.rmtree(self.source / f"skills/sdc-{name}")
        self.run_doctor("--client", "claude")

    def test_claude_only_default_source_is_the_installed_root(self):
        shutil.copy2(DOCTOR, self.source / "scripts/sdc-doctor.mjs")
        _, cache = self.claude()
        self.run_doctor("--client", "claude", defaults=True,
                        script=cache / "scripts/sdc-doctor.mjs")

    def test_minimal_direct_default_source_reports_comparison_unavailable(self):
        _, runtime = self.direct()
        shutil.copy2(DOCTOR, runtime / "scripts/sdc-doctor.mjs")
        payload = self.run_doctor("--client", "hermes", defaults=True, success=False,
                                  script=runtime / "scripts/sdc-doctor.mjs")
        self.assertEqual(self.codes(payload), {"SOURCE_UNAVAILABLE"})

    def generated_install(self, *, claude=False, native=False):
        shutil.rmtree(self.source)
        shutil.copytree(ROOT, self.source, ignore=shutil.ignore_patterns(
            ".git", "node_modules", "__pycache__", ".sdc", "dist"))
        tools = self.base / "tools"
        tools.mkdir()
        # Never run the real Claude CLI, even if it ignores fixture HOME.
        shim = tools / "claude"
        self.put(shim, "#!/bin/sh\nexit 127\n")
        shim.chmod(0o755)
        self.env["PATH"] = str(tools) + os.pathsep + self.env["PATH"]
        if claude:
            (self.home / ".claude/plugins").mkdir(parents=True)
        if native:
            self.env["SDC_CODEX_HOOKS"] = "1"
        for command in ([NODE, "bin/install.js", "sync-public-skills"], [NODE, "bin/install.js"]):
            result = subprocess.run(command, cwd=self.source, env=self.env, capture_output=True,
                                    text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        version = json.loads((self.source / "package.json").read_text())["version"]
        if not claude:
            return self.home / f".codex/plugins/cache/sdc-local/sdc/{version}"
        market = self.home / ".claude/plugins/marketplaces/sdc-local"
        cache = self.home / f".claude/plugins/cache/sdc-local/sdc/{version}"
        shutil.copytree(market, cache)
        self.put_json(self.home / ".claude/settings.json", {"enabledPlugins": {"sdc@sdc-local": True}})
        self.put_json(self.home / ".claude/plugins/known_marketplaces.json", {
            "sdc-local": {"installLocation": str(market)}})
        self.put_json(self.home / ".claude/plugins/installed_plugins.json", {
            "version": 2, "plugins": {"sdc@sdc-local": [
                {"scope": "user", "installPath": str(cache), "version": version}]}})
        return cache

    def test_generated_claude_source_default_root_only_needs_claude_profile(self):
        cache = self.generated_install(claude=True)
        self.assertEqual({x.name for x in (cache / "skills").iterdir()},
                         {f"sdc-{name}" for name in PUBLIC + ADVANCED})
        manifest = json.loads((cache / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(set(manifest["skills"]), {f"./skills/sdc-{name}" for name in ADVANCED})
        self.run_doctor("--client", "claude", defaults=True,
                        script=cache / "scripts/sdc-doctor.mjs")

    def test_generated_claude_source_can_be_selected_explicitly(self):
        cache = self.generated_install(claude=True)
        self.run_doctor("--client", "claude", "--source", str(cache))

    def test_generated_codex_portable_source_needs_no_claude_commands(self):
        cache = self.generated_install()
        for name in ("commands", ".claude-plugin", "bin"):
            shutil.rmtree(cache / name)
        (cache / "package.json").unlink()
        self.run_doctor("--client", "codex", defaults=True,
                        script=cache / "scripts/sdc-doctor.mjs")

    def test_generated_codex_native_source_needs_no_claude_commands(self):
        cache = self.generated_install(native=True)
        for name in ("commands", ".claude-plugin", "bin"):
            shutil.rmtree(cache / name)
        (cache / "package.json").unlink()
        self.run_doctor("--client", "codex", defaults=True,
                        script=cache / "scripts/sdc-doctor.mjs")

    def test_fixed_home_layout_matches_installer_despite_client_overrides(self):
        cache = self.generated_install()
        self.env["CODEX_HOME"] = str(self.base / "unrelated codex home")
        self.env["CLAUDE_CONFIG_DIR"] = str(self.base / "unrelated claude config")
        self.run_doctor("--client", "codex", defaults=True,
                        script=cache / "scripts/sdc-doctor.mjs")

    def test_human_output_has_actionable_blockers(self):
        self.codex()
        result = subprocess.run([NODE, str(DOCTOR), "--home", str(self.home), "--source", str(self.source),
                                 "--client", "hermes"], env=self.env, text=True,
                                capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("BLOCKED", result.stdout)
        self.assertIn("CLIENT_MISSING", result.stdout)
        self.assertIn("Install/enable", result.stdout)

    def test_invalid_manifest_json_has_no_raw_content(self):
        _, cache = self.codex()
        self.put(cache / ".codex-plugin/plugin.json", '{"private":"NEVER_PRINT_SETTINGS_VALUE",')
        payload = self.run_doctor(success=False)
        self.assertIn("INVALID_JSON", self.codes(payload))
        self.assertNotIn("NEVER_PRINT_SETTINGS_VALUE", json.dumps(payload))


if __name__ == "__main__":
    unittest.main()
