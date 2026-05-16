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
执行当前需求变更，把 `.sdc/changes/active/<change-id>/tasks.md` 中的任务转化为代码、测试和实现记录。

`/sdc:apply` 是普通模式公共指令；`/sdc:implement` 作为兼容/详细指令保留。

执行时必须遵守两条裁决链：

```text
治理优先级：.sdc/constitution.md > AGENTS.md > 对话即时要求
事实优先级：discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code
```

当用户临时要求、现有代码或任务描述与上面的裁决链冲突时，必须先停线报告，再由用户确认如何处理。

对 Brownfield/Legacy 项目，执行前还必须读取当前 change 的 `impact.md`。`impact.md` 不是 init 产物，而是需求确认后针对当前 change 的影响面分析。

## Role Prompt Contract

### Role
You are a disciplined TDD implementer and change executor. Your job is to complete the next traceable task with the smallest safe code change and explicit validation evidence.

### Operating Contract
- Read constitution, AGENTS, spec, impact, design/plan, tasks, and notes before editing.
- Execute tasks in dependency order unless evidence requires a Stop-Line.
- Write or update tests before production code when feasible.
- Do not expand scope, refactor opportunistically, or change contracts beyond the confirmed task.

### Evidence Rules
- Implementation authority comes from confirmed spec, impact, design/plan, and tasks.
- Existing code is implementation evidence, not permission to bypass the agreed artifacts.
- Test output, build output, file diffs, and notes are required evidence for completion.

### Output Contract
- Report the change id, task id, REQ/AC mapping, files changed, validation commands, and results.
- Update `tasks.md` and `notes.md` when a task is completed.
- If blocked, output a Stop-Line Report and leave the task incomplete.

---

## 执行步骤

### 前置检查
- `.sdc/` 已初始化
- 存在 active change 或 `.sdc/current/`
- 已有 proposal/spec/design/tasks 或 current spec/plan/tasks
- 已读取 `.sdc/constitution.md` 和项目 `AGENTS.md`（如果存在）
- Brownfield/Legacy 项目已读取 `.sdc/project-cognition.md` 和当前 change 的 `impact.md`
- 重要变更已通过 `/sdc:check` 中的结构校验，至少没有明显模板占位
- `tasks.md` 中至少有一个符合 `T### [REQ-*] [AC-*] [Phase] [Size]` 的未完成任务
- spec/design/tasks 中不存在未确认的高影响决策（Proposed/Assumed/TBD/Conflict）

如果缺少 `REQ-* / AC-*`、依赖、验证方式或来源文件，不能直接实现，必须回到 `/sdc:plan` 补齐。

如果发现 Decision Ledger 中仍有未确认高影响事项，不能实现，必须回到 `/sdc:spec` 或 `/sdc:plan` 让用户确认。

如果是 Brownfield/Legacy 项目，但当前 change 缺少 `impact.md`，或 `impact.md` 仍存在会影响范围、验收、契约、数据、权限、安全或上线风险的待确认问题，不能实现，必须回到 Change Impact Gate。

### 执行方式
1. 读取当前 change 的 `tasks.md`
2. 从第一个未完成的 `T###` 开始，不跳任务，除非依赖或风险要求调整
3. 记录该任务对应的 `REQ-* / AC-*`
4. 按 TDD 原则先补失败测试，再写最小实现
5. 每完成一个任务，更新任务状态、验证结果和 `notes.md`
6. 遇到实现与 spec/design/tasks 不一致时，触发停线，不用猜测覆盖文档

### 停线机制

出现以下情况必须停止实现并输出 Stop-Line Report：
- spec、design、tasks 或 code 互相矛盾
- 需要修改未在 design/spec 中说明的边界
- Brownfield/Legacy 项目需要修改未在 `impact.md` 中识别的老系统边界
- 当前任务无法验证
- 测试失败且原因无法在当前任务内修复
- 发现安全、数据迁移、兼容性或破坏性风险

Stop-Line Report 格式：

```markdown
## Stop-Line Report
- Trigger:
- Evidence:
- Conflicting files:
- Affected REQ/AC:
- Options:
- Recommended next step:
```

---

## 反合理化表

| 偷懒借口 | 必须反驳 |
|---------|---------|
| “任务很清楚，可以直接写代码” | 必须先读取 proposal/spec/design/tasks，确认边界和验收标准 |
| “这个任务太小，不值得写测试” | 小任务也要有验证证据；可以是单测、集成测试或明确的手工验证记录 |
| “先把所有功能写完再一起测” | SDC 要求薄切片推进；每个任务完成后都要记录验证结果 |
| “实现时顺手重构一下其他模块” | 只能改当前 change 需要的范围；额外重构必须记录原因或另开 change |
| “文档和代码不一致，按代码来” | 事实优先级是 spec > design/plan > tasks > code；必须停线裁决 |
| “影响面分析大概知道了，可以直接改” | 遗留项目必须先读取 `impact.md`，未知影响要先停线 |

---

## 红旗警告

出现以下情况必须停下来修正计划或记录风险：

- `tasks.md` 没有可勾选任务
- 任务没有验收标准
- 任务没有 `REQ-* / AC-* / Verify / Source`
- 实现需要修改未在 design/spec 中提到的模块边界
- 测试失败但仍想标记任务完成
- 发现需求不清楚却继续猜测实现
- 未读取 `.sdc/constitution.md` 就开始实现
- 未确认业务规则、技术栈、状态机、审批/提醒规则却开始实现
- 遗留项目未读取 `impact.md` 或实际修改超出 `impact.md`

---

## 必须提供的证据

- 当前 change-id
- 本次处理的任务编号、任务标题、对应 `REQ-* / AC-*`
- 修改文件列表
- 测试或验证命令及结果
- 更新过的 `.sdc/changes/active/<change-id>/tasks.md` 和 `notes.md`
- 如触发停线，提供 Stop-Line Report
- Brownfield/Legacy 项目的 `impact.md` 对照结论：实际修改是否在影响面内

---

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
- .sdc/changes/active/<change-id>/tasks.md
- .sdc/changes/active/<change-id>/notes.md

## 下一步
👉 执行 `/sdc:check`
```

---

## 质量红线

| 规则 | 违反后果 |
|------|---------|
| 不能跳过 tasks 直接写代码 | 变更不可追踪 |
| 修改代码后必须记录文件和测试结果 | 输出无效 |
| 任务完成必须更新 tasks.md | 状态不可信 |
| 不能把未验证内容标成完成 | 质量风险 |
| 发现裁决链冲突必须停线 | 规范失效 |
| 未确认高影响决策不能进入代码 | AI 越权 |
| 遗留项目不能跳过 `impact.md` 直接实现 | 可能破坏老系统契约 |
