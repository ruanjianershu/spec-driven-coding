# SDC Artifact Schemas

This reference defines durable SDC files. Use it when creating, repairing, validating, planning, archiving, or explaining `.sdc/` artifacts.

## Workspace Structure

```text
.sdc/
├── README.md
├── constitution.md
├── project.md
├── project-cognition.md
├── current/
│   ├── discovery.md
│   ├── spec.md
│   ├── plan.md
│   ├── tasks.md
│   └── apply.md
├── changes/
│   ├── active/
│   ├── archive/
│   └── README.md
├── specs/
│   └── README.md
├── standards/
│   ├── README.md
│   ├── coding.md
│   ├── testing.md
│   ├── architecture.md
│   ├── security.md
│   ├── git.md
│   └── ai.md
├── decisions/
│   └── README.md
├── reviews/
│   └── README.md
├── reports/
│   ├── bug/
│   ├── impact/
│   ├── repo-analysis/
│   └── README.md
├── templates/
│   ├── spec.md
│   ├── discovery.md
│   ├── plan.md
│   ├── tasks.md
│   ├── change.md
│   ├── project-cognition.md
│   ├── decision.md
│   ├── stop-line-report.md
│   ├── bug-analysis.md
│   ├── change-impact.md
│   └── repo-analysis.md
└── .gitignore
```

## Artifact Responsibilities

| Path | Purpose |
| --- | --- |
| `.sdc/constitution.md` | Highest project-level engineering governance and decision priority. |
| `.sdc/project.md` | Long-lived project context, users, stack, constraints, and validation commands. |
| `.sdc/project-cognition.md` | Brownfield project map based on code evidence. |
| `.sdc/current/` | Shortcut workspace for the current active requirement. |
| `.sdc/changes/active/` | Active requirement changes. One directory per independent change. |
| `.sdc/changes/archive/` | Completed change histories. |
| `.sdc/specs/` | Stable business specifications promoted from completed changes. |
| `.sdc/standards/` | Long-lived engineering standards for code, tests, architecture, security, git, and AI collaboration. |
| `.sdc/decisions/` | Durable product, technical, and architecture decisions. |
| `.sdc/reviews/` | Review reports. |
| `.sdc/reports/` | Bug, impact, repo-analysis, test, and quality reports. |
| `.sdc/templates/` | Templates used to create consistent artifacts. |

## Active Change Structure

Discovery Open changes intentionally use a small structure:

```text
.sdc/changes/active/YYYY-MM-DD-short-name/
├── discovery.md
├── proposal.md   # Draft
└── notes.md
```

Discovery Closed changes may use the full structure:

```text
.sdc/changes/active/YYYY-MM-DD-short-name/
├── discovery.md
├── impact.md       # Brownfield/Legacy/Unknown only; Greenfield may be N/A
├── proposal.md
├── tasks.md
├── design.md
├── spec.md
└── notes.md
```

Name rules:

- Use `YYYY-MM-DD-short-name`.
- Use lowercase English words and hyphens for `short-name`.
- One change directory represents one independent requirement iteration.

## File Responsibilities In A Change

| File | Purpose |
| --- | --- |
| `discovery.md` | Requirement exploration, candidate directions, tradeoffs, MVP, open questions, Decision Ledger. |
| `proposal.md` | Why the change exists, goals, non-goals, scope, acceptance direction, risks. |
| `spec.md` | Final or draft requirement spec with SCN/REQ/AC, invariants, validation strategy, and traceability. |
| `impact.md` | Brownfield per-change impact analysis after requirement confirmation. |
| `design.md` | Confirmed technical design, tradeoffs, impact boundaries, rollback and migration notes. |
| `tasks.md` | Thin, test-first, traceable execution tasks. |
| `notes.md` | Implementation notes, changed files, validation evidence, issues, decisions made during execution. |

## Artifact Creation Levels

Use the smallest durable artifact set that matches the certainty level:

| Level | Condition | Allowed artifacts |
| --- | --- | --- |
| Intake only | User has not confirmed intake answers | No `.sdc/changes/active/*` files |
| Discovery Open | Intake confirmed, but Open Questions or high-impact decisions remain | `discovery.md`, optional Draft `proposal.md`, brief `notes.md` |
| Discovery Closed | MVP, acceptance direction, and high-impact decisions are confirmed or explicitly deferred | Full change artifacts may be created |

Do not create `spec.md`, `design.md`, `tasks.md`, or `impact.md` while Discovery Open. This keeps token use low and prevents speculative documents from looking authoritative.

## Minimum Constitution Content

`constitution.md` should include:

- Governance priority.
- Fact priority.
- Core chain: discovery -> spec -> impact -> plan -> tasks -> code -> verify -> archive.
- Stop-line rules.
- Traceability rules.
- Human confirmation rules.
- No silent defaults.
- Discovery Gate.
- Brownfield/Legacy impact timing.

## Minimum Standards Files

Create or maintain:

- `coding.md`: naming, functions, error handling, comments.
- `testing.md`: strategy, required tests, validation records.
- `architecture.md`: module boundaries, dependency direction, tradeoffs.
- `security.md`: input/output safety, secrets, dependency safety.
- `git.md`: change size, pre-commit checks, PR expectations.
- `ai.md`: required and forbidden AI assistant behaviors.

## Spec Shape

A durable spec should include:

- Document metadata and status: `Draft` or `Confirmed`.
- Current understanding and source status table.
- Decision Ledger.
- Discovery summary.
- Glossary.
- Background, goal, non-goals.
- Users and roles.
- In scope / out of scope.
- Business invariants `INV-*`.
- Scenarios `SCN-*`.
- Requirements `REQ-*`.
- Acceptance criteria `AC-*`, preferably Given/When/Then.
- Non-functional requirements and external constraints.
- Validation strategy.
- Risks, assumptions, open questions, conflicts.
- Traceability matrix.
- Next SDC step.

## Plan And Task Shape

`design.md` should include:

- Solution summary.
- Impact scope and non-scope.
- Key tradeoffs.
- Data, API, state, or interaction changes as relevant.
- Brownfield/Unknown `impact.md` summary; for confirmed Greenfield, write `N/A` with reason.
- Risk, rollback, and migration notes.
- REQ/AC to design decision mapping.

`tasks.md` must use the shared task format from `workflow-standards.md`.

## Archive Shape

Archiving a completed change should:

1. Copy or promote final `spec.md` to `.sdc/specs/<change-id>.md`.
2. Create `archive.md` in the change directory.
3. Record archive time, delivery conclusion, validation evidence, and residual risks.
4. Preserve REQ/AC/T### coverage.
5. Run the Knowledge Compact Gate.
6. Move the change directory to `.sdc/changes/archive/<change-id>/`.

Never delete change history to make it look cleaner.

`archive.md` should include:

- Change identity and archive time.
- Final delivery conclusion.
- Validation, review, test, quality, security, and Brownfield final impact evidence where applicable.
- REQ/AC/T### coverage summary.
- Deferred scope, follow-up changes, and residual risks.
- Knowledge Compact Gate summary.

## Knowledge Compact Gate Shape

Knowledge Compact Gate is part of archive. It decides what long-lived project memory should be updated after a completed change.

Required durable updates:

- `.sdc/specs/<change-id>.md` for the final confirmed spec.
- `.sdc/changes/archive/<change-id>/archive.md` for the completed change history and evidence.

Conditional durable updates:

- `.sdc/decisions/` when a product, technical, architecture, data, permission, rollout, or security decision is long-lived.
- `.sdc/standards/` when the change creates or corrects a reusable engineering standard.
- `AGENTS.md` through `sdc-harness` when the change exposes a recurring AI execution rule or project guardrail.
- `.sdc/reports/bug/` when a root cause, reproduction, or regression-prevention note should be preserved.
- `.sdc/reports/impact/` or an archive final impact section when Brownfield/Legacy impact evidence should be retained.
- `.sdc/project.md` when project context, stack, validation commands, deployment, or constraints changed.
- `.sdc/project-cognition.md` only when repository-level cognition is stale, incomplete, or affected by structural/code-contract changes.

The gate should output this table:

| Action | Target | Reason | Status |
| --- | --- | --- | --- |
| Required / Recommended / N/A | File or artifact | Evidence-based reason | Done / Needs confirmation / Deferred / N/A |

Archive does not mean updating every knowledge asset. Update only what evidence supports.

Recommended and conditional durable updates require explicit human confirmation before writing. The agent may propose exact target files and content summary, but must not silently write those files.
