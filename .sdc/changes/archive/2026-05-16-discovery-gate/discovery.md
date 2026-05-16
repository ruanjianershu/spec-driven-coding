# Discovery

## Current Understanding

SDC 已有 consent gates，但 `/sdc:change` 仍需要一个正式的需求探索阶段，解决“不确定需求怎么往下推进”的问题。

## Candidate Directions

| Option | Description | Pros | Cons | Status |
|--------|-------------|------|------|--------|
| A | 新增独立 `/sdc:brainstorm` | 入口清晰 | 增加指令复杂度，偏离少指令原则 | Rejected |
| B | 复用 Superpowers brainstorm | 借用成熟心智 | SDC 失去独立闭环，安装依赖变复杂 | Rejected |
| C | 将 Discovery Gate 内置到 `/sdc:change` | 保持少指令，形成闭环 | 需要补模板和规则 | Confirmed |

## Tradeoffs

- Discovery 是阶段，不是新公开指令。
- `change` 是需求入口，`spec` 是规格细化。
- SDC 可吸收 brainstorm 方法，但输出必须收敛到 Decision Ledger 和 Confirmed spec。

## Recommended MVP

在 v1.1.2 中补齐：
- `sdc-change` Discovery Gate
- `sdc-spec` 消费 `discovery.md`
- CLI/template 生成 `discovery.md`
- README/docs 解释 change/spec 心智模型

## Decision Ledger

| ID | Decision | Status | Source | Impact | Next Step |
|----|----------|--------|--------|--------|-----------|
| DEC-01 | Discovery Gate 内置到 `/sdc:change` | Confirmed | 用户要求升级 | 高 | 实施 |
| DEC-02 | 不新增 `/sdc:brainstorm` | Confirmed | 少指令原则 | 中 | 文档说明 |
| DEC-03 | change 目录默认包含 discovery.md | Confirmed | 需要流程资产 | 中 | CLI/template 更新 |

## Open Questions

| ID | Question | Why It Matters | Options | Required Before |
|----|----------|----------------|---------|-----------------|

## Exit Criteria

- [x] MVP scope confirmed
- [x] high-impact decisions confirmed or explicitly deferred
- [x] acceptance direction is clear
