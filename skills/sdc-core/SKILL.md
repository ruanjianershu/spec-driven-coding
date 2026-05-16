---
name: sdc
description: "SDC main entry. Route natural language requests across init, change, plan, apply, check, archive, and harness for spec-driven coding."
---

# Skill: SDC 主入口 sdc

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `/sdc`
- `/sdc 初始化`
- `/sdc 新需求`
- `/sdc 开始实现`
- `/sdc 检查`
- `/sdc 完成`
- "用 SDC 做"

## 核心使命

提供一个统一、简单的 SDC 入口。用户不需要记住所有细分命令，只要描述当前想做什么，本技能负责路由到合适的 SDC 阶段。

SDC 的公共路径是：

```text
init -> change -> plan -> apply -> check -> archive
```

详细能力仍然存在，但默认隐藏在公共路径之后：`spec`、`validate`、`review`、`test`、`quality`、`implement`。

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc`.
- Shared gates and priorities: `../sdc-shared/workflow-standards.md`.
- Discovery decisions: `../sdc-shared/discovery-gate.md`.
- Legacy routing: `../sdc-shared/legacy-impact-gate.md`.

## 路由规则

| 用户意图 | 应执行的 SDC 能力 |
| --- | --- |
| 初始化、第一次使用、建立目录 | `/sdc:init` |
| 新需求、新功能、需求变更 | `/sdc:change` |
| 需求探索、头脑风暴、范围不清楚 | `/sdc:change` 的 Discovery Gate |
| 开始写代码、执行计划 | `/sdc:apply` |
| 检查、验收、能不能交付 | `/sdc:check` |
| 分析 bug、失败原因、日志问题 | `/sdc:check` 的 bug mode |
| 分析影响范围、上线风险 | `/sdc:check` 的 impact mode |
| 分析存量仓库、接手项目 | `/sdc:check` 的 repo mode |
| 遗留项目需求已确认，分析改动影响 | 当前 change 的 Legacy Impact Gate，之后 `/sdc:plan` |
| 完成、归档、沉淀规范 | `/sdc:archive` |
| 记录项目规则、避免重复踩坑 | `/sdc:harness` |

## 执行原则

1. 优先判断阶段，不要求用户记细分命令。
2. 如果 `.sdc/` 不存在，先建议或执行 `/sdc:init`。
3. 新需求必须进入 `.sdc/changes/` 或 `.sdc/current/`。
4. 需求不确定时先进入 Discovery Gate，不能直接生成 Confirmed spec。
5. 遗留项目 init 只做整体认知；具体变更影响面必须在 change 需求确认后执行。
6. apply 前必须有 confirmed spec、impact（如适用）、design/plan 和 tasks。
7. check 承担 validate/review/test/quality，以及 bug/impact/repo 分析入口。
8. spec/design/tasks/code 冲突时必须停线。
9. 高影响决策必须 Confirmed，不能 Silent Default。
10. 完成前必须 check 通过；归档时必须沉淀到 `.sdc/specs/`。

## 输出格式

```text
🔧 SDC
==================================================

## 识别到的阶段
初始化 / 新需求 / 实现 / 检查 / 完成 / 规则沉淀

## 我会执行
- ...

## 当前结果
- ...

## 下一步
👉 ...
```

## 质量红线

- 不能要求用户记住所有细分命令。
- 不能跳过需求记录直接实现。
- 不能绕过校验直接归档。
- 必须给出下一步。
