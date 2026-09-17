# Security Policy

## Scope

SDC is a prompt-first development workflow with a small local runtime helper. It provides skills, slash commands, lifecycle state, context manifests, Candidate recall, optional client session context, measured delivery evidence, and change archiving.

The package does not include MCP servers, background services, telemetry, browser automation, credential handlers, network clients, or persistent daemons.

## Local Trust Boundary

SDC may read and write the active project workspace, especially `.sdc/`, `AGENTS.md`, relevant source and test files, and requested documentation. Runtime session pointers, research scratch, and bounded evidence records stay under git-ignored `.sdc/runtime/`.

Writable SDC paths must remain inside the current repository. The runtime and public CLI reject unsafe IDs, path traversal, and symbolic links in SDC workspace paths. Lifecycle transitions validate source provenance and required artifacts before mutation; `checking`, `archivable`, and archive operations also enforce task and review gates.

`evidence run` executes a user-authorized command with host permissions; it is not a sandbox. Use disposable fixtures, no production credentials, and an appropriate host sandbox. Receipts bind actual exit status and source hashes; reviewer attribution is caller-declared, not authenticated identity or tamper-proof attestation. Stronger assurance requires independent CI/reviewer controls.

The optional Claude hook prefers the `SessionStart` payload session identifier. An ambient `SDC_SESSION_ID` is ignored unless `SDC_ALLOW_ENV_SESSION_ID=1` explicitly enables that fallback. Session pointers require their full schema, timestamp, source, and active change.

## Secrets And Evidence

SDC does not intentionally seek credentials, private keys, browser profiles, email, calendars, payment data, or unrelated private files. Recall is restricted to allowlisted SDC Markdown roots.

The runtime rejects or redacts common credential-shaped values, authorization headers, private-key markers, and high-entropy values before returning recall excerpts or persisting command evidence and summaries. These checks are defense in depth and are not a substitute for a dedicated secret scanner. Users should remove secrets from project files and logs before invoking an AI coding tool.

## Network Behavior

SDC metadata operations make no network requests. An explicitly executed validation command or real-agent evaluation uses the host tool's permissions and may access the network. Installers may contact npm, Git hosting, Claude Code, or Codex package/plugin services. SDC adds no telemetry or automatic project upload.

## Reporting Vulnerabilities

Report security issues through the repository security channel or the maintainer listed in `package.json`. Include the affected SDC version, host tool, reproduction steps, expected and actual behavior, and logs with secrets removed.

## Security Commitments

SDC should remain auditable, telemetry-free by default, explicit about local data and installer changes, fail-closed at workspace and lifecycle boundaries, and easy to uninstall.
