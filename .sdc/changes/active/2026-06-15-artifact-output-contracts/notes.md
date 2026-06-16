# Notes

> Change: 2026-06-15-artifact-output-contracts
> Status: Confirmed - Implementation In Progress

## Discovery Notes

- User confirmed the recommended scope: add Artifact Output Contract as an internal SDC layer without adding public commands.
- Internal workflow reference was used only for design inspiration around explicit stage inputs/outputs.

## Confirmed Decisions

- Keep public commands unchanged.
- Add `skills/sdc-shared/artifact-output-contracts.md`.
- Require final `Test Matrix`.
- Allow optional outputs as N/A only with evidence reason.
- Add CLI/eval/audit enforcement.

## Changed Files

- `skills/sdc-shared/artifact-output-contracts.md`
- `skills/sdc-shared/workflow-standards.md`
- `skills/sdc-shared/delivery-gates.md`
- `skills/sdc-shared/artifact-schemas.md`
- `skills/sdc-shared/role-contracts.md`
- `skills/sdc-shared/workflow-manifest.yaml`
- `commands/change.md`
- `commands/plan.md`
- `commands/apply.md`
- `commands/check.md`
- `commands/archive.md`
- `skills/sdc-spec/SKILL.md`
- `skills/sdc-validate/SKILL.md`
- `skills/sdc-review/SKILL.md`
- `skills/sdc-test/SKILL.md`
- `skills/sdc-quality/SKILL.md`
- `sdc-cli.py`
- `evals/sdc-flow/sdc_flow_provider.py`
- `evals/sdc-flow/promptfooconfig.yaml`
- `scripts/audit-release.mjs`
- `README.md`
- `CHANGELOG.md`
- package/plugin metadata
- `.sdc` managed templates and this change record

## Validation Evidence

- `python3 -m py_compile sdc-cli.py evals/sdc-flow/run_sdc_flow.py evals/sdc-flow/sdc_flow_provider.py` passed.
- `node --check scripts/audit-release.mjs` passed.
- `git diff --check` passed.
- `npm run audit` passed: Release audit passed for SDC 1.2.1.
- `npm run eval:sdc` passed: 13 deterministic SDC flow evals passed, including `missing_artifact_output_contract_blocks_execution`.
- `python3 sdc-cli.py validate 2026-06-15-artifact-output-contracts` passed.
- `python3 sdc-cli.py init` regression passed after narrowing stale-template detection; existing project standards README was not overwritten.

## Pending Questions

None.
