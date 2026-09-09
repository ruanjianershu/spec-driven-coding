# Context Pack

## Goal

Implement the smallest local Gate Evidence schema and direct fail-closed proof, using only the exact Base validator and Markdown task/review handoffs so the downstream chain has a reviewable local schema/provenance input without profile, runtime, default-command, or external-authority behavior.

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| spec.md | Confirmed | REQ-GE-01 through REQ-GE-03 and ACs | Defines scope and acceptance. |
| impact.md | Confirmed | Direct impact list and Base constraint | Defines Brownfield file radius. |
| design.md | Confirmed | Contract, matrix, and Global Constraints | Defines execution interfaces. |
| ANDY-143 / ANDY-151 / ANDY-157 inputs | Confirmed | Scope, Layout A, and root-cause evidence | Bind exact boundary and behavior. |
| Exact Base source evidence | Confirmed | Standard, audit, CLI, task/review helper inspection | Protects existing behavior and handoff compatibility. |
| Portable plan review bundle | Confirmed | ANDY-157 independent revalidation requirement | Provides a persistent, locally verified source for the exact nine-file revision. |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

No knowledge gap affects execution of this narrow local slice.

## Common Ground Used

| ID | Tier | Statement | Source | Why It Matters |
|---|---|---|---|---|

The Common Ground file has no rows.  This handoff relies on confirmed issue inputs and direct Base evidence.

## Expert Profiles Used

| Profile | Why Used | Sources Read | Decisions / Checks Affected |
|---|---|---|---|
| legacy-modernizer | Brownfield edit to a shared standard and audit boundary. | impact.md; Base standard/audit source | Exact Base/range, file restriction, rollback. |
| documentation | Authoritative surface is a durable standards document. | Base standard; proposal.md | Exact wording and heading placement. |
| test-strategy | Every fail-closed case needs deterministic acceptance coverage. | spec.md; Base Python test convention; design.md | Red/green order and test matrix. |

## Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | N/A | `Status` is a documentation field | design.md#process-state-diagrams | N/A because no product workflow or runtime state machine changes. |
| Sequence / Integration Diagram | N/A | No integration is permitted | design.md#sequence-integration-diagrams | N/A because validation is local with no external call. |
| API / Contract Specification | Required | Versioned Markdown contract | design.md#gate-evidence-contract | Gives exact field and local-boundary rules. |
| Data Model / Migration Contract | N/A | No persistent data impact | design.md#data-model-migration-contract | N/A because no stored data model or migration exists. |
| UX Flow / Interaction States | N/A | No UI impact | design.md#ux-flow-interaction-states | N/A because there is no user-facing behavior. |
| Test Matrix | Required | AC validation | design.md#test-matrix | Covers compliant and every required malformed local record plus T000 handoff. |
| Deploy / Release Checklist | N/A | No deploy/config/release impact | design.md#deploy-release-checklist | N/A because deployment and release are outside scope. |
| AI Involvement Note | Required | AI-assisted delivery | design.md#ai-involvement-note | Human authorization and independent review stay mandatory. |

## Global Constraints

| ID | Constraint | Source | Applies To |
|---|---|---|---|
| GC-GE-01 | Create an isolated implementation branch directly from `origin/main@e10a5d221f081fb6d099d342597a707b0dad91c9`. Before T000, `HEAD` must equal that exact Base SHA and porcelain status must be empty. | ANDY-157; exact Base inspection | T000-T900 |
| GC-GE-02 | From Base through a reviewed content candidate, only `sdc-references/workflow-standards.md`, `tests/test_gate_evidence_schema.py`, and `.sdc/changes/active/2026-09-08-gate-evidence-schema/` may change. `sdc-cli.py`, `scripts/`, profiles, hooks, packages, JSONL context manifests, and lifecycle-state files must remain unchanged. | ANDY-143/151 scope; impact.md | T000-T900 |
| GC-GE-03 | Require exactly one `Status: Closed`, `Resolution ID`, `Resolution Source`, `Closure ID`, and `Closure Source`; IDs use lowercase `8-4-4-4-12` hexadecimal text. | ANDY-151 decisions; spec.md | T001-T003 |
| GC-GE-04 | Each named source appears exactly once, is nonempty after trim, and is opaque local Markdown text; do not parse, open, dereference, or authenticate it. | ANDY-151 decision; spec.md | T001-T003 |
| GC-GE-05 | Reject missing fields, noncanonical IDs, a non-Closed status, duplicate/blank named sources, and duplicate Gate Evidence sections. | spec.md#AC-GE-02 | T001-T003 |
| GC-GE-06 | Insert the new section after `## Evidence Discipline`; preserve the existing `## Task Format ... ## Evidence Discipline` audit boundary. | Base `scripts/audit-release.mjs`; impact.md | T002-T900 |
| GC-GE-07 | T000 must not invoke, add, or depend on `scripts/sdc-runtime-context.py`, a JSONL context manifest, or lifecycle state. It validates the nine Markdown artifacts with Base `sdc-cli.py`; Base `sdc-task-brief.py` and `sdc-review-package.py` may create only ignored Markdown handoffs under `.sdc/runtime/2026-09-08-gate-evidence-schema/`. | ANDY-157; Base helper/schema inspection | T000-T900 |
| GC-GE-08 | Each behavioral or scope review binds one clean committed full SHA and the exact `Base..candidate` range. A later durable evidence update may change only this focused package's `tasks.md` and `notes.md`, cites the reviewed SHA, and requires a new candidate/review if it changes any product file. | execution-orchestration.md; spec.md#REQ-GE-03 | T000-T900 |
| GC-GE-09 | Do not start T000 until a human explicitly authorizes Apply and names both the exact plan-revision commit and authorized PR controller. This planning run neither creates nor merges a PR. | ANDY-151 completion condition; ANDY-157 boundary | T000-T900 |
| GC-GE-10 | Before T000, obtain the attached portable plan review bundle, its recorded SHA-256 digest, and exact revision. Verify the digest and `git bundle verify`; use `git clone --no-checkout` only into temporary scratch, prove `Base` is an ancestor of the revision, and compare the complete sorted `Base..revision` changed-path list to the fixed nine repository-relative package paths before import. This transport is not a runtime-context, manifest, state, or candidate-diff path. | ANDY-157 independent revalidation requirement; Git bundle behavior | T000 |

## Execution Orchestration

- Plan Preflight: Passed
- Preflight Evidence: portable-bundle replay from an isolated clean Base
- Mode: Serial test-first execution with one implementer and one independent read-only reviewer per task
- Runtime Workspace: .sdc/runtime/2026-09-08-gate-evidence-schema/
- Task Review: Spec Compliance + Code Quality
- Final Whole-Change Review: Required

The runtime workspace holds ignored Markdown briefs, reports, ledgers, and review packages only.  It is not a JSON manifest/state interface and cannot be the sole durable evidence location.

## Confirmed Product Knowledge

No product behavior is changed.  The confirmed business boundary is local document format and consistency only; no external system is authenticated or represented as authoritative.

## Confirmed Technical Knowledge

- Base `sdc-cli.py validate <change>` validates the full active Markdown package.
- Base `scripts/sdc-task-brief.py` reads tasks/context and emits Markdown brief/report/ledger under ignored runtime scratch.
- Base `scripts/sdc-review-package.py` emits a review diff package under the same runtime scratch.
- Base does not contain the former runtime-context script or a JSONL context-manifest/lifecycle-state schema.

## Execution Boundaries

- Start only from GC-GE-01 Base after the human Apply gate in GC-GE-09.
- Verify GC-GE-10's bundle digest, integrity, exact revision, Base ancestry, and complete sorted fixed nine-path equality before importing, staging only that package, committing `H0`, and validating it before source editing.
- Change only the allowlisted paths in GC-GE-02; any other needed path stops execution for a new confirmed plan.
- Keep all validation local except the authorized PR controller's explicit same-head query.
- Keep durable review results in tracked tasks/notes; ignored runtime scratch is recovery context.

## Forbidden Assumptions

- Do not assume a file existing in a divergent planner worktree exists in the Base.
- Do not infer a JSON schema from an ignored runtime directory.
- Do not treat document presence as a Gate-Closed profile or external authority certification.
- Do not start T000 from an authorization supplied by an agent instead of a human.
- Do not treat an executor-local Git object as the plan source when the attached recorded-digest bundle is unavailable or fails verification.
- Do not substitute a different PR head for the recorded review candidate.

## Task And Traceability Summary

| Task | Requirement / Acceptance | Handoff |
|---|---|---|
| T000 | REQ-GE-03 / AC-GE-03 | Clean Base, verified plan bundle, nine-file package, validator, and ignored T000 brief/review package. |
| T001 | REQ-GE-02 / AC-GE-02 | Red direct test. |
| T002 | REQ-GE-01, REQ-GE-02 / AC-GE-01, AC-GE-02 | Green standard/test candidate. |
| T003 | REQ-GE-01, REQ-GE-02, REQ-GE-03 / AC-GE-01, AC-GE-02, AC-GE-03 | Same-head PR checkpoint and full range checks. |
| T004 | REQ-GE-01, REQ-GE-02, REQ-GE-03 / AC-GE-01, AC-GE-02, AC-GE-03 | Independent exact-range review. |
| T900 | REQ-GE-01, REQ-GE-02, REQ-GE-03 / AC-GE-01, AC-GE-02, AC-GE-03 | Final candidate and whole-change review. |

## Validation Commands

- `git cat-file -e "${BASE}:sdc-cli.py"`
- `! git cat-file -e "${BASE}:scripts/sdc-runtime-context.py"`
- `test "$(shasum -a 256 "$SDC_PLAN_BUNDLE" | awk '{print $1}')" = "$SDC_PLAN_BUNDLE_SHA256" && git bundle verify "$SDC_PLAN_BUNDLE"`
- `set -o pipefail; EXPECTED_PLAN_PATHS="$(printf '%s\n' ".sdc/changes/active/$CHANGE/context-pack.md" ".sdc/changes/active/$CHANGE/design.md" ".sdc/changes/active/$CHANGE/discovery.md" ".sdc/changes/active/$CHANGE/impact.md" ".sdc/changes/active/$CHANGE/knowledge-candidates.md" ".sdc/changes/active/$CHANGE/notes.md" ".sdc/changes/active/$CHANGE/proposal.md" ".sdc/changes/active/$CHANGE/spec.md" ".sdc/changes/active/$CHANGE/tasks.md" | LC_ALL=C sort)"; ACTUAL_PLAN_PATHS="$(git -C "$PLAN_SOURCE" diff --name-only "$BASE..$SDC_PLAN_REVISION" | LC_ALL=C sort)"; test "$ACTUAL_PLAN_PATHS" = "$EXPECTED_PLAN_PATHS"`
- `set -o pipefail; git show "${BASE}:sdc-cli.py" | python3 - validate 2026-09-08-gate-evidence-schema`
- `python3 scripts/sdc-task-brief.py 2026-09-08-gate-evidence-schema T000`
- `python3 scripts/sdc-review-package.py "$BASE" "$CANDIDATE" 2026-09-08-gate-evidence-schema T000`
- `python3 tests/test_gate_evidence_schema.py`
- `git diff --check "$BASE..$CANDIDATE"`
- `git diff --name-only "$BASE..$CANDIDATE"`

## Knowledge Candidate Routing

No candidate is promoted during planning.  Apply or Check records a later durable discovery in `knowledge-candidates.md` with source, evidence needed, target, and archive promotion gate; it does not change long-lived knowledge without required confirmation.
