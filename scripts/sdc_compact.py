"""Narrow, single-authority contracts for behavior-neutral documentation changes.

Semantic eligibility is a cited human/agent assessment, not a file-extension proof.
The runtime enforces structure, declared paths, freshness, and evidence boundaries.
"""

import copy
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "sdc.compact/v1"
EXCLUSIONS = {"behavior", "data", "security", "public_contract", "architecture", "deployment"}
GOVERNANCE = ("AGENTS.md", "CLAUDE.md", ".sdc/constitution.md", ".sdc/common-ground.md",
              ".sdc/expert-routing.md", ".sdc/knowledge/index.md")
STANDARD_ARTIFACTS = ("discovery.md", "proposal.md", "spec.md", "design.md", "tasks.md", "context-pack.md", "impact.md")


def safe_path(root, name):
    if not isinstance(name, str) or not name or "\\" in name or "\0" in name:
        raise ValueError("Compact paths must be nonempty repository-relative paths")
    relative = Path(name)
    if relative.is_absolute() or any(part in {"..", "."} for part in name.split("/")):
        raise ValueError("Compact paths must stay inside the target repository")
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Compact paths must not traverse symlinks: " + name)
    return current


def is_compact(directory):
    if (directory / "compact.json").exists() or (directory / "compact.json").is_symlink():
        return True
    state = directory / "state.json"
    if state.is_file() and not state.is_symlink():
        data = json.loads(state.read_text())
        if not isinstance(data, dict):
            raise ValueError("Invalid lifecycle state object")
        return data.get("artifact_format") == "compact"
    return False


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Compact requires " + label)


def validate_record(data, root, *, delivery=False):
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise ValueError("Unsupported compact schema")
    intake = data.get("intake")
    if not isinstance(intake, dict):
        raise ValueError("Compact requires confirmed intake")
    for field in ("request", "context", "scope", "preferences", "acceptance", "authorization"):
        nonempty(intake.get(field), "intake." + field)
    if intake.get("open_questions") != []:
        raise ValueError("Open questions block compact creation/execution; remain in discovery")
    decisions = intake.get("decisions")
    if not isinstance(decisions, list):
        raise ValueError("Compact requires a decisions list, empty when no decisions were needed")
    for decision in decisions:
        if not isinstance(decision, dict) or decision.get("status") not in {"Confirmed", "Deferred"}:
            raise ValueError("Unconfirmed decision blocks compact execution")
        for field in ("decision", "source"):
            nonempty(decision.get(field), "decision " + field)
        if decision["status"] == "Deferred":
            nonempty(decision.get("outside_scope"), "evidence deferred decision is outside current scope")
    risk = data.get("risk")
    if not isinstance(risk, dict) or risk.get("level") != "light":
        raise ValueError("Compact supports only evidenced light documentation changes")
    exclusions = risk.get("exclusions")
    if not isinstance(exclusions, dict) or set(exclusions) != EXCLUSIONS or any(v is not False for v in exclusions.values()):
        raise ValueError("Compact risk is unknown or elevated; use standard discovery")
    nonempty(risk.get("rationale"), "risk evidence/rationale")
    for field in ("impact", "governance_review", "output_assessment"):
        nonempty(data.get(field), field)
    paths = data.get("paths")
    if not isinstance(paths, list) or not paths or not all(isinstance(p, str) for p in paths) or len(paths) != len(set(paths)):
        raise ValueError("Compact requires unique affected paths")
    for name in paths:
        path = safe_path(root, name)
        if (path.suffix.lower() not in {".md", ".txt", ".rst"}
                or path.name.lower() in {"agents.md", "claude.md", "skill.md", "security.md", "license", "license.md"}
                or any(part.startswith(".") or part.lower() in {"skills", "commands", "sdc-references"} for part in Path(name).parts)):
            raise ValueError("Compact permits prose documents only, not code, governance, skills, or policy: " + name)
        if path.exists():
            if not path.is_file() or path.stat().st_mode & 0o111:
                raise ValueError("Compact document must be a non-executable regular file: " + name)
            path.read_text(encoding="utf-8")
    governance = data.get("governance")
    if not isinstance(governance, list) or not all(isinstance(p, str) for p in governance):
        raise ValueError("Compact governance must list applicable source paths")
    for name in governance:
        if not safe_path(root, name).is_file():
            raise ValueError("Missing cited governing source: " + name)
    task = data.get("task")
    if not isinstance(task, dict):
        raise ValueError("Compact requires one coherent task")
    for field, pattern in (("id", r"T\d{3}"), ("scenario", r"SCN-\d+"), ("requirement", r"REQ-\d+"), ("acceptance", r"AC-\d+")):
        if not isinstance(task.get(field), str) or not re.fullmatch(pattern, task[field]):
            raise ValueError("Compact task requires traceable " + field)
    argv = task.get("verify")
    if not isinstance(argv, list) or not argv or not all(isinstance(v, str) and v and "\0" not in v for v in argv):
        raise ValueError("Compact task Verify must be a nonempty argv list")
    nonempty(task.get("expected"), "independent expected verification result")
    if "complete" in task and not isinstance(task["complete"], bool):
        raise ValueError("Compact task.complete must be boolean")
    if delivery:
        if task.get("complete") is not True:
            raise ValueError("Compact task is not complete")
        review = data.get("review")
        if not isinstance(review, dict) or review.get("spec") != "approved" or review.get("quality") != "approved":
            raise ValueError("Compact requires approved spec and quality review of the whole change")
        if review.get("behavior_neutral") is not True:
            raise ValueError("Independent review must confirm behavior-neutral scope")
        for field in ("reviewer", "evidence"):
            nonempty(review.get(field), "review " + field)
    return data


def load(root, directory):
    path = safe_path(root, (directory / "compact.json").relative_to(root).as_posix())
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or data.get("change_id") != directory.name:
        raise ValueError("Compact change identity mismatch")
    if any((directory / name).exists() for name in STANDARD_ARTIFACTS):
        raise ValueError("Mixed compact and standard artifacts; use explicit escalation")
    state_path = directory / "state.json"
    if state_path.exists():
        state = json.loads(safe_path(root, state_path.relative_to(root).as_posix()).read_text())
        if state.get("artifact_format") != "compact":
            raise ValueError("An existing standard change cannot silently become compact")
    return data


def contract(data, *, plan=False):
    value = copy.deepcopy(data)
    value.pop("review", None)
    if plan:
        value.get("task", {}).pop("complete", None)
    else:
        value.pop("task", None)
    return value


def snapshot(root, directory, *, plan=False):
    data = load(root, directory)
    read_baseline(root, directory, data)
    result = {"compact-contract": hashlib.sha256(json.dumps(contract(data, plan=plan), sort_keys=True).encode()).hexdigest()}
    for name in governing_sources(root, data):
        path = safe_path(root, name)
        result[name] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    return result


def governing_sources(root, data):
    from sdc_evidence import knowledge_dependencies, knowledge_references
    required = set(data.get("governance", []))
    values = [data]
    while values:
        value = values.pop()
        if isinstance(value, str):
            required.update(knowledge_references(value))
        elif isinstance(value, dict):
            values.extend(value.values())
        elif isinstance(value, list):
            values.extend(value)
    sources = {name: name in required for name in set(GOVERNANCE) | required}
    for name in data["paths"]:
        for parent in Path(name).parents:
            for filename in ("AGENTS.md", "CLAUDE.md"):
                sources.setdefault((parent / filename).as_posix(), False)
    pending = sorted(sources)
    visited = set()
    while pending:
        name = pending.pop()
        if name in visited:
            continue
        visited.add(name)
        path = safe_path(root, name)
        if not path.is_file():
            if sources[name]:
                raise ValueError("Cited governing source is missing: " + name)
            continue
        for reference, required_source in sorted(knowledge_dependencies(path.read_text()).items()):
            sources[reference] = sources.get(reference, False) or required_source
            if reference not in visited:
                pending.append(reference)
    for name, required_source in sources.items():
        if not safe_path(root, name).is_file() and required_source:
            raise ValueError("Cited governing source is missing: " + name)
    return dict(sorted(sources.items()))


def read_baseline(root, directory, data):
    binding = data.get("baseline")
    if not isinstance(binding, dict) or binding.get("path") != "evidence/baseline/source.json":
        raise ValueError("Compact requires the captured source baseline")
    baseline_path = safe_path(root, (directory / binding["path"]).relative_to(root).as_posix())
    raw = baseline_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != binding.get("sha256"):
        raise ValueError("Compact source baseline is missing or changed")
    baseline = json.loads(raw)
    if not isinstance(baseline, dict):
        raise ValueError("Invalid source baseline")
    return baseline


def check_scope(root, directory, data):
    from sdc_evidence import source_snapshot
    baseline = read_baseline(root, directory, data)
    current = source_snapshot(root, extra_paths=data["paths"])
    changed = {name for name in set(baseline) | set(current) if baseline.get(name) != current.get(name)}
    unexpected = changed - set(data["paths"])
    if unexpected:
        raise ValueError("Compact scope expanded; stop and escalate: " + ", ".join(sorted(unexpected)))


def validate(root, directory, *, delivery=False):
    data = validate_record(load(root, directory), root, delivery=delivery)
    check_scope(root, directory, data)
    return data


def create(root, change_id, record):
    from sdc_evidence import source_snapshot
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", change_id):
        raise ValueError("Invalid compact change id")
    directory = safe_path(root, ".sdc/changes/active/" + change_id)
    if directory.exists():
        raise ValueError("Change already exists; do not replace or downgrade it")
    data = validate_record(copy.deepcopy(record), root)
    baseline = (json.dumps(source_snapshot(root, extra_paths=data["paths"]), sort_keys=True, indent=2) + "\n").encode("utf-8")
    data.update(change_id=change_id, baseline={"path": "evidence/baseline/source.json",
                                             "sha256": hashlib.sha256(baseline).hexdigest()})
    data["task"]["complete"] = False
    data["review"] = {"spec": "pending", "quality": "pending"}
    governing_sources(root, data)
    ignore = safe_path(root, ".sdc/.gitignore")
    ignore_text = ignore.read_text() if ignore.exists() else ""
    directory.mkdir(parents=True)
    if "/runtime/" not in ignore_text.splitlines():
        ignore.write_text(ignore_text + ("\n" if ignore_text and not ignore_text.endswith("\n") else "") + "/runtime/\n")
    baseline_path = directory / data["baseline"]["path"]
    baseline_path.parent.mkdir(parents=True)
    baseline_path.write_bytes(baseline)
    write_json(directory / "compact.json", data)
    write_json(directory / "state.json", {
        "schema": "sdc.change-state/v1", "change_id": change_id, "state": "discovery",
        "artifact_format": "compact", "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": {"kind": "change-stage", "paths": ["compact.json"]},
    })
    return directory


def write_json(path, data):
    import os
    import tempfile
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")
        temporary = handle.name
    os.replace(temporary, path)
