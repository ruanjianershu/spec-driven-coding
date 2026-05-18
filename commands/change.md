---
description: Start a focused SDC requirement change with mandatory intake and minimal discovery artifacts until confirmed.
---

# SDC Change

Use "$ARGUMENTS" as the requirement or change name.

Always start with Mandatory Change Intake Gate:

1. Ask the 4 required intake questions: project context, core scope, technical preferences, constraints/acceptance.
2. Wait for explicit user confirmation before writing any change file.
3. If any Open Question or high-impact decision remains, stay in Discovery Gate and keep artifacts minimal: `discovery.md`, optional Draft `proposal.md`, and brief `notes.md` only.
4. Do not create or update `spec.md`, `design.md`, `tasks.md`, or `impact.md` until Discovery Gate exits.
5. Never use "if wrong, tell me" / "如有偏差请告知，我先改" as authorization to write files. Ask yes/no or option confirmation and wait.

For Brownfield/Legacy projects, run focused current-change impact analysis only after requirements are confirmed.
