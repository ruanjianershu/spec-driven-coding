---
description: Initialize the standard .sdc workspace for spec-driven coding.
---

# SDC Init

Initialize or repair the standard `.sdc/` workspace in the current project. Treat "$ARGUMENTS" as additional project context.

Do not overwrite user-authored `.sdc/` artifacts. If old SDC-generated managed templates are clearly stale, upgrade them to the current schema only with a `.bak-*` backup and report the repair.

Run the SDC init workflow:

- Create or repair `.sdc/` idempotently.
- Preserve existing user/project memory.
- Create or repair `constitution.md`, `project.md`, `project-cognition.md`, `knowledge/`, `memory/`, `standards/`, `templates/`, `changes/`, `specs/`, `decisions/`, `reviews/`, and `reports/`.
- Classify the project as Greenfield, Brownfield/Legacy, or Unknown using repository evidence.
- Seed a product/technical knowledge index and a memory candidate area; do not treat generated starter content as confirmed facts.
- For Brownfield/Legacy, create or update reusable `project-cognition.md`; do not perform per-change impact analysis during init.
