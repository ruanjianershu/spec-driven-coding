---
name: sdc-change
description: "Create a focused requirement change under .sdc/changes/active with proposal, spec, design, tasks, and notes."
---

# Skill: SDC 需求变更创建 /sdc:change

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `/sdc:change`
- "创建需求变更"
- "新建一次迭代"
- "开始一个 change"
- "记录这次需求"

## 核心使命

创建一次独立、可追踪、可验证的需求迭代。`/sdc:change` 先判断需求确定性：

- 需求不清楚：进入 Discovery Gate，先讨论、比较、收敛。
- 需求清楚：创建 change，并进入 spec/plan。
- 存量/遗留项目：需求确认后必须进入 Legacy Impact Gate，再 plan/apply。

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-change`.
- Shared priority, decision, and stop-line rules: `../sdc-shared/workflow-standards.md`.
- Brainstorm/discovery rules: `../sdc-shared/discovery-gate.md`.
- Brownfield impact rules: `../sdc-shared/legacy-impact-gate.md`.
- Change file schema: `../sdc-shared/artifact-schemas.md`.

## 执行步骤

1. 如果 `.sdc/` 不存在，先执行或建议 `/sdc:init`。
2. 判断需求清晰度：用户、目标、范围、场景、验收、高影响决策。
3. 如果不清晰，创建/更新 `discovery.md`，并停在 Discovery Gate。
4. 如果清晰，生成 change id：`YYYY-MM-DD-short-name`。
5. 创建 `.sdc/changes/active/<change-id>/`。
6. 创建或更新 `discovery.md`、`proposal.md`、`spec.md`、`impact.md`、`design.md`、`tasks.md`、`notes.md`。
7. 未确认高影响决策必须进入 Decision Ledger，不得写成事实。
8. Brownfield/Legacy 项目在需求确认后创建或更新 `impact.md`。
9. 输出推荐下一步：继续 discovery、`/sdc:spec` 或 `/sdc:plan`。

## Discovery Gate

当目标、范围、验收或高影响决策不清楚时，必须使用 `../sdc-shared/discovery-gate.md`。

讨论规则：

- 一次最多提出 3 个关键问题。
- 可以给出 2-3 个候选方向，但必须标为 `Proposed`。
- 推荐最小 MVP slice，而不是完整大方案。
- 用户确认前不能输出 `Confirmed` spec。

## Legacy Impact Gate

对 Brownfield/Legacy 项目，需求确认后必须使用 `../sdc-shared/legacy-impact-gate.md`。

正确顺序：

```text
Discovery Gate -> Confirmed spec -> impact.md -> plan -> apply
```

## 输出格式

```text
✅ SDC 需求变更已创建 / 已进入 Discovery Gate
==================================================

## Change ID
YYYY-MM-DD-short-name

## 当前状态
- Discovery：不需要 / 进行中 / 已完成
- Spec：Draft / Confirmed / 待创建
- Legacy Impact：不适用 / 待分析 / 已完成

## 创建/更新文件
- ...

## 待确认事项
- ...

## 下一步
👉 ...
```

## 质量红线

- 必须创建独立 change 目录。
- 不能覆盖已有 change。
- 模糊需求必须进入 Discovery Gate。
- 未确认高影响决策不能写成事实。
- spec/tasks 不能只有空模板。
- 遗留项目需求确认后不能跳过 Legacy Impact Gate。
