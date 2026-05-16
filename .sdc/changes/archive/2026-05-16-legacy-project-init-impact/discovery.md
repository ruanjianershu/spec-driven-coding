# Discovery

## Current Understanding

SDC init 现在能建立统一 `.sdc/` 结构，但对新项目和遗留项目的差异处理还不够清楚。用户希望遗留项目在初始化时不只是建目录，还要先形成项目整体认知，并准备后续需求变更影响面分析。

## Candidate Directions

| Option | Description | Pros | Cons | Status |
|--------|-------------|------|------|--------|
| A | 新增独立公开指令处理遗留项目 | 功能边界清晰 | 增加用户记忆负担，违背少指令原则 | Rejected |
| B | 在 `/sdc:init` 和 `/sdc:check` 内部增加 legacy/brownfield 分支 | 保持入口少，符合现有模式 | 需要补充模板和校验边界 | Accepted |
| C | 只在 README 写建议，不改模板 | 改动小 | Agent 不会稳定执行 | Rejected |

## Tradeoffs

- SDC 不应为 legacy 场景增加新公共 slash command。
- CLI 可以提供模板资产，但真实项目认知必须由 AI skill 扫描代码后填充。
- 遗留项目影响分析应同时出现在计划前和最终 review/check 后，前者防误改，后者防漏报。

## Recommended MVP

在 `/sdc:init` 中加入项目类型识别：Greenfield 直接建标准结构；Brownfield/Legacy 生成并维护 `project-cognition.md`。具体需求的影响面分析不在 init 做，而是在 `/sdc:change` 需求确认后写入当前 change 的 `impact.md`。在 `/sdc:review` 和 `/sdc:check` delivery 模式中，如果识别为遗留项目，必须输出“老系统改造点与影响点分析”。

## Decision Ledger

| ID | Decision | Status | Source | Impact | Next Step |
|----|----------|--------|--------|--------|-----------|
| DEC-01 | 不新增公开 legacy slash command，复用 init/check/review | Confirmed | 用户曾强调少指令、普通模式保持精简 | High | 实施 |
| DEC-02 | 初始化资产新增 `project-cognition.md`；每个 change 新增 `impact.md` | Confirmed | 用户修正影响面分析时机 | High | 实施 |
| DEC-03 | 遗留项目最终 code review/check 必须输出改造点和影响点 | Confirmed | 用户明确要求 | High | 实施 |

## Open Questions

| ID | Question | Why It Matters | Options | Required Before |
|----|----------|----------------|---------|-----------------|
| OQ-01 | 是否需要公开新指令 | 影响命令复杂度 | 不新增 / 新增 | Resolved by DEC-01 |

## Exit Criteria

- [x] MVP scope confirmed
- [x] high-impact decisions confirmed or explicitly deferred
- [x] acceptance direction is clear
