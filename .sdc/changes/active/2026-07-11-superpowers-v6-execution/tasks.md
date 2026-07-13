# Tasks

## Global Constraints

| ID | Constraint | Source | Applies To |
|---|---|---|---|
| GC-01 | Do not add or rename public commands | spec.md#INV-01 | all tasks |
| GC-02 | Runtime scratch must be git-ignored and never the only evidence | spec.md#INV-02 | T001, T002, T004 |
| GC-03 | User-authored change files are not silently rewritten | impact.md | T002, T004 |
| GC-04 | Reviewer is read-only and cannot be coached to suppress findings | spec.md#REQ-03 | T001, T002, T900 |
| GC-05 | Do not dispatch multiple implementation tasks in parallel | discovery.md#DEC-05 | all tasks |

## Plan Preflight

- Status: Passed
- Reviewed Against: spec.md, impact.md, design.md, tasks.md, standards, Artifact Output Contract
- Findings: None; tasks are independently testable and all interfaces are defined.

## 实现任务

- [x] T001 [REQ-01] [AC-01] [Phase 1] [Size: M] Define execution orchestration and route it through SDC stages
  - Depends on: none
  - Files: sdc-references/execution-orchestration.md, commands/plan.md, commands/apply.md, commands/check.md, shared references, public/advanced skills
  - Consumes: confirmed execution scope and existing SDC governance contracts
  - Produces: vendor-neutral serial task execution, Plan Preflight, file-handoff, dual-verdict review, and final-review contract used by T002
  - Verify: rg "Plan Preflight|Spec Compliance|Final Whole-Change Review" commands skills
  - Expected: all existing plan/apply/check and direct skills route to one shared execution contract
  - Review: Approved
  - Evidence: notes.md#validation-evidence
  - Source: spec.md#REQ-01, spec.md#REQ-03

- [x] T002 [REQ-01] [AC-01] [Phase 2] [Size: M] Enforce task schemas, migration, handoffs, ledger, and delivery evidence in CLI
  - Depends on: T001
  - Files: sdc-cli.py, scripts/sdc-task-brief.py, scripts/sdc-review-package.py, .sdc managed templates
  - Consumes: T001 execution contract and existing Artifact/Knowledge/Common Ground gates
  - Produces: enforceable task/constraint/preflight fields, resolvable dual-review evidence, runtime handoffs, structured ledger checks, and fingerprinted idempotent migration for T004/T900
  - Verify: python3 -m py_compile sdc-cli.py scripts/sdc-task-brief.py scripts/sdc-review-package.py
  - Expected: syntax passes; negative evals block incomplete plan/review/ledger evidence while preserving user-modified managed files
  - Review: Approved
  - Evidence: notes.md#validation-evidence
  - Source: spec.md#REQ-01, spec.md#REQ-02, spec.md#REQ-03, spec.md#REQ-05

- [x] T003 [REQ-04] [AC-06] [Phase 2] [Size: M] Harden Codex marketplace metadata and deterministic packaging
  - Depends on: T001
  - Files: .agents/plugins/marketplace.json, .codex-plugin/plugin.json, bin/install.js, scripts/package-codex-plugin.py, package.json, skills/sdc-*, sdc-references
  - Consumes: Codex v6.1 marketplace and empty-hooks findings plus existing generated skill layout
  - Produces: source-installable Codex workflow with transactional stale-layout replacement and recovery plus rootless minimal portal zip and checksum
  - Verify: python3 scripts/package-codex-plugin.py --allow-dirty --output /tmp/sdc-codex-plugin-1.3.0.zip
  - Expected: source and archive contain valid public/advanced skills, shared contracts are not exposed as a fake skill, archives are byte-identical, and Claude/source-only paths are excluded
  - Review: Approved
  - Evidence: notes.md#validation-evidence
  - Source: spec.md#REQ-04

- [x] T004 [REQ-05] [AC-05] [Phase 3] [Size: M] Add eval/audit/docs/version migration and repair real init drift
  - Depends on: T002, T003
  - Files: evals/sdc-flow, scripts/audit-release.mjs, README.md, CHANGELOG.md, docs, manifests, .sdc workspace
  - Consumes: T002 validators/helpers and T003 package contract
  - Produces: 1.3.0 documentation, release protection, 51-scenario eval suite, and fingerprinted idempotent workspace/runtime-ignore migration used by T900
  - Verify: npm run audit && npm run eval:sdc
  - Expected: release audit passes and all deterministic scenarios pass
  - Review: Approved
  - Evidence: notes.md#validation-evidence
  - Source: spec.md#REQ-05, spec.md#REQ-06

## 验证任务

- [x] T900 [REQ-06] [AC-06] [Phase Verify] [Size: M] Run complete syntax, SDC, packaging, and npm release verification
  - Depends on: T001, T002, T003, T004
  - Files: repository-wide changed files and generated package under /tmp
  - Consumes: all implementation outputs and AC-01 through AC-06
  - Produces: final delivery evidence and approved whole-change review
  - Verify: npm run audit && npm run eval:sdc && git diff --check && npm pack --dry-run
  - Expected: all commands pass, Codex archive is complete, and SDC check approves the change
  - Review: Approved
  - Evidence: notes.md#validation-evidence
  - Source: spec.md#AC-01, spec.md#AC-02, spec.md#AC-03, spec.md#AC-04, spec.md#AC-05, spec.md#AC-06
