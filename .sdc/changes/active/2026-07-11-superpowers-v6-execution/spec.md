# Spec

## 0. 文档元信息

- Status: Confirmed
- Schema: SDC 1.3.0
- Source: user-confirmed Superpowers 6 alignment request

## 1. Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| discovery.md | Confirmed | DEC-01 through DEC-04 | Governs scope and compatibility |
| Superpowers v6 official release notes | Confirmed | GitHub releases v6.0.0-v6.1.1 | Source of execution patterns |
| SDC 1.2.1 source and evals | Confirmed | repository evidence | Baseline behavior |

## 1.1 Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## 1.2 Common Ground Used

| ID | Tier | Statement | Source | Why It Matters |
|---|---|---|---|---|
| CG-01 | ESTABLISHED | SDC keeps a small public command surface | README and user confirmation | Prevents command proliferation |
| CG-02 | ESTABLISHED | Durable project truth belongs outside runtime scratch | constitution and knowledge model | Preserves auditability |

## 1.3 Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | N/A | No product workflow or state-machine change | design.md#process-state-diagrams | N/A because this changes engineering execution rules only |
| Sequence / Integration Diagram | N/A | No service or external integration | design.md#sequence-integration-diagrams | N/A because helpers are local scripts with no runtime integration |
| API / Contract Specification | N/A | No public API contract | design.md#api-contract-specification | N/A because public commands and package bin names stay unchanged |
| Data Model / Migration Contract | N/A | No persistent schema or migration | design.md#data-model-migration-contract | N/A because runtime files are local markdown scratch |
| UX Flow / Interaction States | N/A | No graphical user interface | design.md#ux-flow-interaction-states | N/A because interaction remains existing commands and skills |
| Test Matrix | Required | CLI, helper, installer, and validation behavior | design.md#test-matrix | AC-01 through AC-06 require deterministic evidence |
| Deploy / Release Checklist | Required | Version, plugin manifests, npm package, Codex portal archive | design.md#deploy-release-checklist | Release metadata and packaging change |
| AI Involvement Note | Required | Agent execution and review behavior changes | design.md#ai-involvement-note | Human review must understand AI orchestration boundaries |

## 2. Decision Ledger / 决策台账

| ID | 决策 | 状态 | 依据来源 | 是否允许进入 REQ/AC | 下一步 |
|---|---|---|---|---|---|
| DEC-01 | Public commands remain init/change/plan/apply/check/archive/harness | Confirmed | user and README | Yes | Audit command set |
| DEC-02 | Task review returns Spec Compliance and Code Quality verdicts | Confirmed | Superpowers v6 evidence | Yes | Enforce in references and delivery gates |
| DEC-03 | Runtime handoffs are git-ignored and non-authoritative | Confirmed | SDC durability model | Yes | Persist final evidence in notes/tasks/reports |
| DEC-04 | Codex plugin declares empty hooks and marketplace metadata, and its portal artifact is rootless/minimal | Confirmed | Superpowers v6.1 Codex packaging findings | Yes | Add manifest, packager, and audit |
| DEC-05 | Implementation tasks execute serially through task review and durable evidence | Confirmed | Superpowers v6.0 execution sequence | Yes | Remove parallel implementer allowance |
| DEC-06 | Managed workspace upgrades require an unchanged ownership fingerprint or exact known legacy hash | Confirmed | user-artifact preservation invariant | Yes | Preserve modified files and report manual merge |

## 3. Glossary / 统一语言

- Plan Preflight: one complete plan consistency review before Task 1.
- Task Brief: focused file containing one task plus binding constraints.
- Dual-verdict review: separate Spec Compliance and Code Quality conclusions from one task review.
- Runtime Ledger: ignored recovery map under `.sdc/runtime/<change-id>/progress.md`.
- Final Whole-Change Review: broad review across all tasks and the complete diff.

## 4. 背景与目标

Upgrade SDC's post-plan execution reliability and token efficiency without weakening its confirmation, knowledge, impact, artifact, and traceability gates.

## 5. Business Invariants / 业务不变量

### INV-01

No new public command is introduced.

### INV-02

Runtime scratch never becomes the only durable delivery evidence.

### INV-03

A checked task cannot be complete without approved review and evidence.

## 6. 场景与需求

### SCN-01

An agent plans a confirmed multi-task change.

### REQ-01

Final plan artifacts must include non-empty, cross-artifact-consistent Global Constraints, a Plan Preflight with Passed status, reviewed sources, closed findings, and per-task Files/Consumes/Produces/Verify/Expected/Review/Evidence/Source fields.

### SCN-02

An agent executes tasks in a long session that may compact context.

### REQ-02

Apply must use focused file handoffs and a project-local runtime ledger, executing one implementation task at a time with subagents when supported and inline role isolation otherwise. WORKTREE review must stop when untracked files would be omitted.

### SCN-03

A task or complete change is reviewed.

### REQ-03

Task review must be read-only and persist independent Spec Compliance and Code Quality verdicts with resolvable durable Evidence; final delivery requires the same two verdicts for one whole-change review.

### SCN-04

SDC is installed or packaged for Codex.

### REQ-04

Codex metadata must declare repo marketplace information, `hooks: {}`, Developer Tools category, Interactive capability, complete source-installable public skills, shared contracts outside the skill scan, transactional stale-layout replacement with rollback/recovery, and deterministic rootless portal packaging that excludes source-only files.

### SCN-05

An existing SDC workspace upgrades to 1.3.

### REQ-05

Init must fingerprint managed templates, upgrade only unchanged fingerprints or exact known legacy hashes, preserve modified project rules, append the runtime ignore rule without replacing existing entries, and remain idempotent after migration.

### REQ-06

Release audit and deterministic evals must protect all new contracts.

## 7. Acceptance Criteria / 验收标准

### AC-01

Given a final task omits a required interface field
When SDC validate runs
Then validation fails with the exact missing or empty task field; empty/inconsistent Global Constraints and incomplete Plan Preflight also block.

### AC-02

Given a task is checked complete without Review Approved or durable evidence
When SDC check runs
Then delivery is blocked unless task and final review sections each contain approved Spec Compliance, approved Code Quality, and resolvable durable Evidence.

### AC-03

Given a confirmed task and git diff
When the helper scripts run
Then focused brief, report, ledger, and review-package files are created under `.sdc/runtime/<change-id>/`; WORKTREE generation fails when untracked files would be omitted.

### AC-04

Given all tasks are complete
When SDC check/archive runs
Then an inconsistent present progress ledger or missing Final Whole-Change Review approval blocks delivery, while a missing git-ignored ledger warns and falls back to durable tasks/notes evidence.

### AC-05

Given an old generated workspace
When SDC init runs twice
Then unchanged known templates upgrade with fingerprints/backups, modified managed files and custom `.sdc/.gitignore` entries are preserved while `/runtime/` is added, and the second run changes nothing.

### AC-06

Given release checks run
When audit, eval, syntax, packaging, and npm dry-run complete
Then all checks pass, every source `skills/*` directory is invocable, stale Codex layouts are removed, the repo marketplace exposes the complete workflow, the Codex archive is rootless/minimal and byte-identical across rebuilds, and the public command set remains unchanged.

## 8. 验证策略

Run syntax checks, release audit, 51 deterministic flow evals, repeated init, SDC self-check, Codex/Claude generated-layout checks, Codex portal packaging, and npm pack dry-run.

## 9. 风险、假设与待确认项

The stricter final-plan schema intentionally requires migration of generated templates. User-authored active changes are reported with repair guidance rather than silently rewritten.

## 10. 追溯关系矩阵

| SCN | REQ | AC | Task |
|---|---|---|---|
| SCN-01 | REQ-01 | AC-01 | T001, T002 |
| SCN-02 | REQ-02 | AC-03 | T001, T002 |
| SCN-03 | REQ-03 | AC-02, AC-04 | T001, T002 |
| SCN-04 | REQ-04 | AC-06 | T003 |
| SCN-05 | REQ-05 | AC-05 | T002, T004 |
| SCN-01-SCN-05 | REQ-06 | AC-06 | T004, T900 |
