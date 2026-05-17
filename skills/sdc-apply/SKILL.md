---
name: sdc-apply
description: "Apply the current SDC change by executing tasks incrementally, updating notes, files changed, and validation evidence."
---

# Skill: SDC 执行变更 /sdc:apply

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `/sdc:apply`
- "执行这个 change"
- "开始实现"
- "按计划实现"
- "应用这个变更"

## 核心使命

执行当前需求变更，把 `tasks.md` 中的任务转化为代码、测试和实现记录。

执行必须遵守：

```text
discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code
```

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-apply`.
- Governance, traceability, task, and stop-line rules: `../sdc-shared/workflow-standards.md`.
- Change artifacts and task shape: `../sdc-shared/artifact-schemas.md`.
- Brownfield execution boundary: `../sdc-shared/legacy-impact-gate.md`.

## 前置检查

必须确认：

- `.sdc/` 已初始化。
- 存在 active change 或 `.sdc/current/`。
- 已读取 `.sdc/constitution.md` 和 `AGENTS.md`（如存在）。
- 已有 confirmed spec、design/plan、tasks。
- Brownfield/Legacy 项目已读取 `project-cognition.md` 和当前 change 的 `impact.md`。
- `tasks.md` 至少有一个符合 `T### [REQ-*] [AC-*] [Phase] [Size]` 的未完成任务。
- 没有阻塞性 Proposed / Assumed / TBD / Conflict 高影响决策。

不满足时输出 Stop-Line Report，而不是直接写代码。

## 执行步骤

1. 读取当前 `tasks.md`。
2. 从第一个未完成且依赖满足的 `T###` 开始。
3. 记录该任务对应的 REQ/AC。
4. 先写或更新测试，再写最小实现；如果无法写测试，先在 notes 中记录原因和替代验证方式。
5. 运行任务声明的 Verify 命令或可行的等价验证。
6. 更新 `tasks.md`、`notes.md`、文件变更和验证证据。
7. 如果实现需要超出 spec/design/tasks/impact，立即停线。

## 停线条件

- spec、design、tasks 或 code 互相矛盾。
- 需要修改未在 design/spec/impact 中说明的边界。
- 当前任务无法验证。
- 测试失败且原因无法在当前任务内修复。
- 发现安全、数据迁移、兼容性或破坏性风险。

## 输出格式

```text
🚀 SDC Apply
==================================================

## 当前 Change
<change-id>

## 本次执行任务
- T### [REQ-xx] [AC-xx] ...

## 修改文件
- ...

## 测试结果
- ...

## 更新的 SDC 记录
- ...

## 下一步
👉 执行 `/sdc:check`
```

## 质量红线

- 不能跳过 tasks 直接写代码。
- 任务完成必须更新 `tasks.md` 和 `notes.md`。
- 修改代码后必须记录文件和验证结果。
- 未验证内容不能标成完成。
- 遗留项目不能跳过 `impact.md` 或超出其边界。
