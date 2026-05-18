---
name: sdc-check
description: "Combined delivery check that runs validate, review, test, and quality perspectives with evidence gates."
---

# Skill: SDC 综合检查 /sdc:check

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `/sdc:check`
- "SDC 检查"
- "检查一下"
- "验收一下"
- "能不能交付"

## 核心使命

把交付前最常用的检查动作合并成一个公共指令，避免用户分别记住 `sdc-validate`、`sdc-review`、`sdc-test`、`sdc-quality`。

`/sdc:check` 还承载 `bug`、`impact`、`repo/brownfield` 三类分析模式。

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-check`.
- Delivery gates and modes: `../sdc-shared/delivery-gates.md`.
- Shared decision and traceability rules: `../sdc-shared/workflow-standards.md`.
- Brownfield final impact review: `../sdc-shared/legacy-impact-gate.md`.

## 模式选择

| 用户意图 | 模式 | 行为 |
| --- | --- | --- |
| 检查、验收、能不能交付 | delivery | validate + review + test + quality perspectives |
| 分析 bug、为什么失败、定位问题 | bug | 只分析，不改代码，除非用户明确要求修复 |
| 这个改动影响哪里、上线风险 | impact | 输出影响范围、回归风险和测试建议 |
| 分析仓库、接手项目、遗留系统 | repo | 输出代码证据驱动的项目认知 |

## Delivery 检查顺序

1. Validate：结构、追溯、决策、影响门禁。
2. Review：代码质量、架构、安全、维护性、影响面。
3. Test：测试命令、覆盖 AC、边界和回归。
4. Quality：用户体验、文档、安全、性能、可维护性、交付准备。

前一步有严重问题时，后续可以继续收集信息，但最终结论必须是“不建议交付”。

## Brownfield/Legacy 复核

delivery 模式必须比较：

- `.sdc/project-cognition.md`
- 当前 change 的 `impact.md`
- 实际 git diff
- notes 和验证证据

如果实际修改超出 `impact.md`，且影响范围、验收、契约、数据、权限、安全或上线风险变化，必须阻塞交付。

## 输出格式

```text
🔍 SDC 综合检查报告
==================================================

## 校验结果
- 模式：delivery / bug / impact / repo
- 结论：通过 / 不通过 / 仅分析
- 关键问题：

## 追溯链
- ...

## 决策门禁
- Decision Ledger：
- Silent Defaults：
- Technical Consent Gate：
- Legacy Impact Gate：

## 代码审查
- 严重问题：
- 警告问题：

## 测试结果
- ...

## 安全视角
- ...

## 老系统改造点与影响点分析
- 适用：
- 实际改造点：
- 影响点：
- 超出 impact.md 的部分：
- 残余风险：

## 质量结论
👉 【可以交付】 / 【需要修复后重新检查】

## 下一步
- ...
```

## 质量红线

- delivery 模式必须覆盖 validate/review/test/quality 视角。
- 严重问题不能给出可以交付结论。
- bug 模式默认不得修改代码。
- 未确认高影响决策或 Silent Default 不能放行。
- 遗留项目缺少最终影响复核不能放行。
