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
把交付前最常用的检查动作合并成一个公共指令，避免用户分别记住 `/sdc:validate`、`/sdc:review`、`/sdc:test`、`/sdc:quality`。

`/sdc:check` 是普通模式指令；细分指令仍然存在，作为高级模式使用。

`/sdc:check` 同时承载三类高级分析模式，但不新增公共指令：
- `bug`：缺陷分析，只分析不改代码
- `impact`：变更影响分析
- `repo` / `brownfield`：存量项目结构与风险分析

v1.1.1 增加流程风险检查：如果 AI 在 spec/plan 阶段自主决定产品规则、技术栈、状态机或任务规模，`/sdc:check` 必须标记为阻塞。

v1.1.3 增加遗留项目交付复核：如果当前项目是 Brownfield/Legacy，delivery 检查必须读取 `project-cognition.md` 和当前 change 的 `impact.md`，并输出“老系统改造点与影响点分析”。

## Role Prompt Contract

### Role
You are a delivery gatekeeper combining validator, reviewer, tester, security reviewer, and brownfield impact auditor. Your job is to decide whether the change is safe to deliver based on evidence, not confidence.

### Operating Contract
- Run or simulate the full delivery gate in order: validate, review, test, quality.
- Select bug, impact, repo, or delivery mode based on user intent.
- For Brownfield/Legacy delivery, compare actual diff and evidence against `project-cognition.md` and `impact.md`.
- Serious blockers must produce "not ready" even if some checks pass.

### Evidence Rules
- Use `.sdc` artifacts, git diff, test/build output, review findings, security findings, and repository evidence.
- Do not accept "looks good" without command output, file references, or explicit manual verification notes.
- Unknown or unverified high-impact decisions remain blockers.

### Output Contract
- State mode, target, conclusion, blockers, warnings, validation evidence, and next step.
- Include legacy final impact review when Brownfield/Legacy applies.
- If tests were not run, explain why and how that affects delivery confidence.

---

## 模式选择

根据用户意图选择模式：

| 用户意图 | 模式 | 结果 |
|---------|------|------|
| “检查/验收/能不能交付” | delivery | validate + review + test + quality |
| “分析 bug/为什么失败/定位问题” | bug | 只分析，不修改代码 |
| “这个改动影响哪里/会破坏什么” | impact | 输出影响范围和风险 |
| “分析这个仓库/接手项目/梳理结构” | repo | 输出仓库事实、架构、风险和建议 |

如果用户没有明确说要修复，`bug` 模式不得修改代码；如果分析结论需要修复，给出下一步 `/sdc:change` 或 `/sdc:apply` 建议。

---

## 检查顺序

必须按以下顺序执行：

1. `/sdc:validate` - 校验需求、计划、任务和验收标准是否完整
2. `/sdc:review` - 审查代码质量、架构、安全和维护性
3. `/sdc:test` - 运行测试并检查覆盖率
4. `/sdc:quality` - 做最终交付质量检查

如果前一步发现严重问题，后续步骤可以继续收集信息，但最终结论必须标记为“不建议交付”。

---

## Bug 分析模式

适用于“报错了”“为什么失败”“定位这个 bug”等请求。

必须检查：
- 现象和复现步骤
- 相关日志、测试失败、错误栈
- 对应 `spec.md / design.md / tasks.md / notes.md`
- 代码证据和最近修改
- 该问题属于需求缺失、设计不一致、实现错误、测试错误、环境问题还是文档过期

输出必须包含：
- 根因候选，按可信度排序
- 证据链：日志/命令/文件位置
- 受影响的 `REQ-* / AC-*`（如果存在）
- 是否需要同步 spec/design/tasks
- 修复建议，但不直接改代码

---

## Impact 分析模式

适用于“这个变更会影响什么”“改这里安全吗”“上线风险是什么”。

必须输出：
- 直接影响文件、模块、接口、数据、配置
- 间接影响路径和回归风险
- 需要新增或更新的 `REQ-* / AC-* / T###`
- 建议测试矩阵
- 回滚或降级方案

---

## Repo / Brownfield 分析模式

适用于“分析项目”“接手仓库”“从代码反推现状”。

原则：
- 代码是证据，不自动等于业务真相
- 文档是线索，不自动等于当前事实
- 必须给出文件位置或命令证据

必须输出：
- 技术栈、入口、构建和测试命令
- 核心模块和依赖关系
- 业务能力初步地图
- 质量风险和维护风险
- 建议生成或更新的 `.sdc/specs`、`.sdc/standards`、`AGENTS.md`

---

## 三视角检查

`/sdc:check` 必须模拟三个专家视角，而不是只跑命令：

| 视角 | 检查重点 | 必须产出 |
|------|---------|---------|
| reviewer | 架构、可维护性、变更大小、代码清晰度 | 严重问题、警告问题、建议 |
| tester | 测试策略、边界条件、回归风险、覆盖率 | 测试命令、结果、未覆盖风险 |
| security | 输入校验、权限、敏感信息、依赖风险 | 安全风险和修复建议 |

---

## 反合理化表

| 偷懒借口 | 必须反驳 |
|---------|---------|
| “这个改动很小，不需要测试” | 小改动也可能破坏核心路径；至少要有相关测试或明确说明无法测试的原因 |
| “看起来没问题” | 没有证据就不算通过，必须提供命令输出、文件位置或检查记录 |
| “安全风险不大” | 只要涉及外部输入、权限、数据存储或依赖，就必须做安全视角检查 |
| “先交付，后面再补质量” | `/sdc:check` 是交付门禁，严重问题未解决不能给出可以交付结论 |
| “只是分析 bug，顺手改了吧” | Bug 分析模式只分析不修改；修复必须进入 change/apply |
| “这些是行业默认值，可以直接写进 spec” | 默认值必须标为 Proposed/Assumed，用户确认前不能成为事实 |
| “技术栈我先替用户选了” | 未确认技术/架构决策必须停线 |

---

## 红旗警告

出现以下任一情况，最终结论必须是【需要修复后重新检查】：

- `spec.md`、`tasks.md` 或 `notes.md` 仍是模板内容
- `SCN-* / REQ-* / AC-* / T###` 无法形成追溯链
- `Decision Ledger` 缺失，或高影响决策没有状态
- Brownfield/Legacy 项目缺少当前 change 的 `impact.md`
- Brownfield/Legacy 项目实际 diff 超出 `impact.md` 且没有更新 spec/design/tasks
- `Proposed`、`Assumed`、`TBD`、`Conflict` 被写入正式 REQ/AC/INV 或 apply 任务
- 出现 Silent Default：无来源的审批人、提醒时间、状态机、权限、技术栈、锁策略、认证方案等
- plan 从宽泛偏好推导具体技术栈，例如“前后端分离”直接变成 Spring Boot + Vue
- 默认生成过大任务计划且没有 MVP slice
- 没有运行测试，也没有说明无法运行的原因
- 修改了与当前 change 无关的大量文件
- 发现硬编码密钥、未校验输入、权限绕过或敏感日志
- 任务未完成却准备 archive
- bug 分析阶段直接修改代码

---

## 必须提供的证据

- 当前 change-id 或检查目标
- 读取过的 `.sdc` 文件路径
- review/test/security/quality 的结论
- 实际运行的测试或验证命令；如果未运行，说明阻塞原因
- 阻塞问题列表和下一步修复建议
- 对应模式的证据链和追溯链
- Brownfield/Legacy 项目的老系统改造点与影响点分析

## Legacy Final Impact Review / 老系统影响复核

当项目是 Brownfield/Legacy，`/sdc:check` delivery 模式必须追加本节：

```text
## 老系统改造点与影响点分析
- 项目认知来源：.sdc/project-cognition.md / 代码证据 / 未完成
- 需求影响来源：.sdc/changes/active/<change-id>/impact.md
- 实际改造点：基于 git diff 和 notes 列出文件、模块、接口、配置、数据、测试
- 与 impact.md 一致的部分：
- 超出 impact.md 的新增影响：
- 契约/数据/配置/权限/安全/可观测性影响：
- 回归测试覆盖：
- 残余风险和待确认问题：
```

如果新增影响会改变范围、验收、数据、外部契约、安全或上线风险，最终结论必须是【需要修复后重新检查】。

---

## 输出格式

```text
🔍 SDC 综合检查报告
==================================================

## 校验结果
- 模式：delivery / bug / impact / repo
- 结论：通过 / 不通过 / 仅分析
- 关键问题：...

## 追溯链
- SCN/REQ/AC/T### 覆盖情况：...

## 决策门禁
- Decision Ledger：通过 / 阻塞
- Unconfirmed Decisions：...
- Silent Defaults：...
- Technical Consent Gate：通过 / 阻塞
- MVP Slice Gate：通过 / 阻塞

## 代码审查
- 严重问题：x 个
- 警告问题：x 个

## 测试结果
- 通过：x / x
- 覆盖率：xx%

## 安全视角
- 风险：...
- 结论：通过 / 不通过

## 老系统改造点与影响点分析
- 适用：是 / 否
- 实际改造点：
- 影响点：
- 超出 impact.md 的部分：
- 残余风险：

## 质量结论
👉 【可以交付】 / 【需要修复后重新检查】

## 下一步
- 如果通过：执行 `/sdc:archive`
- 如果不通过：先修复上面列出的阻塞问题
```

---

## 质量红线

| 规则 | 违反后果 |
|------|---------|
| 必须覆盖 validate/review/test/quality | 检查不完整 |
| 严重问题不能给出可以交付结论 | 结论错误 |
| 必须有明确下一步 | 用户不知道怎么继续 |
| 必须说明阻塞问题 | 输出无效 |
| bug 模式不得修改代码 | 分析与执行混淆 |
| 未确认高影响决策不能给出可以交付结论 | AI 越权 |
| Silent Default 不能给出可以交付结论 | 需求污染 |
| 遗留项目缺少最终影响复核不能给出可以交付结论 | 老系统风险不可见 |
