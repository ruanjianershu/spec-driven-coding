---
name: sdc-validate
description: "Validate SDC current or active change files for structure, acceptance criteria, tasks, tests, and non-template content."
---

# Skill: SDC 规范校验 /sdc:validate

## 触发条件
当用户输入以下任一内容时，自动触发本技能：
- `/sdc:validate`
- "校验 SDC"
- "检查需求完整性"
- "能不能开始实现"
- "能不能归档"

## 核心使命
校验 `.sdc/current/` 或 `.sdc/changes/active/<change-id>/` 是否满足进入下一阶段的最低质量门槛。这是 SDC 对 OpenSpec validate 的轻量吸收：不追求复杂规则引擎，只检查会影响交付的核心缺口。

v1.1 以后，校验重点从“文件是否存在”升级为“裁决链和追溯链是否成立”：

```text
.sdc/constitution.md -> spec.md -> design.md/plan.md -> tasks.md -> 验证证据
SCN-* -> REQ-* -> AC-* -> T###
```

---

## 校验范围

### 全局校验
检查：
- `.sdc/constitution.md`
- `.sdc/standards/`
- `AGENTS.md`（如存在）

### current 校验
检查：
- `.sdc/current/spec.md`
- `.sdc/current/plan.md`
- `.sdc/current/tasks.md`
- `.sdc/current/apply.md`

### change 校验
检查：
- `.sdc/changes/active/<change-id>/proposal.md`
- `.sdc/changes/active/<change-id>/tasks.md`
- `.sdc/changes/active/<change-id>/spec.md`
- 必要时检查 `design.md` 和 `notes.md`

---

## 必须检查的规则

| 类型 | 规则 |
|------|------|
| 结构 | 必须有 proposal/tasks/spec 或 current/spec/plan |
| 治理 | 必须有 `.sdc/constitution.md`，且 AGENTS.md 不得与其冲突 |
| 规格 | spec 必须包含 Glossary、业务不变量、SCN/REQ/AC、追溯矩阵 |
| 验收 | 必须有明确验收标准，优先使用 Given/When/Then |
| 任务 | tasks 必须包含 `T### [REQ-*] [AC-*] [Phase] [Size]` 复选框任务 |
| 任务粒度 | 任务只能是 Size S/M，不能出现 Size L |
| 顺序 | 测试任务必须先于对应实现任务 |
| 测试 | 必须有验证策略或验证任务 |
| 内容 | 不能只保留模板占位 |
| 风险 | 重要变更必须有风险和回滚说明 |
| 追溯 | 每个 REQ/AC 必须能追到任务或明确说明未覆盖原因 |

---

## 输出格式

```text
🔍 SDC 校验报告
==================================================

## 校验目标
current / change-id

## ✅ 通过项
- ...

## 🔗 追溯检查
- SCN/REQ/AC 覆盖：...
- T### 覆盖：...
- 缺口：...

## ❌ 必须修复
| 文件 | 问题 | 修复建议 |
|------|------|---------|

## ⚠️ 建议完善
| 文件 | 问题 | 建议 |
|------|------|------|

## 结论
👉 【通过，可以进入下一阶段】 / 【不通过，需要补齐】
```

---

## 质量红线

| 规则 | 违反后果 |
|------|---------|
| 不能只说“看起来可以” | 校验无效 |
| 必须指出具体文件 | 输出无效 |
| 严重缺失时不能放行 | 结论错误 |
| 必须给出修复建议 | 输出无效 |
| 必须有明确结论 | 输出无效 |
| 追溯链断裂不能放行到 apply/archive | 规范失效 |
