# Security Policy

## Scope

SDC is a prompt-only development workflow plugin. It provides skills and slash commands for spec-driven coding, project standards, implementation planning, delivery checks, and change archiving.

The package does not include MCP servers, background services, telemetry, network clients, credential handlers, browser automation, or persistent daemons.

## Permissions and Data Access

SDC skills may ask the AI coding assistant to read and write files in the active project workspace, especially:

- `.sdc/`
- `AGENTS.md`
- project source files affected by a requested change
- test files and documentation files relevant to the requested change

SDC does not intentionally access secrets, credentials, private keys, browser profiles, email, calendars, payment data, or external services.

## Network Behavior

SDC itself does not make network requests during normal skill execution.

The `npx sdc-spec@latest` installer uses npm distribution and may call local plugin managers such as `claude plugin` to register local marketplaces. It does not upload project data.

## Reporting Vulnerabilities

Please report security issues through GitHub issues or by contacting the maintainer listed in `package.json`.

When reporting, include:

- affected SDC version
- affected host tool, for example Claude Code or Codex
- reproduction steps
- expected and actual behavior
- any relevant logs with secrets removed

## Security Commitments

SDC should remain:

- prompt-first and auditable
- free of telemetry by default
- free of hidden network calls
- explicit about installer-side configuration changes
- easy to uninstall

