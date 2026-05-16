# Design

## 背景

v1.1 已有追溯链，但缺少“源头可信度”。本次设计把 consent gate 分散到四个关键位置：spec、plan、validate/check、constitution/harness。

## 方案

1. `sdc-spec` 增加 Brainstorm-first、Decision Ledger、Confirmed-only 规则。
2. `sdc-plan` 增加 Technical Consent Gate 和 MVP Slice Gate。
3. `sdc-validate`/`sdc-check` 增加 unconfirmed decision/silent default 阻塞项。
4. `sdc-init`/CLI constitution 模板和 `sdc-harness` 增加 Human Confirmation / No Silent Defaults。
5. `README.md` 和 `docs/sdc-discipline-core.md` 增加 v1.1.1 consent gate 说明。
6. 版本提升到 `1.1.1` 并更新 changelog/package/plugin metadata。

## 影响范围

- `skills/sdc-spec/SKILL.md`
- `skills/sdc-plan/SKILL.md`
- `skills/sdc-validate/SKILL.md`
- `skills/sdc-check/SKILL.md`
- `skills/sdc-init/SKILL.md`
- `skills/sdc-harness/SKILL.md`
- `skills/sdc-core/SKILL.md`
- `sdc-cli.py`
- `.sdc/constitution.md`
- `README.md`
- `docs/sdc-discipline-core.md`
- package/plugin manifests and changelog

## 不改范围

- 不新增公开 slash command。
- 不调整 install/uninstall 路径。
- 不发布 npm，不提交 git，除非用户后续要求。

## 关键取舍

- 采用“高影响决策门禁”，而不是所有假设都强制确认，避免流程变成问卷。
- 允许 AI 提建议，但必须标注状态并等待确认后才能变成事实。
- plan 阶段可以给候选技术方案，但不能未确认就生成完整 apply 任务。

## REQ/AC 到设计决策的映射

| REQ | AC | 设计决策 |
|-----|----|----------|
| REQ-01 | AC-01 | `sdc-spec` 增加 Decision Ledger 和 Confirmed-only |
| REQ-02 | AC-01, AC-02 | `sdc-spec` 增加 brainstorm-first 和新能力澄清 |
| REQ-03 | AC-03 | `sdc-plan` 增加 Technical Consent Gate |
| REQ-04 | AC-04 | `sdc-validate`/`sdc-check` 增加阻塞项 |
| REQ-05 | AC-05 | init/harness/constitution 模板增加治理规则 |

## 风险

- 规则写在 skill 中仍依赖模型遵守。缓解：在多个技能和 validate/check 中重复设门禁。
- README 可能变长。缓解：只加短段，细节放 docs。

## 回滚方案

恢复本次修改的 skill/docs/metadata，并保留实验日志作为后续议题。

## 替代方案

- 只更新 README：无法约束实际 skill 行为。
- 新增 `/sdc:brainstorm` 指令：违背“少指令”的产品方向。
