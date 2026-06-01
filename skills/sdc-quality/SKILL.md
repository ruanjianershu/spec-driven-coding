---
name: sdc-quality
description: "Perform final delivery quality gate across UX, docs, code quality, security, performance, and maintainability."
---

# Skill: SDC 全面质量检查 sdc-quality

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `sdc-quality`
- "最终检查"
- "可以交付了吗"
- "质量检查"

## 核心使命

交付前的最后质量门禁。它不只看代码是否能跑，还要判断用户是否能使用、文档是否清楚、风险是否可接受、验证证据是否充分。

## Reference Loading

Load only what is needed:

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-quality`.
- Quality gate: `../sdc-shared/delivery-gates.md`.
- Evidence and stop-line rules: `../sdc-shared/workflow-standards.md`.

## 前置检查

确认已有或等价具备：

- spec evidence。
- plan/design evidence。
- apply/implementation notes。
- review evidence。
- test evidence。
- context-pack and knowledge-candidates evidence.

缺少关键证据时，不能给出可交付结论。

## 检查维度

- UX / user flow：核心流程可用，错误信息清晰。
- Documentation：安装、更新、使用、配置、FAQ 或限制说明足够。
- Code quality：格式、调试代码、TODO、硬编码路径、可维护性。
- Security：敏感信息、输入输出、权限、依赖风险。
- Performance：启动、核心路径、资源使用的明显风险。
- Operability：配置、日志、部署/发布、回滚或降级。
- Validation evidence：测试、手动验证、截图或命令输出。
- Knowledge readiness：本次变更是否需要更新产品知识、技术知识、memory、standards 或 AGENTS.md。

## 输出格式

```text
✅ SDC 最终质量检查报告
==================================================

## 检查概览
- 结论：可以交付 / 需要修复后重新检查
- 主要阻塞：

## 维度结果
| 维度 | 结果 | 证据 | 风险 |

## 冒烟测试 / 用户主路径
- ...

## 必须修复
| 问题 | 严重程度 | 最小修复 |

## 建议优化
- ...

## 下一步
👉 ...
```

## 质量红线

- 任何严重问题都不能交付。
- 必须说明验证证据。
- 无法验证的关键路径必须标为风险。
- 必须给出明确 ship / no-ship 结论。
