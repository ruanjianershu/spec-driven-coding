# Claude Code Marketplace

SDC is designed to be submitted to the Claude plugin directory and used from Claude Code as a namespaced plugin.

## Current Distribution

Before SDC is accepted into the official marketplace, users can install it through npm or a local marketplace:

```bash
npx sdc-spec@latest
```

or from a cloned repository:

```bash
claude plugin marketplace add "$(pwd)" --scope user
claude plugin install sdc@sdc-local --scope user
```

After installation, restart Claude Code or run `/reload-plugins` when available.

## Official Marketplace Usage

After SDC is accepted into the official Claude Code marketplace, users should be able to install it with:

```text
/plugin install sdc@claude-plugins-official
```

Then reload plugins and use:

```text
/sdc:init
/sdc:change
/sdc:plan
/sdc:apply
/sdc:check
/sdc:archive
/sdc:harness
```

## Why Slash Commands Work in Claude Code

Claude Code plugins namespace commands and skills by plugin name.

SDC's plugin name is `sdc`, and its command files use short names:

```text
commands/init.md
commands/change.md
commands/plan.md
commands/apply.md
commands/check.md
commands/archive.md
```

This produces user-facing Claude Code commands such as:

```text
/sdc:init
/sdc:change
/sdc:plan
```

SDC also generates a `.claude/skills/` compatibility layout during install so Claude Code versions that scan that path can load the same capabilities.

## Marketplace Submission Positioning

Use this concise description when submitting:

> SDC is a lightweight spec-driven coding workflow for Claude Code. It uses role prompt contracts, requires intake confirmation before creating change files, captures changes, analyzes legacy impact after requirements are confirmed, preserves SCN/REQ/AC traceability, confirms high-impact decisions, applies tasks, runs delivery checks, and archives stable specs in local project files.

Use this longer description when a form allows more context:

> SDC packages a complete spec-driven development lifecycle into a small set of Claude Code commands and skills. It creates a local `.sdc/` workspace for specs, changes, standards, decisions, and reports; uses shared English Role Prompt Contracts for expert behavior, evidence rules, and output discipline while keeping each SKILL.md compact; requires Mandatory Change Intake Gate before creating change files; continues Discovery Gate for unresolved requirements before confirmed specs; creates project cognition for brownfield repositories; runs Change Impact Gate after legacy requirements are confirmed; preserves `SCN -> REQ -> AC -> task -> evidence` traceability; uses consent gates so high-impact AI suggestions do not become silent defaults; applies changes incrementally; runs combined validation, review, test, quality, bug, impact, and repo checks; and archives completed changes into stable project specs. SDC is local-first and prompt-only: it ships no MCP server, no telemetry, no background daemon, no default hooks, and no external service dependency.

## Review Notes

For official review, emphasize:

- prompt-only workflow plugin
- no telemetry or analytics
- no external service integration
- no MCP server or background process
- no default hooks
- local project artifacts only
- explicit uninstall command
- commands are scoped to a spec-driven development lifecycle
- discipline core is documented in `docs/sdc-discipline-core.md`

## Pre-Submission Checks

```bash
node --check bin/install.js
claude plugin validate .
npm pack --dry-run
```

Also test:

```bash
node bin/install.js uninstall
node bin/install.js
claude plugin list
```

Expected result:

```text
sdc@sdc-local
Version: <current version>
Status: enabled
```
