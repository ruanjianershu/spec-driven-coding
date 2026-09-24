import hashlib
import importlib.util
import json
import os
import shutil
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
RUNTIME_CONTEXT = REPO_ROOT / "scripts" / "sdc-runtime-context.py"


def run_sdc(cwd: Path, *args: str):
    result = subprocess.run(
        ["python3", str(SDC_CLI), *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return result.returncode, result.stdout


def run_runtime(cwd: Path, *args: str, env=None):
    runtime_env = os.environ.copy()
    if env:
        runtime_env.update(env)
    result = subprocess.run(
        ["python3", str(RUNTIME_CONTEXT), *args],
        cwd=cwd,
        env=runtime_env,
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


def tree_digest(root: Path, relative: str) -> str:
    base = root / relative
    digest = hashlib.sha256()
    if not base.exists():
        return digest.hexdigest()
    for path in sorted(item for item in base.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


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
  - Verify: python3 -c "assert 1 + 1 == 2"
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
  - Verify: python3 -c "assert 1 + 1 == 2"
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
        # These are measured fixture checks, not evidence of booking business correctness.
        root = change.parents[3]
        if change != root / ".sdc" / "changes" / "active" / change.name or not (root / ".sdc").is_dir():
            return
        # Final task/review artifacts changed; refresh derived context before delivery.
        for role in ("apply", "check"):
            code, output = run_runtime(root, "manifest", "generate", "--change", change.name, "--role", role)
            if code != 0:
                raise AssertionError(output)
        code, output = run_runtime(root, "evidence", "run", "--change", change.name,
                                   "--stage", "check", "--task", "T001", "--task", "T900",
                                   "--", "python3", "-c", "assert 1 + 1 == 2")
        if code != 0:
            raise AssertionError(output)
        code, output = run_runtime(root, "evidence", "review", "--change", change.name,
                                   "--reviewer", "deterministic-fixture-not-an-agent")
        if code != 0:
            raise AssertionError(output)


def advance_change_to_archivable(root: Path, change: Path):
    transitions = [
        ("confirmed", "spec-stage", ("spec.md",)),
    ]
    for state, source, evidence in transitions:
        args = ["state", "set", "--change", change.name, "--state", state, "--source", source]
        for path in evidence:
            args.extend(["--evidence", path])
        code, output = run_runtime(root, *args)
        if code != 0:
            raise AssertionError(output)

    for role in ("apply", "check"):
        code, output = run_runtime(root, "manifest", "generate", "--change", change.name, "--role", role)
        if code != 0:
            raise AssertionError(output)

    transitions = [
        ("planned", "plan-stage", ("design.md", "tasks.md", "context-pack.md")),
        ("applying", "apply-stage", ("tasks.md", "context-pack.md")),
        ("checking", "apply-stage", ("tasks.md", "notes.md")),
        ("archivable", "check-stage", ("tasks.md", "notes.md")),
    ]
    for state, source, evidence in transitions:
        args = ["state", "set", "--change", change.name, "--state", state, "--source", source]
        for path in evidence:
            args.extend(["--evidence", path])
        code, output = run_runtime(root, *args)
        if code != 0:
            raise AssertionError(output)


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
    advance_change_to_archivable(root, change)
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
        "apply command serial: yes" if "serially in dependency order" in command else "apply command serial: no",
        "generated skill serial: yes" if "serially in dependency order" in skill else "generated skill serial: no",
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
        "scripts/sdc-runtime-context.py",
        "sdc-cli.py",
    }
    forbidden_prefixes = ("sdc/", ".agents/", ".claude/", ".claude-plugin/", "commands/", "bin/", "docs/", "evals/", "hooks/")
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


def runtime_distribution_inventory_AC_07(root: Path) -> str:
    init_code, init_output = run_sdc(root, "init")
    if init_code != 0:
        return f"{init_output}\nRESULT: FAIL"
    package = json.loads((REPO_ROOT / "package.json").read_text())
    package_files = set(package.get("files", []))
    packager = (REPO_ROOT / "scripts" / "package-codex-plugin.py").read_text()
    readme = (REPO_ROOT / "README.md").read_text()
    workspace_readme = (root / ".sdc" / "README.md").read_text()
    submission = (REPO_ROOT / "docs" / "official-submission.md").read_text()
    submission_lower = submission.lower()
    checks = [
        "npm ships runtime helper: yes" if "scripts/sdc-runtime-context.py" in package_files else "npm ships runtime helper: no",
        "npm ships Claude hooks: yes" if "hooks/" in package_files else "npm ships Claude hooks: no",
        "Codex pack ships runtime helper: yes" if '"scripts/sdc-runtime-context.py"' in packager else "Codex pack ships runtime helper: no",
        "Codex pack excludes hooks: yes" if '"hooks"' not in packager.split("PAYLOAD_ENTRIES", 1)[1].split(")", 1)[0] else "Codex pack excludes hooks: no",
        "README runtime lifecycle: yes" if "archivable" in readme and "apply-context.jsonl" in readme and "Candidate" in readme else "README runtime lifecycle: no",
        "workspace runtime lifecycle: yes" if "archivable" in workspace_readme and "apply/check JSONL manifests" in workspace_readme else "workspace runtime lifecycle: no",
        "submission client split: yes" if all(marker in submission_lower for marker in ("claude", "sessionstart", "codex", "portable", "sdc_codex_hooks=1")) else "submission client split: no",
        "submission no stale no-hooks claim: yes" if "No default hooks" not in submission else "submission no stale no-hooks claim: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([*checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def source_marketplace_layout_AC_07(root: Path) -> str:
    plugin = json.loads((REPO_ROOT / ".claude-plugin" / "plugin.json").read_text())
    marketplace = json.loads((REPO_ROOT / ".claude-plugin" / "marketplace.json").read_text())
    installer = (REPO_ROOT / "bin" / "install.js").read_text()
    expected_skills = {
        "./skills/sdc-spec",
        "./skills/sdc-implement",
        "./skills/sdc-review",
        "./skills/sdc-test",
        "./skills/sdc-quality",
        "./skills/sdc-validate",
    }
    configured = set(plugin.get("skills", []))
    installer_block = installer.split("function writeLocalClaudeMarketplace", 1)[1].split("function installClaudePlugin", 1)[0]
    checks = [
        "marketplace source is root: yes" if marketplace.get("plugins", [{}])[0].get("source") == "./" else "marketplace source is root: no",
        "explicit advanced source skills: yes" if configured == expected_skills else "explicit advanced source skills: no",
        "configured source paths exist: yes" if all((REPO_ROOT / path.removeprefix("./") / "SKILL.md").is_file() for path in configured) else "configured source paths exist: no",
        "installer keeps root skills: yes" if "includeRootSkills: true" in installer_block else "installer keeps root skills: no",
        "installer omits generated claude layout: yes" if "includeClaudeSkillLayout: false" in installer_block else "installer omits generated claude layout: no",
        "source has no generated claude tree: yes" if not (REPO_ROOT / ".claude" / "skills").exists() else "source has no generated claude tree: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([*checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def lifecycle_state_machine_AC_01(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "runtime-state", "--confirmed-intake")
    change = active_change(root, "runtime-state")
    write_confirmed_change(change, completed=True)
    state_file = change / "state.json"

    get_code, get_output = run_runtime(root, "state", "get", "--change", change.name)
    initial = json.loads(get_output) if get_code == 0 else {}

    first_code, first_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        change.name,
        "--state",
        "confirmed",
        "--source",
        "spec-stage",
        "--evidence",
        "spec.md",
    )
    before_invalid = state_file.read_bytes() if state_file.exists() else b""
    invalid_code, invalid_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        change.name,
        "--state",
        "applying",
        "--source",
        "apply-stage",
        "--evidence",
        "tasks.md",
    )
    after_invalid = state_file.read_bytes() if state_file.exists() else b""

    for role in ("apply", "check"):
        run_runtime(root, "manifest", "generate", "--change", change.name, "--role", role)
    legal_codes = []
    transitions = [
        ("planned", "plan-stage", ("design.md", "tasks.md", "context-pack.md")),
        ("applying", "apply-stage", ("tasks.md", "context-pack.md")),
        ("checking", "apply-stage", ("tasks.md", "notes.md")),
        ("archivable", "check-stage", ("tasks.md", "notes.md")),
    ]
    for next_state, source, evidence in transitions:
        args = ["state", "set", "--change", change.name, "--state", next_state, "--source", source]
        for path in evidence:
            args.extend(["--evidence", path])
        code, _ = run_runtime(root, *args)
        legal_codes.append(code)

    final_code, final_output = run_runtime(root, "state", "get", "--change", change.name)
    final = json.loads(final_output) if final_code == 0 else {}
    checks = [
        "initial discovery: yes" if initial.get("state") == "discovery" else "initial discovery: no",
        "schema: yes" if initial.get("schema") == "sdc.change-state/v1" else "schema: no",
        "source provenance: yes" if isinstance(initial.get("source"), dict) else "source provenance: no",
        "legal first transition: yes" if first_code == 0 else "legal first transition: no",
        "invalid jump rejected: yes" if invalid_code != 0 and "invalid transition" in invalid_output.lower() else "invalid jump rejected: no",
        "rejected transition unchanged: yes" if before_invalid == after_invalid else "rejected transition unchanged: no",
        "legal forward chain: yes" if all(code == 0 for code in legal_codes) else "legal forward chain: no",
        "final archivable: yes" if final.get("state") == "archivable" else "final archivable: no",
        "all states known: yes" if set(final.get("states", [])) == {"intake", "discovery", "confirmed", "planned", "applying", "checking", "archivable"} else "all states known: no",
    ]
    expected = get_code == 0 and final_code == 0 and all(check.endswith("yes") for check in checks)
    return "\n".join([get_output, first_output, invalid_output, final_output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def active_change_resolver_AC_02(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "alpha", "--confirmed-intake")
    run_sdc(root, "change", "beta", "--confirmed-intake")
    alpha = active_change(root, "alpha")
    beta = active_change(root, "beta")

    ambiguous_code, ambiguous_output = run_runtime(root, "resolve")
    explicit_code, explicit_output = run_runtime(root, "resolve", "--change", alpha.name)
    env_code, env_output = run_runtime(root, "resolve", env={"SDC_ACTIVE_CHANGE": beta.name})
    invalid_env_code, invalid_env_output = run_runtime(root, "resolve", env={"SDC_ACTIVE_CHANGE": "missing-change"})
    select_code, select_output = run_runtime(root, "select", "--change", alpha.name, "--session-id", "eval-session")
    session_code, session_output = run_runtime(root, "resolve", "--session-id", "eval-session")

    single_root = root / "single"
    single_root.mkdir()
    run_sdc(single_root, "init")
    run_sdc(single_root, "change", "only", "--confirmed-intake")
    only = active_change(single_root, "only")
    single_code, single_output = run_runtime(single_root, "resolve")

    empty_root = root / "empty"
    empty_root.mkdir()
    run_sdc(empty_root, "init")
    empty_code, empty_output = run_runtime(empty_root, "resolve")

    explicit = json.loads(explicit_output) if explicit_code == 0 else {}
    env_result = json.loads(env_output) if env_code == 0 else {}
    session = json.loads(session_output) if session_code == 0 else {}
    single = json.loads(single_output) if single_code == 0 else {}
    checks = [
        "ambiguous rejected: yes" if ambiguous_code != 0 and alpha.name in ambiguous_output and beta.name in ambiguous_output else "ambiguous rejected: no",
        "explicit wins: yes" if explicit.get("change_id") == alpha.name else "explicit wins: no",
        "env selector: yes" if env_result.get("change_id") == beta.name else "env selector: no",
        "invalid env stops: yes" if invalid_env_code != 0 and "missing-change" in invalid_env_output else "invalid env stops: no",
        "session pointer written: yes" if select_code == 0 and "active-change.json" in select_output else "session pointer written: no",
        "session pointer resolves: yes" if session.get("change_id") == alpha.name else "session pointer resolves: no",
        "single active resolves: yes" if single.get("change_id") == only.name else "single active resolves: no",
        "zero active rejected: yes" if empty_code != 0 and "no active changes" in empty_output.lower() else "zero active rejected: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([
        ambiguous_output,
        explicit_output,
        env_output,
        invalid_env_output,
        select_output,
        session_output,
        single_output,
        empty_output,
        *checks,
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def unsafe_active_change_symlink_AC_02(root: Path) -> str:
    run_sdc(root, "init")
    outside = root / "outside-change"
    outside.mkdir()
    active = root / ".sdc" / "changes" / "active"
    active.joinpath("escape").symlink_to(outside, target_is_directory=True)

    resolve_code, resolve_output = run_runtime(root, "resolve", "--change", "escape")
    state_code, state_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        "escape",
        "--state",
        "discovery",
        "--source",
        "eval",
        "--evidence",
        "discovery.md",
    )
    checks = [
        "unsafe resolve rejected: yes" if resolve_code != 0 and "unsafe" in resolve_output.lower() else "unsafe resolve rejected: no",
        "unsafe state rejected: yes" if state_code != 0 and "unsafe" in state_output.lower() else "unsafe state rejected: no",
        "outside state untouched: yes" if not (outside / "state.json").exists() else "outside state untouched: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([resolve_output, state_output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def unsafe_runtime_ancestor_symlinks_AC_02(root: Path) -> str:
    active_project = root / "active-project"
    active_project.mkdir()
    run_sdc(active_project, "init")
    active = active_project / ".sdc" / "changes" / "active"

    runtime_project = root / "runtime-project"
    runtime_project.mkdir()
    run_sdc(runtime_project, "init")
    run_sdc(runtime_project, "change", "runtime-link", "--confirmed-intake")
    runtime_change = active_change(runtime_project, "runtime-link")

    sdc_project = root / "sdc-project"
    sdc_project.mkdir()

    with tempfile.TemporaryDirectory(prefix="sdc-outside-active-", dir=root.parent) as outside_active_value, tempfile.TemporaryDirectory(
        prefix="sdc-outside-runtime-", dir=root.parent
    ) as outside_runtime_value, tempfile.TemporaryDirectory(prefix="sdc-outside-workspace-", dir=root.parent) as outside_workspace_value:
        outside_active = Path(outside_active_value)
        outside_active.joinpath("escape").mkdir()
        outside_active.joinpath("escape", "discovery.md").write_text("# Discovery\n")
        active.rmdir()
        active.symlink_to(outside_active, target_is_directory=True)

        active_code, active_output = run_runtime(active_project, "resolve", "--change", "escape")

        outside_runtime = Path(outside_runtime_value)
        runtime_path = runtime_project / ".sdc" / "runtime"
        runtime_path.rmdir()
        runtime_path.symlink_to(outside_runtime, target_is_directory=True)
        select_code, select_output = run_runtime(
            runtime_project,
            "select",
            "--change",
            runtime_change.name,
            "--session-id",
            "unsafe-session",
        )
        research_code, research_output = run_runtime(
            runtime_project,
            "research",
            "route",
            "--change",
            runtime_change.name,
            "--stage",
            "apply",
            "--title",
            "unsafe research",
        )
        evidence_code, evidence_output = run_runtime(
            runtime_project,
            "evidence",
            "append",
            "--change",
            runtime_change.name,
            "--stage",
            "apply",
            "--command",
            "pytest",
            "--status",
            "passed",
        )

        outside_workspace = Path(outside_workspace_value)
        run_sdc(outside_workspace, "init")
        run_sdc(outside_workspace, "change", "outside", "--confirmed-intake")
        sdc_project.joinpath(".sdc").symlink_to(outside_workspace / ".sdc", target_is_directory=True)
        sdc_code, sdc_output = run_runtime(sdc_project, "resolve")

        checks = [
            "symlinked active root rejected: yes" if active_code != 0 and "unsafe" in active_output.lower() else "symlinked active root rejected: no",
            "symlinked runtime select rejected: yes" if select_code != 0 and "unsafe" in select_output.lower() else "symlinked runtime select rejected: no",
            "symlinked runtime research rejected: yes" if research_code != 0 and "unsafe" in research_output.lower() else "symlinked runtime research rejected: no",
            "symlinked runtime evidence rejected: yes" if evidence_code != 0 and "unsafe" in evidence_output.lower() else "symlinked runtime evidence rejected: no",
            "outside runtime untouched: yes" if not any(outside_runtime.rglob("*")) else "outside runtime untouched: no",
            "symlinked workspace rejected: yes" if sdc_code != 0 and "unsafe" in sdc_output.lower() else "symlinked workspace rejected: no",
        ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([
        active_output,
        select_output,
        research_output,
        evidence_output,
        sdc_output,
        *checks,
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def explicit_empty_selector_AC_02(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "only", "--confirmed-intake")
    code, output = run_runtime(root, "resolve", "--change", "", env={"SDC_ACTIVE_CHANGE": ""})
    expected = code != 0 and "invalid" in output.lower() and "change id" in output.lower()
    return "\n".join([
        output,
        "explicit empty rejected: yes" if expected else "explicit empty rejected: no",
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def lifecycle_evidence_gate_AC_01(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "evidence-gate", "--confirmed-intake")
    change = active_change(root, "evidence-gate")
    write_confirmed_change(change)
    state_file = change / "state.json"
    original = state_file.read_bytes()

    no_evidence_code, no_evidence_output = run_runtime(
        root, "state", "set", "--change", change.name, "--state", "confirmed", "--source", "spec-stage"
    )
    wrong_source_code, wrong_source_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        change.name,
        "--state",
        "confirmed",
        "--source",
        "manual",
        "--evidence",
        "spec.md",
    )
    missing_code, missing_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        change.name,
        "--state",
        "confirmed",
        "--source",
        "spec-stage",
        "--evidence",
        "missing.md",
    )
    escaping_code, escaping_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        change.name,
        "--state",
        "confirmed",
        "--source",
        "spec-stage",
        "--evidence",
        "../../outside.md",
    )
    unchanged = state_file.read_bytes() == original
    valid_code, valid_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        change.name,
        "--state",
        "confirmed",
        "--source",
        "spec-stage",
        "--evidence",
        "spec.md",
    )
    state_file.write_text(
        json.dumps(
            {
                "schema": "sdc.change-state/v1",
                "change_id": change.name,
                "state": "confirmed",
                "updated_at": "not-a-timestamp",
                "source": {"kind": "spec-stage"},
            }
        )
    )
    malformed_code, malformed_output = run_runtime(root, "state", "get", "--change", change.name)
    checks = [
        "empty evidence rejected: yes" if no_evidence_code != 0 else "empty evidence rejected: no",
        "wrong source rejected: yes" if wrong_source_code != 0 else "wrong source rejected: no",
        "missing evidence rejected: yes" if missing_code != 0 else "missing evidence rejected: no",
        "escaping evidence rejected: yes" if escaping_code != 0 else "escaping evidence rejected: no",
        "rejected transitions unchanged: yes" if unchanged else "rejected transitions unchanged: no",
        "valid evidence accepted: yes" if valid_code == 0 else "valid evidence accepted: no",
        "malformed state rejected: yes" if malformed_code != 0 and "invalid-state" in malformed_output else "malformed state rejected: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([
        no_evidence_output,
        wrong_source_output,
        missing_output,
        escaping_output,
        valid_output,
        malformed_output,
        *checks,
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def archive_requires_archivable_state_AC_01(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "archive-state", "--confirmed-intake")
    change = active_change(root, "archive-state")
    write_confirmed_change(change, completed=True)
    code, output = run_sdc(root, "archive", change.name)
    stable_spec = root / ".sdc" / "specs" / f"{change.name}.md"
    checks = [
        "non-archivable rejected: yes" if code != 0 and "archivable" in output else "non-archivable rejected: no",
        "active change preserved: yes" if change.exists() else "active change preserved: no",
        "stable spec untouched: yes" if not stable_spec.exists() else "stable spec untouched: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def runtime_contract_templates_AC_07(root: Path) -> str:
    init_code, init_output = run_sdc(root, "init")
    run_sdc(root, "change", "runtime-contract", "--confirmed-intake")
    change = active_change(root, "runtime-contract")
    initial_state_path = change / "state.json"
    initial_state = json.loads(initial_state_path.read_text()) if initial_state_path.exists() else {}
    initial_state_path.unlink(missing_ok=True)
    state_code, state_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        change.name,
        "--state",
        "discovery",
        "--source",
        "change-stage",
        "--evidence",
        "discovery.md",
    )

    contract = root / ".sdc" / "templates" / "runtime-context.md"
    contract_text = contract.read_text() if contract.exists() else ""
    existing_file = change / "user-owned.md"
    existing_file.write_text("user-owned active artifact\n")
    before_active = tree_digest(root, f".sdc/changes/active/{change.name}")
    rerun_code, rerun_output = run_sdc(root, "init")
    after_active = tree_digest(root, f".sdc/changes/active/{change.name}")

    custom_root = root / "custom"
    custom_contract = custom_root / ".sdc" / "templates" / "runtime-context.md"
    custom_contract.parent.mkdir(parents=True)
    custom_bytes = b"# Team Runtime Contract\n\nKeep this custom content.\n"
    custom_contract.write_bytes(custom_bytes)
    custom_code, custom_output = run_sdc(custom_root, "init")

    schemas = (REPO_ROOT / "sdc-references" / "artifact-schemas.md").read_text()
    workflow = (REPO_ROOT / "sdc-references" / "workflow-manifest.yaml").read_text()
    command_text = "\n".join(
        (REPO_ROOT / "commands" / name).read_text()
        for name in ("change.md", "plan.md", "apply.md", "check.md")
    )
    schema_markers = (
        "sdc.change-state/v1",
        "sdc.session-pointer/v1",
        "sdc.context-manifest-record/v1",
        "sdc.recall-result/v1",
        "sdc.research-route/v1",
        "sdc.session-context/v1",
        "sdc.evidence-record/v1",
    )
    checks = [
        "runtime template created: yes" if contract.exists() else "runtime template created: no",
        "runtime template managed: yes" if contract_text.startswith("<!-- SDC-MANAGED path=templates/runtime-context.md;") else "runtime template managed: no",
        "runtime template schemas: yes" if all(marker in contract_text for marker in schema_markers) else "runtime template schemas: no",
        "cli discovery state: yes" if initial_state.get("schema") == "sdc.change-state/v1" and initial_state.get("state") == "discovery" else "cli discovery state: no",
        "state materialized: yes" if state_code == 0 and (change / "state.json").exists() else "state materialized: no",
        "active artifacts preserved: yes" if before_active == after_active else "active artifacts preserved: no",
        "custom template preserved: yes" if custom_contract.read_bytes() == custom_bytes else "custom template preserved: no",
        "reference schemas complete: yes" if all(marker in schemas for marker in schema_markers) else "reference schemas complete: no",
        "workflow runtime mapping: yes" if "runtime_contract:" in workflow and "state_transition:" in workflow else "workflow runtime mapping: no",
        "stage commands mapped: yes" if all(marker in command_text for marker in ("--state discovery", "--state planned", "--state applying", "--state checking", "--state archivable")) else "stage commands mapped: no",
    ]
    expected = init_code == 0 and rerun_code == 0 and custom_code == 0 and all(check.endswith("yes") for check in checks)
    return "\n".join([
        init_output,
        state_output,
        rerun_output,
        custom_output,
        *checks,
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def role_context_manifests_AC_03(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "manifest", "--confirmed-intake")
    change = active_change(root, "manifest")
    write_confirmed_change(change)

    apply_first_code, apply_first_output = run_runtime(root, "manifest", "generate", "--change", change.name, "--role", "apply")
    apply_path = change / "apply-context.jsonl"
    apply_first = apply_path.read_bytes() if apply_path.exists() else b""
    apply_second_code, apply_second_output = run_runtime(root, "manifest", "generate", "--change", change.name, "--role", "apply")
    apply_second = apply_path.read_bytes() if apply_path.exists() else b""

    check_first_code, check_first_output = run_runtime(root, "manifest", "generate", "--change", change.name, "--role", "check")
    check_path = change / "check-context.jsonl"
    check_first = check_path.read_bytes() if check_path.exists() else b""
    check_second_code, check_second_output = run_runtime(root, "manifest", "generate", "--change", change.name, "--role", "check")
    check_second = check_path.read_bytes() if check_path.exists() else b""

    required_order = [
        "schema",
        "manifest",
        "change_id",
        "role",
        "order",
        "path",
        "section",
        "purpose",
        "required",
        "source_type",
        "sha256",
    ]
    records = [json.loads(line) for line in apply_second.decode().splitlines() if line.strip()]
    first_record_keys = list(records[0].keys()) if records else []
    root_resolved = root.resolve()
    path_safe = all(
        not Path(record["path"]).is_absolute()
        and ".." not in Path(record["path"]).parts
        and (root_resolved / record["path"]).resolve().is_relative_to(root_resolved)
        for record in records
    )
    hashes_current = all(
        hashlib.sha256((root / record["path"]).read_bytes()).hexdigest() == record["sha256"]
        for record in records
    )
    roles = {record["role"] for record in records}

    spec = change / "spec.md"
    saved_spec = spec.read_text()
    spec.unlink()
    before_missing = apply_path.read_bytes() if apply_path.exists() else b""
    missing_code, missing_output = run_runtime(root, "manifest", "generate", "--change", change.name, "--role", "apply")
    after_missing = apply_path.read_bytes() if apply_path.exists() else b""
    spec.write_text(saved_spec)

    checks = [
        "apply command: yes" if apply_first_code == 0 and apply_second_code == 0 else "apply command: no",
        "check command: yes" if check_first_code == 0 and check_second_code == 0 else "check command: no",
        "apply stable bytes: yes" if apply_first == apply_second and apply_second else "apply stable bytes: no",
        "check stable bytes: yes" if check_first == check_second and check_second else "check stable bytes: no",
        "field order: yes" if first_record_keys == required_order else "field order: no",
        "role specific: yes" if roles == {"apply"} and apply_second != check_second else "role specific: no",
        "path safe: yes" if path_safe else "path safe: no",
        "hashes current: yes" if hashes_current else "hashes current: no",
        "missing required rejected: yes" if missing_code != 0 and "spec.md" in missing_output else "missing required rejected: no",
        "failed write unchanged: yes" if before_missing == after_missing else "failed write unchanged: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([
        apply_first_output,
        apply_second_output,
        check_first_output,
        check_second_output,
        missing_output,
        *checks,
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def memory_recall_candidate_AC_04(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "recall", "--confirmed-intake")
    change = active_change(root, "recall")
    write_confirmed_change(change)
    root.joinpath(".sdc/memory/candidates.md").write_text(
        "# Memory Candidates\n\nDeterministic recall alpha alpha belongs to memory only.\n"
    )
    root.joinpath(".sdc/knowledge/product/rules.md").write_text(
        "# Business Rules\n\nAlpha booking rule is still a candidate until archive.\n"
    )
    root.joinpath(".sdc/memory/token-notes.md").write_text(
        "# Token Notes\n\nalpha secret-token-value must not be recalled.\n"
    )
    runtime_secret = root / ".sdc/runtime/secret.md"
    runtime_secret.parent.mkdir(parents=True, exist_ok=True)
    runtime_secret.write_text("alpha secret token should not be recalled\n")

    before_digest = tree_digest(root, ".sdc")
    first_code, first_output = run_runtime(root, "recall", "--change", change.name, "--query", "alpha", "--limit", "5")
    after_first_digest = tree_digest(root, ".sdc")
    second_code, second_output = run_runtime(root, "recall", "--change", change.name, "--query", "alpha", "--limit", "5")
    limited_code, limited_output = run_runtime(root, "recall", "--change", change.name, "--query", "alpha", "--limit", "1")
    after_second_digest = tree_digest(root, ".sdc")

    records = [json.loads(line) for line in first_output.splitlines() if line.strip().startswith("{")]
    limited_records = [json.loads(line) for line in limited_output.splitlines() if line.strip().startswith("{")]
    checks = [
        "recall command: yes" if first_code == 0 and second_code == 0 and limited_code == 0 else "recall command: no",
        "deterministic: yes" if first_output == second_output else "deterministic: no",
        "candidate only: yes" if records and all(record.get("status") == "Candidate" for record in records) else "candidate only: no",
        "bounded: yes" if len(limited_records) == 1 else "bounded: no",
        "runtime excluded: yes" if ".sdc/runtime" not in first_output and "secret token" not in first_output else "runtime excluded: no",
        "secret excluded: yes" if "secret-token-value" not in first_output and "token-notes.md" not in first_output else "secret excluded: no",
        "read only: yes" if before_digest == after_first_digest == after_second_digest else "read only: no",
        "local paths: yes" if records and all(record.get("path", "").startswith(".sdc/") for record in records) else "local paths: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([first_output, second_output, limited_output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def recall_redacts_adjacent_sensitive_lines_AC_04(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "recall-redaction", "--confirmed-intake")
    change = active_change(root, "recall-redaction")
    memory = root / ".sdc" / "memory" / "adjacent-lines.md"
    memory.write_text(
        "# Adjacent Lines\n\nBooking workflow evidence is still a Candidate.\npassword=LEAK-ME-NOW\n"
    )
    code, output = run_runtime(
        root, "recall", "--change", change.name, "--query", "booking", "--limit", "5"
    )
    checks = [
        "matching candidate retained: yes" if code == 0 and "Booking workflow" in output and "Candidate" in output else "matching candidate retained: no",
        "adjacent secret redacted: yes" if "LEAK-ME-NOW" not in output and "password=" not in output else "adjacent secret redacted: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def research_routing_no_public_command_AC_05(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "research", "--confirmed-intake")
    change = active_change(root, "research")
    write_confirmed_change(change)

    route_code, route_output = run_runtime(root, "research", "route", "--change", change.name, "--stage", "plan", "--title", "trellis-public-summary")
    route = json.loads(route_output) if route_code == 0 else {}
    command_files = sorted(path.name for path in (REPO_ROOT / "commands").glob("*.md"))
    reference = (REPO_ROOT / "sdc-references" / "runtime-context.md").read_text() if (REPO_ROOT / "sdc-references" / "runtime-context.md").exists() else ""
    role_contracts = (REPO_ROOT / "sdc-references" / "role-contracts.md").read_text()
    workflow = (REPO_ROOT / "sdc-references" / "workflow-standards.md").read_text()
    expert = (REPO_ROOT / "sdc-references" / "expert-routing.md").read_text()
    apply_command = (REPO_ROOT / "commands" / "apply.md").read_text()
    checks = [
        "route command: yes" if route_code == 0 else "route command: no",
        "scratch boundary: yes" if route.get("scratch", "").endswith("/research/trellis-public-summary.md") else "scratch boundary: no",
        "citation boundary: yes" if route.get("citation") in {"discovery.md", "notes.md"} else "citation boundary: no",
        "candidate boundary: yes" if route.get("durable_candidate") == "knowledge-candidates.md" else "candidate boundary: no",
        "scratch file exists: yes" if route.get("scratch") and (root / route["scratch"]).exists() else "scratch file exists: no",
        "no public command: yes" if "research.md" not in command_files else "no public command: no",
        "reference documents route: yes" if all("research" in text.lower() and "knowledge-candidates" in text for text in [reference, role_contracts, workflow, expert]) else "reference documents route: no",
        "apply routes candidates: yes" if "Candidate" in apply_command and ".sdc/runtime/<change-id>/research/" in apply_command and "knowledge-candidates.md" in apply_command else "apply routes candidates: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([route_output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def session_context_adapter_and_evidence_AC_06(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "session-context", "--confirmed-intake")
    change = active_change(root, "session-context")
    write_confirmed_change(change)
    root.joinpath(".sdc/memory/candidates.md").write_text(
        "# Memory Candidates\n\nAlpha session context reminder remains Candidate until archive.\n"
    )
    run_runtime(root, "manifest", "generate", "--change", change.name, "--role", "apply")
    run_runtime(root, "manifest", "generate", "--change", change.name, "--role", "check")

    codex_code, codex_output = run_runtime(
        root,
        "session-context",
        "--client",
        "codex",
        "--session-id",
        "eval-session",
        "--change",
        change.name,
        "--query",
        "alpha",
    )
    claude_code, claude_output = run_runtime(
        root,
        "session-context",
        "--client",
        "claude",
        "--session-id",
        "eval-session",
        "--change",
        change.name,
        "--query",
        "alpha",
    )
    run_sdc(root, "change", "ambiguous-context", "--confirmed-intake")
    ambiguous_code, ambiguous_output = run_runtime(root, "session-context", "--client", "codex", "--session-id", "eval-session-2")

    before_evidence = tree_digest(root, ".sdc/runtime")
    evidence_code, evidence_output = run_runtime(
        root,
        "evidence",
        "append",
        "--change",
        change.name,
        "--session-id",
        "eval-session",
        "--stage",
        "apply",
        "--command",
        "npm run eval:sdc",
        "--status",
        "passed",
        "--path",
        f".sdc/changes/active/{change.name}/notes.md",
    )
    evidence_path = root / ".sdc" / "runtime" / change.name / "evidence.jsonl"
    evidence_records = [json.loads(line) for line in evidence_path.read_text().splitlines()] if evidence_path.exists() else []
    evidence_after_valid = evidence_path.read_bytes() if evidence_path.exists() else b""
    invalid_evidence_code, invalid_evidence_output = run_runtime(
        root,
        "evidence",
        "append",
        "--change",
        change.name,
        "--session-id",
        "eval-session",
        "--stage",
        "invalid",
        "--command",
        "npm run eval:sdc",
        "--status",
        "passed",
    )
    evidence_after_invalid = evidence_path.read_bytes() if evidence_path.exists() else b""

    codex = json.loads(codex_output) if codex_code == 0 else {}
    claude = json.loads(claude_output) if claude_code == 0 else {}
    claude_hook = claude.get("hookSpecificOutput", {})
    codex_context = codex.get("additionalContext", "")
    claude_context = claude_hook.get("additionalContext", "")
    latest_evidence = evidence_records[-1] if evidence_records else {}
    checks = [
        "codex adapter command: yes" if codex_code == 0 else "codex adapter command: no",
        "codex adapter shape: yes" if codex.get("schema") == "sdc.session-context/v1" and "hookSpecificOutput" not in codex else "codex adapter shape: no",
        "codex context bounded: yes" if change.name in codex_context and "Candidate" in codex_context and "apply-context.jsonl" in codex_context else "codex context bounded: no",
        "claude hook command: yes" if claude_code == 0 else "claude hook command: no",
        "claude hook shape: yes" if claude_hook.get("hookEventName") == "SessionStart" and "additionalContext" not in claude else "claude hook shape: no",
        "claude context bounded: yes" if change.name in claude_context and "Candidate" in claude_context else "claude context bounded: no",
        "ambiguous adapter rejected: yes" if ambiguous_code != 0 and "ambiguous-active-change" in ambiguous_output else "ambiguous adapter rejected: no",
        "evidence append command: yes" if evidence_code == 0 and evidence_path.exists() else "evidence append command: no",
        "evidence runtime scoped: yes" if latest_evidence.get("path", "").startswith(".sdc/changes/active/") and str(evidence_path.relative_to(root)).startswith(".sdc/runtime/") else "evidence runtime scoped: no",
        "evidence schema: yes" if latest_evidence.get("schema") == "sdc.evidence-record/v1" and latest_evidence.get("stage") == "apply" else "evidence schema: no",
        "invalid evidence rejected: yes" if invalid_evidence_code != 0 and evidence_after_valid == evidence_after_invalid else "invalid evidence rejected: no",
        "runtime changed only on evidence: yes" if before_evidence != tree_digest(root, ".sdc/runtime") else "runtime changed only on evidence: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([
        codex_output,
        claude_output,
        ambiguous_output,
        evidence_output,
        invalid_evidence_output,
        *checks,
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def hook_files_and_installer_boundaries_AC_07(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "hook-context", "--confirmed-intake")
    change = active_change(root, "hook-context")
    write_confirmed_change(change)

    hooks_json = REPO_ROOT / "hooks" / "hooks.json"
    hook_script = REPO_ROOT / "hooks" / "session-start"
    hooks_payload = json.loads(hooks_json.read_text()) if hooks_json.exists() else {}
    hook_entries = hooks_payload.get("hooks", {}).get("SessionStart", [])

    hook_env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(root / "home"),
        "CLAUDE_PLUGIN_ROOT": str(REPO_ROOT),
        "SDC_ACTIVE_CHANGE": change.name,
    }
    hook_result = subprocess.run(
        [str(hook_script)],
        cwd=root,
        env=hook_env,
        input=json.dumps({"session_id": "stdin-hook-session", "hook_event_name": "SessionStart"}),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) if hook_script.exists() else subprocess.CompletedProcess([str(hook_script)], 127, "", "missing hook script")
    malformed_result = subprocess.run(
        [str(hook_script)],
        cwd=root,
        env=hook_env,
        input="{",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) if hook_script.exists() else subprocess.CompletedProcess([str(hook_script)], 127, "", "missing hook script")
    empty_result = subprocess.run(
        [str(hook_script)],
        cwd=root,
        env=hook_env,
        input="",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) if hook_script.exists() else subprocess.CompletedProcess([str(hook_script)], 127, "", "missing hook script")
    forced_env = {**hook_env, "SDC_RUNTIME_FORCE_HOOK_FAILURE": "1"}
    forced_result = subprocess.run(
        [str(hook_script)],
        cwd=root,
        env=forced_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) if hook_script.exists() else subprocess.CompletedProcess([str(hook_script)], 127, "", "missing hook script")

    hook_payload = json.loads(hook_result.stdout) if hook_result.returncode == 0 else {}
    malformed_payload = json.loads(malformed_result.stdout) if malformed_result.returncode == 0 else {}
    empty_payload = json.loads(empty_result.stdout) if empty_result.returncode == 0 else {}
    forced_payload = json.loads(forced_result.stdout) if forced_result.returncode == 0 else {}
    hook_context = hook_payload.get("hookSpecificOutput", {}).get("additionalContext", "")
    forced_context = forced_payload.get("hookSpecificOutput", {}).get("additionalContext", "")

    install_home = root / "install-home"
    install_home.joinpath(".claude", "plugins").mkdir(parents=True)
    install_home.joinpath(".codex", "plugins").mkdir(parents=True)
    install_env = {**os.environ, "HOME": str(install_home), "USERPROFILE": str(install_home), "PATH": os.environ.get("PATH", "")}
    install_result = subprocess.run(
        ["node", str(INSTALLER)],
        cwd=REPO_ROOT,
        env=install_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    claude_marketplace = install_home / ".claude" / "plugins" / "marketplaces" / "sdc-local"
    codex_marketplace = install_home / ".codex" / "local-marketplaces" / "sdc-local" / "plugins" / "sdc"
    codex_cache = install_home / ".codex" / "plugins" / "cache" / "sdc-local" / "sdc" / json.loads((REPO_ROOT / "package.json").read_text())["version"]
    codex_manifest = json.loads((codex_marketplace / ".codex-plugin" / "plugin.json").read_text()) if (codex_marketplace / ".codex-plugin" / "plugin.json").exists() else {}
    checks = [
        "hooks file exists: yes" if hooks_json.exists() and hook_script.exists() else "hooks file exists: no",
        "hooks sessionstart command: yes" if hook_entries and "session-start" in json.dumps(hook_entries) else "hooks sessionstart command: no",
        "hook executable: yes" if hook_script.exists() and os.access(hook_script, os.X_OK) else "hook executable: no",
        "hook output shape: yes" if hook_payload.get("hookSpecificOutput", {}).get("hookEventName") == "SessionStart" and change.name in hook_context else "hook output shape: no",
        "stdin session id: yes" if "Session id: stdin-hook-session" in hook_context else "stdin session id: no",
        "malformed stdin safe: yes" if malformed_result.returncode == 0 and malformed_payload.get("hookSpecificOutput", {}).get("hookEventName") == "SessionStart" else "malformed stdin safe: no",
        "empty stdin safe: yes" if empty_result.returncode == 0 and empty_payload.get("hookSpecificOutput", {}).get("hookEventName") == "SessionStart" else "empty stdin safe: no",
        "forced hook fallback: yes" if forced_result.returncode == 0 and "manual" in forced_context.lower() else "forced hook fallback: no",
        "installer command: yes" if install_result.returncode == 0 else "installer command: no",
        "claude hooks installed: yes" if (claude_marketplace / "hooks" / "hooks.json").exists() and (claude_marketplace / "hooks" / "session-start").exists() else "claude hooks installed: no",
        "claude source skills installed: yes" if (claude_marketplace / "skills" / "sdc-spec" / "SKILL.md").exists() else "claude source skills installed: no",
        "claude generated skills omitted: yes" if not (claude_marketplace / ".claude" / "skills").exists() else "claude generated skills omitted: no",
        "codex hooks omitted: yes" if not (codex_marketplace / "hooks").exists() and not (codex_cache / "hooks").exists() else "codex hooks omitted: no",
        "codex manifest omits hooks: yes" if "hooks" not in codex_manifest else "codex manifest omits hooks: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([
        hook_result.stdout,
        malformed_result.stdout,
        empty_result.stdout,
        forced_result.stdout,
        install_result.stdout,
        *checks,
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def hook_requires_trustworthy_session_id_AC_06(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "hook-alpha", "--confirmed-intake")
    run_sdc(root, "change", "hook-beta", "--confirmed-intake")
    alpha = active_change(root, "hook-alpha")
    select_code, select_output = run_runtime(
        root, "select", "--change", alpha.name, "--session-id", "claude-session"
    )
    hook_script = REPO_ROOT / "hooks" / "session-start"
    hook_env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(root / "home"),
        "CLAUDE_PLUGIN_ROOT": str(REPO_ROOT),
    }
    result = subprocess.run(
        [str(hook_script)],
        cwd=root,
        env=hook_env,
        input="{}",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    payload = json.loads(result.stdout) if result.returncode == 0 else {}
    context = payload.get("hookSpecificOutput", {}).get("additionalContext", "")
    checks = [
        "stale default pointer prepared: yes" if select_code == 0 and "active-change.json" in select_output else "stale default pointer prepared: no",
        "missing session id falls back: yes" if result.returncode == 0 and "runtime context unavailable" in context.lower() else "missing session id falls back: no",
        "stale pointer not reused: yes" if alpha.name not in context else "stale pointer not reused: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([select_output, result.stdout, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def standards_pack_import(root: Path) -> str:
    source = root / "spec-rules"
    source.mkdir()
    source.joinpath("README.md").write_text("# Source Pack Readme\n\nThis source README should not become an imported rule file.\n")
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
        marker(root, ".sdc/standards/company/README.import-ignored.md"),
        "routing index: yes" if "Agents must read this index first" in index_text else "routing index: no",
        "code hint: yes" if "Read when creating new code scaffolds" in index_text else "code hint: no",
        "source readme skipped: yes" if "Source Pack Readme" not in index_text else "source readme skipped: no",
        "path leak: no" if str(source) not in index_text else "path leak: yes",
    ]
    import_readmes = list(target.glob("README.import-*.md"))
    expected = (
        code == 0
        and any(check.endswith("code-generation.md: exists") for check in checks)
        and any(check.endswith("testing.md: exists") for check in checks)
        and any(check.endswith(".DS_Store: absent") for check in checks)
        and not import_readmes
        and "routing index: yes" in checks
        and "code hint: yes" in checks
        and "source readme skipped: yes" in checks
        and "path leak: no" in checks
    )
    return "\n".join([output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def lifecycle_content_gates_AC_01(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "content-gates", "--confirmed-intake")
    change = active_change(root, "content-gates")
    write_confirmed_change(change)

    confirmed_code, confirmed_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        change.name,
        "--state",
        "confirmed",
        "--source",
        "spec-stage",
        "--evidence",
        "spec.md",
    )
    for role in ("apply", "check"):
        run_runtime(root, "manifest", "generate", "--change", change.name, "--role", role)
    for state, source, evidence in (
        ("planned", "plan-stage", ("design.md", "tasks.md", "context-pack.md")),
        ("applying", "apply-stage", ("tasks.md", "context-pack.md")),
    ):
        args = ["state", "set", "--change", change.name, "--state", state, "--source", source]
        for filename in evidence:
            args.extend(["--evidence", filename])
        code, output = run_runtime(root, *args)
        if code != 0:
            raise AssertionError(output)

    state_file = change / "state.json"
    applying_state = state_file.read_bytes()
    pending_code, pending_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        change.name,
        "--state",
        "checking",
        "--source",
        "apply-stage",
        "--evidence",
        "tasks.md",
        "--evidence",
        "notes.md",
    )
    pending_unchanged = state_file.read_bytes() == applying_state
    if not pending_unchanged:
        state_file.write_bytes(applying_state)

    write_confirmed_change(change, completed=True)
    checking_code, checking_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        change.name,
        "--state",
        "checking",
        "--source",
        "apply-stage",
        "--evidence",
        "tasks.md",
        "--evidence",
        "notes.md",
    )
    notes = change / "notes.md"
    approved_notes = notes.read_bytes()
    notes.write_text(notes.read_text().replace("- Status: Approved", "- Status: Pending", 1))
    checking_state = state_file.read_bytes()
    unapproved_code, unapproved_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        change.name,
        "--state",
        "archivable",
        "--source",
        "check-stage",
        "--evidence",
        "tasks.md",
        "--evidence",
        "notes.md",
    )
    unapproved_unchanged = state_file.read_bytes() == checking_state
    if not unapproved_unchanged:
        state_file.write_bytes(checking_state)
    notes.write_bytes(approved_notes)
    archivable_code, archivable_output = run_runtime(
        root,
        "state",
        "set",
        "--change",
        change.name,
        "--state",
        "archivable",
        "--source",
        "check-stage",
        "--evidence",
        "tasks.md",
        "--evidence",
        "notes.md",
    )
    checks = [
        "confirmed accepted: yes" if confirmed_code == 0 else "confirmed accepted: no",
        "pending tasks rejected: yes" if pending_code != 0 else "pending tasks rejected: no",
        "pending rejection unchanged: yes" if pending_unchanged else "pending rejection unchanged: no",
        "completed tasks enter checking: yes" if checking_code == 0 else "completed tasks enter checking: no",
        "unapproved final review rejected: yes" if unapproved_code != 0 else "unapproved final review rejected: no",
        "review rejection unchanged: yes" if unapproved_unchanged else "review rejection unchanged: no",
        "approved delivery archivable: yes" if archivable_code == 0 else "approved delivery archivable: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([
        confirmed_output,
        pending_output,
        checking_output,
        unapproved_output,
        archivable_output,
        *checks,
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def archive_rejects_forged_state_AC_01(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "forged-state", "--confirmed-intake")
    change = active_change(root, "forged-state")
    write_confirmed_change(change)
    state_file = change / "state.json"
    state_file.write_text(
        json.dumps(
            {
                "schema": "sdc.change-state/v1",
                "change_id": change.name,
                "state": "archivable",
                "updated_at": "2026-08-26T00:00:00Z",
                "source": {"kind": "check-stage", "paths": ["tasks.md", "notes.md"]},
            }
        )
    )
    state_code, state_output = run_runtime(root, "state", "get", "--change", change.name)
    code, output = run_sdc(root, "archive", change.name)
    checks = [
        "forged state read rejected: yes" if state_code != 0 else "forged state read rejected: no",
        "forged state rejected: yes" if code != 0 else "forged state rejected: no",
        "active change preserved: yes" if change.exists() else "active change preserved: no",
        "stable spec untouched: yes" if not (root / ".sdc/specs" / f"{change.name}.md").exists() else "stable spec untouched: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([state_output, output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def public_cli_symlink_boundaries_AC_02(root: Path) -> str:
    active_case = root / "active-case"
    archive_case = root / "archive-case"
    active_case.mkdir()
    archive_case.mkdir()

    run_sdc(active_case, "init")
    active_root = active_case / ".sdc/changes/active"
    outside_active = root / "outside-active"
    outside_active.mkdir()
    outside_change = outside_active / "linked-change"
    outside_change.mkdir()
    write_confirmed_change(outside_change, completed=True)
    outside_change.joinpath("state.json").write_text(
        json.dumps(
            {
                "schema": "sdc.change-state/v1",
                "change_id": "linked-change",
                "state": "archivable",
                "updated_at": "2026-08-26T00:00:00Z",
                "source": {"kind": "check-stage", "paths": ["tasks.md", "notes.md"]},
            }
        )
    )
    (active_root / "linked-change").symlink_to(outside_change, target_is_directory=True)
    active_code, active_output = run_sdc(active_case, "archive", "linked-change")

    run_sdc(archive_case, "init")
    run_sdc(archive_case, "change", "archive-link", "--confirmed-intake")
    change = active_change(archive_case, "archive-link")
    write_confirmed_change(change, completed=True)
    advance_change_to_archivable(archive_case, change)
    archive_root = archive_case / ".sdc/changes/archive"
    archive_root.rmdir()
    outside_archive = root / "outside-archive"
    outside_archive.mkdir()
    archive_root.symlink_to(outside_archive, target_is_directory=True)
    archive_code, archive_output = run_sdc(archive_case, "archive", change.name)

    checks = [
        "active symlink rejected: yes" if active_code != 0 else "active symlink rejected: no",
        "outside active untouched: yes" if not (outside_change / "archive.md").exists() else "outside active untouched: no",
        "archive root symlink rejected: yes" if archive_code != 0 else "archive root symlink rejected: no",
        "outside archive untouched: yes" if not any(outside_archive.iterdir()) else "outside archive untouched: no",
        "archive source preserved: yes" if change.exists() else "archive source preserved: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([active_output, archive_output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def recall_root_containment_AC_04(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "recall-containment", "--confirmed-intake")
    change = active_change(root, "recall-containment")
    write_confirmed_change(change)
    root.joinpath(".sdc/knowledge/product/safe.md").write_text(
        "# Safe Candidate\n\nneedle-safe legitimate Candidate evidence.\n"
    )
    private_root = root / ".sdc/private"
    private_root.mkdir()
    private_root.joinpath("private.md").write_text(
        "# Private\n\nneedle-safe INTERNAL-PRIVATE-VALUE must not be recalled.\n"
    )
    memory_root = root / ".sdc/memory"
    shutil.rmtree(memory_root)
    memory_root.symlink_to(private_root, target_is_directory=True)
    with tempfile.TemporaryDirectory(prefix="sdc-external-recall-") as external_value:
        external = Path(external_value) / "external.md"
        external.write_text("needle-safe EXTERNAL-PRIVATE-VALUE must not be recalled.\n")
        root.joinpath(".sdc/knowledge/product/external.md").symlink_to(external)
        code, output = run_runtime(
            root, "recall", "--change", change.name, "--query", "needle-safe", "--limit", "10"
        )
    checks = [
        "safe recall retained: yes" if code == 0 and "legitimate Candidate" in output else "safe recall retained: no",
        "internal symlink excluded: yes" if "INTERNAL-PRIVATE-VALUE" not in output else "internal symlink excluded: no",
        "external symlink excluded: yes" if "EXTERNAL-PRIVATE-VALUE" not in output else "external symlink excluded: no",
        "resolved private path excluded: yes" if ".sdc/private" not in output else "resolved private path excluded: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


def sensitive_runtime_values_AC_04(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "sensitive-values", "--confirmed-intake")
    change = active_change(root, "sensitive-values")
    write_confirmed_change(change)
    raw_token = "sk-live-A1b2C3d4E5f6G7h8"
    high_entropy = "aB3dE6fG8hJ1kL3mN5pQ7rS9tV2xY4z6"
    lowercase_entropy = "qjvowmxncbalksdfueirhtgypzqwmncvbalskdfu"
    numeric_entropy = "907314628509173462850917346285091734"
    hex_entropy = "9f3a7c1e5b8d2a6f0c4e9b7d1a5f8c2e6b0d4a9f3c7e1b5d8a2f6c0e4b9d7a1f"
    safe_long_text = "meetingroomreservationworkflowdocumentation"
    root.joinpath(".sdc/memory/candidates.md").write_text(
        f"# Candidates\n\nentropyprobe candidate {raw_token}\nentropyprobe mixed {high_entropy}\n"
    )
    root.joinpath(".sdc/memory/candidate-a.md").write_text(f"entropyprobe lowercase {lowercase_entropy}\n")
    root.joinpath(".sdc/memory/candidate-b.md").write_text(f"entropyprobe numeric {numeric_entropy}\n")
    root.joinpath(".sdc/memory/candidate-c.md").write_text(f"entropyprobe hex {hex_entropy}\n")
    recall_code, recall_output = run_runtime(
        root, "recall", "--change", change.name, "--query", "entropyprobe", "--limit", "10"
    )
    evidence_path = root / ".sdc/runtime" / change.name / "evidence.jsonl"
    command_code, command_output = run_runtime(
        root,
        "evidence",
        "append",
        "--change",
        change.name,
        "--stage",
        "apply",
        "--command",
        f"curl -H 'Authorization: Bearer {raw_token}' https://example.invalid",
        "--status",
        "failed",
    )
    command_unchanged = not evidence_path.exists()
    summary_code, summary_output = run_runtime(
        root,
        "evidence",
        "append",
        "--change",
        change.name,
        "--stage",
        "apply",
        "--command",
        "npm run eval:sdc",
        "--status",
        "passed",
        "--summary",
        f"Observed {raw_token} {high_entropy} {lowercase_entropy} {numeric_entropy} {hex_entropy}; safe {safe_long_text}",
    )
    persisted = evidence_path.read_text() if evidence_path.exists() else ""
    checks = [
        "sensitive recall redacted: yes" if recall_code == 0 and all(value not in recall_output for value in (raw_token, high_entropy, lowercase_entropy, numeric_entropy, hex_entropy)) else "sensitive recall redacted: no",
        "authorization command rejected: yes" if command_code != 0 else "authorization command rejected: no",
        "rejected command unchanged: yes" if command_unchanged else "rejected command unchanged: no",
        "summary accepted redacted: yes" if summary_code == 0 and "[REDACTED]" in persisted else "summary accepted redacted: no",
        "raw summary not persisted: yes" if all(value not in persisted for value in (raw_token, high_entropy, lowercase_entropy, numeric_entropy, hex_entropy)) else "raw summary not persisted: no",
        "ordinary long text preserved: yes" if safe_long_text in persisted else "ordinary long text preserved: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([
        recall_output,
        command_output,
        summary_output,
        *checks,
        "RESULT: PASS" if expected else "RESULT: FAIL",
    ])


def session_pointer_and_hook_identity_AC_06(root: Path) -> str:
    run_sdc(root, "init")
    run_sdc(root, "change", "payload-selected", "--confirmed-intake")
    payload_change = active_change(root, "payload-selected")
    run_sdc(root, "change", "environment-stale", "--confirmed-intake")
    stale_change = active_change(root, "environment-stale")
    run_runtime(root, "select", "--change", payload_change.name, "--session-id", "payload-session")
    run_runtime(root, "select", "--change", stale_change.name, "--session-id", "stale-session")

    pointer = root / ".sdc/runtime/sessions/payload-session/active-change.json"
    valid_pointer = pointer.read_bytes()
    malformed = json.loads(pointer.read_text())
    malformed.pop("selected_at")
    malformed.pop("source")
    pointer.write_text(json.dumps(malformed))
    malformed_code, malformed_output = run_runtime(
        root, "resolve", "--session-id", "payload-session", env={"SDC_ACTIVE_CHANGE": ""}
    )
    pointer.write_bytes(valid_pointer)

    hook_script = REPO_ROOT / "hooks/session-start"
    hook_env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(root / "home"),
        "CLAUDE_PLUGIN_ROOT": str(REPO_ROOT),
        "SDC_SESSION_ID": "stale-session",
        "SDC_ACTIVE_CHANGE": "",
    }
    hook_result = subprocess.run(
        [str(hook_script)],
        cwd=root,
        env=hook_env,
        input=json.dumps({"session_id": "payload-session", "hook_event_name": "SessionStart"}),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    hook_output = hook_result.stdout
    checks = [
        "incomplete pointer rejected: yes" if malformed_code != 0 and "invalid-session-pointer" in malformed_output else "incomplete pointer rejected: no",
        "payload session preferred: yes" if hook_result.returncode == 0 and payload_change.name in hook_output else "payload session preferred: no",
        "stale environment ignored: yes" if stale_change.name not in hook_output else "stale environment ignored: no",
    ]
    expected = all(check.endswith("yes") for check in checks)
    return "\n".join([malformed_output, hook_output, *checks, "RESULT: PASS" if expected else "RESULT: FAIL"])


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
    "lifecycle_state_machine_AC_01": lifecycle_state_machine_AC_01,
    "lifecycle_evidence_gate_AC_01": lifecycle_evidence_gate_AC_01,
    "lifecycle_content_gates_AC_01": lifecycle_content_gates_AC_01,
    "archive_requires_archivable_state_AC_01": archive_requires_archivable_state_AC_01,
    "archive_rejects_forged_state_AC_01": archive_rejects_forged_state_AC_01,
    "active_change_resolver_AC_02": active_change_resolver_AC_02,
    "unsafe_active_change_symlink_AC_02": unsafe_active_change_symlink_AC_02,
    "unsafe_runtime_ancestor_symlinks_AC_02": unsafe_runtime_ancestor_symlinks_AC_02,
    "explicit_empty_selector_AC_02": explicit_empty_selector_AC_02,
    "public_cli_symlink_boundaries_AC_02": public_cli_symlink_boundaries_AC_02,
    "role_context_manifests_AC_03": role_context_manifests_AC_03,
    "memory_recall_candidate_AC_04": memory_recall_candidate_AC_04,
    "recall_redacts_adjacent_sensitive_lines_AC_04": recall_redacts_adjacent_sensitive_lines_AC_04,
    "recall_root_containment_AC_04": recall_root_containment_AC_04,
    "sensitive_runtime_values_AC_04": sensitive_runtime_values_AC_04,
    "research_routing_no_public_command_AC_05": research_routing_no_public_command_AC_05,
    "session_context_adapter_and_evidence_AC_06": session_context_adapter_and_evidence_AC_06,
    "hook_requires_trustworthy_session_id_AC_06": hook_requires_trustworthy_session_id_AC_06,
    "session_pointer_and_hook_identity_AC_06": session_pointer_and_hook_identity_AC_06,
    "hook_files_and_installer_boundaries_AC_07": hook_files_and_installer_boundaries_AC_07,
    "runtime_contract_templates_AC_07": runtime_contract_templates_AC_07,
    "runtime_distribution_inventory_AC_07": runtime_distribution_inventory_AC_07,
    "source_marketplace_layout_AC_07": source_marketplace_layout_AC_07,
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
