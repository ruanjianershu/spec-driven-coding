# SDC Discipline Core

SDC keeps six public lifecycle entries while making intake, context loading, and verification evidence-governed and proportionate to risk.

The goal is not to copy every OpenSpec, Superpowers, or internal workflow command. The goal is to keep their useful core:

- OpenSpec: change lifecycle, validation, archive.
- Superpowers: lightweight skill-pack distribution.
- Karpathy-style skills and internal workflow practice: think before coding, thin slices, TDD, stop-line reports, evidence over vibes.
- Memory/knowledge-base systems: short indexes, task-focused loading, candidate knowledge, and reviewable archive-time promotion.
- Expert skill libraries: specialist lenses selected internally, without expanding the public command list.

## Public Surface

The six lifecycle commands, or their natural-language equivalents, are:

```text
/sdc:init
/sdc:change
/sdc:plan
/sdc:apply
/sdc:check
/sdc:archive
```

`/sdc` remains the router; `/sdc:harness` remains an optional guardrail utility, not a seventh lifecycle stage. Detailed skills such as `sdc:spec`, `sdc:validate`, `sdc:review`, `sdc:test`, and `sdc:quality` remain available for advanced use and internal routing. Risk policy, reopen, manifests, and receipts add no public commands.

Do not add a separate public compact command. Knowledge compaction is part of `/sdc:archive`.

## Role Prompt Contracts

SDC v1.1.4 adds English Role Prompt Contracts for every skill. The current layout keeps those contracts in `sdc-references/role-contracts.md` so each `SKILL.md` stays short while the agent can still load the exact contract it needs.

Every skill contract uses this shape:

```text
Role
Operating Contract
Evidence Rules
Output Contract
```

These contracts do not add new public commands. They make each existing skill more reliable when loaded by Codex, Claude Code, or another skill-aware agent, while preserving progressive disclosure.

The contract has four goals:

- establish the expert role for the current task.
- prevent unstated assumptions from becoming facts.
- require evidence anchors for conclusions.
- force concrete outputs or Stop-Line Reports instead of generic advice.

## Two Decision Chains

Every SDC workspace should have `.sdc/constitution.md`.

Governance priority:

```text
.sdc/constitution.md > AGENTS.md > conversation instructions
```

Fact priority:

```text
discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code
```

Knowledge priority:

```text
confirmed .sdc/knowledge/ + .sdc/specs/ + .sdc/decisions/ > .sdc/memory/ candidates > AI inference
```

When these sources conflict, the agent should stop and produce a Stop-Line Report instead of guessing.

## Common Ground And Expert Routing

SDC v1.2.1 added two project-level coordination files:

```text
.sdc/common-ground.md
.sdc/expert-routing.md
```

`common-ground.md` makes the agent's hidden assumptions visible:

- `ESTABLISHED` items can drive final artifacts when still supported by evidence.
- `WORKING` items can guide exploration, but cannot silently become project truth.
- `OPEN` items must be clarified before they affect scope, acceptance, data, permissions, architecture, security, rollout, or compatibility.

`expert-routing.md` borrows the useful part of expert skill libraries without creating command sprawl. Users still choose `init/change/plan/apply/check/archive`; the agent internally selects the smallest useful expert profiles, such as product discovery, domain modeling, legacy modernization, architecture, API contract, data, frontend, backend, test strategy, security, operations, or documentation.

Expert profiles may create questions, checks, and investigation tasks. They may not create unconfirmed product facts, architecture choices, data models, permissions, or rollout policies.

`context-pack.md`, check reports, and archive summaries should disclose `Common Ground Used` and `Expert Profiles Used` when those materially affect execution.

## Execution Orchestration

SDC 1.3 keeps orchestration behind `plan`, `apply`, and `check`:

```text
Plan Preflight -> task brief -> implement -> task review -> progress ledger -> final whole-change review
```

Plans carry exact cross-artifact Global Constraints and per-task Files, Consumes, Produces, Verify, Expected, Review, Evidence, and Source fields. Plan Preflight records reviewed sources and closed findings, not only a self-declared status. Large task text, implementer reports, and diffs move through git-ignored files under `.sdc/runtime/<change-id>/` so a coordinating agent does not repeatedly pay for the same context. A WORKTREE review stops when untracked files would be omitted.

Coherent implementation tasks run serially through implement -> review -> durable evidence -> ledger update. Do not split a tiny change into artificial test/edit/review loops. Task review is read-only and returns separate Spec Compliance and Code Quality verdicts backed by durable evidence. Critical/Important findings and acceptance-affecting `Cannot verify from diff` items block completion. Independent reviewer judgment and final whole-change review are required at every risk level. For a single-task light change, one pass over the final snapshot may provide both task and final verdict records; check can reuse unchanged evidence.

Use a separate reviewer context when supported and authorized. Otherwise perform an explicit skeptical role-separated pass and disclose the isolation limitation; do not claim it was external review. Fresh implementers and a multi-agent swarm are not requirements. The runtime ledger supports recovery, while tasks, notes, reports, and archive artifacts preserve durable evidence.

## Internal Risk Policy

The authoritative rules are in [Workflow Standards](../sdc-references/workflow-standards.md#risk-proportionate-policy); consult them when choosing or changing effort, authorization, or context scope.

| Level | Trigger | Effort |
| --- | --- | --- |
| light | Confirmed, narrow, isolated, reversible, behavior-neutral work with known impact and no high-impact boundary change | Affected sources, focused validation, one coherent task when sufficient |
| standard | Routine implementation within existing architecture/contracts, bounded impact, no strict trigger; minimum for unresolved technical impact | Focused impact, affected behavior/regression tests, task and final integration coverage |
| strict | Security/permissions, sensitive data, billing, deletion/retention/migration, destructive actions, public contracts/compatibility, architecture/stack, production rollout, or broad shared/cross-service impact | Authoritative decisions, relevant specialist standards, failure/compatibility and rollback evidence as applicable |

Use the highest applicable level and disclose triggers, evidence, authorization, context scope, and verification rationale. Plausible strict risks remain strict until investigated. Downgrades need new evidence, recorded rationale, and explicit user approval; never silently reduce effort. All levels keep the same semantic acceptance, consent, traceability, impact, output contracts, independent review, and final review. Unknown business requirements remain in discovery at every level.

There is no mandatory full-repository read, expert quota, or repeated test/review loop for small work. Reuse current evidence only when it still covers the delivered change; rerun for changed inputs, missing coverage, or a named unresolved risk.

## Runtime Context And Client Adapters

The Trellis-inspired runtime makes lifecycle and context routing explicit without copying external source code, adding a service, or expanding SDC's public commands.

Design provenance: the comparison used [mindfold-ai/Trellis](https://github.com/mindfold-ai/Trellis) at revision `64e663694201005bc87766ef22de89b8da3d4d79` (AGPL-3.0) as an external conceptual reference for lifecycle visibility, task context, local memory, and client adapters. SDC's implementation was written independently under its own MIT codebase. No Trellis source code or prompt text was copied.

Each active change normally advances through this evidence-gated sequence:

```text
intake -> discovery -> confirmed -> planned -> applying -> checking -> archivable
```

State labels cannot close discovery or bless stale artifacts. Same-state retries are idempotent only while their evidence stays fresh. Use the internal runtime helper to reopen explicitly with a reason: `state reopen --change <id> --state confirmed --reason "<reason>"` permits replanning only with unchanged snapshotted requirements; `--state discovery` reopens changed requirements. Both archive downstream artifacts under `revisions/<id>`, retain history, and invalidate old receipts via a revision nonce. Discovery reopen also archives superseded requirement artifacts. This is not a public lifecycle entry.

The runtime resolves exactly one active change using this precedence: explicit change argument, valid `SDC_ACTIVE_CHANGE`, valid local session pointer, then the sole directory under `.sdc/changes/active/`. An invalid higher-priority selector, zero candidates, or multiple candidates stops execution; modification time is never authority.

After Plan Preflight passes, `plan` generates deterministic `apply-context.jsonl` and `check-context.jsonl` manifests alongside `context-pack.md`. JSONL records contain ordered repository-relative references, sections, purposes, required flags, source types, and current SHA-256 provenance rather than copied file bodies.

`manifest verify --change <id> --role apply|check` verifies exact schema, sources, and hashes before use. Refresh manifests after task/notes progress at safe checkpoints; regeneration does not approve changed requirements. Missing, malformed, or stale required manifests cannot authorize execution.

`evidence run --change <id> --stage apply|check --task T001 --timeout 300 -- <exact Verify argv>` executes bounded validation and captures actual exit status and source snapshot. Delivery requires the latest fresh passed receipt per completed task, exactly matching its Verify argv. Repeated `--task` flags can share a run only for the same argv; shell pipelines must explicitly use `sh -c`. An appended assertion is never proof.

Write last-task progress and final approved independent review notes before `evidence review --change <id> --reviewer "<attribution>"`. It binds those notes/tasks and source snapshots; it does not perform a review or authenticate reviewer identity. Subsequent code changes invalidate it. `evidence verify --change <id>` checks both execution and review receipts. These are internal `python3 scripts/sdc-runtime-context.py` operations; see [Runtime Context](../sdc-references/runtime-context.md) for details.

Memory recall is bounded, deterministic, local, and read-only. It reads only allowlisted project Markdown, excludes runtime payloads and unsafe paths, and labels every result `Candidate`; recall cannot update knowledge, memory, lifecycle state, or Git. Research remains an internal lens of `change`, `plan`, `apply`, and `check`: scratch stays under `.sdc/runtime/<change-id>/research/`, verified citations enter discovery or notes, and reusable findings enter `knowledge-candidates.md` pending archive confirmation.

Supported Claude/Codex packages may use opt-in native hooks for compact, non-authoritative session context. Hooks are never assumed available or enabled. Absent, unsupported, or failed hooks fall back to the portable `session-context` adapter through stage instructions; neither path authorizes execution or promotes memory.

## Project Knowledge And Memory

SDC treats the knowledge base as the project brain, not as a document dump.

`/sdc:init` creates two related but separate assets:

```text
.sdc/knowledge/
├── index.md
├── current.md
├── product/
└── technical/

.sdc/memory/
├── candidates.md
├── procedures.md
└── episodic/
```

The split is intentional:

- Product knowledge answers why the project exists, who uses it, what flows and business rules matter, and what is explicitly out of scope.
- Technical knowledge answers how the system is built, where capabilities live, how data and interfaces work, and how to test, deploy, roll back, or debug it.
- Project, personal, native-client, and cross-device memory record candidates, procedures, lessons, and episodic summaries. Recall is read-only Candidate context and cannot override confirmed project knowledge. Durable promotion needs explicit confirmation of content and destination; cross-device writes need an explicit user request.

Required knowledge states:

| State | Meaning | Can drive implementation |
| --- | --- | --- |
| Confirmed | User-confirmed, archived, decision-backed, or code-evidence-backed technical fact | Yes |
| Candidate | Proposed durable knowledge waiting for archive/user confirmation | No |
| Assumed | Temporary working assumption | No |
| Stale | May be outdated | No |
| Conflict | Contradicts another source | No |
| Deprecated | No longer active | No |

Every non-trivial change should follow this loop:

```text
read knowledge index -> load relevant product/technical knowledge -> create spec/design/context-pack -> apply -> record knowledge-candidates -> archive promotion gate
```

Final `spec.md`, `design.md`, and `context-pack.md` must list Knowledge Sources Used. If relevant knowledge is missing, stale, or conflicting, the agent should record a Knowledge Gap or Stop-Line Report instead of guessing.

Load binding governance and short indexes, then only the sources needed for the current stage: intake confirmations in change, confirmed spec/impact in plan, verified manifest/current task in apply, diff/ACs/receipts in check, and candidates/affected sources in archive. Expand for a named gap or risk, not to reread the whole repository.

Freshness means applicable source identity, not date alone: compare Verified Against revision/hash, affected dirty/untracked files, current contracts, and authorization scope. Refresh affected source evidence within existing authority and record drift; do not ask again for an authorized read or silently rewrite durable knowledge. Changed governing sources invalidate affected approvals. Unchanged unrelated sources do not require a full refresh.

Hard rules:

```text
No Evidence, No Fact.
No Confirmation, No Execution.
No Impact, No Brownfield Change.
```

Every durable knowledge item should record Status, Source, Verified At, Verified Against, and Scope. Every candidate should record Source, Evidence Needed, Target, and Promotion Gate.

`Assumed`, `Proposed`, `TBD`, `Conflict`, `Stale`, and open Knowledge Gaps may appear in discovery and candidates. They must not become final REQ/AC/INV, design decisions, context-pack instructions, implementation tasks, impact claims, code changes, or archive truth.

## Company Standards Packs

Existing team or company rules should not be bundled into public SDC releases. Import them into the business project as a private standards pack:

```bash
sdc standards import /path/to/spec-rules
```

The imported pack lives under `.sdc/standards/company/` by default. Its `README.md` is a routing index: agents read the index first, then load only the rule files relevant to the current task.

Use this boundary:

- `.sdc/knowledge/` says what is true about the product and system.
- `.sdc/standards/` says how this project should be built, tested, reviewed, and operated.
- `.sdc/standards/company/` adapts existing organization rules into the project without publishing private content in SDC itself.

If a company rule conflicts with the project constitution, confirmed knowledge, the current spec, or explicit user direction, stop and record a decision instead of treating the rule as an automatic fact.

## Consent Gates

SDC v1.1.1 adds consent gates to prevent AI-generated defaults from becoming project truth.

AI may propose options, but high-impact decisions need authoritative confirmation or bounded explicit delegation before entering `REQ-*`, `AC-*`, `INV-*`, `design.md`, or `tasks.md`. Valid prior confirmation can be cited without asking again.

High-impact decisions include:

- product rules and business invariants.
- roles, permissions, approval flows, and state machines.
- reminder timing, notification recipients, automation, and timeout behavior.
- technology stack, architecture, data model, authentication, locking, deletion, migration, rollout, and security policy.

Use a Decision Ledger for these decisions:

| Status | Meaning | Implementation-ready |
|--------|---------|----------------------|
| Confirmed | User-confirmed or supported by an authoritative project document | Yes |
| Proposed | Suggested by AI and waiting for user choice | No |
| Assumed | Temporary assumption for discussion | No |
| TBD | Required but unknown | No |
| Conflict | Conflicts with another source of truth | No |

This is the rule: suggestions are useful, silent defaults are not.

Bounded authorized reversible actions may proceed. Record the approving source, allowed action, scope, constraints, and stopping condition. Delegation must identify the decision area, allowed choices, and impact limits; record the chosen option in the Decision Ledger. Generic "use your judgment" does not grant new scope, data, permission, public-contract, or architecture authority and cannot supply unknown business requirements.

## Discovery Gate

`/sdc:change` is the normal entry point for new work. Before change-file writes, its evidence-backed intake covers project context, core scope, technical preferences, and constraints/acceptance using cited current or still-valid prior user/project confirmation. Coverage is mandatory; four new questions are not.

Discovery Gate is SDC's built-in requirement exploration workflow. It borrows the useful shape of brainstorming, but it must end in SDC artifacts:

```text
discovery.md -> Decision Ledger -> confirmed MVP -> spec.md
```

Ask only missing blocking questions. Record evidence-based non-applicability for irrelevant preferences instead of inventing a blocker. Continue Discovery Gate when any needed item remains unresolved:

- target user or affected actor.
- business goal.
- in-scope and out-of-scope boundaries.
- core scenario.
- acceptance direction.
- high-impact product or technical decisions.

While Discovery Gate is open, ask only the missing blocking questions in chat. With explicit persistence authorization, create or update only `discovery.md`, optional Draft `proposal.md`, and brief `notes.md`; the internal lifecycle record may track discovery only. Do not create or update `spec.md`, `design.md`, `tasks.md`, `impact.md`, `context-pack.md`, or `knowledge-candidates.md` until the gate exits. Unknown business requirements cannot be hidden in draft specs, designs, or investigation tasks.

`discovery.md` records current understanding, four-category coverage/source citations, authorization, risk rationale, relevant directions/tradeoffs, MVP, Decision Ledger, blocking questions, and exit criteria.

Exit Discovery Gate only when the current MVP scope is confirmed, high-impact decisions are confirmed or explicitly deferred, and no blocking open questions remain.

Interpretation summaries are not consent. "If wrong, tell me and I will update" is forbidden as write authorization. Cite explicit authorization already covering the action; if none exists, state the proposal, ask a focused question, and wait before writing. Do not repeat approval solely because a stage or session changed.

## Brownfield / Legacy Gates

SDC v1.1.3 separates two legacy concerns:

- `init` builds project cognition.
- `change` runs impact analysis after the requirement is confirmed.

For Brownfield/Legacy projects, `/sdc:init` should create or preserve `.sdc/project-cognition.md`. That file is the overall code-based map of the existing system: runtime shape, entry points, core data models, module map, external integrations, tests, delivery paths, risks, and reading order.

`project-cognition.md` is reusable project memory. SDC should not re-run full repository cognition for every change. Refresh it only when the current change touches an undocumented area, the repository structure or core contracts changed, the file contains relevant open questions, or the user explicitly requests repo re-analysis.

Do not produce a specific change impact analysis during init. There is no concrete requirement yet, so the impact would be guesswork.

After `/sdc:change` exits Discovery Gate and the spec is confirmed, the current change should run Change Impact Gate before `/sdc:plan`:

```text
project-cognition.md -> confirmed spec.md -> impact.md -> plan -> apply
```

`impact.md` is per-change and focused. It should use `project-cognition.md`, relevant product/technical knowledge, and current code evidence to identify only the necessary impact radius: change entry points, direct modification points, cascading impacts, contracts, data/config changes, security/observability effects, regression strategy, rollout order, rollback boundary, and open questions.

Important rule: only confirmed impact can become implementation tasks. Resolve technical inferences by focused investigation within confirmed scope before finalizing dependent tasks. Unknown business requirements stay in discovery; open scope, acceptance, contract, data, permission, security, or rollout decisions stop dependent plan/apply.

At final `sdc-review` or `/sdc:check`, Brownfield/Legacy delivery must include a legacy final impact review: compare actual diff and validation evidence against `impact.md`, then list old-system modification points, impact points, deviations, and residual risks.

## Knowledge Compact Gate

After `/sdc:check` passes, `/sdc:archive` is the normal way to close a requirement and update project memory.

The archive flow is:

```text
check -> archive -> Knowledge Compact Gate -> confirmed durable knowledge/memory updates
```

Required archive writes:

- promote the final confirmed spec to `.sdc/specs/<change-id>.md`.
- move the completed change history to `.sdc/changes/archive/<change-id>/`.
- create `archive.md` with delivery conclusion, evidence, coverage summary, residual risks, and knowledge-update summary.

Conditional memory updates:

- `.sdc/common-ground.md` for confirmed, rejected, promoted, demoted, or newly opened shared assumptions.
- `.sdc/expert-routing.md` for reusable expert profile triggers, stack-specific profiles, or missing risk coverage.
- `.sdc/knowledge/product/` for durable product goals, roles, flows, business rules, non-goals, or product decisions.
- `.sdc/knowledge/technical/` for durable stack, architecture, module, data/interface, operations, or testing knowledge.
- `.sdc/memory/` for useful procedures, lessons, gotchas, and candidate knowledge that should remain reviewable.
- `.sdc/decisions/` for long-lived product, technical, architecture, data, permission, rollout, or security decisions.
- `.sdc/standards/` for reusable engineering rules.
- `AGENTS.md` through `/sdc:harness` for AI execution guardrails.
- `.sdc/reports/bug/` for durable bug/root-cause analysis.
- `.sdc/reports/impact/` or archive final impact notes for Brownfield/Legacy effects.
- `.sdc/project.md` when stack, validation commands, deployment, or long-lived constraints changed.
- `.sdc/project-cognition.md` only when repo-level cognition is stale, incomplete, or affected by structural changes.

The agent proposes incremental conditional updates with exact targets, evidence, freshness checks, and content summary, then obtains explicit confirmation before writing. Candidate and affected-source links guide selection; archive should neither reread nor update every knowledge asset by habit.

## Traceability Chain

Every meaningful change should preserve this chain:

```text
SCN-* -> REQ-* -> AC-* -> T### -> validation evidence
```

Where:

- `SCN-*` is a user or system scenario.
- `REQ-*` is a requirement or business rule.
- `AC-*` is an acceptance criterion, preferably expressed with Given/When/Then.
- `T###` is a concrete task in `tasks.md`.
- Validation evidence is an actual execution receipt, scoped review, or manual verification. A documented blocker is a limitation, not a passing check.

## Stop-Line Report

Use a Stop-Line Report when execution cannot proceed safely:

```markdown
## Stop-Line Report
- Trigger:
- Evidence:
- Conflicting files:
- Affected REQ/AC:
- Options:
- Recommended next step:
```

Common triggers:

- spec, design, tasks, or code conflict.
- acceptance criteria are missing or unverifiable.
- high-impact decisions are Proposed, Assumed, TBD, or Conflict.
- OPEN or high-impact WORKING Common Ground is used as if it were confirmed.
- a high-risk change lacks the relevant expert profile or standards review.
- a plan chooses a concrete technology stack from a vague preference.
- implementation requires changing scope or public behavior.
- Brownfield/Legacy change lacks `impact.md` after requirements are confirmed.
- actual diff exceeds `impact.md` without updating spec/design/tasks.
- tests cannot prove the requested behavior.
- security, data migration, compatibility, or rollout risk appears.

## `/sdc:check` Modes

`/sdc:check` is the single quality entry point. It covers:

- delivery check: validate, review, test, quality.
- bug analysis: analyze only, no code changes unless the user asks for a fix.
- impact analysis: identify affected modules, contracts, data, tests, and rollback.
- repo analysis: brownfield project scan with evidence anchors.

This keeps the public interface simple without losing the deeper workflows.

## Task Format

Tasks must stay small and traceable:

```markdown
- [ ] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] Reject invalid login and verify the regression.
  - Depends on: none
  - Files: src/auth.js, tests/auth.test.js
  - Consumes: confirmed invalid-login behavior in REQ-01
  - Produces: invalid-login rejection with a regression test
  - Verify: npm test -- auth
  - Expected: the regression fails before the fix and passes after it
  - Review: Pending
  - Evidence: Pending
  - Source: .sdc/changes/active/2026-05-15-login/spec.md#AC-01
```

Rules:

- `Size` is `S` or `M`; never `L`.
- meaningful behavior tests come before implementation within the same coherent task where possible; behavior-neutral edits use focused validation.
- each task references at least one `REQ-*` and one `AC-*`.
- each task has dependency, verification, and source information.

## Design Principle

SDC should feel simple to operate and strict when it matters:

- simple outside: a few stable commands.
- disciplined inside: common ground, expert routing, decision chains, traceability, and evidence gates.
- no ceremony for ceremony's sake.
