import hashlib
import importlib.util
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SDC_CLI = REPO_ROOT / "sdc-cli.py"
TASK_BRIEF = REPO_ROOT / "scripts" / "sdc-task-brief.py"
REVIEW_PACKAGE = REPO_ROOT / "scripts" / "sdc-review-package.py"
PACKAGE_CODEX = REPO_ROOT / "scripts" / "package-codex-plugin.py"
INSTALLER = REPO_ROOT / "bin" / "install.js"


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


def fingerprinted_managed(relative: str, body: str) -> str:
    digest = hashlib.sha256(body.encode()).hexdigest()
    return f"<!-- SDC-MANAGED path={relative}; sha256={digest} -->\n{body}"


def write_confirmed_change(change: Path, *, completed: bool = False):
    task_box = "x" if completed else " "
    review_status = "Approved" if completed else "Pending"
    evidence_status = "notes.md#task-review-evidence" if completed else "Pending"
    final_review_status = "Approved" if completed else "Pending"
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
- Schema: SDC 1.3.0
- Source: eval fixture

## 1. Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| .sdc/knowledge/index.md | Confirmed | eval fixture | Routes project knowledge |
| .sdc/knowledge/product/rules.md | Confirmed | eval fixture | Confirms no conflicting business rule in this fixture |

## 1.1 Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## 1.2 Common Ground Used

| ID | Tier | Statement | Source | Why It Matters |
|---|---|---|---|---|
| CG-01 | ESTABLISHED | Meeting room booking MVP is confirmed | eval fixture | Allows final REQ/AC creation |

## 1.3 Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | N/A | No workflow/state change | design.md#process-state-diagrams | N/A because fixture has one simple booking behavior and no workflow state machine |
| Sequence / Integration Diagram | N/A | No integration | design.md#sequence-integration-diagrams | N/A because fixture has no external integration |
| API / Contract Specification | N/A | No public API contract | design.md#api-contract-specification | N/A because fixture validates internal behavior only |
| Data Model / Migration Contract | N/A | No schema migration | design.md#data-model-migration-contract | N/A because fixture has no persistence schema |
| UX Flow / Interaction States | N/A | No UI | design.md#ux-flow-interaction-states | N/A because fixture has no UI |
| Test Matrix | Required | AC validation | design.md#test-matrix | AC-01 behavior validation is required |
| Deploy / Release Checklist | N/A | No runtime release impact | design.md#deploy-release-checklist | N/A because fixture has no deployment/config changes |
| AI Involvement Note | N/A | Eval fixture | design.md#ai-involvement-note | N/A because fixture is deterministic CLI validation |

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

## Common Ground Used

| ID | Tier | Statement | Source | Why It Matters |
|---|---|---|---|---|
| CG-01 | ESTABLISHED | Meeting room booking MVP is confirmed | eval fixture | Allows design planning |

## Global Constraints

| ID | Constraint | Source | Applies To |
|---|---|---|---|
| GC-01 | Reject overlaps without adding notifications | spec.md#REQ-01 | all tasks |

## Plan Preflight

- Status: Passed
- Reviewed Against: spec.md, design.md, tasks.md, Artifact Output Contract
- Findings: None

## Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | N/A | No workflow/state change | design.md#process-state-diagrams | N/A because fixture has one simple booking behavior and no workflow state machine |
| Sequence / Integration Diagram | N/A | No integration | design.md#sequence-integration-diagrams | N/A because fixture has no external integration |
| API / Contract Specification | N/A | No public API contract | design.md#api-contract-specification | N/A because fixture validates internal behavior only |
| Data Model / Migration Contract | N/A | No schema migration | design.md#data-model-migration-contract | N/A because fixture has no persistence schema |
| UX Flow / Interaction States | N/A | No UI | design.md#ux-flow-interaction-states | N/A because fixture has no UI |
| Test Matrix | Required | AC validation | design.md#test-matrix | AC-01 behavior validation is required |
| Deploy / Release Checklist | N/A | No runtime release impact | design.md#deploy-release-checklist | N/A because fixture has no deployment/config changes |
| AI Involvement Note | N/A | Eval fixture | design.md#ai-involvement-note | N/A because fixture is deterministic CLI validation |

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

## Process / State Diagrams
N/A because fixture has one simple booking behavior and no workflow state machine.

## Sequence / Integration Diagrams
N/A because fixture has no external integration.

## API / Contract Specification
N/A because fixture validates internal behavior only.

## Data Model / Migration Contract
N/A because fixture has no persistence schema.

## UX Flow / Interaction States
N/A because fixture has no UI.

## Test Matrix

| AC | Scenario | Level | Verification | Expected Result | Status |
|---|---|---|---|---|---|
| AC-01 | overlapping booking is rejected | behavior | sdc validate current-change | validation stays traceable | Required |

## Deploy / Release Checklist
N/A because fixture has no deployment/config changes.

## AI Involvement Note
N/A because fixture is deterministic CLI validation.

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

## Global Constraints

| ID | Constraint | Source | Applies To |
|---|---|---|---|
| GC-01 | Reject overlaps without adding notifications | spec.md#REQ-01 | T001, T900 |

## Plan Preflight

- Status: Passed
- Reviewed Against: spec.md, design.md, tasks.md, Artifact Output Contract
- Findings: None

## 实现任务

- [{task_box}] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] Write and satisfy overlapping booking behavior validation
  - Depends on: none
  - Files: src/booking.py, tests/test_booking.py
  - Consumes: REQ-01 booking request and existing bookings
  - Produces: overlap rejection behavior used by T900
  - Verify: python3 -m py_compile sdc-cli.py
  - Expected: command exits 0 and overlapping booking behavior remains traceable to AC-01
  - Review: {review_status}
  - Evidence: {evidence_status}
  - Source: spec.md#AC-01

## 验证任务

- [{task_box}] T900 [REQ-01] [AC-01] [Phase Verify] [Size: S] Run validation evidence for simulated flow
  - Depends on: T001
  - Files: .sdc/changes/active/{change.name}/notes.md
  - Consumes: T001 overlap rejection behavior
  - Produces: final AC-01 validation evidence
  - Verify: sdc validate current-change
  - Expected: validation exits 0 with AC-01 traceability intact
  - Review: {review_status}
  - Evidence: {evidence_status}
  - Source: spec.md#AC-01
"""
    )
    change.joinpath("context-pack.md").write_text(
        f"""# Context Pack

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

## Common Ground Used

| ID | Tier | Statement | Source | Why It Matters |
|---|---|---|---|---|
| CG-01 | ESTABLISHED | Meeting room booking MVP is confirmed | eval fixture | Allows execution |

## Expert Profiles Used

| Profile | Why Used | Sources Read | Decisions / Checks Affected |
|---|---|---|---|
| product-discovery | MVP boundary and acceptance | discovery.md, spec.md | Keeps notifications out of scope |
| test-strategy | AC-01 must be behavior-validated | spec.md, tasks.md | Requires validation evidence |

## Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | N/A | No workflow/state change | design.md#process-state-diagrams | N/A because fixture has one simple booking behavior and no workflow state machine |
| Sequence / Integration Diagram | N/A | No integration | design.md#sequence-integration-diagrams | N/A because fixture has no external integration |
| API / Contract Specification | N/A | No public API contract | design.md#api-contract-specification | N/A because fixture validates internal behavior only |
| Data Model / Migration Contract | N/A | No schema migration | design.md#data-model-migration-contract | N/A because fixture has no persistence schema |
| UX Flow / Interaction States | N/A | No UI | design.md#ux-flow-interaction-states | N/A because fixture has no UI |
| Test Matrix | Required | AC validation | design.md#test-matrix | AC-01 behavior validation is required |
| Deploy / Release Checklist | N/A | No runtime release impact | design.md#deploy-release-checklist | N/A because fixture has no deployment/config changes |
| AI Involvement Note | N/A | Eval fixture | design.md#ai-involvement-note | N/A because fixture is deterministic CLI validation |

## Global Constraints

| ID | Constraint | Source | Applies To |
|---|---|---|---|
| GC-01 | Reject overlaps without adding notifications | spec.md#REQ-01 | all tasks |

## Execution Orchestration

- Plan Preflight: Passed
- Mode: Inline fixture with separate implement/review evidence
- Runtime Workspace: .sdc/runtime/{change.name}/
- Task Review: Spec Compliance + Code Quality
- Final Whole-Change Review: Required

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
        f"""# Notes

## Changed Files
Fixture flow only.

## Validation Evidence
Validated by promptfoo SDC flow eval.

## Task Review Evidence

### T001

- Spec Compliance: {review_status}
- Code Quality: {review_status}
- Evidence: notes.md#validation-evidence

### T900

- Spec Compliance: {review_status}
- Code Quality: {review_status}
- Evidence: notes.md#validation-evidence

## Final Whole-Change Review

- Status: {final_review_status}
- Spec Compliance: {final_review_status}
- Code Quality: {final_review_status}
- Evidence: notes.md#validation-evidence

## Knowledge Candidates
See knowledge-candidates.md.
"""
    )

    if completed:
        runtime = change.parents[2] / "runtime" / change.name
        runtime.mkdir(parents=True, exist_ok=True)
        runtime.joinpath("progress.md").write_text(
            """# SDC Execution Progress

| Task | Status | Evidence | Review |
|---|---|---|---|
| T001 | complete | notes.md#task-review-evidence | Approved |
| T900 | complete | notes.md#task-review-evidence | Approved |
"""
        )


def init_greenfield(root: Path) -> str:
    code, output = run_sdc(root, "init")
    checks = [
        marker(root, ".sdc/common-ground.md"),
        marker(root, ".sdc/expert-routing.md"),
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
        fingerprinted_managed("constitution.md", """# SDC Project Constitution

## 1. Governance Priority

## 2. Fact Priority

## 3. Core Chain
""")
    )
    sdc.joinpath("templates", "design.md").write_text(
        fingerprinted_managed("templates/design.md", """# Design

## Knowledge Sources Used

| Source | Why It Matters |
|---|---|

## Solution Summary / 方案摘要
""")
    )
    sdc.joinpath("templates", "context-pack.md").write_text(
        fingerprinted_managed("templates/context-pack.md", """# Context Pack

## Goal

## Knowledge Sources Used

| Source | Why It Matters |
|---|---|
""")
    )
    sdc.joinpath("templates", "knowledge-candidates.md").write_text(
        fingerprinted_managed("templates/knowledge-candidates.md", """# Knowledge Candidates

| Candidate | Type | Scope | Source | Status | Target |
|---|---|---|---|---|---|
""")
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
        "constitution output contract: yes" if "Artifact Output Contract Discipline" in upgraded_files[0].read_text() else "constitution output contract: no",
        "design gaps: yes" if "## Knowledge Gaps" in upgraded_files[1].read_text() else "design gaps: no",
        "design common ground: yes" if "## Common Ground Used" in upgraded_files[1].read_text() else "design common ground: no",
        "design output contract: yes" if "## Artifact Output Contract" in upgraded_files[1].read_text() else "design output contract: no",
        "design test matrix: yes" if "## Test Matrix" in upgraded_files[1].read_text() else "design test matrix: no",
        "context forbidden: yes" if "## Forbidden Assumptions" in upgraded_files[2].read_text() else "context forbidden: no",
        "context profiles: yes" if "## Expert Profiles Used" in upgraded_files[2].read_text() else "context profiles: no",
        "context output contract: yes" if "## Artifact Output Contract" in upgraded_files[2].read_text() else "context output contract: no",
        "candidate evidence: yes" if "Evidence Needed" in upgraded_files[3].read_text() else "candidate evidence: no",
        f"backup count: {len(backups)}",
    ]
    expected = (
        code == 0
        and "已安全升级" in output
        and all(check.endswith("yes") for check in checks[:10])
        and len(backups) >= 4
    )
    return "\n".join([output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def init_preserves_user_modified_managed_file(root: Path) -> str:
    sdc = root / ".sdc"
    sdc.mkdir()
    original = """# SDC Project Constitution

## 1. Governance Priority

## 2. Fact Priority

## 3. Core Chain
"""
    modified = fingerprinted_managed("constitution.md", original) + "\n## Company Rule\n\nNever bypass approval.\n"
    constitution = sdc / "constitution.md"
    constitution.write_text(modified)

    code, output = run_sdc(root, "init")
    backups = list(sdc.glob("constitution.md.bak-*"))
    checks = [
        "custom constitution preserved: yes" if constitution.read_text() == modified else "custom constitution preserved: no",
        "no overwrite backup created: yes" if not backups else "no overwrite backup created: no",
        "preservation reported: yes" if "检测到用户修改，已跳过自动升级" in output else "preservation reported: no",
    ]
    expected = code == 0 and all(check.endswith("yes") for check in checks)
    return "\n".join([output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def init_upgrades_exact_legacy_template(root: Path) -> str:
    tasks = root / ".sdc/current/tasks.md"
    tasks.parent.mkdir(parents=True)
    tasks.write_text(
        """# Current Tasks

> 当前任务清单。任务必须能追溯到 REQ/AC。

## Tasks

- [ ] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] Draft task
  - Depends on: none
  - Verify: TODO
  - Source: current/spec.md#AC-01
"""
    )
    code, output = run_sdc(root, "init")
    content = tasks.read_text()
    checks = [
        "legacy template upgraded: yes" if "## Global Constraints" in content and "Reviewed Against:" in content else "legacy template upgraded: no",
        "managed fingerprint added: yes" if content.startswith("<!-- SDC-MANAGED path=current/tasks.md;") else "managed fingerprint added: no",
        "legacy backup created: yes" if list(tasks.parent.glob("tasks.md.bak-*")) else "legacy backup created: no",
    ]
    expected = code == 0 and all(check.endswith("yes") for check in checks)
    return "\n".join([output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def managed_fingerprint_is_not_real_content(root: Path) -> str:
    filepath = root / "empty-managed.md"
    filepath.write_text(fingerprinted_managed("empty-managed.md", "# Empty Managed Template\n"))
    spec = importlib.util.spec_from_file_location("sdc_cli_eval_module", SDC_CLI)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected = not module.has_real_content(filepath)
    return "\n".join([
        "fingerprint ignored as content: yes" if expected else "fingerprint ignored as content: no",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def init_adds_runtime_ignore_without_overwriting(root: Path) -> str:
    sdc = root / ".sdc"
    sdc.mkdir()
    gitignore = sdc / ".gitignore"
    gitignore.write_text("# Team-local rules\n*.tmp\n/private-notes/\n")

    first_code, first_output = run_sdc(root, "init")
    second_code, second_output = run_sdc(root, "init")
    content = gitignore.read_text()
    checks = [
        "custom rule preserved: yes" if "/private-notes/" in content else "custom rule preserved: no",
        "runtime ignored once: yes" if content.splitlines().count("/runtime/") == 1 else "runtime ignored once: no",
        "second init idempotent: yes" if "未覆盖任何文件" in second_output else "second init idempotent: no",
    ]
    expected = first_code == 0 and second_code == 0 and all(check.endswith("yes") for check in checks)
    return "\n".join([first_output, second_output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


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
        and ".sdc/common-ground.md" in archive_text
        and ".sdc/expert-routing.md" in archive_text
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
            "|---|---|---|---|---|---|\n\n## Common Ground Used",
            "|---|---|---|---|---|---|\n| KG-01 | Permission model | Needed for booking access | REQ-01 | Ask user | Open |\n\n## Common Ground Used",
        )
    )
    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Knowledge Gap" in output and "未闭合" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: open knowledge gap" if expected else "UNEXPECTED_PASS: open knowledge gap",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def open_common_ground_blocks_execution(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    context = change / "context-pack.md"
    context.write_text(
        context.read_text().replace(
            "| CG-01 | ESTABLISHED | Meeting room booking MVP is confirmed | eval fixture | Allows execution |",
            "| CG-01 | OPEN | Permission model is not confirmed | eval fixture | Blocks access rules |",
        )
    )
    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Common Ground" in output and "OPEN" in output and "不可执行" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: open common ground" if expected else "UNEXPECTED_PASS: open common ground",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def working_common_ground_blocks_final_execution(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    context = change / "context-pack.md"
    context.write_text(
        context.read_text().replace(
            "| CG-01 | ESTABLISHED | Meeting room booking MVP is confirmed | eval fixture | Allows execution |",
            "| CG-01 | WORKING | Room approval policy looks simple but is not confirmed | eval fixture | Could change scope |",
        )
    )
    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Common Ground" in output and "WORKING" in output and "不可执行" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: working common ground" if expected else "UNEXPECTED_PASS: working common ground",
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


def missing_artifact_output_contract_blocks_execution(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)

    spec = change / "spec.md"
    spec.write_text(
        spec.read_text().replace(
            "The system must reject overlapping bookings for the same room.",
            "The system must reject overlapping bookings for the same room through a POST /rooms/bookings API endpoint.",
        )
    )

    design = change / "design.md"
    design.write_text(
        "\n".join(
            line
            for line in design.read_text().splitlines()
            if "API / Contract Specification" not in line
        )
    )

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "API / Contract Specification" in output and "触发式交付物" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: missing artifact output contract" if expected else "UNEXPECTED_PASS: missing artifact output contract",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def missing_task_interface_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(tasks.read_text().replace("  - Produces: overlap rejection behavior used by T900\n", "", 1))

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "T001 缺少任务字段: Produces:" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: missing task interface" if expected else "UNEXPECTED_PASS: missing task interface",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def empty_global_constraints_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    design = change / "design.md"
    design.write_text(
        design.read_text().replace(
            "| GC-01 | Reject overlaps without adding notifications | spec.md#REQ-01 | all tasks |",
            "",
            1,
        )
    )

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Global Constraints 缺少有效 GC-* 行" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: empty global constraints" if expected else "UNEXPECTED_PASS: empty global constraints",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def conflicting_global_constraints_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    context = change / "context-pack.md"
    context.write_text(
        context.read_text().replace(
            "Reject overlaps without adding notifications",
            "Allow notifications as an optional side effect",
            1,
        )
    )

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Global Constraints 与" in output and "不一致" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: conflicting global constraints" if expected else "UNEXPECTED_PASS: conflicting global constraints",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def incomplete_plan_preflight_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(
        tasks.read_text()
        .replace("- Reviewed Against: spec.md, design.md, tasks.md, Artifact Output Contract", "- Reviewed Against:", 1)
        .replace("- Findings: None", "- Findings: Pending", 1)
    )

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Plan Preflight Reviewed Against 不完整" in output and "Plan Preflight Findings 未闭合" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: incomplete plan preflight" if expected else "UNEXPECTED_PASS: incomplete plan preflight",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def open_plan_preflight_findings_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(tasks.read_text().replace("- Findings: None", "- Findings: Blocking conflict remains", 1))

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Plan Preflight Findings 未闭合" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: open plan preflight findings" if expected else "UNEXPECTED_PASS: open plan preflight findings",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def uncertain_plan_preflight_findings_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(tasks.read_text().replace("- Findings: None", "- Findings: Resolved?", 1))

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Plan Preflight Findings 未闭合" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: uncertain preflight closure" if expected else "UNEXPECTED_PASS: uncertain preflight closure",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def uncertain_plan_preflight_status_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(tasks.read_text().replace("- Status: Passed", "- Status: Passed?", 1))

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "缺少已通过的 Plan Preflight" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: uncertain preflight status" if expected else "UNEXPECTED_PASS: uncertain preflight status",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def current_plan_global_constraints_are_validated(root: Path) -> str:
    run_sdc(root, "init")
    code, output = run_sdc(root, "validate", "current")
    expected = code != 0 and ".sdc/current/plan.md Global Constraints 缺少有效 GC-* 行" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: current plan global constraints" if expected else "MISSING_BLOCK: current plan global constraints",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def malformed_global_constraint_id_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(
        tasks.read_text().replace(
            "| GC-01 | Reject overlaps without adding notifications | spec.md#REQ-01 | T001, T900 |",
            "| GC-01 | Reject overlaps without adding notifications | spec.md#REQ-01 | T001, T900 |\n"
            "| GC-02? | Preserve existing bookings | spec.md#REQ-01 | T001 |",
            1,
        )
    )

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Global Constraints ID 无效: GC-02?" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: malformed global constraint id" if expected else "UNEXPECTED_PASS: malformed global constraint id",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def duplicate_task_id_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(tasks.read_text().replace("- [ ] T900", "- [ ] T001", 1))

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "存在重复任务 ID: T001" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: duplicate task id" if expected else "UNEXPECTED_PASS: duplicate task id",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def uncertain_context_pack_preflight_status_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    context = change / "context-pack.md"
    context.write_text(context.read_text().replace("- Plan Preflight: Passed", "- Plan Preflight: Passed?", 1))

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Execution Orchestration 缺少或未确认: Plan Preflight: Passed" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: uncertain context preflight status" if expected else "UNEXPECTED_PASS: uncertain context preflight status",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def invalid_task_ids_block_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(tasks.read_text().replace("T001", "t001").replace("T900", "t900"))

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "缺少有效 T### 任务" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: invalid task ids" if expected else "UNEXPECTED_PASS: invalid task ids",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def mixed_invalid_task_id_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(tasks.read_text().replace("- [ ] T900", "- [ ] t900", 1))

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "任务 checkbox 行格式无效" in output and "t900" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: mixed invalid task id" if expected else "UNEXPECTED_PASS: mixed invalid task id",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def invalid_runtime_workspace_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    context = change / "context-pack.md"
    context.write_text(
        context.read_text().replace(
            f"- Runtime Workspace: .sdc/runtime/{change.name}/",
            "- Runtime Workspace: Pending",
            1,
        )
    )

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Execution Orchestration 缺少或未确认: Runtime Workspace" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: invalid runtime workspace" if expected else "UNEXPECTED_PASS: invalid runtime workspace",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def negated_task_review_contract_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    context = change / "context-pack.md"
    context.write_text(
        context.read_text().replace(
            "- Task Review: Spec Compliance + Code Quality",
            "- Task Review: Do not require Spec Compliance or Code Quality",
            1,
        )
    )

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Execution Orchestration 缺少或未确认: Task Review" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: negated task review contract" if expected else "UNEXPECTED_PASS: negated task review contract",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def duplicate_plan_preflight_field_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(tasks.read_text().replace("- Status: Passed", "- Status: Passed\n- Status: Pending", 1))

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Plan Preflight Status 字段重复" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: duplicate preflight field" if expected else "UNEXPECTED_PASS: duplicate preflight field",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def duplicate_task_interface_field_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(tasks.read_text().replace("  - Review: Pending", "  - Review: Pending\n  - Review: Needs Fixes", 1))

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "T001 存在重复任务字段: Review:" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: duplicate task field" if expected else "UNEXPECTED_PASS: duplicate task field",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def contradictory_dual_review_verdict_blocks_check(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change, completed=True)
    notes = change / "notes.md"
    notes.write_text(
        notes.read_text().replace(
            "- Code Quality: Approved",
            "- Code Quality: Approved\n- Code Quality: Needs Fixes",
            1,
        )
    )

    code, output = run_sdc(root, "check", change.name)
    expected = code != 0 and "T001 存在重复 Code Quality verdict" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: contradictory review verdict" if expected else "UNEXPECTED_PASS: contradictory review verdict",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def duplicate_plan_preflight_section_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(
        tasks.read_text()
        + "\n## Plan Preflight\n\n- Status: Blocked\n- Reviewed Against: spec.md\n- Findings: Blocking conflict remains\n"
    )

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "Plan Preflight 章节重复" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: duplicate preflight section" if expected else "UNEXPECTED_PASS: duplicate preflight section",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def duplicate_task_review_block_blocks_check(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change, completed=True)
    notes = change / "notes.md"
    notes.write_text(
        notes.read_text().replace(
            "## Final Whole-Change Review",
            "### T001\n\n- Spec Compliance: Approved\n- Code Quality: Needs Fixes\n"
            "- Evidence: notes.md#validation-evidence\n\n## Final Whole-Change Review",
            1,
        )
    )

    code, output = run_sdc(root, "check", change.name)
    expected = code != 0 and "存在重复 T001 Task Review Evidence 块" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: duplicate task review block" if expected else "UNEXPECTED_PASS: duplicate task review block",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def duplicate_final_review_section_blocks_check(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change, completed=True)
    notes = change / "notes.md"
    notes.write_text(
        notes.read_text()
        + "\n## Final Whole-Change Review\n\n- Status: Needs Fixes\n"
        "- Spec Compliance: Needs Fixes\n- Code Quality: Needs Fixes\n"
        "- Evidence: notes.md#validation-evidence\n"
    )

    code, output = run_sdc(root, "check", change.name)
    expected = code != 0 and "Final Whole-Change Review 章节重复" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: duplicate final review section" if expected else "UNEXPECTED_PASS: duplicate final review section",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def empty_task_interface_blocks_plan(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)
    tasks = change / "tasks.md"
    tasks.write_text(
        tasks.read_text().replace(
            "  - Consumes: REQ-01 booking request and existing bookings",
            "  - Consumes: ",
            1,
        )
    )

    code, output = run_sdc(root, "validate", change.name)
    expected = code != 0 and "T001 的 Consumes 仍是占位值: (empty)" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: empty task interface" if expected else "UNEXPECTED_PASS: empty task interface",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def completed_task_without_review_blocks_check(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change, completed=True)
    tasks = change / "tasks.md"
    tasks.write_text(tasks.read_text().replace("  - Review: Approved\n", "  - Review: Pending\n", 1))

    code, output = run_sdc(root, "check", change.name)
    expected = code != 0 and "T001 已完成但 Review 不是 Approved" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: completed task missing approved review" if expected else "UNEXPECTED_PASS: completed task missing approved review",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def missing_dual_review_verdict_blocks_check(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change, completed=True)
    notes = change / "notes.md"
    notes.write_text(notes.read_text().replace("- Code Quality: Approved\n", "", 1))

    code, output = run_sdc(root, "check", change.name)
    expected = code != 0 and "T001 缺少已批准的 Code Quality verdict" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: missing dual review verdict" if expected else "UNEXPECTED_PASS: missing dual review verdict",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def missing_review_evidence_target_blocks_check(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change, completed=True)
    notes = change / "notes.md"
    notes.write_text(notes.read_text().replace("notes.md#validation-evidence", "missing-review.md#evidence", 1))

    code, output = run_sdc(root, "check", change.name)
    expected = code != 0 and "T001 Evidence 引用不存在或锚点无效" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: missing review evidence target" if expected else "UNEXPECTED_PASS: missing review evidence target",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def ignored_review_evidence_blocks_check(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change, completed=True)
    runtime = root / ".sdc" / "runtime" / change.name
    proof = runtime / "review-proof.md"
    proof.write_text("# Review Proof\n")
    notes = change / "notes.md"
    notes.write_text(
        notes.read_text().replace(
            "notes.md#validation-evidence",
            f".sdc/runtime/{change.name}/review-proof.md#review-proof",
            1,
        )
    )

    code, output = run_sdc(root, "check", change.name)
    expected = code != 0 and "T001 Evidence 引用不存在或锚点无效" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: ignored review evidence" if expected else "UNEXPECTED_PASS: ignored review evidence",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def delivery_check_allows_missing_runtime_ledger(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change, completed=True)
    ledger = root / ".sdc" / "runtime" / change.name / "progress.md"
    ledger.unlink()

    code, output = run_sdc(root, "check", change.name)
    expected = code == 0 and "运行态恢复账本不存在" in output
    return "\n".join([
        output,
        "EXPECTED_WARN: missing non-authoritative runtime ledger" if expected else "UNEXPECTED_BLOCK: missing non-authoritative runtime ledger",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def inconsistent_runtime_ledger_blocks_check(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change, completed=True)
    ledger = root / ".sdc" / "runtime" / change.name / "progress.md"
    ledger.write_text(ledger.read_text().replace("| T001 | complete |", "| T001 | pending |"))

    code, output = run_sdc(root, "check", change.name)
    expected = code != 0 and "已完成任务 T001 的 Status 不是 complete" in output
    return "\n".join([
        output,
        "EXPECTED_BLOCK: inconsistent runtime ledger" if expected else "UNEXPECTED_PASS: inconsistent runtime ledger",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def execution_helpers_create_file_handoffs(root: Path) -> str:
    subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    subprocess.run(["git", "config", "user.name", "SDC Eval"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "sdc-eval@example.invalid"], cwd=root, check=True)
    run_sdc(root, "init")
    run_sdc(root, "change", "meeting-room", "--confirmed-intake")
    change = active_change(root, "meeting-room")
    write_confirmed_change(change)

    brief_result = subprocess.run(
        ["python3", str(TASK_BRIEF), change.name, "T001"],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    root.joinpath("sample.txt").write_text("before\n")
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "eval baseline"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True, stdout=subprocess.PIPE
    ).stdout.strip()
    root.joinpath("sample.txt").write_text("after\n")

    review_result = subprocess.run(
        ["python3", str(REVIEW_PACKAGE), base, "WORKTREE", change.name, "T001"],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    runtime = root / ".sdc" / "runtime" / change.name
    brief = runtime / "task-T001-brief.md"
    report = runtime / "task-T001-report.md"
    ledger = runtime / "progress.md"
    review = runtime / "task-T001-review-package.md"
    checks = [
        marker(root, str(brief.relative_to(root))),
        marker(root, str(report.relative_to(root))),
        marker(root, str(ledger.relative_to(root))),
        marker(root, str(review.relative_to(root))),
        "brief interfaces: yes" if brief.exists() and "Produces:" in brief.read_text() else "brief interfaces: no",
        "review diff: yes" if review.exists() and "-before" in review.read_text() and "+after" in review.read_text() else "review diff: no",
    ]
    expected = brief_result.returncode == 0 and review_result.returncode == 0 and all(
        item.endswith("exists") or item.endswith("yes") for item in checks
    )
    return "\n".join([
        brief_result.stdout,
        review_result.stdout,
        *checks,
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def review_package_blocks_untracked_worktree(root: Path) -> str:
    subprocess.run(["git", "init"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    subprocess.run(["git", "config", "user.name", "SDC Eval"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "sdc-eval@example.invalid"], cwd=root, check=True)
    root.joinpath("tracked.txt").write_text("baseline\n")
    subprocess.run(["git", "add", "tracked.txt"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "baseline"], cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    root.joinpath("new-source.py").write_text("print('must be reviewed')\n")

    result = subprocess.run(
        ["python3", str(REVIEW_PACKAGE), base, "WORKTREE", "untracked-review", "T001"],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    expected = result.returncode != 0 and "untracked" in result.stdout.lower() and not (root / ".sdc/runtime/untracked-review/task-T001-review-package.md").exists()
    return "\n".join([
        result.stdout,
        "EXPECTED_BLOCK: untracked files missing from WORKTREE diff" if expected else "UNEXPECTED_PACKAGE: untracked files missing from WORKTREE diff",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def execution_contract_serializes_tasks(root: Path) -> str:
    reference = (REPO_ROOT / "sdc-references/execution-orchestration.md").read_text()
    command = (REPO_ROOT / "commands/apply.md").read_text()
    skill = (REPO_ROOT / "skills/sdc-apply/SKILL.md").read_text()
    checks = [
        "shared contract serial: yes" if "do not dispatch multiple implementation tasks in parallel" in reference else "shared contract serial: no",
        "apply command serial: yes" if "Execute tasks serially" in command else "apply command serial: no",
        "generated skill serial: yes" if "Execute tasks serially" in skill else "generated skill serial: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([*checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def codex_install_removes_stale_layout(root: Path) -> str:
    home = root / "home"
    stale = home / ".codex/local-marketplaces/sdc-local/plugins/sdc/skills/sdc-shared/legacy.md"
    stale.parent.mkdir(parents=True)
    stale.write_text("stale shared layout\n")
    (home / ".codex/plugins").mkdir(parents=True)
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["USERPROFILE"] = str(home)

    result = subprocess.run(
        ["node", str(INSTALLER)],
        cwd=REPO_ROOT,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    plugin = home / ".codex/local-marketplaces/sdc-local/plugins/sdc"
    cache_root = home / ".codex/plugins/cache/sdc-local/sdc"
    cache_versions = [path for path in cache_root.iterdir() if path.is_dir()] if cache_root.exists() else []
    cache_plugin = cache_versions[0] if len(cache_versions) == 1 else None
    checks = [
        "stale shared removed: yes" if not stale.exists() else "stale shared removed: no",
        "public skill installed: yes" if (plugin / "skills/sdc-core/SKILL.md").exists() else "public skill installed: no",
        "root references installed: yes" if (plugin / "sdc-references/execution-orchestration.md").exists() else "root references installed: no",
        "marketplace Claude skills absent: yes" if not (plugin / ".claude/skills").exists() else "marketplace Claude skills absent: no",
        "cache Claude skills absent: yes" if cache_plugin and not (cache_plugin / ".claude/skills").exists() else "cache Claude skills absent: no",
    ]
    expected = result.returncode == 0 and all(check.endswith("yes") for check in checks)
    return "\n".join([result.stdout, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def codex_install_recovers_interrupted_swap(root: Path) -> str:
    home = root / "home"
    plugin = home / ".codex/local-marketplaces/sdc-local/plugins/sdc"
    backup = plugin.with_name("sdc.backup")
    backup.mkdir(parents=True)
    backup.joinpath("interrupted-marker.txt").write_text("previous valid plugin\n")
    (home / ".codex/plugins").mkdir(parents=True)
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["USERPROFILE"] = str(home)

    result = subprocess.run(
        ["node", str(INSTALLER)],
        cwd=REPO_ROOT,
        env=env,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    checks = [
        "interrupted backup cleaned: yes" if not backup.exists() else "interrupted backup cleaned: no",
        "recovered plugin installed: yes" if (plugin / "skills/sdc-core/SKILL.md").exists() else "recovered plugin installed: no",
        "transaction stage cleaned: yes" if not plugin.with_name("sdc.stage").exists() else "transaction stage cleaned: no",
    ]
    expected = result.returncode == 0 and all(check.endswith("yes") for check in checks)
    return "\n".join([result.stdout, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def codex_package_is_rootless_and_deterministic(root: Path) -> str:
    first = root / "sdc-codex-a.zip"
    second = root / "sdc-codex-b.zip"
    results = [
        subprocess.run(
            ["python3", str(PACKAGE_CODEX), "--allow-dirty", "--output", str(output)],
            cwd=REPO_ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for output in (first, second)
    ]

    names = set()
    if first.exists():
        with zipfile.ZipFile(first) as archive:
            names = set(archive.namelist())
    required = {
        ".codex-plugin/plugin.json",
        "skills/sdc-core/SKILL.md",
        "skills/sdc-init/SKILL.md",
        "skills/sdc-apply/SKILL.md",
        "sdc-references/execution-orchestration.md",
        "scripts/sdc-task-brief.py",
        "scripts/sdc-review-package.py",
        "sdc-cli.py",
    }
    forbidden_prefixes = ("sdc/", ".agents/", ".claude/", ".claude-plugin/", "commands/", "bin/", "docs/", "evals/")
    forbidden = [name for name in names if name.startswith(forbidden_prefixes) or "__pycache__" in name or name.endswith(".pyc")]
    digest_match = (
        first.exists()
        and second.exists()
        and hashlib.sha256(first.read_bytes()).digest() == hashlib.sha256(second.read_bytes()).digest()
    )
    checks = [
        "package commands: yes" if all(result.returncode == 0 for result in results) else "package commands: no",
        "rootless manifest: yes" if ".codex-plugin/plugin.json" in names and not any(name.startswith("sdc/") for name in names) else "rootless manifest: no",
        "required runtime files: yes" if required.issubset(names) else "required runtime files: no",
        "source-only paths absent: yes" if not forbidden else "source-only paths absent: no",
        "deterministic digest: yes" if digest_match else "deterministic digest: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([*(result.stdout for result in results), *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def standards_pack_import(root: Path) -> str:
    source = root / "spec-rules"
    source.mkdir()
    source.joinpath("code-generation.md").write_text(
        """# Code Generation

Use project conventions when generating service and entity scaffolds.
"""
    )
    source.joinpath("testing.md").write_text(
        """# Testing

Behavior tests should prove acceptance criteria before implementation details.
"""
    )
    source.joinpath(".DS_Store").write_text("system file should not be imported")

    code, output = run_sdc(root, "init", "--standards", str(source))
    target = root / ".sdc" / "standards" / "company"
    index = target / "README.md"
    index_text = index.read_text() if index.exists() else ""
    checks = [
        marker(root, ".sdc/standards/company/code-generation.md"),
        marker(root, ".sdc/standards/company/testing.md"),
        marker(root, ".sdc/standards/company/.DS_Store"),
        "routing index: yes" if "Agents must read this index first" in index_text else "routing index: no",
        "code hint: yes" if "Read when creating new code scaffolds" in index_text else "code hint: no",
        "path leak: no" if str(source) not in index_text else "path leak: yes",
    ]
    expected = (
        code == 0
        and any(check.endswith("code-generation.md: exists") for check in checks)
        and any(check.endswith("testing.md: exists") for check in checks)
        and any(check.endswith(".DS_Store: absent") for check in checks)
        and "routing index: yes" in checks
        and "code hint: yes" in checks
        and "path leak: no" in checks
    )
    return "\n".join([output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


SCENARIOS = {
    "init_greenfield": init_greenfield,
    "init_upgrades_stale_managed_templates": init_upgrades_stale_managed_templates,
    "init_preserves_user_modified_managed_file": init_preserves_user_modified_managed_file,
    "init_upgrades_exact_legacy_template": init_upgrades_exact_legacy_template,
    "managed_fingerprint_is_not_real_content": managed_fingerprint_is_not_real_content,
    "init_adds_runtime_ignore_without_overwriting": init_adds_runtime_ignore_without_overwriting,
    "standards_pack_import": standards_pack_import,
    "change_discovery_open": change_discovery_open,
    "discovery_open_blocks_context_pack": discovery_open_blocks_context_pack,
    "brownfield_requires_impact": brownfield_requires_impact,
    "archive_knowledge_compact_gate": archive_knowledge_compact_gate,
    "unconfirmed_assumption_blocks_execution": unconfirmed_assumption_blocks_execution,
    "open_knowledge_gap_blocks_execution": open_knowledge_gap_blocks_execution,
    "open_common_ground_blocks_execution": open_common_ground_blocks_execution,
    "working_common_ground_blocks_final_execution": working_common_ground_blocks_final_execution,
    "incomplete_candidate_blocks_archive_readiness": incomplete_candidate_blocks_archive_readiness,
    "missing_artifact_output_contract_blocks_execution": missing_artifact_output_contract_blocks_execution,
    "missing_task_interface_blocks_plan": missing_task_interface_blocks_plan,
    "empty_global_constraints_blocks_plan": empty_global_constraints_blocks_plan,
    "conflicting_global_constraints_blocks_plan": conflicting_global_constraints_blocks_plan,
    "incomplete_plan_preflight_blocks_plan": incomplete_plan_preflight_blocks_plan,
    "open_plan_preflight_findings_blocks_plan": open_plan_preflight_findings_blocks_plan,
    "uncertain_plan_preflight_findings_blocks_plan": uncertain_plan_preflight_findings_blocks_plan,
    "uncertain_plan_preflight_status_blocks_plan": uncertain_plan_preflight_status_blocks_plan,
    "current_plan_global_constraints_are_validated": current_plan_global_constraints_are_validated,
    "malformed_global_constraint_id_blocks_plan": malformed_global_constraint_id_blocks_plan,
    "duplicate_task_id_blocks_plan": duplicate_task_id_blocks_plan,
    "uncertain_context_pack_preflight_status_blocks_plan": uncertain_context_pack_preflight_status_blocks_plan,
    "invalid_task_ids_block_plan": invalid_task_ids_block_plan,
    "mixed_invalid_task_id_blocks_plan": mixed_invalid_task_id_blocks_plan,
    "invalid_runtime_workspace_blocks_plan": invalid_runtime_workspace_blocks_plan,
    "negated_task_review_contract_blocks_plan": negated_task_review_contract_blocks_plan,
    "duplicate_plan_preflight_field_blocks_plan": duplicate_plan_preflight_field_blocks_plan,
    "duplicate_task_interface_field_blocks_plan": duplicate_task_interface_field_blocks_plan,
    "contradictory_dual_review_verdict_blocks_check": contradictory_dual_review_verdict_blocks_check,
    "duplicate_plan_preflight_section_blocks_plan": duplicate_plan_preflight_section_blocks_plan,
    "duplicate_task_review_block_blocks_check": duplicate_task_review_block_blocks_check,
    "duplicate_final_review_section_blocks_check": duplicate_final_review_section_blocks_check,
    "empty_task_interface_blocks_plan": empty_task_interface_blocks_plan,
    "completed_task_without_review_blocks_check": completed_task_without_review_blocks_check,
    "missing_dual_review_verdict_blocks_check": missing_dual_review_verdict_blocks_check,
    "missing_review_evidence_target_blocks_check": missing_review_evidence_target_blocks_check,
    "ignored_review_evidence_blocks_check": ignored_review_evidence_blocks_check,
    "delivery_check_allows_missing_runtime_ledger": delivery_check_allows_missing_runtime_ledger,
    "inconsistent_runtime_ledger_blocks_check": inconsistent_runtime_ledger_blocks_check,
    "execution_helpers_create_file_handoffs": execution_helpers_create_file_handoffs,
    "review_package_blocks_untracked_worktree": review_package_blocks_untracked_worktree,
    "execution_contract_serializes_tasks": execution_contract_serializes_tasks,
    "codex_install_removes_stale_layout": codex_install_removes_stale_layout,
    "codex_install_recovers_interrupted_swap": codex_install_recovers_interrupted_swap,
    "codex_package_is_rootless_and_deterministic": codex_package_is_rootless_and_deterministic,
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
