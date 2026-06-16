# 2026-06-15-artifact-output-contracts Proposal

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| discovery.md | Confirmed | Closed Decision Ledger | Defines confirmed scope |
| README.md | Confirmed | Current SDC user docs | Must explain new capability succinctly |
| skills/sdc-shared/* | Confirmed | Existing references | Defines where the new contract belongs |
| sdc-cli.py | Confirmed | Current templates and validators | Implements managed workspace behavior |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## Input Evidence

| Source | Type | Status | Summary | Evidence / Link |
|---|---|---|---|---|
| User request | Requirement | Confirmed | SDC needs mandatory stage input/output standards similar to enterprise workflow deliverables. | Current conversation |
| Existing SDC validation | Code evidence | Confirmed | Existing gates validate traceability, knowledge, Common Ground, and impact but not triggered output artifacts. | sdc-cli.py |

## Draft Artifact Output Contract

| Output | Proposed Status | Trigger | Needed Before | Notes |
|---|---|---|---|---|
| Process / State Diagram | Confirmed | workflow/state/user journey | plan/check | Triggered only when relevant |
| Sequence / Integration Diagram | Confirmed | integration/async/event | plan/check | Triggered only when relevant |
| API / Contract Specification | Confirmed | API/event/contract | plan/check | Triggered only when relevant |
| Data Model / Migration Contract | Confirmed | data/schema/migration | plan/check | Triggered only when relevant |
| UX Flow / Interaction States | Confirmed | UI/user-facing states | plan/check | Triggered only when relevant |
| Test Matrix | Confirmed | every final change | plan/check | Required |
| Deploy / Release Checklist | Confirmed | deployment/config/runtime | check/archive | Triggered only when relevant |
| AI Involvement Note | Confirmed | AI-assisted delivery | check/archive | Triggered unless N/A evidenced |

## 背景

SDC 已经具备流程治理、反乱猜门禁、知识库、Common Ground、Expert Routing、Brownfield impact 和归档知识沉淀。但它对阶段产物的强制性不足：即使需求触发流程图、API 契约、数据模型、测试矩阵或上线清单，现有校验也可能只检查 spec/design/tasks/context-pack 的结构，而不检查“该输出的标准产物是否真的输出”。

## Status

Confirmed - Discovery Closed

## 目标

- 在不增加公开命令的前提下，为 SDC 增加 Artifact Output Contract。
- 让 `change` 记录输入证据和候选标准产物。
- 让 `plan` 生成被触发的标准产物。
- 让 `check/validate` 阻断缺失的触发式交付物。
- 用 deterministic eval 覆盖缺失触发产物的失败场景。

## 非目标

- 不新增 `/requirement-analysis`、`/tech-design`、`/test-plan`、`/deploy-checklist` 等公开命令。
- 不强制每个小需求都生成大型设计文档。
- 不把内部公司资料原文公开写入项目。

## 初始场景

- SCN-01: 用户执行 SDC change，AI 在 intake 中记录输入证据和候选输出产物，但不在需求确认前生成完整设计。
- SCN-02: 需求确认后，plan 根据触发条件输出流程图、API/数据契约、测试矩阵和上线清单等标准产物。
- SCN-03: check/validate 发现触发了 API 或数据等风险但缺少对应产物时阻断交付。

## 初始需求

- REQ-01: SDC must define a shared Artifact Output Contract reference.
- REQ-02: SDC change/plan/check/validate workflows must apply the contract without adding public commands.
- REQ-03: SDC CLI templates and validation must require final artifact contract coverage.
- REQ-04: SDC evals and release audit must catch regressions in artifact output contract enforcement.

## 初始验收标准

- AC-01: README and shared references document Artifact Output Contract and triggered outputs.
- AC-02: Managed templates contain Artifact Output Contract and final design contains Test Matrix.
- AC-03: CLI validation fails when API trigger evidence exists but API/Contract output is missing.
- AC-04: `npm run audit` and `npm run eval:sdc` pass.

## 任务清单

See tasks.md.

## 风险和回滚

Risk: validation becomes too heavy for simple changes. Mitigation: optional outputs can be `N/A` with evidence reason; only Test Matrix is always required for final plan/check.

Rollback: remove the reference, validation function, template sections, and eval scenario.
