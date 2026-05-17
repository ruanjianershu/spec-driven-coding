# SDC Workflow Standards

This reference contains the shared execution rules for all SDC skills. Keep `SKILL.md` files thin and load this file only when a task depends on governance, traceability, confirmation, or stop-line behavior.

## Priority Chains

System and developer instructions always remain above project files. Inside a project, SDC uses these chains:

- Governance priority: `.sdc/constitution.md` > `AGENTS.md` > current conversation instructions > skill guidance.
- Fact priority: `discovery.md` > `spec.md` > `impact.md` > `design.md` / `plan.md` > `tasks.md` > code.
- Execution chain: discovery -> spec -> impact -> plan -> tasks -> code -> verify -> archive.

When these sources conflict, stop and report the conflict instead of guessing.

## Traceability

Every durable change should preserve this chain:

```text
SCN-* -> REQ-* -> AC-* -> T### -> validation evidence
```

Rules:

- Scenarios use `SCN-*`.
- Requirements use `REQ-*`.
- Acceptance criteria use `AC-*`.
- Tasks use `T###`.
- Tasks must reference at least one `REQ-*` and one `AC-*`.
- Tests and validation notes should reference the relevant `AC-*`.
- Completed tasks require evidence: command output, manual verification notes, screenshots, logs, or explicit reason why validation could not run.

## Decision States

Use the Decision Ledger for high-impact decisions and unclear assumptions.

| State | Meaning | Can enter final REQ/AC/design/tasks? |
| --- | --- | --- |
| Confirmed | Explicitly confirmed by the user or authoritative project docs | Yes |
| Proposed | Suggested option waiting for selection | No |
| Assumed | Temporary working assumption with stated risk | No |
| TBD | Known missing decision | No |
| Conflict | Contradiction between sources | No |
| Deferred | Intentionally postponed and outside the current MVP | Only when it does not affect the current MVP |

## High-Impact Decisions

Never silently decide these items:

- Product rules, permissions, roles, state machines, approval flows, reminder behavior, billing, deletion, retention, migration, rollout, security policy.
- Technology stack, framework, database, ORM, authentication, locking, queueing, scheduler, external integration, public API contract.
- Data model, permission boundary, compatibility rule, destructive operation, background job, feature flag, observability strategy.

If a high-impact decision is not confirmed, record it as `Proposed`, `Assumed`, `TBD`, or `Conflict`, then stop before final spec, plan, apply, or archive.

## No Silent Defaults

Do not convert common practice into project truth.

Examples that must not be silently created:

- "Needs approval" -> specific approvers, timeout rules, or auto-approval behavior.
- "Needs reminder" -> reminder time, channel, audience, or retry policy.
- "Frontend/backend separation" -> Spring Boot, Vue, JWT, MyBatis, or a specific deployment layout.
- "Admin user" -> concrete RBAC matrix.

When a high-impact decision is unconfirmed, offer 2-3 options, mark them as `Proposed`, and ask for confirmation.

## Stop-Line Report

Stop and produce a report when:

- Required SDC artifacts are missing, contradictory, or still templates.
- Requirements, acceptance criteria, high-impact decisions, or impact boundaries are unresolved.
- Implementation requires changing behavior, public contracts, data, permissions, security, architecture, or scope beyond the approved artifacts.
- Validation cannot prove the relevant acceptance criteria.
- Brownfield work lacks a current `impact.md` or exceeds it.

Use this format:

```markdown
## Stop-Line Report
- Trigger:
- Evidence:
- Conflicting files:
- Affected SCN/REQ/AC:
- Options:
- Recommended next step:
```

## Task Format

Use this task shape:

```markdown
- [ ] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] Write a failing behavior test for ...
  - Depends on: none
  - Verify: <command or manual check>
  - Source: .sdc/changes/active/<change-id>/spec.md#AC-01
```

Task rules:

- Use only `Size: S` or `Size: M`.
- Put tests before the implementation tasks they verify.
- Avoid vague verbs such as "optimize", "handle", "improve", or "polish" unless the observable outcome is defined.
- Default to the first deliverable MVP slice; do not generate a huge task list unless explicitly requested.

## Evidence Discipline

SDC conclusions must be evidence-backed:

- Requirement evidence: user statements, confirmed discovery, authoritative documents.
- Brownfield evidence: source files, build files, package manifests, tests, configuration, CI, database scripts, launch scripts, public contracts.
- Delivery evidence: git diff, test/build output, review findings, security findings, manual verification notes.

README files, comments, old docs, and historical notes are clues. They are not confirmed facts unless current code or the user confirms them.

## Privacy And Local Path Hygiene

Do not write personal local paths, usernames, cloud-drive paths, desktop paths, private machine names, or local-only absolute paths into committed project artifacts.

Use portable placeholders instead:

- `<repo-root>` for the repository root.
- `<user-provided-session-log>` for a local input log supplied by the user.
- `<local-reference>/...` for local reference repositories or documents.
- `$HOME/...` only when documenting a client installation path that must literally live under a user's home directory.

When recording verification commands, prefer portable commands based on `pwd`, repository-relative paths, or environment variables.
