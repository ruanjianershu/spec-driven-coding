---
description: Start a focused SDC requirement change with mandatory intake and minimal discovery artifacts until confirmed.
---

# SDC Change

Use "$ARGUMENTS" as the requirement or change name.

Always start with Mandatory Change Intake Gate:

1. Ask the 4 required intake questions: project context, core scope, technical preferences, constraints/acceptance.
2. Read `.sdc/knowledge/index.md` if it exists, then prefill known context as `Confirmed` only when the source is confirmed; memory-derived content remains `Candidate`.
3. Wait for explicit user confirmation before writing any change file.
4. If any Open Question or high-impact decision remains, stay in Discovery Gate and keep artifacts minimal: `discovery.md`, optional Draft `proposal.md`, and brief `notes.md` only.
5. Do not create or update `spec.md`, `design.md`, `tasks.md`, `impact.md`, `context-pack.md`, or `knowledge-candidates.md` until Discovery Gate exits.
6. Never use "if wrong, tell me" / "如有偏差请告知，我先改" as authorization to write files. Ask yes/no or option confirmation and wait.
7. If the user says "use your judgment", record options as `Proposed` or `Assumed`; do not mark them `Confirmed` or use them as execution inputs.

For Brownfield/Legacy projects, run focused current-change impact analysis only after requirements are confirmed.
