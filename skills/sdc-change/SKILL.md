---
name: sdc-change
description: "Use when starting or clarifying a focused requirement change under SDC governance."
---

> Codex/Hermes workflow skill generated from `commands/change.md`.
> Treat the user's current request as `$ARGUMENTS`. In Codex/Hermes, route to the matching SDC skill/workflow instead of expecting `/sdc:*` slash-command support.

# SDC Change

Resolve `SDC_PLUGIN_ROOT` from this installed command/skill: the parent of `commands/`, or two levels above `skills/<skill>/`. Do not assume this variable is already set. Verify the helper exists and keep the target project as the working directory when invoking it. For legacy direct skills and Hermes layouts, if the derived root lacks `sdc-cli.py`, use its `sdc-runtime/` child after verifying both the CLI and runtime helper exist there. Missing helpers are an installation blocker, not permission to guess another checkout.

Use "$ARGUMENTS" as the requirement or change name.

Run the evidence-backed Change Intake Gate:

For a new, confirmed behavior-neutral prose correction, assess the compact format in `../../sdc-references/compact-workflow.md` before invoking full init or generating standard artifacts. Unknown requirements stay in discovery; existing standard changes never silently become compact. For compact changes use that format's canonical record and lifecycle steps instead of the standard artifact list below.

1. Cover four categories: project context, core scope, technical preferences, and constraints/acceptance. Cite current user instructions or still-valid prior user/project confirmation for each; ask only missing blocking questions, with no fixed question count or repeated approval ritual. Use `../../sdc-references/discovery-gate.md` for intake and discovery details.
2. Start with the knowledge index and relevant Common Ground/routing entries. Load only affected sources; `ESTABLISHED` must still be current, and personal/native/project memory recall remains `Candidate`, not confirmation.
3. Make authorization and the internal `light` / `standard` / `strict` risk rationale visible. Use `../../sdc-references/workflow-standards.md` for risk selection, delegation boundaries, or stale-source handling. Risk level never resolves unknown business requirements.
4. Use `product-discovery` and relevant expert lenses to identify gaps, not invent facts. Consult `../../sdc-references/artifact-output-contracts.md` when output triggers need assessment; keep unconfirmed outputs `Proposed`.
5. Preserve no write-ahead confirmation. Cite existing explicit authorization before writes; if it does not cover the action, ask and wait. Bounded authorized reversible actions may proceed, but scope, data, permissions, public contracts, and architecture need authoritative confirmation or bounded explicit delegation. Generic "use your judgment" is not blanket consent.
6. If business requirements or other blocking decisions remain unknown, stay in discovery. With authorization to persist discovery, write only `discovery.md`, optional Draft `proposal.md`, and brief `notes.md`; do not create or update `spec.md`, `design.md`, `tasks.md`, `impact.md`, `context-pack.md`, or `knowledge-candidates.md` until Discovery Gate exits.
7. Research scratch stays under `.sdc/runtime/<change-id>/research/`; cite findings in discovery/notes. After discovery closes, reusable findings may be recorded in `knowledge-candidates.md` as Candidate, never automatically promoted.
8. When supported opt-in hooks are absent or fail, recover compact context with `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" session-context --client codex --change <change-id>`. Context injection is non-authoritative; ambiguity remains a stop signal.
9. After authorized minimal discovery artifacts exist, materialize lifecycle `discovery` through the internal runtime helper. Advance to `confirmed` only after discovery closes and the confirmed spec passes its content gates. Complete required impact analysis after confirmation and before planning. For changed requirements, use `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" state reopen --change <change-id> --state discovery --reason "<reason>"`; it archives superseded requirement/downstream artifacts under `revisions/<id>` and invalidates old receipts. Never overwrite state to bypass invalidated approvals. Consult `../../sdc-references/runtime-context.md` for mechanics.

For Brownfield/Legacy projects, run focused current-change impact analysis only after requirements are confirmed.
