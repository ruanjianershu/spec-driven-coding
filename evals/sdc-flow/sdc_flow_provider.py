import subprocess
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SDC_CLI = REPO_ROOT / "sdc-cli.py"


def run_sdc(cwd: Path, *args: str):
    result = subprocess.run(
        ["python3", str(SDC_CLI), *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return result.returncode, result.stdout


def active_change(root: Path, suffix: str) -> Path:
    matches = sorted((root / ".sdc" / "changes" / "active").glob(f"*-{suffix}"))
    if not matches:
        raise AssertionError(f"No active change found for suffix {suffix}")
    return matches[-1]


def marker(root: Path, relative: str) -> str:
    status = "exists" if (root / relative).exists() else "absent"
    return f"{relative}: {status}"


def write_confirmed_change(change: Path, *, completed: bool = False):
    task_box = "x" if completed else " "
    change.joinpath("discovery.md").write_text(
        """# Discovery

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| .sdc/knowledge/index.md | Confirmed | eval fixture | No conflicting knowledge in this fixture |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## Current Understanding
Meeting room booking MVP is confirmed.

## Candidate Directions

| Option | Description | Pros | Cons | Status |
|---|---|---|---|---|
| MVP | Booking with conflict prevention | Small | No notifications | Confirmed |

## Tradeoffs
Notifications are deferred.

## Recommended MVP
Employees can book a room; overlapping bookings for the same room are rejected.

## Decision Ledger

| ID | Decision | Status | Source | Impact | Next Step |
|---|---|---|---|---|---|
| D-01 | Notifications are outside the MVP | Confirmed | eval fixture | Keeps scope small | Record as non-goal |

## Open Questions

| ID | Question | Why It Matters | Options | Required Before |
|---|---|---|---|---|

## Exit Criteria

- [x] MVP scope confirmed
- [x] high-impact decisions confirmed or explicitly deferred
- [x] acceptance direction is clear
"""
    )
    change.joinpath("proposal.md").write_text(
        """# Meeting Room Proposal

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| .sdc/knowledge/index.md | Confirmed | eval fixture | Routes project knowledge for the MVP |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## 背景
Employees need a simple way to reserve meeting rooms.

## 目标
Provide a meeting room booking MVP with conflict prevention.

## 非目标
Notifications are deferred.

## 初始场景
Employee books an available room.

## 初始需求
The system prevents duplicate bookings for the same room and time range.

## 初始验收标准
A duplicate booking attempt is rejected with a clear error.

## 任务清单
See tasks.md.

## 风险和回滚
No migration risk in this fixture.
"""
    )
    change.joinpath("spec.md").write_text(
        """# Spec

## 0. 文档元信息

- Status: Confirmed
- Schema: SDC 1.1.10
- Source: eval fixture

## 1. Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| .sdc/knowledge/index.md | Confirmed | eval fixture | Routes project knowledge |
| .sdc/knowledge/product/rules.md | Confirmed | eval fixture | Confirms no conflicting business rule in this fixture |

## 1.1 Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## 2. Decision Ledger / 决策台账

| ID | 决策 | 状态 | 依据来源 | 是否允许进入 REQ/AC | 下一步 |
|---|---|---|---|---|---|
| D-01 | Notifications are outside the MVP | Confirmed | eval fixture | Yes | Track as non-goal |

## 3. Glossary / 统一语言
Room booking means reserving one room for one time range.

## 4. 背景与目标
Support employees reserving meeting rooms.

## 5. Business Invariants / 业务不变量

### INV-01
One room cannot have overlapping confirmed bookings.

## 6. 场景与需求

### SCN-01
Employee reserves an available room.

### REQ-01
The system must reject overlapping bookings for the same room.

## 7. Acceptance Criteria / 验收标准

### AC-01
Given a room already has a booking for a time range
When an employee requests an overlapping booking for that room
Then the system rejects the request and keeps the original booking unchanged.

## 8. 验证策略
Run a behavior test for overlapping bookings.

## 9. 风险、假设与待确认项
No blocking risks remain for the MVP.

## 10. 追溯关系矩阵

| SCN | REQ | AC | Task |
|---|---|---|---|
| SCN-01 | REQ-01 | AC-01 | T001 |
"""
    )
    change.joinpath("design.md").write_text(
        """# Design

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| .sdc/knowledge/technical/testing.md | Confirmed | eval fixture | Provides validation strategy slot |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## Solution Summary / 方案摘要
Add conflict checking before persisting a booking.

## Impact Scope / 影响范围
Booking creation behavior only.

## Non-Scope / 不改范围
Notifications and payments are out of scope.

## Key Tradeoffs / 关键取舍
Use a small behavior-first implementation.

## Data, API, State, or Interaction Changes / 数据、接口、状态或交互变化
Booking conflict validation is required.

## Brownfield Impact Summary / 遗留影响摘要
N/A for greenfield fixtures; brownfield fixtures intentionally require impact.md.

## REQ/AC to Design Decision Mapping / 追溯映射
REQ-01 and AC-01 map to conflict validation.

## Risks, Rollback, and Migration / 风险、回滚和迁移
Rollback removes conflict validation in this fixture.

## Alternatives / 替代方案
Database constraint can be added later if persistence exists.
"""
    )
    change.joinpath("tasks.md").write_text(
        f"""# Tasks

## 实现任务

- [{task_box}] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] Write and satisfy overlapping booking behavior validation
  - Depends on: none
  - Verify: python3 -m py_compile sdc-cli.py
  - Source: spec.md#AC-01

## 验证任务

- [{task_box}] T900 [REQ-01] [AC-01] [Phase Verify] [Size: S] Run validation evidence for simulated flow
  - Depends on: T001
  - Verify: sdc validate current-change
  - Source: spec.md#AC-01
"""
    )
    change.joinpath("context-pack.md").write_text(
        """# Context Pack

## Goal
Implement meeting room booking conflict prevention for the MVP.

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| .sdc/knowledge/index.md | Confirmed | eval fixture | Selects relevant product and technical knowledge |
| spec.md | Confirmed | spec.md#AC-01 | Defines REQ-01 and AC-01 |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## Confirmed Product Knowledge
Duplicate room/time bookings must be rejected.

## Confirmed Technical Knowledge
Validation is behavior-first in this fixture.

## Execution Boundaries
Do not add notifications.

## Forbidden Assumptions
Do not invent approval workflows.

## Task And Traceability Summary
T001 covers REQ-01 and AC-01.

## Validation Commands
sdc validate current-change

## Knowledge Candidate Routing

- Product knowledge candidates: overlapping booking rule
- Technical knowledge candidates: conflict validation strategy
- Memory/procedure candidates: run validate before archive
"""
    )
    change.joinpath("knowledge-candidates.md").write_text(
        """# Knowledge Candidates

| Candidate | Type | Scope | Source | Status | Target | Evidence Needed | Promotion Gate |
|---|---|---|---|---|---|---|---|
| Same room overlapping bookings are rejected | Product Rule | Project | spec.md#AC-01 | Candidate | .sdc/knowledge/product/rules.md | user/archive confirmation | archive confirmation |
| Run validate before archive | Procedure | Project | tasks.md#T900 | Candidate | .sdc/memory/procedures.md | recurring evidence | archive confirmation |
"""
    )
    change.joinpath("notes.md").write_text(
        """# Notes

## Changed Files
Fixture flow only.

## Validation Evidence
Validated by promptfoo SDC flow eval.

## Knowledge Candidates
See knowledge-candidates.md.
"""
    )


def init_greenfield(root: Path) -> str:
    code, output = run_sdc(root, "init")
    checks = [
        marker(root, ".sdc/knowledge/index.md"),
        marker(root, ".sdc/memory/candidates.md"),
        marker(root, ".sdc/current/context-pack.md"),
        marker(root, ".sdc/current/knowledge-candidates.md"),
    ]
    return "\n".join([output, *checks, "RESULT: PASS" if code == 0 and all("exists" in c for c in checks) else "RESULT: FAIL"])


def init_upgrades_stale_managed_templates(root: Path) -> str:
    sdc = root / ".sdc"
    sdc.joinpath("templates").mkdir(parents=True)
    sdc.joinpath("current").mkdir(parents=True)
    sdc.joinpath("constitution.md").write_text(
        """# SDC Project Constitution

## 1. Governance Priority

## 2. Fact Priority

## 3. Core Chain
"""
    )
    sdc.joinpath("templates", "design.md").write_text(
        """# Design

## Knowledge Sources Used

| Source | Why It Matters |
|---|---|

## Solution Summary / 方案摘要
"""
    )
    sdc.joinpath("templates", "context-pack.md").write_text(
        """# Context Pack

## Goal

## Knowledge Sources Used

| Source | Why It Matters |
|---|---|
"""
    )
    sdc.joinpath("templates", "knowledge-candidates.md").write_text(
        """# Knowledge Candidates

| Candidate | Type | Scope | Source | Status | Target |
|---|---|---|---|---|---|
"""
    )

    code, output = run_sdc(root, "init")
    upgraded_files = [
        sdc / "constitution.md",
        sdc / "templates" / "design.md",
        sdc / "templates" / "context-pack.md",
        sdc / "templates" / "knowledge-candidates.md",
    ]
    backups = list(sdc.rglob("*.bak-*"))
    checks = [
        "constitution anti-guess: yes" if "No Evidence, No Fact" in upgraded_files[0].read_text() else "constitution anti-guess: no",
        "design gaps: yes" if "## Knowledge Gaps" in upgraded_files[1].read_text() else "design gaps: no",
        "context forbidden: yes" if "## Forbidden Assumptions" in upgraded_files[2].read_text() else "context forbidden: no",
        "candidate evidence: yes" if "Evidence Needed" in upgraded_files[3].read_text() else "candidate evidence: no",
        f"backup count: {len(backups)}",
    ]
    expected = (
        code == 0
        and "已安全升级" in output
        and all(check.endswith("yes") for check in checks[:4])
        and len(backups) >= 4
    )
    return "\n".join([output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def change_discovery_open(root: Path) -> str:
    run_sdc(root, "init")
    code, output = run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    checks = [
        marker(change, "discovery.md"),
        marker(change, "proposal.md"),
        marker(change, "notes.md"),
        marker(change, "spec.md"),
        marker(change, "context-pack.md"),
    ]
    passed = code == 0 and all(item in checks for item in ["discovery.md: exists", "proposal.md: exists", "notes.md: exists", "spec.md: absent", "context-pack.md: absent"])
    return "\n".join([output, *checks, "RESULT: PASS" if passed else "RESULT: FAIL"])


def discovery_open_blocks_context_pack(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    change.joinpath("context-pack.md").write_text("# Context Pack\n\n## Goal\nPremature handoff.\n")
    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Discovery Gate" in output and "context-pack.md" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: discovery-open context-pack" if expected else "UNEXPECTED_PASS: discovery-open context-pack",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def brownfield_requires_impact(root: Path) -> str:
    root.joinpath("package.json").write_text('{"scripts":{"test":"echo ok"}}\n')
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "impact.md" in output and "brownfield" in output.lower()
    return "\n".join([
        output,
        "EXPECTED_BLOCK: brownfield missing impact" if expected else "UNEXPECTED_PASS: brownfield missing impact",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def archive_knowledge_compact_gate(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change, completed=True)
    validate_code, validate_output = run_sdc(root, "validate", change.name)
    archive_code, archive_output = run_sdc(root, "archive", change.name)
    archive_file = root / ".sdc" / "changes" / "archive" / change.name / "archive.md"
    archive_text = archive_file.read_text() if archive_file.exists() else ""
    expected = (
        validate_code == 0
        and archive_code == 0
        and ".sdc/knowledge/product/" in archive_text
        and ".sdc/knowledge/technical/" in archive_text
        and ".sdc/memory/ or .sdc/knowledge/" in archive_text
    )
    return "\n".join([
        validate_output,
        archive_output,
        archive_text,
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def unconfirmed_assumption_blocks_execution(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    spec = change / "spec.md"
    spec.write_text(spec.read_text().replace("Status: Confirmed", "Status: Confirmed\n- Assumption: Assumed approval flow"))
    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Assumed" in output and "不可执行" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: unconfirmed assumption" if expected else "UNEXPECTED_PASS: unconfirmed assumption",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def open_knowledge_gap_blocks_execution(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    context = change / "context-pack.md"
    context.write_text(
        context.read_text().replace(
            "|---|---|---|---|---|---|\n\n## Confirmed Product Knowledge",
            "|---|---|---|---|---|---|\n| KG-01 | Permission model | Needed for booking access | REQ-01 | Ask user | Open |\n\n## Confirmed Product Knowledge",
        )
    )
    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Knowledge Gap" in output and "未闭合" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: open knowledge gap" if expected else "UNEXPECTED_PASS: open knowledge gap",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def incomplete_candidate_blocks_archive_readiness(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    (change / "knowledge-candidates.md").write_text(
        """# Knowledge Candidates

| Candidate | Type | Scope | Source | Status | Target | Evidence Needed | Promotion Gate |
|---|---|---|---|---|---|---|---|
| Booking rule | Product Rule | Project |  | Candidate | .sdc/knowledge/product/rules.md |  | archive confirmation |
"""
    )
    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "候选知识缺少必填字段" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: incomplete knowledge candidate" if expected else "UNEXPECTED_PASS: incomplete knowledge candidate",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


SCENARIOS = {
    "init_greenfield": init_greenfield,
    "init_upgrades_stale_managed_templates": init_upgrades_stale_managed_templates,
    "change_discovery_open": change_discovery_open,
    "discovery_open_blocks_context_pack": discovery_open_blocks_context_pack,
    "brownfield_requires_impact": brownfield_requires_impact,
    "archive_knowledge_compact_gate": archive_knowledge_compact_gate,
    "unconfirmed_assumption_blocks_execution": unconfirmed_assumption_blocks_execution,
    "open_knowledge_gap_blocks_execution": open_knowledge_gap_blocks_execution,
    "incomplete_candidate_blocks_archive_readiness": incomplete_candidate_blocks_archive_readiness,
}


def call_api(prompt, options, context):
    scenario = context.get("vars", {}).get("scenario") or prompt.strip()
    if scenario not in SCENARIOS:
        return {"output": f"RESULT: FAIL\nUnknown scenario: {scenario}"}

    with tempfile.TemporaryDirectory(prefix="sdc-promptfoo-") as tmp:
        root = Path(tmp)
        try:
            output = SCENARIOS[scenario](root)
        except Exception as exc:
            output = f"RESULT: FAIL\nException: {type(exc).__name__}: {exc}"

    return {"output": output}
