---
description: SDC main entry. Route init, change, plan, apply, check, archive, and harness for spec-driven coding.
---

# SDC Main Entry

Resolve `SDC_PLUGIN_ROOT` from this installed command/skill: the parent of `commands/`, or two levels above `skills/<skill>/`. Do not assume this variable is already set. Verify the helper exists and keep the target project as the working directory when invoking it. For legacy direct skills and Hermes layouts, if the derived root lacks `sdc-cli.py`, use its `sdc-runtime/` child after verifying both the CLI and runtime helper exist there. Missing helpers are an installation blocker, not permission to guess another checkout.

Use this command as the unified SDC entry. Interpret "$ARGUMENTS" as the user's current intent and route to the correct SDC stage:

- initialize workspace and company standards inside Claude Code -> `/sdc:init`
- align shared assumptions and expert routing -> read `.sdc/common-ground.md` and `.sdc/expert-routing.md` inside the chosen SDC stage
- import existing company/team standards -> initialize first, then place or import them into `.sdc/standards/company/` with a routing index
- recover active-change context when native hooks are unavailable -> run `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" session-context --client codex --change <change-id>` or set `SDC_ACTIVE_CHANGE`
- new requirement/change -> read knowledge index, `/sdc:change`, then confirmed specification and `/sdc:plan`
- implement current change -> `/sdc:apply`
- delivery check -> `/sdc:check`
- missing/duplicate/stale installed commands or skills -> `/sdc:check installation` (read-only diagnostics, no active change required)
- archive completed work -> `/sdc:archive`
- generate project AI rules -> `/sdc:harness`

Keep the six lifecycle entries `init/change/plan/apply/check/archive`; `sdc` is the router and `harness` is an existing optional guardrail utility, not another lifecycle stage. Use internal expert routing instead of adding public commands or a multi-agent swarm.

For a new confirmed prose correction, assess `sdc-references/compact-workflow.md` before routing through full init or standard planning. Existing project rules win; unknown scope stays in discovery. Compact is a format within the same stages, not a new public command.

At the chosen stage, load only relevant sources and reuse cited current confirmations. Consult `sdc-references/workflow-standards.md` for risk selection, authorization boundaries, or freshness/reopen decisions. Internal `light` / `standard` / `strict` policies vary effort, never semantic acceptance. Ask only missing blocking questions; unknown business requirements remain in discovery, and high-impact actions require authoritative confirmation or bounded explicit delegation.
