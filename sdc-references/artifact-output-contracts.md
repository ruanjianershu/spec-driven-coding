# SDC Artifact Output Contracts

This reference defines stage-level input and output contracts for SDC. It turns enterprise delivery expectations into explicit artifacts without adding public commands.

## Principle

SDC keeps the public workflow small:

```text
init -> change -> plan -> apply -> check -> archive
```

Each stage still has a strict artifact contract:

```text
stage inputs + risk triggers -> required outputs -> validation evidence
```

Do not create large documents while Discovery Gate is open. Output contracts become final only after intake, MVP scope, acceptance direction, and high-impact decisions are confirmed or explicitly deferred.

Apply `workflow-standards.md` when selecting risk level or evidence breadth. Outputs follow actual triggers at every level; light work may use concise sections and shared evidence, never weaker acceptance or invented requirements.

## Stage Contracts

| Stage | Required Inputs | Required Outputs |
| --- | --- | --- |
| change | User request, source PRD/notes if provided, `.sdc/common-ground.md`, `.sdc/knowledge/index.md`, `.sdc/expert-routing.md` | Input evidence summary, functional decomposition, business rules, scenarios, open questions, Decision Ledger, proposed output artifact contract |
| spec | Closed discovery, established Common Ground, confirmed knowledge, Decision Ledger | Spec with SCN/REQ/AC, invariants, validation strategy, traceability, and accepted output artifact contract; no speculative spec while business requirements remain unknown |
| plan | Confirmed spec, impact when required, relevant knowledge and standards, expert routing | Detailed technical design, required diagrams/checklists/contracts, tasks, context-pack, validation strategy |
| apply | Context-pack, tasks, design, relevant standards and knowledge | Code changes, task evidence, notes, validation output, knowledge candidates |
| check | Final artifacts, actual diff, tests/build/manual evidence | Validate/review/test/quality report, AC coverage, missing artifact findings, deploy/release readiness, knowledge compact recommendations |
| archive | Completed checked change, final spec, evidence, knowledge candidates | Stable spec, archived change history, archive evidence, Knowledge Compact Gate decisions |

## Triggered Output Artifacts

Use this table when creating `discovery.md`, `spec.md`, `design.md`, `context-pack.md`, and check reports.

| Trigger Signal | Required Output | Minimum Shape | Can Be N/A? |
| --- | --- | --- | --- |
| Business workflow, approval, status transition, user journey, or state machine | Process / State Diagram | Mermaid `flowchart`, `sequenceDiagram`, or `stateDiagram`; include actors and failure branches | Yes, with reason and evidence |
| Multi-service call, async job, event, webhook, queue, external integration, or non-trivial interaction order | Sequence / Integration Diagram | Mermaid `sequenceDiagram` or integration flow with producer/consumer and error paths | Yes, with reason and evidence |
| Public API, internal API, event contract, request/response, permission boundary, or compatibility rule | API / Contract Specification | Endpoint/event name, method/type, request, response, errors, auth/permission, compatibility | Yes, with reason and evidence |
| Data model, schema, table, migration, DDL, consistency, locking, transaction, or rollback data concern | Data Model / Migration Contract | Entities/tables, fields, indexes, migration/rollback, transaction and consistency boundary | Yes, with reason and evidence |
| UI, form, workflow screen, user-facing error, accessibility, or visual state | UX Flow / Interaction States | Main path, empty/loading/error states, validation, accessibility and smoke path | Yes, with reason and evidence |
| Test strategy, risk, boundary, error, security, compatibility, or regression concern | Test Matrix | AC, scenario, level, command/manual check, expected result, owner/status | No for final plan/check |
| Deployment, config, feature flag, Nacos/env, MQ/topic, cron/job, observability, rollback, or release readiness | Deploy / Release Checklist | Config, data, jobs/events, monitoring, rollback, smoke verification, owner/status | Yes, only when no release/runtime impact |
| AI-generated code, AI-assisted review, or PR preparation | AI Involvement Note | What AI generated, what human must review, tests run, known limitations | Yes, for non-code documentation-only changes |

## Artifact Contract Section

Final `spec.md`, `design.md`, and `context-pack.md` should include an Artifact Output Contract section.

Minimum table:

```markdown
## Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
| --- | --- | --- | --- | --- |
| Process / State Diagram | Required / N/A | workflow/state/... | design.md#... | ... |
| Sequence / Integration Diagram | Required / N/A | integration/async/... | design.md#... | ... |
| API / Contract Specification | Required / N/A | API/event/... | design.md#... | ... |
| Data Model / Migration Contract | Required / N/A | data/schema/... | design.md#... | ... |
| UX Flow / Interaction States | Required / N/A | UI/user-flow/... | design.md#... | ... |
| Test Matrix | Required | acceptance/regression | design.md#... or tasks.md | ... |
| Deploy / Release Checklist | Required / N/A | deploy/config/runtime | design.md#... or check report | ... |
| AI Involvement Note | Required / N/A | AI-assisted delivery | check/archive/PR summary | ... |
```

Rules:

- `Required` outputs must point to a concrete section or file.
- `N/A` outputs must include a short evidence-based reason.
- `Test Matrix` is required for final plan/check because every change needs acceptance validation.
- Do not use an output contract to invent product rules, APIs, schemas, rollout policy, or permissions. Unconfirmed items remain `Proposed`, `Assumed`, `TBD`, or `Conflict` and block final execution.
- For Brownfield/Legacy work, the contract must align with `impact.md`; missing impact areas block plan/apply/check.

## Change Intake Use

During `sdc-change`, collect only enough information to decide which outputs are likely required.

Cover within the four intake categories using cited current/prior confirmation; ask only missing blocking questions:

- Input sources: PRD link, meeting notes, issue, logs, screenshots, code evidence, or direct user request.
- Product output triggers: workflow, roles, permission, approval, state, user journey, business rules.
- Technical output triggers: API, data, integration, async/job, UI, deployment, config, migration, security, rollback.
- Acceptance output triggers: tests, manual verification, deploy checklist, AI involvement note.

Unconfirmed output requirements remain `Proposed`; reuse still-valid confirmed scope and applicable project standards without asking again. While Discovery Gate is open, keep the output contract as a draft in `discovery.md` or `proposal.md`.

## Plan Use

During `sdc-plan`, turn the confirmed artifact contract into concrete sections:

- Add diagrams only when triggered; use Mermaid unless a project standard says otherwise.
- Add API/data/deploy/test contracts when triggered.
- Include production/validation of triggered outputs in the coherent task that needs them; split only when independently verifiable. Do not add artificial artifact-only tasks to a tiny change.
- Put the final contract summary in `context-pack.md` so implementation agents know what must remain true.

## Check Use

During `sdc-check` and `sdc-validate`, block delivery when:

- A triggered output is missing.
- A required output is listed as `N/A` without an evidence-based reason.
- A diagram, contract, matrix, or checklist contradicts spec, impact, tasks, code, or tests.
- Actual diff introduces API/data/deploy/security/UX impact that was not captured in the artifact contract.
- Test Matrix does not map back to ACs.

## Minimalism

The output contract is not permission to produce bulky documents for every change.

Use the smallest sufficient artifact:

- Simple wording-only documentation change: output contract table + Test Matrix may be enough.
- CRUD or API change: API contract, data contract, test matrix, and release checklist are usually required.
- Workflow or approval change: process/state diagram and test matrix are usually required.
- Brownfield risky change: impact-aligned diagrams/checklists are required where the current change touches those risks.
