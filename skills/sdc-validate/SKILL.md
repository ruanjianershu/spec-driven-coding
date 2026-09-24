---
name: sdc-validate
description: "Use when current or active SDC artifacts need structural and traceability validation."
---

# Skill: SDC 规范校验 sdc-validate

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `sdc-validate`
- "校验 SDC"
- "检查需求完整性"
- "能不能开始实现"
- "能不能归档"

## 核心使命

校验 `.sdc/current/` 或 `.sdc/changes/active/<change-id>/` 是否满足进入下一阶段的最低质量门槛。

## Reference Loading

Load only what is needed:

- For `compact.json`, use `../../sdc-references/compact-workflow.md` for artifact requirements instead of the standard document list below. It preserves confirmation, traceability, current receipts, and independent review; do not request synthetic spec/design/tasks files.

- Role contract: `../../sdc-references/role-contracts.md`, section `sdc-validate`.
- Shared validation and decision rules: `../../sdc-references/workflow-standards.md`.
- Common Ground and expert routing: `../../sdc-references/common-ground.md`, `../../sdc-references/expert-routing.md`.
- Artifact schemas: `../../sdc-references/artifact-schemas.md`.
- Artifact output contracts: `../../sdc-references/artifact-output-contracts.md`.
- Execution orchestration contracts: `../../sdc-references/execution-orchestration.md`.
- Validate gate: `../../sdc-references/delivery-gates.md`.
- Brownfield impact gate: `../../sdc-references/legacy-impact-gate.md`.

## 校验范围

### 全局

- `.sdc/constitution.md`
- `.sdc/common-ground.md`
- `.sdc/expert-routing.md`
- `.sdc/knowledge/index.md`
- `.sdc/knowledge/product/`
- `.sdc/knowledge/technical/`
- `.sdc/memory/`
- `.sdc/standards/`
- `AGENTS.md`（如存在）

### current

- `.sdc/current/spec.md`
- `.sdc/current/plan.md`
- `.sdc/current/tasks.md`
- `.sdc/current/apply.md`
- `.sdc/current/context-pack.md`
- `.sdc/current/knowledge-candidates.md`

### active change

- `proposal.md`
- `discovery.md`
- Discovery Open: only `discovery.md`, Draft `proposal.md`, and `notes.md` are expected.
- Discovery Closed: `spec.md`, `impact.md`（Brownfield/Legacy 必须）, `design.md`, `tasks.md`, `context-pack.md`, `knowledge-candidates.md`
- `notes.md`

## 必须检查

- 文件是否存在且不是空模板。
- spec 是否包含 Glossary、INV、SCN、REQ、AC、验证策略、追溯矩阵。
- spec/design/context-pack 是否记录 Knowledge Sources Used。
- spec/design/context-pack 是否记录 Common Ground Used。
- spec/design/context-pack 是否记录 Artifact Output Contract。
- context-pack/check 是否记录 Expert Profiles Used 且与实际风险匹配。
- 触发流程/状态、集成、API、数据、UX、测试、部署、AI 参与等场景时，是否有对应流程图、时序/集成图、API 契约、数据/迁移契约、UX 状态、测试矩阵、上线检查清单或 AI 参与说明；不适用时是否写明 `N/A + 证据原因`。
- memory candidates 是否被错误当作 confirmed facts。
- final spec/design/context-pack/tasks/impact 是否含有 `Assumed`、`Proposed`、`TBD`、`Conflict`、`Stale` 或未闭合 Knowledge Gap。
- 知识项是否记录 Status、Source、Verified At、Verified Against、Scope。
- 候选知识是否记录 Source、Evidence Needed、Target、Promotion Gate。
- 是否遵守 No Evidence, No Fact / No Confirmation, No Execution / No Impact, No Brownfield Change。
- tasks 是否包含标准 `T### [REQ-*] [AC-*] [Phase] [Size]`。
- 任务是否只使用 Size S/M。
- 行为变更是否在同一可验收任务内先验证失败再实现；不强制拆出独立测试任务。
- Decision Ledger 是否存在且状态正确。
- Proposed / Assumed / TBD / Conflict 是否被错误写入最终范围。
- Discovery Gate 未退出时，是否错误生成了完整 spec/design/tasks/impact/context-pack/knowledge-candidates。
- Silent Defaults 是否出现。
- Brownfield/Legacy 当前 change 是否有有效 `impact.md`。
- `impact.md` 是否仍有阻塞性待确认项。
- apply/check 是否记录了必要的 `knowledge-candidates.md`，并留待 archive 确认。
- Artifact Output Contract 是否与实际 diff、impact.md、tasks 和验证证据一致。
- Global Constraints 和 Plan Preflight 是否完整且通过。
- 每个任务是否包含 Files、Consumes、Produces、Verify、Expected、Review、Evidence 和 Source。
- 已完成任务是否 Review Approved 且 Evidence 非 Pending；delivery check/archive 是否有 Final Whole-Change Review，且 runtime 账本存在时是否与持久证据一致。git-ignored 账本缺失只警告。

## 输出格式

```text
🔍 SDC 校验报告
==================================================

## 校验目标
current / change-id

## 通过项
- ...

## 追溯检查
- ...

## 决策确认检查
- ...

## 必须修复
| 文件 | 问题 | 修复建议 |

## 建议完善
| 文件 | 问题 | 建议 |

## 结论
👉 【通过，可以进入下一阶段】 / 【不通过，需要补齐】
```

## 质量红线

- 不能只说“看起来可以”。
- 必须指出具体文件和修复建议。
- 严重缺失不能放行。
- 追溯链断裂不能放行到 apply/archive。
- 未确认高影响决策或 Silent Default 不能放行。
- OPEN 或高影响 WORKING Common Ground 被当成事实时不能放行。
- 高风险改动缺少对应 expert profile / standards 覆盖时不能放行。
- 触发式交付物缺失、或者用无证据 `N/A` 跳过时不能放行。
- Plan Preflight、任务接口、任务审查、执行证据或最终整体审查缺失时不能放行。
