# SDC Expert Routing

Expert Routing gives SDC the benefits of a large expert skill library without adding public commands. Users choose the workflow stage; SDC internally selects the smallest relevant expert lenses and reference files.

## Principle

Do not ask users to choose between dozens of expert commands.

Use the public workflow:

```text
init -> change -> plan -> apply -> check -> archive
```

Then route internally:

```text
workflow stage + project evidence + change scope -> expert profiles -> relevant standards/knowledge/references
```

## Public Surface Rule

- Do not add public slash commands for every expert.
- Do not expose technology-specific command sprawl.
- Expert profiles are internal lenses that guide reading, questioning, planning, review, and testing.
- Profiles do not imply separate agents, mandatory full-repository reads, or repeated review/test loops. Use `workflow-standards.md` when risk classification or context breadth is unclear.
- The agent must disclose which expert profiles were used in `context-pack.md`, review/check reports, or archive summaries when those profiles materially affected decisions.

## Expert Profile Registry

Use these generic profiles first. Projects may extend them in `.sdc/expert-routing.md`.

| Profile | When To Use | Primary Reads | Output Bias |
| --- | --- | --- | --- |
| product-discovery | Requirement is vague, user value is unclear, scope is broad, or acceptance is missing. | `common-ground.md`, `knowledge/product/*`, discovery artifacts. | Questions, MVP slicing, non-goals, acceptance clarity. |
| domain-modeling | Domain terms, roles, state transitions, business invariants, permissions, or approval flows matter. | `knowledge/product/domain.md`, `roles.md`, `rules.md`, specs, decisions. | Glossary, invariants, state/permission clarity. |
| legacy-modernizer | Brownfield/Legacy or Unknown projects, migrations, compatibility, risky refactors. | `project-cognition.md`, `impact.md`, code evidence, technical knowledge. | Impact radius, regression risk, rollback boundary. |
| architecture | Module boundaries, dependency direction, cross-cutting design, scalability, maintainability. | `knowledge/technical/architecture.md`, `modules.md`, standards. | Minimal architecture decision, tradeoff, boundary protection. |
| api-contract | Public APIs, integration contracts, events, request/response shape, compatibility. | `knowledge/technical/data-and-interfaces.md`, specs, tests, API code. | Contract stability, backward compatibility, validation. |
| data | Data model, schema, migration, transaction, locking, consistency, reporting. | `knowledge/technical/data-and-interfaces.md`, DB scripts, standards. | Data integrity, migration/rollback, edge cases. |
| backend | Services, jobs, queues, domain services, integrations, server-side behavior. | stack/modules/architecture knowledge and relevant standards. | Service boundaries, error handling, observability. |
| frontend | UI flows, state, forms, accessibility, visual regression, frontend architecture. | product flows, frontend modules, design/testing standards. | User journey, interaction states, accessibility. |
| test-strategy | Acceptance coverage, regression risk, flaky areas, missing test commands. | `knowledge/technical/testing.md`, tasks, tests, CI evidence. | Test-first tasks, AC coverage, fallback validation. |
| security | Auth, permissions, secrets, input/output safety, compliance, destructive operations. | security standards, roles, APIs, config, dependency evidence. | Threat-focused questions and blockers. |
| operations | Deployment, config, observability, rollback, runtime behavior, performance baseline. | operations knowledge, scripts, CI/CD, logs, config. | Release readiness, rollback, diagnostics. |
| documentation | Public docs, README, onboarding, developer handoff, changelog. | project docs, specs, archive evidence. | Concise, durable docs with traceability. |
| research | External or prior evidence is needed before change, plan, apply, check, or archive. | public sources, local knowledge, `.sdc/runtime/<change-id>/research/`, citations, `knowledge-candidates.md`. | Scratch evidence stays runtime-local; durable findings remain Candidate until archive confirmation. |

## Routing File Shape

`.sdc/expert-routing.md` should use this shape:

```markdown
# Expert Routing

## Project Profile
- Primary domain:
- Project type: Greenfield / Brownfield / Legacy / Unknown
- Main stack evidence:
- Critical risk areas:

## Default Profiles
| Profile | Status | Trigger | Required Reads | Notes |
| --- | --- | --- | --- | --- |

## Stack-Specific Profiles
| Profile | Applies When | Required Reads | Standards / References |
| --- | --- | --- | --- |

## Routing Decisions
| Date | Change / Scope | Profiles Used | Why | Evidence |
| --- | --- | --- | --- | --- |
```

## Stage Routing

### init

- Create `expert-routing.md`.
- Identify project type and stack evidence.
- Seed default profiles as `Candidate`, not confirmed truth.
- For Brownfield/Legacy, enable `legacy-modernizer`, `architecture`, `test-strategy`, and `operations` as likely profiles until evidence says otherwise.

### change

- Use `product-discovery` for every new requirement.
- Add `domain-modeling` when roles, permissions, states, business rules, or approval flows appear.
- Do not use expert profiles to invent product rules. They can only generate questions and options before confirmation.

### plan

- Select the smallest relevant profile set with no numeric quota; one lens may suffice for a narrow change.
- Read required knowledge/standards for those profiles.
- Write the selected profiles into `context-pack.md`.
- If no profile fits, state `Profiles Used: baseline-sdc` and continue with core SDC rules.

### apply

- Follow `context-pack.md` profile selections.
- Do not add a new expert profile mid-implementation if it changes scope; stop and update plan/context-pack first.

### check

- Validate that selected expert profiles match the actual diff and risk.
- Add missing profile findings when the implementation touched a risk area not covered by the plan.
- Validate research routing when research influenced the change: scratch in runtime, citations in discovery/notes, durable findings in `knowledge-candidates.md`.

### archive

- Record profiles that were useful and whether `.sdc/expert-routing.md`, standards, or knowledge should be updated.
- Updating routing rules is a conditional durable update requiring human confirmation.
- Evaluate research candidates without promoting them automatically.

## Anti-Guess Rules

- Expert profiles may suggest questions, checks, and investigation tasks.
- Investigations remain within confirmed scope; unknown business requirements belong in discovery, not spec/design/tasks. Personal/native/project memory and research results are Candidate until verified and confirmed.
- Expert profiles may not create unconfirmed product facts, architecture choices, data models, permissions, or rollout policies.
- A profile recommendation that affects scope, data, security, public contracts, or compatibility must enter the Decision Ledger as `Proposed` until confirmed.
- Imported company/team standards outrank generic expert guidance when they are relevant and do not conflict with confirmed project facts.

## Minimal Output Contract

When expert routing materially affects a plan, context pack, check, or archive, include:

```markdown
## Expert Profiles Used
| Profile | Why Used | Sources Read | Decisions / Checks Affected |
| --- | --- | --- | --- |
```
