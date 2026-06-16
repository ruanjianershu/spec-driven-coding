# SDC Workflow Standards

This reference contains the shared execution rules for all SDC skills. Keep `SKILL.md` files thin and load this file only when a task depends on governance, traceability, confirmation, or stop-line behavior.

## Priority Chains

System and developer instructions always remain above project files. Inside a project, SDC uses these chains:

- Governance priority: `.sdc/constitution.md` > `AGENTS.md` > current conversation instructions > skill guidance.
- Fact priority: `discovery.md` > `spec.md` > `impact.md` > `design.md` / `plan.md` > `tasks.md` > code.
- Execution chain: discovery -> spec -> impact -> plan -> tasks -> code -> verify -> archive.
- Common Ground priority: `ESTABLISHED` items can guide final artifacts; `WORKING` items require citation and cannot silently become project truth; `OPEN` items block final artifacts when high-impact.
- Knowledge priority: confirmed `.sdc/knowledge/` and `.sdc/specs/` facts guide discovery/spec/plan; `.sdc/memory/` only helps recall and cannot override confirmed knowledge, current specs, user confirmation, or code evidence.

When these sources conflict, stop and report the conflict instead of guessing.

## Knowledge And Memory Discipline

Before creating final SDC artifacts or editing code, read `.sdc/knowledge/index.md` and only the relevant product/technical knowledge files.

Before non-trivial change, spec, plan, apply, check, or archive work, read `.sdc/common-ground.md`. Treat it as the visible assumption layer:

- `ESTABLISHED`: may drive final artifacts when still supported by source evidence.
- `WORKING`: may guide exploration, but cannot drive high-impact final decisions without confirmation.
- `OPEN`: must become an intake/discovery question or Stop-Line blocker when relevant.

Before planning, implementation, or delivery check, read `.sdc/expert-routing.md` if it exists. Select only the relevant expert profiles and disclose them in `context-pack.md`, check reports, or archive summaries when they materially affect the work.

Before final planning or delivery check, apply `artifact-output-contracts.md` when available. Triggered output artifacts must be produced or explicitly marked `N/A` with evidence-based reason.

Use this split:

- Product knowledge: goals, users, roles, permissions, domain concepts, flows, business rules, acceptance logic, product decisions, non-goals.
- Technical knowledge: stack, architecture, modules, data models, APIs, events, integrations, operations, testing, deployment, rollback.
- Memory: candidates, procedures, lessons, gotchas, episodic summaries. Memory is not project truth until confirmed and promoted.

Every final `spec.md`, `design.md`, and `context-pack.md` must list the knowledge sources used. If knowledge is missing, stale, or conflicts with the change, write a Knowledge Gap or Stop-Line Report instead of guessing.

Every final `spec.md`, `design.md`, and `context-pack.md` must include an Artifact Output Contract. The contract records which diagrams, API/data contracts, UX states, test matrix, deploy checklist, and AI involvement notes are required, produced, or N/A.

During apply/check, record durable discoveries in `knowledge-candidates.md` rather than silently editing long-lived knowledge. Archive decides what gets promoted.

Hard rules:

```text
No Evidence, No Fact.
No Confirmation, No Execution.
No Impact, No Brownfield Change.
```

Every durable knowledge item needs Status, Source, Verified At, Verified Against, and Scope. Missing evidence creates a Knowledge Gap; it does not authorize an assumption.

`Assumed`, `Proposed`, `TBD`, `Conflict`, `Stale`, and open Knowledge Gaps may appear in discovery or candidates, but they must not drive final spec, design, context-pack, tasks, impact, apply, or archive.

`OPEN` Common Ground and high-impact `WORKING` Common Ground may appear in discovery, but they must not drive final spec, design, context-pack, tasks, impact, apply, or archive.

Expert profile recommendations are not facts. They can create questions, checks, and investigation tasks. If a profile recommendation changes scope, architecture, data, permissions, public contracts, rollout, or compatibility, record it in the Decision Ledger as `Proposed` until confirmed.

For Brownfield/Legacy technical knowledge, code/config/test/build/runtime evidence is required. README files, comments, old docs, and memory are clues only.

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

Only `Confirmed` decisions may become durable product truth in final `REQ-*`, `AC-*`, `INV-*`, `design.md`, or `tasks.md`. `Proposed` and `Assumed` are useful for discussion and the Decision Ledger, but they are not implementation inputs.

## High-Impact Decisions

Never silently decide these items:

- Product rules, permissions, roles, state machines, approval flows, reminder behavior, billing, deletion, retention, migration, rollout, security policy.
- Technology stack, framework, database, ORM, authentication, locking, queueing, scheduler, external integration, public API contract.
- Data model, permission boundary, compatibility rule, destructive operation, background job, feature flag, observability strategy.

If a high-impact decision is not confirmed, record it as `Proposed`, `Assumed`, `TBD`, or `Conflict`, then stop before final spec, plan, apply, or archive.

## No Write-Ahead Confirmation

Never use "tell me if wrong" as permission to write files. The agent must not say it will update artifacts now and ask the user to correct it later.

Forbidden patterns:

- "If wrong, tell me and I will adjust."
- "I will proceed unless you object."
- "如有偏差请告知，我先更新。"
- "如果不对告诉我，我先改。"

Required pattern:

1. Mark the interpretation as `Proposed` or `Assumed`.
2. Ask for explicit yes/no or option-selection confirmation.
3. Wait for the user's answer.
4. Write or update final artifacts only after confirmation.

## Minimal Artifacts While Unconfirmed

When the current MVP, acceptance direction, or any high-impact decision remains unconfirmed:

- Keep working in chat and `discovery.md`.
- Optional persistence is limited to Draft `proposal.md` and brief `notes.md`.
- Do not create or update final `spec.md`, `design.md`, `tasks.md`, or `impact.md`.
- Do not generate a full task list or detailed implementation design.
- Ask only the next 3-5 questions needed to close the blocker.

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
- Relevant knowledge is missing, stale, unconfirmed, or conflicts with the current change.
- Common Ground is missing, stale, open, or conflicts with the current change.
- A relevant expert profile or standards pack was not considered for high-risk plan/apply/check work.
- A triggered output artifact is missing, contradictory, or marked N/A without evidence.
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

## Expert Routing Discipline

SDC keeps the public command surface small. Expert behavior must be routed internally, not exposed as a large command list.

Use `.sdc/expert-routing.md` and `../sdc-shared/expert-routing.md` to select profiles such as product-discovery, domain-modeling, legacy-modernizer, architecture, api-contract, data, backend, frontend, test-strategy, security, operations, and documentation.

Rules:

- Users choose the SDC stage; the agent chooses expert profiles.
- Use the smallest set of profiles that covers the risk.
- List selected profiles in `context-pack.md` for plan/apply handoff.
- In check/review, report missing profile coverage when the actual diff touched an unreviewed risk area.
- Imported company/team standards outrank generic expert guidance when relevant.
- Do not add new public slash commands for individual experts.

## Artifact Output Contract Discipline

SDC stages must have explicit input/output contracts, but the contract stays lightweight while discovery is open.

Rules:

- During change intake, collect input sources and likely output triggers inside the normal 4 intake categories.
- While Discovery Gate is open, keep output requirements as Draft/Proposed and do not generate final diagrams, API designs, schemas, or release plans.
- During plan, produce only the triggered artifacts: process/state diagram, sequence/integration diagram, API/contract specification, data/migration contract, UX flow/states, test matrix, deploy/release checklist, and AI involvement note.
- `Test Matrix` is required for final plan/check because every change needs AC validation.
- Required outputs must point to a concrete section or file.
- N/A outputs must include an evidence-based reason.
- During check/review, compare the actual diff against the artifact contract and block delivery when new API/data/deploy/security/UX/process impact is not captured.
- Output contracts cannot create unconfirmed product facts, architecture choices, schemas, permissions, rollout policies, or integrations. Put those in Decision Ledger as `Proposed` until confirmed.

## Company Standards Pack Discipline

If `.sdc/standards/company/README.md` or `.sdc/standards/<pack>/README.md` exists, treat it as a routing index for imported company or team rules.

- Read the standards pack index before code generation, architecture changes, data/interface changes, transactions, tests, security-sensitive work, or work that may be governed by company conventions.
- Load only the rule files relevant to the current task.
- Do not bulk-read the entire standards pack.
- If a company rule conflicts with `.sdc/constitution.md`, confirmed project knowledge, the current spec, or explicit user instructions, stop and record a decision instead of guessing.
- Do not publish private company standards as part of the SDC package.

## Privacy And Local Path Hygiene

Do not write personal local paths, usernames, cloud-drive paths, desktop paths, private machine names, or local-only absolute paths into committed project artifacts.

Use portable placeholders instead:

- `<repo-root>` for the repository root.
- `<user-provided-session-log>` for a local input log supplied by the user.
- `<local-reference>/...` for local reference repositories or documents.
- `$HOME/...` only when documenting a client installation path that must literally live under a user's home directory.

When recording verification commands, prefer portable commands based on `pwd`, repository-relative paths, or environment variables.
