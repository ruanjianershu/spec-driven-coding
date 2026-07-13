# Tasks

## 实现任务

- [x] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] Add shared Artifact Output Contract reference and README/changelog positioning
  - Depends on: none
  - Verify: `rg "Artifact Output Contract|Test Matrix|上线检查清单" README.md CHANGELOG.md sdc-references/artifact-output-contracts.md`
  - Source: spec.md#AC-01

- [x] T002 [REQ-02] [AC-02] [Phase 1] [Size: M] Wire Artifact Output Contract through commands, advanced skills, schemas, gates, and role contracts
  - Depends on: T001
  - Verify: `rg "artifact-output-contracts|Artifact Output Contract" commands skills`
  - Source: spec.md#AC-02

- [x] T003 [REQ-03] [AC-03] [Phase 1] [Size: M] Add CLI templates and validation for triggered output artifacts
  - Depends on: T002
  - Verify: `rg "ARTIFACT_OUTPUT_CONTRACTS|validate_artifact_output_contract|Test Matrix" sdc-cli.py`
  - Source: spec.md#AC-03

- [x] T004 [REQ-04] [AC-04] [Phase 1] [Size: S] Add eval and audit coverage for missing triggered output artifacts
  - Depends on: T003
  - Verify: `rg "missing_artifact_output_contract_blocks_execution|Artifact Output Contract" evals scripts/audit-release.mjs`
  - Source: spec.md#AC-04

## 验证任务

- [x] T900 [REQ-04] [AC-04] [Phase Verify] [Size: S] Run syntax checks, release audit, deterministic evals, and SDC self-validation
  - Depends on: T001, T002, T003, T004
  - Verify: `python3 -m py_compile sdc-cli.py evals/sdc-flow/run_sdc_flow.py evals/sdc-flow/sdc_flow_provider.py && node --check scripts/audit-release.mjs && npm run audit && npm run eval:sdc && python3 sdc-cli.py validate 2026-06-15-artifact-output-contracts`
  - Source: spec.md#AC-04
