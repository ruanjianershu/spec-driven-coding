# Discovery

Change: `2026-09-24-compact-workflow-upgrade`. Record date: 2026-09-24.
Format: STANDARD. Current repair scope is confirmed; historical gates are not reconstructed.

## Current Understanding

The compact/guidance/doctor/findings upgrade was already coded without a formal change package. The assistant subsequently reproduced six issues during verification. The current user directs fixing the reported issues and pushing to GitHub. This whole change includes production repairs, tests, current runtime evidence, independent review and GitHub delivery.

Artifact preparation is one delegated step. Pending fields describe initial handoff status, not permanent acceptance requirements. Main reviews this package before runtime gates.

## Input Evidence

| ID | Source | Status | Scope |
|---|---|---|---|
| U-01 | Current user instruction, English translation: "Fix the issues, then push to GitHub." | Confirmed | Repair reported issues and deliver to GitHub; not detailed technical requirements |
| U-02 | Earlier user direction, English translation: "Upgrade according to your understanding." | Prior direction relayed by lead agent | Upgrade intent and engineering discretion, not a historical formal gate |
| U-03 | Earlier user direction, English translation: "Perform full verification." | Prior direction relayed by lead agent | Verification request, not proof of passing tests |
| A-01 | Lead agent's artifact-preparation/reconciliation instructions and provenance corrections | Delegated strategy | STANDARD artifacts, honest chronology, public-safe English content, bounded writer authority and main review before gates |
| A-02 | Assistant's reproduced verification report, relayed by lead agent | Reported technical evidence | F-001 through F-006; not user-authored requirements or reproductions by this artifact writer |
| A-03 | Lead agent's current measured-result and coverage updates | Attributed results | 245 tests, 74 flows and 4 installed tests reported passing; new retarget/ledger-rewrite cases reported freshly passing; full rerun count not asserted |
| H-01 | `docs/plans/2026-09-24-compact-workflow-upgrade.md` | Historical record | Earlier scope and claimed results, not current receipts |
| S-01 | `.sdc/constitution.md`, `.sdc/project.md`, standards and artifact schemas | Inspected | Existing engineering and schema contracts |
| S-02 | `impact.md#evidence-index` | Inspected source map | Affected staging, doctor, findings, snapshot, reviewer and test boundaries |

User wording is explicitly translated. Lead-agent delegation is not attributed to the user as a quote or new explicit decision.

## Reported Findings

| ID | Assistant-Reproduced Issue | Repair Target |
|---|---|---|
| F-001 | Frozen evaluator omits required runtime imports | Runnable bounded frozen staging |
| F-002 | Equal payload conceals missing effective Claude skill selection | Effective registration diagnosis |
| F-003 | Findings helpers are resolved from the product project | Installed plugin/runtime paths |
| F-004 | Filtered tracked code and non-Git directory symlinks escape compact freshness | Source coverage and freshness |
| F-005 | An absent findings.json null snapshot key breaks older STANDARD receipts | Compatible absent-ledger shape |
| F-006 | Harmless long reviewer attribution is rejected as sensitive | Narrow prose-label acceptance with secret defenses |

Source and tests changed during inspection. Candidate repairs and A-03 results are reconciliation inputs; main owns the final source identity, actual outputs and completion updates.

## Intake Coverage

| Category | Established Understanding | Source And Scope | Blocking? |
|---|---|---|---|
| Project context | Existing local-first SDC plugin/CLI and Brownfield adapters | S-01; package.json; inspected code | No |
| Core scope | Finish upgrade, repair reported defects, verify and push to GitHub | U-01 through U-03; A-02; H-01 | No |
| Technical preferences | Preserve Python standard-library helpers, Node.js and current lifecycle/contracts | Existing contracts; engineering judgment within U-02 | No |
| Constraints and acceptance | Current evidence/review before GitHub delivery; no additional publication/install target | U-01; A-01; SDC policy | No |

## Authorization And Risk

U-01 authorizes repairs to A-02's reported issues and GitHub delivery. Detailed ACs derive from those defects and existing contracts, not extra user quotations. The current GitHub direction supersedes H-01's prior no-push limit; it does not authorize npm publication, internal GitLab delivery or user installation.

A-01 limits this artifact writer to this change directory and schema validation without production/Git/runtime edits or gate advancement. That temporary delegation is not a whole-change prohibition. Main reviews artifacts before gates.

STANDARD is the format. Risk is strict under existing workflow-standards triggers for shared path/source freshness, approval compatibility and secret screening. Stop on new business scope, unsupported contract decisions, inadequate evidence or unresolved blocking findings.

## Knowledge Sources Used

Read the knowledge index; relevant product overview/flows/rules/decisions/domain and technical stack/architecture/modules/data-and-interfaces/operations/testing; cognition; Common Ground; expert routing; standards, schemas and templates; the earlier plan; and affected source/tests in impact.md.

Root knowledge/cognition are mostly empty templates or Candidate entries, not confirmed behavior. Relevant sdc-references include workflow-standards, discovery-gate, legacy-impact-gate, execution-orchestration, artifact-output-contracts, compact-workflow, installation-diagnostics, review-findings, domain-knowledge and test-quality.

## Knowledge Gaps

No unresolved requirement or technical planning gap blocks this bounded plan. This writer has not inspected original failure outputs or main's full logs/snapshots. Main owns current evidence and baseline-limit disclosure; no result is invented.

## Common Ground And Expert Routing

No root candidate is promoted. User direction establishes scope; A-02 and inspected contracts establish technical repair context. Use legacy-modernizer, api-contract, security, test-strategy and documentation as internal lenses, not approval authorities.

## Candidate Directions

| Option | Description | Tradeoff | Status |
|---|---|---|---|
| A | Reconcile honestly, repair and complete current gates before GitHub delivery | Preserves prior work without invented history | Selected engineering strategy under A-01 and SDC policy |
| B | Treat old checked tasks as formal approval | Fabricates provenance | Rejected |
| C | Use compact format for runtime repairs | Violates prose-only eligibility | Rejected by existing contract |

## Tradeoffs

Keep existing modules and entrypoints. Use bounded fixes and discriminating regressions, not a broader client parser or new evidence architecture. Reuse evidence only when command, scope and source match.

## Recommended MVP

Repair F-001 through F-006, preserve the original upgrade and its gates, complete verification and independent review, and perform the authorized GitHub push.

## Decision Ledger

| ID | Decision | Status | Source | Impact | Next Step |
|---|---|---|---|---|---|
| D-01 | Reconcile already-coded work in STANDARD without backdated gates | Confirmed | A-01 strategy; SDC schema/evidence policy | Historical integrity | Main reviews package |
| D-02 | Repair six reported defects within existing contracts | Confirmed | U-01 refers to A-02; engineering judgment | REQ-01 through REQ-07 | T001-T005 |
| D-03 | Completion requires actual current evidence and independent review | Confirmed | Existing SDC policy; A-01 | Evidence integrity | Main records outcomes |
| D-04 | Push to GitHub after current repair/delivery gates | Confirmed | U-01; A-01 delivery boundary; SDC policy | Authorized delivery | Main records pushed revision |
| D-05 | Use strict risk controls with STANDARD format | Confirmed | Existing risk triggers; engineering assessment | Compatibility/security checks | Review affected risks |
| D-06 | Do not infer live-client or token gains from local tests | Confirmed | Existing test-quality policy; H-01 limits | Accurate claims | Disclose limits |

## Decision Provenance

Confirmed engineering choices are selected within existing authority/contracts, not separately quoted user decisions. Main's artifact review remains pending.

## Artifact Output Contract

Eight required outputs are in design.md: process/state flow, integration flow, CLI/API contract, snapshot compatibility, CLI states, Test Matrix, GitHub checklist and AI involvement note.

## Open Questions

None.

## Exit Criteria

- [x] U-01 establishes current repair/GitHub scope referring to A-02.
- [x] Engineering choices stay within existing contracts and U-02 discretion.
- [x] Acceptance derives from reported defects, existing behavior and U-03 verification.
- [x] A-01 authorizes preparation; main reviews before runtime gates.

These are current intake facts, not historical gates or lifecycle transitions.
