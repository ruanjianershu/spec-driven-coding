# Tasks

## 实现任务

- [x] T001 [REQ-01] [AC-01] [Phase 1] [Size: M] 升级 init 的 Greenfield/Brownfield 识别和项目整体认知模板
  - Depends on: none
  - Verify: `rg "project-cognition|Greenfield|Brownfield|Legacy" skills/sdc-init/SKILL.md sdc-cli.py README.md`
  - Source: spec.md#AC-01

- [x] T002 [REQ-02] [AC-02] [Phase 1] [Size: M] 在 change/plan/apply 中加入需求确认后的 Change Impact Gate
  - Depends on: T001
  - Verify: `rg "Change Impact Gate|impact.md|需求确认" skills/sdc-change/SKILL.md skills/sdc-plan/SKILL.md skills/sdc-apply/SKILL.md sdc-cli.py`
  - Source: spec.md#AC-02

- [x] T003 [REQ-03] [AC-04] [Phase 1] [Size: S] 在 review/check 中加入遗留项目最终改造点和影响点复核
  - Depends on: T002
  - Verify: `rg "老系统改造点|Legacy Final Impact Review|impact.md" skills/sdc-review/SKILL.md skills/sdc-check/SKILL.md`
  - Source: spec.md#AC-04

- [x] T004 [REQ-01] [AC-01] [Phase 1] [Size: S] 更新 README/docs/changelog/package/plugin metadata
  - Depends on: T003
  - Verify: `rg "project-cognition|Change Impact Gate|legacy|brownfield" README.md docs CHANGELOG.md package.json .claude-plugin .codex-plugin`
  - Source: spec.md#AC-01

## 验证任务

- [x] T900 [REQ-02] [AC-03] [Phase Verify] [Size: S] 运行 SDC change 校验
  - Depends on: T001, T002, T003, T004
  - Verify: `python3 sdc-cli.py validate 2026-05-16-legacy-project-init-impact`
  - Source: spec.md#AC-03

- [x] T901 [REQ-01] [AC-05] [Phase Verify] [Size: S] 运行发布前基础验证
  - Depends on: T900
  - Verify: `python3 -m py_compile sdc-cli.py && node --check bin/install.js && claude plugin validate . && npm pack --dry-run`
  - Source: spec.md#AC-05
