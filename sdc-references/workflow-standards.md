# SDC Workflow Standards

This reference contains the shared execution rules for all SDC skills. Keep `SKILL.md` files thin and load this file only when a task depends on governance, traceability, confirmation, or stop-line behavior.

## Priority Chains

System and developer instructions always remain above project files. Inside a project, SDC uses these chains:

- Governance priority: `.sdc/constitution.md` > `AGENTS.md` > current conversation instructions > skill guidance.
- Fact priority: `discovery.md` > `spec.md` > `impact.md` > `design.md` / `plan.md` > `tasks.md` > code.
- Execution chain: discovery -> spec -> impact -> plan -> tasks -> code -> verify -> archive.
- Runtime lifecycle: `intake -> discovery -> confirmed -> planned -> applying -> checking -> archivable`. Advance one boundary only after its durable content gates pass. Same-state retries are idempotent only while evidence is valid. Changed governing inputs require explicit reasoned reopen to discovery or confirmed, preserved history, and fresh affected approvals; they never silently reapprove delivery. `checking` requires completed tasks and approved task reviews; `archivable` also requires approved final whole-change review and current validation receipts. See `runtime-context.md` for mechanics.
- Common Ground priority: `ESTABLISHED` items can guide final artifacts; `WORKING` items require citation and cannot silently become project truth; `OPEN` items block final artifacts when high-impact.
- Knowledge priority: confirmed `.sdc/knowledge/` and `.sdc/specs/` facts guide discovery/spec/plan; `.sdc/memory/` only helps recall and cannot override confirmed knowledge, current specs, user confirmation, or code evidence.

When these sources conflict, stop and report the conflict instead of guessing.

Active-change resolution must select exactly one valid, non-symlink directory using explicit argument, `SDC_ACTIVE_CHANGE`, valid session pointer, then sole active directory. Invalid higher-priority selectors, zero candidates, or multiple candidates stop; directory recency is never authority.

## Risk-Proportionate Policy

This is the authoritative internal effort policy. Load it when classifying a change, revising risk, or deciding context/review/test scope. It adds no public commands or permission overrides.

| Level | Triggers | Proportionate execution |
| --- | --- | --- |
| light | All apply: confirmed narrow scope, isolated and locally reversible edits, known impact, no business behavior, persistent data, permissions/security, public contract, architecture, or deployment change. Examples: behavior-neutral wording or a local mechanical correction with evidence. | One coherent task may suffice; affected sources and focused validation, concise contracts, one final-snapshot review may cover task and whole-change verdicts. |
| standard | Confirmed routine implementation within existing architecture/contracts, bounded module-level impact, and no strict trigger. Also the minimum when technical impact is not yet established. | Focused impact analysis, coherent dependency-ordered tasks, affected behavior/regression tests, independent task review and final integration review. |
| strict | Any security/permission boundary, sensitive data, billing, deletion/retention/migration, destructive or hard-to-reverse operation, public contract/compatibility, architecture/stack decision, production rollout, or broad cross-service/shared-infrastructure impact. | Explicit authoritative decision evidence, affected specialist standards, failure/compatibility checks, migration/rollback evidence when relevant, and review proportional to blast radius. |

- Record level, matched triggers, evidence, authorization, context scope, validation/review scope, and why this is sufficient in discovery/notes, then `context-pack.md` and check evidence. Keep the rationale visible to the user.
- Use the highest applicable level. Unclear technical impact requires focused investigation; plausible strict impact stays strict until resolved. Unknown business scope or acceptance stays in discovery regardless of level.
- Escalate visibly when new evidence triggers higher risk. Never silently downgrade: a lower level requires new evidence, recorded rationale, and explicit user approval; it cannot remove a governing project gate.
- All levels preserve the same semantic acceptance: confirmed requirements, traceability, applicable output contracts, Brownfield impact, current evidence, independent read-only review, final whole-change review, and consent. Scale breadth and repetition, not correctness.
- New confirmed behavior-neutral prose edits may use `compact-workflow.md`: one canonical compact record, the same lifecycle and fresh evidence, no mandatory full init. Other light work and all existing standard changes keep the standard schema. Eligibility is narrower than the light risk tier; a Markdown filename alone is not proof. Do not claim token savings without actual-client measurements.
- No arbitrary full-repository read, expert count, task count, or repeated test/review loop is mandatory. One focused pass can serve multiple gates when its scope and source snapshot cover each; record each required verdict and AC mapping. Re-run for changed inputs, missing coverage, or a named unresolved risk.

## Authorization Boundaries

The four intake categories are coverage obligations, not four new questions. Cite current or still-valid prior user/project confirmation and ask only missing blocking questions. A missing irrelevant preference is not a blocker; record why it does not affect this scope.

Bounded authorized reversible actions may proceed without asking again. Record the approving source, allowed action, scope, constraints, and stopping condition. Confirmation of a requirement is not blanket permission to deploy, delete, publish, change permissions, or write unrelated files.

Scope, data, permissions, public contracts, architecture, and other high-impact decisions need authoritative confirmation or bounded explicit delegation before execution. Delegation must identify the decision area, allowed options/constraints, impact limits, and stop/escalation boundary. Record the selected option and its source in the Decision Ledger; it is confirmed only within that delegation. Generic "use your judgment" cannot fill unknown business requirements or grant blanket consent. Model confidence, current code, and memory cannot authorize new business policy.

## Selective Context And Freshness

Load binding governance and short indexes once, then use stage-specific context. Reuse already-loaded sources only while their recorded identity and scope remain current.

| Stage | Necessary context | Expand only when |
| --- | --- | --- |
| init | Project entrypoints, configuration/build evidence, existing indexes | A missing/stale map section prevents routing |
| change | User request, cited confirmation, relevant Common Ground and knowledge entries | A blocking category, business rule, or output trigger is unresolved |
| plan | Confirmed spec, affected impact, relevant standards/knowledge | A design interface or risk lacks evidence |
| apply | Verified apply manifest, context-pack, current task, binding constraints and affected code | Changed inputs or a named dependency/risk require more context |
| check | Verified check manifest, final diff, AC mapping, review and validation receipts | Missing coverage, drift, or a concrete failure requires investigation |
| archive | Final checked artifacts, candidates and affected source entries | A proposed durable update needs source verification |

Freshness is source identity and applicability, not date alone. Use Status, Source, Verified At, Verified Against (revision/hash or authoritative confirmation), and Scope. Compare affected source bytes/contracts, dirty and relevant untracked files, and approval scope before reuse. A fresh timestamp does not cure a changed source; an old timestamp alone does not invalidate unchanged evidence.

Refresh affected source evidence within existing read authority; do not ask for permission to repeat an authorized read. Record drift and candidates locally, invalidate affected approvals/manifests, and use explicit reopen when governing inputs change. Unrelated changes do not justify blanket knowledge-base rereads. Durable knowledge edits/promotions still require explicit confirmation of content and destination. Conflicting authority or unresolved business meaning blocks dependent work.

## Knowledge And Memory Discipline

Before creating final SDC artifacts or editing code, read `.sdc/knowledge/index.md` and only the relevant product/technical knowledge files.

Before non-trivial change, spec, plan, apply, check, or archive work, read `.sdc/common-ground.md`. Treat it as the visible assumption layer:

- `ESTABLISHED`: may drive final artifacts when still supported by source evidence.
- `WORKING`: may guide exploration, but cannot drive high-impact final decisions without confirmation.
- `OPEN`: must become an intake/discovery question or Stop-Line blocker when relevant.

Before planning, implementation, or delivery check, read `.sdc/expert-routing.md` if it exists. Select only the relevant expert profiles and disclose them in `context-pack.md`, check reports, or archive summaries when they materially affect the work.

Before final planning or delivery check, apply `artifact-output-contracts.md` when available. Triggered output artifacts must be produced or explicitly marked `N/A` with evidence-based reason.

Before final planning, apply `execution-orchestration.md` when available. Plan Preflight, Global Constraints, task interfaces, per-task review fields, file handoffs, progress ledger, and whole-change review are internal stage requirements; they do not add public commands.

Use this split:

- Product knowledge: goals, users, roles, permissions, domain concepts, flows, business rules, acceptance logic, product decisions, non-goals.
- Technical knowledge: stack, architecture, modules, data models, APIs, events, integrations, operations, testing, deployment, rollback.
- Memory: project, personal, native-client, or cross-device recall, procedures, lessons, and episodic summaries are Candidate context. Memory is not project truth until verified against authoritative sources and explicitly confirmed for promotion. Do not write personal/cross-device memory without the user's explicit request.

Every final `spec.md`, `design.md`, and `context-pack.md` must list the knowledge sources used. If knowledge is missing, stale, or conflicts with the change, write a Knowledge Gap or Stop-Line Report instead of guessing.

Every final `spec.md`, `design.md`, and `context-pack.md` must include an Artifact Output Contract. The contract records which diagrams, API/data contracts, UX states, test matrix, deploy checklist, and AI involvement notes are required, produced, or N/A.

During apply/check, record durable discoveries in `knowledge-candidates.md` rather than silently editing long-lived knowledge. Archive decides what gets promoted.

Internal research follows the same boundary: scratch material belongs under `.sdc/runtime/<change-id>/research/`, citations belong in `discovery.md` or `notes.md`, and, after discovery closes, reusable findings belong in `knowledge-candidates.md` as Candidate until archive confirmation.

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
- Completed tasks require acceptance evidence: actual command receipts, scoped manual verification, screenshots, or logs. A reason validation could not run records a limitation, not a pass; required acceptance must still be proved.
- Completed tasks require `Review: Approved` plus durable evidence. `Cannot verify`, `Needs fixes`, missing review, or `Evidence: Pending` cannot be treated as complete.

## Decision States

Use the Decision Ledger for high-impact decisions and unclear assumptions.

| State | Meaning | Can enter final REQ/AC/design/tasks? |
| --- | --- | --- |
| Confirmed | Explicitly confirmed by the user or authoritative project docs, including a choice within recorded bounded explicit delegation | Yes, within the confirmed scope |
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

When existing confirmation or bounded explicit delegation does not cover the action:

1. Mark the interpretation as `Proposed` or `Assumed`.
2. Ask for explicit yes/no or option-selection confirmation.
3. Wait for the user's answer.
4. Write or update final artifacts only after confirmation.

When valid explicit authorization already covers the action, cite it and proceed within its boundaries. Do not re-ask merely because a new stage or session started.

## Minimal Artifacts While Unconfirmed

When the current MVP, acceptance direction, or any high-impact decision remains unconfirmed:

- Keep working in chat and `discovery.md`.
- Optional persistence is limited to Draft `proposal.md` and brief `notes.md`.
- Do not create or update `spec.md`, `design.md`, `tasks.md`, `impact.md`, `context-pack.md`, or `knowledge-candidates.md`, even as speculative drafts.
- Do not generate a full task list or detailed implementation design.
- Ask only missing blocking questions, without a fixed count. Discovery persistence itself requires authorization.

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
- Required Common Ground remains missing, stale, open, or conflicting after focused source checks; unrelated open entries do not block the change.
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
- [ ] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] Implement and verify the confirmed behavior for ...
  - Depends on: none
  - Files: tests/path/to/test_file.py, src/path/to/implementation.py
  - Consumes: confirmed REQ-01 behavior and existing test fixtures
  - Produces: AC-01 behavior and its regression test
  - Verify: <executable command argv>
  - Expected: regression test fails for the intended missing behavior first, then passes after implementation
  - Review: Pending
  - Evidence: Pending
  - Source: .sdc/changes/active/<change-id>/spec.md#AC-01
```

Task rules:

- Use only `Size: S` or `Size: M`.
- Put meaningful behavior tests before the implementation they verify, within the same coherent task where possible. For behavior-neutral changes, record focused validation instead of inventing failing tests.
- Avoid vague verbs such as "optimize", "handle", "improve", or "polish" unless the observable outcome is defined.
- Default to the first deliverable MVP slice; do not generate a huge task list unless explicitly requested.

## Evidence Discipline

SDC conclusions must be evidence-backed:

- Requirement evidence: user statements, confirmed discovery, authoritative documents.
- Brownfield evidence: source files, build files, package manifests, tests, configuration, CI, database scripts, launch scripts, public contracts.
- Delivery evidence: git diff, test/build output, review findings, security findings, manual verification notes.

README files, comments, old docs, and historical notes are clues. They are not confirmed facts unless current code or the user confirms them.

Executable validation uses the bounded internal evidence runner: preserve actual command, exit status, scope, and source snapshot. Final delivery requires the latest fresh passed receipt per completed task with argv exactly matching its Verify command; manual observations supplement rather than replace that receipt. An appended status or an agent's assertion is not an execution receipt. Failed, timed-out, missing, or stale required runs cannot pass. Verify manifests and approval snapshots before using them; preserve invalidated evidence as history, never overwrite it into a new approval. Reuse current evidence only when it still covers the delivered change.

An expected red-phase failure is useful TDD evidence, not a passing delivery receipt. Complete the coherent behavior task with its final green verification before marking it done.

Write final task progress and approved independent review notes before binding the review receipt. Reviewer attribution is not authenticated identity, and receipt capture does not perform review. Verify execution and review receipts together; code edits afterward invalidate affected evidence. Consult `runtime-context.md` for exact internal operations.

## Expert Routing Discipline

SDC keeps the public command surface small. Expert behavior must be routed internally, not exposed as a large command list.

Use `.sdc/expert-routing.md` and `expert-routing.md` to select profiles such as product-discovery, domain-modeling, legacy-modernizer, architecture, api-contract, data, backend, frontend, test-strategy, security, operations, and documentation.
Use the internal research lens when a stage needs external or prior evidence. Research is not a public command; it only routes scratch, citations, and Candidate knowledge.

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

- During change intake, cover input sources and likely output triggers within the four categories using cited confirmations or missing blocking questions.
- While Discovery Gate is open, keep output requirements as Draft/Proposed and do not generate final diagrams, API designs, schemas, or release plans.
- During plan, produce only the triggered artifacts: process/state diagram, sequence/integration diagram, API/contract specification, data/migration contract, UX flow/states, test matrix, deploy/release checklist, and AI involvement note.
- `Test Matrix` is required for final plan/check because every change needs AC validation.
- Required outputs must point to a concrete section or file.
- N/A outputs must include an evidence-based reason.
- During check/review, compare the actual diff against the artifact contract and block delivery when new API/data/deploy/security/UX/process impact is not captured.

## Execution Orchestration Discipline

- Final plan artifacts include exact Global Constraints and `Plan Preflight: Passed`.
- Each coherent task declares Files, Consumes, Produces, Verify, Expected, Review, Evidence, and Source; do not manufacture separate tasks for test setup, edits, or documentation that share one acceptance boundary.
- Use `.sdc/runtime/<change-id>/` for ignored briefs, reports, diff packages, and progress ledger; promote durable evidence into tasks/notes/reports.
- Use a separate read-only reviewer when supported and authorized. Otherwise explicitly separate implementation and skeptical review passes and disclose the isolation limitation. Fresh implementers and a multi-agent swarm are not requirements.
- One task review returns separate Spec Compliance and Code Quality verdicts. Critical/Important findings and acceptance-affecting `Cannot verify` items block completion.
- Controllers must not tell reviewers what to ignore or how to pre-rate a finding.
- Require final whole-change review after all implementation across the complete change range. For a single-task light change, one final-snapshot pass can supply both task and final verdicts; unchanged evidence need not be regenerated at check.
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
