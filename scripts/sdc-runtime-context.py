#!/usr/bin/env python3
"""Internal SDC runtime context helper.

This script is intentionally dependency-free. It provides machine-readable
state, active-change resolution, session pointers, and later shared context
helpers without adding public slash commands.
"""

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from sdc_evidence import (
    UnsupportedSubmoduleError, change_lock, change_source_snapshot, execute, input_snapshot, review_snapshot, source_snapshot,
    task_verifications, verification_snapshot,
)
import sdc_compact
from sdc_findings import assert_clear, list_findings


STATE_SCHEMA = "sdc.change-state/v1"
SESSION_POINTER_SCHEMA = "sdc.session-pointer/v1"
RUNTIME_ERROR_SCHEMA = "sdc.runtime-error/v1"
MANIFEST_RECORD_SCHEMA = "sdc.context-manifest-record/v1"
SESSION_CONTEXT_SCHEMA = "sdc.session-context/v1"
EVIDENCE_RECORD_SCHEMA = "sdc.evidence-record/v1"

STATES = (
    "intake",
    "discovery",
    "confirmed",
    "planned",
    "applying",
    "checking",
    "archivable",
)
NEXT_STATES = {state: STATES[index + 1] for index, state in enumerate(STATES[:-1])}
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

STATE_REQUIREMENTS = {
    "discovery": ("change-stage", ("discovery.md",)),
    "confirmed": ("spec-stage", ("spec.md",)),
    "planned": ("plan-stage", ("design.md", "tasks.md", "context-pack.md")),
    "applying": ("apply-stage", ("tasks.md", "context-pack.md")),
    "checking": ("apply-stage", ("tasks.md", "notes.md")),
    "archivable": ("check-stage", ("tasks.md", "notes.md")),
}
STATE_ADDITIONAL_FILES = {
    "planned": ("apply-context.jsonl", "check-context.jsonl"),
}

MANIFEST_SOURCES = {
    "apply": (
        (".sdc/constitution.md", "full", "Apply governance priority, stop-line rules, and execution discipline.", True, "governance"),
        (".sdc/common-ground.md", "full", "Check ESTABLISHED/WORKING/OPEN common ground before implementation.", True, "governance"),
        (".sdc/expert-routing.md", "full", "Confirm expert profiles used by the active change.", True, "governance"),
        (".sdc/knowledge/index.md", "full", "Route only relevant confirmed product and technical knowledge.", True, "knowledge"),
        ("{change}/spec.md", "full", "Implement only confirmed REQ/AC scope.", True, "change-artifact"),
        ("{change}/impact.md", "full", "Respect brownfield impact boundaries and rollback constraints.", False, "change-artifact"),
        ("{change}/design.md", "Global Constraints; API / Contract Specification; Test Matrix", "Use confirmed design contracts and validation matrix.", True, "change-artifact"),
        ("{change}/tasks.md", "full", "Execute dependency-ready T### tasks with review and evidence fields.", True, "change-artifact"),
        ("{change}/context-pack.md", "full", "Use the concise execution handoff and forbidden assumptions.", True, "change-artifact"),
        ("{change}/notes.md", "Validation Evidence; Task Review Evidence", "Append durable implementation evidence.", True, "change-artifact"),
    ),
    "check": (
        (".sdc/constitution.md", "full", "Validate governance, traceability, and stop-line rules.", True, "governance"),
        (".sdc/common-ground.md", "full", "Verify OPEN/WORKING common ground was not promoted silently.", True, "governance"),
        (".sdc/expert-routing.md", "full", "Check expert coverage against actual diff risk.", True, "governance"),
        (".sdc/knowledge/index.md", "full", "Check confirmed knowledge and candidate boundaries.", True, "knowledge"),
        ("{change}/spec.md", "Acceptance Criteria; Traceability", "Verify implementation against confirmed ACs.", True, "change-artifact"),
        ("{change}/impact.md", "full", "Verify brownfield changes stayed inside impact scope.", False, "change-artifact"),
        ("{change}/design.md", "Artifact Output Contract; Test Matrix; Deploy / Release Checklist", "Check output contract drift and release readiness.", True, "change-artifact"),
        ("{change}/tasks.md", "full", "Verify task statuses, interfaces, reviews, and evidence.", True, "change-artifact"),
        ("{change}/context-pack.md", "full", "Verify execution constraints and validation command coverage.", True, "change-artifact"),
        ("{change}/notes.md", "Validation Evidence; Final Whole-Change Review", "Verify durable evidence and final review state.", True, "change-artifact"),
        ("{change}/knowledge-candidates.md", "full", "Confirm candidates remain pending archive promotion.", True, "change-artifact"),
    ),
}

RECALL_ROOTS = (
    ".sdc/knowledge",
    ".sdc/memory",
    ".sdc/current",
    ".sdc/changes/active/{change_id}",
)
RECALL_EXCLUDED_PARTS = {"runtime", "__pycache__", ".git"}
SENSITIVE_RECALL_MARKERS = ("secret", "token", "password", "credential", ".env")
SENSITIVE_VALUE_PATTERNS = (
    re.compile(
        r"(?i)\b(?:password|passwd|secret|credential|api[_-]?key|access[_-]?token|client[_-]?secret)\b"
        r"\s*[:=]\s*[^\s,;]+"
    ),
    re.compile(r"(?i)\bauthorization\s*:\s*(?:bearer|basic)\s+\S+"),
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(
        r"\b(?:sk-(?:live|test|proj)-?[A-Za-z0-9_-]{8,}|gh[pousr]_[A-Za-z0-9]{20,}|"
        r"AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,})\b"
    ),
)
HIGH_ENTROPY_VALUE_RE = re.compile(r"\b[A-Za-z0-9_+=-]{32,}\b")
RESEARCH_STAGES = {"change", "plan", "apply", "check", "archive"}
SESSION_CONTEXT_CLIENTS = {"claude", "codex", "generic"}
EVIDENCE_STATUSES = {"passed", "failed", "blocked", "skipped", "info"}
MAX_SESSION_CONTEXT_CHARS = 4000
MAX_EVIDENCE_RECORDS = 200


class RuntimeErrorWithCode(Exception):
    def __init__(self, code, message, *, candidates=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.candidates = candidates or []


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def emit_json(value):
    # Compact callers need the outcome and digest, not a repository-sized hash map.
    if isinstance(value, dict) and "snapshot" in value:
        snapshot = value["snapshot"]
        compact = value.get("artifact_format") == "compact" or "compact-contract" in snapshot.get("inputs", {})
        if compact:
            value = {key: item for key, item in value.items() if key != "snapshot"}
            value["snapshot_sha256"] = hashlib.sha256(json.dumps(snapshot, sort_keys=True).encode()).hexdigest()
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))


def emit_error(error):
    emit_json(
        {
            "schema": RUNTIME_ERROR_SCHEMA,
            "error": error.code,
            "message": error.message,
            "candidates": error.candidates,
        }
    )


def repo_root():
    return Path.cwd().resolve()


def safe_workspace_path(root, filepath, label, *, must_exist=False):
    root = root.resolve()
    lexical = Path(os.path.abspath(filepath))
    try:
        relative = lexical.relative_to(root)
    except ValueError as exc:
        raise RuntimeErrorWithCode("unsafe-path", f"Unsafe {label} outside repository: {filepath}") from exc

    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise RuntimeErrorWithCode("unsafe-path", f"Unsafe {label} contains a symbolic link: {filepath}")

    try:
        lexical.resolve(strict=False).relative_to(root)
    except ValueError as exc:
        raise RuntimeErrorWithCode("unsafe-path", f"Unsafe {label} escapes repository: {filepath}") from exc
    if must_exist and not lexical.exists():
        raise RuntimeErrorWithCode("missing-path", f"Required {label} does not exist: {filepath}")
    return lexical


def sdc_dir(root):
    return root / ".sdc"


def active_dir(root):
    return sdc_dir(root) / "changes" / "active"


def change_dir(root, change_id):
    return active_dir(root) / change_id


def ensure_sdc(root):
    if not sdc_dir(root).exists():
        raise RuntimeErrorWithCode("workspace-missing", "No .sdc workspace found. Run sdc init first.")
    workspace = safe_workspace_path(root, sdc_dir(root), "SDC workspace", must_exist=True)
    if not workspace.is_dir():
        raise RuntimeErrorWithCode("workspace-missing", "No .sdc workspace found. Run sdc init first.")


def active_candidates(root):
    directory = safe_workspace_path(root, active_dir(root), "active changes directory")
    if not directory.is_dir():
        return []
    return sorted(
        path.name
        for path in directory.iterdir()
        if path.is_dir()
        and not path.is_symlink()
        and safe_workspace_path(root, path, "active change").parent == directory
    )


def require_safe_id(value, label):
    if not value or not SAFE_ID_RE.fullmatch(value):
        raise RuntimeErrorWithCode("invalid-id", f"Invalid {label}: {value!r}")
    return value


def require_active_change(root, change_id, source):
    require_safe_id(change_id, "change id")
    safe_workspace_path(root, active_dir(root), "active changes directory")
    directory = safe_workspace_path(root, change_dir(root, change_id), "active change")
    if not directory.is_dir():
        raise RuntimeErrorWithCode(
            "change-not-found",
            f"{source} selected missing active change: {change_id}",
            candidates=active_candidates(root),
        )
    return directory


def session_pointer_path(root, session_id):
    safe_session = require_safe_id(session_id, "session id")
    return safe_workspace_path(
        root,
        sdc_dir(root) / "runtime" / "sessions" / safe_session / "active-change.json",
        "session pointer",
    )


def read_session_pointer(root, session_id):
    pointer_path = session_pointer_path(root, session_id)
    if not pointer_path.exists():
        return None
    try:
        data = json.loads(pointer_path.read_text())
    except json.JSONDecodeError as exc:
        raise RuntimeErrorWithCode("invalid-session-pointer", f"Invalid session pointer JSON: {exc}") from exc
    if data.get("schema") != SESSION_POINTER_SCHEMA or data.get("session_id") != session_id:
        raise RuntimeErrorWithCode("invalid-session-pointer", f"Invalid session pointer schema for {session_id}")
    if not isinstance(data.get("change_id"), str) or not SAFE_ID_RE.fullmatch(data["change_id"]):
        raise RuntimeErrorWithCode("invalid-session-pointer", f"Invalid session pointer change id for {session_id}")
    if data.get("source") != "explicit":
        raise RuntimeErrorWithCode("invalid-session-pointer", f"Invalid session pointer source for {session_id}")
    try:
        parse_timestamp(data.get("selected_at"), session_id)
    except RuntimeErrorWithCode as exc:
        raise RuntimeErrorWithCode(
            "invalid-session-pointer", f"Invalid session pointer timestamp for {session_id}"
        ) from exc
    return data


def resolve_change(root, *, explicit=None, session_id=None, env=None, validate_state=True):
    ensure_sdc(root)
    env = env or os.environ
    if explicit is not None:
        directory = require_active_change(root, explicit, "explicit --change")
        return resolved_payload(root, explicit, directory, "explicit", validate_state=validate_state)

    env_change = env.get("SDC_ACTIVE_CHANGE", "").strip()
    if env_change:
        directory = require_active_change(root, env_change, "SDC_ACTIVE_CHANGE")
        return resolved_payload(root, env_change, directory, "environment", validate_state=validate_state)

    if session_id:
        pointer = read_session_pointer(root, session_id)
        if pointer:
            change_id = pointer.get("change_id", "")
            directory = require_active_change(root, change_id, "session pointer")
            return resolved_payload(root, change_id, directory, "session", validate_state=validate_state)

    candidates = active_candidates(root)
    if len(candidates) == 1:
        change_id = candidates[0]
        return resolved_payload(root, change_id, change_dir(root, change_id), "single-active", validate_state=validate_state)
    if not candidates:
        raise RuntimeErrorWithCode("no-active-change", "No active changes found. Pass --change or create one with sdc change.")
    raise RuntimeErrorWithCode(
        "ambiguous-active-change",
        "Multiple active changes found. Pass --change <change-id> or set SDC_ACTIVE_CHANGE.",
        candidates=candidates,
    )


def resolved_payload(root, change_id, directory, source, *, validate_state=True):
    return {
        "schema": "sdc.active-change-resolution/v1",
        "change_id": change_id,
        "path": directory.relative_to(root).as_posix(),
        "source": source,
        "state": load_or_derive_state(root, change_id)["state"] if validate_state else read_raw_state(root, change_id)["state"],
    }


def existing_artifact_paths(directory):
    names = ("state.json", "compact.json", "discovery.md", "proposal.md", "spec.md", "impact.md", "design.md", "tasks.md", "context-pack.md", "notes.md")
    return [name for name in names if (directory / name).exists()]


def derive_state(directory):
    # Files are recoverable context, never evidence of approval by themselves.
    if sdc_compact.is_compact(directory) or (directory / "discovery.md").exists() or (directory / "proposal.md").exists():
        return "discovery"
    return "intake"


def state_path(root, change_id):
    return safe_workspace_path(root, change_dir(root, change_id) / "state.json", "change state")


def parse_timestamp(value, change_id):
    if not isinstance(value, str) or not value.strip():
        raise RuntimeErrorWithCode("invalid-state", f"State updated_at is required for {change_id}")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RuntimeErrorWithCode("invalid-state", f"State updated_at is not RFC3339 for {change_id}: {value}") from exc
    if parsed.tzinfo is None:
        raise RuntimeErrorWithCode("invalid-state", f"State updated_at must include a timezone for {change_id}")


def resolve_state_evidence(root, change_id, evidence):
    directory = require_active_change(root, change_id, "state evidence")
    resolved = []
    for value in evidence:
        if not isinstance(value, str) or not value.strip():
            raise RuntimeErrorWithCode("invalid-evidence", f"State evidence path must not be empty for {change_id}")
        relative_value = Path(value)
        if relative_value.is_absolute():
            raise RuntimeErrorWithCode("unsafe-path", f"State evidence must be repository-relative: {value}")
        candidate = root / relative_value if relative_value.parts[:1] == (".sdc",) else directory / relative_value
        candidate = safe_workspace_path(root, candidate, "state evidence", must_exist=True)
        try:
            change_relative = candidate.relative_to(directory)
        except ValueError as exc:
            raise RuntimeErrorWithCode(
                "unsafe-path", f"State evidence must belong to active change {change_id}: {value}"
            ) from exc
        if len(change_relative.parts) != 1 or not candidate.is_file():
            raise RuntimeErrorWithCode(
                "invalid-evidence", f"State evidence must be a top-level active-change file: {value}"
            )
        resolved.append(change_relative.as_posix())
    return resolved


def validate_state_evidence(root, change_id, state, source_kind, evidence):
    requirement = STATE_REQUIREMENTS.get(state)
    if not requirement:
        return []
    expected_source, required_paths = requirement
    if sdc_compact.is_compact(change_dir(root, change_id)):
        required_paths = ("compact.json",)
    if source_kind != expected_source:
        raise RuntimeErrorWithCode(
            "invalid-evidence",
            f"State {state} requires source {expected_source}, received {source_kind or '<empty>'}",
        )
    if not isinstance(evidence, list) or not evidence:
        raise RuntimeErrorWithCode("invalid-evidence", f"State {state} requires evidence: {', '.join(required_paths)}")
    resolved = resolve_state_evidence(root, change_id, evidence)
    missing = [path for path in required_paths if path not in resolved]
    if missing:
        raise RuntimeErrorWithCode("invalid-evidence", f"State {state} is missing evidence: {', '.join(missing)}")
    directory = require_active_change(root, change_id, "state evidence")
    for filename in STATE_ADDITIONAL_FILES.get(state, ()):
        safe_workspace_path(root, directory / filename, "state prerequisite", must_exist=True)
    return resolved


def validate_state_payload(root, data, change_id):
    if data.get("schema") != STATE_SCHEMA:
        raise RuntimeErrorWithCode("invalid-state", f"Invalid state schema for {change_id}")
    if data.get("change_id") != change_id:
        raise RuntimeErrorWithCode("invalid-state", f"State change_id does not match {change_id}")
    if data.get("state") not in STATES:
        raise RuntimeErrorWithCode("invalid-state", f"Unknown lifecycle state for {change_id}: {data.get('state')}")
    parse_timestamp(data.get("updated_at"), change_id)
    source = data.get("source")
    if not isinstance(source, dict):
        raise RuntimeErrorWithCode("invalid-state", f"State source provenance is required for {change_id}")
    kind = source.get("kind")
    paths = source.get("paths")
    if not isinstance(kind, str) or not kind.strip() or not isinstance(paths, list):
        raise RuntimeErrorWithCode("invalid-state", f"State source kind and paths are required for {change_id}")
    validate_state_evidence(root, change_id, data["state"], kind, paths)
    if data["state"] in STATES[2:]:
        if not isinstance(data.get("snapshot"), dict):
            raise RuntimeErrorWithCode("unbound-state", "Legacy state has no evidence snapshot; reopen discovery and revalidate.")
        if data["snapshot"] != lifecycle_snapshot(root, change_id, data["state"]):
            raise RuntimeErrorWithCode("stale-state", "Governing inputs or reviewed sources changed; reopen the affected stage.")
        if data["state"] == "archivable":
            validate_delivery_receipts(root, change_id)
    validate_lifecycle_content_gate(root, change_id, data["state"])


def validate_lifecycle_content_gate(root, change_id, state):
    if state not in STATES[2:]:
        return
    cli = Path(__file__).resolve().parents[1] / "sdc-cli.py"
    result = subprocess.run(
        [sys.executable, str(cli), "__lifecycle-gate", change_id, state],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        detail = re.sub(r"\x1b\[[0-9;]*m", "", result.stdout).strip()
        if len(detail) > 1200:
            detail = detail[-1200:]
        raise RuntimeErrorWithCode(
            "lifecycle-gate-failed",
            f"State {state} content gate failed for {change_id}: {detail or 'validation failed'}",
        )


def load_or_derive_state(root, change_id):
    directory = require_active_change(root, change_id, "state")
    filepath = state_path(root, change_id)
    if filepath.exists():
        try:
            data = json.loads(filepath.read_text())
        except json.JSONDecodeError as exc:
            raise RuntimeErrorWithCode("invalid-state", f"Invalid state JSON for {change_id}: {exc}") from exc
        validate_state_payload(root, data, change_id)
        data["states"] = list(STATES)
        return data

    return {
        "schema": STATE_SCHEMA,
        "change_id": change_id,
        "state": derive_state(directory),
        "updated_at": utc_now(),
        "source": {"kind": "derived", "paths": existing_artifact_paths(directory)},
        "states": list(STATES),
    }


def atomic_write_json(filepath, data):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=filepath.parent, delete=False) as handle:
        handle.write(text)
        temp_name = handle.name
    os.replace(temp_name, filepath)


def atomic_write_text(filepath, text):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=filepath.parent, delete=False) as handle:
        handle.write(text)
        temp_name = handle.name
    os.replace(temp_name, filepath)


def safe_repo_relative(root, path_value):
    path = safe_workspace_path(root, root / path_value, "repository path")
    return path.relative_to(root).as_posix()


def manifest_path(root, change_id, role):
    return safe_workspace_path(
        root, change_dir(root, change_id) / f"{role}-context.jsonl", "context manifest"
    )


def manifest_records(root, change_id, role):
    resolved = resolve_change(root, explicit=change_id, validate_state=False)
    change_relative = Path(resolved["path"]).as_posix()
    records = []
    missing = []
    sources = MANIFEST_SOURCES[role]
    directory = root / change_relative
    if sdc_compact.is_compact(directory):
        data = sdc_compact.load(root, directory)
        sources = [("{change}/compact.json", "full", "Canonical confirmed compact contract, task, and review.", True, "change-artifact")]
        sources += [(name, "full", "Apply existing governance; compact does not override project rules.", required, "governance")
                    for name, required in sdc_compact.governing_sources(root, data).items()]
    for index, (template, section, purpose, required, source_type) in enumerate(sources, start=1):
        relative_value = template.format(change=change_relative)
        relative = safe_repo_relative(root, relative_value)
        filepath = root / relative
        if not filepath.is_file():
            if required:
                missing.append(relative)
            continue
        records.append(
            {
                "schema": MANIFEST_RECORD_SCHEMA,
                "manifest": f"{role}-context",
                "change_id": change_id,
                "role": role,
                "order": index,
                "path": relative,
                "section": section,
                "purpose": purpose,
                "required": required,
                "source_type": source_type,
                "sha256": hashlib_file(filepath),
            }
        )
    if missing:
        raise RuntimeErrorWithCode("manifest-source-missing", "Missing required manifest sources: " + ", ".join(missing))
    return records


def hashlib_file(filepath):
    return hashlib.sha256(filepath.read_bytes()).hexdigest()


def write_manifest(root, change_id, role):
    records = manifest_records(root, change_id, role)
    output = "\n".join(json.dumps(record, ensure_ascii=False, separators=(",", ":")) for record in records) + "\n"
    filepath = manifest_path(root, change_id, role)
    atomic_write_text(filepath, output)
    return {
        "schema": "sdc.context-manifest/v1",
        "change_id": change_id,
        "role": role,
        "records": len(records),
        "path": filepath.relative_to(root).as_posix(),
    }


def compact_excerpt(text, position, width=180):
    start = max(0, position - width // 2)
    end = min(len(text), position + width // 2)
    excerpt = re.sub(r"\s+", " ", text[start:end]).strip()
    if start > 0:
        excerpt = "..." + excerpt
    if end < len(text):
        excerpt = excerpt + "..."
    return excerpt


def looks_high_entropy(value):
    if len(value) < 32 or len(set(value)) < 8:
        return False
    frequencies = (count / len(value) for count in Counter(value).values())
    entropy = -sum(probability * math.log2(probability) for probability in frequencies)
    if value.isdigit():
        return entropy >= 3.1
    if len(value) >= 48 and re.fullmatch(r"[0-9a-fA-F]+", value):
        return entropy >= 3.5
    return entropy >= 4.0


def redact_sensitive_text(value):
    redacted = value
    for pattern in SENSITIVE_VALUE_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    redacted = HIGH_ENTROPY_VALUE_RE.sub(
        lambda match: "[REDACTED]" if looks_high_entropy(match.group(0)) else match.group(0),
        redacted,
    )
    return redacted


def contains_sensitive_value(value):
    return redact_sensitive_text(value) != value


def contains_sensitive_reviewer(value):
    if any(pattern.search(value) for pattern in SENSITIVE_VALUE_PATTERNS):
        return True
    # A bounded, dated review label is prose, not one opaque credential token.
    dated_label = re.fullmatch(
        r"(?:[a-z]{2,16}-){2,}20\d{2}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])(?:-[a-z]{2,16}){0,4}", value)
    if len(value) <= 128 and dated_label and {"review", "reviewer"}.intersection(value.split("-")):
        return contains_sensitive_value(value.replace("-", " "))
    return contains_sensitive_value(value)


def iter_recall_files(root, change_id):
    seen = set()
    for template in RECALL_ROOTS:
        lexical_base = root / template.format(change_id=change_id)
        try:
            base = safe_workspace_path(root, lexical_base, "recall root")
        except RuntimeErrorWithCode:
            continue
        if not base.exists():
            continue
        candidates = [base] if base.is_file() else sorted(base.rglob("*.md"), key=lambda path: path.as_posix())
        for path in candidates:
            try:
                safe_path = safe_workspace_path(root, path, "recall file", must_exist=True)
                safe_path.relative_to(base)
            except (RuntimeErrorWithCode, ValueError):
                continue
            if not safe_path.is_file() or set(safe_path.relative_to(root).parts) & RECALL_EXCLUDED_PARTS:
                continue
            relative = safe_path.relative_to(root).as_posix()
            if any(marker in relative.lower() for marker in SENSITIVE_RECALL_MARKERS):
                continue
            if relative in seen:
                continue
            seen.add(relative)
            yield relative, safe_path


def recall_records(root, change_id, query, limit):
    terms = [term.lower() for term in re.findall(r"[A-Za-z0-9\u4e00-\u9fff_-]+", query)]
    if not terms:
        raise RuntimeErrorWithCode("invalid-query", "Recall query must contain at least one searchable token.")
    bounded_limit = max(1, min(limit, 20))
    matches = []
    for relative, path in iter_recall_files(root, change_id):
        text = path.read_text(errors="ignore")
        lowered = text.lower()
        score = sum(lowered.count(term) for term in terms)
        if score <= 0:
            continue
        positions = [lowered.find(term) for term in terms if lowered.find(term) >= 0]
        position = min(positions) if positions else 0
        line = text[:position].count("\n") + 1
        lines = text.splitlines()
        line_text = lines[line - 1] if line <= len(lines) else ""
        if contains_sensitive_value(line_text):
            continue
        excerpt = re.sub(r"\s+", " ", line_text).strip()
        if contains_sensitive_value(excerpt):
            continue
        matches.append(
            {
                "schema": "sdc.recall-result/v1",
                "status": "Candidate",
                "change_id": change_id,
                "path": relative,
                "line": line,
                "score": score,
                "excerpt": bounded_text(excerpt, 180),
            }
        )
    matches.sort(key=lambda record: (-record["score"], record["path"], record["line"], record["excerpt"]))
    return matches[:bounded_limit]


def write_jsonl(records):
    for record in records:
        print(json.dumps(record, ensure_ascii=False, separators=(",", ":")))


def slugify(value):
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip().lower()).strip("-._")
    return slug or "research"


def research_route(root, change_id, stage, title):
    if stage not in RESEARCH_STAGES:
        raise RuntimeErrorWithCode("invalid-stage", f"Unknown research stage: {stage}")
    resolved = resolve_change(root, explicit=change_id)
    scratch = safe_workspace_path(
        root,
        sdc_dir(root) / "runtime" / resolved["change_id"] / "research" / f"{slugify(title)}.md",
        "research scratch",
    )
    if not scratch.exists():
        atomic_write_text(
            scratch,
            f"# Research Scratch: {title}\n\n- Stage: {stage}\n- Status: Scratch\n- Durable Boundary: knowledge-candidates.md pending archive confirmation\n",
        )
    citation = "discovery.md" if stage == "change" else "notes.md"
    return {
        "schema": "sdc.research-route/v1",
        "change_id": resolved["change_id"],
        "stage": stage,
        "scratch": scratch.relative_to(root).as_posix(),
        "citation": citation,
        "durable_candidate": "knowledge-candidates.md",
        "public_command": None,
    }


def manifest_summary(root, change_id):
    summaries = {}
    for role in sorted(MANIFEST_SOURCES):
        filepath = manifest_path(root, change_id, role)
        if filepath.is_file():
            verify_manifest(root, change_id, role)
        summaries[role] = {
            "path": filepath.relative_to(root).as_posix(),
            "exists": filepath.is_file(),
            "records": len([line for line in filepath.read_text(errors="ignore").splitlines() if line.strip()]) if filepath.is_file() else 0,
        }
    return summaries


def bounded_text(value, limit):
    if len(value) <= limit:
        return value
    return value[: limit - 14].rstrip() + "\n...[truncated]"


def build_session_context(root, resolved, session_id, query):
    change_id = resolved["change_id"]
    state = load_or_derive_state(root, change_id)
    manifests = manifest_summary(root, change_id)
    recall = recall_records(root, change_id, query, 5) if query else []
    lines = [
        "SDC runtime context",
        f"Active change: {change_id}",
        f"Selection source: {resolved['source']}",
        f"Lifecycle state: {state['state']}",
    ]
    if session_id:
        lines.append(f"Session id: {session_id}")
    lines.extend(
        [
            f"Apply manifest: {manifests['apply']['path']} ({'present' if manifests['apply']['exists'] else 'missing'})",
            f"Check manifest: {manifests['check']['path']} ({'present' if manifests['check']['exists'] else 'missing'})",
            "Authority: confirmed specs, design, tasks, and project knowledge outrank runtime state and Candidate recall.",
        ]
    )
    if recall:
        lines.append("Candidate recall (unconfirmed):")
        for record in recall:
            excerpt = bounded_text(record["excerpt"], 220)
            lines.append(f"- {record['path']}:{record['line']} Candidate score={record['score']} {excerpt}")
    else:
        lines.append("Candidate recall (unconfirmed): none")
    lines.append("Manual fallback: run the normal SDC stage command and pass --change or set SDC_ACTIVE_CHANGE when selection is ambiguous.")
    return bounded_text("\n".join(lines), MAX_SESSION_CONTEXT_CHARS), manifests, recall


def session_context_payload(root, args):
    if args.client not in SESSION_CONTEXT_CLIENTS:
        raise RuntimeErrorWithCode("invalid-client", f"Unknown session context client: {args.client}")
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id)
    context, manifests, recall = build_session_context(root, resolved, args.session_id, args.query)
    if args.client == "claude":
        return {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        }
    return {
        "schema": SESSION_CONTEXT_SCHEMA,
        "client": args.client,
        "session_id": args.session_id,
        "change_id": resolved["change_id"],
        "change_path": resolved["path"],
        "selection_source": resolved["source"],
        "state": resolved["state"],
        "manifests": manifests,
        "recall_count": len(recall),
        "additionalContext": context,
    }


def evidence_output_path(root, change_id):
    return safe_workspace_path(
        root, sdc_dir(root) / "runtime" / change_id / "evidence.jsonl", "runtime evidence"
    )


def require_safe_command(value):
    command = value.strip()
    if not command:
        raise RuntimeErrorWithCode("invalid-evidence", "Evidence command must not be empty.")
    if contains_sensitive_value(command):
        raise RuntimeErrorWithCode("sensitive-evidence", "Evidence command appears to contain a sensitive value.")
    return bounded_text(command, 300)


def append_evidence_record(root, change_id, record):
    filepath = evidence_output_path(root, change_id)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if filepath.exists():
        existing = [line for line in filepath.read_text(errors="ignore").splitlines() if line.strip()]
    next_lines = existing[-(MAX_EVIDENCE_RECORDS - 1) :] + [
        json.dumps(record, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    ]
    atomic_write_text(filepath, "\n".join(next_lines) + "\n")
    return filepath


def cmd_resolve(args):
    emit_json(resolve_change(repo_root(), explicit=args.change, session_id=args.session_id))


def cmd_select(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change)
    pointer_path = session_pointer_path(root, args.session_id)
    payload = {
        "schema": SESSION_POINTER_SCHEMA,
        "session_id": args.session_id,
        "change_id": resolved["change_id"],
        "selected_at": utc_now(),
        "source": "explicit",
    }
    atomic_write_json(pointer_path, payload)
    emit_json({**payload, "path": pointer_path.relative_to(root).as_posix()})


def cmd_state_get(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id)
    emit_json(load_or_derive_state(root, resolved["change_id"]))


def cmd_state_set(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id, validate_state=False)
    with change_lock(root, resolved["change_id"]):
        return set_state_locked(args)


def set_state_locked(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id)
    change_id = resolved["change_id"]
    current = load_or_derive_state(root, change_id)
    expected_next = NEXT_STATES.get(current["state"])
    materializing_derived_state = not state_path(root, change_id).exists() and args.state == current["state"]
    same_state = args.state == current["state"]
    if not materializing_derived_state and not same_state and expected_next != args.state:
        raise RuntimeErrorWithCode(
            "invalid-transition",
            f"Invalid transition for {change_id}: {current['state']} -> {args.state}; expected {expected_next or 'terminal'}",
        )

    evidence = validate_state_evidence(root, change_id, args.state, args.source, args.evidence)
    validate_lifecycle_content_gate(root, change_id, args.state)
    if args.state in {"planned", "applying"}:
        for role in MANIFEST_SOURCES:
            verify_manifest(root, change_id, role)
    if args.state == "archivable":
        validate_delivery_receipts(root, change_id)
    if same_state and state_path(root, change_id).exists():
        emit_json(current)
        return
    payload = {
        "schema": STATE_SCHEMA,
        "change_id": change_id,
        "state": args.state,
        "updated_at": utc_now(),
        "source": {"kind": args.source, "paths": evidence},
        "revision": current.get("revision", "initial"),
        "history": current.get("history", []),
    }
    if sdc_compact.is_compact(change_dir(root, change_id)):
        payload["artifact_format"] = "compact"
    if args.state in STATES[2:]:
        payload["snapshot"] = lifecycle_snapshot(root, change_id, args.state)
    filepath = state_path(root, change_id)
    atomic_write_json(filepath, payload)
    emit_json({**payload, "path": filepath.relative_to(root).as_posix(), "states": list(STATES)})


def cmd_manifest_generate(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id)
    emit_json(write_manifest(root, resolved["change_id"], args.role))


def cmd_recall(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id)
    write_jsonl(recall_records(root, resolved["change_id"], args.query, args.limit))


def cmd_research_route(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id)
    emit_json(research_route(root, resolved["change_id"], args.stage, args.title))


def cmd_session_context(args):
    emit_json(session_context_payload(repo_root(), args))


def cmd_evidence_append(args):
    root = repo_root()
    if args.stage not in RESEARCH_STAGES:
        raise RuntimeErrorWithCode("invalid-stage", f"Unknown evidence stage: {args.stage}")
    if args.status not in EVIDENCE_STATUSES:
        raise RuntimeErrorWithCode("invalid-status", f"Unknown evidence status: {args.status}")
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id)
    evidence_path = safe_repo_relative(root, args.path) if args.path else None
    if evidence_path and contains_sensitive_value(evidence_path):
        raise RuntimeErrorWithCode("sensitive-evidence", "Evidence path appears to contain a sensitive value.")
    record = {
        "schema": EVIDENCE_RECORD_SCHEMA,
        "provenance": "agent-assertion-not-execution",
        "change_id": resolved["change_id"],
        "session_id": args.session_id,
        "stage": args.stage,
        "command": require_safe_command(args.command),
        "status": args.status,
        "path": evidence_path,
        "summary": bounded_text(redact_sensitive_text(args.summary.strip()), 500) if args.summary else "",
        "recorded_at": utc_now(),
    }
    filepath = append_evidence_record(root, resolved["change_id"], record)
    emit_json(
        {
            "schema": "sdc.evidence-append/v1",
            "change_id": resolved["change_id"],
            "path": filepath.relative_to(root).as_posix(),
            "records_kept": len(filepath.read_text(errors="ignore").splitlines()),
        }
    )


def lifecycle_snapshot(root, change_id, state):
    directory = require_active_change(root, change_id, "snapshot")
    result = {"requirements": input_snapshot(root, directory)}
    if state in {"planned", "applying", "checking", "archivable"}:
        result["plan"] = input_snapshot(root, directory, plan=True)
    if state in {"checking", "archivable"}:
        result["sources"] = change_source_snapshot(root, directory)
    if state == "archivable":
        result["review"] = review_snapshot(root, directory)
    return result


def verify_manifest(root, change_id, role):
    path = safe_workspace_path(root, manifest_path(root, change_id, role), "manifest", must_exist=True)
    try:
        records = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    except (ValueError, UnicodeError) as exc:
        raise RuntimeErrorWithCode("invalid-manifest", "Manifest must contain valid UTF-8 JSONL.") from exc
    expected = manifest_records(root, change_id, role)
    if records != expected:
        raise RuntimeErrorWithCode("stale-manifest", f"{role} manifest schema, source set, or hashes changed; refresh only after validating inputs.")
    return {"role": role, "records": len(records), "valid": True}


def cmd_manifest_verify(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id)
    emit_json(verify_manifest(root, resolved["change_id"], args.role))


def read_raw_state(root, change_id):
    path = state_path(root, change_id)
    if not path.exists():
        return {"state": "discovery", "revision": "initial"}
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or data.get("change_id") != change_id or data.get("state") not in STATES:
        raise RuntimeErrorWithCode("invalid-state", "State identity is invalid; refusing to reuse or reopen evidence.")
    return data


def cmd_state_reopen(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id, validate_state=False)
    with change_lock(root, resolved["change_id"]):
        return reopen_state_locked(args)


def reopen_state_locked(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id, validate_state=False)
    change_id = resolved["change_id"]
    directory = require_active_change(root, change_id, "reopen")
    reason = args.reason.strip()
    if not reason or contains_sensitive_value(reason):
        raise RuntimeErrorWithCode("invalid-reason", "Reopening requires a non-sensitive reason.")
    current = read_raw_state(root, change_id)
    if args.to_standard and (args.state != "discovery" or not sdc_compact.is_compact(directory)):
        raise RuntimeErrorWithCode("invalid-escalation", "Only compact changes can explicitly escalate to standard discovery.")
    if args.state == "confirmed":
        previous = current.get("snapshot", {}).get("requirements")
        if previous != input_snapshot(root, directory):
            raise RuntimeErrorWithCode("stale-requirements", "Requirements changed or are unbound; reopen discovery for confirmation first.")
        validate_lifecycle_content_gate(root, change_id, "confirmed")
    revision = uuid.uuid4().hex
    backup = safe_workspace_path(root, directory / "revisions" / revision, "revision archive")
    if sdc_compact.is_compact(directory):
        data = sdc_compact.load(root, directory)
        backup.mkdir(parents=True)
        for name in ("compact.json", "state.json", "apply-context.jsonl", "check-context.jsonl", "findings.json", "notes.md"):
            path = safe_workspace_path(root, directory / name, "compact revision source")
            if path.is_file():
                shutil.copyfile(path, backup / name)
        baseline = safe_workspace_path(root, directory / "evidence/baseline/source.json", "compact source baseline", must_exist=True)
        (backup / "evidence/baseline").mkdir(parents=True)
        shutil.copyfile(baseline, backup / "evidence/baseline/source.json")
        data["task"]["complete"] = False
        data["review"] = {"spec": "pending", "quality": "pending"}
        if args.state == "discovery":
            data["intake"]["authorization"] = ""
            data["intake"]["open_questions"] = ["Reconfirm changed scope: " + reason]
        if not args.to_standard:
            atomic_write_json(directory / "compact.json", data)
        history = list(current.get("history", []))
        history.append({"from": current["state"], "to": args.state, "reason": reason, "revision": revision})
        payload = {"schema": STATE_SCHEMA, "change_id": change_id, "state": args.state,
                   "artifact_format": "compact", "revision": revision, "history": history, "updated_at": utc_now(),
                   "source": {"kind": "change-stage" if args.state == "discovery" else "spec-stage", "paths": ["compact.json"]}}
        if args.to_standard:
            # Keep only a minimal draft until the broader requirement is confirmed.
            discovery = ("# Discovery\n\n## Current Understanding\n"
                         "Previous compact scope is historical, not approval for the expanded request.\n\n"
                         "## Decision Ledger\n| ID | Decision | Status | Source | Impact | Next Step |\n"
                         "| --- | --- | --- | --- | --- | --- |\n\n"
                         "## Open Questions\n- Confirm the revised scope, acceptance, and authority: " + reason +
                         "\n\n## Exit Criteria\n- [ ] Revised scope and authority confirmed\n")
            for name, text in {"discovery.md": discovery,
                               "proposal.md": "# Change Proposal\n\nStatus: Draft\n\n## 背景\n" + reason + "\n\n## 目标\nPending confirmation.\n",
                               "notes.md": "# Notes\n\n## Revision\nEscalated from compact; preserved in revisions/" + revision + "/.\n"}.items():
                atomic_write_text(directory / name, text)
            (directory / "compact.json").unlink()
            payload["artifact_format"] = "standard"
            payload["source"]["paths"] = ["discovery.md", "proposal.md", "notes.md"]
        if args.state == "confirmed":
            payload["snapshot"] = lifecycle_snapshot(root, change_id, "confirmed")
        atomic_write_json(state_path(root, change_id), payload)
        for role in MANIFEST_SOURCES:
            path = manifest_path(root, change_id, role)
            if path.exists():
                path.unlink()
        emit_json(payload)
        return
    names = ["design.md", "tasks.md", "context-pack.md", "notes.md", "apply-context.jsonl", "check-context.jsonl", "state.json"]
    if args.state == "discovery":
        names += ["spec.md", "impact.md", "proposal.md", "knowledge-candidates.md"]
    files = [safe_workspace_path(root, directory / name, "revision source") for name in names]
    safe_workspace_path(root, directory / "discovery.md", "discovery evidence", must_exist=True)
    ledger = safe_workspace_path(root, sdc_dir(root) / "runtime" / change_id / "progress.md", "revision ledger")
    files.append(ledger)
    backup.mkdir(parents=True)
    for path in files:
        if path.is_file():
            shutil.copyfile(path, backup / path.name)
    history = list(current.get("history", []))
    history.append({"from": current["state"], "to": args.state, "reason": bounded_text(reason, 500),
                    "at": utc_now(), "archive": backup.relative_to(root).as_posix(),
                    "previous_revision": current.get("revision", "initial")})
    payload = {"schema": STATE_SCHEMA, "change_id": change_id, "state": args.state,
               "updated_at": utc_now(), "revision": revision, "history": history,
               "source": {"kind": "change-stage" if args.state == "discovery" else "spec-stage",
                          "paths": ["discovery.md"] if args.state == "discovery" else ["spec.md"]}}
    if args.state == "confirmed":
        payload["snapshot"] = lifecycle_snapshot(root, change_id, "confirmed")
    # Save the lowered state first: an interruption cannot retain delivery authorization.
    atomic_write_json(state_path(root, change_id), payload)
    for path in files:
        if path.name != "state.json" and path.is_file():
            path.unlink()
    atomic_write_text(directory / "notes.md", "# Notes\n\n## Revision\n\n" + reason + "\n")
    emit_json(payload)


def receipt_directory(root, change_id):
    return safe_workspace_path(root, change_dir(root, change_id) / "evidence", "durable evidence")


def save_receipt(root, change_id, record):
    require_active_change(root, change_id, "receipt destination")
    directory = receipt_directory(root, change_id)
    path = safe_workspace_path(root, directory / (record["id"] + ".json"), "receipt")
    atomic_write_json(path, record)
    return path.relative_to(root).as_posix()


def receipt_base(root, change_id, kind):
    return {"schema": "sdc.delivery-receipt/v1", "id": uuid.uuid4().hex, "kind": kind,
            "change_id": change_id, "revision": read_raw_state(root, change_id).get("revision", "initial"),
            "recorded_at": datetime.now(timezone.utc).isoformat(timespec="microseconds")}


def cmd_evidence_run(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id, validate_state=False)
    with change_lock(root, resolved["change_id"]):
        return run_evidence_locked(args)


def run_evidence_locked(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id, validate_state=False)
    change_id = resolved["change_id"]
    directory = require_active_change(root, change_id, "validation run")
    paused = [f["id"] for f in list_findings(root, change_id) if f["status"] in {"adjudication-required", "accepted-risk"}]
    if paused:
        raise RuntimeErrorWithCode("repair-adjudication-required", "Human adjudication required before another automatic run: " + ", ".join(paused))
    if sdc_compact.is_compact(directory):
        sdc_compact.validate(root, directory)
    argv = args.argv[1:] if args.argv[:1] == ["--"] else args.argv
    if not argv or not 0 < args.timeout <= 3600 or not math.isfinite(args.timeout):
        raise RuntimeErrorWithCode("invalid-command", "Supply argv after -- and a finite timeout from 0 to 3600 seconds.")
    for arg in argv:
        if contains_sensitive_value(arg):
            raise RuntimeErrorWithCode("sensitive-evidence", "Do not put credentials in validation arguments.")
    tasks = task_verifications(directory)
    if any(task not in tasks for task in args.task):
        raise RuntimeErrorWithCode("invalid-task", "Execution receipts must identify planned tasks with Verify commands.")
    # Validate the destination before starting a command that could have side effects.
    receipt_directory(root, change_id)
    before = verification_snapshot(root, directory)
    record = receipt_base(root, change_id, "execution")
    record.update({"argv": argv, "tasks": sorted(set(args.task)), "stage": args.stage,
                   "status": "running", "exit_code": None, "snapshot": before,
                   "environment": {"platform": sys.platform, "python": sys.version.split()[0]}})
    save_receipt(root, change_id, record)
    try:
        record.update(execute(argv, root, args.timeout))
        try:
            if verification_snapshot(root, directory) != before:
                record["status"] = "changed-during-run"
        except (ValueError, OSError) as exc:
            record["status"] = "snapshot-error"
            record["error"] = bounded_text(redact_sensitive_text(str(exc)), 500)
    except BaseException:
        record["status"] = "interrupted"
        save_receipt(root, change_id, record)
        raise
    record["completed_at"] = datetime.now(timezone.utc).isoformat(timespec="microseconds")
    record["path"] = save_receipt(root, change_id, record)
    emit_json(record)
    return 0 if record["status"] == "passed" else 1


def cmd_evidence_review(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id, validate_state=False)
    with change_lock(root, resolved["change_id"]):
        return review_evidence_locked(args)


def review_evidence_locked(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id, validate_state=False)
    change_id = resolved["change_id"]
    reviewer = args.reviewer.strip()
    if not reviewer or contains_sensitive_reviewer(reviewer):
        raise RuntimeErrorWithCode("invalid-reviewer", "A non-sensitive reviewer attribution is required.")
    directory = require_active_change(root, change_id, "review receipt")
    if sdc_compact.is_compact(directory) and sdc_compact.load(root, directory).get("review", {}).get("reviewer") != reviewer:
        raise RuntimeErrorWithCode("invalid-reviewer", "Review receipt attribution must match the compact review record.")
    cli = Path(__file__).resolve().parents[1] / "sdc-cli.py"
    result = subprocess.run([sys.executable, str(cli), "__lifecycle-gate", change_id, "reviewed"],
                            cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode:
        raise RuntimeErrorWithCode("review-not-approved", bounded_text(result.stdout, 1200))
    record = receipt_base(root, change_id, "review")
    record.update({"reviewer": reviewer, "status": "approved", "snapshot": review_snapshot(root, directory),
                   "attribution": "caller-declared; not identity authentication"})
    record["path"] = save_receipt(root, change_id, record)
    emit_json(record)


def validate_delivery_receipts(root, change_id):
    directory = require_active_change(root, change_id, "delivery receipts")
    assert_clear(root, change_id)
    for role in MANIFEST_SOURCES:
        verify_manifest(root, change_id, role)
    receipts = receipt_directory(root, change_id)
    revision = read_raw_state(root, change_id).get("revision", "initial")
    records = []
    for path in sorted(receipts.glob("*.json")) if receipts.exists() else []:
        safe_workspace_path(root, path, "receipt", must_exist=True)
        record = json.loads(path.read_text())
        if not isinstance(record, dict) or record.get("schema") != "sdc.delivery-receipt/v1" or record.get("change_id") != change_id:
            raise RuntimeErrorWithCode("invalid-receipt", "Malformed or mismatched delivery receipt.")
        parse_timestamp(record.get("recorded_at"), change_id)
        if record.get("revision") == revision:
            records.append(record)
    def recorded_at(record):
        return datetime.fromisoformat(record["recorded_at"].replace("Z", "+00:00"))

    records.sort(key=lambda record: (recorded_at(record), record["id"]))
    current = verification_snapshot(root, directory)
    tasks = task_verifications(directory)
    for task, details in tasks.items():
        if not details["complete"]:
            continue
        matches = [record for record in records if record.get("kind") == "execution" and task in record.get("tasks", [])]
        latest = matches[-1] if matches else {}
        incomplete = [record for record in matches if record.get("status") in {"running", "interrupted"}]
        if incomplete and recorded_at(latest) <= max(recorded_at(record) for record in incomplete):
            raise RuntimeErrorWithCode(
                "incomplete-execution", f"{task} needs a newer successful receipt to supersede its pending or interrupted validation.")
        if (latest.get("status") != "passed" or latest.get("exit_code") != 0
                or latest.get("snapshot") != current or latest.get("argv") != details["argv"]):
            raise RuntimeErrorWithCode("missing-fresh-execution", f"{task} needs a successful current-revision receipt matching its Verify command.")
    reviews = [record for record in records if record.get("kind") == "review"]
    review = reviews[-1] if reviews else {}
    if review.get("status") != "approved" or not review.get("reviewer") or review.get("snapshot") != review_snapshot(root, directory):
        raise RuntimeErrorWithCode("missing-fresh-review", "An approved review receipt for the current source and review artifacts is required.")
    return {"valid": True, "revision": revision, "tasks": sorted(task for task, data in tasks.items() if data["complete"])}


def cmd_evidence_verify(args):
    root = repo_root()
    resolved = resolve_change(root, explicit=args.change, session_id=args.session_id, validate_state=False)
    emit_json(validate_delivery_receipts(root, resolved["change_id"]))


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve_parser = subparsers.add_parser("resolve", help="Resolve exactly one active SDC change.")
    resolve_parser.add_argument("--change")
    resolve_parser.add_argument("--session-id")
    resolve_parser.set_defaults(func=cmd_resolve)

    select_parser = subparsers.add_parser("select", help="Select an active change for a local session.")
    select_parser.add_argument("--change", required=True)
    select_parser.add_argument("--session-id", required=True)
    select_parser.set_defaults(func=cmd_select)

    state_parser = subparsers.add_parser("state", help="Read or advance lifecycle state.")
    state_subparsers = state_parser.add_subparsers(dest="state_command", required=True)

    state_get = state_subparsers.add_parser("get", help="Read lifecycle state.")
    state_get.add_argument("--change")
    state_get.add_argument("--session-id")
    state_get.set_defaults(func=cmd_state_get)

    state_set = state_subparsers.add_parser("set", help="Advance lifecycle state.")
    state_set.add_argument("--change")
    state_set.add_argument("--session-id")
    state_set.add_argument("--state", required=True, choices=STATES)
    state_set.add_argument("--source", default="manual")
    state_set.add_argument("--evidence", action="append", default=[])
    state_set.set_defaults(func=cmd_state_set)

    state_reopen = state_subparsers.add_parser("reopen", help="Retain history and invalidate downstream approvals.")
    state_reopen.add_argument("--change")
    state_reopen.add_argument("--session-id")
    state_reopen.add_argument("--state", required=True, choices=("discovery", "confirmed"))
    state_reopen.add_argument("--reason", required=True)
    state_reopen.add_argument("--to-standard", action="store_true", help="Escalate compact to standard discovery without deleting history.")
    state_reopen.set_defaults(func=cmd_state_reopen)

    manifest_parser = subparsers.add_parser("manifest", help="Generate role-specific context manifests.")
    manifest_subparsers = manifest_parser.add_subparsers(dest="manifest_command", required=True)

    manifest_generate = manifest_subparsers.add_parser("generate", help="Generate apply/check context JSONL.")
    manifest_generate.add_argument("--change")
    manifest_generate.add_argument("--session-id")
    manifest_generate.add_argument("--role", required=True, choices=sorted(MANIFEST_SOURCES))
    manifest_generate.set_defaults(func=cmd_manifest_generate)

    manifest_verify = manifest_subparsers.add_parser("verify", help="Verify schema, source set, and current hashes.")
    manifest_verify.add_argument("--change")
    manifest_verify.add_argument("--session-id")
    manifest_verify.add_argument("--role", required=True, choices=sorted(MANIFEST_SOURCES))
    manifest_verify.set_defaults(func=cmd_manifest_verify)

    recall_parser = subparsers.add_parser("recall", help="Search local SDC memory as Candidate-only JSONL.")
    recall_parser.add_argument("--change")
    recall_parser.add_argument("--session-id")
    recall_parser.add_argument("--query", required=True)
    recall_parser.add_argument("--limit", type=int, default=5)
    recall_parser.set_defaults(func=cmd_recall)

    research_parser = subparsers.add_parser("research", help="Route internal research artifacts.")
    research_subparsers = research_parser.add_subparsers(dest="research_command", required=True)

    research_route_parser = research_subparsers.add_parser("route", help="Return scratch/citation/candidate destinations.")
    research_route_parser.add_argument("--change")
    research_route_parser.add_argument("--session-id")
    research_route_parser.add_argument("--stage", required=True, choices=sorted(RESEARCH_STAGES))
    research_route_parser.add_argument("--title", required=True)
    research_route_parser.set_defaults(func=cmd_research_route)

    session_context = subparsers.add_parser("session-context", help="Emit compact active-change context for supported clients.")
    session_context.add_argument("--client", required=True, choices=sorted(SESSION_CONTEXT_CLIENTS))
    session_context.add_argument("--session-id")
    session_context.add_argument("--change")
    session_context.add_argument("--query")
    session_context.set_defaults(func=cmd_session_context)

    evidence_parser = subparsers.add_parser("evidence", help="Append ignored local runtime evidence.")
    evidence_subparsers = evidence_parser.add_subparsers(dest="evidence_command", required=True)

    evidence_append = evidence_subparsers.add_parser("append", help="Append a bounded runtime evidence JSONL record.")
    evidence_append.add_argument("--change")
    evidence_append.add_argument("--session-id")
    evidence_append.add_argument("--stage", required=True)
    evidence_append.add_argument("--command", required=True)
    evidence_append.add_argument("--status", required=True)
    evidence_append.add_argument("--path")
    evidence_append.add_argument("--summary")
    evidence_append.set_defaults(func=cmd_evidence_append)

    evidence_run = evidence_subparsers.add_parser("run", help="Execute an authorized command and persist a measured receipt.")
    evidence_run.add_argument("--change")
    evidence_run.add_argument("--session-id")
    evidence_run.add_argument("--stage", choices=("apply", "check"), required=True)
    evidence_run.add_argument("--task", action="append", required=True)
    evidence_run.add_argument("--timeout", type=float, default=300)
    evidence_run.add_argument("argv", nargs=argparse.REMAINDER)
    evidence_run.set_defaults(func=cmd_evidence_run)

    evidence_review = evidence_subparsers.add_parser("review", help="Bind an already completed independent review to its inputs.")
    evidence_review.add_argument("--change")
    evidence_review.add_argument("--session-id")
    evidence_review.add_argument("--reviewer", required=True)
    evidence_review.set_defaults(func=cmd_evidence_review)

    evidence_verify = evidence_subparsers.add_parser("verify", help="Verify fresh task execution and review receipts.")
    evidence_verify.add_argument("--change")
    evidence_verify.add_argument("--session-id")
    evidence_verify.set_defaults(func=cmd_evidence_verify)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.func(args)
    except RuntimeErrorWithCode as exc:
        emit_error(exc)
        return 2
    except UnsupportedSubmoduleError as exc:
        emit_error(RuntimeErrorWithCode("unsupported-submodule", str(exc)))
        return 2
    except (ValueError, OSError) as exc:
        emit_error(RuntimeErrorWithCode("invalid-evidence", str(exc)))
        return 2
    if isinstance(result, int):
        return result
    return 0


if __name__ == "__main__":
    sys.exit(main())
