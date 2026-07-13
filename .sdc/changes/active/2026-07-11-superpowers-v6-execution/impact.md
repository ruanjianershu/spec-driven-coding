# Change Impact

## Analysis Snapshot

- Repository: spec-driven-coding
- Change: 2026-07-11-superpowers-v6-execution
- Branch: codex/superpowers-v6-execution
- Evidence limits: local source, official Superpowers release notes, deterministic CLI/eval/package verification; no npm publication in this change.

## Entry Points And Call Chain

- Public prompts: `commands/plan.md`, `commands/apply.md`, `commands/check.md`.
- Shared governance: `sdc-references/*`.
- Advanced direct skills: implement, review, validate, test, quality.
- Workspace generation and validation: `sdc-cli.py`.
- File handoffs: `scripts/sdc-task-brief.py`, `scripts/sdc-review-package.py`.
- Codex install/package path: `.codex-plugin`, `.agents/plugins`, `bin/install.js`, rootless package script.
- Release protection: audit and evals.

## Direct Changes Required

| File / Contract | Reason | Evidence | Related REQ/AC |
|---|---|---|---|
| execution-orchestration reference | Define internal execution contract | Superpowers v6 comparison | REQ-01-REQ-03 / AC-01-AC-04 |
| plan/apply/check and role contracts | Route contract through existing commands | public surface invariant | REQ-01-REQ-03 |
| CLI templates and validators | Make rules enforceable and migratable | existing SDC thin runtime | REQ-01, REQ-03, REQ-05 |
| task/review helper scripts | Provide file-based handoffs | context-cost requirement | REQ-02 / AC-03 |
| Codex metadata/source skills/package script | Align repo marketplace and rootless portal behavior | v6.1 Codex changes | REQ-04 / AC-06 |
| eval/audit/docs/version | Prevent drift and explain behavior | release discipline | REQ-06 / AC-05-AC-06 |

## Cascading Impact

- New final plans are stricter and old generated templates require safe migration.
- Completed tasks now require approved review/evidence before check/archive.
- Runtime scratch is ignored; durable evidence remains in existing change artifacts.
- WORKTREE review packages refuse untracked files rather than omitting them.
- Managed-file fingerprints preserve user changes; only unchanged/known stock templates auto-upgrade.
- Codex local plugin roots are transactionally replaced with rollback/recovery so removed skill directories cannot survive updates.
- Public command names and Claude command/skill separation remain unchanged.

## Contracts / Data / Config / Permissions / Security / Observability

- Public commands: unchanged.
- Skill discovery: public workflow skills are committed for Codex; shared contracts move from `skills/sdc-shared/` to root `sdc-references/`.
- CLI bin names: unchanged.
- Persistent data/schema: N/A, no database or domain data change.
- Config: additive `.sdc/.gitignore` migration, managed ownership fingerprints, plugin manifests, package scripts.
- Permissions/security: reviewer becomes explicitly read-only; package contains no hook execution.
- Observability: progress ledger and review evidence improve execution visibility.

## Tests And Regression Strategy

- Python and Node syntax checks.
- `npm run audit`.
- `npm run eval:sdc` with plan consistency, dual-review evidence, ledger, handoff, migration-preservation, stale-install, and package scenarios.
- Repeated `python3 sdc-cli.py init` for idempotency.
- `python3 sdc-cli.py check 2026-07-11-superpowers-v6-execution`.
- Codex portal package generation and archive inspection.
- `npm pack --dry-run`.

## Implementation Order And Rollback Boundary

1. Add execution reference and workflow routing.
2. Upgrade templates, validators, and file-handoff helpers.
3. Add Codex metadata and package tooling.
4. Add eval/audit/docs/version migration.
5. Run complete validation and repair discovered drift.

Rollback can remove the new reference, helper scripts, new schema fields, marketplace metadata, and evals while retaining existing SDC 1.2 governance.

## Open Questions

| Question | Why It Matters | Blocking? |
|---|---|---|

## Evidence Index

| Claim | Source |
|---|---|
| Public command set unchanged | commands directory and release audit |
| Task fields and review gates are enforced | sdc-cli.py and evals |
| Runtime handoffs are ignored without replacing team rules | `.sdc/.gitignore` migration and eval |
| Codex package is rootless, minimal, and includes generated public skills | package script verification |
