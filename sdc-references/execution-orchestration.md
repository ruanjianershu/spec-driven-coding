# SDC Execution Orchestration Contract

This reference defines how SDC executes a confirmed implementation plan without adding public commands.

Use the risk policy in [workflow standards](workflow-standards.md) when choosing execution breadth. The same acceptance, consent, and independent review gates apply at every level; task count, context size, and repeated runs are not proxies for quality.

```text
plan preflight -> task brief -> implement -> evidence -> task review -> ledger -> next task -> whole-change review
```

The public workflow remains:

```text
init -> change -> plan -> apply -> check -> archive
```

## Core Principles

- A fresh execution context should receive one task, its interfaces, and the binding global constraints, not the full conversation history.
- Every completed task must have read-only review evidence with separate specification compliance and implementation quality verdicts.
- A final whole-change review checks cross-task behavior, integration, regressions, and Artifact Output Contract drift.
- Conversation memory is not a progress database. Persist execution progress in a project-local ledger.
- Review is read-only. A reviewer must not mutate the working tree, index, HEAD, branch, plan, or evidence package.
- Reviewers judge evidence independently. Controllers and implementers must not suppress findings, pre-rate severity, or instruct a reviewer to ignore plan-mandated defects.
- Use files for large handoffs. Do not paste full plans, accumulated task history, reports, or diffs into repeated agent prompts.

## Plan Preflight

Before Task 1, inspect the complete plan once for:

- contradictions between tasks;
- contradictions with Global Constraints, confirmed spec, impact analysis, standards, or Artifact Output Contract;
- placeholders, undefined interfaces, missing exact values, or unverifiable commands;
- tasks that are too large for focused verification or artificially split one acceptance boundary into redundant test/edit/review loops;
- plan-mandated behavior that the review rubric would reject as a defect.

Record one of:

- `Passed`: no blocking conflict remains;
- `Blocked`: list all conflicts together and ask the user which source governs;
- `Needs update`: repair the plan before apply.

Persist closed findings explicitly as `Findings: None`, `Findings: Resolved: ...`, `Findings: Closed: ...`, or `Findings: No blocking findings ...`. A sentence describing an open or remaining conflict is not a closed preflight.

Do not discover one known plan contradiction per task. Batch preflight findings before execution begins.

## Global Constraints

`design.md`, `tasks.md`, and `context-pack.md` must carry the exact project-wide constraints that bind every task, for example:

- version floors and dependency limits;
- architecture and module boundaries;
- exact names, values, formats, and compatibility rules;
- security, data, transaction, migration, rollout, and rollback constraints;
- relevant company/project standards;
- confirmed non-scope and forbidden assumptions.

Copy exact values from confirmed sources. Do not paraphrase an exact contract into a weaker statement.

## Task Contract

Each `T###` task must contain:

- `Depends on`: prior tasks or `none`;
- `Files`: exact files or focused areas expected to change;
- `Consumes`: exact interfaces, types, data, decisions, or outputs used from prior work;
- `Produces`: exact interfaces, types, behavior, or evidence later work relies on;
- `Verify`: executable command argv for the required delivery receipt; manual observations may supplement it;
- `Expected`: the observable expected result;
- `Review`: `Pending`, `Approved`, `Needs fixes`, or `Cannot verify`;
- `Evidence`: report, command output, commit/diff range, or `Pending`;
- `Source`: `REQ-*` / `AC-*` source.

A task is a coherent acceptance boundary. Fold meaningful test-first work, setup, configuration, generated files, and documentation into the task that needs them. Split a task only when a reviewer could reasonably approve one part and reject the other. A tiny behavior-neutral change may use one task with focused validation rather than a manufactured failing test or multiple review loops.

### Vertical Behavior Slices

Default to a verifiable behavior slice: a confirmed input or action, its observable outcome, and the evidence that distinguishes success from failure. Include only the layers needed for that behavior. "Reject an expired invitation without creating membership" is a slice; separate "all models", "all services", and "all tests" tasks usually leave acceptance unverified until the end.

- Name `Depends on` only when a task consumes an actual output, interface, prerequisite decision, or migration state from another task. Explain that connection in `Consumes` and `Produces`; do not manufacture dependencies from file order or role labels. Execution remains serial under the orchestration rules below even when tasks have no semantic dependency.
- Verify each slice at its public boundary and include the affected failure or regression checks. If the slice cannot be meaningfully checked until unrelated future work, revise its boundary or identify the real prerequisite.
- Do not require every slice to touch UI, API, service, database, or infrastructure. A CLI-only behavior, documentation correction, or isolated library change needs only its affected surfaces. A slice does not require one agent per layer.
- A behavior-neutral mechanical migration may instead group files by a transformation invariant, such as preserving imports during a package rename. State the invariant, affected surface, and executable compatibility checks. This exception does not make data migration or changed business behavior low risk; the shared risk policy still applies.

Load [test quality](test-quality.md) when designing or assessing behavior tests, reproducing a bug, or judging whether a passing command proves acceptance. Keep the detailed test guidance there rather than copying it into every task brief.

## Runtime Workspace

Use project-local ignored scratch space:

```text
.sdc/runtime/<change-id>/
├── progress.md
├── task-T001-brief.md
├── task-T001-report.md
├── task-T001-review-package.md
└── final-review-package.md
```

The runtime workspace is not durable project truth and must be git-ignored. Durable outcomes still belong in `tasks.md`, `notes.md`, `knowledge-candidates.md`, review/test reports, and archive evidence.

Before dispatching or starting a task, check `progress.md` when present. A task marked complete there must not be re-executed merely because conversation context was compacted or lost. Reconcile the ledger against durable review evidence, source snapshots, git history, and the working tree; an ignored ledger never authorizes stale work. Verify required manifests and refresh only affected sources. Changed governing inputs require explicit reasoned reopen and invalidation of affected approvals, not a fabricated resume point.

## File Handoffs

### Task Brief

The task brief contains:

- the task's complete task block;
- binding Global Constraints;
- relevant execution boundaries and forbidden assumptions;
- exact interfaces consumed and produced;
- relevant validation commands.

It excludes unrelated tasks, prior conversation, and broad repository summaries.

### Implementer Report

When handing work between contexts, the implementer writes a detailed report to a file and returns a short status:

- `DONE`;
- `DONE_WITH_CONCERNS`;
- `NEEDS_CONTEXT`;
- `BLOCKED`.

The report records changed files, tests written first where meaningful, red/green evidence, commands and actual execution receipts, deviations, concerns, and the diff/commit boundary. Use `evidence run --change <id> --stage apply|check --task T001 --timeout 300 -- <exact Verify argv>` through the internal runtime helper; repeated task flags require shared exact argv, and pipelines require explicit `sh -c`.

For a small inline task, a concise durable notes section may serve as brief/report without duplicated scratch files. Preserve the same interfaces, evidence, and review records.

### Review Package

The reviewer receives paths to the task brief, implementer report, and review package. The review package contains the relevant commit list or working diff, stat summary, and contextual diff. Do not make every reviewer reconstruct the same diff or permanently paste it into controller context.

For `WORKTREE` review, all task files must already be tracked in the index or a commit. If untracked files exist, stop instead of generating a package that silently omits them.

## Per-Task Review Gate

One task reviewer returns both verdicts:

1. `Spec Compliance`: compliant, issues found, and any `Cannot verify from diff` items.
2. `Code Quality`: approved or needs fixes, with Critical, Important, and Minor findings.

Every finding must cite file and line evidence when available. The implementer report is an unverified claim, not proof.

Critical and Important findings block task completion. Fix them together, append test evidence to the report, and re-review the task. Minor findings remain visible in the ledger for the final whole-change review.

Re-review affected findings and integration risks after fixes; do not repeat unchanged review or trustworthy tests without a named risk. For a single-task light change, one independent final-snapshot pass may cover both the task and complete change. Persist both task and final verdict records pointing to that evidence; no review gate is waived.

`Cannot verify` is not approval. The coordinating agent must perform the focused check, cite evidence, and either approve the item or return it for implementation.

When a finding conflicts with an explicit plan requirement, report it as plan-mandated and ask the user which source governs. Do not silently dismiss the finding or fix against the confirmed plan.

## Reviewer Independence

Review prompts must not contain instructions such as:

- "do not flag";
- "ignore this";
- "minor at most";
- "the plan chose this, so accept it".

The reviewer is read-only and skeptical of rationales. It may inspect unchanged code only for a concrete named risk that cannot be judged from the diff. It should not rerun broad test suites already covered by trustworthy evidence unless a specific unresolved risk requires a focused command.

## Harness And Model Adaptation

When supported and authorized, use a separate read-only reviewer context. Fresh implementer contexts are useful for substantive handoffs, not mandatory for every tiny edit:

- use a task-scoped implementer context and only the relevant sources;
- use a separate read-only reviewer context;
- do not dispatch multiple implementation tasks in parallel. Complete implementation, review, durable evidence, and ledger update for the current task before starting the next task.

When separate contexts are unavailable or not authorized, execute inline but reset the role boundary explicitly: finish implementation, write the report, then perform a separate skeptical review pass from the brief and actual diff. Disclose the isolation limitation; do not call self-review an external review. Expert profiles are lenses, not a mandate to build a multi-agent swarm.

When the harness exposes model selection, choose an explicit capability tier appropriate to task risk and record it in the report. Do not invent model identifiers when selection is unavailable; record `Auto` or `N/A` instead.

## Durable Progress

After a task review is approved:

- mark the task checkbox complete;
- set `Review: Approved`;
- replace `Evidence: Pending` with the report and diff/commit evidence;
- append a concise completion row to `.sdc/runtime/<change-id>/progress.md`;
- summarize durable evidence in `notes.md`.

Never use the runtime ledger as the only delivery evidence.

## Final Whole-Change Review

After all implementation is complete, require one final review over the complete change range, with depth proportional to risk. A single-task light change may share this pass with its task review only when both cover the same final snapshot. It must cover:

- cross-task integration and interface consistency;
- confirmed spec and AC coverage;
- architecture, security, data integrity, compatibility, performance, and maintainability;
- Brownfield `impact.md` alignment;
- Artifact Output Contract drift;
- unresolved per-task Minor and `Cannot verify` items;
- final test and release evidence.

Record the final verdict and evidence in `notes.md` or a linked review report. `sdc-check` and `sdc-archive` must block completed delivery when this evidence is missing or not approved.

Check may reuse approved final-review evidence when the reviewed inputs and scope are unchanged. A changed diff, governing source, or unresolved acceptance risk invalidates the affected approval; review that change before delivery. Run executable validation through the bounded evidence runner and retain actual outcomes/snapshots, never self-declared success.

Persist last-task progress and final approved review notes before capturing a review receipt with the internal helper's `evidence review --change <id> --reviewer "<attribution>"`. Refresh/verify role manifests after progress at safe checkpoints, without blessing changed requirements. The review command binds existing approved notes/tasks and source snapshots; it neither performs review nor authenticates the attribution. `evidence verify --change <id>` checks that receipt and the latest fresh passed run per completed task with exact Verify argv. Later source edits or reopen invalidate affected receipts. See `runtime-context.md` for full commands.

## Stop Conditions

Stop execution when:

- Plan Preflight is not `Passed`;
- a task lacks exact interfaces or verification evidence;
- an implementer returns `BLOCKED` and the blocker cannot be resolved from confirmed context;
- a review has unresolved Critical or Important findings;
- a `Cannot verify` item affects acceptance, data, permissions, security, compatibility, rollout, or rollback;
- implementation discovers a new high-impact decision or output artifact not captured by spec/design/context-pack;
- actual work exceeds confirmed impact or scope.
