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

创建一次独立、可追踪、可验证的需求迭代。`/sdc:change` 不能由 AI 自己判断“需求是否足够清楚”，必须先执行强制 intake：

- 创建任何 change 文件前：先问 4 个 intake 问题，并等待用户确认。
- 用户确认后：如果需求已敲定，再创建完整 change 并进入 spec/plan。
- 仍有不确定项：继续 Discovery Gate，只保留轻量 Draft，不生成完整 spec/design/tasks。
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
2. 执行 Mandatory Change Intake Gate：复述用户原话，提出 4 个 intake 问题。
3. 用户确认前，不得创建或更新 `.sdc/changes/active/*` 文件。
4. 用户确认后，生成 change id：`YYYY-MM-DD-short-name`。
5. 如果确认后仍有 Open Questions 或高影响未确认决策，只创建或更新最小 Draft：`discovery.md`、可选 `proposal.md`、简短 `notes.md`。
6. Discovery Gate 未退出前，不得创建或更新 `spec.md`、`impact.md`、`design.md`、`tasks.md`。
7. Discovery Gate 退出后，再创建或更新完整 change artifacts：`proposal.md`、`spec.md`、`impact.md`（如适用）、`design.md`、`tasks.md`、`notes.md`。
8. 未确认高影响决策必须进入 Decision Ledger，状态为 `Proposed` 或 `Assumed`，不得写成事实。
9. Brownfield/Legacy 项目在需求确认后创建或更新 `impact.md`。
10. 输出推荐下一步：继续 discovery、`/sdc:spec` 或 `/sdc:plan`。

## Discovery Gate

创建 change 文件前必须先使用 `../sdc-shared/discovery-gate.md` 中的 Mandatory Change Intake Gate。目标、范围、验收或高影响决策仍不清楚时，继续 Discovery Gate。

讨论规则：

- intake 阶段固定提出 4 个问题，覆盖项目背景、核心范围、技术偏好、约束与验收。
- discovery 阶段一次提出 3-5 个关键问题。
- 可以给出 2-3 个候选方向，但必须标为 `Proposed`。
- 推荐最小 MVP slice，而不是完整大方案。
- 用户确认前不能创建 change files，也不能输出 `Confirmed` spec。
- Open Questions 未闭合时默认只问下一批 3-5 个关键问题，不展开完整 spec/design/tasks。
- 禁止“如果不对告诉我，我先改”式写法；必须先问 yes/no 或选项确认，再写入持久文件。

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
- 所有新 change 必须先进入 Mandatory Change Intake Gate。
- 未确认高影响决策不能写成事实。
- Open Questions 未闭合时不能生成完整 `spec.md`、`design.md`、`tasks.md`。
- 不能用“如有偏差请告知”替代用户确认。
- spec/tasks 不能只有空模板。
- 遗留项目需求确认后不能跳过 Legacy Impact Gate。
