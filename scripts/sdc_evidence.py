"""Snapshot and execution primitives shared by the SDC runtime.

Receipts are local provenance, not cryptographic attestations of reviewer identity.
No command output or environment variable values are persisted here.
"""

import hashlib
import json
import os
import re
import shlex
import signal
import stat
import subprocess
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import unquote


class UnsupportedSubmoduleError(ValueError):
    """Gitlink contents cannot be bound by the local source snapshot."""


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def digest_json(value):
    return digest_bytes(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def task_contract(text):
    text = re.sub(r"(?m)^(\s*- )\[[xX ]\](\s+T\d+)", r"\1[ ]\2", text)
    return re.sub(r"(?mi)^[ \t]*-[ \t]*(?:Review|Evidence):[^\n]*", "", text)


LEGACY_OPTIONAL_COMPANY_POLICY = (
    "- \u5982\u679c `.sdc/standards/company/README.md` \u5b58\u5728\u4e14\u5f53\u524d\u4efb\u52a1\u6d89\u53ca\u4ee3\u7801\u751f\u6210\u3001\u67b6\u6784\u3001\u63a5\u53e3\u3001\u6570\u636e\u3001\u4e8b\u52a1\u3001\u6d4b\u8bd5\u3001\u5b89\u5168\u6216\u516c\u53f8\u7ea6\u5b9a\uff0c\u5148\u8bfb\u8be5\u7d22\u5f15\uff0c\u518d\u53ea\u8bfb\u53d6\u76f8\u5173\u516c\u53f8\u89c4\u8303\u6587\u4ef6"
)


def knowledge_references(text):
    references = set()
    covered = []
    patterns = (
        (r"`([^`\n]+)`", False),
        (r'''\]\((<[^>\n]+>|[^\s()]+)(?:[ \t]+(?:"[^"\n]*"|'[^'\n]*'|\([^()\n]*\)))?[ \t]*\)''', True),
        (r"<([^>\n]+)>", True),
    )
    for pattern, is_url in patterns:
        for match in re.finditer(pattern, text):
            if any(start <= match.start() < end for start, end in covered):
                continue
            path = match.group(1).strip("<>").split("#", 1)[0]
            if is_url:
                path = unquote(path, errors="strict")
            if path.startswith((".sdc/knowledge/", ".sdc/standards/")):
                covered.append(match.span())
                if not path.endswith("/"):
                    references.add(path)
    for match in re.finditer(r"\.sdc/(?:knowledge|standards)/[^\s`<>|()\[\]]*", text):
        if any(start <= match.start() < end for start, end in covered):
            continue
        path = match.group().split("#", 1)[0].rstrip(".,;")
        if path.endswith("/"):
            continue
        if Path(path).suffix.lower() not in {".md", ".markdown", ".txt", ".json", ".yaml", ".yml", ".toml", ".xml", ".csv"}:
            raise ValueError("Unsupported knowledge citation; use a complete backtick path or Markdown link: " + path)
        references.add(path)
    for path in references:
        if ".." in Path(path).parts or "\\" in path or "\0" in path:
            raise ValueError("Knowledge citations must stay inside their source root")
    return references


def knowledge_dependencies(text):
    """Classify only the exact bundled conditional; all other citations are required."""
    dependencies = {}
    required_lines = []
    for line in text.splitlines(keepends=True):
        if line.rstrip("\r\n") == LEGACY_OPTIONAL_COMPANY_POLICY:
            dependencies[".sdc/standards/company/README.md"] = False
            required_lines.append("\n")
        else:
            required_lines.append(line)
    dependencies.update(dict.fromkeys(knowledge_references("".join(required_lines)), True))
    return dependencies


@contextmanager
def change_lock(root, change_id):
    """Serialize evidence mutation/revision/archive; OS releases locks on process exit."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", change_id):
        raise ValueError("Invalid change id for delivery lock")
    path = root / ".sdc" / "runtime" / change_id / "delivery.lock"
    current = root
    for part in path.relative_to(root).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Delivery lock may not traverse a symlink")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as handle:
        if os.name == "posix":
            import fcntl
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise ValueError("Change is busy with validation, revision, or archival; retry after it finishes") from exc
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)
        elif os.name == "nt":
            import msvcrt
            if handle.tell() == 0:
                handle.write(b"0")
                handle.flush()
            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise ValueError("Change is busy with validation, revision, or archival") from exc
            try:
                yield
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            raise ValueError("This platform has no supported delivery lock")


def input_snapshot(root, directory, *, plan=False):
    from sdc_compact import is_compact, snapshot
    if is_compact(directory):
        return snapshot(root, directory, plan=plan)
    names = {".sdc/constitution.md", ".sdc/common-ground.md", ".sdc/expert-routing.md", ".sdc/knowledge/index.md"}
    artifacts = ["discovery.md", "spec.md"]
    if plan:
        artifacts += ["impact.md", "design.md", "tasks.md", "context-pack.md"]
    for name in artifacts:
        names.add((directory / name).relative_to(root).as_posix())
    # Include only explicitly cited knowledge/standards; an index is routing, not a full corpus load.
    artifact_names = {(directory / name).relative_to(root).as_posix() for name in artifacts}
    pending = sorted(names)
    visited = set()
    required_refs = set()
    while pending:
        name = pending.pop()
        if name in visited:
            continue
        visited.add(name)
        path = root / name
        current = root
        for part in Path(name).parts:
            current = current / part
            if current.is_symlink():
                raise ValueError(f"Snapshot input must not be a symlink: {name}")
        if not path.is_file() or path.is_symlink():
            continue
        text = path.read_text(errors="replace")
        dependencies = (dict.fromkeys(knowledge_references(text), True) if name in artifact_names
                        else knowledge_dependencies(text))
        for reference, required in sorted(dependencies.items()):
            names.add(reference)
            if required:
                required_refs.add(reference)
            if reference not in visited:
                pending.append(reference)
    result = {}
    for name in sorted(names):
        path = root / name
        current = root
        for part in Path(name).parts:
            current = current / part
            if current.is_symlink():
                raise ValueError(f"Snapshot input must not be a symlink: {name}")
        value = path.read_bytes() if path.is_file() else None
        if value is None and name in required_refs:
            raise ValueError(f"Cited knowledge/standard source is missing: {name}")
        if value is not None and path == directory / "tasks.md":
            value = task_contract(value.decode()).encode()
        result[name] = digest_bytes(value) if value is not None else None
    return result


def source_snapshot(root, *, extra_paths=()):
    ignored_dirs = {".sdc", ".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache"}
    tracked = set()
    git = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                         cwd=root, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if git.returncode == 0:
        index = subprocess.run(["git", "ls-files", "--stage", "-z"],
                               cwd=root, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if index.returncode:
            raise ValueError("Cannot inspect Git index for unsupported submodules")
        # Check index modes even when a submodule is absent or under an excluded directory.
        for entry in index.stdout.split(b"\0"):
            metadata, _, path = entry.partition(b"\t")
            if path:
                tracked.add(os.fsdecode(path))
            if metadata.split(b" ", 1)[0] == b"160000":
                raise UnsupportedSubmoduleError(
                    "Source snapshots do not support Git submodules (gitlink): " + os.fsdecode(path))
        names = {os.fsdecode(name) for name in git.stdout.split(b"\0") if name}
    else:
        names = set()
        for base, dirs, files in os.walk(root, followlinks=False):
            for name in dirs:
                path = Path(base) / name
                if path.is_symlink():
                    names.add(path.relative_to(root).as_posix())
            dirs[:] = sorted(name for name in dirs if name not in ignored_dirs)
            for name in files:
                names.add((Path(base) / name).relative_to(root).as_posix())
    explicit = set(extra_paths)
    names.update(explicit)
    result = {}
    for name in sorted(names):
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            if name in explicit:
                raise ValueError("Explicit source paths must stay inside the repository")
            continue
        # SDC/Git bookkeeping has separate snapshots; tracked product files do not
        # become disposable merely because an ancestor resembles a cache directory.
        if relative.parts[0] in {".sdc", ".git"}:
            continue
        if (name not in explicit and name not in tracked
                and not (root / relative).is_symlink()
                and any(part in ignored_dirs for part in relative.parts)):
            continue
        path = root / relative
        linked_parent = None
        parent = root
        for part in relative.parts[:-1]:
            parent /= part
            if parent.is_symlink():
                linked_parent = parent
                break
        if linked_parent is not None:
            # Bind the first link's routing without probing any of its descendants.
            result[name] = digest_bytes(json.dumps({
                "symlink_parent": linked_parent.relative_to(root).as_posix(),
                "target": os.readlink(linked_parent),
            }, sort_keys=True).encode())
            continue
        if path.is_symlink():
            result[name] = digest_bytes(os.fsencode(os.readlink(path)))
        elif path.is_file():
            mode = stat.S_IMODE(path.stat().st_mode)
            result[name] = digest_bytes(str(mode).encode() + b"\0" + path.read_bytes())
        elif not path.exists():
            result[name] = None
    return result


def change_support_snapshot(root, directory):
    # Governance/progress have dedicated snapshots. Extra scripts and fixtures do not.
    artifacts = {
        "discovery.md", "spec.md", "impact.md", "design.md", "tasks.md", "context-pack.md",
        "notes.md", "proposal.md", "knowledge-candidates.md", "state.json",
        "apply-context.jsonl", "check-context.jsonl", "compact.json", "findings.json",
    }
    result = {}
    pending = [directory]
    while pending:
        folder = pending.pop()
        for path in sorted(folder.iterdir()):
            if folder == directory and path.name in artifacts | {"evidence", "revisions"}:
                continue
            if path.name in {"__pycache__", ".pytest_cache", ".mypy_cache"}:
                continue
            if path.is_symlink():
                raise ValueError("Change support files must not traverse symlinks: " + path.relative_to(root).as_posix())
            if path.is_dir():
                pending.append(path)
            elif path.is_file():
                mode = stat.S_IMODE(path.stat().st_mode)
                result[path.relative_to(root).as_posix()] = digest_bytes(str(mode).encode() + b"\0" + path.read_bytes())
    return result


def verification_snapshot(root, directory):
    return {"inputs": input_snapshot(root, directory, plan=True), "sources": change_source_snapshot(root, directory),
            "change_support": change_support_snapshot(root, directory)}


def change_source_snapshot(root, directory):
    from sdc_compact import is_compact, load
    paths = load(root, directory)["paths"] if is_compact(directory) else ()
    return source_snapshot(root, extra_paths=paths)


def review_snapshot(root, directory):
    from sdc_compact import is_compact
    result = verification_snapshot(root, directory)
    names = ("compact.json",) if is_compact(directory) else ("tasks.md", "notes.md")
    result["review_artifacts"] = {
        name: digest_bytes((directory / name).read_bytes())
        for name in names
    }
    findings = directory / "findings.json"
    if findings.is_symlink():
        raise ValueError("Finding evidence must not be a symlink")
    if findings.is_file():
        result["review_artifacts"]["findings.json"] = digest_bytes(findings.read_bytes())
    if is_compact(directory):
        notes = directory / "notes.md"
        if notes.is_symlink():
            raise ValueError("Compact notes must not be a symlink")
        result["review_artifacts"]["notes.md"] = digest_bytes(notes.read_bytes()) if notes.is_file() else None
    return result


def task_verifications(directory):
    from sdc_compact import is_compact, load
    if is_compact(directory):
        root = directory.parents[3]
        task = load(root, directory)["task"]
        return {task["id"]: {"complete": task.get("complete") is True, "argv": task["verify"]}}
    lines = (directory / "tasks.md").read_text().splitlines()
    checkbox_indexes = [
        index for index, line in enumerate(lines)
        if re.match(r"^\s*-\s*\[[ xX]\]\s+", line)
    ]
    # Match validate_task_trace's stripped headers and all-checkbox block boundaries.
    task_pattern = re.compile(
        r"- \[([ xX])\] (T\d{3}) \[REQ-[^\]]+\] \[AC-[^\]]+\] "
        r"\[Phase [^\]]+\] \[Size: [SM]\][ \t]+\S.*"
    )
    tasks = {}
    for offset, position in enumerate(checkbox_indexes):
        match = task_pattern.fullmatch(lines[position].strip())
        if not match:
            raise ValueError("Invalid task checkbox: " + lines[position].strip())
        end = checkbox_indexes[offset + 1] if offset + 1 < len(checkbox_indexes) else len(lines)
        block = "\n".join(lines[position:end])
        verifies = re.findall(r"(?mi)^[ \t]*-[ \t]*Verify:[ \t]*(.*)$", block)
        if len(verifies) != 1 or not verifies[0].strip() or match.group(2) in tasks:
            raise ValueError("Every unique task needs exactly one nonempty Verify command")
        argv = shlex.split(verifies[0].strip().strip("`"))
        if not argv:
            raise ValueError("Every task needs a nonempty Verify command argv")
        tasks[match.group(2)] = {
            "complete": match.group(1).lower() == "x",
            "argv": argv,
        }
    if not tasks:
        raise ValueError("No verifiable tasks found")
    return tasks


def execute(argv, root, timeout):
    started = time.monotonic()
    timed_out = False
    with tempfile.TemporaryFile() as output:
        try:
            process = subprocess.Popen(argv, cwd=root, stdout=output, stderr=subprocess.STDOUT,
                                       stdin=subprocess.DEVNULL, start_new_session=(os.name == "posix"))
        except OSError as exc:
            return {"status": "failed", "exit_code": 127, "duration_seconds": round(time.monotonic() - started, 3),
                    "output_sha256": None, "error": type(exc).__name__}
        try:
            try:
                code = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                process.kill()
                code = process.wait()
        finally:
            if os.name == "posix":
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            elif process.poll() is None:
                process.kill()
            process.wait()
        # Streaming hash avoids loading an unbounded test log into model or process memory.
        output.seek(0)
        digest = hashlib.sha256()
        for block in iter(lambda: output.read(65536), b""):
            digest.update(block)
    return {"status": "timeout" if timed_out else "passed" if code == 0 else "failed",
            "exit_code": code, "duration_seconds": round(time.monotonic() - started, 3),
            "output_sha256": digest.hexdigest()}
