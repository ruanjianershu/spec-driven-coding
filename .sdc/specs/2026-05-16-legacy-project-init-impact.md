# Archived Spec: 2026-05-16-legacy-project-init-impact

# Spec

## 0. 文档元信息

- 状态: Confirmed
- Change: 2026-05-16-legacy-project-init-impact
- 日期: 2026-05-16

## 1. Decision Ledger / 决策台账

| ID | 决策 | 状态 | 依据来源 | 是否允许进入 REQ/AC | 下一步 |
|----|------|------|----------|----------------------|--------|
| DEC-01 | `init` 只处理项目整体认知，不做具体需求影响分析 | Confirmed | 用户修正：“遗留项目变更分析应该在 change 中确定完需求之后调用” | 是 | 实施 |
| DEC-02 | 遗留项目变更影响分析作为 `change` 需求确认后的门禁 | Confirmed | 用户明确要求，并与本地参考流程的 change-impact-analysis 一致 | 是 | 实施 |
| DEC-03 | 不新增公开命令，复用 init/change/check/review | Confirmed | SDC 少指令原则 | 是 | 实施 |
| DEC-04 | 最终 code review/check 需要复核实际老系统改造点与影响点 | Confirmed | 用户明确要求 | 是 | 实施 |

## 2. Glossary / 统一语言

| 术语 | 定义 | 状态 | 备注 |
|------|------|------|------|
| Greenfield / 新项目 | 尚无既有代码事实或历史兼容包袱的项目 | Confirmed | init 直接创建标准结构 |
| Brownfield / Legacy / 遗留项目 | 已有运行代码、配置、数据模型、历史接口或兼容约束的项目 | Confirmed | init 先做项目整体认知 |
| Project Cognition | 基于现有代码形成的项目整体认知报告 | Confirmed | init/repo 模式产物 |
| Change Impact Gate | 需求确认后、plan/apply 前的遗留项目影响面分析门禁 | Confirmed | change 内产物为 `impact.md` |
| Legacy Final Impact Review | 实现后在 review/check 中复核实际改造点和影响点 | Confirmed | 防止实现偏离影响面分析 |

## 3. 背景与目标

遗留项目的核心难点不是“有没有 `.sdc/` 结构”，而是既有系统已有真实代码、配置、数据和外部契约。SDC 需要把项目认知和具体需求影响面分开：init 负责建立项目整体认知入口；change 在需求确定后才分析该需求的影响半径；最终 review/check 再复核实际改造点与风险。

## 4. 场景与需求

### SCN-01: 遗留项目初始化

- 目标: 用户在既有代码仓库中初始化 SDC 后，能知道先建立项目整体认知。
- 触发条件: 当前仓库已有源码、构建文件、配置、测试或 CI 等代码事实。
- 主流程: `/sdc:init` -> 识别为 Brownfield/Legacy -> 创建 `project-cognition.md` 模板 -> 提示用 `/sdc:check repo` 完成整体认知。
- 异常流程: 如果是新项目，只创建标准结构，不要求填写项目整体认知。
- 关联需求: REQ-01

### REQ-01: init 区分新项目和遗留项目

- 业务规则: `/sdc:init` 必须说明 Greenfield 与 Brownfield/Legacy 的不同后续路径。
- 边界条件: init 不得为尚未确定的具体需求生成 change impact 分析。
- 关联场景: SCN-01

### SCN-02: 遗留项目需求确定后分析影响面

- 目标: 在改遗留系统前，先知道本次需求会触碰哪些入口、调用链、契约、数据、配置和测试。
- 触发条件: `/sdc:change` 已完成 Discovery Gate 或 spec 已经 Confirmed，且项目为 Brownfield/Legacy。
- 主流程: change -> confirmed spec -> Change Impact Gate -> `impact.md` -> plan -> apply。
- 异常流程: 如果影响分析发现待确认问题会改变范围或验收，必须停线回到 spec/change。
- 关联需求: REQ-02

### REQ-02: change 在需求确认后触发 impact gate

- 业务规则: 对遗留项目，`/sdc:change` 和 `/sdc:plan` 必须要求在 plan/apply 前形成当前 change 的 `impact.md`。
- 边界条件: `impact.md` 不能靠目录名脑补，必须区分已确认事实、合理推断和待确认问题。
- 关联场景: SCN-02

### SCN-03: 遗留项目最终 review/check

- 目标: 实现完成后，审查者能看到当前需求对老系统的实际改造点与影响点，而不只是通用代码质量结论。
- 触发条件: 遗留项目执行 `/sdc:review` 或 `/sdc:check` delivery。
- 主流程: 读取 spec/design/tasks/impact/notes/git diff -> 输出 Legacy Final Impact Review -> 标注实际修改点、级联影响、契约/数据/配置影响、测试覆盖、残余风险。
- 异常流程: 如果实际改动超出 `impact.md` 或 spec，需要标为阻塞。
- 关联需求: REQ-03

### REQ-03: review/check 输出老系统改造点与影响点

- 业务规则: 遗留项目最终审查必须包含“老系统改造点与影响点分析”。
- 边界条件: 只能基于代码 diff、`.sdc` 文件和测试证据，不得编造影响。
- 关联场景: SCN-03

## 5. Acceptance Criteria / 验收标准

### AC-01: init legacy cognition

Given 用户在遗留项目中执行 `/sdc:init`
When SDC 完成初始化
Then 生成或提示维护 `project-cognition.md`，并明确“init 只做项目整体认知，不做具体需求影响分析”

### AC-02: change impact after confirmed requirement

Given 遗留项目中某个 change 的需求已经 Confirmed
When 进入 `/sdc:plan` 或准备 `/sdc:apply`
Then SDC 要求先生成当前 change 的 `impact.md`，内容覆盖变更入口、直接修改点、级联影响、契约/数据/配置、安全/观测、测试回归、实施顺序和待确认问题

### AC-03: block unresolved legacy impact

Given `impact.md` 存在待确认问题且会影响范围、验收、契约、数据或安全
When 继续 plan/apply/check
Then SDC 必须停线，而不是继续实现

### AC-04: final review includes legacy impact

Given 遗留项目完成实现并执行 `/sdc:review` 或 `/sdc:check`
When 输出审查结果
Then 必须包含老系统改造点与影响点分析，并对照 `impact.md` 与实际 diff 标出新增、偏离和残余风险

### AC-05: validation passes

Given 本次 SDC 升级完成
When 运行 CLI、插件和包校验
Then validate/check、Python/Node/manifest/Claude/npm dry-run 均通过

## 6. 验证策略

| AC | 验证方式 | 需要的测试/检查 | 备注 |
|----|----------|-----------------|------|
| AC-01 | 文档和 CLI 模板检查 | `rg "project-cognition|Greenfield|Brownfield|Legacy" skills/sdc-init/SKILL.md sdc-cli.py README.md` | init |
| AC-02 | 文档和 CLI 模板检查 | `rg "Change Impact Gate|impact.md|需求确认" skills/sdc-change/SKILL.md skills/sdc-plan/SKILL.md sdc-cli.py` | change/plan |
| AC-03 | 文档检查 | `rg "待确认问题|停线|impact.md" skills/sdc-plan/SKILL.md skills/sdc-apply/SKILL.md skills/sdc-check/SKILL.md` | gates |
| AC-04 | 文档检查 | `rg "老系统改造点|Legacy Final Impact Review|impact.md" skills/sdc-review/SKILL.md skills/sdc-check/SKILL.md` | review/check |
| AC-05 | 命令验证 | py_compile, node --check, manifest parse, claude validate, npm pack | 发布 |

## 7. 风险、假设与待确认项

| ID | 类型 | 描述 | 影响 | 处理建议 |
|----|------|------|------|----------|
| RISK-01 | 风险 | 遗留项目模板较重 | 用户觉得 SDC 复杂 | 不新增公共命令，仅作为 legacy 内部门禁 |
| RISK-02 | 风险 | CLI 无法真正理解项目 | 只能创建模板和提示 | 真实分析由 skill/AI 根据代码证据完成 |
| ASM-01 | 假设 | 用户希望本轮直接升级实现 | 本次直接改代码和文档 | 已记录 change |

## 8. 追溯关系矩阵

| SCN | REQ | AC | 风险/假设 |
|-----|-----|----|-----------|
| SCN-01 | REQ-01 | AC-01, AC-05 | RISK-02 |
| SCN-02 | REQ-02 | AC-02, AC-03, AC-05 | RISK-01 |
| SCN-03 | REQ-03 | AC-04, AC-05 | RISK-01, ASM-01 |
