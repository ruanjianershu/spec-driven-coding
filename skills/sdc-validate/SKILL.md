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

---

## 校验范围

### current 校验
检查：
- `.sdc/current/spec.md`
- `.sdc/current/plan.md`
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
| 验收 | 必须有明确验收标准 |
| 任务 | tasks 必须包含复选框任务 |
| 测试 | 必须有测试计划或验证任务 |
| 内容 | 不能只保留模板占位 |
| 风险 | 重要变更必须有风险和回滚说明 |

---

## 输出格式

```text
🔍 SDC 校验报告
==================================================

## 校验目标
current / change-id

## ✅ 通过项
- ...

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
