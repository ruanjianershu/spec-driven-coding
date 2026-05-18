# Changelog

All notable changes to SDC are documented here.

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
