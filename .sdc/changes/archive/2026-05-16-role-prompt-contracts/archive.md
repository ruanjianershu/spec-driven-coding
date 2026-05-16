# Archive

> Change: 2026-05-16-role-prompt-contracts
> Archived: 2026-05-16T13:55:51.806435

## 归档结果

- 稳定规范: `../../specs/2026-05-16-role-prompt-contracts.md`
- 原始变更目录: `.sdc/changes/active/2026-05-16-role-prompt-contracts`

## 交付结论

可以交付。所有 SDC skills 已补充英文 Role Prompt Contract，每次 skill 调用时都会明确专家角色、工作契约、证据规则和输出契约，从而具备角色化任务 Prompt 的稳定行为，同时保持 SDC 的少指令模型。

## 追溯摘要

- REQ/AC/T### 覆盖：REQ-01/AC-01/T001，REQ-02/AC-02/T002，REQ-03/AC-03/T003，AC-04/T900/T901。
- 验证证据：全 skill contract 搜索、全 skill 四段结构搜索、`python3 sdc-cli.py validate 2026-05-16-role-prompt-contracts`、`git diff --check`、`python3 -m py_compile sdc-cli.py`、`node --check bin/install.js`、manifest JSON parse、`claude plugin validate .`、`npm pack --dry-run` 均通过。
- 遗留项：无阻塞遗留。后续可基于真实调用日志继续微调各 skill 的 Role Prompt Contract。
