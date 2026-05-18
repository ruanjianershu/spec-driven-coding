---
name: sdc-review
description: "Review code like a senior engineer across architecture, quality, security, performance, and maintainability."
---

# Skill: SDC 代码审查 sdc-review

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `sdc-review`
- "帮我审查代码"
- "代码质量检查"
- "看看有没有问题"

## 核心使命

像资深工程师一样审查实际 diff 和相关上下文，优先发现具体缺陷、架构风险、安全风险、兼容性问题和维护成本。

Brownfield/Legacy 项目还必须复核实际改动是否符合当前 change 的 `impact.md`。

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-review`.
- Review gate: `../sdc-shared/delivery-gates.md`.
- Shared evidence and stop-line rules: `../sdc-shared/workflow-standards.md`.
- Legacy impact review: `../sdc-shared/legacy-impact-gate.md`.

## 审查范围

必须覆盖：

- Correctness：行为是否满足 REQ/AC，是否有边界遗漏。
- Architecture：模块边界、依赖方向、职责拆分、过度设计。
- Security：输入校验、权限、敏感信息、注入、危险 API。
- Data and contracts：数据迁移、公共接口、兼容性。
- Performance：明显低效、N+1、内存或并发风险。
- Maintainability：命名、重复、复杂度、错误处理、注释质量。
- Legacy impact：实际 diff 是否超出 `impact.md`。

## Findings 规则

- Findings 先行，按严重程度排序。
- 每个 finding 必须有文件/行号、影响、修复建议。
- 不要编造问题；没有问题就明确说没有发现阻塞问题。
- 将 confirmed defects、risks、optional improvements 分开。
- 测试缺口和上下文限制要明确写出。

## 输出格式

```text
🔍 SDC 代码审查报告
==================================================

## 严重问题
| 文件 | 位置 | 问题 | 影响 | 修复建议 |

## 警告问题
| 文件 | 位置 | 问题 | 影响 | 修复建议 |

## 可选改进
- ...

## 老系统改造点与影响点分析
- 适用：
- impact.md 来源：
- 实际改造点：
- 与 impact.md 不一致或新增的影响：
- 残余风险：

## 测试/上下文缺口
- ...

## 结论
👉 ...
```

## 质量红线

- 问题必须具体到文件和行号。
- 严重问题必须说明后果和修复建议。
- 无问题时不得为了凑数编造 finding。
- 遗留项目实际 diff 超出 `impact.md` 必须标记为严重风险。
