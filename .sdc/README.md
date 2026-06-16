# SDC Workspace

这个目录记录项目的规范驱动开发过程。所有需求、计划、实现记录、审查、测试和质量检查都应该沉淀在这里。

## 目录

- `project.md` - 项目长期背景、目标用户、技术约束和验证命令
- `project-cognition.md` - 遗留项目整体认知，基于代码证据建立维护地图
- `common-ground.md` - 共同认知层：区分 ESTABLISHED / WORKING / OPEN，防止 AI 隐性假设
- `expert-routing.md` - 专家路由层：按任务自动选择产品、架构、数据、测试、安全等内部专家视角
- `constitution.md` - 项目最高工程裁决规则
- `knowledge/` - 项目确认知识库，分为产品知识和技术知识
- `memory/` - 项目记忆与候选知识，默认不高于 confirmed knowledge
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

1. `/sdc:change <name>` 创建 `changes/active/<name>/` 的轻量 Discovery Open 草稿
2. 需求不确定时只更新 `discovery.md`、Draft `proposal.md` 和简短 `notes.md`
3. 需求确认后读取 `common-ground.md`、`knowledge/index.md` 和相关产品/技术知识，再生成 spec
4. `sdc-spec` 将已确认 discovery 收敛为 SCN/REQ/AC
5. 遗留项目在需求确认后先更新当前 change 的 `impact.md`
6. `/sdc:plan` 通过 `expert-routing.md` 选择内部专家视角，生成 design/tasks/context-pack
7. `/sdc:apply` 执行实现，记录验证证据和 `knowledge-candidates.md`
8. `/sdc:check` 综合校验、审查、测试、质量和知识漂移
9. `/sdc:archive <name>` 归档到 `changes/archive/`，并运行 Knowledge Compact Gate 判断长期知识沉淀

## 三类核心资产

- `specs/` - 业务规范：项目应该做什么
- `changes/` - 需求迭代：这次为什么改、怎么改、如何验收
- `common-ground.md` - 共同认知：哪些事实已确认、哪些只是工作假设、哪些必须先问
- `expert-routing.md` - 专家路由：不增加用户指令，由 AI 根据场景选择内部专家参考
- `knowledge/` - 项目知识：产品事实、业务规则、技术事实和运行方式
- `Artifact Output Contract` - 阶段输入输出契约：按触发条件要求流程图、接口/数据契约、测试矩阵和上线清单
- `standards/` - 开发规范：代码、测试、架构、安全、Git 和 AI 协作规则
- `standards/company/` - 可选公司/团队规范包，通过索引按需读取
- `memory/` - 项目记忆：候选知识、经验、流程和可回顾的工作片段

## SDC v1.2 纪律内核

```text
治理优先级：.sdc/constitution.md > AGENTS.md > 对话即时要求
事实优先级：discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code
追溯链：SCN-* -> REQ-* -> AC-* -> T### -> 验证证据
确认门禁：高影响决策必须 Confirmed，不能 Silent Default
探索门禁：不确定需求必须先 discovery，再 spec
知识门禁：change/plan/apply 前读取 knowledge index；memory 只能辅助召回，不能覆盖 confirmed knowledge
共同认知门禁：OPEN 不能驱动 final spec/plan/apply；WORKING 不能静默升级为 ESTABLISHED
专家路由门禁：用户只选 SDC 阶段，AI 内部选择专家视角并在 context-pack/check/archive 中披露
输出契约门禁：触发流程/API/数据/UX/测试/部署/AI 参与风险时，必须有对应产物或 N/A 证据
```
