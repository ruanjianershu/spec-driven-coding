# Changelog

All notable changes to SDC are documented here.

## 1.1.10

- Fixed the remaining Claude Code duplicate UX where public slash commands such as `sdc:apply` still appeared beside equivalent plugin skills such as `sdc:sdc-apply`.
- Claude Code now exposes public workflows only as slash commands; Claude skills are limited to advanced non-public capabilities: spec, implement, review, test, quality, and validate.
- Made Claude public command prompts self-contained instead of referencing backing skills that are intentionally not exposed in Claude.
- Updated installer, release audit, and docs to prevent public command backing skills from being generated in Claude `.claude/skills/`.

## 1.1.9

- Fixed Claude Code duplicate command/skill registration by generating Claude skill directories with `sdc-*` names instead of short command aliases.
- Changed the Claude plugin manifest to declare skills explicitly as an array, so public slash commands such as `/sdc:init` do not collide with same-named plugin skills.
- Updated installer and release audit checks to prevent short Claude skill alias directories from returning.

## 1.1.8

- Changed Codex installation to plugin-first by default and clean stale `~/.agents/skills/sdc-*` and `~/.codex/plugins/sdc` direct installs to avoid duplicate SDC entries.
- Added `SDC_CODEX_DIRECT_SKILLS=1` as an explicit legacy fallback for older Codex builds that only scan direct skills.
- Fixed CLI validation so confirmed Greenfield changes can proceed without `impact.md`; Brownfield/Unknown changes still require it.
- Fixed `sdc validate` and `sdc check` exit codes so structural validation errors return a non-zero status for scripts and CI.
- Split installer completion guidance by platform so Codex users are not told to expect `/sdc:*` slash commands.
- Aligned the command model so Codex declares skills only, Claude exposes only public slash commands, and detailed controls remain skills.
- Strengthened CLI validation for confirmed changes: confirmed specs must not be Draft, design.md is checked, common template placeholders are rejected, and impact.md accepts the English Change Impact Gate schema.
- Fixed Claude local install fallback so the generated marketplace is written even when the `claude` CLI is unavailable, without leaving a direct root plugin copy.
- Added a release audit script to catch version drift, command exposure drift, Codex slash-command drift, stale schema strings, and README command-model drift before publishing.
- Clarified Brownfield analysis layering: project cognition is reusable repo memory, while each confirmed change gets a focused `impact.md`; full repo cognition is refreshed only when stale, incomplete, structurally changed, or explicitly requested.
- Added positioning guidance: SDC's strongest value is safe Brownfield/Legacy iteration, while Greenfield projects benefit from early specs, standards, traceability, and test discipline.
- Added Knowledge Compact Gate inside archive so completed changes recommend the right durable updates to specs, archive history, decisions, standards, reports, AGENTS.md, project context, or project cognition without adding another public command.
- Hardened CLI archive behavior: archive now runs validation first, blocks Draft specs, unchecked tasks, existing stable specs, and existing archive directories, and writes a correct archived spec relative link.
- Updated README and release checklist with Codex duplicate-skill verification.

## 1.1.7

- Aligned spec templates with the current schema by adding explicit `INV-*` business invariant placeholders and schema metadata.
- Updated validation to require `INV-*` alongside `SCN-*`, `REQ-*`, and `AC-*`.
- Added safe init repair for stale SDC-generated templates: old managed templates are upgraded with `.bak-*` backups instead of being left to fail later validation.
- Clarified Discovery Open versus Discovery Closed active change structures.

## 1.1.6

- Added Discovery Artifact Budget: unresolved requirements now stay in `discovery.md`, optional Draft `proposal.md`, and brief `notes.md` instead of generating full `spec.md`, `design.md`, `tasks.md`, or `impact.md`.
- Added No Write-Ahead Confirmation rules to forbid "if wrong, tell me, I will update now" as authorization.
- Strengthened Decision Ledger gates so high-impact inferences remain `Proposed` or `Assumed` until explicit confirmation.
- Updated CLI `sdc change` to create a minimal Discovery Open draft by default.
- Updated validation to flag full artifacts created before Discovery Gate exits.

## 1.1.5

- Fixed Claude Code local marketplace packaging so it exposes only `.claude/skills/` and no longer registers duplicate root `skills/` entries.
- Kept Codex and Hermes skill packaging unchanged.
- Added release checklist coverage for duplicate skill registration.

## 1.1.4

- Added English Role Prompt Contracts to every SDC skill.
- Standardized each contract around Role, Operating Contract, Evidence Rules, and Output Contract.
- Strengthened expert persona behavior without adding new public commands.
- Updated README, docs, package metadata, and plugin metadata for the role contract upgrade.

## 1.1.3

- Added Brownfield/Legacy project cognition during init through `project-cognition.md`.
- Clarified that legacy change impact analysis happens after requirements are confirmed inside the current change, not during init.
- Added per-change `impact.md` generation and Change Impact Gate before plan/apply for legacy projects.
- Updated review/check to include final old-system modification and impact analysis for legacy deliveries.
- Expanded CLI/templates/docs/metadata for legacy project cognition and confirmed-requirement impact analysis.

## 1.1.2

- Added Discovery Gate as the built-in requirement exploration phase inside `/sdc:change`.
- Added `discovery.md` templates to init and change workspaces for current understanding, candidate directions, tradeoffs, recommended MVP, Decision Ledger, open questions, and exit criteria.
- Updated `/sdc:spec` to consume `discovery.md` and refuse Confirmed specs while blocking discovery questions or high-impact decisions remain unresolved.
- Documented the command model: `change` is the normal entry point, `spec` is the specification refinement inside a change.

## 1.1.1

- Added consent gates to prevent AI-generated assumptions from becoming confirmed requirements or implementation tasks.
- Added Brainstorm-first and Decision Ledger rules to `/sdc:spec`.
- Added Technical Consent Gate and MVP Slice Gate to `/sdc:plan`.
- Updated `/sdc:validate` and `/sdc:check` to flag unconfirmed decisions, silent defaults, and over-large task plans.
- Updated constitution, harness, README, and discipline docs with Human Confirmation and No Silent Defaults rules.

## 1.1.0

- Added the SDC discipline core: governance priority, fact priority, traceability chain, and Stop-Line Report rules.
- Upgraded `/sdc:init` to generate `.sdc/constitution.md`, current tasks, reports, and templates for bug, impact, repo analysis, and stop-line reports.
- Upgraded `/sdc:spec`, `/sdc:plan`, `/sdc:apply`, `/sdc:validate`, `/sdc:check`, `/sdc:archive`, and `/sdc:harness` to preserve `SCN -> REQ -> AC -> T### -> evidence` traceability.
- Extended `/sdc:check` with delivery, bug, impact, and repo/brownfield modes without adding new public commands.
- Added documentation for the v1.1 discipline core and updated README usage expectations.
- Included docs, security, privacy, and changelog files in local plugin copies created by the installer.

## 1.0.9

- Added Claude Code compatible `.claude/skills/` layout generation during install.
- Updated Claude plugin manifest to point to `./.claude/skills/` and `./commands/`.
- Renamed Claude command files to namespace-friendly names such as `commands/init.md`, producing `/sdc:init`.
- Added one-command uninstall support through `npx sdc-spec@latest uninstall`.
- Improved Codex and Claude installer cleanup behavior for stale local plugin copies.
- Documented Codex custom slash command limitation and Claude Code restart requirement.

## 1.0.8

- Added a valid Claude Code marketplace manifest.
- Updated Claude plugin metadata to current manifest schema.
- Installed SDC through Claude Code local marketplace flow.
- Added command files for Claude plugin namespace behavior.

## 1.0.7

- Added Codex local marketplace and plugin cache installation.
- Added Codex command files and plugin metadata.
- Synchronized SDC skills into Codex-discoverable skill locations.

## Earlier

- Introduced SDC core skills: init, change, spec, plan, apply, check, validate, review, test, quality, archive, and harness.
- Added `.sdc/` workspace initialization workflow.
- Added project standards generation under `.sdc/standards/`.
