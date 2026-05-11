# Privacy Policy

## Summary

SDC does not collect, transmit, sell, or share user data.

SDC is a local plugin and skill pack for AI coding tools. Its files are installed on the user's machine and are interpreted by the host tool, such as Claude Code or Codex.

## Data Processed

When a user invokes SDC, the host AI coding tool may process project files according to that host tool's own behavior and user permissions. SDC itself only provides workflow instructions.

Typical project files created by SDC include:

- `.sdc/specs/`
- `.sdc/changes/`
- `.sdc/standards/`
- `.sdc/reports/`
- `AGENTS.md`

These files remain in the user's project unless the user or their AI tool moves, commits, uploads, or deletes them.

## Telemetry

SDC does not include telemetry, analytics, tracking pixels, remote logging, or background reporting.

## External Services

SDC does not require accounts, API keys, webhooks, cloud services, or external SaaS integrations.

The installer may interact with local package and plugin managers, for example npm, Claude Code, or Codex, to copy files and register local plugin marketplaces.

## Uninstalling

Users can remove SDC with:

```bash
npx sdc-spec@latest uninstall
```

This removes SDC plugin registrations, local marketplaces, plugin caches, and copied SDC skill directories where supported.

