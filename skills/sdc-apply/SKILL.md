---
name: sdc-apply
description: "Use when an approved SDC plan is ready for implementation and evidence capture."
---

> Codex/Hermes workflow skill generated from `commands/apply.md`.
> Treat the user's current request as `$ARGUMENTS`. In Codex/Hermes, route to the matching SDC skill/workflow instead of expecting `/sdc:*` slash-command support.

# SDC Apply

Use "$ARGUMENTS" to identify the target change or task. Implement the planned work, keep notes/tasks updated, and preserve verification evidence.

Run the SDC apply workflow:

- Read `.sdc/constitution.md`, `.sdc/common-ground.md`, `.sdc/expert-routing.md`, `.sdc/knowledge/index.md`, relevant product/technical knowledge, the active change `spec.md`, `design.md`, `tasks.md`, `context-pack.md`, and `notes.md` before editing.
- Stop if final artifacts contain open Knowledge Gaps or `Assumed` / `Proposed` / `TBD` / `Conflict` / `Stale` execution inputs.
- Stop if final artifacts depend on OPEN or high-impact WORKING Common Ground.
- Follow the Expert Profiles Used in `context-pack.md`; if implementation discovers a new high-risk profile, stop and update plan/context-pack first.
- Follow the Artifact Output Contract in `context-pack.md`; if implementation discovers new API, data, workflow, UX, deployment, test, or AI involvement output requirements, stop and update plan/context-pack first.
- Read `../../sdc-references/execution-orchestration.md` when available and stop unless Plan Preflight is `Passed`.
- Resume from `.sdc/runtime/<change-id>/progress.md` when it exists; reconcile it with tasks and git evidence instead of re-running completed tasks after context loss.
- Execute tasks serially in dependency order using one task brief at a time. Use one fresh implementer context for the current task when the client supports subagents; do not start another implementation task until review, durable evidence, and ledger update finish. Otherwise preserve the same implement-report-review boundaries inline.
- Hand large task text, implementer reports, and diffs through files under `.sdc/runtime/<change-id>/`; do not repeatedly paste full plans, history, or diffs into agent prompts.
- Write or update tests before production code when meaningful.
- Do not expand scope or refactor opportunistically.
- After each task, run one read-only review with separate Spec Compliance and Code Quality verdicts. Resolve Critical/Important findings and every acceptance-affecting `Cannot verify` item before marking the task complete.
- Reviewers must not mutate repository state and must not be coached to ignore, suppress, or pre-rate findings.
- Update task status, review status, evidence, notes, changed files, and validation evidence.
- After all tasks, run one whole-change review over the complete change range and record the approved verdict before check/archive.
- Record durable discoveries in `knowledge-candidates.md`; do not silently edit long-lived knowledge while applying code.
- Stop with a clear report if requirements, impact, design, tasks, or code conflict.
