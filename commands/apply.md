---
description: Implement the active SDC change and update task and notes evidence.
---

# SDC Apply

Use "$ARGUMENTS" to identify the target change or task. Implement the planned work, keep notes/tasks updated, and preserve verification evidence.

Run the SDC apply workflow:

- Read `.sdc/constitution.md`, `.sdc/knowledge/index.md`, relevant product/technical knowledge, the active change `spec.md`, `design.md`, `tasks.md`, `context-pack.md`, and `notes.md` before editing.
- Stop if final artifacts contain open Knowledge Gaps or `Assumed` / `Proposed` / `TBD` / `Conflict` / `Stale` execution inputs.
- Execute tasks in dependency order.
- Write or update tests before production code when meaningful.
- Do not expand scope or refactor opportunistically.
- Update task status, notes, changed files, and validation evidence.
- Record durable discoveries in `knowledge-candidates.md`; do not silently edit long-lived knowledge while applying code.
- Stop with a clear report if requirements, impact, design, tasks, or code conflict.
