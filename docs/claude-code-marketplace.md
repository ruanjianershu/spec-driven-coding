# Claude Code Marketplace

SDC is designed to be submitted to the Claude plugin directory and used from Claude Code as a namespaced plugin.

## Current Distribution

Before SDC is accepted into the official marketplace, users can install it through npm:

```bash
npx sdc-spec@latest
```

from a cloned repository:

```bash
node bin/install.js
```

or directly as a Git-hosted Claude marketplace:

```text
/plugin marketplace add ruanjianershu/spec-driven-coding
/plugin install sdc@sdc-local
```

The repository root is a valid marketplace source. Its manifest explicitly lists only the six advanced `skills/sdc-*` directories. Under Claude's marketplace-root rule, these specific paths replace the default `skills/` scan, so the public workflows remain slash commands and are not registered a second time as skills. The same source tree remains usable by Codex/Hermes.

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
commands/harness.md
commands/sdc.md
```

This produces user-facing Claude Code commands such as:

```text
/sdc:init
/sdc:change
/sdc:plan
```

The Claude manifest explicitly exposes advanced non-public capabilities such as `skills/sdc-spec/`, `skills/sdc-review/`, and `skills/sdc-validate/`. Public workflows such as init, change, plan, apply, check, archive, harness, and the main SDC entry are exposed only through slash commands, so users do not see duplicate entries like `sdc:apply` and `sdc:sdc-apply`.

## Marketplace Submission Positioning

Use this concise description when submitting:

> SDC is a lightweight spec-driven coding workflow for Claude Code. It uses role prompt contracts, requires intake confirmation before creating change files, keeps unresolved requirements in minimal draft discovery artifacts, separates product knowledge from technical knowledge, analyzes legacy impact after requirements are confirmed, preserves SCN/REQ/AC traceability, confirms high-impact decisions, applies tasks from a short context pack, runs delivery checks, archives stable specs, and compacts durable project knowledge in local files.

Use this longer description when a form allows more context:

> SDC packages a complete spec-driven development lifecycle into a small set of Claude Code commands and skills. It creates a local `.sdc/` workspace for specs, changes, product knowledge, technical knowledge, memory candidates, standards, decisions, and reports; requires confirmed intake and discovery before execution; preserves `SCN -> REQ -> AC -> task -> evidence` traceability; carries an evidence-gated seven-state lifecycle; generates deterministic apply/check context manifests; keeps recall local, read-only, and Candidate-only; analyzes brownfield impact; applies reviewed task slices; runs delivery checks; and compacts durable knowledge at archive. SDC ships no MCP server, telemetry, background daemon, or external service dependency. Its optional local Claude `SessionStart` adapter has a safe manual fallback.

## Review Notes

For official review, emphasize:

- local-first skills workflow with deterministic local helpers
- no telemetry or analytics
- no external service integration
- no MCP server or background process
- optional local Claude `SessionStart` adapter with safe manual fallback
- local project artifacts only
- explicit uninstall command
- commands are scoped to a spec-driven development lifecycle
- discipline core is documented in `docs/sdc-discipline-core.md`

## Pre-Submission Checks

```bash
node scripts/audit-release.mjs
node --check bin/install.js
claude plugin validate --strict .
node bin/install.js
claude plugin validate --strict "$HOME/.claude/plugins/marketplaces/sdc-local"
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
