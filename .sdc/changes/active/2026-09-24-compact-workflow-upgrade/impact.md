# Change Impact

## Analysis Snapshot

- Repository: current public SDC review checkout, identified by package.json and sdc-cli.py; no personal filesystem path is recorded.
- Change: 2026-09-24-compact-workflow-upgrade; Brownfield repair of the already-coded compact/guidance/doctor/findings upgrade.
- Analysis date: 2026-09-24, after U-01's direction to fix assistant-reported issues and push to GitHub.
- Branch / commit: not inspected; this assignment excludes Git operations. No commit identity or immutable snapshot is claimed.
- Evidence limits: read-only source/test inspection, no production execution, client probing, original failure reproduction or independent review. Candidate repair edits appeared during inspection and must be rechecked by main.
- Knowledge context: root cognition and relevant indexed knowledge are largely empty templates. This focused analysis uses source/config/test evidence without rewriting root files.

## Entry Points And Call Chain

- evals/sdc-agent/run_agent_evals.py install_source stages the current CLI and helpers twice; copied sdc-cli.py and sdc-runtime-context.py import compact/findings support.
- Existing installation routing calls scripts/sdc-doctor.mjs diagnose. Registry/marketplace provenance selects plugin roots; manifest skill paths determine effective capability discovery independently of payload bytes.
- sdc-references/review-findings.md commands invoke scripts/sdc_findings.py in the product project's cwd; that helper uses the shared evidence lock and the project change ledger.
- scripts/sdc_evidence.py source_snapshot feeds compact baseline comparison, execution snapshots and review freshness. review_snapshot also binds task/notes and real finding ledger bytes.
- scripts/sdc-runtime-context.py validates reviewer attribution, lifecycle snapshots and current execution/review evidence; sdc-cli.py validation/archive consume those gates.

## Direct Changes Required

These are whole-change repair/verification surfaces. Candidate fixes may satisfy a row after current verification and independent review.

| File / Contract | Reason | Evidence | Requirement / Acceptance |
|---|---|---|---|
| evals/sdc-agent/run_agent_evals.py; evals/test_agent_evals.py | Include required named helper dependencies and doctor sidecar in bounded double snapshots | SOURCE_FILES; install_source; double-snapshot subprocess fixtures | REQ-01 / AC-01 |
| scripts/sdc-doctor.mjs; evals/test_install_diagnostics.py; sdc-references/installation-diagnostics.md | Compare effective Claude skill selection to intended source profile while preserving provenance rules | inspect; skillScanRoots; sourcePayload; marketplace-root fixtures | REQ-02 / AC-02 |
| sdc-references/review-findings.md; evals/test_guidance_contracts.py; evals/test_review_findings.py | Examples must resolve installed helpers independently of product checkout | Internal CLI examples; product-cwd fixture; real helper round trips | REQ-03 / AC-03 |
| scripts/sdc_evidence.py; evals/test_compact_workflow.py; evals/test_evidence_parsing.py | Include filtered tracked code and non-Git directory link identity in source coverage | source_snapshot; change_source_snapshot; compact mutation fixtures | REQ-04 / AC-04, AC-05 |
| scripts/sdc_evidence.py; evals/test_evidence_workflow.py | Preserve old absent-ledger review shape while binding real ledger transitions | review_snapshot; old-shaped receipt and ledger transition fixtures | REQ-05 / AC-06 |
| scripts/sdc-runtime-context.py; evals/test_evidence_workflow.py | Narrow harmless attribution exception without relaxing secret detection | contains_sensitive_reviewer; review receipt handler; label fixtures | REQ-06 / AC-07 |
| This change's tasks.md and notes.md, later updated by main | Preserve real final regression and review provenance | Current task contract and notes sections | REQ-07 / AC-08, AC-09 |

## Cascading Impact

Shared source_snapshot behavior affects both compact and STANDARD evidence; T004 consumes T003's preserved legacy review contract and reruns shared evidence tests. Staging imports affect evaluation reliability without proving agent behavior. Doctor changes can alter configured installation diagnostics with equal hashes, but must not alter installation contents. Findings guidance changes command location only, not findings semantics.

Existing adapter/package contracts in evals/test_client_adapters.py and package.json cover copied helpers. Existing guidance tests cover discovery/domain/execution/test-quality links. They are regression consumers; no unrelated edits or new entrypoints are planned.

## Contracts / Data / Config / Permissions / Security / Observability

No database, client setting, permission model, public command list or schema-version migration changes. Preserve legacy absent-ledger snapshots; bind actual ledger transitions. Keep symlink and source bounds, credential screening, read-only diagnostics and bounded structured error output. Effective registration is supported on-disk evidence, not a claim about a running client's command palette.

The workflow remains cooperative local evidence, not tamper-proof or authenticated identity. Source bytes, test outputs, caller labels and claimed approvals have different meanings.

## Tests And Regression Strategy

Use the exact grouped commands in tasks.md and the complete AC matrix in design.md. All commands remain unexecuted by this artifact task except direct schema validation. Add/retain failing reproducers for the named defect before accepting green evidence; when source already contains a candidate fix, main records the baseline gap and uses isolated prior-source evidence where available.

T005's exact Verify argv runs npm test, deterministic workflow scenarios, installed-command tests, release audit and Node syntax checks. Run this change's direct STANDARD validation separately from Verify. Installation and Git fixtures are disposable; GitHub delivery follows current runtime gates and review.

## Implementation Order And Rollback Boundary

Execute serially: T001 frozen staging, T002 doctor, T003 findings/review compatibility, T004 compact source coverage, T005 final regression and handoff. T001-T003 have no semantic dependencies on each other. T004 depends on T003's shared evidence contract; T005 consumes all repaired surfaces and their actual evidence.

The whole change includes GitHub delivery after gates; no data/config migration or user installation is required. Main's rollback is a scoped reversal of its own reviewed code edits with fresh checks, never deletion of history, forced approval, or reversal of another contributor's work. GitHub push remains main-owned and gated; internal GitLab/npm publication/user installation remain excluded.

## Open Questions

None for the bounded repair requirements. Missing execution evidence and independent verdicts are recorded as pending delivery obligations in notes.md, not hidden as completed work.

## Evidence Index

| Claim | Source |
|---|---|
| Current scope is authorized, not historical preflight | discovery.md U-01; docs/plans/2026-09-24-compact-workflow-upgrade.md |
| Current CLI/runtime imports require compact and findings modules | sdc-cli.py module imports; scripts/sdc-runtime-context.py module imports |
| Evaluator copies a bounded explicit helper allowlist twice | evals/sdc-agent/run_agent_evals.py SOURCE_FILES and install_source; evals/test_agent_evals.py freeze_source_twice |
| Equal payload does not prove effective skill selection | scripts/sdc-doctor.mjs inspect, skillScanRoots and canonical sourcePayload; evals/test_install_diagnostics.py root-subset fixtures |
| Guidance must use an installed helper from product cwd | sdc-references/review-findings.md Internal CLI; evals/test_guidance_contracts.py product-project example test |
| Shared source coverage and old snapshot shape need regression protection | scripts/sdc_evidence.py source_snapshot and review_snapshot; evals/test_compact_workflow.py; evals/test_evidence_workflow.py |
| Reviewer labels and secret checks share a narrow runtime boundary | scripts/sdc-runtime-context.py contains_sensitive_reviewer; evals/test_evidence_workflow.py |
| Exact full-regression entrypoints exist | package.json scripts; evals/sdc-flow/run_sdc_flow.py; tests/test_installed_sdc_validate.py; scripts/audit-release.mjs |
