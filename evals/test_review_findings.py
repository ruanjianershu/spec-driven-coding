"""Finding-ledger contracts exercised through real files and CLI subprocesses."""

import importlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts/sdc_findings.py"
sys.path.insert(0, str(REPO / "scripts"))


class ReviewFindingsTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), "The standalone finding ledger is not implemented")
        self.api = importlib.import_module("sdc_findings")
        self.temp = tempfile.TemporaryDirectory(prefix="sdc-findings-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.change_id = "stable-review"
        self.change = self.root / ".sdc/changes/active" / self.change_id
        self.change.mkdir(parents=True)
        self.ledger = self.change / "findings.json"
        self.revision("r1")

    def revision(self, value):
        (self.change / "state.json").write_text(json.dumps({"revision": value}))

    def record(self, finding_id="F-9", source="snapshot-a", evidence="failure-a", **kwargs):
        return self.api.record(self.root, self.change_id, finding_id,
                               summary=kwargs.get("summary", "Missing authorization check"),
                               source=source, evidence=evidence,
                               actor=kwargs.get("actor", "reviewer-label"))

    def resolve(self, finding_id="F-9", **kwargs):
        params = {"source": "verification-receipt", "evidence": "Regression now passes",
                  "actor": "reviewer-label"}
        params.update(kwargs)
        return self.api.resolve(self.root, self.change_id, finding_id, **params)

    def adjudicate(self, decision="retry", finding_id="F-9", **kwargs):
        params = {"source": "human-decision-17", "rationale": "Try the narrower fix once",
                  "actor": "human-label", "retry_limit": 1 if decision == "retry" else 0}
        params.update(kwargs)
        return self.api.adjudicate(self.root, self.change_id, finding_id,
                                   decision=decision, **params)

    def exhaust(self, finding_id="F-9"):
        for index in range(3):
            result = self.record(finding_id, evidence=f"failure-{index}")
        return result

    def cli(self, *args, ok=True):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), *args], cwd=self.root,
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "", result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["ok"], ok)
        if not ok:
            self.assertIsInstance(data["error"], str)
        return data

    def test_legacy_missing_ledger_is_clear_and_read_only(self):
        self.assertIsNone(self.api.assert_clear(self.root, self.change_id))
        self.assertEqual(self.api.list_findings(self.root, self.change_id), [])
        self.assertFalse(self.ledger.exists())
        self.assertFalse((self.root / ".sdc/runtime").exists())

    def test_stable_ids_and_append_only_history(self):
        self.record("F-90")
        before = json.loads(self.ledger.read_text())["history"]
        self.record("F-2", evidence="unrelated defect")
        history = json.loads(self.ledger.read_text())["history"]
        self.assertEqual(history[:len(before)], before)
        self.assertEqual([f["id"] for f in self.api.list_findings(self.root, self.change_id)],
                         ["F-90", "F-2"])
        with self.assertRaisesRegex(ValueError, "F-90.*open"):
            self.api.assert_clear(self.root, self.change_id)

    def test_duplicate_evidence_does_not_count_even_across_revisions_or_labels(self):
        first = self.record()
        self.revision("r2")
        second = self.record(actor="different-label", summary="Reworded finding")
        self.assertEqual(second["failed_attempts"], 1)
        self.assertEqual(second["retry_remaining"], 2)
        self.assertEqual([event["revision"] for event in second["history"]], ["r1", "r2"])
        self.assertEqual(second["history"][0], first["history"][0])
        self.assertEqual(second["history"][0]["fingerprint"],
                         second["history"][1]["fingerprint"])

    def test_fingerprint_tracks_both_source_and_evidence(self):
        self.record(source="source-1", evidence="evidence-1")
        self.record(source="source-2", evidence="evidence-1")
        result = self.record(source="source-2", evidence="evidence-2")
        self.assertEqual(result["failed_attempts"], 3)
        self.assertEqual(result["status"], "adjudication-required")

    def test_unrelated_ids_do_not_share_failure_counts(self):
        for name in ("F-1", "F-2", "F-3"):
            result = self.record(name)
            self.assertEqual(result["failed_attempts"], 1)
            self.assertEqual(result["status"], "open")

    def test_third_failure_blocks_distinct_retry_and_resolution_until_adjudication(self):
        self.exhaust()
        before = self.ledger.read_bytes()
        with self.assertRaisesRegex(ValueError, "adjudication"):
            self.record(evidence="fourth-failure")
        with self.assertRaisesRegex(ValueError, "adjudication"):
            self.api.assert_retry_allowed(self.root, self.change_id, "F-9")
        with self.assertRaisesRegex(ValueError, "adjudication"):
            self.resolve()
        self.assertEqual(self.ledger.read_bytes(), before)
        duplicate = self.record(evidence="failure-0")
        self.assertEqual(duplicate["failed_attempts"], 3)
        self.assertEqual(duplicate["status"], "adjudication-required")
        with self.assertRaises(ValueError):
            self.api.assert_clear(self.root, self.change_id)

    def test_revision_does_not_reset_unresolved_chain_or_modify_archived_files(self):
        self.record(evidence="failure-1")
        self.revision("r2")
        archive = self.change / "revisions/r1/findings.json"
        archive.parent.mkdir(parents=True)
        archive.write_bytes(self.ledger.read_bytes())
        archived = archive.read_bytes()
        self.record(evidence="failure-2")
        self.revision("r3")
        result = self.record(evidence="failure-3")
        self.assertEqual(result["status"], "adjudication-required")
        self.assertEqual([event["revision"] for event in result["history"]], ["r1", "r2", "r3"])
        self.assertEqual(archive.read_bytes(), archived)

    def test_adjudication_grants_bounded_retry_without_resolving_or_resetting_count(self):
        self.exhaust()
        decision = self.adjudicate(retry_limit=2)
        self.assertEqual(decision["status"], "open")
        self.assertEqual(decision["failed_attempts"], 3)
        self.assertEqual(decision["retry_remaining"], 2)
        with self.assertRaises(ValueError):
            self.api.assert_clear(self.root, self.change_id)
        self.api.assert_retry_allowed(self.root, self.change_id, "F-9")
        self.record(evidence="failure-0")
        fourth = self.record(evidence="failure-4")
        self.assertEqual(fourth["retry_remaining"], 1)
        fifth = self.record(evidence="failure-5")
        self.assertEqual(fifth["failed_attempts"], 5)
        self.assertEqual(fifth["retry_remaining"], 0)
        self.assertEqual(fifth["status"], "adjudication-required")
        with self.assertRaises(ValueError):
            self.record(evidence="failure-6")

    def test_adjudication_cannot_be_stacked_or_replayed_to_mint_retries(self):
        self.exhaust()
        self.adjudicate()
        before = self.ledger.read_bytes()
        with self.assertRaises(ValueError):
            self.adjudicate(source="another-decision")
        self.assertEqual(self.ledger.read_bytes(), before)
        self.record(evidence="failure-4")
        with self.assertRaisesRegex(ValueError, "already recorded"):
            self.adjudicate()
        decision = self.adjudicate(source="human-decision-18")
        self.assertEqual(decision["retry_remaining"], 1)

    def test_relabeling_same_adjudication_source_cannot_authorize_more_retries(self):
        self.exhaust()
        self.adjudicate()
        self.record(evidence="failure-4")
        before = self.ledger.read_bytes()
        for changed in ({"actor": "different-label"}, {"rationale": "Reworded rationale"},
                        {"retry_limit": 2}):
            with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, "already recorded"):
                self.adjudicate(**changed)
            self.assertEqual(self.ledger.read_bytes(), before)

    def test_accepted_risk_remains_blocking_and_keeps_unresolved_count(self):
        self.record()
        result = self.adjudicate("accepted-risk")
        self.assertEqual(result["status"], "accepted-risk")
        with self.assertRaisesRegex(ValueError, "accepted-risk"):
            self.api.assert_clear(self.root, self.change_id)
        with self.assertRaises(ValueError):
            self.record(evidence="failure-2")
        with self.assertRaises(ValueError):
            self.api.assert_retry_allowed(self.root, self.change_id, "F-9")
        self.adjudicate(source="human-decision-18")
        result = self.record(evidence="failure-2")
        self.assertEqual(result["failed_attempts"], 2)
        self.assertEqual(result["status"], "adjudication-required")

    def test_resolution_requires_evidence_source_and_attribution(self):
        self.record()
        before = self.ledger.read_bytes()
        for key in ("evidence", "actor", "source"):
            for value in ("", " \n", None, []):
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    self.resolve(**{key: value})
                self.assertEqual(self.ledger.read_bytes(), before)
        result = self.resolve()
        self.assertEqual(result["status"], "resolved")
        self.assertIsNone(self.api.assert_clear(self.root, self.change_id))
        self.assertEqual(result["history"][-1]["actor"], "reviewer-label")

    def test_resolution_after_authorized_retry_requires_its_own_evidence_event(self):
        self.exhaust()
        self.adjudicate()
        with self.assertRaises(ValueError):
            self.api.assert_clear(self.root, self.change_id)
        with self.assertRaises(ValueError):
            self.resolve(evidence=" ")
        result = self.resolve()
        self.assertEqual(result["status"], "resolved")
        self.assertEqual(result["failed_attempts"], 3)
        self.api.assert_clear(self.root, self.change_id)
        with self.assertRaises(ValueError):
            self.adjudicate(source="human-decision-18")
        with self.assertRaises(ValueError):
            self.resolve()

    def test_resolved_issue_reopens_only_for_new_fingerprint_and_preserves_old_chain(self):
        self.record()
        self.record(evidence="failure-b")
        self.resolve()
        replay = self.record()
        self.assertEqual(replay["status"], "resolved")
        result = self.record(evidence="new-regression")
        self.assertEqual(result["id"], "F-9")
        self.assertEqual(result["failed_attempts"], 1)
        self.assertEqual(result["total_failed_attempts"], 3)
        self.assertEqual(len(result["history"]), 5)
        self.assertEqual(result["status"], "open")

    def test_adjudication_requires_bounded_limit_source_rationale_and_actor(self):
        self.exhaust()
        before = self.ledger.read_bytes()
        for key, values in {"source": ["", None], "rationale": ["", " "],
                            "actor": ["", []], "retry_limit": [0, -1, 4, True, 1.5]}.items():
            for value in values:
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    self.adjudicate(**{key: value})
        for decision in ("pass", "resolved", "dismiss"):
            with self.subTest(decision=decision), self.assertRaises(ValueError):
                self.adjudicate(decision)
        self.assertEqual(self.ledger.read_bytes(), before)

    def test_unknown_id_cannot_be_resolved_adjudicated_or_checked_for_retry(self):
        for operation in (self.resolve, self.adjudicate):
            with self.assertRaises(ValueError):
                operation(finding_id="missing")
        with self.assertRaises(ValueError):
            self.api.assert_retry_allowed(self.root, self.change_id, "missing")
        self.assertFalse(self.ledger.exists())

    def test_invalid_ids_and_missing_changes_are_rejected(self):
        for value in ("../escape", "/absolute", "a/b", "a\\b", "..", "", "a\x00b"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.api.assert_clear(self.root, value)
            with self.subTest(finding=value), self.assertRaises(ValueError):
                self.record(value)
        with self.assertRaises(ValueError):
            self.api.assert_clear(self.root, "nonexistent")

    def test_record_requires_nonempty_source_evidence_summary_and_actor(self):
        for field in ("summary", "source", "evidence", "actor"):
            for value in ("", " \n", None, []):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    self.record(**{field: value})
        self.assertFalse(self.ledger.exists())

    def test_malformed_ledgers_fail_closed_and_are_not_overwritten(self):
        self.record()
        valid = json.loads(self.ledger.read_text())
        corrupt = ["{", "null", "[]", "{}", '{"schema":1,"schema":1}',
                   json.dumps({**valid, "schema": 999}),
                   json.dumps({**valid, "change_id": "other-change"}),
                   json.dumps({**valid, "history": [None]}),
                   json.dumps({**valid, "history": [{**valid["history"][0], "fingerprint": "fake"}]})]
        for data in corrupt:
            with self.subTest(data=data):
                self.ledger.write_text(data)
                with self.assertRaises(ValueError):
                    self.api.assert_clear(self.root, self.change_id)
                with self.assertRaises(ValueError):
                    self.record()
                self.assertEqual(self.ledger.read_text(), data)

    def test_symlinked_ledger_or_state_is_rejected_without_writing_target(self):
        target = self.root / "outside.json"
        target.write_text('{"revision":"r1"}')
        for name in ("findings.json", "state.json"):
            with self.subTest(name=name):
                path = self.change / name
                path.unlink(missing_ok=True)
                path.symlink_to(target)
                with self.assertRaises(ValueError):
                    self.record()
                self.assertEqual(target.read_text(), '{"revision":"r1"}')
                path.unlink()
                self.revision("r1")
        self.ledger.symlink_to(self.root / "missing.json")
        with self.assertRaises(ValueError):
            self.api.assert_clear(self.root, self.change_id)

    def test_symlinked_workspace_component_and_delivery_lock_are_rejected(self):
        target = self.root / "outside"
        target.mkdir()
        self.change.rename(target / self.change_id)
        self.change.symlink_to(target / self.change_id, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.api.assert_clear(self.root, self.change_id)
        with self.assertRaises(ValueError):
            self.record()
        self.change.unlink()
        (target / self.change_id).rename(self.change)
        runtime = self.root / ".sdc/runtime"
        runtime.symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.record()
        self.assertFalse((target / self.change_id / "delivery.lock").exists())

    def test_invalid_state_and_cli_ledger_shapes_are_json_errors(self):
        self.record()
        before = self.ledger.read_bytes()
        for data in ("{", "null", "[]", '{"revision":null}', '{"revision":" "}'):
            with self.subTest(data=data):
                (self.change / "state.json").write_text(data)
                with self.assertRaises(ValueError):
                    self.record(evidence="failure-2")
                self.assertEqual(self.ledger.read_bytes(), before)
        self.revision("r2")
        for data in (b"{", b"null", b"[]", b"\xff"):
            self.ledger.write_bytes(data)
            self.cli("list", "--change", self.change_id, ok=False)
            self.assertEqual(self.ledger.read_bytes(), data)

    def test_malformed_transitions_cannot_forge_a_clear_ledger(self):
        self.record()
        valid = json.loads(self.ledger.read_text())
        event = valid["history"][0]
        corrupt = [
            {**event, "kind": "resolved"},
            {key: value for key, value in event.items() if key != "actor"},
            {**event, "revision": None},
            {**event, "kind": "resolve", "evidence": ""},
        ]
        for appended in corrupt:
            self.ledger.write_text(json.dumps({**valid, "history": [event, appended]}))
            with self.subTest(event=appended), self.assertRaises(ValueError):
                self.api.assert_clear(self.root, self.change_id)

    def test_mutation_uses_shared_lock_but_gate_is_safe_inside_parent_lock(self):
        from sdc_evidence import change_lock
        self.record()
        with change_lock(self.root, self.change_id):
            common = ("--change", self.change_id, "--id", "F-9", "--source", "source",
                      "--actor", "label")
            for args in (("record", "--summary", "Issue", "--evidence", "failure"),
                         ("resolve", "--evidence", "Fixed"),
                         ("adjudicate", "--decision", "accepted-risk", "--rationale", "Deferred")):
                result = self.cli(*args, *common, ok=False)
                self.assertIn("busy", result["error"].lower())
            with self.assertRaisesRegex(ValueError, "F-9.*open"):
                self.api.assert_clear(self.root, self.change_id)

    def test_competing_cli_writers_preserve_every_successful_event(self):
        attempts = []
        for index in range(8):
            args = ("record", "--change", self.change_id, "--id", f"F-{index}",
                    "--source", "source", "--evidence", "failure", "--summary", "Issue",
                    "--actor", "label")
            process = subprocess.Popen([sys.executable, "-B", str(SCRIPT), *args], cwd=self.root,
                                       text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.addCleanup(lambda p=process: p.poll() is None and (p.kill(), p.wait()))
            attempts.append((process, args))
        for process, args in attempts:
            output, error = process.communicate(timeout=10)
            self.assertEqual(error, "")
            result = json.loads(output)
            if process.returncode:
                self.assertFalse(result["ok"])
                self.assertIn("busy", result["error"].lower())
                self.cli(*args)
            else:
                self.assertTrue(result["ok"])
        findings = self.api.list_findings(self.root, self.change_id)
        self.assertEqual({finding["id"] for finding in findings}, {f"F-{i}" for i in range(8)})
        self.assertEqual(len(json.loads(self.ledger.read_text())["history"]), 8)
        self.assertEqual(list(self.change.glob(".findings-*.tmp")), [])

    def test_cli_round_trip_and_errors_are_json_without_command_execution(self):
        marker = self.root / "MUST_NOT_EXIST"
        evidence = f"$(touch {marker}); python3 -c 'raise SystemExit(1)'"
        args = ("--change", self.change_id, "--id", "F-9", "--source", "source",
                "--actor", "caller-label")
        recorded = self.cli("record", *args, "--summary", "Bug", "--evidence", evidence)
        self.assertEqual(recorded["finding"]["id"], "F-9")
        self.assertFalse(marker.exists())
        listed = self.cli("list", "--change", self.change_id)
        self.assertEqual(len(listed["findings"]), 1)
        accepted = self.cli("adjudicate", *args, "--decision", "accepted-risk",
                            "--rationale", "Deferred by maintainer")
        self.assertEqual(accepted["finding"]["status"], "accepted-risk")
        resolved = self.cli("resolve", *args, "--evidence", "Regression passes")
        self.assertEqual(resolved["finding"]["status"], "resolved")
        self.api.assert_clear(self.root, self.change_id)
        for bad in (("record",), ("delete",), ("list", "--change", "../escape"),
                    ("adjudicate", *args, "--decision", "pass"),
                    ("adjudicate", *args, "--decision", "retry", "--retry-limit", "abc")):
            with self.subTest(args=bad):
                self.cli(*bad, ok=False)

    def test_cli_explicit_root_and_initial_revision_without_state(self):
        (self.change / "state.json").unlink()
        result = self.cli("record", "--root", str(self.root), "--change", self.change_id,
                          "--id", "F-9", "--summary", "Bug", "--source", "snapshot",
                          "--evidence", "Failure", "--actor", "caller-label")
        self.assertEqual(result["finding"]["history"][0]["revision"], "initial")

    @unittest.skipUnless(os.name == "posix", "FIFO check needs POSIX")
    def test_non_regular_ledger_is_rejected_without_blocking(self):
        os.mkfifo(self.ledger)
        self.cli("list", "--change", self.change_id, ok=False)


if __name__ == "__main__":
    unittest.main()
