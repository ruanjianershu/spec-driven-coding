---
name: sdc-check
description: "Use when an SDC change needs validation, review, testing, quality, impact, or repository checks."
---

> Codex/Hermes workflow skill generated from `commands/check.md`.
> Treat the user's current request as `$ARGUMENTS`. In Codex/Hermes, route to the matching SDC skill/workflow instead of expecting `/sdc:*` slash-command support.

# SDC Check

Resolve `SDC_PLUGIN_ROOT` from this installed command/skill: the parent of `commands/`, or two levels above `skills/<skill>/`. Do not assume this variable is already set. Verify the helper exists and keep the target project as the working directory when invoking it. For legacy direct skills and Hermes layouts, if the derived root lacks `sdc-cli.py`, use its `sdc-runtime/` child after verifying both the CLI and runtime helper exist there. Missing helpers are an installation blocker, not permission to guess another checkout.

Use "$ARGUMENTS" as the target change or scope. Run the combined validation, review, test, and quality perspectives with concrete evidence.

Run the SDC check workflow:

- Read the verified check manifest, confirmed acceptance/boundaries, actual diff, and relevant evidence. Expand to surrounding sources only for a named risk. Validate the recorded risk rationale against the actual diff using `../../sdc-references/workflow-standards.md` when needed; no silent downgrade or reduced acceptance.
- Validate structure, traceability, decision status, task format, evidence, and Brownfield impact gates.
- Validate Common Ground usage and block final execution if OPEN or high-impact WORKING items were treated as facts.
- Validate Expert Profiles Used against actual diff and risk areas.
- Validate knowledge source usage, `context-pack.md`, and candidate-vs-confirmed boundaries.
- Validate Candidate memory recall and research boundaries: recall is read-only, research scratch is runtime-local, citations are in discovery/notes, durable findings are Candidate in `knowledge-candidates.md`, and no public research command exists.
- Validate session adapter and evidence boundaries: supported opt-in Claude/Codex hooks must remain compact and non-authoritative; absent, unsupported, or failed hooks use the portable `session-context` fallback. Require actual bounded-run receipts for executable validation, not self-reported appended statuses; local runtime evidence stays under `.sdc/runtime/` and durable conclusions stay in tasks/notes/reports.
- Verify manifest hashes, approval snapshots, and validation freshness for the delivery being checked. Missing, malformed, stale, failed, or timed-out required evidence cannot pass; use explicit reasoned reopen for revisions rather than reusing stale state.
- Run `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" manifest verify --change <change-id> --role check` and `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" evidence verify --change <change-id>`. Delivery needs the latest fresh passed execution receipt for each completed task with argv exactly equal to its Verify command, plus a current review receipt binding approved independent review notes/tasks and sources.
- Validate the Artifact Output Contract: triggered diagrams, API/data contracts, UX flow, test matrix, deploy/release checklist, and AI involvement note must exist or be explicitly `N/A` with evidence.
- Validate the Execution Orchestration Contract: Plan Preflight passed, task interfaces are complete, checked tasks have approved dual-verdict reviews and evidence, and any present progress ledger agrees with durable task/notes evidence. A missing git-ignored ledger warns but does not override durable evidence.
- Validate "No Evidence, No Fact / No Confirmation, No Execution / No Impact, No Brownfield Change".
- Review actual diffs and surrounding code for correctness, architecture, security, data integrity, compatibility, and maintainability.
- Treat review as read-only. Report `Cannot verify from diff` separately and resolve it with focused evidence; never silently convert it to approval.
- Require final whole-change review coverage after all implementation, including cross-task integration and unresolved Minor/`Cannot verify` items. One final-snapshot pass may cover both task and whole-change review for a single-task light change, with both verdict records retained.
- Run or assess relevant tests against acceptance criteria, boundaries, regressions, and failure modes. Reuse trustworthy current receipts; rerun only for changed inputs, missing coverage, or a named unresolved risk, not because another stage started.
- When a new run is needed, use `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" evidence run --change <change-id> --stage check --task T001 --timeout 300 -- <exact Verify argv>`; repeated `--task` flags require shared exact argv and shell pipelines require explicit `sh -c`. After final task/review-note changes, refresh/verify manifests and bind already-approved review with `evidence review --change <change-id> --reviewer "<attribution>"`, then verify evidence again. Reviewer attribution is not authenticated identity.
- Evaluate final quality across user-facing flow, docs, security, performance, maintainability, and release readiness.
- Only when validate, review, test, quality, impact, artifact-output, knowledge, and final whole-change review gates all pass, advance `checking -> archivable` with `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" state set --change <change-id> --state archivable --source check-stage --evidence tasks.md --evidence notes.md`. Failed or incomplete checks leave the state unchanged.
- Report whether Common Ground, expert routing, product/technical knowledge, memory candidates, standards, or AGENTS.md need archive-time updates.
- In bug mode, analyze without modifying code unless explicitly requested.
