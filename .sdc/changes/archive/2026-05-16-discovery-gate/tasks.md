# Tasks

## 实现任务

- [x] T001 [REQ-01] [AC-01] [Phase 1] [Size: M] 升级 sdc-change 的 Discovery Gate 规则
  - Depends on: none
  - Verify: `rg "Discovery Gate|需求确定性" skills/sdc-change/SKILL.md`
  - Source: spec.md#AC-01

- [x] T002 [REQ-02] [AC-02] [Phase 1] [Size: S] 升级 sdc-spec 消费 discovery.md 的规则
  - Depends on: T001
  - Verify: `rg "discovery.md|Discovery" skills/sdc-spec/SKILL.md`
  - Source: spec.md#AC-02

- [x] T003 [REQ-03] [AC-03] [Phase 1] [Size: M] 更新 CLI init/change 模板生成 discovery.md
  - Depends on: T002
  - Verify: `tmpdir=$(mktemp -d); (cd "$tmpdir" && python3 /Users/liting/andy-opc/spec-driven-coding/sdc-cli.py init >/dev/null && python3 /Users/liting/andy-opc/spec-driven-coding/sdc-cli.py change demo >/dev/null && test -f .sdc/templates/discovery.md && find .sdc/changes/active -name discovery.md); rm -rf "$tmpdir"`
  - Source: spec.md#AC-03

- [x] T004 [REQ-04] [AC-04] [Phase 1] [Size: S] 更新 README/docs/changelog/package/plugin metadata
  - Depends on: T003
  - Verify: `rg "Discovery Gate|change 是入口|spec 是" README.md docs/sdc-discipline-core.md CHANGELOG.md package.json`
  - Source: spec.md#AC-04

## 验证任务

- [x] T900 [REQ-03] [AC-05] [Phase Verify] [Size: S] 运行 SDC change 校验
  - Depends on: T001, T002, T003, T004
  - Verify: `python3 sdc-cli.py validate 2026-05-16-discovery-gate`
  - Source: spec.md#AC-05

- [x] T901 [REQ-03] [AC-05] [Phase Verify] [Size: S] 运行发布前基础验证
  - Depends on: T900
  - Verify: `python3 -m py_compile sdc-cli.py && node --check bin/install.js && claude plugin validate . && npm pack --dry-run`
  - Source: spec.md#AC-05
