---
name: sdc-change
description: "Create a focused requirement change under .sdc/changes/active with proposal, spec, design, tasks, and notes."
---

# Skill: SDC 需求变更创建 /sdc:change

## 触发条件
当用户输入以下任一内容时，自动触发本技能：
- `/sdc:change`
- "创建需求变更"
- "新建一次迭代"
- "开始一个 change"
- "记录这次需求"

## 核心使命
创建一次独立、可追踪、可验证的需求迭代。它吸收 OpenSpec 的核心 change 思路，但只保留 SDC 需要的最小闭环：为什么改、改什么、怎么做、怎么验收、最后如何归档。

`/sdc:change` 不是直接把一句话需求写成文件，而是先判断需求确定性。需求清楚时创建可执行 change；需求不清楚时进入 Discovery Gate，先发散、比较、收敛，再进入 `/sdc:spec`。

v1.1 起，change 创建阶段要为后续追溯预留结构：`SCN-* -> REQ-* -> AC-* -> T###`。不要求一开始完整，但必须避免只创建空白模板。

v1.1.1 起，change 创建阶段还要识别高影响决策，并将未确认项标为 Proposed/Assumed/TBD，不能直接写成已确认范围。

v1.1.2 起，Discovery Gate 是 SDC 内置能力，不依赖 Superpowers。SDC 可以吸收通用 brainstorm 的发散方法，但输出必须收敛到 `discovery.md -> Decision Ledger -> Confirmed spec`。

---

## 标准输出/落盘结构

每次变更必须在 `.sdc/changes/active/` 下创建一个目录：

```text
.sdc/changes/active/YYYY-MM-DD-short-name/
├── discovery.md
├── proposal.md
├── tasks.md
├── design.md
├── spec.md
└── notes.md
```

## 文件职责

| 文件 | 作用 |
|------|------|
| `discovery.md` | 需求不确定时的探索记录：当前理解、候选方向、取舍、MVP、问题、决策台账 |
| `proposal.md` | 背景、目标、非目标、验收标准、风险 |
| `tasks.md` | 可执行任务清单，每项必须关联 REQ/AC 并可验收 |
| `design.md` | 关键技术设计、数据变化、替代方案 |
| `spec.md` | 最终需求规范，完成后可沉淀到 `.sdc/specs/` |
| `notes.md` | 实现过程、问题、验证记录 |

---

## Discovery Gate / 需求探索门禁

当用户的需求还不够清晰时，先进入 Discovery Gate，不急着生成 Confirmed spec，也不直接生成 plan。讨论目标是把想法从不确定状态推进到可确认的 MVP change。

### 需求确定性判定

只有同时满足以下条件，才能跳过 Discovery Gate 进入 `/sdc:spec`：
- 目标用户或受影响对象明确
- 业务目标明确
- In Scope / Out of Scope 基本明确
- 至少一个核心场景可描述
- 验收方式初步明确
- 高影响决策没有明显未知项，或已进入 Decision Ledger 且为 Confirmed

如果任一条件不满足，必须进入 Discovery Gate。

### Discovery Gate 输出

Discovery Gate 必须输出或更新 `discovery.md`：

```markdown
# Discovery

## Current Understanding

## Candidate Directions
| Option | Description | Pros | Cons | Status |
|--------|-------------|------|------|--------|

## Tradeoffs

## Recommended MVP

## Decision Ledger
| ID | Decision | Status | Source | Impact | Next Step |
|----|----------|--------|--------|--------|-----------|

## Open Questions
| ID | Question | Why It Matters | Options | Required Before |
|----|----------|----------------|---------|-----------------|

## Exit Criteria
- [ ] MVP scope confirmed
- [ ] high-impact decisions confirmed or explicitly deferred
- [ ] acceptance direction is clear
```

### Discovery Gate 退出条件

只有满足以下条件，才能进入 `/sdc:spec`：
- 推荐 MVP 或当前 change 范围已确认
- 高影响决策已 Confirmed，或明确标记为 Deferred 且不会影响当前 MVP
- Open Questions 中没有阻塞 spec 的问题
- 用户确认可以把 discovery 收敛为 spec

### 需要主动澄清的内容

| 维度 | 要问清的问题 |
|------|-------------|
| 背景 | 为什么现在要做？触发场景是什么？ |
| 用户 | 谁会使用或受到影响？ |
| 目标 | 这次迭代完成后，用户能多做什么或少受什么问题？ |
| 非目标 | 哪些事情这次明确不做？ |
| 范围 | 这是一个 change，还是需要拆成多个 change？ |
| 约束 | 是否有兼容性、性能、安全、数据、交互或上线限制？ |
| 验收 | 怎样证明这次 change 已经完成？ |
| 高影响决策 | 是否涉及权限、状态机、审批、提醒、技术栈、架构、数据或安全策略？哪些已确认？ |

### 讨论规则

1. 一次最多提出 3 个关键问题，避免把用户拖进长问卷
2. 如果信息足够，直接给出 change 草案并请求确认
3. 如果信息不足，先输出 Discovery Gate，而不是生成 Confirmed spec
4. 如果用户说“先按你的判断来”，可以给出 Recommended MVP，但必须标为 Proposed，并等待用户确认
5. 如果发现需求过大，先建议拆分，并说明推荐的第一个 change
6. 讨论结束后再创建或更新 `.sdc/changes/active/YYYY-MM-DD-short-name/`

### 收敛输出

在真正落盘前，先给出一个简短草案：

```text
## Change 草案
- 背景：
- 目标：
- 非目标：
- 范围：
- 初始场景（SCN）：
- 初始需求（REQ）：
- 初始验收标准（AC）：
- 风险/假设：
- Discovery 状态：不需要 / 进行中 / 已完成
- 建议 Change ID：

确认后我会创建 SDC change 文件。
```

---

## 执行规则

1. 如果 `.sdc/` 不存在，先执行 `/sdc:init`
2. short-name 必须简短、稳定，推荐英文小写和连字符
3. 一个 change 只表达一次独立需求迭代
4. 不要把多个互相独立的需求塞进同一个 change
5. 初始 `spec.md` 至少要有 SCN/REQ/AC 占位和待确认项
6. 初始 `tasks.md` 必须使用 `T### [REQ-*] [AC-*] [Phase] [Size]` 格式，待计划任务可标记为 Draft
7. 创建后必须给出下一步：`/sdc:spec` 或 `/sdc:plan`
8. 未确认高影响决策必须写入 Decision Ledger，不得写成 Confirmed
9. 需求不确定时必须先创建/更新 `discovery.md`，并且下一步只能是继续 discovery 或 `/sdc:spec`

---

## 输出格式

```text
✅ SDC 需求变更已创建
==================================================

## Change ID
YYYY-MM-DD-short-name

## 创建文件
- .sdc/changes/active/YYYY-MM-DD-short-name/proposal.md
- .sdc/changes/active/YYYY-MM-DD-short-name/discovery.md
- .sdc/changes/active/YYYY-MM-DD-short-name/tasks.md
- .sdc/changes/active/YYYY-MM-DD-short-name/design.md
- .sdc/changes/active/YYYY-MM-DD-short-name/spec.md
- .sdc/changes/active/YYYY-MM-DD-short-name/notes.md

## 下一步
👉 完善 proposal.md 和 spec.md，然后执行 `/sdc:validate`
```

---

## 质量红线

| 规则 | 违反后果 |
|------|---------|
| 必须创建独立 change 目录 | 变更不可追踪 |
| 必须包含 proposal/tasks/spec | 输出无效 |
| 不能覆盖已有 change | 数据丢失 |
| 必须有验收标准 | 无法验证 |
| 必须给出下一步 | 输出无效 |
| 模糊需求必须进入 Discovery Gate | 后续计划不可执行 |
| spec/tasks 不能只有空模板 | 后续无法追溯 |
| 未确认高影响决策不能写成事实 | AI 越权 |
| Discovery 未退出不能进入 plan/apply | 需求尚未收敛 |
