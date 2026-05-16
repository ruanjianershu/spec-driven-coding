# Tasks

## 实现任务

- [x] T001 [REQ-01] [AC-01] [Phase 1] [Size: M] 升级 sdc-spec 的 Brainstorm-first 和 Decision Ledger 规则
  - Depends on: none
  - Verify: `rg "Brainstorm-first|Decision Ledger|Confirmed" skills/sdc-spec/SKILL.md`
  - Source: spec.md#AC-01

- [x] T002 [REQ-02] [AC-02] [Phase 1] [Size: S] 在 sdc-spec 中增加审批/提醒等高影响业务规则确认要求
  - Depends on: T001
  - Verify: `rg "审批|提醒|TBD|Proposed" skills/sdc-spec/SKILL.md`
  - Source: spec.md#AC-02

- [x] T003 [REQ-03] [AC-03] [Phase 1] [Size: M] 升级 sdc-plan 的 Technical Consent Gate 和 Stop-Line 规则
  - Depends on: T001
  - Verify: `rg "Technical Consent Gate|Stop-Line|MVP Slice" skills/sdc-plan/SKILL.md`
  - Source: spec.md#AC-03

- [x] T004 [REQ-04] [AC-04] [Phase 1] [Size: M] 升级 validate/check 对未确认决策和 silent defaults 的阻塞检查
  - Depends on: T001, T003
  - Verify: `rg "Unconfirmed|Silent Default|TBD" skills/sdc-validate/SKILL.md skills/sdc-check/SKILL.md`
  - Source: spec.md#AC-04

- [x] T005 [REQ-05] [AC-05] [Phase 1] [Size: M] 升级 init/harness/constitution/CLI 模板的人类确认规则
  - Depends on: T004
  - Verify: `rg "Human Confirmation|No Silent Defaults|Decision Ledger" .sdc/constitution.md skills/sdc-init/SKILL.md skills/sdc-harness/SKILL.md sdc-cli.py`
  - Source: spec.md#AC-05

- [x] T006 [REQ-01] [AC-01] [Phase 1] [Size: S] 更新 README/docs/changelog/package/plugin metadata
  - Depends on: T005
  - Verify: `rg "consent|确认|Decision Ledger" README.md docs/sdc-discipline-core.md CHANGELOG.md package.json`
  - Source: spec.md#AC-01

## 验证任务

- [x] T900 [REQ-04] [AC-06] [Phase Verify] [Size: S] 运行 SDC change 校验
  - Depends on: T001, T002, T003, T004, T005, T006
  - Verify: `python3 sdc-cli.py validate 2026-05-16-consent-gates`
  - Source: spec.md#AC-06

- [x] T901 [REQ-04] [AC-06] [Phase Verify] [Size: S] 运行发布前基础验证
  - Depends on: T900
  - Verify: `python3 -m py_compile sdc-cli.py && node --check bin/install.js && claude plugin validate . && npm pack --dry-run`
  - Source: spec.md#AC-06
