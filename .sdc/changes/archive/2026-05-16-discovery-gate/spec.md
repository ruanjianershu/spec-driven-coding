# Spec

## 0. 文档元信息

- 状态: Confirmed
- Change: 2026-05-16-discovery-gate
- 日期: 2026-05-16

## 1. Decision Ledger / 决策台账

| ID | 决策 | 状态 | 依据来源 | 是否允许进入 REQ/AC | 下一步 |
|----|------|------|----------|----------------------|--------|
| DEC-01 | SDC 内置 Discovery Gate，不依赖 Superpowers | Confirmed | 用户问题和产品独立性目标 | 是 | 实施 |
| DEC-02 | 不新增公开 `/sdc:brainstorm` 指令 | Confirmed | 少指令原则 | 是 | 复用 `/sdc:change` |
| DEC-03 | change 默认创建 discovery.md | Confirmed | 需要真实流程资产 | 是 | 更新 CLI |

## 2. Glossary / 统一语言

| 术语 | 定义 | 状态 | 备注 |
|------|------|------|------|
| Discovery Gate | 需求不确定时进入的探索门禁，先发散再收敛 | Confirmed | 本次核心 |
| Discovery | 当前理解、候选方向、取舍、MVP、问题和决策台账 | Confirmed | 产物为 `discovery.md` |
| Confirmed Spec | 基于已确认 discovery 结果生成的正式规格 | Confirmed | 可进入 plan |

## 3. 背景与目标

SDC 需要把“不确定需求”从 spec 阶段前置出来。change 是需求入口，应该先判断是否可进入 spec；如果不确定，应进入 discovery，而不是让 spec 背负所有探索工作。

## 4. 场景与需求

### SCN-01: 模糊需求进入 change

- 目标: 用户只表达方向时，SDC 先探索而不是直接写 spec。
- 触发条件: 用户输入“我要做一个会议室预约系统”等宽泛需求。
- 主流程: change -> Discovery Gate -> discovery.md -> 用户确认 MVP/决策 -> spec。
- 异常流程: 用户明确说需求已确定，可直接进入 spec。
- 关联需求: REQ-01, REQ-02

### REQ-01: 确定性判定

- 业务规则: `/sdc:change` 必须判断需求是否足够进入 spec。
- 边界条件: 如果目标、用户、范围、验收或高影响决策不清楚，进入 Discovery Gate。
- 关联场景: SCN-01

### REQ-02: Discovery 结构化输出

- 业务规则: Discovery Gate 必须产出当前理解、候选方向、取舍、推荐 MVP、Decision Ledger、open questions。
- 边界条件: Proposed/Assumed/TBD 不能进入 confirmed spec。
- 关联场景: SCN-01

### SCN-02: 用户不知道用 change 还是 spec

- 目标: 普通用户只用 `/sdc:change` 或 `/sdc 新需求`。
- 触发条件: 用户表达一个新需求或新项目。
- 主流程: change 自动判断 discovery/spec/plan 的下一步。
- 关联需求: REQ-03, REQ-04

### REQ-03: CLI 和模板支持 discovery.md

- 业务规则: init 和 change 模板必须包含 discovery.md。
- 边界条件: discovery.md 可以为空模板，但不能替代 spec。
- 关联场景: SCN-02

### REQ-04: 文档说明 change/spec 选择

- 业务规则: README/docs 必须说明 change 是入口，spec 是规格细化。
- 边界条件: 不把 spec 描述成 0 到 1 专用命令。
- 关联场景: SCN-02

## 5. Acceptance Criteria / 验收标准

### AC-01: change 有 Discovery Gate

Given 用户输入模糊需求
When 触发 `/sdc:change`
Then SDC 输出 Discovery Gate，而不是直接生成 confirmed spec/plan

### AC-02: spec 消费 discovery

Given `discovery.md` 中仍有 TBD 或 Proposed 高影响决策
When 触发 `/sdc:spec`
Then SDC 不能生成 Confirmed spec，必须要求确认

### AC-03: CLI 创建 discovery.md

Given 用户运行 `sdc init` 和 `sdc change demo`
When 查看 `.sdc/templates/` 和 change 目录
Then 能看到 `discovery.md`

### AC-04: 文档解释命令选择

Given 用户阅读 README
When 查看实际工作流或命令说明
Then 能理解日常从 change 开始，spec 是 change 内的规格细化

### AC-05: 验证通过

Given 本次修改完成
When 运行验证命令
Then SDC validate、Python/Node/manifest/Claude/npm 验证通过

## 6. 验证策略

| AC | 验证方式 | 需要的测试/检查 | 备注 |
|----|----------|-----------------|------|
| AC-01 | 文档检查 | `rg "Discovery Gate" skills/sdc-change/SKILL.md` | change |
| AC-02 | 文档检查 | `rg "discovery.md" skills/sdc-spec/SKILL.md` | spec |
| AC-03 | CLI 临时目录测试 | `python3 sdc-cli.py init && python3 sdc-cli.py change demo` | CLI |
| AC-04 | 文档检查 | `rg "change 是入口|spec 是" README.md docs/sdc-discipline-core.md` | docs |
| AC-05 | 命令验证 | py_compile, node --check, manifest parse, claude validate, npm pack | 发布 |

## 7. 风险、假设与待确认项

| ID | 类型 | 描述 | 影响 | 处理建议 |
|----|------|------|------|----------|
| RISK-01 | 风险 | discovery.md 增加文件数量 | 用户觉得重 | 明确仅不确定需求需要填写 |
| ASM-01 | 假设 | 用户希望直接升级实现 | 本次直接修改 | 已记录 change |

## 8. 追溯关系矩阵

| SCN | REQ | AC | 风险/假设 |
|-----|-----|----|-----------|
| SCN-01 | REQ-01, REQ-02 | AC-01, AC-02 | RISK-01 |
| SCN-02 | REQ-03, REQ-04 | AC-03, AC-04, AC-05 | ASM-01 |
