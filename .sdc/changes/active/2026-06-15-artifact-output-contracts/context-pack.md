# Context Pack

## Goal

Implement Artifact Output Contracts for SDC so existing stages enforce enterprise-style input/output deliverables without adding public commands.

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| spec.md | Confirmed | AC-01 through AC-04 | Defines scope and acceptance |
| design.md | Confirmed | Artifact Output Contract and Test Matrix | Defines implementation structure |
| impact.md | Confirmed | Direct change table | Defines Brownfield impact radius |
| skills/sdc-shared/* | Confirmed | Shared references | Keeps prompt rules consistent |
| sdc-cli.py | Confirmed | CLI validation/templates | Enforces the contract |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## Common Ground Used

| ID | Tier | Statement | Source | Why It Matters |
|---|---|---|---|---|
| CG-01 | ESTABLISHED | SDC keeps a small public command surface and routes specialist behavior internally. | README.md, expert-routing.md | Guides non-command implementation |
| CG-02 | ESTABLISHED | Discovery Open must not generate final artifacts. | workflow-standards.md | Keeps output contract draft-only during discovery |
| CG-03 | ESTABLISHED | Final validation must block unconfirmed execution inputs. | sdc-cli.py | Keeps output contracts compatible with gates |

## Expert Profiles Used

| Profile | Why Used | Sources Read | Decisions / Checks Affected |
|---|---|---|---|
| product-discovery | The request is about workflow/product shape and command simplicity | discovery.md, README.md | Kept public commands unchanged |
| architecture | The change modifies shared prompt/reference architecture | skills/sdc-shared/*, commands/* | Added one reference instead of command sprawl |
| test-strategy | Enforcement needs deterministic proof | evals/sdc-flow/*, scripts/audit-release.mjs | Added negative eval and audit markers |
| documentation | README/metadata must describe new behavior succinctly | README.md, plugin manifests | Updated user-facing docs and package metadata |

## Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | N/A | No product workflow/state behavior changed by SDC itself | design.md#process-state-diagrams | N/A because this change updates governance and templates, not a business workflow |
| Sequence / Integration Diagram | N/A | No multi-service/runtime integration | design.md#sequence-integration-diagrams | N/A because SDC remains prompt/CLI-only |
| API / Contract Specification | N/A | No public API endpoint/event contract | design.md#api-contract-specification | N/A because there is no API endpoint or event schema |
| Data Model / Migration Contract | N/A | No database/schema migration | design.md#data-model-migration-contract | N/A because SDC has no persistent database schema |
| UX Flow / Interaction States | N/A | No frontend/UI surface | design.md#ux-flow-interaction-states | N/A because this change touches CLI, docs, and prompts |
| Test Matrix | Required | AC validation | design.md#test-matrix | AC-01 through AC-04 are mapped in design.md |
| Deploy / Release Checklist | N/A | No service runtime deploy | design.md#deploy-release-checklist | N/A because package release is covered by audit/eval checks |
| AI Involvement Note | Required | AI-assisted workflow change | design.md#ai-involvement-note | Required for archive/check evidence |

## Confirmed Product Knowledge

- SDC should keep few public commands and route detailed deliverables internally.
- Output deliverables are stage artifacts, not new public commands.

## Confirmed Technical Knowledge

- `sdc-cli.py` owns managed workspace templates and validation checks.
- `scripts/audit-release.mjs` owns release-time marker checks.
- `evals/sdc-flow/sdc_flow_provider.py` owns deterministic CLI flow scenarios.

## Execution Boundaries

- Do not add public command files.
- Do not publish npm or bump version in this change.
- Do not copy internal private document content into public files.
- Do not remove existing Common Ground, Expert Routing, knowledge, or impact gates.

## Forbidden Assumptions

- Do not infer product workflows, APIs, schemas, rollout policy, or permissions from output contract triggers.
- Do not mark optional outputs as N/A without evidence.
- Do not treat AI involvement as a substitute for human review.

## Task And Traceability Summary

- T001 -> REQ-01 / AC-01
- T002 -> REQ-02 / AC-02
- T003 -> REQ-03 / AC-03
- T004, T900 -> REQ-04 / AC-04

## Validation Commands

- `python3 -m py_compile sdc-cli.py evals/sdc-flow/run_sdc_flow.py evals/sdc-flow/sdc_flow_provider.py`
- `node --check scripts/audit-release.mjs`
- `npm run audit`
- `npm run eval:sdc`
- `python3 sdc-cli.py validate 2026-06-15-artifact-output-contracts`

## Knowledge Candidate Routing

- Product knowledge candidates: SDC has Artifact Output Contract as an internal stage deliverable standard.
- Technical knowledge candidates: CLI validates triggered artifact output coverage.
- Memory/procedure candidates: after changing SDC templates, rerun `sdc init`, remove generated backups, then run audit/evals.
