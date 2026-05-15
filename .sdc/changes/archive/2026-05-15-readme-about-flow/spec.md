# Spec

## 0. 文档元信息

- 状态: Confirmed
- Change: 2026-05-15-readme-about-flow
- 日期: 2026-05-15

## 1. Glossary / 统一语言

| 术语 | 定义 | 状态 | 备注 |
|------|------|------|------|
| SDC | Spec-Driven-Coding, 面向 AI 编码的轻量规范驱动工作流 | 已确认 | 项目名称 |
| Discipline Core | 裁决链、事实链、追溯链、停线报告等内部工程纪律 | 已确认 | v1.1 核心 |
| Skill Plugin | Codex 中通过 skill/plugin 能力触发，而不是自定义 slash command | 已确认 | README 必须说清 |
| Slash Command | Claude Code 中可注册的 `/sdc:*` 命令 | 已确认 | Claude Code 场景 |
| About | GitHub repository description 和 topics | 已确认 | 通过 `gh repo edit` 更新 |

## 2. 背景与目标

当前 README 已覆盖安装、命令和 v1.1 能力，但表达仍像功能堆叠。目标是让 README 变成 SDC 自己的示范：先讲流程，随后讲平台差异，最后讲质量门禁和市场提交信息。

## 3. 场景与需求

### SCN-01: 新用户首次阅读 README

- 目标: 快速理解 SDC 不是命令合集，而是轻量 spec-driven lifecycle。
- 主流程: 打开 README -> 看到一句话定位 -> 看到完整流程 -> 选择 Claude/Codex 安装方式。
- 异常流程: 如果用户只用 Codex CLI，应能看到不能使用 `/sdc:init` 是预期行为。

### REQ-01: README 价值定位

- 业务规则: 第一屏必须强调少量入口、完整闭环、内部纪律。
- 边界条件: 不夸大为通用自动化平台，不承诺官方 marketplace 已收录。
- 关联场景: SCN-01

### SCN-02: 用户想照着流程跑

- 目标: 复制 README 里的示例即可理解 SDC lifecycle。
- 主流程: init -> change/spec/plan -> apply -> check -> archive。
- 异常流程: Codex 用户使用自然语言或 skills 触发，不依赖 slash command。

### REQ-02: 端到端流程示例

- 业务规则: README 必须给出“实际工作流”而不是只列命令。
- 边界条件: 普通模式保持 6-7 个公共入口，高级指令只作为细分能力出现。
- 关联场景: SCN-02

### SCN-03: GitHub 访客或审核者查看 About

- 目标: 一眼看到 SDC 与 Claude Code、Codex、traceability、spec-driven coding 的关系。
- 主流程: 打开 GitHub -> 看到 description 和 topics -> 判断项目适用性。

### REQ-03: About 元信息

- 业务规则: description 必须包含 traceability 或 discipline core 的核心价值。
- 边界条件: topics 不添加无关平台或夸大标签。
- 关联场景: SCN-03

### SCN-04: 维护者检查本次改动

- 目标: 能看到 `.sdc/` change 记录和验证证据。
- 主流程: 查看 proposal/spec/design/tasks/notes -> 运行 validate/check -> 查看归档。

### REQ-04: 自举验证

- 业务规则: 本次 README/About 更新必须留下 SDC 记录并通过基础验证。
- 边界条件: 不提交 `.idea/`。
- 关联场景: SCN-04

## 4. Acceptance Criteria / 验收标准

### AC-01: README 第一屏定位

Given 新用户打开 README
When 读取开头两屏
Then 能看到 SDC 的一句话定位、v1.1 discipline core、普通流程入口和平台差异提示

### AC-02: 完整流程示例

Given 用户想照着 SDC 跑一次需求迭代
When 阅读使用示例
Then 能看到从 init 到 archive 的完整 lifecycle，并理解 check 是综合入口

### AC-03: Codex 使用差异

Given 用户在 Codex CLI 或 Codex App 使用 SDC
When 阅读 Codex 使用方式
Then 明确知道通过自然语言或 skills 触发，不期待 `/sdc:*` 自定义 slash command

### AC-04: GitHub About

Given 用户打开 GitHub 仓库首页
When 查看 About
Then description 和 topics 反映 spec-driven-coding、traceability、SDD、Claude Code、Codex 等定位

### AC-05: 验证通过

Given 维护者准备交付
When 运行基础验证
Then Python/Node 语法、Claude plugin validate、npm pack dry-run 均通过

## 5. 验证策略

| AC | 验证方式 | 需要的测试/检查 | 备注 |
|----|----------|-----------------|------|
| AC-01 | 人工阅读 + diff 检查 | `git diff -- README.md` | README 首屏 |
| AC-02 | 人工阅读 + flow 记录 | `.sdc/changes/.../tasks.md` | lifecycle |
| AC-03 | 人工阅读 | README Codex section | 平台差异 |
| AC-04 | GitHub CLI 查询 | `gh repo view --json description,repositoryTopics` | About |
| AC-05 | 命令验证 | py_compile, node --check, claude validate, npm pack | 交付门禁 |

## 6. 风险、假设与待确认项

| ID | 类型 | 描述 | 影响 | 处理建议 |
|----|------|------|------|----------|
| RISK-01 | 风险 | README 过长 | 新用户失焦 | 前置精简流程，细节后置 |
| RISK-02 | 风险 | GitHub topic 重复或不支持 | About 更新失败 | 使用 `gh repo edit` 后查询验证 |
| ASM-01 | 假设 | 用户说的 about 指 GitHub About | 可能也包括 package description | 同步更新 GitHub About 和 package/plugin metadata |

## 7. 追溯关系矩阵

| SCN | REQ | AC | 风险/假设 |
|-----|-----|----|-----------|
| SCN-01 | REQ-01 | AC-01 | RISK-01 |
| SCN-02 | REQ-02 | AC-02, AC-03 | RISK-01 |
| SCN-03 | REQ-03 | AC-04 | RISK-02, ASM-01 |
| SCN-04 | REQ-04 | AC-05 | ASM-01 |
