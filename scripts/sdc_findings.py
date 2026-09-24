#!/usr/bin/env python3
"""Standalone internal finding ledger. Caller attribution is not authenticated identity.

This module stores claims and fingerprints; it never runs evidence commands.
"""

import argparse
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from sdc_evidence import change_lock, digest_json


SCHEMA = 1
FAILURE_LIMIT = 3
SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonempty text")
    return value.strip()


def _safe_id(value, label):
    if not isinstance(value, str) or not SAFE_ID.fullmatch(value):
        raise ValueError(f"Invalid {label}: {value!r}")
    return value


def _safe_path(root, path):
    current = root
    for part in path.relative_to(root).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"Finding paths must not traverse symlinks: {current}")
    return path


def _ledger_path(root, change_id):
    _safe_id(change_id, "change id")
    root = Path(root).resolve()
    path = _safe_path(root, root / ".sdc/changes/active" / change_id / "findings.json")
    if not path.parent.is_dir():
        raise ValueError(f"Missing active change: {change_id}")
    return root, path


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _read_json(path):
    if not path.is_file():
        raise ValueError(f"Expected a regular JSON file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (OSError, ValueError) as exc:
        raise ValueError(f"Cannot read {path.name}: {exc}") from exc


def _load(path, change_id):
    if not path.exists():
        return {"schema": SCHEMA, "change_id": change_id, "history": []}
    data = _read_json(path)
    if (not isinstance(data, dict) or set(data) != {"schema", "change_id", "history"}
            or type(data["schema"]) is not int or data["schema"] != SCHEMA
            or data["change_id"] != change_id or not isinstance(data["history"], list)):
        raise ValueError("Invalid finding ledger schema or change id")
    return data


def _fingerprint(event):
    return digest_json({key: event[key] for key in ("source", "evidence")})


def _validate_event(event):
    if not isinstance(event, dict):
        raise ValueError("Finding history entries must be objects")
    common = {"kind", "id", "revision", "at", "source", "actor"}
    extra = {"record": {"summary", "evidence", "fingerprint"}, "resolve": {"evidence"},
             "adjudicate": {"decision", "rationale", "retry_limit"}}
    kind = event.get("kind")
    if not isinstance(kind, str) or kind not in extra or set(event) != common | extra[kind]:
        raise ValueError("Invalid finding history event schema")
    _safe_id(event["id"], "finding id")
    for key in common - {"kind", "id"}:
        _text(event[key], key)
    if kind in {"record", "resolve"}:
        _text(event["evidence"], "evidence")
    if kind == "record":
        _text(event["summary"], "summary")
        if event["fingerprint"] != _fingerprint(event):
            raise ValueError("Finding evidence fingerprint does not match its source/evidence")
    if kind == "adjudicate":
        _text(event["rationale"], "rationale")
        decision, limit = event["decision"], event["retry_limit"]
        if decision not in ("retry", "accepted-risk"):
            raise ValueError("Adjudication must be retry or accepted-risk, never a pass")
        if type(limit) is not int or (decision == "retry" and not 1 <= limit <= FAILURE_LIMIT):
            raise ValueError(f"retry_limit must be an integer from 1 to {FAILURE_LIMIT}")
        if decision == "accepted-risk" and limit != 0:
            raise ValueError("accepted-risk cannot authorize retries")


def _replay(history):
    findings, fingerprints, decisions = {}, {}, {}
    for event in history:
        _validate_event(event)
        key, kind = event["id"], event["kind"]
        if key not in findings:
            if kind != "record":
                raise ValueError(f"Unknown finding: {key}")
            findings[key] = {"id": key, "summary": event["summary"], "status": "open",
                             "failed_attempts": 0, "total_failed_attempts": 0,
                             "retry_remaining": FAILURE_LIMIT, "history": []}
            fingerprints[key], decisions[key] = set(), set()
        finding = findings[key]
        status = finding["status"]
        if kind == "record":
            # Identity, revision, and summary labels do not make evidence distinct.
            if event["fingerprint"] not in fingerprints[key]:
                if status in {"adjudication-required", "accepted-risk"}:
                    raise ValueError(f"{key}: {status}; human adjudication must authorize retry")
                if status == "resolved":
                    finding.update(failed_attempts=0, retry_remaining=FAILURE_LIMIT)
                fingerprints[key].add(event["fingerprint"])
                finding["failed_attempts"] += 1
                finding["total_failed_attempts"] += 1
                finding["retry_remaining"] -= 1
                finding["status"] = "open" if finding["retry_remaining"] else "adjudication-required"
            finding["summary"] = event["summary"]
        elif kind == "resolve":
            if status == "adjudication-required":
                raise ValueError(f"{key}: human adjudication is required before resolution")
            if status == "resolved":
                raise ValueError(f"{key}: already resolved")
            finding.update(status="resolved", retry_remaining=0)
        else:
            if status == "resolved":
                raise ValueError(f"{key}: already resolved")
            # A repeated human-decision citation must not replenish an exhausted grant.
            decision_id = event["source"]
            if decision_id in decisions[key]:
                raise ValueError(f"{key}: adjudication already recorded; cite a new human decision")
            if event["decision"] == "retry":
                if status not in {"adjudication-required", "accepted-risk"}:
                    raise ValueError(f"{key}: cannot stack retry authorizations while retries remain")
                finding.update(status="open", retry_remaining=event["retry_limit"])
            else:
                finding.update(status="accepted-risk", retry_remaining=0)
            decisions[key].add(decision_id)
        finding["history"].append(event)
    return list(findings.values())


def _revision(root, directory):
    path = _safe_path(root, directory / "state.json")
    if not path.exists():
        return "initial"
    state = _read_json(path)
    if not isinstance(state, dict):
        raise ValueError("Invalid change state for finding revision")
    return _text(state.get("revision", "initial"), "revision")


def _write(path, data):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".findings-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(data, handle, indent=2, ensure_ascii=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _append(root, change_id, finding_id, kind, **fields):
    _safe_id(finding_id, "finding id")
    root, path = _ledger_path(root, change_id)
    with change_lock(root, change_id):
        root, path = _ledger_path(root, change_id)
        data = _load(path, change_id)
        event = {"kind": kind, "id": finding_id, "revision": _revision(root, path.parent),
                 "at": datetime.now(timezone.utc).isoformat(), **fields}
        if kind == "record":
            event["fingerprint"] = _fingerprint(event)
        data["history"].append(event)
        findings = _replay(data["history"])
        _write(path, data)
        return next(finding for finding in findings if finding["id"] == finding_id)


def record(root: Path, change_id: str, finding_id: str, *, summary: str,
           source: str, evidence: str, actor: str):
    """Record a failed observation; duplicate source/evidence pairs only add history."""
    return _append(root, change_id, finding_id, "record", summary=_text(summary, "summary"),
                   source=_text(source, "source"), evidence=_text(evidence, "evidence"),
                   actor=_text(actor, "actor"))


def resolve(root: Path, change_id: str, finding_id: str, *, source: str,
            evidence: str, actor: str):
    """Resolve with nonempty evidence and attribution, not an authenticated pass."""
    return _append(root, change_id, finding_id, "resolve", source=_text(source, "source"),
                   evidence=_text(evidence, "evidence"), actor=_text(actor, "actor"))


def adjudicate(root: Path, change_id: str, finding_id: str, *, decision: str,
               source: str, rationale: str, actor: str, retry_limit: int = 0):
    """Record a human decision: accept risk or authorize 1-3 more distinct failures."""
    return _append(root, change_id, finding_id, "adjudicate", decision=decision,
                   source=_text(source, "source"), rationale=_text(rationale, "rationale"),
                   actor=_text(actor, "actor"), retry_limit=retry_limit)


def list_findings(root: Path, change_id: str):
    """Read derived findings in insertion order without creating files or taking a lock."""
    _, path = _ledger_path(root, change_id)
    return _replay(_load(path, change_id)["history"])


def assert_clear(root: Path, change_id: str):
    """Raise ValueError for any unresolved finding; absent legacy ledgers are allowed.

    Does not acquire a lock: the caller must hold change_lock across a verdict or
    archive transaction. Malformed ledgers fail closed instead of being reset.
    """
    blocked = [f"{finding['id']} ({finding['status']})"
               for finding in list_findings(root, change_id) if finding["status"] != "resolved"]
    if blocked:
        raise ValueError("Unresolved review findings: " + ", ".join(blocked))


def assert_retry_allowed(root: Path, change_id: str, finding_id: str):
    """Read-only preflight for cooperating retry runners; does not reserve an attempt."""
    _safe_id(finding_id, "finding id")
    for finding in list_findings(root, change_id):
        if finding["id"] == finding_id:
            if finding["status"] != "open" or finding["retry_remaining"] <= 0:
                raise ValueError(f"{finding_id}: {finding['status']}; automatic retry blocked")
            return
    raise ValueError(f"Unknown finding: {finding_id}")


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def main(argv=None):
    parser = _Parser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("record", "resolve", "adjudicate", "list"):
        command = commands.add_parser(name)
        command.add_argument("--root", type=Path, default=Path.cwd())
        command.add_argument("--change", required=True)
        if name == "list":
            continue
        command.add_argument("--id", required=True, dest="finding_id")
        command.add_argument("--source", required=True)
        command.add_argument("--actor", required=True)
        if name in {"record", "resolve"}:
            command.add_argument("--evidence", required=True)
        if name == "record":
            command.add_argument("--summary", required=True)
        if name == "adjudicate":
            command.add_argument("--decision", required=True, choices=("retry", "accepted-risk"))
            command.add_argument("--rationale", required=True)
            command.add_argument("--retry-limit", type=int, default=0)
    try:
        args = vars(parser.parse_args(argv))
        name, root, change_id = args.pop("command"), args.pop("root"), args.pop("change")
        if name == "list":
            result = {"findings": list_findings(root, change_id)}
        else:
            operation = {"record": record, "resolve": resolve, "adjudicate": adjudicate}[name]
            result = {"finding": operation(root, change_id, **args)}
        print(json.dumps({"ok": True, **result}))
        return 0
    except (ValueError, OSError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
