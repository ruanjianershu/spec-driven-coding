---
description: Generate or update the SDC implementation plan for the active change.
---

# SDC Plan

Use "$ARGUMENTS" as extra planning context. Ensure the plan is based on current SDC proposal/spec/design/tasks and produces small, verifiable tasks.

Run the SDC plan workflow:

- Plan only from confirmed requirements and confirmed impact analysis when required.
- Read `.sdc/common-ground.md`; do not plan final execution from OPEN or high-impact WORKING items.
- Read `.sdc/expert-routing.md`; select the smallest relevant expert profiles internally.
- Read `.sdc/knowledge/index.md` and relevant product/technical knowledge before planning.
- Read `sdc-references/artifact-output-contracts.md` when available. Convert the confirmed output contract into concrete design sections and validation tasks.
- Read `sdc-references/execution-orchestration.md` when available. Produce the Global Constraints, Plan Preflight, task interface, and review fields required for reliable execution.
- Stop if relevant knowledge is missing, stale, conflict-marked, or only memory-derived; record a Knowledge Gap instead of guessing.
- Do not turn unresolved decisions into implementation tasks.
- Produce or update design and tasks with `SCN -> REQ -> AC -> T###` traceability.
- Produce triggered output artifacts in `design.md`: process/state diagrams, sequence/integration diagrams, API/contract specs, data/migration contracts, UX flow, test matrix, deploy/release checklist, and AI involvement note. If a triggered artifact is not applicable, write `N/A` with evidence-based reason.
- Produce or update `context-pack.md` as the short execution handoff: goal, knowledge sources, Common Ground used, Expert Profiles Used, confirmed product/technical knowledge, boundaries, forbidden assumptions, tasks, validation commands, and candidate routing.
- Summarize `Artifact Output Contract` in `context-pack.md` so apply/check agents know which outputs must remain satisfied.
- Copy exact project-wide requirements into `Global Constraints` in `design.md`, `tasks.md`, and `context-pack.md`; do not weaken exact values by paraphrasing.
- Run Plan Preflight before handoff and record `Status: Passed` only after task conflicts, placeholders, undefined interfaces, and review-hostile instructions are resolved.
- Every task must declare exact `Files`, `Consumes`, `Produces`, `Verify`, `Expected`, `Review`, `Evidence`, and `Source` fields.
- Keep tasks thin, test-first, dependency ordered, and sized only `S` or `M`.
- Convert reasonable inferences into investigation tasks instead of silent defaults.
