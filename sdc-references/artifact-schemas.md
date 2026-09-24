# SDC Artifact Schemas

This reference defines durable SDC files. Use it when creating, repairing, validating, planning, archiving, or explaining `.sdc/` artifacts.

The following structures describe the standard format. New confirmed prose-only changes may use `compact-workflow.md` and its executable `sdc.compact/v1` schema instead. Never validate a compact change against the standard template package, or use compact to weaken a standard change's gates.

## Workspace Structure

```text
.sdc/
├── README.md
├── constitution.md
├── project.md
├── project-cognition.md
├── common-ground.md
├── expert-routing.md
├── knowledge/
│   ├── README.md
│   ├── index.md
│   ├── current.md
│   ├── product/
│   │   ├── README.md
│   │   ├── overview.md
│   │   ├── roles.md
│   │   ├── domain.md
│   │   ├── flows.md
│   │   ├── rules.md
│   │   └── decisions.md
│   └── technical/
│       ├── README.md
│       ├── stack.md
│       ├── architecture.md
│       ├── modules.md
│       ├── data-and-interfaces.md
│       ├── operations.md
│       └── testing.md
├── memory/
│   ├── README.md
│   ├── candidates.md
│   ├── procedures.md
│   └── episodic/
│       └── README.md
├── current/
│   ├── discovery.md
│   ├── spec.md
│   ├── plan.md
│   ├── tasks.md
│   ├── apply.md
│   ├── context-pack.md
│   └── knowledge-candidates.md
├── changes/
│   ├── active/
│   ├── archive/
│   └── README.md
├── specs/
│   └── README.md
├── standards/
│   ├── README.md
│   ├── company/
│   │   └── README.md
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
├── runtime/              # git-ignored execution scratch
│   ├── sessions/<session-id>/active-change.json
│   └── <change-id>/
│       ├── progress.md
│       ├── evidence.jsonl
│       ├── research/
│       ├── task-T###-brief.md
│       ├── task-T###-report.md
│       └── task-T###-review-package.md
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
│   ├── context-pack.md
│   ├── common-ground.md
│   ├── expert-routing.md
│   ├── knowledge-candidates.md
│   ├── knowledge-index.md
│   └── repo-analysis.md
└── .gitignore
```

## Artifact Responsibilities

| Path | Purpose |
| --- | --- |
| `.sdc/constitution.md` | Highest project-level engineering governance and decision priority. |
| `.sdc/project.md` | Long-lived project context, users, stack, constraints, and validation commands. |
| `.sdc/project-cognition.md` | Brownfield project map based on code evidence. |
| `.sdc/common-ground.md` | Shared project assumptions split into ESTABLISHED, WORKING, and OPEN tiers. |
| `.sdc/expert-routing.md` | Internal expert profile routing so SDC can use specialist lenses without adding public commands. |
| `.sdc/knowledge/` | Confirmed project knowledge split into product and technical knowledge. |
| `.sdc/knowledge/index.md` | Short routing index read before non-trivial change, plan, apply, and check work. |
| `.sdc/knowledge/product/` | Product goals, roles, domain concepts, flows, business rules, and product decisions. |
| `.sdc/knowledge/technical/` | Stack, architecture, modules, data/interfaces, operations, and testing knowledge. |
| `.sdc/memory/` | Project memory, procedures, episodic notes, and knowledge candidates. Memory does not override confirmed knowledge. |
| `.sdc/current/` | Shortcut workspace for the current active requirement. |
| `.sdc/changes/active/` | Active requirement changes. One directory per independent change. |
| `.sdc/changes/archive/` | Completed change histories. |
| `.sdc/specs/` | Stable business specifications promoted from completed changes. |
| `.sdc/standards/` | Long-lived engineering standards for code, tests, architecture, security, git, and AI collaboration. |
| `.sdc/standards/company/` | Optional imported company/team standards pack. Read `README.md` first, then only the relevant rule files. |
| `.sdc/decisions/` | Durable product, technical, and architecture decisions. |
| `.sdc/reviews/` | Review reports. |
| `.sdc/reports/` | Bug, impact, repo-analysis, test, and quality reports. |
| `.sdc/runtime/` | Git-ignored task briefs, reports, diff packages, and progress ledgers used for context-efficient execution and recovery. It is not durable project truth. |
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
├── state.json
├── tasks.md
├── design.md
├── spec.md
├── context-pack.md
├── apply-context.jsonl
├── check-context.jsonl
├── knowledge-candidates.md
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
| `design.md` | Confirmed technical design, tradeoffs, impact boundaries, rollback and migration notes, plus triggered output artifacts. |
| `tasks.md` | Thin, test-first, traceable execution tasks. |
| `context-pack.md` | Short handoff package for execution agents: goal, knowledge sources, boundaries, forbidden assumptions, validation commands. |
| `knowledge-candidates.md` | Candidate knowledge discovered during apply/check; archive decides what becomes durable. |
| `notes.md` | Implementation notes, changed files, validation evidence, issues, decisions made during execution. |

## Artifact Creation Levels

Use the smallest durable artifact set that matches the certainty level:

| Level | Condition | Allowed artifacts |
| --- | --- | --- |
| Intake only | Coverage/authorization not established and persistence not authorized | No `.sdc/changes/active/*` files |
| Discovery Open | Four-category coverage records confirmed sources and blocking gaps; discovery persistence is authorized | `discovery.md`, optional Draft `proposal.md`, brief `notes.md`; internal lifecycle record may track discovery only |
| Discovery Closed | MVP, acceptance direction, and high-impact decisions are confirmed or explicitly deferred | Full change artifacts may be created, including `context-pack.md` and `knowledge-candidates.md` |

Do not create `spec.md`, `design.md`, `tasks.md`, `impact.md`, `context-pack.md`, or `knowledge-candidates.md` while Discovery Open. This keeps token use low and prevents speculative documents from looking authoritative.

Intake coverage cites current or still-valid prior user/project confirmation; there is no fixed question count. Ask only missing blocking questions. Unknown business requirements cannot be represented as draft specs or investigation tasks. See `discovery-gate.md` for authorization and minimal output details.

## Knowledge And Memory Responsibilities

SDC separates durable knowledge from project memory:

- Knowledge is confirmed, shared, auditable project truth.
- Common Ground is the shared assumption layer that says which facts are ESTABLISHED, which interpretations are WORKING, and which questions remain OPEN.
- Expert Routing is the internal profile map for selecting specialist checks and references without exposing extra user commands.
- Product knowledge answers why the project exists, who uses it, which workflows matter, and what business rules must hold.
- Technical knowledge answers how the system is built, where capabilities live, how contracts work, and how to verify or operate the system.
- Memory records candidates, procedures, lessons, and episodic summaries that may help future agents recall context.
- Project, personal, native-client, and cross-device memory remain Candidate recall; they cannot override confirmed knowledge, current specs, user confirmation, or code evidence. Promotion needs explicit confirmation of content and destination.

Knowledge item states:

| State | Meaning | Can drive spec/plan/apply? |
| --- | --- | --- |
| Confirmed | Explicitly confirmed by user, authoritative project docs, archived spec, decision record, or code evidence where technical fact is current behavior | Yes |
| Candidate | Proposed durable knowledge awaiting archive/user confirmation | No |
| Assumed | Temporary working assumption | No |
| Stale | May be outdated and needs refresh | No, unless reconfirmed |
| Conflict | Contradicts another source | No |
| Deprecated | Preserved for history, no longer active | No |

Before final spec, plan, apply, or check, use `.sdc/knowledge/index.md` and only relevant product/technical source sections. Reuse loaded context when its source identity and applicability remain current. Refresh affected source evidence within existing authority; stop on unresolved business gaps or conflicts, not age alone. Durable knowledge edits still need confirmation. See `workflow-standards.md` for selective context and freshness policy.

Before non-trivial change, spec, plan, apply, check, or archive work, agents must read `.sdc/common-ground.md`. OPEN items block final artifacts when they affect scope, acceptance, data, permissions, architecture, security, rollout, or compatibility. WORKING items must be cited and cannot silently become ESTABLISHED.

During plan/check/archive, agents should read `.sdc/expert-routing.md` and select the smallest relevant expert profiles. Expert profile guidance can create questions, checks, and investigation tasks, but it cannot create unconfirmed product facts or technical decisions.

During plan/check, agents should apply `artifact-output-contracts.md`. Triggered outputs such as diagrams, API/data contracts, UX flow, test matrix, deploy checklist, and AI involvement note must be produced or explicitly marked N/A with evidence.

Every durable knowledge row should record:

- Status.
- Source.
- Verified At.
- Verified Against.
- Scope.

Every candidate knowledge row should record:

- Candidate.
- Type.
- Scope.
- Source.
- Status.
- Target.
- Evidence Needed.
- Promotion Gate.

The evidence contract is:

```text
No Evidence, No Fact.
No Confirmation, No Execution.
No Impact, No Brownfield Change.
```

Open Knowledge Gaps and `Assumed`, `Proposed`, `TBD`, `Conflict`, or `Stale` entries are allowed in discovery and candidates, but not in final execution inputs.

## Minimum Constitution Content

`constitution.md` should include:

- Governance priority.
- Fact priority.
- Knowledge and memory discipline.
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
- Knowledge sources used.
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
- Artifact Output Contract with required outputs or N/A reasons.
- Risks, assumptions, open questions, conflicts.
- Traceability matrix.
- Next SDC step.

## Plan And Task Shape

`design.md` should include:

- Knowledge sources used.
- Solution summary.
- Impact scope and non-scope.
- Key tradeoffs.
- Data, API, state, or interaction changes as relevant.
- Artifact Output Contract.
- Exact Global Constraints that bind every task.
- Plan Preflight status and findings.
- Process/state diagrams, sequence/integration diagrams, API/data contracts, UX flow/states, test matrix, deploy/release checklist, and AI involvement note as triggered.
- Brownfield/Unknown `impact.md` summary; for confirmed Greenfield, write `N/A` with reason.
- Risk, rollback, and migration notes.
- REQ/AC to design decision mapping.

`tasks.md` must use the shared task format from `workflow-standards.md`. Every task declares Files, Consumes, Produces, Verify, Expected, Review, Evidence, and Source. Completed tasks require approved review and non-pending evidence.

`context-pack.md` should include:

- Goal.
- Internal risk level (`light` / `standard` / `strict`), matched triggers, evidence, visible rationale, and any approved downgrade.
- Authorization source, scope, bounded delegated choices, and stopping conditions.
- Affected source scope and proportionate validation/review plan; all levels keep the same semantic acceptance.
- Knowledge sources used.
- Knowledge gaps, empty only when none remain.
- Common Ground used.
- Expert profiles used.
- Artifact Output Contract summary.
- Exact Global Constraints.
- Execution Orchestration mode, runtime workspace, review policy, and final-review requirement.
- Confirmed product knowledge.
- Confirmed technical knowledge.
- Execution boundaries.
- Forbidden assumptions.
- Task and traceability summary.
- Validation commands.
- Knowledge candidate routing.

Runtime task briefs, implementer reports, review packages, and progress ledger are created under `.sdc/runtime/<change-id>/`. They are intentionally ignored. Durable review and validation conclusions must be copied into `tasks.md`, `notes.md`, review/test reports, or archive evidence.

Completed delivery uses a machine-readable durable review shape in `notes.md` (or `current/apply.md`): one `### T###` block per completed task with `Spec Compliance: Approved`, `Code Quality: Approved`, and an `Evidence` reference to an existing local Markdown anchor or `git:<commit>`. `Final Whole-Change Review` requires `Status: Approved`, the same two verdicts, and durable evidence.

For a single-task light change, task and final blocks may reference one independent review of the complete final snapshot. Both verdict records remain required. Focused tests and review receipts may be reused across gates only while their scope and source snapshots stay current.

## Runtime State And Context Schemas

These contracts are internal. They support the existing public stages and do not create a new slash command.

### Change State

Tracked path: `.sdc/changes/active/<change-id>/state.json`.

```json
{"schema":"sdc.change-state/v1","change_id":"2026-08-25-example","state":"planned","updated_at":"2026-08-25T00:00:00Z","source":{"kind":"plan-stage","paths":["design.md","tasks.md","context-pack.md"]}}
```

Allowed states are exactly `intake`, `discovery`, `confirmed`, `planned`, `applying`, `checking`, and `archivable`. Normal transitions advance one boundary with validated content and provenance; valid same-state retries are idempotent. Changed governing inputs require explicit reasoned reopen to discovery or confirmed, retained history, and invalidated affected approvals. A label alone never grants confirmation or delivery approval. `planned` requires current verified role manifests; `checking` requires completed tasks with approved task reviews; `archivable` and archive also require approved final whole-change review and fresh required execution receipts. Unsafe or invalid evidence cannot mutate the prior state. See `runtime-context.md` for the current schema, snapshot fields, reopen syntax, and compatibility handling; the JSON above illustrates base identity only.

### Active Change Resolution And Session Pointer

Resolution output uses `sdc.active-change-resolution/v1`. Selection precedence is explicit change, `SDC_ACTIVE_CHANGE`, valid session pointer, then the sole valid active directory. Zero or multiple candidates, invalid selectors, unsafe IDs, and symlinked or escaping workspace, active-change, session, research, or evidence paths stop with a non-zero result.

Ignored path: `.sdc/runtime/sessions/<session-id>/active-change.json`.

```json
{"schema":"sdc.session-pointer/v1","session_id":"client-session","change_id":"2026-08-25-example","selected_at":"2026-08-25T00:00:00Z","source":"explicit"}
```

Session pointers are local convenience data. They require every field shown above, an RFC3339 timestamp, and `source: explicit`. They never override an explicit selector or confirmed project artifacts. Claude's hook uses the event payload session ID first; ambient `SDC_SESSION_ID` fallback is disabled unless `SDC_ALLOW_ENV_SESSION_ID=1` is set intentionally.

### Role Context Manifest

Tracked paths: `apply-context.jsonl` and `check-context.jsonl` in the active change.

Each line uses schema `sdc.context-manifest-record/v1` and the stable field order `schema`, `manifest`, `change_id`, `role`, `order`, `path`, `section`, `purpose`, `required`, `source_type`, `sha256`. Paths are repository-relative, required sources must exist, and hashes reflect current bytes. Generation is atomic and deterministic.

Verify required manifest shape, source identity, and hashes before use. Missing, malformed, or stale manifests cannot authorize execution; regeneration alone cannot reapprove changed governing inputs.

### Candidate Recall And Research Route

Recall output uses `sdc.recall-result/v1`. Every result has `status: Candidate`, a repository-relative Markdown path, line, score, and bounded excerpt. Recall is read-only, remains beneath each allowlisted root, and excludes runtime data, symbolic-link paths, credential-shaped values, and files resolving outside the repository.

Research routing uses `sdc.research-route/v1`. Scratch goes to `.sdc/runtime/<change-id>/research/`; change-stage citations go to `discovery.md`, later citations go to `notes.md`; after discovery closes, durable findings remain Candidate in `knowledge-candidates.md` until archive confirmation.

### Session Context And Evidence

Portable session context uses `sdc.session-context/v1`. It reports the selected change, selection source, lifecycle state, manifest summaries, bounded Candidate recall, and the manual fallback. Supported opt-in Claude/Codex hooks may wrap this compact non-authoritative context; absent, unsupported, or failed hooks use the portable adapter through stage instructions.

Ignored evidence lines use `sdc.evidence-record/v1` at `.sdc/runtime/<change-id>/evidence.jsonl`. Records are bounded and may summarize a stage command, status, safe repository-relative evidence path, and timestamp. Commands containing credential-shaped values are rejected; summaries are redacted before persistence. This best-effort filter does not replace a dedicated secret scanner. Durable tasks and notes remain authoritative.

An appended assertion is not executable proof. Required validation uses the bounded internal runner to capture actual command, outcome/exit status, and source snapshot; missing, failed, timed-out, or stale receipts cannot pass. See `runtime-context.md` for current receipt fields and validation. Durable notes link real evidence and cannot override failed execution.

Every completed task needs the latest fresh passed run receipt with argv exactly matching its executable Verify command. Explicit `sh -c` is required for pipelines; multiple task IDs may share a receipt only for identical Verify argv. Last-task progress and final approved independent review notes must precede the review receipt binding notes/tasks and source snapshots. Reviewer attribution is not authenticated identity. Verify both receipt types; later code edits or the new revision nonce from reopen invalidate old evidence.

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

Knowledge Compact Gate is part of archive. It decides what long-lived project knowledge and memory should be updated after a completed change.

Required durable updates:

- `.sdc/specs/<change-id>.md` for the final confirmed spec.
- `.sdc/changes/archive/<change-id>/archive.md` for the completed change history and evidence.

Conditional durable updates:

- `.sdc/knowledge/product/` when the change creates or changes long-lived product goals, roles, flows, business rules, non-goals, or product decisions.
- `.sdc/knowledge/technical/` when the change creates or changes long-lived stack, architecture, module, data/interface, operations, or testing knowledge.
- `.sdc/memory/` when the change leaves reusable procedures, lessons, gotchas, or candidate knowledge that is not yet confirmed enough for durable knowledge.
- `.sdc/common-ground.md` when the change confirms, rejects, promotes, demotes, or adds shared assumptions.
- `.sdc/expert-routing.md` when the change reveals a reusable profile trigger, stack-specific expert lens, or missing review profile.
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

Archive does not mean reading or updating every knowledge asset. Select affected sources from candidates and delivery evidence, verify their freshness, and propose incremental changes only where justified.

Recommended and conditional durable updates require explicit human confirmation before writing. The agent may propose exact target files and content summary, but must not silently write those files.
