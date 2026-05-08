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

---

## 执行步骤

### 第一步：检查当前项目
先确认当前目录是否已经存在 `.sdc/`：

- 如果不存在：创建完整标准结构
- 如果已存在：只补齐缺失目录和模板，不能覆盖已有文件
- 如果项目已有类似目录：说明将保留原目录，并创建/补齐 `.sdc/`

---

### 第二步：创建标准目录结构

必须创建以下结构：

```text
.sdc/
├── README.md
├── project.md
├── current/
│   ├── spec.md
│   ├── plan.md
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
│   └── README.md
├── templates/
│   ├── change.md
│   └── decision.md
└── .gitignore
```

---

## 每个目录的职责

| 路径 | 作用 |
|------|------|
| `.sdc/project.md` | 项目长期背景、用户、技术栈、约束和验证命令 |
| `.sdc/current/` | 当前正在推进的一次需求迭代的快捷工作区 |
| `.sdc/changes/active/` | 正在推进的需求变更，每个变更一个子目录 |
| `.sdc/changes/archive/` | 已完成归档的需求变更 |
| `.sdc/specs/` | 已稳定沉淀的业务规范 |
| `.sdc/standards/` | 项目长期开发规范，约束代码、测试、架构、安全、Git 和 AI 协作 |
| `.sdc/decisions/` | 架构、产品、技术关键决策 |
| `.sdc/reviews/` | `/sdc:review` 的审查报告 |
| `.sdc/reports/` | `/sdc:test` 和 `/sdc:quality` 的测试/质量报告 |
| `.sdc/templates/` | 需求变更和决策模板 |

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

---

## 迭代记录规范

每次新需求建议在 `.sdc/changes/` 下创建一个目录：

```text
.sdc/changes/active/YYYY-MM-DD-short-name/
├── proposal.md
├── tasks.md
├── design.md
├── spec.md
└── notes.md
```

命名要求：
- 日期使用 `YYYY-MM-DD`
- short-name 使用英文小写和连字符
- 一个目录只记录一次独立需求迭代

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

---

## 💡 设计理念
> 需求不是聊天记录，需求是项目资产。
>
> `.sdc/` 的目标是让每一次迭代都有来路、有计划、有实现记录、有验收结论。
