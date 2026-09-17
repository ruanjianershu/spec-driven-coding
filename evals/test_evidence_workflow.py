"""Regression tests for evidence-bound lifecycle operations, not model behavior."""

import importlib.util
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("flow_fixtures", REPO / "evals/sdc-flow/sdc_flow_provider.py")
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)


class EvidenceWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sdc-evidence-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        fixtures.run_sdc(self.root, "init")
        fixtures.run_sdc(self.root, "change", "evidence", "--confirmed-intake")
        self.change = fixtures.active_change(self.root, "evidence")
        fixtures.write_confirmed_change(self.change, completed=True)
        self.verify = 'python3 -c "assert 1 + 1 == 2"'
        tasks = self.change / "tasks.md"
        tasks.write_text(tasks.read_text().replace("python3 -m py_compile sdc-cli.py", self.verify)
                         .replace("sdc validate current-change", self.verify))
        (self.change / "impact.md").write_text(
            "# Impact\n## Analysis Snapshot\nDisposable fixture.\n"
            "## Direct Changes Required\nLocal source only.\n"
            "## Tests And Regression Strategy\nRun fixture assertions.\n"
            "## Evidence Index\nSee spec.md.\n")

    def runtime(self, *args, ok=True):
        code, output = fixtures.run_runtime(self.root, *args, "--change", self.change.name)
        if ok:
            self.assertEqual(code, 0, output)
        else:
            self.assertNotEqual(code, 0, output)
        return json.loads(output)

    def state(self, state, ok=True):
        source, evidence = {
            "confirmed": ("spec-stage", ["spec.md"]),
            "planned": ("plan-stage", ["design.md", "tasks.md", "context-pack.md"]),
            "applying": ("apply-stage", ["tasks.md", "context-pack.md"]),
            "checking": ("apply-stage", ["tasks.md", "notes.md"]),
            "archivable": ("check-stage", ["tasks.md", "notes.md"]),
        }[state]
        args = ["state", "set", "--state", state, "--source", source]
        for name in evidence:
            args.extend(["--evidence", name])
        return self.runtime(*args, ok=ok)

    def manifests(self):
        for role in ("apply", "check"):
            self.runtime("manifest", "generate", "--role", role)

    def applying(self):
        self.state("confirmed")
        self.manifests()
        self.state("planned")
        self.state("applying")

    def run_evidence(self, command=None, ok=True, timeout="5", tasks=("T001", "T900")):
        args = ["evidence", "run", "--change", self.change.name, "--stage", "check"]
        for task in tasks:
            args.extend(["--task", task])
        args.extend(["--timeout", timeout, "--"])
        command = command or ["python3", "-c", "assert 1 + 1 == 2"]
        code, output = fixtures.run_runtime(self.root, *args, *command)
        self.assertEqual(code == 0, ok, output)
        return json.loads(output)

    def review(self):
        return self.runtime("evidence", "review", "--reviewer", "independent-test-reviewer")

    def archivable(self):
        self.applying()
        self.run_evidence()
        self.review()
        self.state("checking")
        self.state("archivable")

    def test_draft_cannot_be_confirmed(self):
        (self.change / "spec.md").write_text("# Spec\nStatus: Draft\n")
        before = (self.change / "state.json").read_bytes()
        self.state("confirmed", ok=False)
        self.assertEqual(before, (self.change / "state.json").read_bytes())

    def test_open_question_blocks_confirmation_even_with_checked_exit(self):
        path = self.change / "discovery.md"
        path.write_text(path.read_text().replace("## Open Questions", "## Open Questions\n\n- Who may approve a booking?"))
        self.state("confirmed", ok=False)

    def test_file_presence_does_not_derive_confirmation(self):
        (self.change / "state.json").unlink()
        data = self.runtime("state", "get")
        self.assertIn(data["state"], ("intake", "discovery"))

    def test_incomplete_plan_cannot_advance(self):
        self.state("confirmed")
        (self.change / "design.md").write_text("# Design\nNot reviewed yet.\n")
        self.manifests()
        self.state("planned", ok=False)

    def test_missing_snapshot_in_legacy_confirmed_state_requires_revalidation(self):
        self.state("confirmed")
        path = self.change / "state.json"
        data = json.loads(path.read_text())
        data.pop("snapshot", None)
        path.write_text(json.dumps(data))
        self.runtime("state", "get", ok=False)

    def test_valid_same_state_retry_is_idempotent(self):
        self.applying()
        before = (self.change / "state.json").read_bytes()
        self.state("applying")
        self.assertEqual(before, (self.change / "state.json").read_bytes())

    def test_requirement_edit_invalidates_state(self):
        self.applying()
        path = self.change / "spec.md"
        path.write_text(path.read_text() + "\nBookings require manager approval.\n")
        result = self.runtime("state", "get", ok=False)
        self.assertIn("stale", json.dumps(result).lower())

    def test_manifest_hash_and_schema_are_verified(self):
        self.state("confirmed")
        self.manifests()
        path = self.change / "apply-context.jsonl"
        original = path.read_text()
        path.write_text(original.replace('"sha256":"', '"sha256":"bad', 1))
        self.runtime("manifest", "verify", "--role", "apply", ok=False)
        self.state("planned", ok=False)
        path.write_text("{}\n")
        self.runtime("manifest", "verify", "--role", "apply", ok=False)

    def test_replan_preserves_history_and_invalidates_delivery(self):
        self.applying()
        data = self.runtime("state", "reopen", "--state", "confirmed", "--reason", "Revise implementation approach")
        self.assertEqual(data["state"], "confirmed")
        self.assertTrue(data.get("history"))
        self.assertTrue(list((self.change / "revisions").rglob("tasks.md")))
        self.state("archivable", ok=False)

    def test_changed_scope_cannot_skip_discovery_via_replan(self):
        self.applying()
        path = self.change / "spec.md"
        path.write_text(path.read_text() + "\nNew public API scope.\n")
        self.runtime("state", "reopen", "--state", "confirmed", "--reason", "Changed scope", ok=False)
        self.runtime("state", "reopen", "--state", "discovery", "--reason", "Confirm changed scope")
        self.assertFalse((self.change / "spec.md").exists())

    def test_command_receipt_records_actual_failure_and_timeout(self):
        data = self.run_evidence(["python3", "-c", "raise SystemExit(7)"], ok=False)
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["exit_code"], 7)
        data = self.run_evidence(["python3", "-c", "import time; time.sleep(10)"], timeout="0.1", ok=False)
        self.assertEqual(data["status"], "timeout")

    def test_asserted_pass_is_not_executed_evidence(self):
        self.applying()
        self.runtime("evidence", "append", "--stage", "check", "--command", self.verify, "--status", "passed")
        self.state("checking")
        self.state("archivable", ok=False)

    def test_review_and_run_are_bound_to_source(self):
        self.archivable()
        (self.root / "new-source.py").write_text("new_behavior = True\n")
        self.runtime("state", "get", ok=False)

    def test_latest_failed_run_cannot_reuse_earlier_pass(self):
        self.applying()
        self.run_evidence()
        self.review()
        self.run_evidence(["python3", "-c", "raise SystemExit(1)"], ok=False)
        self.state("checking")
        self.state("archivable", ok=False)

    def test_source_change_during_run_does_not_pass(self):
        data = self.run_evidence(["python3", "-c", "from pathlib import Path; Path('new.py').write_text('x=1')"], ok=False)
        self.assertEqual(data["status"], "changed-during-run")

    def test_referenced_knowledge_is_bound_but_unrelated_knowledge_is_not(self):
        knowledge = self.root / ".sdc/knowledge/technical/local-rule.md"
        knowledge.parent.mkdir(parents=True, exist_ok=True)
        knowledge.write_text("# Local rule\nStatus: Confirmed\n")
        spec = self.change / "spec.md"
        spec.write_text(spec.read_text() + "\nSource: .sdc/knowledge/technical/local-rule.md\n")
        self.applying()
        (knowledge.parent / "unrelated.md").write_text("# Unrelated rule\n")
        self.runtime("state", "get")
        knowledge.write_text(knowledge.read_text() + "Different contract.\n")
        self.runtime("state", "get", ok=False)

    def test_missing_cited_knowledge_cannot_authorize_planning(self):
        spec = self.change / "spec.md"
        spec.write_text(spec.read_text() + "\nSource: .sdc/knowledge/technical/missing.md\n")
        self.state("confirmed", ok=False)

    def test_source_mode_change_invalidates_delivery(self):
        path = self.root / "script.sh"
        path.write_text("exit 0\n")
        self.archivable()
        path.chmod(0o755)
        self.runtime("state", "get", ok=False)

    def test_reopen_drops_obsolete_runtime_ledger(self):
        self.applying()
        ledger = self.root / ".sdc/runtime" / self.change.name / "progress.md"
        self.assertTrue(ledger.exists())
        self.runtime("state", "reopen", "--state", "confirmed", "--reason", "New task plan")
        self.assertFalse(ledger.exists())
        self.assertTrue(list((self.change / "revisions").rglob("progress.md")))

    def test_impact_is_analyzed_after_confirmation_without_invalidating_it(self):
        path = self.change / "impact.md"
        content = path.read_text()
        path.unlink()
        self.state("confirmed")
        path.write_text(content)
        self.manifests()
        self.state("planned")

    def test_open_decision_and_duplicate_question_sections_block_confirmation(self):
        path = self.change / "discovery.md"
        original = path.read_text()
        path.write_text(original.replace("| Confirmed | eval fixture | Keeps scope", "| Open | eval fixture | Keeps scope"))
        self.state("confirmed", ok=False)
        path.write_text(original + "\n## Open Questions\n\nWho can delete bookings?\n")
        self.state("confirmed", ok=False)

    def test_open_decisions_do_not_depend_on_id_prefix(self):
        path = self.change / "discovery.md"
        path.write_text(path.read_text().replace("| D-01 |", "| DEC-01 |").replace("| Confirmed | eval fixture | Keeps scope", "| Open | eval fixture | Keeps scope"))
        self.state("confirmed", ok=False)

    def test_closed_option_does_not_close_a_question(self):
        path = self.change / "discovery.md"
        path.write_text(path.read_text().replace("## Exit Criteria", "| Q1 | Which permission? | Boundary | Closed | plan |\n\n## Exit Criteria"))
        self.state("confirmed", ok=False)

    def test_open_spec_decision_blocks_confirmation(self):
        path = self.change / "spec.md"
        path.write_text(path.read_text().replace("| Confirmed | eval fixture | Yes", "| Open | eval fixture | Yes"))
        self.state("confirmed", ok=False)

    def test_lowercase_verify_still_requires_execution(self):
        path = self.change / "tasks.md"
        path.write_text(path.read_text().replace("- Verify:", "- verify:"))
        self.applying()
        self.review()
        self.state("checking")
        self.state("archivable", ok=False)
        self.run_evidence()
        self.state("archivable")

    def test_accepted_field_spacing_allows_progress_updates(self):
        path = self.change / "tasks.md"
        text = path.read_text().replace("- Review:", "-  Review:").replace("- Evidence:", "-  Evidence:")
        pending = text.replace("[x]", "[ ]").replace("Review: Approved", "Review: Pending").replace("Evidence: notes.md#task-review-evidence", "Evidence: Pending")
        path.write_text(pending)
        self.applying()
        path.write_text(text)
        self.runtime("state", "get")

    def test_quoted_knowledge_paths_with_spaces_are_bound(self):
        path = self.root / ".sdc/knowledge/technical/approval rules.md"
        path.write_text("# Policy\nStatus: Confirmed\n")
        spec = self.change / "spec.md"
        spec.write_text(spec.read_text() + "\nSource: `.sdc/knowledge/technical/approval rules.md`\n")
        self.applying()
        path.write_text("# Policy\nChanged scope.\n")
        self.runtime("state", "get", ok=False)

    def prepare_command_delivery(self, source):
        (self.root / "verify.py").write_text(source)
        tasks = self.change / "tasks.md"
        tasks.write_text(tasks.read_text().replace(self.verify, "python3 verify.py"))
        self.applying()
        self.run_evidence(["python3", "verify.py"])
        self.review()
        self.state("checking")
        self.state("archivable")

    def test_post_run_snapshot_error_preserves_actual_failure(self):
        path = self.root / ".sdc/knowledge/technical/local-rule.md"
        path.write_text("# Policy\nStatus: Confirmed\n")
        spec = self.change / "spec.md"
        spec.write_text(spec.read_text() + "\nSource: .sdc/knowledge/technical/local-rule.md\n")
        self.prepare_command_delivery(
            "from pathlib import Path\n"
            "if Path('.sdc/runtime/fail').exists():\n"
            "    Path('.sdc/knowledge/technical/local-rule.md').unlink()\n"
            "    raise SystemExit(7)\n")
        before = len(list((self.change / "evidence").glob("*.json")))
        (self.root / ".sdc/runtime/fail").touch()
        result = self.run_evidence(["python3", "verify.py"], ok=False)
        self.assertEqual(result.get("exit_code"), 7)
        self.assertEqual(len(list((self.change / "evidence").glob("*.json"))), before + 1)
        path.write_text("# Policy\nStatus: Confirmed\n")
        self.runtime("evidence", "verify", ok=False)

    def test_archive_cannot_race_a_running_verification(self):
        self.prepare_command_delivery(
            "from pathlib import Path\nimport time\n"
            "if Path('.sdc/runtime/wait').exists():\n"
            "    Path('.sdc/runtime/started').touch()\n"
            "    while Path('.sdc/runtime/wait').exists(): time.sleep(0.02)\n"
            "    raise SystemExit(7)\n")
        flag = self.root / ".sdc/runtime/wait"
        flag.touch()
        proc = subprocess.Popen([sys.executable, str(fixtures.RUNTIME_CONTEXT), "evidence", "run",
                                 "--change", self.change.name, "--stage", "check", "--task", "T001", "--task", "T900",
                                 "--timeout", "3", "--", "python3", "verify.py"], cwd=self.root,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        try:
            deadline = time.monotonic() + 2
            while not (self.root / ".sdc/runtime/started").exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertTrue((self.root / ".sdc/runtime/started").exists())
            code, output = fixtures.run_sdc(self.root, "archive", self.change.name)
            self.assertNotEqual(code, 0, output)
            self.assertTrue(self.change.exists())
        finally:
            flag.unlink(missing_ok=True)
            proc.communicate(timeout=5)

    def add_gitlink(self, path):
        for args in (("init", "-q"),
                     ("update-index", "--add", "--cacheinfo", "160000," + "1" * 40 + "," + path)):
            result = subprocess.run(["git", *args], cwd=self.root, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_gitlinks_fail_closed_before_execution(self):
        for path, checked_out in (("vendor module", False), ("vendor module", True), (".sdc/vendor", True)):
            with self.subTest(path=path, checked_out=checked_out):
                self.add_gitlink(path)
                if checked_out:
                    (self.root / path).mkdir(parents=True, exist_ok=True)
                    (self.root / path / "source.py").write_text("VALUE = 1\n")
                marker = self.root / ".sdc/runtime/launched"
                result = self.run_evidence(
                    ["python3", "-c", "from pathlib import Path; Path('.sdc/runtime/launched').touch()"],
                    ok=False)
                self.assertEqual(result["error"], "unsupported-submodule")
                self.assertIn(path, result["message"])
                self.assertFalse(marker.exists())
                subprocess.run(["git", "update-index", "--force-remove", path], cwd=self.root, check=True)

    def test_gitlinks_block_existing_delivery_receipts_and_archive(self):
        self.archivable()
        self.add_gitlink("vendor")
        (self.root / "vendor").mkdir()
        result = self.runtime("evidence", "verify", ok=False)
        self.assertEqual(result["error"], "unsupported-submodule")
        code, output = fixtures.run_sdc(self.root, "archive", self.change.name)
        self.assertNotEqual(code, 0, output)
        self.assertTrue(self.change.exists())

    def test_incomplete_history_requires_new_passes_for_each_affected_task(self):
        self.applying()
        self.run_evidence()
        self.review()
        for status in ("running", "interrupted"):
            with self.subTest(status=status):
                record = self.run_evidence()
                receipt = self.root / record.pop("path")
                record.update(status=status, exit_code=None)
                receipt.write_text(json.dumps(record))
                original = receipt.read_bytes()
                self.runtime("evidence", "verify", ok=False)
                self.run_evidence(tasks=("T001",))
                result = self.runtime("evidence", "verify", ok=False)
                self.assertIn("T900", result["message"])
                self.run_evidence(["python3", "-c", "raise SystemExit(7)"], tasks=("T900",), ok=False)
                self.runtime("evidence", "verify", ok=False)
                self.run_evidence(["python3", "-c", "assert True"], tasks=("T900",))
                self.runtime("evidence", "verify", ok=False)
                self.run_evidence(tasks=("T900",))
                source = self.root / "changed-after-retry.py"
                source.write_text("VALUE = 2\n")
                self.review()
                self.runtime("evidence", "verify", ok=False)
                source.unlink()
                self.review()
                self.assertTrue(self.runtime("evidence", "verify")["valid"])
                self.assertEqual(receipt.read_bytes(), original)
        self.state("checking")
        self.state("archivable")

    def test_incomplete_retry_must_be_newer_and_current_revision(self):
        self.applying()
        record = self.run_evidence()
        receipt = self.root / record.pop("path")
        record.update(status="running", exit_code=None)
        receipt.write_text(json.dumps(record))
        original = receipt.read_bytes()
        retry = self.run_evidence()
        retry_path = self.root / retry.pop("path")
        self.review()
        retry_path.write_text(json.dumps({**retry, "revision": "another-revision"}))
        self.runtime("evidence", "verify", ok=False)
        retry_path.write_text(json.dumps({**retry, "id": "f" * 32, "recorded_at": record["recorded_at"]}))
        self.runtime("evidence", "verify", ok=False)
        retry_path.write_text(json.dumps(retry))
        self.assertTrue(self.runtime("evidence", "verify")["valid"])
        self.assertEqual(receipt.read_bytes(), original)

    @unittest.skipUnless(os.name == "posix", "SIGINT/process-group cleanup requires POSIX")
    def test_sigint_cleanup_then_retry_allows_archive(self):
        self.prepare_command_delivery(
            "from pathlib import Path\nimport json, os, subprocess, sys, time\n"
            "if Path('.sdc/runtime/interrupt').exists():\n"
            "    child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\n"
            "    Path('.sdc/runtime/pids.json').write_text(json.dumps([os.getpid(), child.pid]))\n"
            "    time.sleep(60)\n")
        flag = self.root / ".sdc/runtime/interrupt"
        flag.touch()
        pids_file = self.root / ".sdc/runtime/pids.json"
        proc = subprocess.Popen([sys.executable, str(fixtures.RUNTIME_CONTEXT), "evidence", "run",
                                 "--change", self.change.name, "--stage", "check", "--task", "T001", "--task", "T900",
                                 "--timeout", "10", "--", "python3", "verify.py"], cwd=self.root,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        pids = []
        try:
            deadline = time.monotonic() + 5
            while not pids_file.exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertTrue(pids_file.exists())
            pids = json.loads(pids_file.read_text())
            proc.send_signal(signal.SIGINT)
            output, _ = proc.communicate(timeout=5)
            self.assertNotEqual(proc.returncode, 0, output)
            for pid in pids:
                deadline = time.monotonic() + 5
                while time.monotonic() < deadline:
                    state = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)],
                                           text=True, stdout=subprocess.PIPE).stdout.strip()
                    if not state or state.startswith("Z"):
                        break
                    time.sleep(0.02)
                self.assertTrue(not state or state.startswith("Z"), f"Validation process {pid} remains alive: {state}")
            interrupted = [path for path in (self.change / "evidence").glob("*.json")
                           if json.loads(path.read_text()).get("status") == "interrupted"]
            self.assertEqual(len(interrupted), 1)
            original = interrupted[0].read_bytes()
            self.runtime("evidence", "verify", ok=False)
            flag.unlink()
            self.run_evidence(["python3", "verify.py"])
            self.review()
            self.assertTrue(self.runtime("evidence", "verify")["valid"])
            self.assertEqual(interrupted[0].read_bytes(), original)
            code, output = fixtures.run_sdc(self.root, "archive", self.change.name)
            self.assertEqual(code, 0, output)
        finally:
            flag.unlink(missing_ok=True)
            if proc.poll() is None:
                proc.send_signal(signal.SIGINT)
                try:
                    proc.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.communicate(timeout=5)
            if pids:
                try:
                    os.killpg(pids[0], signal.SIGKILL)
                except ProcessLookupError:
                    pass


if __name__ == "__main__":
    unittest.main()
