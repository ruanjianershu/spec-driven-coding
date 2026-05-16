---
name: sdc-harness
description: "Generate AGENTS.md project AI guardrails from project scan and SDC standards to prevent repeated mistakes."
---

# Skill: SDC Harness 生成 /sdc:harness

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `/sdc:harness`
- "生成 AI 规则"
- "创建 AGENTS.md"
- "不要再犯同样的错"

## 核心使命

把项目约束、SDC standards、验证命令和历史错误沉淀成 `AGENTS.md` 执行护栏，让后续 AI 开发更稳定。

`AGENTS.md` 不替代 `.sdc/constitution.md` 和 `.sdc/standards/`：

```text
.sdc/constitution.md > AGENTS.md > 对话即时要求
```

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-harness`.
- Governance and no-silent-default rules: `../sdc-shared/workflow-standards.md`.
- Workspace and standards layout: `../sdc-shared/artifact-schemas.md`.

## 执行步骤

1. 如果没有 `.sdc/constitution.md`，先建议或执行 `/sdc:init`。
2. 读取 `.sdc/constitution.md`、`.sdc/standards/`、项目结构、构建/测试文件、历史 reports 和用户描述的错误。
3. 提炼具体可执行的 must-do / must-not-do 规则。
4. 写入或更新 `AGENTS.md`，不得覆盖用户已有重要内容。
5. 记录验证命令、项目结构、历史错误和更新记录。
6. 如适合，创建或更新 `.sdc/harness.sh` 作为提交前验证脚本。

## AGENTS.md 必须包含

- 裁决链：`.sdc/constitution.md > AGENTS.md > 对话即时要求`。
- 事实链：`discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code`。
- Human Confirmation / No Silent Defaults。
- 项目必须做。
- 项目绝对不要做。
- 验证命令。
- 项目结构说明。
- 历史上犯过的错误。
- 更新记录。

## 输出格式

```text
✅ Harness 已生成 / 已更新
==================================================

## 更新文件
- AGENTS.md
- .sdc/harness.sh（如适用）

## 新增规则
- ...

## 验证命令
- ...

## 下一步
👉 提交前让 AI 先读取 AGENTS.md 并运行对应验证
```

## 质量红线

- 必须包含 must-do、must-not-do、验证命令和历史错误部分。
- 必须包含裁决链和 Human Confirmation / No Silent Defaults。
- 规则必须具体可执行，不能只是口号。
- 不能发明没有证据的项目规则。
