---
description: Generate or update the SDC implementation plan for the active change.
---

# SDC Plan

Use "$ARGUMENTS" as extra planning context. Ensure the plan is based on current SDC proposal/spec/design/tasks and produces small, verifiable tasks.

Run the SDC plan workflow:

- Plan only from confirmed requirements and confirmed impact analysis when required.
- Do not turn unresolved decisions into implementation tasks.
- Produce or update design and tasks with `SCN -> REQ -> AC -> T###` traceability.
- Keep tasks thin, test-first, dependency ordered, and sized only `S` or `M`.
- Convert reasonable inferences into investigation tasks instead of silent defaults.
