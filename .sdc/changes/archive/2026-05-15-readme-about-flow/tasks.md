# Tasks

## 实现任务

- [x] T001 [REQ-04] [AC-05] [Phase 1] [Size: S] 初始化 SDC 工作区并创建本次 change 记录
  - Depends on: none
  - Verify: `python3 sdc-cli.py init && python3 sdc-cli.py change readme-about-flow`
  - Source: spec.md#AC-05

- [x] T002 [REQ-01] [AC-01] [Phase 1] [Size: M] 优化 README 第一屏定位和 discipline core 表达
  - Depends on: T001
  - Verify: `git diff -- README.md`
  - Source: spec.md#AC-01

- [x] T003 [REQ-02] [AC-02] [Phase 1] [Size: M] 补充实际 SDC lifecycle 示例
  - Depends on: T002
  - Verify: `rg "实际工作流|init -> change" README.md`
  - Source: spec.md#AC-02

- [x] T004 [REQ-02] [AC-03] [Phase 1] [Size: S] 收紧 Codex 与 Claude Code 的使用差异说明
  - Depends on: T003
  - Verify: `rg "skill plugin|slash command" README.md`
  - Source: spec.md#AC-03

- [x] T005 [REQ-03] [AC-04] [Phase 1] [Size: S] 更新 package/plugin metadata 和 GitHub About
  - Depends on: T004
  - Verify: `gh repo view --json description,repositoryTopics`
  - Source: spec.md#AC-04

## 验证任务

- [x] T900 [REQ-04] [AC-05] [Phase Verify] [Size: S] 运行 SDC validate/check
  - Depends on: T001, T002, T003, T004, T005
  - Verify: `python3 sdc-cli.py validate 2026-05-15-readme-about-flow && python3 sdc-cli.py check 2026-05-15-readme-about-flow`
  - Source: spec.md#AC-05

- [x] T901 [REQ-04] [AC-05] [Phase Verify] [Size: S] 运行代码和打包验证
  - Depends on: T900
  - Verify: `python3 -m py_compile sdc-cli.py && node --check bin/install.js && claude plugin validate . && npm pack --dry-run`
  - Source: spec.md#AC-05
