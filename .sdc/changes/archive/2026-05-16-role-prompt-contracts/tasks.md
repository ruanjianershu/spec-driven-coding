# Tasks

## 实现任务

- [x] T001 [REQ-01] [AC-01] [Phase 1] [Size: M] 为所有 SDC skills 增加英文 Role Prompt Contract
  - Depends on: none
  - Verify: `for f in skills/*/SKILL.md; do rg "## Role Prompt Contract" "$f" >/dev/null || exit 1; done`
  - Source: spec.md#AC-01

- [x] T002 [REQ-02] [AC-02] [Phase 1] [Size: S] 确保所有 contract 包含统一四段结构
  - Depends on: T001
  - Verify: `for f in skills/*/SKILL.md; do rg "### Role" "$f" >/dev/null && rg "### Operating Contract" "$f" >/dev/null && rg "### Evidence Rules" "$f" >/dev/null && rg "### Output Contract" "$f" >/dev/null || exit 1; done`
  - Source: spec.md#AC-02

- [x] T003 [REQ-03] [AC-03] [Phase 1] [Size: S] 更新 README/docs/changelog/package/plugin metadata 到 1.1.4
  - Depends on: T002
  - Verify: `rg "1.1.4|role prompt contract|Role Prompt Contract" README.md CHANGELOG.md package.json .claude-plugin .codex-plugin docs`
  - Source: spec.md#AC-03

## 验证任务

- [x] T900 [REQ-01] [AC-04] [Phase Verify] [Size: S] 运行 SDC change 校验
  - Depends on: T001, T002, T003
  - Verify: `python3 sdc-cli.py validate 2026-05-16-role-prompt-contracts`
  - Source: spec.md#AC-04

- [x] T901 [REQ-03] [AC-04] [Phase Verify] [Size: S] 运行发布前基础验证
  - Depends on: T900
  - Verify: `python3 -m py_compile sdc-cli.py && node --check bin/install.js && claude plugin validate . && npm pack --dry-run`
  - Source: spec.md#AC-04
