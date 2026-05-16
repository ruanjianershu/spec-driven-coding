# Notes

> Change: 2026-05-16-role-prompt-contracts
> Created: 2026-05-16T13:48:22.075662

## 实现记录

- 已为 14 个 `skills/*/SKILL.md` 增加英文 `## Role Prompt Contract`。
- 每个 contract 均包含 `### Role`、`### Operating Contract`、`### Evidence Rules`、`### Output Contract`。
- 已按 skill 职责定制角色：router、workspace architect、change facilitator、spec editor、planner、TDD executor、delivery gatekeeper、reviewer、validator、tester、quality assessor、archivist、harness maintainer、compat implementation executor。
- 已更新 README、discipline docs、marketplace docs、official submission notes、CHANGELOG、package/plugin metadata。
- 版本已提升到 1.1.4。

## 问题记录

- 无阻塞问题。

## 验证记录

- PASS 全 skill contract 搜索：14 个 skill 均包含 `## Role Prompt Contract`
- PASS 全 skill 四段结构搜索：Role / Operating Contract / Evidence Rules / Output Contract
- PASS `python3 sdc-cli.py validate 2026-05-16-role-prompt-contracts`
- PASS `git diff --check`
- PASS `python3 -m py_compile sdc-cli.py`
- PASS `node --check bin/install.js`
- PASS JSON parse: `package.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`
- PASS `claude plugin validate .`
- PASS `npm pack --dry-run`
