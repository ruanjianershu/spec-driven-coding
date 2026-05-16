# 2026-05-16-role-prompt-contracts Proposal

## 背景

用户指出参考流程的提示词会在每次调用时给出明确角色定义和工作要求。SDC 当前有流程规则，但角色化程度还不够强。

## 目标

- 为每个 SDC skill 补充英文 Role Prompt Contract。
- 明确每个 skill 的 Role、Operating Contract、Evidence Rules、Output Contract。
- 让 SDC 调用时具备“角色化任务 Prompt”的清晰专家角色，但仍保留 SDC 的少指令和可追溯流程。
- 更新 README、docs、changelog、package/plugin metadata。

## 非目标

- 不删除现有中文流程规则。
- 不新增公开 slash command。
- 不引入外部服务、MCP 或运行时依赖。

## 初始场景

- SCN-01: 用户调用任意 SDC skill，希望 AI 明确知道自己在扮演什么专家角色。
- SCN-02: 用户调用 SDC skill，希望 AI 不只按流程跑，还要遵守证据规则和输出契约。

## 初始需求

- REQ-01: every skill has role contract
- REQ-02: contract uses English
- REQ-03: docs and package metadata reflect the upgrade

## 初始验收标准

- AC-01: every `skills/*/SKILL.md` includes `## Role Prompt Contract`.
- AC-02: each contract includes Role, Operating Contract, Evidence Rules, and Output Contract.
- AC-03: README/changelog/package/plugin metadata mention role prompt contracts.
- AC-04: validation and package checks pass.

## 任务清单

见 `tasks.md`。

## 风险和回滚

- 风险：skill 文件变长。
- 缓解：英文 contract 保持短而强，不复制长模板。
- 回滚：删除新增 Role Prompt Contract sections 并恢复版本号。
