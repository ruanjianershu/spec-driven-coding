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
