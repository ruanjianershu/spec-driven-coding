# Expert Routing

> 专家路由层。用户仍然只使用 init/change/plan/apply/check/archive；SDC 内部根据任务选择相关专家视角和参考资料。

## Project Profile

- Primary domain:
- Project type: Greenfield / Brownfield / Legacy / Unknown
- Main stack evidence:
- Critical risk areas:

## Default Profiles

| Profile | Status | Trigger | Required Reads | Notes |
|---------|--------|---------|----------------|-------|
| product-discovery | Candidate | New or unclear requirement | common-ground.md, knowledge/product/*, discovery.md | Questions, MVP, non-goals, acceptance clarity |
| domain-modeling | Candidate | Roles, permissions, states, business rules | product/domain.md, roles.md, rules.md | Glossary, invariants, state and permission clarity |
| legacy-modernizer | Candidate | Brownfield/Legacy/Unknown project | project-cognition.md, impact.md, code evidence | Impact radius, regression risk, rollback |
| architecture | Candidate | Module boundaries or cross-cutting design | technical/architecture.md, modules.md, standards | Boundaries, tradeoffs, maintainability |
| api-contract | Candidate | Public API, integration, event, contract | technical/data-and-interfaces.md, specs, tests | Compatibility and validation |
| data | Candidate | Schema, transaction, migration, consistency | technical/data-and-interfaces.md, DB scripts, standards | Data integrity, rollback |
| backend | Candidate | Services, jobs, integrations | technical stack/modules, standards | Service boundaries, error handling |
| frontend | Candidate | UI flow, state, forms, accessibility | product flows, frontend modules, testing standards | User journey and interaction states |
| test-strategy | Candidate | Acceptance coverage or regression risk | technical/testing.md, tasks, tests, CI | Test-first tasks and AC coverage |
| security | Candidate | Auth, permissions, secrets, destructive ops | security standards, roles, APIs, config | Threat-focused blockers |
| operations | Candidate | Deployment, config, observability, runtime | technical/operations.md, scripts, CI/CD | Release readiness and rollback |
| documentation | Candidate | Docs, README, handoff, changelog | specs, archive evidence, project docs | Durable concise documentation |

## Stack-Specific Profiles

| Profile | Applies When | Required Reads | Standards / References |
|---------|--------------|----------------|------------------------|

## Routing Decisions

| Date | Change / Scope | Profiles Used | Why | Evidence |
|------|----------------|---------------|-----|----------|

## Rules

- Expert profiles can suggest questions, checks, and investigation tasks.
- Expert profiles cannot create unconfirmed product facts, architecture choices, data models, permissions, or rollout policy.
- If a profile recommendation affects scope, data, security, public contracts, or compatibility, put it in the Decision Ledger as Proposed until confirmed.
