# Changelog

All notable changes to SDC are documented here.

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
