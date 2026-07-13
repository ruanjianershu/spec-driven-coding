---
description: Start a focused SDC requirement change with mandatory intake and minimal discovery artifacts until confirmed.
---

# SDC Change

Use "$ARGUMENTS" as the requirement or change name.

Always start with Mandatory Change Intake Gate:

1. Ask the 4 required intake questions: project context, core scope, technical preferences, constraints/acceptance.
2. Read `.sdc/common-ground.md` if it exists; use ESTABLISHED items to avoid repeated questions, treat WORKING items as candidates, and ask about relevant OPEN items.
3. Read `.sdc/expert-routing.md` if it exists; use `product-discovery` and relevant domain/data/security profiles to shape questions, not to create facts.
4. Read `.sdc/knowledge/index.md` if it exists, then prefill known context as `Confirmed` only when the source is confirmed; memory-derived content remains `Candidate`.
5. Read `sdc-references/artifact-output-contracts.md` when available. Within the same 4 intake categories, identify likely input evidence and required output artifacts: process/state diagram, sequence/integration diagram, API/contract specification, data/migration contract, UX flow, test matrix, deploy/release checklist, and AI involvement note.
6. Treat output artifact requirements as `Proposed` until the user confirms scope. Do not generate final diagrams, API designs, schemas, or release plans during intake.
7. Wait for explicit user confirmation before writing any change file.
8. If any Open Question or high-impact decision remains, stay in Discovery Gate and keep artifacts minimal: `discovery.md`, optional Draft `proposal.md`, and brief `notes.md` only.
9. Do not create or update `spec.md`, `design.md`, `tasks.md`, `impact.md`, `context-pack.md`, or `knowledge-candidates.md` until Discovery Gate exits.
10. Never use "if wrong, tell me" / "如有偏差请告知，我先改" as authorization to write files. Ask yes/no or option confirmation and wait.
11. If the user says "use your judgment", record options as `Proposed` or `Assumed`; do not mark them `Confirmed` or use them as execution inputs.

For Brownfield/Legacy projects, run focused current-change impact analysis only after requirements are confirmed.
