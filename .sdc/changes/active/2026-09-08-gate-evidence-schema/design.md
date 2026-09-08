# Gate Evidence Schema Design

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| spec.md | Confirmed | REQ-GE-01 through REQ-GE-03 and ACs | Defines implementation contract. |
| impact.md | Confirmed | Direct paths and Base boundary | Defines Brownfield radius. |
| Base `workflow-standards.md` | Confirmed | Existing heading order and Evidence Discipline | Defines target and placement boundary. |
| Base `scripts/audit-release.mjs` | Confirmed | Bounded Task Format scan | Protects audit compatibility. |
| Base `sdc-cli.py` | Confirmed | Active-change validation | Defines plan validation boundary. |
| Base task/review helpers | Confirmed | Tracked helper source | Defines ignored Markdown handoff without a JSON schema. |
| Portable plan review bundle | Confirmed | ANDY-157 independent revalidation requirement | Defines the independently retrievable, locally verified source of the nine planning artifacts. |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

No knowledge gap affects the selected local documentation/test slice.  Empty project knowledge and cognition templates are not used as facts.

## Common Ground Used

| ID | Tier | Statement | Source | Why It Matters |
|---|---|---|---|---|

The Common Ground file has no rows.  Direct issue and exact Base evidence are the sole inputs to this design.

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

## Plan Preflight

- Status: Passed
- Reviewed Against: spec.md, impact.md, design.md, tasks.md, context-pack.md, Artifact Output Contract, Base `sdc-cli.py`, Base task/review helpers, portable-bundle replay, and execution-orchestration.md
- Findings: Resolved: the former missing runtime-context dependency, undeclared JSON schemas, allowlist mismatch, executor-local-only plan revision, zsh Git-object pipeline masking, cardinality-only package acceptance, implicit H0 materialization, inconsistent Apply gate, and task-trace mismatch are removed; each task now has a Base-existing interface and verification command.
- Result: T000 is reproducible from the exact Base with a recorded-digest, independently retrievable nine-file bundle, Base validation, and Base Markdown handoffs.  Human Apply authorization remains an execution gate.

## Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | N/A | `Status` is a documentation field | design.md#process-state-diagrams | N/A because no business workflow or runtime state machine is touched. |
| Sequence / Integration Diagram | N/A | No integration is in scope | design.md#sequence-integration-diagrams | N/A because validation is local and makes no external call. |
| API / Contract Specification | Required | Versioned Markdown contract | design.md#gate-evidence-contract | Specifies exact field names, cardinality, and local-only boundary. |
| Data Model / Migration Contract | N/A | No stored schema/migration | design.md#data-model-migration-contract | N/A because no persistent data model changes. |
| UX Flow / Interaction States | N/A | No UI surface | design.md#ux-flow-interaction-states | N/A because this is a documentation/test-only slice. |
| Test Matrix | Required | Fail-closed acceptance validation | design.md#test-matrix | Maps every acceptance criterion to a command and expected result. |
| Deploy / Release Checklist | N/A | No deploy/config/release behavior | design.md#deploy-release-checklist | N/A because deployment and release are excluded. |
| AI Involvement Note | Required | AI-assisted plan and implementation | design.md#ai-involvement-note | Names human authorization and independent review requirements. |

## Solution Summary

Use a single versioned Markdown section plus one self-contained direct Python test. T000 locally verifies the digest, Git-bundle integrity, revision, Base ancestry, and the complete sorted fixed nine-path set of the approved package at the exact Base before it imports, stages only that package, commits `H0`, and invokes Base `sdc-cli.py validate` through a `set -o pipefail` pipeline using `${BASE}:path` syntax; it does not materialize a state file or context manifest. Existing Base task/review helpers create ignored Markdown handoffs after validation. This makes the plan independently reviewable without changing SDC runtime behavior.

## Runtime Context Handoff

The supported Base handoff is not a JSON schema.  The portable Git bundle is a review/package transport only, not an execution-runtime interface.  `scripts/sdc-task-brief.py <change> <T###>` reads `tasks.md` and `context-pack.md` and writes `task-T###-brief.md`, `task-T###-report.md`, and `progress.md` under ignored `.sdc/runtime/<change-id>/`.  `scripts/sdc-review-package.py <base> <head> <change> <label>` writes a task or final review package in the same runtime directory.  T000 verifies these outputs exist after the Base validator passes; durable facts remain in the tracked package.

## Impact Scope

- `sdc-references/workflow-standards.md`: one authoritative Layout A section.
- `tests/test_gate_evidence_schema.py`: one direct local fail-closed test suite.
- The focused Markdown package: source, traceability, review plan, validation evidence, and durable outcomes.

## Non-Scope

- `sdc-cli.py`, `scripts/`, JSONL manifests, lifecycle state, Gate-Closed profiles, default validation dispatch, package metadata, public commands, and external systems.
- URL parsing, source-target I/O, external authority validation, persistence, deployment, and release workflows.

## Key Tradeoffs

- A test-local checker proves the standard without coupling a static documentation rule to default SDC validation.
- The Base validator and tracked handoff helpers provide reproducible execution inputs without inventing a new runtime protocol.
- Opaque source text satisfies the local-only predicate while avoiding a new path/link grammar.
- A fixed standard location protects the existing Task Format audit contract.

## Gate Evidence Contract

The new `## Gate Evidence` section is placed after `## Evidence Discipline` and before the next peer heading.  It declares a single record shape whose fields occur once each in this order:

1. `Status` has exactly literal value `Closed`.
2. `Resolution ID` has lowercase hexadecimal groups of `8-4-4-4-12` characters.
3. `Resolution Source` is present once and remains nonempty after trim.
4. `Closure ID` has the same confirmed UUID textual shape.
5. `Closure Source` is present once and remains nonempty after trim.

The standard states that a missing field, duplicate field, malformed ID, status other than `Closed`, blank named source, or more than one Gate Evidence section is invalid.  Source values remain local opaque Markdown text: validation neither parses nor accesses a target and makes no authority claim.

## Data, API, State, or Interaction Changes

No runtime data, API, lifecycle state, interaction, or public behavior changes occur.  The required contract artifact is a versioned Markdown document interface only.

## Process / State Diagrams

N/A because `Status: Closed` is a record field and this change does not touch a product workflow or runtime state machine.

## Sequence / Integration Diagrams

N/A because the test performs no network, service, queue, webhook, or external-system interaction.

## API / Contract Specification

The contract is the versioned Markdown Layout A described in `Gate Evidence Contract`.  It has no endpoint, request, response, permission, or compatibility surface beyond exact named fields and the local validation boundary.

## Data Model / Migration Contract

N/A because no persistent data, migration, transaction, index, or rollback data concern exists.

## UX Flow / Interaction States

N/A because no user-facing screen, form, error display, or accessibility behavior is touched.

## Test Matrix

| AC | Scenario | Level | Verification | Expected Result | Owner / Status |
|---|---|---|---|---|---|
| AC-GE-01 | Standard contains one Layout A section in the audit-safe location. | Direct documentation test | `python3 tests/test_gate_evidence_schema.py` | Compliant standard fixture is accepted and placement/cardinality assertions pass. | Apply implementer / Required |
| AC-GE-02 | Malformed local records exercise every fail-closed rule. | Direct unit test | `python3 tests/test_gate_evidence_schema.py` | Invalid ID, missing field, non-Closed status, bad named source, and duplicate section are rejected. | Apply implementer / Required |
| AC-GE-03 | T000 uses only Base-existing plan validation and Markdown handoff interfaces. | Clean-base bundle replay | T000 commands in tasks.md | Recorded digest, bundle, revision ancestry, and exact fixed nine-path equality validate; expected ignored handoff files appear; missing runtime-context dependency is never invoked. | Apply implementer / Required |

## Deploy / Release Checklist

N/A because no configuration, deployment, service restart, package publication, or release action is part of this change.

## AI Involvement Note

AI prepares the package and may implement only after explicit human Apply confirmation.  Human review verifies exact Base/candidate range, local-only scope, field wording, test coverage, and diagnostic boundaries.  Reviewers are independent and read-only.

## Brownfield Impact Summary

This is a Brownfield change.  `impact.md` limits product-file radius to the shared standard and one direct test.  Existing project-cognition and technical-knowledge files are templates without relevant confirmed rows, so this summary relies on direct source inspection.

## REQ/AC to Design Decision Mapping

| REQ | AC | Design Decision |
|---|---|---|
| REQ-GE-01 | AC-GE-01 | Add one audit-safe Layout A standard section. |
| REQ-GE-02 | AC-GE-02 | Use one standard-library direct test and test-local fixtures. |
| REQ-GE-03 | AC-GE-03 | Validate the nine-file package with Base `sdc-cli.py` and use only Base Markdown handoff helpers. |

## Risks, Rollback, and Migration

- Risk: a heading inserted inside the Task Format body breaks release audit.  Mitigation: fixed placement after `## Evidence Discipline` and direct placement assertion.
- Risk: a static test grows into a runtime validator.  Mitigation: no runtime implementation task and changed-path review.
- Risk: opaque source text appears in a failure message.  Mitigation: diagnostics report only field/rule class.
- Risk: a later worktree helper is treated as a Base dependency.  Mitigation: T000 verifies Base paths before any source edit.
- Risk: an executor-local-only plan commit cannot be independently reviewed.  Mitigation: attach a portable Git bundle and digest manifest, then replay it from a clean Base before Preflight passes.
- Rollback: revert the standard section and direct test as one Git range; no data migration or runtime rollback exists.
