# SDC Discipline Core

SDC v1.1 keeps the public command surface small while strengthening the internal engineering discipline.

The goal is not to copy every OpenSpec, Superpowers, or internal workflow command. The goal is to keep their useful core:

- OpenSpec: change lifecycle, validation, archive.
- Superpowers: lightweight skill-pack distribution.
- Karpathy-style skills and internal workflow practice: think before coding, thin slices, TDD, stop-line reports, evidence over vibes.
- Memory/knowledge-base systems: short indexes, task-focused loading, candidate knowledge, and reviewable archive-time promotion.

## Public Surface

Normal users should only need these commands or natural-language equivalents:

```text
/sdc:init
/sdc:change
/sdc:plan
/sdc:apply
/sdc:check
/sdc:archive
/sdc:harness
```

Detailed skills such as `sdc:spec`, `sdc:validate`, `sdc:review`, `sdc:test`, and `sdc:quality` remain available for advanced users and internal routing.

Do not add a separate public compact command. Knowledge compaction is part of `/sdc:archive`.

## Role Prompt Contracts

SDC v1.1.4 adds English Role Prompt Contracts for every skill. The current layout keeps those contracts in `skills/sdc-shared/role-contracts.md` so each `SKILL.md` stays short while the agent can still load the exact contract it needs.

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
- Memory records candidates, procedures, lessons, and episodic summaries. It helps future agents recall context but does not override confirmed knowledge.

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

AI may propose options, but high-impact decisions must be confirmed before they enter `REQ-*`, `AC-*`, `INV-*`, `design.md`, or `tasks.md`.

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

## Discovery Gate

`/sdc:change` is the normal entry point for new work. It must always start with Mandatory Change Intake Gate before creating files. The agent must not decide silently whether the request is "clear enough".

Discovery Gate is SDC's built-in requirement exploration workflow. It borrows the useful shape of brainstorming, but it must end in SDC artifacts:

```text
discovery.md -> Decision Ledger -> confirmed MVP -> spec.md
```

Mandatory Change Intake Gate always asks project context, core scope, technical preferences, and constraints/acceptance questions. After intake, continue Discovery Gate when any of these remain unresolved:

- target user or affected actor.
- business goal.
- in-scope and out-of-scope boundaries.
- core scenario.
- acceptance direction.
- high-impact product or technical decisions.

While Discovery Gate is open, keep artifacts intentionally small. The default output is the next 3-5 confirmation questions in chat. If persistence is needed after intake confirmation, create or update only `discovery.md`, optional Draft `proposal.md`, and brief `notes.md`. Do not create or update `spec.md`, `design.md`, `tasks.md`, `impact.md`, `context-pack.md`, or `knowledge-candidates.md` until the gate exits.

`discovery.md` should contain current understanding, candidate directions, tradeoffs, recommended MVP, Decision Ledger, open questions, and exit criteria.

Exit Discovery Gate only when the current MVP scope is confirmed, high-impact decisions are confirmed or explicitly deferred, and no blocking open questions remain.

Interpretation summaries are not consent. "If wrong, tell me and I will update" is forbidden as write authorization. State the interpretation as `Proposed`, ask a yes/no or option-selection question, wait for the user, then write durable artifacts.

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

Important rule: only confirmed impact can become implementation tasks. Reasonable inferences may become investigation tasks. Open questions that affect scope, acceptance, contracts, data, permissions, security, or rollout must stop plan/apply.

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

The agent must recommend conditional updates with evidence and target files, then ask for explicit yes/no confirmation before writing them. Archive should not update every knowledge asset by habit.

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
- Validation evidence is a test command, review note, manual verification, or documented blocker.

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
- [ ] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] Write failing test for invalid login.
  - Depends on: none
  - Verify: npm test -- auth
  - Source: .sdc/changes/active/2026-05-15-login/spec.md#AC-01
```

Rules:

- `Size` is `S` or `M`; never `L`.
- tests come before implementation tasks.
- each task references at least one `REQ-*` and one `AC-*`.
- each task has dependency, verification, and source information.

## Design Principle

SDC should feel simple to operate and strict when it matters:

- simple outside: a few stable commands.
- disciplined inside: decision chains, traceability, and evidence gates.
- no ceremony for ceremony's sake.
