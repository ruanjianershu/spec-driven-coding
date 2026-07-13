# Design

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| spec.md | Confirmed | REQ-01 through REQ-06 | Defines required behavior |
| impact.md | Confirmed | source and package call chain | Bounds Brownfield impact |
| existing SDC templates/evals | Confirmed | repository evidence | Preserves compatibility |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## Common Ground Used

| ID | Tier | Statement | Source | Why It Matters |
|---|---|---|---|---|
| CG-01 | ESTABLISHED | Public commands remain small | spec.md#INV-01 | Routes changes internally |
| CG-02 | ESTABLISHED | Runtime scratch is non-authoritative | spec.md#INV-02 | Keeps durable evidence explicit |

## Global Constraints

| ID | Constraint | Source | Applies To |
|---|---|---|---|
| GC-01 | Do not add or rename public commands | spec.md#INV-01 | commands, installer, README, audit |
| GC-02 | Runtime scratch must be git-ignored and never the only evidence | spec.md#INV-02 | helpers, CLI, docs |
| GC-03 | User-authored change files are not silently rewritten | impact.md | init migration |
| GC-04 | Reviewer is read-only and cannot be coached to suppress findings | spec.md#REQ-03 | apply, review, check |
| GC-05 | Do not dispatch multiple implementation tasks in parallel | discovery.md#DEC-05 | all clients |

## Plan Preflight

- Status: Passed
- Reviewed Against: spec.md, impact.md, design.md, tasks.md, standards, Artifact Output Contract
- Findings: No blocking findings; public commands are unchanged, tasks own one test/review boundary, and interfaces are defined.

## Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | N/A | No product workflow/state change | design.md#process-state-diagrams | N/A because this is an engineering execution contract |
| Sequence / Integration Diagram | N/A | No service integration | design.md#sequence-integration-diagrams | N/A because helpers are local and synchronous |
| API / Contract Specification | N/A | No public API change | design.md#api-contract-specification | N/A because commands and bin names stay unchanged |
| Data Model / Migration Contract | N/A | No persistent schema | design.md#data-model-migration-contract | N/A because runtime artifacts are markdown scratch |
| UX Flow / Interaction States | N/A | No graphical UI | design.md#ux-flow-interaction-states | N/A because existing command/skill UX remains |
| Test Matrix | Required | AC-01 through AC-06 | design.md#test-matrix | Deterministic evidence listed below |
| Deploy / Release Checklist | Required | Version and package changes | design.md#deploy-release-checklist | Package and metadata must be verified |
| AI Involvement Note | Required | Agent execution/review behavior | design.md#ai-involvement-note | Human review boundaries documented below |

## Solution Summary / 方案摘要

Add one shared execution reference and route it through existing SDC stages. Extend managed templates and validators, add focused file-handoff helpers, gate completed delivery on task/final reviews, and harden Codex marketplace packaging.

## Impact Scope / 影响范围

Plan/apply/check prompts, advanced skills, shared references, CLI templates/validation, evals, release audit, Codex metadata, package tooling, README/CHANGELOG, and the project `.sdc` workspace.

## Non-Scope / 不改范围

No public command, background service, remote dependency, brainstorm UI, required worktree, or required per-task commit.

## Key Tradeoffs / 关键取舍

- Runtime handoffs reduce context cost but require durable evidence promotion.
- Strict task interfaces increase plan effort but remove downstream guessing.
- Subagent execution improves isolation where supported; inline fallback preserves portability.

## Data, API, State, or Interaction Changes / 数据、接口、状态或交互变化

Internal markdown schemas and local plugin metadata change. Public commands, bin names, and user-facing stage sequence remain stable.

## Process / State Diagrams

N/A because there is no product workflow or state-machine change.

## Sequence / Integration Diagrams

N/A because no external or multi-service integration is introduced.

## API / Contract Specification

N/A because the public command and package bin contracts are unchanged.

## Data Model / Migration Contract

N/A because no persistent model or migration is introduced.

## UX Flow / Interaction States

N/A because existing command and skill entry points remain unchanged.

## Test Matrix

| AC | Scenario | Level | Verification | Expected Result | Status |
|---|---|---|---|---|---|
| AC-01 | missing/empty task interface, empty/conflicting constraints, incomplete preflight | CLI eval | `npm run eval:sdc` | validation blocks each incomplete plan shape | Passed |
| AC-02 | missing aggregate/dual verdict or unresolved evidence reference | CLI eval | `npm run eval:sdc` | check blocks delivery | Passed |
| AC-03 | task brief/review package and untracked WORKTREE | helper eval | `npm run eval:sdc` | handoffs created for tracked diff; untracked omission blocked | Passed |
| AC-04 | durable delivery evidence with optional recovery ledger | SDC self-check/eval | check with consistent, conflicting, and missing runtime ledger | approved reviews/final review required; present ledger must agree; missing ignored ledger warns | Passed |
| AC-05 | fingerprinted user modification, exact legacy template, custom ignore, repeated init | migration eval | `npm run eval:sdc` and run init twice | modified file preserved; known stock file upgraded; second run changes nothing | Passed |
| AC-06 | stale install, source marketplace, rootless deterministic release package | release/package eval | sync skills, audit, install fixture, validate skill layout, build twice, npm dry-run | stale layout removed, complete valid skills, required runtime files only, matching digests | Passed |

## Deploy / Release Checklist

- [x] Version sources set to 1.3.0.
- [x] Codex marketplace manifest added.
- [x] Codex hooks explicitly empty and category is Developer Tools.
- [x] Installer packages scripts and marketplace metadata.
- [x] Rootless minimal deterministic Codex archive and checksum tooling added.
- [x] Public Codex workflow skills are generated into source; shared contracts moved to `sdc-references/` outside skill discovery.
- [x] npm and Codex package paths exclude generated Python caches.
- [x] Existing `.sdc/.gitignore` migration preserves custom rules.
- [x] Managed workspace files carry ownership fingerprints and preserve modified project rules.
- [x] Codex local plugin replacement removes stale pre-1.3 directories transactionally with rollback and interrupted-swap recovery.
- [x] Release audit and eval coverage added.
- [x] README and changelog updated.

## AI Involvement Note

- AI generated the implementation and change artifacts under user-confirmed scope.
- Human review should focus on task-schema strictness, runtime durability boundary, reviewer independence, and Codex package layout.
- Deterministic tests and self-check evidence are recorded in notes.md.
- No package was published and no remote branch was pushed in this change.

## Brownfield Impact Summary / 遗留影响摘要

Existing generated workspaces safely migrate on init; active user-authored change artifacts receive validation guidance rather than automatic rewrites. Existing public command behavior remains compatible.

## REQ/AC to Design Decision Mapping / 追溯映射

| REQ / AC | Design Decision |
|---|---|
| REQ-01 / AC-01 | task schema and preflight validators |
| REQ-02 / AC-03 | runtime helper scripts and ignored ledger |
| REQ-03 / AC-02, AC-04 | dual-verdict and final-review delivery gate |
| REQ-04 / AC-06 | Codex manifests and rootless deterministic package script |
| REQ-05 / AC-05 | stale-template/runtime-ignore migration and idempotency repair |
| REQ-06 / AC-06 | release audit and 51-scenario eval suite |

## Risks, Rollback, and Migration / 风险、回滚和迁移

Stricter plan validation can block legacy active changes. Generated templates are safely upgraded with backup; manual changes remain user-owned. Rollback removes the new schema and helpers without changing archived specs.

## Alternatives / 替代方案

Copying all Superpowers skills was rejected because it would duplicate SDC governance and expand the command surface.
