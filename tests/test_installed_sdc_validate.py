#!/usr/bin/env python3
"""Regression coverage for the npm-installed ``sdc validate`` entrypoint."""

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CLI = REPO_ROOT / "sdc-cli.py"
EVAL_FIXTURES = REPO_ROOT / "evals" / "sdc-flow" / "sdc_flow_provider.py"


def run_command(args, *, cwd):
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def load_eval_fixtures():
    spec = importlib.util.spec_from_file_location("sdc_installed_cli_eval_fixtures", EVAL_FIXTURES)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class InstalledSdcValidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory(prefix="sdc-installed-validate-")
        cls.temp_root = Path(cls.temp_dir.name)
        pack_dir = cls.temp_root / "pack"
        pack_dir.mkdir()

        packed = run_command(
            ["npm", "pack", "--json", "--pack-destination", str(pack_dir)],
            cwd=REPO_ROOT,
        )
        if packed.returncode != 0:
            raise AssertionError(f"npm pack failed:\n{packed.stdout}")
        tarball_name = json.loads(packed.stdout)[0]["filename"]
        tarball = pack_dir / tarball_name

        cls.prefix = cls.temp_root / "prefix"
        installed = run_command(
            [
                "npm",
                "install",
                "--ignore-scripts",
                "--no-audit",
                "--no-fund",
                "--prefix",
                str(cls.prefix),
                str(tarball),
            ],
            cwd=REPO_ROOT,
        )
        if installed.returncode != 0:
            raise AssertionError(f"npm install failed:\n{installed.stdout}")

        suffix = ".cmd" if os.name == "nt" else ""
        cls.installed_sdc = cls.prefix / "node_modules" / ".bin" / f"sdc{suffix}"
        if not cls.installed_sdc.exists():
            raise AssertionError(f"npm install did not expose {cls.installed_sdc}")
        cls.eval_fixtures = load_eval_fixtures()

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def make_valid_change(self):
        fixture_root = Path(tempfile.mkdtemp(dir=self.temp_root, prefix="fixture-"))
        for args in (("init",), ("change", "known-change", "--confirmed-intake")):
            result = run_command(["python3", str(SOURCE_CLI), *args], cwd=fixture_root)
            self.assertEqual(result.returncode, 0, result.stdout)

        change = self.eval_fixtures.active_change(fixture_root, "known-change")
        self.eval_fixtures.write_confirmed_change(change)
        return fixture_root, change.name

    def test_installed_validate_matches_source_cli_for_a_valid_change(self):
        fixture_root, change_name = self.make_valid_change()

        source = run_command(["python3", str(SOURCE_CLI), "validate", change_name], cwd=fixture_root)
        installed = run_command([str(self.installed_sdc), "validate", change_name], cwd=fixture_root)

        self.assertEqual(source.returncode, 0, source.stdout)
        self.assertEqual(installed.returncode, source.returncode, installed.stdout)
        self.assertEqual(installed.stdout, source.stdout)

    def test_installed_validate_propagates_python_validation_failures(self):
        fixture_root, _ = self.make_valid_change()
        args = ("validate", "missing-change")

        source = run_command(["python3", str(SOURCE_CLI), *args], cwd=fixture_root)
        installed = run_command([str(self.installed_sdc), *args], cwd=fixture_root)

        self.assertNotEqual(source.returncode, 0, source.stdout)
        self.assertEqual(installed.returncode, source.returncode, installed.stdout)
        self.assertEqual(installed.stdout, source.stdout)

    def test_installed_validate_rejects_missing_or_illegal_arguments(self):
        fixture_root, change_name = self.make_valid_change()

        for args in (
            ("validate",),
            ("validate", "--unexpected"),
            ("validate", change_name, "--unexpected"),
        ):
            with self.subTest(args=args):
                result = run_command([str(self.installed_sdc), *args], cwd=fixture_root)
                self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_installed_sdc_keeps_unknown_commands_as_failures(self):
        result = run_command([str(self.installed_sdc), "not-a-command"], cwd=self.temp_root)

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("未知指令", result.stdout)


if __name__ == "__main__":
    unittest.main()
