---
name: sdc-harness
description: "Use when project-level AI guardrails must be generated from SDC standards."
---

> Codex/Hermes workflow skill generated from `commands/harness.md`.
> Treat the user's current request as `$ARGUMENTS`. In Codex/Hermes, route to the matching SDC skill/workflow instead of expecting `/sdc:*` slash-command support.

# SDC Harness

Use "$ARGUMENTS" as extra context. Generate or update project-level AI guardrails from `.sdc/standards/`, confirmed `.sdc/knowledge/`, and repeated issues recorded in `.sdc/memory/`.

Run the SDC harness workflow:

- Read binding governance and knowledge/standards indexes, then only relevant confirmed sources, routing entries, validation commands, or reports supporting the requested guardrails. Do not bulk-read history or the repository.
- If `.sdc/standards/company/README.md` exists, read that index first and pull only durable, relevant company/team rules into `AGENTS.md`.
- Generate concrete `AGENTS.md` rules for must-do, must-not-do, validation commands, and known recurring mistakes.
- Convert repeated Common Ground or expert routing misses into concrete guardrails only after user confirmation.
- Preserve `.sdc/constitution.md` as higher authority.
- Do not promote project, personal, or native memory candidates into `AGENTS.md` unless the user confirms the exact durable rule and destination.
- Do not invent project rules without evidence or explicit user direction.
