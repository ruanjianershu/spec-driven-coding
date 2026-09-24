---
name: sdc-spec
description: "Use when requirements must be refined into a structured SDC specification after discovery."
---

# Skill: SDC 规范生成 sdc-spec

Resolve `SDC_PLUGIN_ROOT` from this installed command/skill: the parent of `commands/`, or two levels above `skills/<skill>/`. Do not assume this variable is already set. Verify the helper exists and keep the target project as the working directory when invoking it. For legacy direct skills and Hermes layouts, if the derived root lacks `sdc-cli.py`, use its `sdc-runtime/` child after verifying both the CLI and runtime helper exist there. Missing helpers are an installation blocker, not permission to guess another checkout.

## 触发条件

当用户输入以下任一内容时，自动触发本技能：

- `sdc-spec`
- "帮我生成规范"
- "先理清楚需求"
- "这个需求怎么做"

## 核心使命

将已确认或接近确认的需求转化为结构化、可验证、可执行的规范文档。spec 必须支持：

```text
SCN-* -> REQ-* -> AC-* -> T### -> validation evidence
```

`sdc-spec` 不能替用户决定产品规则或技术方案；它只把已确认的事实写成规范，把未确认事项留在 Decision Ledger 或 Open Questions。

## Reference Loading

Load only what is needed:

- For an existing `compact.json`, use `../../sdc-references/compact-workflow.md` for confirmation and traceability instead of generating a second spec. Wider requirements require explicit escalation, not implicit format conversion.
- Domain meanings or glossary conflicts: `../../sdc-references/domain-knowledge.md`.

- Role contract: `../../sdc-references/role-contracts.md`, section `sdc-spec`.
- Decision, traceability, and stop-line rules: `../../sdc-references/workflow-standards.md`.
- Common Ground rules: `../../sdc-references/common-ground.md`.
- If discovery is incomplete: `../../sdc-references/discovery-gate.md`.
- Spec schema: `../../sdc-references/artifact-schemas.md`.
- Artifact output contracts: `../../sdc-references/artifact-output-contracts.md`.

## 执行步骤

1. 读取 `.sdc/constitution.md`、`.sdc/project.md`、`.sdc/common-ground.md`、`.sdc/knowledge/index.md`、相关产品/技术知识、当前 change 的 `proposal.md`、`discovery.md` 和已有 `spec.md`。
2. 如果 `discovery.md` 仍有阻塞问题，只维护已授权的 discovery、可选 Draft proposal 和简短 notes，不创建 spec/design/tasks。
3. 如果需求明显不确定且没有 discovery，建议回到 `/sdc:change` 的 Discovery Gate。
4. 建立或更新 Decision Ledger。
5. 只把 `Confirmed` 或明确不影响当前 MVP 的 `Deferred` 决策写入正式 REQ/AC/INV。
6. 记录 Knowledge Sources Used；如果知识缺失、过期或冲突，输出 Knowledge Gap / Stop-Line。
7. 输出 SCN/REQ/AC、业务不变量、验证策略、风险、追溯矩阵和下一步。
8. 输出或更新 Artifact Output Contract：记录本需求是否触发流程图、时序/集成图、API 契约、数据/迁移契约、UX 状态、测试矩阵、上线检查清单和 AI 参与说明。未确认的输出要求保持 Proposed，不得进入 final spec。
9. 只询问缺失的阻塞项，不设问题数量；引用仍有效的已有确认或有边界的明确授权，不重复确认。未决事项留在 discovery 中。
10. Confirmed spec 和 Discovery Exit Criteria 有效时，执行 `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" state set --change <change-id> --state confirmed --source spec-stage --evidence spec.md`。存量项目在此后完成 impact 分析，再进入 plan。相同且仍有效的状态可幂等恢复；改变需求须按 `runtime-context.md` 显式 reopen，不能跳过确认。

## Spec 要求

参考 `../../sdc-references/artifact-schemas.md` 的 spec shape。最低必须包含：

- 文档状态：Draft / Confirmed。
- Knowledge Sources Used。
- Common Ground Used。
- Artifact Output Contract。
- Knowledge Gaps（没有则明确为空）。
- Decision Ledger。
- Discovery Summary。
- Glossary。
- 背景、目标、非目标。
- In Scope / Out of Scope。
- Business Invariants。
- SCN / REQ / AC。
- 验证策略。
- 风险、假设、待确认项。
- 追溯关系矩阵。

## 输出格式

```text
📋 SDC 规范文档
==================================================

## 状态
Draft / Confirmed

## Decision Ledger
- ...

## SCN / REQ / AC
- ...

## 验证策略
- ...

## 阻塞项
- ...

## 下一步
👉 ...
```

## 质量红线

- 每个 REQ 必须有至少一个可验证 AC。
- AC 必须描述业务行为，不描述内部实现。
- 必须包含 Decision Ledger、Glossary、业务不变量和追溯矩阵。
- Proposed / Assumed / TBD / Conflict 不得进入正式 REQ/AC/INV。
- spec 阶段不得混入未确认实现方案。
- spec 必须区分产品知识、技术知识和 memory candidate；memory 不能当作 confirmed fact。
- No Evidence, No Fact；没有 Source / Verified Against 的内容不能写成 final REQ/AC/INV。
- OPEN 或高影响 WORKING Common Ground 不能写成 final REQ/AC/INV。
- Discovery 未退出不能输出 Confirmed spec。
- Open Questions 未闭合时不得顺手生成完整 design/tasks。
- 禁止“如果不对告诉我，我先改”；解释推断后必须等待用户确认。
