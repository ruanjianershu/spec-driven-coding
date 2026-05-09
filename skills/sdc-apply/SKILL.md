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

---

## 执行步骤

### 前置检查
- `.sdc/` 已初始化
- 存在 active change 或 `.sdc/current/`
- 已有 proposal/spec/design/tasks 或 current spec/plan
- 重要变更已通过 `/sdc:check` 中的结构校验，至少没有明显模板占位

### 执行方式
1. 读取当前 change 的 `tasks.md`
2. 从第一个未完成任务开始
3. 按 TDD 原则先补测试，再写实现
4. 每完成一个任务，更新任务状态和 `notes.md`
5. 遇到实现与设计不一致时，更新 `design.md` 或记录偏差原因

---

## 反合理化表

| 偷懒借口 | 必须反驳 |
|---------|---------|
| “任务很清楚，可以直接写代码” | 必须先读取 proposal/spec/design/tasks，确认边界和验收标准 |
| “这个任务太小，不值得写测试” | 小任务也要有验证证据；可以是单测、集成测试或明确的手工验证记录 |
| “先把所有功能写完再一起测” | SDC 要求薄切片推进；每个任务完成后都要记录验证结果 |
| “实现时顺手重构一下其他模块” | 只能改当前 change 需要的范围；额外重构必须记录原因或另开 change |

---

## 红旗警告

出现以下情况必须停下来修正计划或记录风险：

- `tasks.md` 没有可勾选任务
- 任务没有验收标准
- 实现需要修改未在 design/spec 中提到的模块边界
- 测试失败但仍想标记任务完成
- 发现需求不清楚却继续猜测实现

---

## 必须提供的证据

- 当前 change-id
- 本次处理的任务编号或任务标题
- 修改文件列表
- 测试或验证命令及结果
- 更新过的 `.sdc/changes/active/<change-id>/tasks.md` 和 `notes.md`

---

## 输出格式

```text
🚀 SDC Apply
==================================================

## 当前 Change
<change-id>

## 本次执行任务
- ...

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
