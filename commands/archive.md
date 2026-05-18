---
description: Archive a completed SDC change, preserve stable specs and evidence, and run the Knowledge Compact Gate.
---

# SDC Archive

Use "$ARGUMENTS" as the change id. Archive only after required checks pass or equivalent evidence exists.

During archive, run the Knowledge Compact Gate. Required spec/archive writes may proceed; optional updates to decisions, standards, reports, AGENTS.md, project.md, or project-cognition.md require explicit user confirmation before writing.

Run the SDC archive workflow:

- Require a final confirmed spec, completed tasks, traceability, and check evidence.
- Promote the final spec to `.sdc/specs/<change-id>.md`.
- Create or update `archive.md` with conclusion, evidence, residual risks, coverage summary, and Knowledge Compact Gate.
- Move the completed change into `.sdc/changes/archive/<change-id>/`.
- Never delete change history or silently overwrite an existing stable spec.
