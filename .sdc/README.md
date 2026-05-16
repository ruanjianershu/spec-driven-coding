# SDC Workspace

这个目录记录项目的规范驱动开发过程。所有需求、计划、实现记录、审查、测试和质量检查都应该沉淀在这里。

## 目录

- `project.md` - 项目长期背景、目标用户、技术约束和验证命令
- `project-cognition.md` - 遗留项目整体认知，基于代码证据建立维护地图
- `constitution.md` - 项目最高工程裁决规则
- `current/` - 当前正在推进的一次需求迭代，包含 discovery/spec/plan/tasks/apply
- `changes/active/` - 正在推进的需求变更，每个变更一个子目录
- `changes/archive/` - 已完成归档的需求变更
- `specs/` - 已稳定的业务规范和能力说明
- `standards/` - 项目长期开发规范，约束人和 AI 怎么写代码
- `decisions/` - 架构决策记录
- `reviews/` - 代码审查记录
- `reports/` - 测试、质量、bug、impact、repo-analysis 和交付报告
- `templates/` - discovery、需求迭代、项目认知、影响面、停线和分析模板

## 推荐流程

1. `/sdc:change <name>` 创建 `changes/active/<name>/`
2. 需求不确定时先进入 Discovery Gate，更新 `discovery.md`
3. `/sdc:spec` 将已确认 discovery 收敛为 SCN/REQ/AC
4. 遗留项目在需求确认后先更新当前 change 的 `impact.md`
5. `/sdc:plan` 生成 proposal/spec/design/tasks
6. `/sdc:apply` 执行实现并记录过程
7. `/sdc:check` 综合校验、审查、测试和质量检查
8. `/sdc:archive <name>` 归档到 `changes/archive/`

## 三类核心资产

- `specs/` - 业务规范：项目应该做什么
- `changes/` - 需求迭代：这次为什么改、怎么改、如何验收
- `standards/` - 开发规范：代码、测试、架构、安全、Git 和 AI 协作规则

## SDC v1.1 纪律内核

```text
治理优先级：.sdc/constitution.md > AGENTS.md > 对话即时要求
事实优先级：discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code
追溯链：SCN-* -> REQ-* -> AC-* -> T### -> 验证证据
确认门禁：高影响决策必须 Confirmed，不能 Silent Default
探索门禁：不确定需求必须先 discovery，再 spec
```
