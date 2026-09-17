# Official Marketplace Submission Notes

This document prepares SDC for submission to the Claude plugin directory and, later, other official plugin marketplaces.

For Claude Code specific marketplace behavior, install commands, and user-facing slash command expectations, see `docs/claude-code-marketplace.md`.

## Short Description

SDC is a lightweight spec-driven coding workflow for Claude Code. It uses role prompt contracts, requires intake confirmation before creating change files, keeps unresolved requirements in minimal draft discovery artifacts, resolves exactly one active change, carries a seven-state local lifecycle, generates deterministic apply/check context manifests, keeps memory recall local and Candidate-only, runs delivery checks, archives stable specs, and compacts durable project knowledge in local files.

## Long Description

SDC packages a complete spec-driven development lifecycle into a small set of Claude Code commands and skills:

- initialize a `.sdc/` workspace
- create local product knowledge, technical knowledge, and memory candidate areas
- use shared English role prompt contracts for expert behavior, evidence rules, and output discipline
- create structured requirement changes
- require intake confirmation before creating change files, then continue Discovery Gate with minimal draft artifacts when needed
- forbid write-ahead confirmation patterns such as "if wrong, tell me and I will update now"
- brainstorm and confirm high-impact product or technical decisions
- build project cognition for brownfield repositories
- analyze legacy change impact after requirements are confirmed
- turn requirements into traceable `SCN -> REQ -> AC -> task -> evidence` plans
- execute implementation tasks incrementally
- preflight plans, carry exact global constraints and task interfaces, and exchange large task/review inputs through local files
- advance the local lifecycle through `intake`, `discovery`, `confirmed`, `planned`, `applying`, `checking`, and `archivable`
- resolve exactly one active change from an explicit argument, environment selector, session pointer, or sole active directory, stopping on invalid or ambiguous input
- generate deterministic `apply-context.jsonl` and `check-context.jsonl` manifests from the final plan while retaining the human-readable context pack
- recall only allowlisted local memory as bounded, read-only `Candidate` results that cannot override confirmed knowledge
- route research scratch, citations, and durable candidates internally through existing stages without adding a public command
- return separate Spec Compliance and Code Quality verdicts from one read-only task review, then run one final whole-change review
- run combined validation, review, test, quality, bug, impact, and repo checks
- archive completed changes into stable project specs
- run Knowledge Compact Gate to recommend durable updates to product knowledge, technical knowledge, memory, decisions, standards, reports, AGENTS.md, project context, or project cognition
- generate project-level AI guardrails

The plugin is intentionally narrow. It does not add external services, network integrations, MCP servers, telemetry, or background processes. Claude may use an optional local `SessionStart` adapter; failure or absence falls back to normal command execution.

## Codex Portal Package

SDC also ships a Codex-native marketplace manifest at `.agents/plugins/marketplace.json`. Default generated Codex packages use the portable skill adapter with no native hook enabled. `SDC_CODEX_HOOKS=1` explicitly packages the separate Codex `SessionStart` adapter for supported clients; trust is reviewed in the client. Source installs suppress automatic Claude hook discovery with `hooks: []`.

Build the portal artifact from a clean worktree:

```bash
npm run package:codex -- --output /tmp/sdc-codex-plugin.zip
```

The archive is rootless and contains only the Codex manifest, generated public and advanced skills, runtime handoff helpers, the SDC CLI, and required project/license documents. The packager normalizes timestamps, preserves executable modes, writes a SHA-256 file, and rejects dirty release builds by default.

## Claude Code Commands

```text
/sdc
/sdc:init
/sdc:change
/sdc:plan
/sdc:apply
/sdc:check
/sdc:archive
/sdc:harness
```

Advanced skills are available for users who need finer control. They are not part of the default public slash-command set:

```text
sdc-spec
sdc-implement
sdc-review
sdc-test
sdc-quality
sdc-validate
```

## Intended Audience

SDC is for developers and teams who want a repeatable AI-assisted development lifecycle without adopting a large toolchain.

It is especially useful for:

- solo developers who want lightweight spec discipline
- teams using Claude Code for implementation work
- projects that want requirement history and acceptance criteria stored in-repo
- teams that want AI coding guardrails without custom infrastructure

## Safety and Privacy Position

SDC is local-first. It combines skills and prompts with deterministic local CLI/helper scripts; it does not run a service or upload project data by itself.

- No telemetry
- No analytics
- No external service dependency
- No MCP server
- Optional local Claude `SessionStart` adapter with safe manual fallback
- Portable Codex adapter by default; explicitly opted-in native hooks still require client trust and retain safe fallback
- Limited local credential detection and redaction; no credential storage or transmission
- No background process
- No project data upload by SDC itself

The plugin may guide the host AI tool to read or write project files when the user asks it to perform development work.

## Why This Belongs in the Marketplace

SDC bundles a coherent end-to-end workflow rather than a single prompt. It gives Claude Code a reusable development lifecycle with clear artifacts, evidence gates, and completion criteria.

It is complementary to existing coding plugins:

- It does not replace source control, issue trackers, or language tools.
- It focuses on planning, implementation discipline, and delivery evidence.
- It keeps workflow state in local project files so users can inspect, edit, and version it.

## Review Checklist

Before submitting:

- Run `node scripts/audit-release.mjs`
- Run `python3 evals/sdc-flow/run_sdc_flow.py`
- Build the rootless Codex portal package twice and confirm matching SHA-256 values
- Run `claude plugin validate --strict .` so the Git-hosted marketplace source is independently installable
- Run `node bin/install.js`, then `claude plugin validate --strict "$HOME/.claude/plugins/marketplaces/sdc-local"`
- Run `npm pack --dry-run`
- Run `node bin/install.js uninstall`
- Run `node bin/install.js`
- Confirm `/sdc:init` appears after Claude Code reload
- Confirm `npx sdc-spec@latest uninstall` removes local SDC state
- Confirm `SECURITY.md`, `PRIVACY.md`, and `CHANGELOG.md` are current
- Tag a GitHub release for the submitted version

## Proposed Official Marketplace Entry

Suggested plugin name:

```text
sdc
```

Suggested category:

```text
development
```

Suggested tags:

```text
spec-driven-coding, ai-coding, tdd, code-review, quality, development-workflow
```

Suggested one-line summary:

```text
Lightweight spec-driven coding workflow for Claude Code.
```

Suggested install command after acceptance:

```text
/plugin install sdc@claude-plugins-official
```

## Submission Links

Use the official Anthropic submission forms:

- Claude.ai: https://claude.ai/settings/plugins/submit
- Console: https://platform.claude.com/plugins/submit
