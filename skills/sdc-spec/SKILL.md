---
name: sdc-spec
description: "Turn vague requirements into structured, verifiable specs with acceptance criteria, test plan, risks, and next steps."
---

# Skill: SDC 规范生成 sdc-spec

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

- Role contract: `../sdc-shared/role-contracts.md`, section `sdc-spec`.
- Decision, traceability, and stop-line rules: `../sdc-shared/workflow-standards.md`.
- If discovery is incomplete: `../sdc-shared/discovery-gate.md`.
- Spec schema: `../sdc-shared/artifact-schemas.md`.

## 执行步骤

1. 读取 `.sdc/constitution.md`、`.sdc/project.md`、`.sdc/knowledge/index.md`、相关产品/技术知识、当前 change 的 `proposal.md`、`discovery.md` 和已有 `spec.md`。
2. 如果 `discovery.md` 仍有阻塞问题，不能输出 `Confirmed` spec。
3. 如果需求明显不确定且没有 discovery，建议回到 `/sdc:change` 的 Discovery Gate。
4. 建立或更新 Decision Ledger。
5. 只把 `Confirmed` 或明确不影响当前 MVP 的 `Deferred` 决策写入正式 REQ/AC/INV。
6. 记录 Knowledge Sources Used；如果知识缺失、过期或冲突，输出 Knowledge Gap / Stop-Line。
7. 输出 SCN/REQ/AC、业务不变量、验证策略、风险、追溯矩阵和下一步。
8. 如果仍缺关键确认，优先输出 Stop-Line 信息和下一批 3-5 个确认问题；只有用户明确要求保留草稿时，才输出 Draft spec。

## Spec 要求

参考 `../sdc-shared/artifact-schemas.md` 的 spec shape。最低必须包含：

- 文档状态：Draft / Confirmed。
- Knowledge Sources Used。
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
- Discovery 未退出不能输出 Confirmed spec。
- Open Questions 未闭合时不得顺手生成完整 design/tasks。
- 禁止“如果不对告诉我，我先改”；解释推断后必须等待用户确认。
