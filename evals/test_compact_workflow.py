"""Exercise the compact format through the real CLI and evidence runtime."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
CLI = REPO / "sdc-cli.py"
RUNTIME = REPO / "scripts/sdc-runtime-context.py"


def confirmed_record():
    return {
        "schema": "sdc.compact/v1",
        "intake": {
            "request": "Correct teh to the in README.md only.",
            "context": "Existing documentation; local maintainer request.",
            "scope": "One spelling correction, no instructions or behavior changes.",
            "preferences": "Keep existing Markdown; stack is unaffected.",
            "acceptance": "README contains the overview and no teh overview.",
            "authorization": "User: correct the typo and verify the local result; no publish.",
            "open_questions": [],
            "decisions": [],
        },
        "risk": {
            "level": "light",
            "rationale": "Inspected README: isolated spelling, not a policy or contract.",
            "exclusions": dict.fromkeys(("behavior", "data", "security", "public_contract", "architecture", "deployment"), False),
        },
        "paths": ["README.md"],
        "impact": "Only README spelling changes; no callers or runtime impact.",
        "governance": [],
        "governance_review": "No project-specific governance exists in this disposable fixture.",
        "output_assessment": "Text correction only; no process, API, data, UX, or release contract changes.",
        "task": {
            "id": "T001", "scenario": "SCN-001", "requirement": "REQ-001", "acceptance": "AC-001",
            "verify": [sys.executable, "-c", "from pathlib import Path; s=Path('README.md').read_text(); assert 'the overview' in s and 'teh overview' not in s"],
            "expected": "Spelling assertion passes and diff contains only the authorized correction.",
        },
    }


class CompactWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sdc-compact-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        (self.root / "README.md").write_text("Read teh overview.\n")
        self.input = Path(self.temp.name) / "intake.json"
        self.record = confirmed_record()

    def call(self, script, *args, ok=True):
        result = subprocess.run([sys.executable, str(script), *args], cwd=self.root, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(result.returncode == 0, ok, result.stdout)
        return result.stdout

    def create(self, ok=True):
        self.input.write_text(json.dumps(self.record))
        output = self.call(CLI, "change", "readme-spelling", "--compact", "--record", str(self.input), ok=ok)
        if ok:
            self.assertTrue((self.root / ".sdc/changes/active").is_dir(), output)
            self.change = next((self.root / ".sdc/changes/active").iterdir())
        return output

    def runtime(self, *args, ok=True):
        return json.loads(self.call(RUNTIME, *args, "--change", self.change.name, ok=ok))

    def state(self, state, ok=True):
        source = {"confirmed": "spec-stage", "planned": "plan-stage", "applying": "apply-stage",
                  "checking": "apply-stage", "archivable": "check-stage"}[state]
        return self.runtime("state", "set", "--state", state, "--source", source,
                            "--evidence", "compact.json", ok=ok)

    def update(self, fn):
        path = self.change / "compact.json"
        data = json.loads(path.read_text())
        fn(data)
        path.write_text(json.dumps(data, indent=2) + "\n")

    def applying(self):
        self.create()
        self.state("confirmed")
        for role in ("apply", "check"):
            self.runtime("manifest", "generate", "--role", role)
        self.state("planned")
        self.state("applying")

    def finish(self):
        (self.root / "README.md").write_text("Read the overview.\n")
        self.update(lambda d: d["task"].update(complete=True))
        self.call(RUNTIME, "evidence", "run", "--change", self.change.name, "--stage", "check", "--task", "T001",
                  "--timeout", "10", "--", *self.record["task"]["verify"])
        self.update(lambda d: d.update(review={"spec": "approved", "quality": "approved", "reviewer": "fixture-reviewer",
                    "evidence": "README diff inspected: spelling only; independent expected spelling assertion.",
                    "behavior_neutral": True}))
        self.runtime("evidence", "review", "--reviewer", "fixture-reviewer")
        for role in ("apply", "check"):
            self.runtime("manifest", "generate", "--role", role)
        self.state("checking")

    def test_cold_start_creates_two_files_and_no_workspace_template_package(self):
        self.create()
        self.assertEqual({p.name for p in self.change.iterdir() if p.is_file()}, {"compact.json", "state.json"})
        self.assertTrue((self.change / "evidence/baseline/source.json").is_file())
        self.assertFalse((self.root / ".sdc/templates").exists())
        self.assertFalse((self.root / ".sdc/constitution.md").exists())
        ignore = self.root / ".sdc/.gitignore"
        self.assertTrue(ignore.is_file(), "Cold-start runtime scratch must be git-ignored")
        self.assertIn("/runtime/", ignore.read_text())
        self.call(CLI, "validate", self.change.name)

    def test_open_questions_and_missing_authority_write_nothing(self):
        for field, value in (("open_questions", ["Who approves?"]), ("authorization", "")):
            with self.subTest(field=field):
                self.record = confirmed_record()
                self.record["intake"][field] = value
                self.create(ok=False)
                self.assertFalse((self.root / ".sdc").exists())

    def test_risk_or_non_document_scope_is_rejected(self):
        for key in self.record["risk"]["exclusions"]:
            self.record = confirmed_record()
            self.record["risk"]["exclusions"][key] = True
            self.create(ok=False)
        for name in ("app.py", "../outside.md", "/tmp/escape.md", "AGENTS.md", ".sdc/constitution.md", "skills/sample/SKILL.md"):
            self.record = confirmed_record()
            self.record["paths"] = [name]
            self.create(ok=False)

    def test_real_validation_catches_typo_then_full_flow_archives(self):
        self.applying()
        self.call(RUNTIME, "evidence", "run", "--change", self.change.name, "--stage", "check", "--task", "T001",
                  "--timeout", "10", "--", *self.record["task"]["verify"], ok=False)
        self.finish()
        self.state("archivable")
        self.call(CLI, "check", self.change.name)
        self.call(CLI, "archive", self.change.name)
        self.assertFalse(self.change.exists())
        archived = self.root / ".sdc/changes/archive" / self.change.name
        self.assertTrue((archived / "compact.json").is_file())
        self.assertTrue((archived / "archive.md").is_file())
        self.assertFalse((self.root / ".sdc/knowledge").exists())

    def test_scope_expansion_blocks_checking(self):
        self.applying()
        (self.root / "app.py").write_text("changed = True\n")
        self.update(lambda d: d["task"].update(complete=True))
        self.state("checking", ok=False)

    def test_freshness_and_review_cannot_be_skipped(self):
        self.applying()
        self.state("checking", ok=False)
        self.finish()
        (self.root / "README.md").write_text("Read the overview with a new policy.\n")
        self.state("archivable", ok=False)

    def test_existing_governance_change_invalidates_confirmation(self):
        (self.root / "AGENTS.md").write_text("Do not publish.\n")
        self.applying()
        (self.root / "AGENTS.md").write_text("Do not edit README.\n")
        self.runtime("state", "get", ok=False)

    def test_revision_preserves_compact_history_and_invalidates_receipts(self):
        self.applying()
        self.finish()
        self.state("archivable")
        self.runtime("state", "reopen", "--state", "discovery", "--reason", "Confirm revised wording")
        self.assertTrue(list((self.change / "revisions").rglob("compact.json")))
        self.state("confirmed", ok=False)

    def test_escalation_preserves_history_and_returns_to_standard_discovery(self):
        self.applying()
        self.runtime("state", "reopen", "--state", "discovery", "--to-standard", "--reason", "User now requests behavior changes")
        self.assertFalse((self.change / "compact.json").exists())
        self.assertTrue(list((self.change / "revisions").rglob("compact.json")))
        self.assertTrue((self.change / "discovery.md").is_file())
        self.assertFalse((self.change / "spec.md").exists())
        self.assertFalse((self.change / "tasks.md").exists())
        self.runtime("state", "get")
        self.runtime("evidence", "verify", ok=False)

    def test_symlink_document_rejected_without_external_writes(self):
        outside = Path(self.temp.name) / "private.md"
        outside.write_text("untouched")
        (self.root / "README.md").unlink()
        (self.root / "README.md").symlink_to(outside)
        self.create(ok=False)
        self.assertEqual(outside.read_text(), "untouched")
        self.assertFalse((self.root / ".sdc").exists())

    def test_missing_compact_record_cannot_fall_back_to_standard(self):
        self.applying()
        (self.change / "compact.json").unlink()
        self.call(CLI, "validate", self.change.name, ok=False)
        self.runtime("state", "get", ok=False)

    def test_invalid_record_shape_has_no_side_effects(self):
        for key, value in (("intake", []), ("risk", []), ("task", None), ("governance", ["../outside.md"])):
            with self.subTest(key=key):
                self.record = confirmed_record()
                self.record[key] = value
                self.create(ok=False)
                self.assertFalse((self.root / ".sdc").exists())

    def test_corrupt_manifest_blocks_delivery_and_archive(self):
        self.applying()
        self.finish()
        self.state("archivable")
        (self.change / "check-context.jsonl").write_text("{}\n")
        self.runtime("evidence", "verify", ok=False)
        self.call(CLI, "archive", self.change.name, ok=False)
        self.assertTrue(self.change.exists())

    def test_baseline_is_machine_evidence_not_copied_into_compact_context(self):
        for index in range(50):
            (self.root / f"source-{index}.py").write_text("existing = True\n")
        self.create()
        data = json.loads((self.change / "compact.json").read_text())
        self.assertEqual(set(data["baseline"]), {"path", "sha256"})
        self.assertNotIn("source-49.py", (self.change / "compact.json").read_text())
        baseline = self.change / data["baseline"]["path"]
        baseline.write_text("{}\n")
        self.call(CLI, "validate", self.change.name, ok=False)

    def test_ignored_target_cannot_reuse_fresh_receipts_after_edit(self):
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        (self.root / ".gitignore").write_text("README.md\n")
        self.applying()
        self.finish()
        self.state("archivable")
        (self.root / "README.md").write_text("Read teh overview.\n")
        self.runtime("evidence", "verify", ok=False)
        self.call(CLI, "archive", self.change.name, ok=False)

    def test_transitively_cited_governance_invalidates_approval(self):
        rules = self.root / ".sdc/standards"
        rules.mkdir(parents=True)
        (rules / "docs.md").write_text("Follow `.sdc/standards/review.md`.\n")
        downstream = rules / "review.md"
        downstream.write_text("Require spelling review.\n")
        self.record["governance"] = [".sdc/standards/docs.md"]
        self.applying()
        self.finish()
        self.state("archivable")
        downstream.write_text("Require separate owner review.\n")
        self.runtime("state", "get", ok=False)
        self.runtime("manifest", "verify", "--role", "check", ok=False)
        self.call(CLI, "archive", self.change.name, ok=False)

    def test_escalation_preserves_existing_notes(self):
        self.applying()
        note = "# Notes\nOriginal investigation and authorization evidence.\n"
        (self.change / "notes.md").write_text(note)
        self.runtime("state", "reopen", "--state", "discovery", "--to-standard", "--reason", "Confirmed scope expansion")
        backups = list((self.change / "revisions").rglob("notes.md"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), note)

    def test_explicit_target_survives_default_directory_filters(self):
        target = self.root / "docs/venv/README.md"
        target.parent.mkdir(parents=True)
        target.write_text("Read teh overview.\n")
        self.record["paths"] = ["README.md", "docs/venv/README.md"]
        self.record["task"]["verify"][-1] += "; assert 'teh' not in Path('docs/venv/README.md').read_text()"
        self.applying()
        target.write_text("Read the overview.\n")
        self.finish()
        self.state("archivable")
        target.write_text("Read teh overview.\n")
        self.runtime("evidence", "verify", ok=False)
        self.call(CLI, "archive", self.change.name, ok=False)

    def test_automatic_governance_citations_invalidate_approval(self):
        rules = self.root / ".sdc/standards"
        rules.mkdir(parents=True)
        rule = rules / "review.md"
        rule.write_text("Require spelling review.\n")
        (self.root / "AGENTS.md").write_text("Follow `.sdc/standards/review.md`.\n")
        self.applying()
        self.finish()
        self.state("archivable")
        rule.write_text("Require separate owner review.\n")
        self.runtime("state", "get", ok=False)
        self.runtime("evidence", "verify", ok=False)
        self.call(CLI, "archive", self.change.name, ok=False)

    def test_scoped_governance_citations_are_required_before_creation(self):
        docs = self.root / "docs"
        docs.mkdir()
        (docs / "AGENTS.md").write_text("Follow `.sdc/standards/missing.md`.\n")
        self.record["paths"] = ["docs/README.md"]
        self.create(ok=False)
        self.assertFalse((self.root / ".sdc/changes").exists())

    def test_baseline_digest_matches_bytes_with_windows_text_translation(self):
        with patch.object(sys, "path", [str(REPO / "scripts"), *sys.path]):
            import sdc_compact
            original = Path.write_text

            def windows_text(path, text, *args, **kwargs):
                if path.name == "source.json":
                    text = text.replace("\n", "\r\n")
                return original(path, text, *args, **kwargs)

            with patch.object(Path, "write_text", windows_text):
                directory = sdc_compact.create(self.root, "windows-baseline", self.record)
            sdc_compact.validate(self.root, directory)

    def test_cited_optional_governance_root_becomes_required(self):
        (self.root / "AGENTS.md").write_text("Follow `.sdc/knowledge/index.md`.\n")
        self.create(ok=False)
        self.assertFalse((self.root / ".sdc/changes").exists())

    def test_standalone_receipts_bind_baseline_integrity(self):
        self.applying()
        self.finish()
        self.state("archivable")
        baseline = self.change / "evidence/baseline/source.json"
        baseline.write_text("{}\n")
        self.runtime("evidence", "verify", ok=False)
        baseline.unlink()
        self.runtime("evidence", "verify", ok=False)

    def test_tracked_code_under_filtered_directory_cannot_escape_scope(self):
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        code = self.root / "docs/venv/runner.py"
        code.parent.mkdir(parents=True)
        code.write_text("allowed = False\n")
        subprocess.run(["git", "add", "README.md", "docs/venv/runner.py"], cwd=self.root, check=True)
        self.applying()
        self.finish()
        self.state("archivable")
        code.write_text("allowed = True\n")
        self.call(CLI, "validate", self.change.name, ok=False)
        self.runtime("evidence", "verify", ok=False)
        self.call(CLI, "archive", self.change.name, ok=False)

    def test_non_git_directory_symlink_cannot_escape_scope(self):
        self.applying()
        self.finish()
        self.state("archivable")
        outside = Path(self.temp.name) / "external-code"
        outside.mkdir()
        (outside / "runner.py").write_text("enabled = True\n")
        (self.root / "src").symlink_to(outside, target_is_directory=True)
        self.call(CLI, "validate", self.change.name, ok=False)
        self.runtime("evidence", "verify", ok=False)
        self.call(CLI, "archive", self.change.name, ok=False)

    def test_existing_directory_symlink_retarget_invalidates_approval(self):
        targets = [Path(self.temp.name) / name for name in ("old-source", "new-source")]
        for target in targets:
            target.mkdir()
            (target / "runner.py").write_text("enabled = True\n")
        link = self.root / "src"
        link.symlink_to(targets[0], target_is_directory=True)
        self.applying()
        self.finish()
        self.state("archivable")
        link.unlink()
        link.symlink_to(targets[1], target_is_directory=True)
        self.call(CLI, "validate", self.change.name, ok=False)
        self.runtime("evidence", "verify", ok=False)
        self.call(CLI, "archive", self.change.name, ok=False)
        for target in targets:
            self.assertEqual((target / "runner.py").read_text(), "enabled = True\n")

    def test_ignored_symlink_ancestor_of_tracked_file_is_bound(self):
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        tracked = self.root / "docs/venv/runner.py"
        tracked.parent.mkdir(parents=True)
        tracked.write_text("enabled = False\n")
        for name, enabled in (("impl-a", False), ("impl-b", True)):
            target = self.root / name
            target.mkdir()
            (target / "runner.py").write_text(f"enabled = {enabled}\n")
        (self.root / ".gitignore").write_text("/docs/venv\n")
        subprocess.run(["git", "add", "README.md", ".gitignore", "impl-a", "impl-b"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "-f", "docs/venv/runner.py"], cwd=self.root, check=True)
        tracked.unlink()
        tracked.parent.rmdir()
        # Use a real target before approval; the index still contains its old child.
        tracked.parent.symlink_to("../impl-a", target_is_directory=True)
        self.assertTrue(tracked.is_file())
        self.applying()
        self.finish()
        self.state("archivable")
        tracked.parent.unlink()
        tracked.parent.symlink_to("../impl-b", target_is_directory=True)
        self.call(CLI, "validate", self.change.name, ok=False)
        self.runtime("evidence", "verify", ok=False)
        self.call(CLI, "archive", self.change.name, ok=False)


    def cite_default_ai_policy(self):
        self.call(CLI, "init")
        ai = self.root / ".sdc/standards/ai.md"
        self.assertIn("`.sdc/standards/company/README.md`", ai.read_text())
        self.record["governance"] = [".sdc/standards/ai.md"]
        company = self.root / ".sdc/standards/company/README.md"
        company.unlink(missing_ok=True)
        return company

    def test_f011_default_ai_allows_absent_company_and_binds_appearance(self):
        company = self.cite_default_ai_policy()
        self.applying()
        self.finish()
        self.state("archivable")
        with patch.object(sys, "path", [str(REPO / "scripts"), *sys.path]):
            import sdc_compact
            self.assertIsNone(sdc_compact.snapshot(self.root, self.change)[
                ".sdc/standards/company/README.md"])
        self.runtime("evidence", "verify")
        company.parent.mkdir(parents=True, exist_ok=True)
        company.write_text("# Company standards\n")
        self.runtime("state", "get", ok=False)
        self.runtime("evidence", "verify", ok=False)

    def test_f011_explicit_record_company_citation_overrides_optional(self):
        self.cite_default_ai_policy()
        self.record["impact"] += " Follow `.sdc/standards/company/README.md`."
        output = self.create(ok=False)
        self.assertIn("Cited governing source is missing: .sdc/standards/company/README.md", output)

    def test_f011_required_company_citation_wins_in_either_traversal_order(self):
        company = self.cite_default_ai_policy()
        with patch.object(sys, "path", [str(REPO / "scripts"), *sys.path]):
            import sdc_compact
            policy = (self.root / ".sdc/standards/ai.md").read_text()
            names = (".sdc/standards/first.md", ".sdc/standards/second.md")
            data = {"paths": [], "governance": []}
            for optional, required in (names, names[::-1]):
                with self.subTest(optional=optional):
                    (self.root / optional).write_text(policy)
                    (self.root / required).write_text("Follow `.sdc/standards/company/README.md`.\n")
                    # Swap contents under stable names to exercise both traversal orders.
                    (self.root / ".sdc/standards/order.md").write_text(
                        "Follow `" + names[0] + "` and `" + names[1] + "`.\n")
                    data["governance"] = [".sdc/standards/order.md"]
                    with self.assertRaisesRegex(ValueError, "Cited governing source is missing: .*company/README"):
                        sdc_compact.governing_sources(self.root, data)
            self.assertFalse(company.exists())

    def test_f011_provided_company_citations_are_recursively_required_and_bound(self):
        company = self.cite_default_ai_policy()
        company.parent.mkdir(parents=True, exist_ok=True)
        company.write_text("Follow `.sdc/standards/company/review.md`.\n")
        self.assertIn("company/review.md", self.create(ok=False))
        review = company.parent / "review.md"
        review.write_text("Follow `.sdc/standards/company/testing.md`.\n")
        self.assertIn("company/testing.md", self.create(ok=False))
        testing = company.parent / "testing.md"
        testing.write_text("Run targeted tests.\n")
        self.applying()
        self.finish()
        self.state("archivable")
        testing.write_text("Run full regression tests.\n")
        self.runtime("state", "get", ok=False)
        self.runtime("evidence", "verify", ok=False)

    def test_f011_optional_company_symlinks_are_rejected_even_if_dangling(self):
        company = self.cite_default_ai_policy()
        company.parent.mkdir(parents=True, exist_ok=True)
        for target in (company, company.parent):
            with self.subTest(target=target.name):
                if target.is_dir():
                    target.rename(target.with_name("company-original"))
                target.symlink_to(self.root / "missing-external", target_is_directory=target == company.parent)
                with patch.object(sys, "path", [str(REPO / "scripts"), *sys.path]):
                    import sdc_compact
                    with self.assertRaisesRegex(ValueError, "symlink"):
                        sdc_compact.governing_sources(self.root, self.record)
                self.assertRegex(self.create(ok=False).lower(), "symlink|symbolic link")
                target.unlink()


if __name__ == "__main__":
    unittest.main()
