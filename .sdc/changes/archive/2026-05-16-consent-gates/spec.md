# Spec

## 0. 文档元信息

- 状态: Confirmed
- Change: 2026-05-16-consent-gates
- 日期: 2026-05-16
- 输入证据: `/Users/liting/Library/Mobile Documents/com~apple~CloudDocs/Desktop/跨境/2026/session-log-2026-05-15.md`

## 1. Glossary / 统一语言

| 术语 | 定义 | 状态 | 备注 |
|------|------|------|------|
| Brainstorm-first | 在生成正式 spec/plan 前先讨论目标、边界、候选方案和取舍 | Confirmed | 本次核心 |
| Consent Gate | 高影响决策进入 spec/plan/apply 前必须得到用户确认或显式授权 | Confirmed | 本次核心 |
| Decision Ledger | 记录 Confirmed/Proposed/Assumed/TBD/Conflict 的决策表 | Confirmed | 防止假设伪装成事实 |
| High-impact Decision | 产品规则、权限、状态机、自动化行为、技术栈、架构、数据模型、安全策略等 | Confirmed | 需要门禁 |
| Silent Default | AI 未说明来源和状态就写入需求或设计的默认值 | Confirmed | 必须禁止 |

## 1.1 Decision Ledger / 决策台账

| ID | 决策 | 状态 | 依据来源 | 是否允许进入 REQ/AC | 下一步 |
|----|------|------|----------|----------------------|--------|
| DEC-01 | 增加 Brainstorm-first 和 Consent Gate | Confirmed | 用户反馈实验问题 | 是 | 实施 |
| DEC-02 | 不新增公开 `/sdc:brainstorm` 指令 | Confirmed | 项目“少指令”原则 | 是 | 复用 spec/change/plan |
| DEC-03 | 高影响决策必须确认后才能进入 apply | Confirmed | session log + constitution | 是 | 写入 skills |

## 2. 背景与目标

实验日志说明 SDC v1.1 的 traceability 还不够。追溯链能追到文件和任务，但如果源头是 AI 自主决策，追溯链只会把错误传播得更漂亮。因此 v1.1.1 需要在源头增加“讨论和确认”的门禁。

## 3. 场景与需求

### SCN-01: 模糊需求进入 spec

- 目标: SDC 先和用户讨论需求边界，再生成正式 spec。
- 触发条件: 用户输入类似“我要做会议室预约系统”。
- 主流程: SDC 读取 project/constitution -> 输出理解、候选范围、关键问题 -> 用户确认 -> 生成 spec。
- 异常流程: 用户要求“先按你的判断”，SDC 可以提出建议，但必须标为 Proposed/Assumed，不得标为 Confirmed。
- 关联需求: REQ-01, REQ-02

### REQ-01: Decision Ledger 状态隔离

- 业务规则: spec 中所有高影响决策必须标记状态。
- 边界条件: `Proposed`、`Assumed`、`TBD`、`Conflict` 不得进入正式 `REQ-*`、`AC-*` 或 `INV-*`，除非明确标注“Draft，不可 apply”。
- 关联场景: SCN-01

### REQ-02: Brainstorm-first 输出

- 业务规则: 信息不足时，SDC 必须先输出短轮头脑风暴，而不是直接生成完整规范。
- 边界条件: 一轮最多 3 个关键问题，但必须覆盖目标、范围、验收或高影响决策。
- 关联场景: SCN-01

### SCN-02: 用户提出审批/提醒等新能力

- 目标: SDC 不自行发明审批人、自动通过、超时策略、提醒时间等规则。
- 触发条件: 用户只说“需要审批流程”“需要会议提醒功能”。
- 主流程: SDC 列出需要确认的业务决策和候选选项 -> 用户确认 -> 写入 spec。
- 异常流程: 用户未确认时，相关规则保留为 TBD/Proposed。
- 关联需求: REQ-01, REQ-02, REQ-04

### SCN-03: plan 遇到未确认技术栈

- 目标: SDC 不从宽泛偏好推导具体实现方案。
- 触发条件: spec 只有“前后端分离”或没有技术约束。
- 主流程: SDC 输出技术候选方案、取舍、需要确认的问题和 Stop-Line Report，不生成完整任务。
- 异常流程: 用户明确授权“按你的判断选”，SDC 仍必须记录选择理由、替代方案、风险和回滚。
- 关联需求: REQ-03

### REQ-03: Technical Consent Gate

- 业务规则: 技术栈、架构风格、认证方案、ORM、状态机、异步任务、通知机制等不得在未确认时落为最终设计。
- 边界条件: 可以输出候选方案，但不能把候选方案拆成 apply 任务。
- 关联场景: SCN-03

### SCN-04: check/validate 拦截流程风险

- 目标: 未确认决策不能进入 apply/archive。
- 触发条件: spec/design/tasks 中出现 Proposed/Assumed/TBD/Conflict 或过大任务计划。
- 主流程: validate/check 输出阻塞项和修复建议。
- 关联需求: REQ-04, REQ-05

### REQ-04: Unconfirmed Decision Blocker

- 业务规则: validate/check 必须将未确认高影响决策、silent defaults、技术栈越权、过大任务计划标记为阻塞。
- 边界条件: 低影响措辞、文档结构和示例文字不需要用户确认。
- 关联场景: SCN-04

### REQ-05: Constitution/Harness Governance

- 业务规则: 初始化和 harness 必须把“AI 不得自主决定高影响事项”写入治理规则。
- 边界条件: 不要求全局禁止 AI 建议，只禁止未确认建议落成事实。
- 关联场景: SCN-04

## 4. Acceptance Criteria / 验收标准

### AC-01: spec 阶段不再把假设写成事实

Given 用户只输入模糊需求
When 触发 `/sdc:spec`
Then SDC 先输出 brainstorm / decision ledger，并把未确认项标为 Proposed/Assumed/TBD，而不是写成 Confirmed REQ/AC

### AC-02: 新能力需要业务规则确认

Given 用户只说“需要审批流程和提醒”
When SDC 更新 spec
Then 必须先询问审批人、审批状态、超时策略、提醒对象、提醒时间等关键规则，或将其列为 TBD

### AC-03: plan 不得自主选技术栈

Given spec 没有明确 Spring/Vue/MyBatis/JWT 等技术选型
When 触发 `/sdc:plan`
Then SDC 输出技术候选和 Stop-Line Report，不能直接生成基于某一技术栈的完整任务清单

### AC-04: validate/check 能拦截未确认决策

Given spec/design/tasks 含 Proposed/Assumed/TBD/Conflict 高影响项
When 触发 `/sdc:validate` 或 `/sdc:check`
Then 结论必须是不通过或需要确认后再继续

### AC-05: constitution/harness 约束 AI 决策权

Given 新项目执行 `/sdc:init` 或 `/sdc:harness`
When 查看 constitution 或 AGENTS.md
Then 能看到 human confirmation、no silent defaults、decision ledger、stop-line 的规则

### AC-06: 发布校验通过

Given 本次修改完成
When 运行基础验证
Then Python/Node 语法、JSON manifest、Claude plugin validate、npm pack dry-run 通过

## 5. 验证策略

| AC | 验证方式 | 需要的测试/检查 | 备注 |
|----|----------|-----------------|------|
| AC-01 | 文档检查 | `rg "Decision Ledger|Brainstorm" skills/sdc-spec/SKILL.md` | spec |
| AC-02 | 文档检查 | `rg "审批|提醒|TBD|Proposed" skills/sdc-spec/SKILL.md` | 防默认值 |
| AC-03 | 文档检查 | `rg "Technical Consent Gate|Stop-Line" skills/sdc-plan/SKILL.md` | plan |
| AC-04 | 文档检查 | `rg "Unconfirmed|Silent Default|TBD" skills/sdc-validate/SKILL.md skills/sdc-check/SKILL.md` | validate/check |
| AC-05 | 文档检查 | `rg "Human Confirmation|No Silent Defaults" .sdc/constitution.md skills/sdc-init/SKILL.md skills/sdc-harness/SKILL.md` | governance |
| AC-06 | 命令验证 | py_compile, node --check, JSON parse, claude validate, npm pack | 发布门禁 |

## 6. 风险、假设与待确认项

| ID | 类型 | 描述 | 影响 | 处理建议 |
|----|------|------|------|----------|
| RISK-01 | 风险 | 门禁太多会降低速度 | 用户体验变重 | 只限制高影响决策 |
| RISK-02 | 风险 | 模型仍可能忽略规则 | 规则不生效 | 在 spec/plan/validate/check 多点重复约束 |
| ASM-01 | 假设 | 用户希望我们直接优化项目 | 本次会修改 skills/docs | 已按“按照判断升级”的历史偏好执行 |

## 7. 追溯关系矩阵

| SCN | REQ | AC | 风险/假设 |
|-----|-----|----|-----------|
| SCN-01 | REQ-01, REQ-02 | AC-01 | RISK-01 |
| SCN-02 | REQ-01, REQ-02, REQ-04 | AC-02, AC-04 | RISK-02 |
| SCN-03 | REQ-03 | AC-03 | RISK-01 |
| SCN-04 | REQ-04, REQ-05 | AC-04, AC-05, AC-06 | RISK-02, ASM-01 |
