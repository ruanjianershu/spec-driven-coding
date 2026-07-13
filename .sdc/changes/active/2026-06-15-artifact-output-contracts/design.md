# Design

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| spec.md | Confirmed | REQ/AC and output contract | Defines implementation scope |
| impact.md | Confirmed | Direct change list | Defines Brownfield impact radius |
| sdc-references/workflow-standards.md | Confirmed | Current governance reference | Must be extended consistently |
| sdc-cli.py | Confirmed | Existing template and validation structure | Determines implementation approach |
| evals/sdc-flow/sdc_flow_provider.py | Confirmed | Existing deterministic scenarios | Determines regression test shape |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## Common Ground Used

| ID | Tier | Statement | Source | Why It Matters |
|---|---|---|---|---|
| CG-01 | ESTABLISHED | SDC keeps a small public command surface and routes specialist behavior internally. | README.md, expert-routing.md | Guides non-command implementation |
| CG-02 | ESTABLISHED | Discovery Open must not generate final artifacts. | workflow-standards.md | Keeps contract draft-only during discovery |
| CG-03 | ESTABLISHED | Final validation must block unconfirmed execution inputs. | sdc-cli.py | Keeps output contracts compatible with gates |

## Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | N/A | No product workflow/state behavior changed by SDC itself | design.md#process-state-diagrams | N/A because this change updates governance and templates, not a business workflow |
| Sequence / Integration Diagram | N/A | No multi-service/runtime integration | design.md#sequence-integration-diagrams | N/A because SDC remains prompt/CLI-only |
| API / Contract Specification | N/A | No public API endpoint/event contract | design.md#api-contract-specification | N/A because there is no API endpoint or event schema |
| Data Model / Migration Contract | N/A | No database/schema migration | design.md#data-model-migration-contract | N/A because SDC has no persistent database schema |
| UX Flow / Interaction States | N/A | No frontend/UI surface | design.md#ux-flow-interaction-states | N/A because this change touches CLI, docs, and prompts |
| Test Matrix | Required | AC validation | design.md#test-matrix | AC-01 through AC-04 are mapped below |
| Deploy / Release Checklist | N/A | No service runtime deploy | design.md#deploy-release-checklist | N/A because package release is covered by audit/eval checks, not deployment |
| AI Involvement Note | Required | AI-assisted workflow change | design.md#ai-involvement-note | Required so archive/check can state AI-authored changes and verification |

## Solution Summary / 方案摘要

Add a shared `artifact-output-contracts.md` reference and wire it through SDC's existing stages. The CLI gains an artifact output contract validator and managed templates gain contract tables plus a Test Matrix section. Evals gain a negative scenario proving that a triggered API output cannot be silently omitted.

## Impact Scope / 影响范围

- Shared references and role contracts.
- Public command prompts.
- Advanced skill prompts.
- CLI managed templates and validators.
- Deterministic evals and release audit.
- README/changelog/plugin metadata.
- Project `.sdc` change record.

## Non-Scope / 不改范围

- No new public slash commands.
- No package version bump.
- No npm publish.
- No external marketplace submission.
- No company-private internal document content copied into public files.

## Key Tradeoffs / 关键取舍

- Use one internal output contract instead of many public workflow commands.
- Make `Test Matrix` mandatory but allow other outputs to be N/A with evidence.
- Keep diagrams/contracts in `design.md` so `context-pack.md` can summarize instead of duplicating large content.

## Data, API, State, or Interaction Changes / 数据、接口、状态或交互变化

No runtime data/API/state/UI change. The only contract change is SDC artifact schema and validation expectations.

## Process / State Diagrams

N/A because this change updates governance and templates, not a business workflow.

## Sequence / Integration Diagrams

N/A because SDC remains prompt/CLI-only and does not add runtime integrations.

## API / Contract Specification

N/A because there is no API endpoint, event schema, webhook, or public runtime contract.

## Data Model / Migration Contract

N/A because SDC has no persistent database schema and this change does not migrate stored data.

## UX Flow / Interaction States

N/A because this change touches CLI, docs, and prompt instructions, not a frontend UI.

## Test Matrix

| AC | Scenario | Level | Verification | Expected Result | Status |
|---|---|---|---|---|---|
| AC-01 | Shared reference and docs describe Artifact Output Contract | Static audit | `npm run audit` | Required markers exist | Required |
| AC-02 | Managed templates include output contract and Test Matrix | Deterministic eval | `npm run eval:sdc` | stale template upgrade scenario passes | Required |
| AC-03 | API trigger without API contract is blocked | Deterministic eval | `npm run eval:sdc` | missing artifact output scenario passes | Required |
| AC-04 | Release checks pass | Release audit/evals | `npm run audit && npm run eval:sdc` | all checks pass | Required |

## Deploy / Release Checklist

N/A because this change does not deploy a service, alter runtime config, add jobs, or require rollback infrastructure. Package release readiness is covered by audit/eval/syntax checks.

## AI Involvement Note

This change is AI-assisted. Human-confirmed product direction: add enterprise-style output standards without adding public commands. Required review focus: confirm validation is not too heavy for simple changes, and confirm public/internal docs do not expose private internal reference content.

## Brownfield Impact Summary / 遗留影响摘要

This is a Brownfield change to the SDC repository. `impact.md` identifies direct changes in prompts, shared references, CLI templates/validators, evals, audit, docs, and metadata. No runtime public command contract changes.

## REQ/AC to Design Decision Mapping / 追溯映射

| REQ | AC | Design Decision |
|---|---|---|
| REQ-01 | AC-01 | Add shared English reference and docs |
| REQ-02 | AC-02 | Update stage prompts, skills, schemas, and templates |
| REQ-03 | AC-03 | Add CLI validator and negative eval |
| REQ-04 | AC-04 | Add audit/eval coverage |

## Risks, Rollback, and Migration / 风险、回滚和迁移

- Risk: output contract validation can feel strict. Mitigation: optional outputs support N/A with evidence.
- Risk: old `.sdc` templates are stale. Mitigation: safe init upgrade detects missing output contract sections.
- Rollback: remove new reference, prompt rules, validator, templates, eval scenario, audit markers, and docs.

## Alternatives / 替代方案

- Add public commands for each deliverable type: rejected because it increases user decision load.
- Documentation-only output standard: rejected because validate/check could still pass missing deliverables.
