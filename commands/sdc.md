---
description: SDC main entry. Route init, change, plan, apply, check, archive, and harness for spec-driven coding.
---

# SDC Main Entry

Use this command as the unified SDC entry. Interpret "$ARGUMENTS" as the user's current intent and route to the correct SDC stage:

- initialize workspace -> `/sdc:init`
- align shared assumptions and expert routing -> read `.sdc/common-ground.md` and `.sdc/expert-routing.md` inside the chosen SDC stage
- import existing company/team standards -> initialize first, then place or import them into `.sdc/standards/company/` with a routing index
- new requirement/change -> read knowledge index, `/sdc:change`, then confirmed specification and `/sdc:plan`
- implement current change -> `/sdc:apply`
- delivery check -> `/sdc:check`
- archive completed work -> `/sdc:archive`
- generate project AI rules -> `/sdc:harness`

Prefer the smallest correct public SDC capability. Use internal expert routing instead of adding new public commands. Stop instead of inventing shortcuts when discovery, Common Ground, decisions, knowledge sources, impact, traceability, expert coverage, or validation evidence is missing.
