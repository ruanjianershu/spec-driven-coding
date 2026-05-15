# SDC Workspace

这个目录记录项目的规范驱动开发过程。所有需求、计划、实现记录、审查、测试和质量检查都应该沉淀在这里。

## 目录

- `project.md` - 项目长期背景、目标用户、技术约束和验证命令
- `constitution.md` - 项目最高工程裁决规则
- `current/` - 当前正在推进的一次需求迭代
- `changes/active/` - 正在推进的需求变更，每个变更一个子目录
- `changes/archive/` - 已完成归档的需求变更
- `specs/` - 已稳定的业务规范和能力说明
- `standards/` - 项目长期开发规范，约束人和 AI 怎么写代码
- `decisions/` - 架构决策记录
- `reviews/` - 代码审查记录
- `reports/` - 测试、质量、bug、impact、repo-analysis 和交付报告
- `templates/` - 需求迭代、停线和分析模板

## 推荐流程

1. `/sdc:change <name>` 创建 `changes/active/<name>/`
2. `/sdc:plan` 生成 proposal/spec/design/tasks
3. `/sdc:apply` 执行实现并记录过程
4. `/sdc:check` 综合校验、审查、测试和质量检查
5. `/sdc:archive <name>` 归档到 `changes/archive/`

## 三类核心资产

- `specs/` - 业务规范：项目应该做什么
- `changes/` - 需求迭代：这次为什么改、怎么改、如何验收
- `standards/` - 开发规范：代码、测试、架构、安全、Git 和 AI 协作规则

## SDC v1.1 纪律内核

```text
治理优先级：.sdc/constitution.md > AGENTS.md > 对话即时要求
事实优先级：spec.md > design.md/plan.md > tasks.md > code
追溯链：SCN-* -> REQ-* -> AC-* -> T### -> 验证证据
```
