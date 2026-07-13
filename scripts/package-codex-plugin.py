#!/usr/bin/env python3
"""Build a deterministic Codex plugin archive from the generated SDC layout."""

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_ENTRIES = (
    ".codex-plugin",
    "skills",
    "sdc-references",
    "scripts/sdc-task-brief.py",
    "scripts/sdc-review-package.py",
    "sdc-cli.py",
    "README.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "PRIVACY.md",
    "LICENSE",
)


def run(args, *, cwd=ROOT, env=None):
    result = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        raise SystemExit(result.stdout.strip() or f"Command failed: {' '.join(args)}")
    return result.stdout


def ensure_clean(allow_dirty):
    if allow_dirty:
        return
    status_output = run(["git", "status", "--porcelain"])
    if status_output.strip():
        raise SystemExit("Refusing to package a dirty worktree. Commit/stash changes or pass --allow-dirty for local verification.")


def stage_payload(plugin_root, stage):
    for relative_value in PAYLOAD_ENTRIES:
        relative = Path(relative_value)
        source = plugin_root / relative
        target = stage / relative
        if not source.exists():
            raise SystemExit(f"Generated Codex plugin is missing required payload entry: {relative_value}")
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(
                source,
                target,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "*.pyd"),
            )
        else:
            shutil.copy2(source, target)


def verify_payload(stage):
    if not (stage / ".codex-plugin" / "plugin.json").exists():
        raise SystemExit("Codex portal payload is missing .codex-plugin/plugin.json")
    if not (stage / "skills" / "sdc-core" / "SKILL.md").exists():
        raise SystemExit("Codex portal payload is missing public workflow skills")

    skill_dirs = [path for path in (stage / "skills").iterdir() if path.is_dir()]
    missing_skills = [path.name for path in skill_dirs if not (path / "SKILL.md").exists()]
    if missing_skills:
        raise SystemExit(f"Codex portal payload has skill directories without SKILL.md: {', '.join(missing_skills)}")

    forbidden = [
        path.relative_to(stage).as_posix()
        for path in stage.rglob("*")
        if path.is_file()
        and (
            "__pycache__" in path.parts
            or path.suffix in {".pyc", ".pyo", ".pyd"}
            or path.relative_to(stage).parts[0] in {".agents", ".claude", ".claude-plugin", "commands", "bin", "docs", "evals"}
        )
    ]
    if forbidden:
        raise SystemExit(f"Codex portal payload contains source-only files: {', '.join(forbidden)}")


def zip_tree(source, output):
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(source.rglob("*"), key=lambda item: item.as_posix()):
            if not path.is_file():
                continue
            relative = path.relative_to(source)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = stat.S_IMODE(path.stat().st_mode)
            info.external_attr = (mode & 0xFFFF) << 16
            info.create_system = 3
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Archive output path")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow local verification from a dirty worktree")
    args = parser.parse_args()

    package = json.loads((ROOT / "package.json").read_text())
    version = package["version"]
    output = args.output or ROOT / "dist" / f"sdc-codex-plugin-{version}.zip"
    output = output.resolve()

    ensure_clean(args.allow_dirty)
    run(["npm", "run", "audit"])

    with tempfile.TemporaryDirectory(prefix="sdc-codex-package-") as temp_value:
        temp = Path(temp_value)
        env = os.environ.copy()
        env["HOME"] = str(temp)
        env["USERPROFILE"] = str(temp)
        run(["node", "bin/install.js"], env=env)
        plugin_root = temp / ".codex" / "local-marketplaces" / "sdc-local" / "plugins" / "sdc"
        if not (plugin_root / ".codex-plugin" / "plugin.json").exists():
            raise SystemExit("Generated Codex plugin is missing .codex-plugin/plugin.json")
        if not (plugin_root / "skills" / "sdc-core" / "SKILL.md").exists():
            raise SystemExit("Generated Codex plugin is missing public workflow skills")
        stage = temp / "payload"
        stage.mkdir()
        stage_payload(plugin_root, stage)
        verify_payload(stage)
        zip_tree(stage, output)

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    checksum = output.with_suffix(output.suffix + ".sha256")
    checksum.write_text(f"{digest}  {output.name}\n")
    print(output)
    print(checksum)


if __name__ == "__main__":
    main()
