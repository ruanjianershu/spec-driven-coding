---
name: sdc-archive
description: "Archive a completed SDC change, preserve history, promote final spec, and run the Knowledge Compact Gate."
---

# Skill: SDC 需求归档 /sdc:archive

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `/sdc:archive`
- "归档这个需求"
- "完成这个 change"
- "沉淀到 specs"
- "结束这次迭代"

## 核心使命

把完成的需求迭代从 `.sdc/changes/active/<change-id>/` 沉淀为稳定项目资产，并移动到 `.sdc/changes/archive/<change-id>/`。

归档后的 `.sdc/specs/<change-id>.md` 必须保留 SCN/REQ/AC 和最终验证证据。

同时执行 Knowledge Compact Gate：判断本次需求是否需要更新长期知识库，例如 `.sdc/decisions/`、`.sdc/standards/`、`AGENTS.md`、`.sdc/reports/`、`.sdc/project.md` 或 `.sdc/project-cognition.md`。必需归档动作可以直接执行；可选长期知识更新必须先给出建议、理由和目标文件，并等待用户确认。

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-archive`.
- Archive schema: `../sdc-shared/artifact-schemas.md`.
- Archive gate: `../sdc-shared/delivery-gates.md`.
- Traceability and evidence rules: `../sdc-shared/workflow-standards.md`.

## 归档前置条件

必须确认：

- `sdc-validate` 已通过或有等价证据。
- `/sdc:check` 已通过或有等价 review/test/security/quality 证据。
- 关键 tasks 已完成。
- `spec.md` 是最终 confirmed 版本。
- SCN/REQ/AC/T###/验证证据可追溯。
- 测试和质量结论记录在 `notes.md`、`reports/` 或 change 目录中。

## 归档动作

1. 将 active change 的最终 `spec.md` 复制或提升为 `.sdc/specs/<change-id>.md`。
2. 在 change 目录创建 `archive.md`。
3. 记录归档时间、交付结论、验证结果、残余风险。
4. 记录 REQ/AC/T### 覆盖摘要和遗留项。
5. 运行 Knowledge Compact Gate，判断长期知识库更新项。
6. 将目录移动到 `.sdc/changes/archive/<change-id>/`。

不要删除 change 目录。历史上下文是资产。

## Knowledge Compact Gate

归档时必须输出一张知识沉淀判断表，但不要把所有文件都机械更新。

必需项：

- `.sdc/specs/<change-id>.md`：最终 confirmed spec。
- `.sdc/changes/archive/<change-id>/archive.md`：归档结论、证据、风险、知识沉淀摘要。

条件项：

- `.sdc/decisions/`：本次产生了长期产品、技术、架构、数据、权限、发布或安全决策。
- `.sdc/standards/`：本次沉淀出可复用开发规范、测试规范、架构边界、安全规则、Git 规则或 AI 协作规则。
- `AGENTS.md`：本次暴露了 AI 易犯的重复错误、必须遵守的执行护栏，或需要把 standards 提炼成代理可执行规则。需要建议用户运行或等价执行 `/sdc:harness`。
- `.sdc/reports/bug/`：本次包含值得长期保留的缺陷根因、复现路径或防回归策略。
- `.sdc/reports/impact/` 或 archive final impact section：Brownfield/Legacy 变更需要保留最终旧系统改造点、影响点、偏差和残余风险。
- `.sdc/project.md`：项目背景、技术栈、验证命令、部署方式或长期约束发生变化。
- `.sdc/project-cognition.md`：仅当仓库结构、核心模块、数据模型、公共契约或集成方式发生长期变化，或相关认知已明显过期时更新；不要每次 archive 都重跑完整项目认知。

可选长期知识更新必须先询问用户，例如：

```text
Knowledge Compact Gate 建议更新 2 个长期知识文件：
1. .sdc/decisions/2026-05-18-auth-timeout.md：本次确认了登录超时策略。
2. AGENTS.md：本次暴露了 AI 容易跳过 intake 的问题，需要新增执行护栏。

是否现在写入这些长期知识更新？请回复 yes/no。
```

用户未确认前，不要写入条件项。

## 输出格式

```text
✅ SDC 需求迭代已归档
==================================================

## Change
<change-id>

## 沉淀文件
- .sdc/specs/<change-id>.md
- .sdc/changes/archive/<change-id>/archive.md

## 归档结论
- ...

## Knowledge Compact Gate
| Action | Target | Reason | Status |
| --- | --- | --- | --- |
| Required | .sdc/specs/<change-id>.md | Final confirmed spec | Done |
| Required | .sdc/changes/archive/<change-id>/archive.md | Archive evidence | Done |
| Recommended | .sdc/decisions/... | Long-lived decision found | Needs confirmation |
| N/A | .sdc/project-cognition.md | No repo-level cognition change | N/A |

## 下一步
👉 新需求执行 `/sdc:change <short-name>`
```

## 质量红线

- 校验未通过不能归档。
- 不能删除 change 历史。
- 不能静默覆盖已有 specs 文件。
- 追溯链不完整不能归档为稳定规范。
- 未完成任务必须关闭、迁移到新 change，或记录明确理由。
- 不能跳过 Knowledge Compact Gate。
- 不能在用户未确认时写入 decisions、standards、AGENTS.md、reports 或 project cognition 等条件项。
- 不能把每次需求归档都升级成完整项目认知重扫。
