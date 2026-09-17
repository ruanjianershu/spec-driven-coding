# Gate Evidence Schema Specification

## 0. Document Metadata

- Status: Confirmed
- Change: `2026-09-08-gate-evidence-schema`
- Exact implementation baseline: `origin/main@e10a5d221f081fb6d099d342597a707b0dad91c9`
- Scope authority: ANDY-143, ANDY-151, and ANDY-157 issue inputs.

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| discovery.md | Confirmed | DEC-GE-001 through DEC-GE-009 | Provides closed discovery inputs. |
| ANDY-143 / ANDY-151 inputs | Confirmed | Scope and Layout A decisions | Define the local contract and non-scope. |
| ANDY-157 input | Confirmed | Clean-base preflight failure | Requires removal of the impossible runtime dependency. |
| Base `sdc-cli.py` | Confirmed | Active-change validation implementation | Defines the supported plan validation command. |
| Base `scripts/sdc-task-brief.py` / `sdc-review-package.py` | Confirmed | Tracked helper source | Defines the Markdown runtime handoff used after validation. |
| Portable Git bundle review object | Confirmed | ANDY-157 independent revalidation requirement | Makes the exact nine-file plan revision independently readable and locally verifiable. |
| Base standards, audit, and test sources | Confirmed | Direct Git-object inspection | Define placement, scope, and test conventions. |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

No knowledge gap affects this narrow local documentation/test slice.  Project knowledge and cognition files are empty templates and are not used as factual input; technical facts here come from the exact Base and confirmed issue inputs.

## Common Ground Used

| ID | Tier | Statement | Source | Why It Matters |
|---|---|---|---|---|

The Common Ground file has no rows.  No Common Ground item drives this specification.

## Decision Ledger

| ID | Decision | Status | Source | Allows REQ/AC | Effect |
|---|---|---|---|---|---|
| DEC-GE-001 | Layout A field names and literal closed value. | Confirmed | discovery.md / ANDY-151 input | Yes | Defines the standard section. |
| DEC-GE-002 | Lowercase `8-4-4-4-12` hexadecimal textual UUID shape. | Confirmed | ANDY-143 / ANDY-151 inputs | Yes | Defines accepted IDs. |
| DEC-GE-003 | Each named source is exactly once, trim-nonempty opaque local text. | Confirmed | discovery.md | Yes | Defines provenance consistency. |
| DEC-GE-004 | Direct local test only; no default command, runtime, or profile change. | Confirmed | ANDY-143 scope and Base inspection | Yes | Limits implementation surface. |
| DEC-GE-006 | T000 uses Base validator and Base Markdown task/review handoffs, never JSON manifest/state generation. | Confirmed | ANDY-157 root cause and Base inspection | Yes | Makes clean-base execution reproducible. |
| DEC-GE-007 | T000 verifies a portable Git bundle digest, exact revision, Base ancestry, and equality of the complete sorted `Base..revision` changed-path list to the fixed nine package paths before import. | Confirmed | discovery.md / ANDY-157 independent revalidation | Yes | Removes executor-local revision availability and cardinality-only package acceptance as implicit prerequisites. |
| DEC-GE-008 | T000 uses `set -o pipefail` and `${BASE}:path` syntax for Git-object pipelines. | Confirmed | discovery.md / isolated zsh replay | Yes | Preserves fail-closed behavior across the supported local shell. |
| DEC-GE-009 | T000 stages only the verified package directory and creates `H0` before Base validation and handoff. | Confirmed | discovery.md / isolated Base replay | Yes | Makes the imported artifact set the actual reviewed candidate. |

## Discovery Summary

Discovery is complete: field semantics, local-only provenance behavior, direct proof surface, and the Base-supported T000 handoff are all fixed by confirmed inputs and repository evidence.

## Glossary

- Gate Evidence: the local versioned Markdown record specified by this change.
- Resolution ID / Closure ID: the two distinct lowercase UUID textual fields in the record.
- Named source: the source field paired with one ID; it is opaque text checked only for exactly one nonblank occurrence.
- Runtime handoff: ignored Markdown task brief, implementer report, progress ledger, and review package emitted by existing Base helpers.
- Plan review bundle: a portable Git bundle attached with its SHA-256 digest; it transports the nine planning artifacts only and is not a runtime-context or lifecycle interface.
- Fail closed: reject a record whenever a required layout, ID, status, or named-source rule is violated.

## Background And Goal

The downstream planning chain needs one durable local schema/provenance input.  The goal is a concise standard plus deterministic direct proof and a clean Base handoff, not a runtime feature or an external-control-plane assertion.

## In Scope

- One `## Gate Evidence` section in `sdc-references/workflow-standards.md`.
- One direct Python `unittest` test file with test-local positive and negative record fixtures.
- Nine governed Markdown change artifacts and Base-supported ignored task/review handoffs.

## Out of Scope

- Gate-Closed profile behavior, `sdc-cli.py`, default `validate` behavior, package behavior, public command behavior, and product behavior.
- `scripts/sdc-runtime-context.py`, JSONL context manifests, lifecycle state, and any new runtime schema.
- External target parsing, network access, external authority authentication, deployment, publishing, and release actions.
- UUID version/variant restrictions beyond the confirmed lowercase `8-4-4-4-12` hexadecimal textual form.

## Business Invariants / 业务不变量

### INV-GE-01

The standard uses exactly `Status`, `Resolution ID`, `Resolution Source`, `Closure ID`, and `Closure Source`.

### INV-GE-02

The only accepted status value is `Closed`; each ID matches the confirmed lowercase `8-4-4-4-12` hexadecimal textual UUID form.

### INV-GE-03

Each named source appears exactly once and is nonempty after trimming; neither source is parsed, resolved, opened, or authenticated.

### INV-GE-04

The direct proof is fail-closed and does not change runtime, profile, or default command behavior.

### INV-GE-05

T000 consumes only Base-existing tools, nine Markdown artifacts, and a locally verified portable plan review bundle; an absent runtime-context script or JSON schema cannot be an implicit execution prerequisite.

## Scenarios And Requirements

### SCN-GE-01 — A downstream planner needs a durable local contract

#### REQ-GE-01

`sdc-references/workflow-standards.md` must define one `## Gate Evidence` section after `## Evidence Discipline`.  It must state the five exact fields, literal `Closed` value, lowercase `8-4-4-4-12` hexadecimal ID rule, exactly-once source rule, and local-only provenance boundary.

### SCN-GE-02 — A maintainer checks a local record before relying on it

#### REQ-GE-02

`tests/test_gate_evidence_schema.py` must directly prove the contract with test-local fixtures.  It must accept a compliant record and reject an invalid ID, missing required field, status other than `Closed`, missing/duplicate/whitespace-only named source, and more than one Gate Evidence section.  Diagnostics identify rule/field class without echoing opaque source text.

### SCN-GE-03 — The documentation slice starts from a reproducible Base

#### REQ-GE-03

T000 must start from a clean exact Base, verify the SHA-256 digest and Git-bundle integrity of the human-supplied plan review bundle, prove its exact plan-revision commit descends from the Base, compare the complete sorted `Base..revision` changed-path list with a fixed nine repository-relative Markdown path allowlist, import only that exact set, stage only that package directory, and create committed `H0`. Its shell verification must enable `set -o pipefail` and use `${BASE}:path` syntax for Git-object paths. It must pass `sdc-cli.py validate 2026-09-08-gate-evidence-schema` and use only the tracked Base task/review helpers for ignored handoff files. It must not invoke, add, or depend on `scripts/sdc-runtime-context.py`, JSONL context manifests, or lifecycle state.

## Acceptance Criteria / 验收标准

### AC-GE-01

Given the exact Base standard has no Gate Evidence contract, when T002 adds the governed section, then the standard contains exactly one Layout A section with the five confirmed fields and their exact local validation rules.

### AC-GE-02

Given the direct local test and its fixtures, when it evaluates compliant and malformed records, then the compliant record passes and every required malformed category is rejected without external lookup or opaque-source-value output.

### AC-GE-03

Given a human has authorized Apply and supplied the attached plan review bundle, its SHA-256 digest, and an exact plan-revision commit, when T000 runs from `e10a5d221f081fb6d099d342597a707b0dad91c9`, then it verifies the bundle, imports, stages, commits, and validates the exact nine Markdown artifacts, emits the existing ignored Markdown handoff, and fails before source editing if the Base, digest, bundle, revision ancestry, sorted fixed package-path equality, staging scope, validator pipeline, helper, or changed-path allowlist check is invalid. The candidate diff never changes `sdc-cli.py`, `scripts/`, profiles, packages, JSONL manifests, or lifecycle state.

## Non-Functional Constraints

- The test uses only the Python standard library and local repository files.
- The test does not make network calls, parse URLs, or open a named source target.
- The Task Format section remains byte-for-byte outside the new section's placement boundary.
- Commands and evidence use repository-relative paths and full Git object IDs.
- Runtime handoff files stay under ignored `.sdc/runtime/2026-09-08-gate-evidence-schema/`; durable review conclusions stay in `tasks.md` and `notes.md`.
- The plan review bundle is checked locally from its recorded digest; T000 does not fetch or publish it over a network.

## Validation Strategy

- T000 proves the clean Base, recorded-digest plan review bundle, exact fixed nine-path plan package, Base validator, and Base task/review handoff before any standard/test edit.
- T001 writes and executes the red direct test against the section-absent Base.
- T002 adds the section and reruns the same direct test green.
- T003 captures a clean full candidate SHA, validates the full allowed range, and has the authorized controller confirm the PR head equals that SHA.
- T004 obtains a fresh independent read-only review of the recorded Base-to-candidate range.
- T900 repeats the full acceptance matrix and whole-change review on one final candidate SHA.

## Artifact Output Contract

| Output | Status | Trigger | Location | Evidence / N/A Reason |
|---|---|---|---|---|
| Process / State Diagram | N/A | `Status` is only a document field | design.md#process-state-diagrams | N/A because no workflow or runtime state machine changes. |
| Sequence / Integration Diagram | N/A | No service integration | design.md#sequence-integration-diagrams | N/A because the test is local and makes no external call. |
| API / Contract Specification | Required | Versioned Markdown contract | design.md#gate-evidence-contract | Defines precise field, pairing, and compatibility boundaries. |
| Data Model / Migration Contract | N/A | No persistent schema or migration | design.md#data-model-migration-contract | N/A because the Markdown standard is not application data. |
| UX Flow / Interaction States | N/A | No UI surface | design.md#ux-flow-interaction-states | N/A because there is no user-facing interaction. |
| Test Matrix | Required | AC validation and fail-closed cases | design.md#test-matrix | Maps AC-GE-01 through AC-GE-03 to direct evidence. |
| Deploy / Release Checklist | N/A | No deploy/config/release change | design.md#deploy-release-checklist | N/A because deployment and release actions are outside scope. |
| AI Involvement Note | Required | AI-assisted delivery | design.md#ai-involvement-note | Requires human Apply confirmation and independent review. |

## Risks And Boundaries

- The UUID textual shape is exactly the confirmed scope; a stricter version/variant rule is not part of this change.
- A source string proves only local record structure; it never elevates an external system to authoritative status.
- If implementation requires a path beyond the allowlist, it stops for a new confirmed plan before editing.

## Traceability Matrix / 追溯关系矩阵

| SCN | REQ | AC | Tasks |
|---|---|---|---|
| SCN-GE-01 | REQ-GE-01 | AC-GE-01 | T002, T003, T004, T900 |
| SCN-GE-02 | REQ-GE-02 | AC-GE-02 | T001, T002, T003, T004, T900 |
| SCN-GE-03 | REQ-GE-03 | AC-GE-03 | T000, T003, T004, T900 |

## Next SDC Step

The plan is executable only after explicit human Apply authorization names the attached plan review bundle, its exact revision, and authorized PR controller.  That authorization is not supplied by this planning run.
