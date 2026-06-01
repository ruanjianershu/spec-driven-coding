---
description: Generate project-level AI guardrails from SDC standards.
---

# SDC Harness

Use "$ARGUMENTS" as extra context. Generate or update project-level AI guardrails from `.sdc/standards/`, confirmed `.sdc/knowledge/`, and repeated issues recorded in `.sdc/memory/`.

Run the SDC harness workflow:

- Read `.sdc/constitution.md`, `.sdc/standards/`, `.sdc/knowledge/index.md`, relevant confirmed knowledge, project structure, validation commands, historical reports, and user-provided mistakes or constraints.
- Generate concrete `AGENTS.md` rules for must-do, must-not-do, validation commands, and known recurring mistakes.
- Preserve `.sdc/constitution.md` as higher authority.
- Do not promote memory candidates into `AGENTS.md` unless the user confirms they are durable rules.
- Do not invent project rules without evidence or explicit user direction.
