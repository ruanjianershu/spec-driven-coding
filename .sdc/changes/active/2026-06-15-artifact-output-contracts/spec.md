# Spec

## 0. 文档元信息

- Status: Confirmed
- Schema: SDC 1.2.1
- Source: discovery.md, proposal.md, user confirmation

## 1. Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| discovery.md | Confirmed | Decision Ledger closed | Defines accepted scope |
| README.md | Confirmed | User-facing workflow docs | Must remain concise and accurate |
| skills/sdc-shared/workflow-standards.md | Confirmed | Existing governance reference | Must include new stop-line rule |
| skills/sdc-shared/delivery-gates.md | Confirmed | Existing gate reference | Must validate output coverage |
| sdc-cli.py | Confirmed | CLI templates and validators | Must enforce output contract |
| evals/sdc-flow/sdc_flow_provider.py | Confirmed | Deterministic eval suite | Must prove enforcement |

## 1.1 Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## 1.2 Common Ground Used

| ID | Tier | Statement | Source | Why It Matters |
|---|---|---|---|---|
| CG-01 | ESTABLISHED | SDC keeps a small public command surface and routes specialist behavior internally. | README.md, expert-routing.md | Prevents command sprawl |
| CG-02 | ESTABLISHED | Discovery Open must not generate final spec/design/tasks. | workflow-standards.md | Keeps output contract from creating speculative docs |
| CG-03 | ESTABLISHED | Final validation must block unconfirmed execution inputs. | sdc-cli.py | Output contracts must not bypass confirmation gates |

## 1.3 Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | N/A | No product workflow/state behavior changed by SDC itself | design.md#process-state-diagrams | N/A because this change updates workflow governance, not a user business workflow |
| Sequence / Integration Diagram | N/A | No multi-service/runtime integration | design.md#sequence-integration-diagrams | N/A because SDC remains prompt/CLI-only |
| API / Contract Specification | N/A | No public API endpoint/event contract | design.md#api-contract-specification | N/A because this change updates CLI validation and prompt contracts only |
| Data Model / Migration Contract | N/A | No database/schema migration | design.md#data-model-migration-contract | N/A because SDC has no persistence schema |
| UX Flow / Interaction States | N/A | No frontend/UI surface | design.md#ux-flow-interaction-states | N/A because SDC has CLI/skill docs only |
| Test Matrix | Required | Every final change needs AC validation | design.md#test-matrix | AC-01 through AC-04 must map to validation evidence |
| Deploy / Release Checklist | N/A | No runtime deploy; package/release checks only | design.md#deploy-release-checklist | N/A because verification is audit/eval/package syntax, not service deployment |
| AI Involvement Note | Required | AI-assisted product/workflow change | design.md#ai-involvement-note | Archive/check should preserve AI involvement note |

## 2. Decision Ledger / 决策台账

| ID | 决策 | 状态 | 依据来源 | 是否允许进入 REQ/AC | 下一步 |
|---|---|---|---|---|---|
| DEC-01 | Keep public commands unchanged and implement output standards internally | Confirmed | User confirmed recommended方案 | Yes | Update references, prompts, validators |
| DEC-02 | Add shared English `artifact-output-contracts.md` | Confirmed | User prefers model-readable reference standards | Yes | Add reference and load rules |
| DEC-03 | Require Test Matrix for final plan/check | Confirmed | Acceptance validation is always needed | Yes | Enforce in templates and CLI |
| DEC-04 | Optional outputs may be N/A only with evidence reason | Confirmed | Avoids heavy docs for small changes | Yes | Enforce in CLI |

## 3. Glossary / 统一语言

- Artifact Output Contract: A stage-level table that records which standard deliverables are required, produced, or N/A.
- Triggered output: A diagram, contract, matrix, checklist, or note required because the requirement or diff touches a risk area.
- Test Matrix: A required final validation table mapping ACs to tests or manual checks.

## 4. 背景与目标

The internal AI development workflow uses explicit stage deliverables. SDC should borrow that clarity while keeping its simplified command model. The goal is to make input/output standards validate-able inside existing SDC stages.

## 5. Business Invariants / 业务不变量

### INV-01

SDC must keep the public workflow small: init, change, plan, apply, check, archive, harness.

### INV-02

Output contracts must not override confirmation gates. Unconfirmed product rules, architecture choices, data models, rollout policy, permissions, or integrations remain blockers.

### INV-03

Final plan/check must include a Test Matrix with AC validation coverage.

## 6. 场景与需求

### SCN-01

A user starts a new SDC change and wants enterprise-style deliverable standards.

### REQ-01

SDC must define a shared Artifact Output Contract reference that describes stage inputs, triggered outputs, N/A rules, and check behavior.

### SCN-02

A confirmed change enters planning.

### REQ-02

SDC plan/check/validate must require triggered output artifacts in design/context-pack or explicit `N/A + evidence reason`.

### SCN-03

A change mentions an API endpoint, data model, workflow, UI, deployment, or test risk.

### REQ-03

SDC validation must block final readiness when the corresponding triggered output artifact is missing.

### SCN-04

Future releases risk dropping the output contract from templates or evals.

### REQ-04

SDC audit and evals must verify that Artifact Output Contract references, templates, and enforcement scenarios remain present.

## 7. Acceptance Criteria / 验收标准

### AC-01

Given the SDC shared references
When a model plans or checks a change
Then `artifact-output-contracts.md` defines required stage inputs, triggered outputs, N/A rules, and check behavior.

### AC-02

Given a managed SDC template for spec, design, or context-pack
When it is initialized or safely upgraded
Then it includes Artifact Output Contract coverage and design includes a Test Matrix section.

### AC-03

Given a confirmed change whose spec mentions a `POST /rooms/bookings API endpoint`
When design omits the `API / Contract Specification` output row
Then `sdc validate <change>` fails with a triggered artifact output error.

### AC-04

Given the upgraded project
When release checks run
Then `npm run audit` and `npm run eval:sdc` pass.

## 8. 验证策略

- Run Python syntax checks for `sdc-cli.py` and eval provider.
- Run Node syntax checks for installer and audit script.
- Run `npm run audit`.
- Run `npm run eval:sdc`.
- Run `sdc validate 2026-06-15-artifact-output-contracts`.

## 9. 风险、假设与待确认项

No blocking open questions remain. The main risk is over-heavy artifacts; the N/A evidence rule mitigates it.

## 10. 追溯关系矩阵

| SCN | REQ | AC | Task |
|---|---|---|---|
| SCN-01 | REQ-01 | AC-01 | T001 |
| SCN-02 | REQ-02 | AC-02 | T002 |
| SCN-03 | REQ-03 | AC-03 | T003 |
| SCN-04 | REQ-04 | AC-04 | T004, T900 |
