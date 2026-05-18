---
description: Generate project-level AI guardrails from SDC standards.
---

# SDC Harness

Use "$ARGUMENTS" as extra context. Generate or update project-level AI guardrails from `.sdc/standards/`.

Run the SDC harness workflow:

- Read `.sdc/constitution.md`, `.sdc/standards/`, project structure, validation commands, historical reports, and user-provided mistakes or constraints.
- Generate concrete `AGENTS.md` rules for must-do, must-not-do, validation commands, and known recurring mistakes.
- Preserve `.sdc/constitution.md` as higher authority.
- Do not invent project rules without evidence or explicit user direction.
