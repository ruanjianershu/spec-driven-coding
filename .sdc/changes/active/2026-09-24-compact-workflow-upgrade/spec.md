# Spec

- Status: Confirmed
- Schema: SDC 1.3.0 STANDARD
- Change: 2026-09-24-compact-workflow-upgrade
- Confirmation source: discovery.md U-01 directs repair of A-02's reported issues and GitHub delivery; U-02/U-03 establish prior upgrade and verification direction.
- Meaning of confirmation: repair/delivery scope is authorized. Detailed ACs are engineering derivations from reported defects and existing contracts, not detailed user quotations. Main reviews artifacts before runtime gates.

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| discovery.md U-01 through U-03; A-01/A-02; D-01 through D-06 | User scope / engineering derivation | Provenance separated in discovery | Scope, reported defects and bounded decisions |
| `.sdc/constitution.md`, `.sdc/project.md`, `.sdc/standards/testing.md`, `.sdc/standards/security.md` | Inspected | Existing project rules | Governance, regression and safety |
| `.sdc/knowledge/index.md`, `.sdc/common-ground.md`, `.sdc/expert-routing.md` | Inspected | Empty/Candidate knowledge and routing templates | No implied promotion |
| `docs/plans/2026-09-24-compact-workflow-upgrade.md` | Historical record | Approved upgrade description and attributed claims | Preserve original intent, not unverified results |
| `impact.md#evidence-index` | Inspected | Named runtime functions and real test modules | Source-backed technical context |
| sdc-references/artifact-schemas.md; sdc-references/workflow-standards.md; sdc-references/compact-workflow.md; sdc-references/review-findings.md; sdc-references/test-quality.md | Inspected | Existing contracts | Format, authority, findings and evidence limits |

## Knowledge Gaps

None that block the scoped requirements. Root knowledge stubs are not execution facts. Fresh regression, review and lifecycle evidence must still be produced by the main task.

## Common Ground Used

Root Common Ground has no populated ESTABLISHED facts for this scope. Use U-01 for repair/delivery direction, A-02 for reported technical defects, and inspected contracts for engineering choices; no memory candidate or empty template confirms requirements.

## Decision Ledger

| ID | Decision | Status | Source | Impact | Next Step |
|---|---|---|---|---|---|
| D-01 | Reconcile in STANDARD without backdated gates | Confirmed | A-01 strategy; existing schema/evidence policy | AC-09 | Preserve honest chronology |
| D-02 | Repair the six assistant-reported issues within existing contracts | Confirmed | U-01 refers to A-02; engineering judgment | AC-01 through AC-08 | T001-T005 |
| D-03 | Completion requires actual current evidence and independent review | Confirmed | Existing SDC policy | AC-09 | Main records outcomes |
| D-04 | Push to GitHub after current delivery gates | Confirmed | U-01; A-01 delivery boundary; SDC policy | AC-09 | Record pushed revision |
| D-05 | Strict risk controls with STANDARD format | Confirmed | Existing risk triggers; engineering assessment | All ACs | Review affected risks |

## Discovery Summary

U-01 confirms fixing reported issues and pushing to GitHub. A-01 is the lead agent's reconciliation strategy, not user-authored requirements. The initial implementation preceded this package. Existing candidate repairs and results require source-bound evidence and main's review before completion.

## Glossary

| Term | Meaning In This Change |
|---|---|
| STANDARD | Full Markdown SDC artifact format; distinct from the lowercase risk tier `standard` |
| Compact | Narrow `sdc.compact/v1` format for confirmed behavior-neutral prose; not eligible for this repair |
| Frozen evaluator | Bounded source snapshot copied first to a frozen source and then to a disposable trial project |
| Effective registration | SDC skill entrypoints actually selected by the supported Claude on-disk manifest/marketplace loading model, not merely present bytes |
| Receipt | Runtime-generated evidence bound to exact command, revision and source; prose claims are not receipts |
| Reviewer attribution | Caller-supplied non-sensitive label; not authenticated identity or independent-review proof |
| F-001-F-006 | Stable IDs from the assistant's reproduced report; U-01 authorizes their repair |

## Background And Goal

Restore trustworthy execution and compatibility for the already-coded compact/guidance/doctor/findings upgrade. Target users are maintainers running SDC CLI workflows, plugin users following installed guidance, and reviewers checking real evidence.

## In Scope

Actual production code and test repairs for F-001 through F-006, current verification/runtime evidence, independent reviews and the authorized GitHub push. Preserve compact eligibility, lifecycle gates, read-only doctor behavior, focused guidance, stable findings, STANDARD compatibility and existing adapters. Record chronology and authority honestly.

## Out Of Scope

New public commands, stack/dependency changes, broader client configuration support, authenticated identity, live-client benchmarks, unrelated refactors, internal GitLab delivery, npm publication and user-home installations. Production repairs, real evidence and GitHub delivery are explicitly in scope.

## Business Invariants / 业务不变量

- INV-01: Confirmation, scope, source freshness, exact-command execution evidence, clear blocking findings, and independent reviews remain mandatory; no repair can grant its own approval.
- INV-02: Compact remains limited to new confirmed behavior-neutral prose changes. Existing STANDARD changes never silently downgrade.
- INV-03: Installation diagnostics are local and read-only; running doctor does not grant configuration repair, installation or network authority.
- INV-04: Legacy compatibility must not suppress a real change in source, finding history, review inputs or authorization.
- INV-05: Current confirmation cannot certify past preflight, tests or review. Completion requires actual current evidence and independent verdicts; pending statuses may advance when these obligations are met.
- INV-06: Public lifecycle entries remain `init/change/plan/apply/check/archive`, with existing `sdc` routing and optional `harness`; no additional public stage.

## Scenarios And Requirements

| Scenario | Requirement | Required Behavior | Finding |
|---|---|---|---|
| SCN-01: Evaluate from an isolated frozen source | REQ-01 | Preserve runnable copied helpers and required support files without host import leakage or relaxed staging safety | F-001 |
| SCN-02: Diagnose a same-byte Claude install whose selection omits skills | REQ-02 | Detect missing effective SDC entrypoints separately from payload drift, preserving loading semantics and read-only reporting | F-002 |
| SCN-03: Run findings guidance from a product project | REQ-03 | Resolve helpers from the selected plugin/runtime, preserving target-project working directory and finding gates | F-003 |
| SCN-04: Modify undeclared source after compact approval | REQ-04 | Detect tracked code hidden by directory filters and non-Git directory-link changes before compact delivery | F-004 |
| SCN-05: Reuse an unchanged STANDARD receipt made before findings support | REQ-05 | Preserve truly unchanged old approval while invalidating reviews on real ledger appearance, change or removal | F-005 |
| SCN-06: Attribute review with a descriptive long label | REQ-06 | Accept non-sensitive prose labels without weakening credential screening or claiming authenticated identity | F-006 |
| SCN-07: Verify and deliver the complete reconciled change | REQ-07 | Preserve all four upgrade areas and existing workflows, with honest current evidence and completed independent reviews before GitHub delivery | All |

## Acceptance Criteria / 验收标准

### AC-01

Given a current source copied into a frozen evaluator and copied again into a disposable project without host `PYTHONPATH`, when real CLI/runtime/findings helper entrypoints run, then imports succeed and expected help/structured outcomes are returned. Required compact/findings modules and the explicit doctor sidecar survive both copies. Older source versions that do not need those helpers remain evaluable. Symlink and byte/file bounds remain enforced. Covers REQ-01, F-001.

### AC-02

Given matching source and installed payload bytes but a supported marketplace-root Claude skill selection that omits intended entrypoints, when doctor runs, then it returns a blocking, actionable structured configuration diagnostic and nonzero exit. Equivalent ordering, duplicate paths and trailing slashes do not create false drift; default/additive discovery and genuine duplicate detection remain intact. Source/home contents and modification times remain unchanged. Covers REQ-02, F-002.

AC-02 also covers independent-review cases F-007 through F-009 within the same
fail-closed diagnostic contract: a cached default source cannot certify missing
public command entrypoints; unsupported non-string hook declarations must be
rejected; quoted top-level TOML registration keys cannot silently evade inspection.
The supported portable Codex empty hook list still means no hooks, not an error.

### AC-03

Given a product project with an active change but no SDC source checkout, when the documented findings commands use a resolved installed plugin/runtime root, then list/record/adjudicate/resolve address that project and return the helper's defined JSON outcomes without project-relative helper lookup or shell execution of evidence. Existing identity, retry and blocking-finding semantics remain intact. Covers REQ-03, F-003.

### AC-04

Given a compact change declaring only a README correction and Git-tracked code under a normally filtered directory such as `docs/venv/runner.py`, when that code changes after the compact baseline or approval, then validation, evidence verification and archive reject the out-of-scope/stale change. Source exclusions must not hide tracked product files. Covers REQ-04, F-004.

AC-04 additionally covers F-010: if a tracked child's parent is replaced by an
ignored directory link, retargeting that ancestor changes source identity and
invalidates approval. Bind the first link destination without traversing it.

### AC-05

Given an equivalent non-Git compact fixture, when an undeclared directory symlink is added or retargeted, then compact scope/freshness checks block delivery without traversing or modifying its external target. Existing declared-path, ignored-target and governing-source freshness checks remain enforced. Covers REQ-04, F-004.

### AC-06

Given an otherwise unchanged valid older STANDARD state and review receipt with no findings ledger and no findings snapshot key, when read, evidence verification and archive run, then absence alone does not invalidate approval. Creating, modifying or removing an actual ledger invalidates the affected review; no compatibility normalization conceals these transitions. Open, adjudication-required and accepted-risk findings still block delivery. Covers REQ-05, F-005.

### AC-07

Given valid review prerequisites and the harmless label `parent-independent-review-2026-09-24-frozen-portable`, when a review receipt is requested, then the label is accepted as attribution. Labels containing explicit credentials or opaque secret-like values are still rejected without leaking them. Label acceptance neither performs review nor authenticates a person. Covers REQ-06, F-006.

### AC-08

Given the repaired final source, when the focused groups and the full regression command in T005 run, then all required local suites and audit/syntax checks succeed. Compact cold start and archive, STANDARD delivery/freshness, stable findings, installed adapters, and guidance routing remain compatible. Skips and failures are reported, not counted as proof of uncovered ACs. Static guidance tests do not prove agent quality or token savings. Covers REQ-07 and all original upgrade areas.

### AC-09

Given the repaired change is ready for delivery, when completion is asserted and the GitHub push is performed, then the record truthfully identifies initial code as preceding formal artifacts, distinguishes user direction from assistant findings and engineering strategy, and links actual current verification and independent task/whole-change reviews to the delivered source. Required runtime gates and receipts must be current before push, and the pushed revision/result must be recorded. No historical preflight, approval or test result is fabricated; no internal GitLab push, npm publication or user installation is included. Covers REQ-07.

## Non-Functional Constraints

Preserve Node.js `>=14.0.0`, Python standard-library runtime helpers, local-first operation, existing module ownership and bounded scans. No new dependencies, telemetry, background service or MCP server. Public prose is English without personal paths, private names or closed-source attribution. Legacy non-English heading tokens are retained only where the current validator requires them.

## Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | Required | Lifecycle and retrospective boundaries | design.md#process--state-diagrams | Preserve current authorization, review and freshness gates |
| Sequence / Integration Diagram | Required | Frozen staging, diagnostics and evidence integration | design.md#sequence--integration-diagrams | F-001-F-006 cross existing modules |
| API / Contract Specification | Required | CLI and reviewer compatibility | design.md#api--contract-specification | AC-01 through AC-07 |
| Data Model / Migration Contract | Required | Snapshot and findings compatibility | design.md#data-model--migration-contract | AC-06; no forced migration |
| UX Flow / Interaction States | Required | CLI diagnosis and blocked delivery | design.md#ux-flow--interaction-states | Human-readable errors and structured results |
| Test Matrix | Required | Acceptance validation | design.md#test-matrix | All ACs mapped to tasks and actual test modules |
| Deploy / Release Checklist | Required | GitHub delivery after current gates | design.md#deploy--release-checklist | AC-09; no other publication or user installation |
| AI Involvement Note | Required | AI-assisted artifacts and review provenance | design.md#ai-involvement-note | Honest chronology, actual evidence and explicit limitations |

## Validation Strategy

Use the exact Verify argv in `tasks.md`. Test the public boundaries with isolated fixtures and independently defined expectations. Main records actual red/green evidence or explicitly discloses the missing original baseline; existing fixes must not be reverted in the shared checkout to manufacture a red phase. Use isolated unfixed snapshots when available. Main must bind final successful runs and independent reviews to the final source. Evidence reuse requires matching command, scope and current source. Initial handoff status is in notes.md.

## Risks And Open Questions

No unresolved requirements or delegated contract choices remain for this scope. Technical risks are shared snapshot regressions, false-positive secret filtering, and confusing selected capabilities with present payloads. Evidence availability, concurrent source changes, and independent review are pending delivery obligations, not proof of success.

## Traceability / 追溯关系矩阵

| Scenario | Requirement | Acceptance | Task | Evidence State |
|---|---|---|---|---|
| SCN-01 | REQ-01 | AC-01 | T001, T005 | Pending |
| SCN-02 | REQ-02 | AC-02 | T002, T005 | Pending |
| SCN-03 | REQ-03 | AC-03 | T003, T005 | Pending |
| SCN-04 | REQ-04 | AC-04, AC-05 | T004, T005 | Pending |
| SCN-05 | REQ-05 | AC-06 | T003, T005 | Pending |
| SCN-06 | REQ-06 | AC-07 | T003, T005 | Pending |
| SCN-07 | REQ-07 | AC-08, AC-09 | T005 | Pending; artifact validation alone is insufficient |

## Next SDC Step

Main reviews the package, reconciles repaired source and measured evidence, completes independent review and runtime gates, and performs the authorized GitHub push. Initial handoff status is recorded separately in notes.md.
