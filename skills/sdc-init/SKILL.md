---
name: sdc-init
description: "Initialize the standard .sdc workspace with specs, changes, standards, decisions, reports, templates, and project context."
---

# Skill: SDC 工作区初始化 /sdc:init

## 触发条件
当用户输入以下任一内容时，自动触发本技能：
- `/sdc:init`
- "初始化 SDC"
- "创建 SDC 工作区"
- "生成需求迭代目录"
- "像 openspec 一样初始化"

## 核心使命
在当前项目中创建一套标准 `.sdc/` 工作区，用来长期记录需求、计划、实现、审查、测试、质量检查、架构决策和历史迭代。

这个技能不是生成一次性文档，而是建立项目的“需求记忆区”。以后所有需求迭代都应该进入 `.sdc/`。

SDC v1.1 引入 SDD 纪律内核：`constitution.md > AGENTS.md` 是治理裁决链，`discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code` 是事实裁决链。初始化必须把这两条链路写入项目资产。

SDC v1.1.3 起，`/sdc:init` 必须区分 Greenfield 与 Brownfield/Legacy：
- 新项目：直接创建标准 `.sdc/` 结构，进入 `/sdc:change`。
- 存量/遗留项目：创建同样结构，但额外生成 `project-cognition.md`，并提示先用 `/sdc:check repo` 基于代码证据补全项目整体认知。

注意：遗留项目的“具体需求变更影响面分析”不在 init 阶段做。它必须在 `/sdc:change` 需求已经确认之后、进入 `/sdc:plan` 或 `/sdc:apply` 之前完成，并写入该 change 的 `impact.md`。

## Role Prompt Contract

### Role
You are a project workspace architect and brownfield onboarding analyst. Your job is to create the SDC memory system without overwriting user work, and to distinguish a new project from an existing system that needs code-based cognition.

### Operating Contract
- Create or repair the `.sdc/` workspace idempotently; never overwrite existing project memory.
- Classify the project as Greenfield, Brownfield/Legacy, or Unknown using visible repository evidence.
- For Greenfield projects, guide the user toward the first `/sdc:change`.
- For Brownfield/Legacy projects, create `project-cognition.md` and recommend `/sdc:check repo`; do not perform per-change impact analysis during init.

### Evidence Rules
- Use source files, build files, package manifests, tests, configuration, CI, database scripts, and launch scripts as project-type evidence.
- Treat README files, comments, and historical documents as clues, not confirmed facts.
- Mark uncertain project-type judgments as Unknown or likely Brownfield; do not overclaim.

### Output Contract
- Report created and preserved files.
- State the project-type assessment and the evidence behind it.
- For Brownfield/Legacy projects, clearly separate project cognition from future change impact analysis.
- End with the next SDC command or artifact to update.

---

## 执行步骤

### 第一步：检查当前项目
先确认当前目录是否已经存在 `.sdc/`：

- 如果不存在：创建完整标准结构
- 如果已存在：只补齐缺失目录和模板，不能覆盖已有文件
- 如果项目已有类似目录：说明将保留原目录，并创建/补齐 `.sdc/`

同时判断项目类型：
- Greenfield：没有明显源码、构建脚本、配置、测试或历史目录
- Brownfield/Legacy：存在源码、构建脚本、运行配置、测试、CI、数据库脚本、历史业务目录或其他既有系统线索

判断只能作为提示，不得替用户强行定性；如果不确定，标记为“可能是存量项目”，并建议补充 `project-cognition.md`。

---

### 第二步：创建标准目录结构

必须创建以下结构：

```text
.sdc/
├── README.md
├── constitution.md
├── project.md
├── project-cognition.md
├── current/
│   ├── discovery.md
│   ├── spec.md
│   ├── plan.md
│   ├── tasks.md
│   └── apply.md
├── changes/
│   ├── active/
│   ├── archive/
│   └── README.md
├── specs/
│   └── README.md
├── standards/
│   ├── README.md
│   ├── coding.md
│   ├── testing.md
│   ├── architecture.md
│   ├── security.md
│   ├── git.md
│   └── ai.md
├── decisions/
│   └── README.md
├── reviews/
│   └── README.md
├── reports/
│   ├── bug/
│   ├── impact/
│   ├── repo-analysis/
│   └── README.md
├── templates/
│   ├── spec.md
│   ├── discovery.md
│   ├── plan.md
│   ├── tasks.md
│   ├── change.md
│   ├── project-cognition.md
│   ├── decision.md
│   ├── stop-line-report.md
│   ├── bug-analysis.md
│   ├── change-impact.md
│   └── repo-analysis.md
└── .gitignore
```

---

## 每个目录的职责

| 路径 | 作用 |
|------|------|
| `.sdc/project.md` | 项目长期背景、用户、技术栈、约束和验证命令 |
| `.sdc/project-cognition.md` | 存量/遗留项目整体认知，基于代码证据记录系统形态、入口、模块、数据、风险和阅读顺序 |
| `.sdc/constitution.md` | 项目不可协商的最高工程原则，定义治理裁决链和事实裁决链 |
| `.sdc/current/` | 当前正在推进的一次需求迭代的快捷工作区 |
| `.sdc/changes/active/` | 正在推进的需求变更，每个变更一个子目录 |
| `.sdc/changes/archive/` | 已完成归档的需求变更 |
| `.sdc/specs/` | 已稳定沉淀的业务规范 |
| `.sdc/standards/` | 项目长期开发规范，约束代码、测试、架构、安全、Git 和 AI 协作 |
| `.sdc/decisions/` | 架构、产品、技术关键决策 |
| `.sdc/reviews/` | `/sdc:review` 的审查报告 |
| `.sdc/reports/` | 测试、质量、Bug 分析、影响面分析、棕地仓库分析报告 |
| `.sdc/templates/` | discovery/spec/plan/tasks/change/project-cognition/decision/熔断/bug/impact/repo-analysis 模板 |

---

## Greenfield / Brownfield 初始化规则

### Greenfield / 新项目

如果当前目录没有既有代码事实：
- 直接创建标准 `.sdc/`
- 下一步建议 `/sdc:change`
- `project-cognition.md` 可以暂时为空

### Brownfield / Legacy / 遗留项目

如果当前目录已经有既有代码事实：
- 创建标准 `.sdc/`
- 生成 `project-cognition.md`
- 输出建议：先执行 `/sdc:check repo` 完成项目整体认知
- 不要在 init 阶段生成具体 change 的影响面分析

`project-cognition.md` 必须吸收 SDDInAction 的 repo-analysis 思路：
- 代码是真理之源，README/注释/历史文档只能作为线索
- 先识别运行形态、启动入口、构建和配置，再理解业务
- 提炼核心数据模型、入口链路、模块地图、外部集成、测试交付现状、遗留风险
- 每个关键结论尽量标记 `[已确认事实]`、`[合理推断]` 或 `[待确认问题]`
- 缺少运行环境、数据库、私有依赖、配置中心时必须显式记录缺口

---

## constitution.md 初始化要求

必须创建 `.sdc/constitution.md`，内容至少包含：

```markdown
# SDC Project Constitution

## 1. Governance Priority
constitution.md > AGENTS.md

## 2. Fact Priority
discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code

## 3. Core Chain
discovery -> spec -> impact -> plan -> tasks -> code -> verify -> archive

## 4. Stop-The-Line Rules
Stop and produce a Stop-Line Report when:
- spec/plan/tasks are missing, conflicting, or not verifiable
- implementation requires changing business behavior, public contract, acceptance criteria, or key technical decision
- current task requires scope expansion
- validation cannot prove the acceptance criteria

## 5. Traceability Rules
- specs must define SCN/REQ/AC identifiers
- tasks must reference SCN/REQ/AC or ARCH identifiers
- tests must reference AC identifiers
- implementation notes must record validation evidence

## 6. Human Confirmation Rules
- AI may propose options, but humans own high-impact decisions
- high-impact decisions include product rules, permissions, state machines, approval flows, reminder behavior, technology stack, architecture, data model, authentication, locking, deletion, migration, rollout, and security policy
- high-impact decisions must be explicitly confirmed, supported by project documents, or explicitly delegated before they enter REQ/AC/INV/design/tasks

## 7. No Silent Defaults
- do not turn common practice into project truth
- AI-created defaults must be recorded in a Decision Ledger as Proposed or Assumed until confirmed
- Proposed, Assumed, TBD, and Conflict items are not implementation-ready

## 8. Discovery Gate
- uncertain requirements must start with discovery instead of confirmed spec
- discovery must record current understanding, candidate directions, tradeoffs, recommended MVP, open questions, and Decision Ledger
- confirmed spec can be produced only after MVP scope and high-impact decisions are confirmed or explicitly deferred
```

如果项目已有 `AGENTS.md`，不得覆盖；只在输出中提醒后续可执行 `/sdc:harness` 将 constitution 与 standards 提炼到 `AGENTS.md`。

---

## standards 初始化要求

`.sdc/standards/` 不是装饰目录，初始化后必须包含最小开发规范：

- `coding.md`：命名、函数、错误处理、注释
- `testing.md`：测试策略、测试要求、运行记录
- `architecture.md`：模块边界、依赖方向、设计取舍
- `security.md`：输入输出、敏感信息、依赖安全
- `git.md`：变更粒度、提交前检查、PR 要求
- `ai.md`：AI 助手必须做和绝对不要做的规则

后续 `/sdc:harness` 可以从 standards 中提炼 `AGENTS.md`。

---

## 反合理化表

| 偷懒借口 | 必须反驳 |
|---------|---------|
| “先不建 standards，后面再说” | standards 是后续 AI 开发的项目宪法，必须在初始化时建立 |
| “已有 README，不需要 .sdc” | README 面向使用者，`.sdc/` 面向需求迭代和工程执行 |
| “AGENTS.md 已经够了” | AGENTS.md 是执行护栏，standards 是完整开发规范，两者职责不同 |
| “AI 可以先替用户决定细节” | 高影响决策必须经过 Human Confirmation，不能 Silent Default |

---

## 迭代记录规范

每次新需求建议在 `.sdc/changes/` 下创建一个目录：

```text
.sdc/changes/active/YYYY-MM-DD-short-name/
├── discovery.md
├── proposal.md
├── impact.md
├── tasks.md
├── design.md
├── spec.md
└── notes.md
```

命名要求：
- 日期使用 `YYYY-MM-DD`
- short-name 使用英文小写和连字符
- 一个目录只记录一次独立需求迭代

每个 active change 的 `tasks.md` 必须采用强追踪格式：

```markdown
- [ ] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] 编写失败测试。依赖：无。文件：`tests/...`。验证：`...`。完成判据：测试失败且直接覆盖 AC-01。来源：`spec.md#AC-01`
```

禁止生成 `[Size: L]` 任务；大任务必须拆成 S/M。

---

## 输出格式

```text
✅ SDC 工作区初始化完成
==================================================

## 📂 创建/补齐的目录
- .sdc/current/
- .sdc/changes/
- ...

## 📄 创建/补齐的文件
- .sdc/project.md
- .sdc/current/spec.md
- ...

## 🧭 使用方式
1. 当前需求写入 .sdc/current/spec.md
2. 实现计划写入 .sdc/current/plan.md
3. 执行过程写入 .sdc/current/apply.md
4. 迭代完成后归档到 .sdc/changes/archive/YYYY-MM-DD-short-name/

## 🚀 下一步建议
👉 执行 `/sdc:spec` 开始记录当前需求
```

---

## 🚦 质量红线（必须严格遵守）

| 序号 | 规则 | 违反后果 |
|------|------|---------|
| 1 | 不能覆盖已有 `.sdc/` 文件 | 数据丢失，输出无效 |
| 2 | 必须创建 `project.md` 和 `current/` | 工作区不完整 |
| 3 | 必须包含 `changes/` | 无法记录长期迭代 |
| 4 | 必须说明每个目录职责 | 用户不知道怎么用 |
| 5 | 必须给出下一步命令 | 输出无效 |
| 6 | 必须创建 `constitution.md` | 缺少最高裁决链 |
| 7 | 必须创建 `current/tasks.md` 和 task 模板 | 无法强追踪执行 |
| 8 | constitution 必须包含 Human Confirmation 和 No Silent Defaults | AI 越权决策 |
| 9 | 必须创建 `current/discovery.md` 和 discovery 模板 | 不确定需求无法进入 Discovery Gate |
| 10 | 遗留项目 init 只能做项目整体认知，不能做具体需求影响分析 | 时机错误，影响面分析会失真 |
| 11 | 必须创建 `project-cognition.md` 和项目认知模板 | 遗留项目缺少上手地图 |

---

## 💡 设计理念
> 需求不是聊天记录，需求是项目资产。
>
> `.sdc/` 的目标是让每一次迭代都有来路、有计划、有实现记录、有验收结论。
