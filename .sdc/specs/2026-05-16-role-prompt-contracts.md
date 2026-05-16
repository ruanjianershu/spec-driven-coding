# Archived Spec: 2026-05-16-role-prompt-contracts

# Spec

## 0. 文档元信息

- 状态: Confirmed
- Change: 2026-05-16-role-prompt-contracts
- 日期: 2026-05-16

## 1. Decision Ledger / 决策台账

| ID | 决策 | 状态 | 依据来源 | 是否允许进入 REQ/AC | 下一步 |
|----|------|------|----------|----------------------|--------|
| DEC-01 | 为所有 SDC skills 增加英文 Role Prompt Contract | Confirmed | 用户明确要求 | 是 | 实施 |
| DEC-02 | 保留现有中文规则，只补充英文角色化契约 | Confirmed | 避免破坏现有用户理解 | 是 | 实施 |
| DEC-03 | 升级版本到 1.1.4 | Confirmed | 行为与文档变化需要版本标识 | 是 | 实施 |

## 2. Glossary / 统一语言

| 术语 | 定义 | 状态 | 备注 |
|------|------|------|------|
| Role Prompt Contract | 每个 skill 触发时加载的英文角色、工作契约、证据规则和输出契约 | Confirmed | 本次核心 |
| Operating Contract | AI 在该 skill 中必须如何行动 | Confirmed | 不替代执行步骤 |
| Evidence Rules | 哪些来源可以作为事实、哪些只能作为线索 | Confirmed | 防止脑补 |
| Output Contract | 该 skill 的输出必须具备什么结构和边界 | Confirmed | 防止泛化回答 |

## 3. 背景与目标

SDC 要同时具备流程治理和角色化执行力。现有 skill 已经有任务步骤与质量红线，但还需要在 skill 启动时明确“你是谁、你怎么工作、你凭什么下结论、你必须输出什么”。

## 4. 场景与需求

### SCN-01: skill 调用时建立专家角色

- 目标: 每次调用 SDC skill 时，AI 都能进入对应专家角色。
- 触发条件: 任意 `skills/*/SKILL.md` 被加载。
- 主流程: 读取 Role Prompt Contract -> 按 Operating Contract 执行 -> 用 Evidence Rules 约束结论 -> 按 Output Contract 输出。
- 关联需求: REQ-01, REQ-02

### REQ-01: 每个 skill 都有 Role Prompt Contract

- 业务规则: 所有 SDC skills 必须包含 `## Role Prompt Contract`。
- 边界条件: 不能只在 README 或公共文档里写；必须写入 skill 文件。
- 关联场景: SCN-01

### REQ-02: 合同结构统一且使用英文

- 业务规则: 每个 Role Prompt Contract 至少包含 Role、Operating Contract、Evidence Rules、Output Contract。
- 边界条件: 合同内容可以按 skill 定制，但标题和基本结构必须统一。
- 关联场景: SCN-01

### SCN-02: 文档和发布包体现能力升级

- 目标: 用户和安装方知道 SDC 已增强角色化 prompt。
- 触发条件: 用户查看 README、CHANGELOG、package 或 plugin metadata。
- 主流程: 文档描述 Role Prompt Contracts -> metadata version 更新。
- 关联需求: REQ-03

### REQ-03: 文档和 metadata 更新

- 业务规则: README、CHANGELOG、package/plugin metadata 必须描述 role prompt contract 能力。
- 边界条件: 不夸大为新增运行时功能。
- 关联场景: SCN-02

## 5. Acceptance Criteria / 验收标准

### AC-01: all skills have contract

Given 仓库中存在 `skills/*/SKILL.md`
When 搜索 `## Role Prompt Contract`
Then 每个 SDC skill 文件都包含该章节

### AC-02: contract has required subsections

Given 任意 SDC skill 文件
When 查看 Role Prompt Contract
Then 能看到 `### Role`、`### Operating Contract`、`### Evidence Rules`、`### Output Contract`

### AC-03: docs and metadata updated

Given 用户查看 README、CHANGELOG、package/plugin metadata
When 搜索 role prompt contract
Then 能看到本次能力说明和版本 1.1.4

### AC-04: validation passes

Given 本次修改完成
When 运行 SDC validate/check、语法、manifest、Claude plugin 和 npm dry-run
Then 所有验证通过

## 6. 验证策略

| AC | 验证方式 | 需要的测试/检查 | 备注 |
|----|----------|-----------------|------|
| AC-01 | 文件搜索 | `for f in skills/*/SKILL.md; do rg "## Role Prompt Contract" "$f"` | 全 skill |
| AC-02 | 文件搜索 | `rg "### Role|### Operating Contract|### Evidence Rules|### Output Contract" skills` | 结构 |
| AC-03 | 文件搜索 | `rg "1.1.4|role prompt contract|Role Prompt Contract" README.md CHANGELOG.md package.json .claude-plugin .codex-plugin` | 文档 |
| AC-04 | 命令验证 | py_compile, node --check, manifest parse, claude validate, npm pack | 发布 |

## 7. 风险、假设与待确认项

| ID | 类型 | 描述 | 影响 | 处理建议 |
|----|------|------|------|----------|
| RISK-01 | 风险 | 增加 skill 文件长度 | 可能略增加载上下文 | 保持短而强 |
| ASM-01 | 假设 | 用户希望直接实现英文补充 | 本轮直接修改 | 已记录 change |

## 8. 追溯关系矩阵

| SCN | REQ | AC | 风险/假设 |
|-----|-----|----|-----------|
| SCN-01 | REQ-01, REQ-02 | AC-01, AC-02, AC-04 | RISK-01 |
| SCN-02 | REQ-03 | AC-03, AC-04 | ASM-01 |
