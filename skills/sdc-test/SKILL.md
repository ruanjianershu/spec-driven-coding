---
name: sdc-test
description: "Run and assess tests with coverage, failure details, boundary cases, and improvement suggestions."
---

# Skill: SDC 测试驱动 /sdc:test

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `/sdc:test`
- "运行测试"
- "测试一下"
- "写测试"

## 核心使命

证明当前 change 满足 acceptance criteria、边界条件、回归路径和失败模式。测试的目标是发现问题，而不是只追求覆盖率数字。

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-test`.
- Test gate: `../sdc-shared/delivery-gates.md`.
- Traceability and evidence rules: `../sdc-shared/workflow-standards.md`.

## 执行步骤

1. 读取当前 spec/tasks/notes，识别 REQ/AC。
2. 确认已有测试覆盖哪些 AC。
3. 根据项目实际工具运行相关测试。
4. 如果不能运行测试，说明阻塞原因和替代验证路径。
5. 分析失败、缺失覆盖、边界、错误、安全、兼容性和回归风险。
6. 给出需要新增或修正的测试建议。

## 测试层级

按项目实际情况覆盖：

- Unit：单函数/类行为，边界和错误分支。
- Integration：模块协作、API 契约、数据流转、外部依赖替身。
- End-to-end / smoke：用户主路径或关键 CLI/API 流程。
- Regression：老系统或历史行为保护。

## 输出格式

```text
🧪 SDC 测试报告
==================================================

## 测试命令
- ...

## 结果概览
- 通过：
- 失败：
- 未运行：

## AC 覆盖
| AC | 测试/验证 | 结果 | 缺口 |

## 失败详情
| 测试 | 错误 | 复现方式 |

## 风险与建议
- ...

## 结论
👉 已充分验证 / 未充分验证
```

## 质量红线

- 测试失败不能进入下一阶段。
- 未运行测试必须说明原因和风险。
- AC 未覆盖必须明确标出。
- 覆盖率不能替代行为验证。
- 必须覆盖关键异常和边界情况，或说明无法覆盖的风险。
