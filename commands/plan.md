---
description: Generate or update the SDC implementation plan for the active change.
---

# SDC Plan

Use "$ARGUMENTS" as extra planning context. Ensure the plan is based on current SDC proposal/spec/design/tasks and produces small, verifiable tasks.

Run the SDC plan workflow:

- Plan only from confirmed requirements and confirmed impact analysis when required.
- Read `.sdc/knowledge/index.md` and relevant product/technical knowledge before planning.
- Stop if relevant knowledge is missing, stale, conflict-marked, or only memory-derived; record a Knowledge Gap instead of guessing.
- Do not turn unresolved decisions into implementation tasks.
- Produce or update design and tasks with `SCN -> REQ -> AC -> T###` traceability.
- Produce or update `context-pack.md` as the short execution handoff: goal, knowledge sources, confirmed product/technical knowledge, boundaries, forbidden assumptions, tasks, validation commands, and candidate routing.
- Keep tasks thin, test-first, dependency ordered, and sized only `S` or `M`.
- Convert reasonable inferences into investigation tasks instead of silent defaults.
