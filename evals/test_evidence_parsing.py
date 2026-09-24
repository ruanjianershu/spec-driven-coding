"""Parsing regressions for delivery receipts and cited governing inputs."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from evals import test_evidence_workflow as workflow
from scripts import sdc_evidence as evidence


REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sdc_cli_parsing", REPO / "sdc-cli.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)

TASK_PREAMBLE = """# Tasks
## Global Constraints
| ID | Constraint | Source | Applies To |
|---|---|---|---|
| GC-01 | Keep the approved scope | spec.md#REQ-01 | all tasks |
## Plan Preflight
- Status: Passed
- Reviewed Against: spec.md, design.md, tasks.md, Artifact Output Contract
- Findings: None
## Tasks
"""


def task_block(task_id="T001", indent="", box=" ", verify='python3 -c "assert True"'):
    return (
        f"{indent}- [{box}] {task_id} [REQ-01] [AC-01] [Phase 1] [Size: S] Verify the contract\n"
        "  - Depends on: none\n"
        "  - Files: source.py\n"
        "  - Consumes: approved contract\n"
        "  - Produces: validated behavior\n"
        f"  - Verify: {verify}\n"
        "  - Expected: command exits zero\n"
        "  - Review: Pending\n"
        "  - Evidence: Pending\n"
        "  - Source: spec.md#AC-01\n"
    )


class TaskParsingTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="sdc-task-parsing-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.path = self.root / "tasks.md"

    def write_tasks(self, text):
        self.path.write_text(TASK_PREAMBLE + text)

    def test_all_cli_accepted_indents_are_parsed(self):
        for indent in ("", "  ", "\t", "    "):
            with self.subTest(indent=indent):
                self.write_tasks(task_block(indent=indent) + task_block("T900"))
                errors = []
                cli.validate_task_trace(errors, self.path)
                self.assertEqual(errors, [])
                tasks = evidence.task_verifications(self.root)
                self.assertEqual(set(tasks), {"T001", "T900"})
                self.assertEqual(tasks["T001"]["argv"], ["python3", "-c", "assert True"])

    def test_mixed_indents_keep_commands_and_completion_with_their_tasks(self):
        self.write_tasks(
            task_block(indent="  ", box="X", verify="python3 first.py")
            + task_block("T002", indent="\t", box="x", verify="python3 second.py")
            + task_block("T900", verify="python3 third.py")
        )
        self.assertEqual(evidence.task_verifications(self.root), {
            "T001": {"complete": True, "argv": ["python3", "first.py"]},
            "T002": {"complete": True, "argv": ["python3", "second.py"]},
            "T900": {"complete": False, "argv": ["python3", "third.py"]},
        })

    def test_rejects_cli_invalid_headers_instead_of_skipping_them(self):
        valid = task_block()
        invalid = (
            valid.replace("T001", "T1"),
            valid.replace("T001", "T0001"),
            valid.replace("T001", "t001"),
            valid.replace("- [ ]", "-  [ ]", 1),
            valid.replace("[ ] T001", "[ ]\tT001", 1),
            valid.replace("[REQ-01] ", "", 1),
            valid.replace("[Size: S]", "[Size: L]", 1),
            valid.replace("Verify the contract", "", 1),
            "- [ ] This checkbox has no task ID\n",
        )
        for text in invalid:
            with self.subTest(header=text.splitlines()[0]):
                self.write_tasks(text + task_block("T900"))
                errors = []
                cli.validate_task_trace(errors, self.path)
                self.assertTrue(errors)
                with self.assertRaises(ValueError):
                    evidence.task_verifications(self.root)

    def test_duplicate_indented_task_ids_are_rejected(self):
        self.write_tasks(task_block(indent="  ") + task_block())
        with self.assertRaises(ValueError):
            evidence.task_verifications(self.root)

    def test_verify_fields_keep_cli_case_and_spacing_rules(self):
        for field in ("  - verify:", "\t-  VERIFY:", "-Verify:"):
            with self.subTest(field=field):
                self.write_tasks(task_block().replace("  - Verify:", field))
                errors = []
                cli.validate_task_trace(errors, self.path)
                self.assertEqual(errors, [])
                self.assertEqual(evidence.task_verifications(self.root)["T001"]["argv"],
                                 ["python3", "-c", "assert True"])

    def test_missing_duplicate_and_empty_verify_commands_are_rejected(self):
        line = '  - Verify: python3 -c "assert True"\n'
        for text in (task_block().replace(line, ""),
                     task_block().replace(line, line + line),
                     task_block(verify=""), task_block(verify="``")):
            with self.subTest(text=text):
                self.write_tasks(text)
                with self.assertRaises(ValueError):
                    evidence.task_verifications(self.root)

    def test_empty_task_set_is_rejected(self):
        self.write_tasks("")
        with self.assertRaises(ValueError):
            evidence.task_verifications(self.root)


class CitationParsingTests(unittest.TestCase):
    def test_link_destinations_exclude_titles_and_decode_spaces(self):
        expected = {".sdc/knowledge/technical/approval rules.md"}
        links = (
            '[Policy](.sdc/knowledge/technical/approval%20rules.md "Policy title")',
            "[Policy](.sdc/knowledge/technical/approval%20rules.md 'Policy title')",
            '[Policy](<.sdc/knowledge/technical/approval rules.md> "Policy title")',
            '[Policy](.sdc/knowledge/technical/approval%20rules.md#approval)',
        )
        for link in links:
            with self.subTest(link=link):
                self.assertEqual(evidence.knowledge_references(link), expected)

    def test_encoded_traversal_is_rejected_after_decoding(self):
        with self.assertRaises(ValueError):
            evidence.knowledge_references('[Policy](.sdc/knowledge/%2e%2e/constitution.md "Title")')

    def test_backtick_paths_are_literal_not_url_decoded(self):
        self.assertEqual(evidence.knowledge_references('`.sdc/knowledge/a%20b.md`'),
                         {".sdc/knowledge/a%20b.md"})

    def test_change_support_files_are_part_of_execution_snapshot(self):
        with tempfile.TemporaryDirectory(prefix="sdc-support-snapshot-") as temp:
            root = Path(temp)
            change = root / ".sdc/changes/active/example"
            change.mkdir(parents=True)
            script = change / "verify.sh"
            script.write_text("exit 0\n")
            before = evidence.verification_snapshot(root, change)
            script.write_text("exit 1\n")
            self.assertNotEqual(before, evidence.verification_snapshot(root, change))

    def test_support_symlinks_are_rejected(self):
        with tempfile.TemporaryDirectory(prefix="sdc-support-snapshot-") as temp:
            root = Path(temp)
            change = root / ".sdc/changes/active/example"
            change.mkdir(parents=True)
            (root / "outside").write_text("not a source\n")
            (change / "verify.sh").symlink_to(root / "outside")
            with self.assertRaises(ValueError):
                evidence.verification_snapshot(root, change)


class ParsingDeliveryTests(unittest.TestCase):
    def test_indented_task_requires_its_own_execution_receipt(self):
        case = workflow.EvidenceWorkflowTests()
        case.setUp()
        self.addCleanup(case.doCleanups)
        for path in (case.change / "evidence").glob("*.json"):
            path.unlink()
        tasks = case.change / "tasks.md"
        tasks.write_text(tasks.read_text().replace("\n- [x] T001", "\n  - [x] T001"))
        case.applying()

        def run(task_id):
            code, output = workflow.fixtures.run_runtime(
                case.root, "evidence", "run", "--change", case.change.name,
                "--stage", "check", "--task", task_id, "--",
                "python3", "-c", "assert 1 + 1 == 2")
            self.assertEqual(code, 0, output)

        run("T900")
        case.review()
        case.state("checking")
        result = case.state("archivable", ok=False)
        self.assertIn("T001", json.dumps(result))
        run("T001")
        case.state("archivable")


class OptionalKnowledgeDependencyTests(unittest.TestCase):
    company = ".sdc/standards/company/README.md"

    def bundled_policy(self):
        return next(line for line in cli.INIT_FILES["standards/ai.md"].splitlines()
                    if self.company in line)

    def test_f011_actual_bundled_policy_classifies_only_company_index_optional(self):
        self.assertEqual(evidence.knowledge_dependencies(cli.INIT_FILES["standards/ai.md"]), {
            ".sdc/knowledge/index.md": True, self.company: False,
        })

    def test_f011_only_exact_legacy_line_is_optional(self):
        line = self.bundled_policy()
        for text in (" " + line, line + " Extra condition.", "If it exists: `" + self.company + "`",
                     line.replace(self.company, ".sdc/standards/company/other.md")):
            with self.subTest(text=text):
                self.assertTrue(all(evidence.knowledge_dependencies(text).values()))

    def test_f011_required_occurrence_dominates_in_either_text_order(self):
        for citation in ("Follow `" + self.company + "`.", "[Company](" + self.company + ")"):
            for lines in ((self.bundled_policy(), citation), (citation, self.bundled_policy())):
                with self.subTest(lines=lines):
                    self.assertTrue(evidence.knowledge_dependencies("\n".join(lines))[self.company])

    def test_f011_optional_policy_does_not_mask_unsafe_links(self):
        with self.assertRaises(ValueError):
            evidence.knowledge_dependencies(self.bundled_policy() +
                "\n[Unsafe](.sdc/standards/company/%2e%2e/secret.md)")

    def test_f011_explicit_artifact_citation_wins_in_either_traversal_order(self):
        with tempfile.TemporaryDirectory(prefix="sdc-optional-order-") as temp:
            root = Path(temp)
            change = root / ".sdc/changes/active/example"
            change.mkdir(parents=True)
            ai = root / ".sdc/standards/ai.md"
            ai.parent.mkdir(parents=True)
            ai.write_text(cli.INIT_FILES["standards/ai.md"])
            index = root / ".sdc/knowledge/index.md"
            index.parent.mkdir(parents=True)
            index.write_text("# Knowledge\n")
            for optional, required in (("spec.md", "discovery.md"), ("discovery.md", "spec.md")):
                with self.subTest(optional=optional):
                    (change / optional).write_text("Follow `.sdc/standards/ai.md`.\n")
                    (change / required).write_text("Follow `" + self.company + "`.\n")
                    with self.assertRaisesRegex(ValueError, "Cited knowledge/standard source is missing: .*company/README"):
                        evidence.input_snapshot(root, change)

    def test_f011_explicit_artifact_copy_of_policy_is_still_required(self):
        with tempfile.TemporaryDirectory(prefix="sdc-optional-artifact-") as temp:
            root = Path(temp)
            change = root / ".sdc/changes/active/example"
            change.mkdir(parents=True)
            (change / "spec.md").write_text(self.bundled_policy())
            with self.assertRaisesRegex(ValueError, "Cited knowledge/standard source is missing"):
                evidence.input_snapshot(root, change)

    def test_f011_governing_root_requirements_agree_across_formats(self):
        from scripts import sdc_compact
        for governing in ("constitution.md", "common-ground.md", "expert-routing.md", "knowledge/index.md"):
            with self.subTest(governing=governing), tempfile.TemporaryDirectory(prefix="sdc-root-citation-") as temp:
                root = Path(temp)
                change = root / ".sdc/changes/active/example"
                change.mkdir(parents=True)
                ai = root / ".sdc/standards/ai.md"
                ai.parent.mkdir(parents=True)
                ai.write_text(cli.INIT_FILES["standards/ai.md"])
                index = root / ".sdc/knowledge/index.md"
                index.parent.mkdir(parents=True)
                index.write_text("# Knowledge\n")
                (root / ".sdc" / governing).write_text("Required: `" + self.company + "`\n")
                (change / "spec.md").write_text("Follow `.sdc/standards/ai.md`.\n")
                with self.assertRaisesRegex(ValueError, "company/README.md"):
                    evidence.input_snapshot(root, change)
                with self.assertRaisesRegex(ValueError, "company/README.md"):
                    sdc_compact.governing_sources(root, {"paths": ["README.md"],
                                                        "governance": [".sdc/standards/ai.md"]})


if __name__ == "__main__":
    unittest.main()
