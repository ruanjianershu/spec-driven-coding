# Context Pack

## Goal

Deliver SDC 1.3 execution orchestration without increasing the public command surface.

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| spec.md | Confirmed | REQ-01 through REQ-06 | Governs implementation |
| impact.md | Confirmed | source and package call chain | Bounds compatibility |
| design.md | Confirmed | Plan Preflight Passed | Defines execution structure |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## Common Ground Used

| ID | Tier | Statement | Source | Why It Matters |
|---|---|---|---|---|
| CG-01 | ESTABLISHED | Public commands remain small | spec.md#INV-01 | Prevents command sprawl |
| CG-02 | ESTABLISHED | Runtime scratch is non-authoritative | spec.md#INV-02 | Preserves durable evidence |

## Expert Profiles Used

| Profile | Why Used | Sources Read | Decisions / Checks Affected |
|---|---|---|---|
| architecture | Cross-client execution boundaries | design, installer | shared contract and fallback |
| test-strategy | Enforcement and eval design | CLI, evals | negative and helper scenarios |
| security | Read-only review and no hooks | release notes, manifests | reviewer and Codex metadata |
| documentation | Keep public UX concise | README, commands | no new commands |

## Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | N/A | No product workflow/state change | design.md#process-state-diagrams | N/A because this is engineering execution governance |
| Sequence / Integration Diagram | N/A | No service integration | design.md#sequence-integration-diagrams | N/A because helpers are local scripts |
| API / Contract Specification | N/A | No public API change | design.md#api-contract-specification | N/A because public commands and bin names stay unchanged |
| Data Model / Migration Contract | N/A | No persistent schema | design.md#data-model-migration-contract | N/A because runtime is markdown scratch |
| UX Flow / Interaction States | N/A | No graphical UI | design.md#ux-flow-interaction-states | N/A because command/skill UX remains |
| Test Matrix | Required | AC-01 through AC-06 | design.md#test-matrix | deterministic evidence exists |
| Deploy / Release Checklist | Required | package and metadata change | design.md#deploy-release-checklist | release checklist completed |
| AI Involvement Note | Required | agent behavior changes | design.md#ai-involvement-note | boundaries documented |

## Global Constraints

| ID | Constraint | Source | Applies To |
|---|---|---|---|
| GC-01 | Do not add or rename public commands | spec.md#INV-01 | all tasks |
| GC-02 | Runtime scratch must be git-ignored and never the only evidence | spec.md#INV-02 | execution/helpers |
| GC-03 | User-authored change files are not silently rewritten | impact.md | CLI init |
| GC-04 | Reviewer is read-only and cannot be coached to suppress findings | spec.md#REQ-03 | review/check |
| GC-05 | Do not dispatch multiple implementation tasks in parallel | discovery.md#DEC-05 | all clients |

## Execution Orchestration

- Plan Preflight: Passed
- Mode: Inline implementation with separate skeptical review; subagent path documented for capable clients
- Runtime Workspace: .sdc/runtime/2026-07-11-superpowers-v6-execution/
- Task Review: Spec Compliance + Code Quality
- Final Whole-Change Review: Required

## Confirmed Product Knowledge

SDC remains a small-command spec-driven workflow; execution orchestration is internal.

## Confirmed Technical Knowledge

Generated public workflow skills are created by the installer; source advanced skills remain separate to avoid Claude command duplication.

## Execution Boundaries

Change prompts, references, templates, validators, helpers, evals, metadata, package tooling, and docs only. Do not publish packages or push remotes.

## Forbidden Assumptions

- Do not assume every client supports subagents or model selection.
- Do not treat runtime scratch as durable evidence.
- Do not add public commands or reintroduce Claude command/skill duplicates.
- Do not silently rewrite user-authored active changes.

## Task And Traceability Summary

T001-T004 implement REQ-01 through REQ-06; T900 proves AC-01 through AC-06.

## Validation Commands

- `python3 -m py_compile sdc-cli.py scripts/*.py evals/sdc-flow/*.py`
- `node --check scripts/audit-release.mjs`
- `npm run audit`
- `npm run eval:sdc`
- `python3 scripts/package-codex-plugin.py --allow-dirty --output /tmp/sdc-codex-plugin-1.3.0.zip`
- `npm pack --dry-run`
- `python3 sdc-cli.py check 2026-07-11-superpowers-v6-execution`

## Knowledge Candidate Routing

- Product knowledge candidates: execution orchestration stays internal to existing commands.
- Technical knowledge candidates: file-based handoff and dual-verdict review contract.
- Memory/procedure candidates: use runtime ledger to recover after context compaction.
