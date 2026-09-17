---
description: Initialize the standard .sdc workspace for spec-driven coding.
---

# SDC Init

Initialize or repair the standard `.sdc/` workspace in the current project. Treat "$ARGUMENTS" as additional project context.

Do not overwrite user-authored `.sdc/` artifacts. If old SDC-generated managed templates are clearly stale, upgrade them to the current schema only with a `.bak-*` backup and report the repair.

In Claude Code, `/sdc:init` is the single project-level entry. Run the bundled initializer within this workflow; do not ask the user to initialize separately and then run `/sdc:init` again.

Run the SDC init workflow:

- Resolve `SDC_PLUGIN_ROOT` to the installed SDC root containing `sdc-cli.py`, using the current command or skill file's location: above `commands/`, or two levels above `skills/<skill>/`. Verify that the CLI exists; do not guess a home-directory checkout.
- For legacy direct skills and Hermes layouts, if that root lacks `sdc-cli.py`, use its `sdc-runtime/` child after verifying the CLI and runtime helper exist there.
- From the target project's working directory, run `python3 "$SDC_PLUGIN_ROOT/sdc-cli.py" init` to create or repair `.sdc/` idempotently. If Python 3 or the bundled CLI is unavailable, report that blocker; do not silently claim initialization succeeded.
- Do not install or update clients, clone repositories, or run private bootstrap scripts during project initialization.
- Preserve existing user/project memory; native or personal memory is Candidate context, not project authority.
- Create or repair `constitution.md`, `project.md`, `project-cognition.md`, `common-ground.md`, `expert-routing.md`, `knowledge/`, `memory/`, `standards/`, `templates/`, `changes/`, `specs/`, `decisions/`, `reviews/`, and `reports/`.
- Existing imported standards under `.sdc/standards/company/README.md` must be read by index. Standards are optional: an absent pack is not a setup warning, and a generated index is not evidence that private rules were imported.
- Classify the project as Greenfield, Brownfield/Legacy, or Unknown using repository evidence.
- Seed `common-ground.md` with ESTABLISHED / WORKING / OPEN sections; do not mark generated starter content as ESTABLISHED.
- Seed `expert-routing.md` with candidate expert profiles; do not expose those profiles as additional public slash commands.
- Seed a product/technical knowledge index and a memory candidate area; do not treat generated starter content as confirmed facts.
- Only if the user explicitly supplies a private standards path, run `python3 "$SDC_PLUGIN_ROOT/sdc-cli.py" standards import "/path/to/user-supplied/standards"` in the target project to import it under `.sdc/standards/company/` and create a routing index. Do not auto-discover standards in home directories or fetch a company repository. Do not publish those private rules with SDC.
- For Brownfield/Legacy, create or update reusable `project-cognition.md` using code/config/build/test evidence. Start with entrypoints and indexes, refresh affected or missing sections, and expand only for a named gap; no mandatory full-repository read. This is project cognition, not per-change impact analysis.
- Do not perform per-change impact analysis during init; impact analysis belongs inside a confirmed change.
- Do not invent product facts, business rules, permissions, timelines, owners, or undocumented architecture. Record missing information as Knowledge Gaps.
- End with the next step: start the first requirement through `/sdc:change <name>`; do not tell the user to run `/sdc:init` again.
