---
name: sdc-validate
description: "Validate SDC current or active change files for structure, acceptance criteria, tasks, tests, and non-template content."
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

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-validate`.
- Shared validation and decision rules: `../sdc-shared/workflow-standards.md`.
- Artifact schemas: `../sdc-shared/artifact-schemas.md`.
- Validate gate: `../sdc-shared/delivery-gates.md`.
- Brownfield impact gate: `../sdc-shared/legacy-impact-gate.md`.

## 校验范围

### 全局

- `.sdc/constitution.md`
- `.sdc/standards/`
- `AGENTS.md`（如存在）

### current

- `.sdc/current/spec.md`
- `.sdc/current/plan.md`
- `.sdc/current/tasks.md`
- `.sdc/current/apply.md`

### active change

- `proposal.md`
- `discovery.md`
- Discovery Open: only `discovery.md`, Draft `proposal.md`, and `notes.md` are expected.
- Discovery Closed: `spec.md`, `impact.md`（Brownfield/Legacy 必须）, `design.md`, `tasks.md`
- `notes.md`

## 必须检查

- 文件是否存在且不是空模板。
- spec 是否包含 Glossary、INV、SCN、REQ、AC、验证策略、追溯矩阵。
- tasks 是否包含标准 `T### [REQ-*] [AC-*] [Phase] [Size]`。
- 任务是否只使用 Size S/M。
- 测试任务是否先于实现任务。
- Decision Ledger 是否存在且状态正确。
- Proposed / Assumed / TBD / Conflict 是否被错误写入最终范围。
- Discovery Gate 未退出时，是否错误生成了完整 spec/design/tasks/impact。
- Silent Defaults 是否出现。
- Brownfield/Legacy 当前 change 是否有有效 `impact.md`。
- `impact.md` 是否仍有阻塞性待确认项。

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
