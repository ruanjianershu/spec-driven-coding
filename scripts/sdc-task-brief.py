#!/usr/bin/env python3
"""Create a focused SDC task brief, report file, and recovery ledger."""

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path


def read_text(path):
    return path.read_text() if path.exists() else ""


def resolve_change(value):
    candidate = Path(value)
    if candidate.is_dir():
        return candidate

    if value == "current":
        candidate = Path(".sdc/current")
        if candidate.is_dir():
            return candidate

    for parent in (Path(".sdc/changes/active"), Path(".sdc/changes/archive")):
        exact = parent / value
        if exact.is_dir():
            return exact
        matches = sorted(parent.glob(f"*-{value}"))
        if matches:
            return matches[-1]

    raise SystemExit(f"Cannot find SDC change: {value}")


def section(text, heading):
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n(?P<body>[\s\S]*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE | re.IGNORECASE,
    )
    return match.group("body").strip() if match else ""


def task_block(text, task_id):
    match = re.search(
        rf"^(?P<header>- \[[ xX]\]\s+{re.escape(task_id)}\b[^\n]*)\n(?P<body>[\s\S]*?)(?=^- \[[ xX]\]\s+T\d{{3}}\b|^##\s+|\Z)",
        text,
        re.MULTILINE,
    )
    if not match:
        raise SystemExit(f"Cannot find task {task_id}")
    return f"{match.group('header')}\n{match.group('body').rstrip()}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change", help="Change id, suffix, path, or current")
    parser.add_argument("task", help="Task id such as T001")
    args = parser.parse_args()

    task_id = args.task.upper()
    if not re.fullmatch(r"T\d{3}", task_id):
        raise SystemExit("Task id must match T###")

    change = resolve_change(args.change)
    tasks_file = change / "tasks.md"
    context_file = change / "context-pack.md"
    tasks_text = read_text(tasks_file)
    context_text = read_text(context_file)
    if not tasks_text:
        raise SystemExit(f"Missing tasks.md: {tasks_file}")
    if not context_text:
        raise SystemExit(f"Missing context-pack.md: {context_file}")

    runtime_id = "current" if change == Path(".sdc/current") else change.name
    runtime = Path(".sdc/runtime") / runtime_id
    runtime.mkdir(parents=True, exist_ok=True)

    brief = runtime / f"task-{task_id}-brief.md"
    report = runtime / f"task-{task_id}-report.md"
    ledger = runtime / "progress.md"
    generated_at = datetime.now(timezone.utc).isoformat()

    global_constraints = section(context_text, "Global Constraints") or section(tasks_text, "Global Constraints")
    execution_boundaries = section(context_text, "Execution Boundaries")
    forbidden_assumptions = section(context_text, "Forbidden Assumptions")
    validation_commands = section(context_text, "Validation Commands")

    brief.write_text(
        f"""# {task_id} Task Brief

- Change: {change}
- Generated At: {generated_at}
- Requirements Source: {tasks_file}

## Global Constraints

{global_constraints or 'No confirmed Global Constraints found. Stop and repair the plan.'}

## Task

{task_block(tasks_text, task_id)}

## Execution Boundaries

{execution_boundaries or 'Use the confirmed spec, design, and task scope only.'}

## Forbidden Assumptions

{forbidden_assumptions or 'Do not invent product or technical decisions.'}

## Validation Commands

{validation_commands or 'Use the exact Verify and Expected fields in the task.'}
"""
    )

    if not report.exists():
        report.write_text(
            f"""# {task_id} Implementer Report

- Status: NEEDS_CONTEXT
- Model / Execution Mode: Auto
- Base: Pending
- Head / Working Tree: Pending

## Changed Files

## TDD Evidence

## Commands And Results

## Deviations And Concerns

## Self-Review
"""
        )

    if not ledger.exists():
        ledger.write_text(
            """# SDC Execution Progress

| Task | Status | Evidence | Review |
|------|--------|----------|--------|
"""
        )

    print(f"Brief: {brief}")
    print(f"Report: {report}")
    print(f"Ledger: {ledger}")


if __name__ == "__main__":
    main()
