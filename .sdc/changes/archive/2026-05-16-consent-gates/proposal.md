# 2026-05-16 Consent Gates Proposal

## 背景

2026-05-15 的 SDC 实验日志显示，SDC 虽然能生成 `.sdc/` 工作区、spec 和 plan，但在需求讨论和决策边界上仍然偏弱：

- `sdc-spec` 问了问题，但更像表单收集，不是头脑风暴。
- spec 阶段询问并记录技术栈，越过了“业务先行、技术后置”的边界。
- AI 将“多级角色”“审批流程”“会议提醒”等模糊输入扩展成具体业务规则，例如审批人、自动通过、超时取消、15 分钟提醒。
- `sdc-plan` 在未确认技术选型的情况下选择了 Spring Boot、Vue、MyBatis、MapStruct、JWT 等实现方案，并生成 56 个任务。
- 这些行为没有体现 `.sdc/constitution.md` 中的“人机责任、极简、小步、显式失败、文档裁决”。

## 目标

- 增加“讨论优先/确认优先”的硬规则。
- 明确 AI 可以提出候选方案，但不能把候选方案写成已确认需求或设计。
- 在 spec、plan、validate、constitution、harness 中加入 consent gates。
- 让 `/sdc:check` 能识别“AI 自主决策过多”的流程风险。
- 更新 README/docs/changelog/package 版本，说明 v1.1.1 的边界修复。

## 非目标

- 不新增公开指令。
- 不要求用户每一步都手动确认所有细节；只对产品规则、技术栈、架构、权限、状态机、自动化行为等高影响决策设门禁。
- 不修改安装器平台路径逻辑。

## 初始场景

- SCN-01: 用户输入一个模糊需求，希望 SDC 先陪他讨论，而不是直接生成完整 spec。
- SCN-02: 用户补充“需要审批/提醒”等能力，SDC 应该先澄清业务规则，而不是补默认规则。
- SCN-03: SDC plan 发现技术栈、架构、状态机或任务规模未确认，应输出候选方案和 Stop-Line Report。
- SCN-04: SDC validate/check 应该阻止未确认假设进入 apply/archive。

## 初始需求

- REQ-01: spec 阶段必须区分 Confirmed / Proposed / Assumed / TBD / Conflict，未确认项不得写成正式 REQ/AC。
- REQ-02: spec 阶段必须支持轻量头脑风暴，先输出共识草案和待确认决策，再生成规范。
- REQ-03: plan 阶段必须有技术/架构 consent gate，不能从“前后端分离”等宽泛偏好直接推导具体技术栈。
- REQ-04: validate/check 必须把未确认业务规则、技术决策和过大任务计划列为阻塞风险。
- REQ-05: init/constitution/harness 必须把“AI 不得自主决定高影响事项”写入项目级治理规则。

## 初始验收标准

- AC-01: `skills/sdc-spec/SKILL.md` 包含 brainstorm-first、decision ledger、confirmed-only 规则。
- AC-02: `skills/sdc-plan/SKILL.md` 包含 technical consent gate、MVP slice gate、Stop-Line Report 要求。
- AC-03: `skills/sdc-validate/SKILL.md` 和 `skills/sdc-check/SKILL.md` 能识别 unconfirmed decisions。
- AC-04: `.sdc/constitution.md`、`skills/sdc-init/SKILL.md`、`skills/sdc-harness/SKILL.md` 包含 human confirmation / no silent defaults 规则。
- AC-05: README/docs/changelog/package/plugin metadata 反映 v1.1.1 的 consent-gate 修复。
- AC-06: 语法、manifest、Claude plugin validate、npm pack dry-run 全部通过。

## 风险和回滚

- 风险：规则过严导致 SDC 变慢。缓解：只对高影响决策设门禁，低影响文本组织仍可由 AI 自动处理。
- 风险：README 继续膨胀。缓解：把详细规则放到 docs，README 只描述核心原则。
- 回滚：恢复本次修改并保留实验日志分析记录。
