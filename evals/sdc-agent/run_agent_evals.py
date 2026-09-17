#!/usr/bin/env python3
"""Run bounded real-CLI trials. Python standard library only; no fake provider."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import selectors
import shutil
import signal
import subprocess
import sys
import tempfile
import time

from agent_adapters import agent_command, probe_agent
from grading import aggregate_outcome, check, classify_execution, parse_transcript, structural_checks
from scenarios import SAFETY, SCENARIOS, advance_revision, seed_project


SOURCE_FILES = ("sdc-cli.py", "scripts/sdc-runtime-context.py", "scripts/sdc-task-brief.py", "scripts/sdc-review-package.py", "scripts/sdc_evidence.py")
SOURCE_DIRS = ("commands", "sdc-references")
MAX_SOURCE_BYTES = 10_000_000


def dump_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_manifest(root):
    result = {}
    total = 0
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            result[relative] = "SYMLINK"
        elif path.is_file():
            total += path.stat().st_size
            if len(result) >= 10_000 or total > 25_000_000:
                raise ValueError("Project snapshot exceeds bounded file/byte limit")
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def install_source(source, project):
    if source is None:
        return {"kind": "no-sdc", "files": {}, "sha256": None}
    source = Path(source).resolve(strict=True)
    required = [source / "sdc-cli.py", source / "commands/sdc.md"]
    if not all(path.is_file() for path in required):
        raise ValueError("Source root must contain sdc-cli.py and commands/sdc.md")
    selected = [source / name for name in SOURCE_FILES if (source / name).exists()]
    for name in SOURCE_DIRS:
        directory = source / name
        if directory.is_symlink():
            raise ValueError("Symlinked source directory: " + name)
        if directory.exists():
            selected += list(directory.rglob("*"))
    total = 0
    manifest = {}
    for path in sorted(selected):
        relative = path.relative_to(source)
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != source and source in parent.parents):
            raise ValueError("Symlinks are not allowed in selected source: " + str(relative))
        if path.is_dir() or "__pycache__" in path.parts:
            continue
        if not path.is_file():
            raise ValueError("Non-regular source file: " + str(relative))
        # No arbitrary bundled binary/config payloads, hooks, or plugin manifests.
        if path.suffix not in {".py", ".md", ".yaml", ".yml", ".json", ".txt"}:
            continue
        total += path.stat().st_size
        if total > MAX_SOURCE_BYTES or len(manifest) >= 2000:
            raise ValueError("Source snapshot exceeds bounded file/byte limit")
        target = project / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        manifest[relative.as_posix()] = hashlib.sha256(target.read_bytes()).hexdigest()
    return {"kind": "explicit-source", "source_root": str(source), "files": manifest,
            "sha256": hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()}


def isolated_env(root, parent, auth_mode):
    home = root / "home"
    for path in (home, home / ".codex", home / ".claude", root / "tmp", root / "cache", root / "config"):
        path.mkdir(parents=True, exist_ok=True)
    env = {key: parent[key] for key in ("PATH", "LANG", "LC_ALL", "SYSTEMROOT") if key in parent}
    env.update({"HOME": str(home), "CODEX_HOME": str(home / ".codex"), "CLAUDE_CONFIG_DIR": str(home / ".claude"),
                "TMPDIR": str(root / "tmp"), "XDG_CACHE_HOME": str(root / "cache"), "XDG_CONFIG_HOME": str(root / "config"),
                "PYTHONDONTWRITEBYTECODE": "1", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1", "DISABLE_AUTOUPDATER": "1",
                "CLAUDE_CODE_MAX_RETRIES": "0", "NO_COLOR": "1"})
    if auth_mode == "host":
        original_home = Path(parent.get("HOME", str(Path.home())))
        env["CODEX_HOME"] = parent.get("CODEX_HOME", str(original_home / ".codex"))
        env["CLAUDE_CONFIG_DIR"] = parent.get("CLAUDE_CONFIG_DIR", str(original_home / ".claude"))
    return env


def kill_group(process):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait(timeout=3)


def run_process(command, cwd, env, prompt, transcript, *, timeout, max_output_bytes, stop_on_agent_error=False):
    start = time.monotonic()
    stdout_path = Path(str(transcript) + ".stdout.jsonl")
    stderr_path = Path(str(transcript) + ".stderr.txt")
    result = {"command": command, "exit_code": None, "status": "launch_error", "attempts": 1,
              "timed_out": False, "elapsed_seconds": 0, "stdout_ref": stdout_path.name, "stderr_ref": stderr_path.name}
    process = None
    total = 0
    event_buffer = b""
    with tempfile.TemporaryFile() as stdin, stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr, selectors.DefaultSelector() as selector:
        stdin.write(prompt.encode())
        stdin.seek(0)
        try:
            process = subprocess.Popen(command, cwd=cwd, env=env, stdin=stdin, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, start_new_session=True)
            result["pid"] = process.pid
            for stream, target in ((process.stdout, stdout), (process.stderr, stderr)):
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, selectors.EVENT_READ, target)
            result["status"] = "completed"
            while selector.get_map():
                if time.monotonic() - start >= timeout:
                    result.update(status="timeout", timed_out=True)
                    break
                for key, _ in selector.select(timeout=min(0.05, max(0, timeout - (time.monotonic() - start)))):
                    chunk = os.read(key.fileobj.fileno(), 65536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    kept = chunk[:max(0, max_output_bytes - total)]
                    key.data.write(kept)
                    key.data.flush()
                    total += len(chunk)
                    if total > max_output_bytes:
                        result["status"] = "output_limit"
                        break
                    if stop_on_agent_error and key.data is stdout:
                        event_buffer += kept
                        lines = event_buffer.split(b"\n")
                        event_buffer = lines.pop()
                        for line in lines:
                            try:
                                event = json.loads(line)
                            except (ValueError, UnicodeError):
                                continue
                            if isinstance(event, dict) and event.get("type") == "error":
                                message = str(event.get("message", ""))
                                result["status"] = "client_retry_detected" if "reconnect" in message.lower() or "retry" in message.lower() else "model_error"
                                result["stream_error"] = message[:1000]
                                break
                if result["status"] != "completed":
                    break
            if result["status"] == "completed":
                try:
                    process.wait(timeout=max(0.001, timeout - (time.monotonic() - start)))
                except subprocess.TimeoutExpired:
                    result.update(status="timeout", timed_out=True)
        except OSError as exc:
            result.update(status="launch_error", error=type(exc).__name__ + ": " + str(exc))
        except KeyboardInterrupt:
            result["status"] = "interrupted"
        finally:
            if process is not None:
                # Also terminate descendants after an apparently clean parent exit.
                kill_group(process)
                result["exit_code"] = process.returncode
                process.stdout.close()
                process.stderr.close()
            result["elapsed_seconds"] = round(time.monotonic() - start, 4)
            result["output_bytes_observed"] = total
    if result["status"] == "completed" and result["exit_code"] != 0:
        result["status"] = "process_failed"
    return result


def export_project(project, destination):
    manifest = file_manifest(project)
    destination.mkdir()
    for name, digest in manifest.items():
        if digest == "SYMLINK":
            continue
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(project / name, target)
    return manifest


def run_trial(agent, source, label, scenario, index, args, output):
    trial_dir = output / (label + "--" + scenario + "--" + str(index))
    trial_dir.mkdir()
    result = {"schema": "sdc.agent-trial/v1", "evidence_kind": "real-cli", "arm": label, "scenario": scenario,
              "trial": index, "agent": agent, "requested_model": args.model, "phases": [],
              "budgets": {"wall_seconds": args.timeout, "output_bytes": args.max_output_bytes, "harness_retries": 0,
                          "token_limit": None, "cost_limit_usd": None},
              "semantic": {"status": "unknown", "method": "not model-judged", "rubric": SCENARIOS[scenario]["semantic_rubric"], "judgments": []},
              "objective_outcome": "unknown", "outcome": "unknown", "structural_checks": []}
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="sdc-agent-project-") as temp:
        root = Path(temp).resolve()
        project = root / "project"
        project.mkdir()
        result["temporary_project"] = str(project)
        env = isolated_env(root, os.environ, args.auth_mode)
        result["isolation"] = {
            "auth_mode": args.auth_mode, "temporary_home": True, "native_autoload_disabled": True,
            "plugin_hooks_installed": False, "source_delivery": "explicit prompt and local files",
            "shell": "workspace-write sandbox, network disabled" if agent == "codex" else "disabled; restricted file tools only",
            "limits": ["Not a container; OS policy, CLI defaults, and server-side context may apply.",
                       "Host-auth mode exposes CLI auth/state directories to the CLI; no credentials copied or read by harness.",
                       "Streamed retry/error events abort the process; unreported CLI internal retries cannot be prevented or counted.",
                       "Token and dollar ceilings are not enforced; wall-time/output limits are hard local bounds."]}
        try:
            result["source"] = install_source(source, project)
            seed_project(project, scenario)
            before = file_manifest(project)
            dump_json(trial_dir / "before.json", before)
            fixture = {key: value for key, value in before.items() if key not in result["source"]["files"]}
            result["fixture_sha256"] = hashlib.sha256(json.dumps(fixture, sort_keys=True).encode()).hexdigest()
            preflight = probe_agent(agent, env, project)
            result["preflight"] = preflight
            if preflight.get("ready") is not True:
                result["status"] = "unavailable"
                result["execution"] = {"status": "unavailable", "failure_category": "preflight"}
            else:
                deadline = time.monotonic() + args.timeout
                remaining_output = args.max_output_bytes
                for number, task in enumerate(SCENARIOS[scenario]["prompts"], 1):
                    if number > 1:
                        advance_revision(project)
                    prompt = SAFETY
                    if source is not None:
                        prompt += "\nUse only the selected SDC source in this project. The local commands/sdc.md is injected below. Read the applicable local commands/<stage>.md and referenced sdc-references/ files. Interpret slash-command names as those local workflow files, not installed plugins or generated skill copies. Use python3 sdc-cli.py and scripts/ helpers locally where needed.\n\n<selected-sdc-entry>\n"
                        prompt += (project / "commands/sdc.md").read_text(encoding="utf-8") + "\n</selected-sdc-entry>\n"
                    prompt += "\nUser task:\n" + task + "\n"
                    (trial_dir / ("phase-" + str(number) + ".prompt.txt")).write_text(prompt)
                    process = run_process(agent_command(agent, preflight["executable"], args.model), project, env, prompt,
                                          trial_dir / ("phase-" + str(number)), timeout=max(0.001, deadline - time.monotonic()),
                                          max_output_bytes=max(0, remaining_output), stop_on_agent_error=True)
                    remaining_output -= process["output_bytes_observed"]
                    telemetry = parse_transcript(agent, (trial_dir / process["stdout_ref"]).read_text(errors="replace"))
                    execution = classify_execution(process, telemetry, (trial_dir / process["stderr_ref"]).read_text(errors="replace"))
                    phase = {"number": number, "process": process, "telemetry": telemetry, "execution": execution}
                    if scenario == "revision-invalidation":
                        phase["project_ref"] = "phase-" + str(number) + "-project"
                        export_project(project, trial_dir / phase["project_ref"])
                    result["phases"].append(phase)
                    dump_json(trial_dir / "result.json", result)
                    if execution["status"] != "completed":
                        break
                result["execution"] = result["phases"][-1]["execution"]
                result["status"] = result["execution"]["status"]
            result["structural_checks"] = structural_checks(scenario, project, before, result["phases"])
            after = export_project(project, trial_dir / "project")
            modified_source = [name for name, digest in result["source"]["files"].items() if after.get(name) != digest]
            result["structural_checks"].append(check("selected_source_unchanged", "fail" if modified_source else "pass", modified_source))
            dump_json(trial_dir / "after.json", after)
            if result["phases"]:
                model_status = result["phases"][-1]["telemetry"]["model_status"]
                result["objective_outcome"] = aggregate_outcome(result["status"], model_status, result["structural_checks"])
                result["outcome"] = "fail" if result["objective_outcome"] == "fail" else "unknown"
        except (OSError, ValueError, RuntimeError) as exc:
            result.update(status="harness_error", error=type(exc).__name__ + ": " + str(exc), objective_outcome="unknown", outcome="unknown")
        finally:
            result["elapsed_seconds"] = round(time.monotonic() - start, 4)
            result["usage"] = {}
            for key in ("input_tokens", "cached_input_tokens", "output_tokens", "cost_usd"):
                values = [phase["telemetry"]["usage"][key] for phase in result["phases"]]
                result["usage"][key] = sum(values) if values and all(value is not None for value in values) else None
            result["project_removed_after_trial"] = True
            dump_json(trial_dir / "result.json", result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=("codex", "claude"), default="codex")
    parser.add_argument("--model", default="default", help="CLI default unless explicitly supplied; shared across all arms")
    parser.add_argument("--source", action="append", default=[], metavar="LABEL=ROOT", help="Repeat for current/previous source roots")
    parser.add_argument("--baseline", action="store_true", help="Include no-SDC arm (also default when no source is supplied)")
    parser.add_argument("--scenario", action="append", choices=sorted(SCENARIOS), help="Repeat; defaults to all six")
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=120, help="Total model wall seconds per trial, shared by revision phases")
    parser.add_argument("--max-output-bytes", type=int, default=2_000_000)
    parser.add_argument("--max-total-trials", type=int, default=24)
    parser.add_argument("--auth-mode", choices=("isolated", "host"), default="isolated", help="host explicitly reuses CLI auth/state directories, not settings")
    parser.add_argument("--output", type=Path, help="New artifact directory, outside fixture projects; default new system temp directory")
    parser.add_argument("--doctor", action="store_true", help="Only inspect installed CLIs/auth using normal status commands; no model calls")
    parser.add_argument("--list", action="store_true", help="List scenarios without probing CLIs")
    args = parser.parse_args(argv)
    if args.list:
        print("\n".join(SCENARIOS))
        return 0
    if not (0 < args.timeout <= 1800 and 0 < args.trials <= 100 and 0 < args.max_output_bytes <= 20_000_000 and 0 < args.max_total_trials <= 1000):
        parser.error("Budgets must be positive and within timeout<=1800s, trials<=100, bytes<=20000000, total<=1000")
    if os.name != "posix":
        parser.error("POSIX process groups are required for bounded process cleanup")
    if args.doctor:
        with tempfile.TemporaryDirectory(prefix="sdc-agent-doctor-") as temp:
            root = Path(temp).resolve()
            env = isolated_env(root, os.environ, args.auth_mode)
            print(json.dumps([probe_agent(agent, env, root) for agent in ("codex", "claude")], indent=2))
        return 0
    arms = [("baseline", None)] if args.baseline or not args.source else []
    for value in args.source:
        label, separator, path = value.partition("=")
        if not separator or not label or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in label):
            parser.error("--source requires a safe LABEL=/absolute/source/root")
        if label in {name for name, _ in arms}:
            parser.error("Duplicate arm label: " + label)
        arms.append((label, Path(path).expanduser().resolve()))
    selected = list(dict.fromkeys(args.scenario or list(SCENARIOS)))
    total = len(arms) * len(selected) * args.trials
    if total > args.max_total_trials:
        parser.error("Matrix exceeds --max-total-trials; explicitly raise the bound or reduce the matrix")
    output = args.output.expanduser().resolve() if args.output else Path(tempfile.mkdtemp(prefix="sdc-agent-results-")).resolve()
    if args.output:
        output.mkdir(parents=True, exist_ok=False)
    run = {"schema": "sdc.agent-run/v1", "started_at": datetime.now(timezone.utc).isoformat(),
           "agent": args.agent, "requested_model": args.model, "trial_count": total, "scenario_order": selected,
           "trials_per_arm": args.trials, "auth_mode": args.auth_mode, "results": [],
           "comparison_limits": "Fixed-order, unpaired random seeds; compare arms within one CLI/model only. Default models can drift. No broad improvement inference from smoke trials."}
    dump_json(output / "run.json", run)
    # Freeze each supplied root once so later trials cannot silently pick up edits.
    frozen = []
    for label, source in arms:
        if source is None:
            frozen.append((label, None))
            continue
        destination = output / ("source-" + label)
        destination.mkdir()
        try:
            manifest = install_source(source, destination)
        except (OSError, ValueError) as exc:
            run["setup_error"] = str(exc)
            dump_json(output / "run.json", run)
            print("Source setup failed; artifacts: " + str(output), file=sys.stderr)
            return 1
        dump_json(output / ("source-" + label + ".json"), manifest)
        frozen.append((label, destination))
    for scenario in selected:
        for index in range(1, args.trials + 1):
            for label, source in frozen:
                result = run_trial(args.agent, source, label, scenario, index, args, output)
                reference = label + "--" + scenario + "--" + str(index) + "/result.json"
                run["results"].append({"ref": reference, "status": result["status"], "objective_outcome": result["objective_outcome"], "outcome": result["outcome"]})
                dump_json(output / "run.json", run)
                print(label + " " + scenario + " trial=" + str(index) + " status=" + result["status"] + " objective=" + result["objective_outcome"] + " semantic=unknown", flush=True)
                if any(phase["process"]["status"] == "interrupted" for phase in result["phases"]):
                    print("Interrupted; remaining matrix not run. Artifacts: " + str(output))
                    return 130
    print("Artifacts: " + str(output))
    return 1 if any(item["outcome"] == "fail" for item in run["results"]) else 2


if __name__ == "__main__":
    sys.exit(main())
