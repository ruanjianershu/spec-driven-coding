---
name: sdc-init
description: "Use when a project needs an SDC workspace, project cognition, or standards import."
---

> Codex/Hermes workflow skill generated from `commands/init.md`.
> Treat the user's current request as `$ARGUMENTS`. In Codex/Hermes, route to the matching SDC skill/workflow instead of expecting `/sdc:*` slash-command support.

# SDC Init

Initialize or repair the standard `.sdc/` workspace in the current project. Treat "$ARGUMENTS" as additional project context.

Do not overwrite user-authored `.sdc/` artifacts. If old SDC-generated managed templates are clearly stale, upgrade them to the current schema only with a `.bak-*` backup and report the repair.

In Claude Code, `/sdc:init` is the single project-level entry. Do not ask the user to run terminal `sdc-init` and then run `/sdc:init` again.

Run the SDC init workflow:

- First run the local internal project initializer when available:
  - Prefer: `sdc-init --project "$PWD" --skip-install`
  - If `sdc-init` is not on PATH but `SDC_HOME` is set, run: `"$SDC_HOME/bin/sdc-init" --project "$PWD" --skip-install`
  - If neither is available but `$HOME/workspace/spec-driven-coding/bin/sdc-init` exists, run that script with `--project "$PWD" --skip-install`.
  - If no local initializer exists, continue with the artifact workflow below and report that the company standards pack could not be imported automatically.
- Create or repair `.sdc/` idempotently if the local initializer did not already do it.
- Preserve existing user/project memory.
- Create or repair `constitution.md`, `project.md`, `project-cognition.md`, `common-ground.md`, `expert-routing.md`, `knowledge/`, `memory/`, `standards/`, `templates/`, `changes/`, `specs/`, `decisions/`, `reviews/`, and `reports/`.
- Verify whether `.sdc/standards/company/README.md` exists. If it exists, report that company standards are available and must be read by index. If it does not exist, record this as a setup warning.
- Classify the project as Greenfield, Brownfield/Legacy, or Unknown using repository evidence.
- Seed `common-ground.md` with ESTABLISHED / WORKING / OPEN sections; do not mark generated starter content as ESTABLISHED.
- Seed `expert-routing.md` with candidate expert profiles; do not expose those profiles as additional public slash commands.
- Seed a product/technical knowledge index and a memory candidate area; do not treat generated starter content as confirmed facts.
- If the user provides an existing standards directory, import it as a private company/team standards pack under `.sdc/standards/company/` and create a routing index. Do not publish those private rules with SDC.
- For Brownfield/Legacy, create or update reusable `project-cognition.md` using code/config/build/test evidence. This is an agent-level project cognition pass, not a per-change impact analysis.
- Do not perform per-change impact analysis during init; impact analysis belongs inside a confirmed change.
- Do not invent product facts, business rules, permissions, timelines, owners, or undocumented architecture. Record missing information as Knowledge Gaps.
- End with the next step: start the first requirement through `/sdc:change <name>`; do not tell the user to run `/sdc:init` again.
