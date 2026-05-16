---
name: sdc-plan
description: "Generate or update proposal, spec, design, and task plan for a change, with test-first strategy and thin slices."
---

# Skill: SDC 计划生成 /sdc:plan

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `/sdc:plan`
- "帮我生成实现计划"
- "下一步怎么做"
- "怎么拆分任务"

## 核心使命

将 confirmed spec 和必要的 impact analysis 转化为分步可执行、可追溯、可验证的实现计划。

计划必须形成：

```text
SCN-* -> REQ-* -> AC-* -> T### -> validation evidence
```

默认只展开第一个可交付 MVP slice，避免一次生成过大的任务清单。

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-plan`.
- Decision, task, and stop-line rules: `../sdc-shared/workflow-standards.md`.
- Plan/design/task schema: `../sdc-shared/artifact-schemas.md`.
- Brownfield impact rules: `../sdc-shared/legacy-impact-gate.md`.

## 前置检查

计划前必须读取：

- `.sdc/constitution.md`
- `.sdc/project.md`
- 当前 change 的 `spec.md`
- 当前 change 的 `proposal.md`
- 当前 change 的 `impact.md`（Brownfield/Legacy 必须）
- 已存在的 `design.md`、`tasks.md`（如有）

如果 spec 缺少 SCN/REQ/AC、验收场景或关键约束，必须停线回到 `/sdc:spec`。

如果存在未确认高影响决策，必须输出 Stop-Line Report，不能写成最终 design/tasks。

如果是 Brownfield/Legacy 项目且缺少有效 `impact.md`，必须先回到 Legacy Impact Gate。

## 执行步骤

1. 确认 spec 状态和 Decision Ledger。
2. 确认 Brownfield/Legacy impact 是否适用且已完成。
3. 提炼设计摘要、影响范围、不改范围、风险和回滚。
4. 将 REQ/AC 映射到设计决策。
5. 拆出 5-12 个当前 MVP slice 的薄任务。
6. 测试任务排在实现任务前。
7. 每个任务写清 Depends on、Verify、Source。
8. 更新 `design.md` 和 `tasks.md`。

## Technical Consent Gate

以下事项必须 Confirmed、由权威项目文档支持，或被 constitution 授权：

- 技术栈、框架、数据库、ORM。
- 架构、模块边界、部署形态。
- 认证、权限、审批、状态机。
- 自动化行为、定时任务、提醒规则。
- 数据规则、删除/保留、锁策略、迁移。
- 安全策略、审计、敏感信息处理。

宽泛偏好不能直接推导为具体技术方案。

## 输出格式

```text
📋 SDC 实现计划
==================================================

## 规格追溯
| SCN | REQ | AC | Task |

## 设计摘要
- 影响范围：
- 不改范围：
- 关键取舍：
- 风险/回滚：

## 遗留项目影响面
- 适用：
- impact.md：
- 阻塞项：

## 任务拆解
- [ ] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] ...
  - Depends on:
  - Verify:
  - Source:

## 下一步
👉 执行 `/sdc:apply`
```

## 质量红线

- 每个任务必须有 `T### [REQ-*] [AC-*] [Phase] [Size]`。
- `Size` 只能是 S/M。
- 测试任务必须先于对应实现任务。
- 未确认技术/架构/状态机/权限决策必须停线。
- 默认只展开当前 MVP slice。
- 遗留项目缺少有效 `impact.md` 不能进入最终 plan。
