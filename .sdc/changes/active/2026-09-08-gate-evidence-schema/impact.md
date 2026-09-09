# Change Impact

## Analysis Snapshot

- Repository: `spec-driven-coding`
- Change: `2026-09-08-gate-evidence-schema`
- Exact implementation baseline: `origin/main@e10a5d221f081fb6d099d342597a707b0dad91c9`
- Evidence limits: direct Git-object and confirmed issue inspection; no external-control-plane inspection is relevant or authorized.
- Baseline/runtime conclusion: the Base has no `scripts/sdc-runtime-context.py`, JSONL context-manifest contract, or lifecycle-state contract.  The Base supports Markdown change validation and ignored task/review handoffs only.

## Entry Points And Call Chain

1. `sdc-references/workflow-standards.md` is the authoritative versioned standard named by ANDY-143.
2. `scripts/audit-release.mjs` statically reads the bounded `## Task Format ... ## Evidence Discipline` range; the new section is placed after that boundary.
3. `tests/test_gate_evidence_schema.py` is a new direct local test entrypoint; it reads the standard and uses test-local fixtures only.
4. `sdc-cli.py validate <change>` is the supported Base plan validator for the active change package.
5. `scripts/sdc-task-brief.py` and `scripts/sdc-review-package.py` create ignored Markdown handoffs from tracked task/context inputs; they are not a manifest/state API.
6. The portable Git bundle attached for plan review is a transport-only input: T000 verifies its digest, exact revision, Base ancestry, and complete sorted fixed nine-path equality locally before it archives the nine artifacts into the clean Base checkout.

## Direct Changes Required

| File / Contract | Reason | Evidence | Related REQ/AC |
|---|---|---|---|
| `sdc-references/workflow-standards.md` | Publish the sole authoritative Layout A contract after `## Evidence Discipline`. | ANDY-143 file boundary; Base lacks all five field rules; audit boundary inspection. | REQ-GE-01 / AC-GE-01 |
| `tests/test_gate_evidence_schema.py` | Prove the standard and fail-closed local record cases with no runtime coupling. | Base Python `unittest` convention and ANDY-151 verification scope. | REQ-GE-02 / AC-GE-02 |
| `.sdc/changes/active/2026-09-08-gate-evidence-schema/{discovery.md,proposal.md,spec.md,impact.md,design.md,tasks.md,context-pack.md,notes.md,knowledge-candidates.md}` | Preserve traceability, T000 package input, task interfaces, and durable review evidence. | Constitution, Base `sdc-cli.py`, and execution-orchestration contracts. | REQ-GE-01 through REQ-GE-03 |
| Issue-attached portable plan review bundle and digest manifest | Supply a persistent, independently readable revision source for T000 and review. | ANDY-157 independent revalidation requirement; Git bundle verification. | REQ-GE-03 / AC-GE-03 |

## Cascading Impact

- The standard becomes a durable input for the serial Gate-Closed planning chain only after independent review of its exact candidate head.
- Existing runtime evidence, profile behavior, default artifact validation, package behavior, and public commands remain unchanged.
- The audit remains compatible because its Task Format bounded scan ends at `## Evidence Discipline` before the new section.
- Ignored task/review files are recoverable local context only; durable evidence remains in the change package.
- The review bundle is not a repository runtime file and does not expand the candidate changed-path allowlist.

## Contracts / Data / Config / Permissions / Security / Observability

| Area | Impact | Evidence |
|---|---|---|
| Versioned Markdown contract | Direct | `workflow-standards.md` gains the Layout A local contract. |
| Plan/runtime handoff | Direct, Base-supported | `sdc-cli.py`, task-brief, review-package, and Markdown progress-ledger sources. |
| JSON manifest or lifecycle-state contract | None | Base schema and validator do not define or consume one. |
| Public/runtime contract | None | ANDY-143 excludes profile, runtime, and default `validate` behavior. |
| Data/migration | None | No persistent data model or stored-data migration exists in scope. |
| Config/deployment | None | No configuration, job, service, or deployment path changes. |
| Permissions/external authority | None | Sources remain opaque local text; no dereference or authentication occurs. |
| Observability | None | No runtime behavior changes. |
| Security | Direct test diagnostic boundary | The test reports field/rule class and does not echo opaque source values. |

## Tests And Regression Strategy

- Red first: run `python3 tests/test_gate_evidence_schema.py` against the Base-standard shape and observe the expected section-absence failure.
- Green: rerun the same command after T002; it must accept the compliant fixture and reject each named malformed category.
- T000: verify the attached bundle digest, bundle integrity, exact revision, Base ancestry, and equality of the complete sorted `Base..revision` changed-path list to the fixed nine paths; run `set -o pipefail; git show "${BASE}:sdc-cli.py" | python3 - validate 2026-09-08-gate-evidence-schema`; then emit `task-T000-brief.md`, `task-T000-report.md`, and `progress.md` using the existing task-brief helper.
- Scope: review a clean content candidate, compare exact `Base..candidate`, require Base ancestry, empty porcelain status, `git diff --check`, and an explicit changed-path allowlist.
- Review: use the existing review-package helper and a separate read-only reviewer for each candidate; write durable conclusion in `tasks.md` and `notes.md` after approval.

## Implementation Order And Rollback Boundary

1. Start from the exact Base, verify the recorded-digest portable plan review bundle, prove exact equality to the nine fixed package paths from the exact plan-revision commit, import and stage only those artifacts, commit `H0`, validate it, and generate only the Base-supported ignored T000 handoff.
2. Create the direct red test and fixtures, then add the standard section in the designated location.
3. Capture and review each clean content candidate before continuing.
4. Capture one final candidate for the whole-change review and PR snapshot.

Rollback is a version-control revert of the standard section and direct test.  It has no data, runtime, configuration, or deployment rollback path.

## Open Questions

| Question | Why It Matters | Blocking? |
|---|---|---|

No open question affects the planned implementation.  Human Apply authorization remains the execution gate.

## Evidence Index

| Claim | Source |
|---|---|
| The exact Base lacks the governed section and fields. | `git show origin/main:sdc-references/workflow-standards.md` |
| The exact Base lacks the former runtime-context script. | `git cat-file -e origin/main:scripts/sdc-runtime-context.py` exits 128. |
| The Base validator supports active Markdown change packages. | `git show origin/main:sdc-cli.py` (`cmd_validate`). |
| The Base task/review helpers create ignored Markdown handoffs. | `git show origin/main:scripts/sdc-task-brief.py`; `scripts/sdc-review-package.py`. |
| The CLI has no Gate Evidence consumer and default behavior must stay unchanged. | `git show origin/main:sdc-cli.py`; ANDY-143 scope. |
| The direct-test convention exists. | `git show origin/main:tests/test_installed_sdc_validate.py`. |
| The Task Format placement boundary is audit-sensitive. | `git show origin/main:scripts/audit-release.mjs`. |
| The local-only Layout A semantics are confirmed. | ANDY-151 decision inputs. |
