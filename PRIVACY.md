# Privacy Policy

## Summary

SDC processes project context locally. It does not include telemetry, analytics, tracking pixels, remote logging, or background reporting, and it does not sell or share user data.

The host AI coding tool may separately process project files under its own privacy policy, permissions, and network configuration.

## Local Data Processed

SDC skills and its local runtime helper may read these allowlisted project sources when a workflow requires them:

- confirmed governance, knowledge, standards, and active-change Markdown under `.sdc/`
- Candidate recall sources under `.sdc/knowledge/`, `.sdc/memory/`, `.sdc/current/`, and the selected active change
- the selected change's state, context manifests, tasks, notes, and evidence references
- local source bytes to calculate validation snapshots, including dirty and untracked non-ignored files
- a client `SessionStart` payload containing a session identifier, when an optional trusted hook is enabled

SDC may create or update:

- durable project artifacts under `.sdc/changes/`, `.sdc/specs/`, `.sdc/knowledge/`, `.sdc/standards/`, and `.sdc/reports/`
- local state and deterministic context manifests for an active change
- tracked revision archives and delivery receipts containing relative source paths/hashes, command arguments, actual result, timing, and reviewer attribution; not raw output or environment variable values
- git-ignored session pointers, research scratch, and bounded evidence records under `.sdc/runtime/`
- project guidance such as `AGENTS.md` when explicitly requested

Candidate recall is local, read-only, bounded, and non-authoritative. It does not promote memory into confirmed knowledge.

## Sensitive Data

SDC uses best-effort rejection or redaction for common credential formats, authorization headers, private-key markers, and high-entropy values in recall excerpts and runtime evidence. This is not a complete secret scanner. Do not place credentials or private keys in `.sdc/` artifacts, prompts, command summaries, or evidence.

## Storage And Retention

Project artifacts remain until the user edits or deletes them. Git-ignored runtime data also persists locally until it is removed, for example by deleting `.sdc/runtime/` after the related work is complete.

The uninstall command removes SDC plugin registrations, local marketplaces, caches, and copied skill directories where supported. It does not delete project-local `.sdc/` data or `AGENTS.md` because those may contain user-owned records.

## Network Behavior

SDC metadata operations make no network request. Explicit validation commands and real-agent evaluation CLIs use the host's permissions, network, and privacy policy. Evaluation transcripts stay in the chosen local report directory and must be reviewed before sharing. Installation or updates may contact package/plugin services. SDC adds no telemetry or automatic project upload.

## Uninstalling

```bash
npx sdc-spec@latest uninstall
```
