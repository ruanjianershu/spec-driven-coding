---
description: Generate or update the SDC implementation plan for the active change.
---

# SDC Plan

Resolve `SDC_PLUGIN_ROOT` from this installed command/skill: the parent of `commands/`, or two levels above `skills/<skill>/`. Do not assume this variable is already set. Verify the helper exists and keep the target project as the working directory when invoking it. For legacy direct skills and Hermes layouts, if the derived root lacks `sdc-cli.py`, use its `sdc-runtime/` child after verifying both the CLI and runtime helper exist there. Missing helpers are an installation blocker, not permission to guess another checkout.

Use "$ARGUMENTS" as extra planning context. Ensure the plan is based on current SDC proposal/spec/design/tasks and produces small, verifiable tasks.

Run the SDC plan workflow:

If the selected change uses `compact.json`, load `sdc-references/compact-workflow.md` and follow its single-record plan/manifest gates instead of generating the standard artifacts below. The compact contract is the authority; state/manifests are derived evidence, not additional policy sources.

- Plan only from confirmed requirements and confirmed impact analysis when required.
- Read the knowledge index and relevant Common Ground, routing, and confirmed source sections; reuse still-current context rather than rereading the repository. Do not plan final execution from OPEN or high-impact WORKING items.
- Read `.sdc/expert-routing.md`; select the smallest relevant expert profiles internally.
- Record the internal `light` / `standard` / `strict` level, triggers, authorization, context scope, and validation rationale in `context-pack.md`. Consult `sdc-references/workflow-standards.md` when selecting or changing policy; no silent downgrade or weaker acceptance is allowed.
- Use `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" recall --change <change-id> --query "<terms>"` only for bounded Candidate context recovery; do not plan from recall output unless confirmed by the user or project knowledge.
- If the session has no injected active-change context, use `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" session-context --client codex --change <change-id>` as the portable adapter; do not infer from directory recency.
- Read `sdc-references/artifact-output-contracts.md` when available. Convert the confirmed output contract into concrete design sections and validation tasks.
- Read `sdc-references/execution-orchestration.md` when available. Produce the Global Constraints, Plan Preflight, task interface, and review fields required for reliable execution.
- Check source freshness against the affected files/contracts and confirmation scope. Refresh affected source evidence within existing authority; stop on unresolved conflicts, business gaps, or missing authorization, not merely an old timestamp. Personal/native memory is Candidate too.
- Do not turn unresolved decisions into implementation tasks.
- Produce or update design and tasks with `SCN -> REQ -> AC -> T###` traceability.
- Route research evidence internally when needed: `.sdc/runtime/<change-id>/research/` for scratch, discovery/notes for citations, and `knowledge-candidates.md` for durable Candidate findings.
- Produce triggered output artifacts in `design.md`: process/state diagrams, sequence/integration diagrams, API/contract specs, data/migration contracts, UX flow, test matrix, deploy/release checklist, and AI involvement note. If a triggered artifact is not applicable, write `N/A` with evidence-based reason.
- Produce or update `context-pack.md` as the short execution handoff: goal, knowledge sources, Common Ground used, Expert Profiles Used, confirmed product/technical knowledge, boundaries, forbidden assumptions, tasks, validation commands, and candidate routing.
- Read `sdc-references/runtime-context.md` when available. After final design/tasks/context-pack are coherent, generate role manifests with `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" manifest generate --change <change-id> --role apply` and `--role check`; keep `context-pack.md` as the human-readable handoff.
- Verify each generated manifest with `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" manifest verify --change <change-id> --role apply` and `--role check`, then advance `confirmed -> planned` with `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" state set --change <change-id> --state planned --source plan-stage --evidence design.md --evidence tasks.md --evidence context-pack.md` after Plan Preflight passes. Same-state retries are idempotent only while fresh.
- For replanning, use `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" state reopen --change <change-id> --state confirmed --reason "<reason>"` only with unchanged snapshotted requirements. Changed requirements require `--state discovery`. Reopen archives downstream artifacts under `revisions/<id>`, preserves history, and invalidates old receipts; rebuild affected artifacts/approvals instead of forcing state forward.
- Summarize `Artifact Output Contract` in `context-pack.md` so apply/check agents know which outputs must remain satisfied.
- Copy exact project-wide requirements into `Global Constraints` in `design.md`, `tasks.md`, and `context-pack.md`; do not weaken exact values by paraphrasing.
- Run Plan Preflight before handoff and record `Status: Passed` only after task conflicts, placeholders, undefined interfaces, and review-hostile instructions are resolved.
- Every task must declare exact `Files`, `Consumes`, `Produces`, `Verify`, `Expected`, `Review`, `Evidence`, and `Source` fields.
- Choose executable `Verify` argv that proves the task's ACs; final delivery requires its exact matching run receipt. Manual observations can supplement that check, not replace a required receipt. Use explicit `sh -c` for shell pipelines.
- Keep tasks thin, dependency ordered, and sized only `S` or `M`. For meaningful behavior tests use test-first work within the same coherent task; do not split a tiny change into artificial test/implementation/review loops.
- Consult `sdc-references/test-quality.md` when selecting tests and independent expected results. Use meaningful behavior slices and explicit task dependencies as defined in `execution-orchestration.md`, not separate database/API/UI tickets by default.
- Unknown business requirements belong only in discovery, not spec/design/tasks. Resolve technical uncertainties by focused investigation within confirmed scope before finalizing dependent implementation tasks.
