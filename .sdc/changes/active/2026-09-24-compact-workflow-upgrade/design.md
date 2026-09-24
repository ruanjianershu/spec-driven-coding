# Design

## Independent Review Boundary Addendum

The final repair verification includes F-007 through F-010 under existing REQ-02
and REQ-04, without new public behavior or broader supported client formats.
The doctor requires all public command entrypoints in both source and installed
Claude profiles, rejects unsupported hook values except the existing portable
Codex empty list, and classifies quoted TOML namespace keys before failing closed.
Source snapshots bind the first symlink ancestor's path and destination before
probing an indexed child; they never traverse that link to inspect its target.
The regressions are part of the existing T002 and T004 Verify groups, respectively.

The first real planning attempt also reproduced F-011: the bundled AI standard's
conditional company-index reference was misclassified as mandatory in a public
workspace without imported company standards. Recognize only that exact bundled
conditional as optional, bind absence, and let any explicit required citation
win. Existing missing-required-source and symlink gates remain unchanged. Cover
both STANDARD and compact traversal in the T003/T004 groups. No root governance
file or synthetic company standard is changed to make the gate pass.

Design date: 2026-09-24. This is a present repair/verification design for an already-coded upgrade. It is not evidence that a formal design or preflight preceded that code.

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| spec.md; discovery.md U-01 and A-02 | Confirmed scope / engineering derivation | Repair direction, defects and derived ACs | Defines the repair boundary |
| .sdc/constitution.md; .sdc/project.md; .sdc/standards/coding.md; .sdc/standards/testing.md; .sdc/standards/security.md; .sdc/standards/architecture.md; .sdc/standards/ai.md | Inspected | Existing project rules | Local-first compatibility and reviews |
| .sdc/knowledge/index.md; .sdc/project-cognition.md; .sdc/common-ground.md; .sdc/expert-routing.md | Inspected | Mostly empty templates | No unsupported project fact is promoted |
| impact.md#evidence-index | Inspected | Named functions and existing test modules | Bounded Brownfield implementation surface |
| sdc-references/workflow-standards.md; sdc-references/execution-orchestration.md; sdc-references/artifact-output-contracts.md; sdc-references/test-quality.md | Inspected | Current risk, task and evidence contracts | Coherent slices and honest preflight |

## Knowledge Gaps

No blocking planning gap remains after the focused source inspection. Missing measured execution/review evidence remains a delivery obligation. Reinspect affected sources before main's gates because source and tests changed during preparation.

## Common Ground Used

No populated root ESTABLISHED rows apply. Use the current user confirmation and directly inspected technical contracts, not empty knowledge templates or historical test claims. Relevant internal expert lenses and their checks are listed in context-pack.md.

## Global Constraints

| ID | Constraint | Source | Applies To |
|---|---|---|---|
| GC-01 | Use STANDARD artifacts. Preserve public lifecycle init/change/plan/apply/check/archive, existing sdc routing and optional harness; never downgrade existing STANDARD changes to compact. | sdc-references/artifact-schemas.md; spec.md INV-02, INV-06 | T001-T005 |
| GC-02 | Preserve confirmation, scope/freshness, exact Verify argv receipts, stable blocking findings, separate Spec Compliance and Code Quality verdicts, and final whole-change review. | .sdc/constitution.md; spec.md INV-01, INV-04 | T001-T005 |
| GC-03 | Preserve Node.js >=14.0.0, Python standard-library helpers and local-first operation; no new dependencies, telemetry, background service or MCP server. | package.json; .sdc/project.md | T001-T005 |
| GC-04 | Repair actual code, tests and directly affected guidance within the approved issues and impact scope; preserve unrelated work and do not rewrite governance or history to bypass a gate. | discovery.md U-01, A-02; .sdc/constitution.md; impact.md | T001-T005 |
| GC-05 | Complete repairs, current evidence and independent review before the authorized GitHub push. No internal GitLab push, npm publication or user-home installation is included. | discovery.md U-01, A-01; spec.md AC-09 | T001-T005 and delivery |
| GC-06 | Behavioral and installation probes use disposable projects/fake homes; keep bounded scans and secret/path defenses; do not claim live-client behavior, agent quality or token savings from local tests. | spec.md AC-01 through AC-08; sdc-references/test-quality.md | T001-T005 |
| GC-07 | Record initial code as preceding formal change artifacts. Never fabricate historical preflight, approval, failures or passes; mark completion only from actual current evidence and independent review. | discovery.md A-01; .sdc/constitution.md; spec.md INV-05 | T001-T005 |
| GC-08 | Normative content is English; no personal paths, private names or closed-source attribution. Retain only schema-required legacy heading labels. | discovery.md A-01; sdc-cli.py validation contracts | T001-T005 and artifacts |

## Plan Preflight

- Status: Passed
- Reviewed Against: spec.md, impact.md, design.md, tasks.md, context-pack.md, .sdc/standards/, Artifact Output Contract, current affected source and test entrypoints.
- Findings: No blocking findings; current plan self-inspection reconciled provenance, whole-change scope, AC/task coverage, real test entrypoints and shared constraints. This is not historical preflight or independent code review; main reviews artifacts before runtime gates.

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

## Solution Summary

Preserve the existing implementation architecture and reconcile each repair against current code before editing. Do not rewrite an already-correct candidate repair merely to make a new diff. Each task includes the missing or existing discriminating regression, focused verification and independent review. Original red evidence must be attributed to actual runs; where a fix already exists, use an isolated known-unfixed snapshot or disclose the baseline gap.

- DD-01 / T001: Keep the frozen evaluator's explicit source allowlist complete for current imports: sdc_compact.py, sdc_findings.py and the doctor sidecar as well as existing helpers. Copy the explicitly named .mjs helper without opening the general payload filter. Check source -> frozen -> project, not only one copy or string presence. Do not require newly introduced helpers from older sources that never imported them.
- DD-02 / T002: Compare intended source SDC skill entrypoints with the effective supported Claude selection separately from byte fingerprints. Respect the marketplace-root replacement exception and nonroot additive discovery. Emit CONFIGURATION_DRIFT with bounded missing paths/counts when present bytes are not selected. Preserve PAYLOAD_DRIFT, malformed-config, duplicate, missing-source and read-only behavior.
- DD-03 / T003: Findings examples use the installed SDC_PLUGIN_ROOT/scripts/sdc_findings.py, with the resolved sdc-runtime child for direct layouts, while keeping the product project as cwd. Preserve the append-only ledger and exact command/review gates. Omit a nonexistent findings ledger from STANDARD review snapshots rather than manufacturing a null key; bind real ledger bytes when present. Narrowly distinguish bounded descriptive dated reviewer prose from credential-like strings without changing general secret redaction.
- DD-04 / T004: Separate tracked product files from disposable-directory filtering in source_snapshot. Track non-Git directory symlink identity without following targets so added/retargeted links affect the baseline. Preserve separate SDC bookkeeping snapshots, explicit target coverage, file modes, missing-file handling, gitlink rejection and source-safety checks.
- DD-05 / T005: Verify the whole final upgrade, guidance links, generated adapter/payload contracts and artifact schema; obtain independent final review and runtime evidence under main control. No historical result in the older plan is reused as a current receipt.

## Impact Scope

Brownfield impact is detailed in impact.md. Direct repair surfaces are evals/sdc-agent/run_agent_evals.py, scripts/sdc-doctor.mjs, scripts/sdc_evidence.py, scripts/sdc-runtime-context.py, sdc-references/review-findings.md, sdc-references/installation-diagnostics.md and their existing test modules. scripts/sdc_compact.py, scripts/sdc_findings.py, sdc-cli.py, bin/install.js and generated adapters are affected consumers or contract references, not invitations to refactor them.

## Non-Scope

No unrelated refactors, new public stages, changed compact eligibility, generic client configuration parser, universal secret-classifier replacement or receipt migration by assertion. Disposable installation fixtures must not replace a user's plugin. Production repairs and GitHub delivery are in scope.

## Key Tradeoffs

Explicit frozen helper selection is bounded and auditable; copying all scripts or broadening every extension would add unnecessary payload. Effective loading checks supplement hashes because identical files do not prove registration. Restoring the absent-ledger shape preserves old STANDARD approval without ignoring real ledger transitions. Source coverage changes stay in the shared helper to keep compact and STANDARD consumers consistent, so shared compatibility tests are mandatory.

## Process / State Diagrams

```text
Historical: user upgrade direction -> initial code outside formal change -> assistant F-001-F-006 report
Current:    U-01 fix-and-push direction -> A-01 reconciliation -> spec/impact/design/tasks
Handoff:    plan self-inspection -> schema validation -> main artifact review
Main later: authorized lifecycle reconciliation -> repair + exact-command evidence
            -> independent task reviews -> final review -> runtime delivery gates
            -> GitHub-only push
```

Existing lifecycle states remain intake -> discovery -> confirmed -> planned -> applying -> checking -> archivable. This is the whole-change delivery sequence; runtime state has not been advanced by artifact preparation. Reopen/revision rules still apply whenever governing inputs change; no backdated execution state is invented.

## Sequence / Integration Diagrams

```text
Evaluator source -> install_source -> frozen allowlist -> install_source -> isolated helper process
Source profile + registered marketplace + plugin manifest -> doctor selection + hashes -> report
Product cwd + resolved plugin/runtime root -> findings CLI -> project ledger -> review freshness
Git index or non-Git walk + explicit compact paths -> source_snapshot -> compact baseline / receipts
Current inputs + exact Verify argv + approved independent verdicts -> main-owned evidence gate
```

## API / Contract Specification

| Boundary | Preserved Contract | Repair / Failure Behavior |
|---|---|---|
| install_source(source, project) | Bounded selected files and deterministic manifest; no host import fallback | Copy required named runtime helpers twice; reject unsafe source links and bounds violations |
| diagnose(options) and existing init/check installation routing | sdc.install-diagnostics/v1; ok, issues, installations; 0 without blockers and nonzero for blockers | CONFIGURATION_DRIFT reports missing effective Claude entrypoints independently of equal fingerprints; no settings values or writes |
| Findings internal CLI | Explicit --change; product cwd or --root; JSON success/error; stable IDs and bounded adjudication | Installed helper path is independent of product checkout layout; evidence remains data |
| source_snapshot / compact validate / evidence verify / archive | Fresh source and in-scope baseline required at all delivery gates | Track filtered indexed code and directory-link identity; do not follow external targets |
| review_snapshot for STANDARD | Existing inputs/sources/support and tasks/notes remain bound | Missing ledger creates no extra key; existing ledger bytes are included and transitions invalidate approval |
| evidence review --reviewer | Non-sensitive caller attribution after actual review prerequisites | Accept named harmless prose fixture, reject credential-like labels; no identity authentication |

## Data Model / Migration Contract

No new database, schema version, lifecycle state, public command, or mandatory migration is introduced. Existing findings.json remains schema 1 with stable IDs and append-only history. Ledger updates must record actual observations, not synthesized historical attempts.

Preserve the older STANDARD review_artifacts shape when findings.json does not exist. When it exists, hash its bytes; creation, modification and removal change review freshness. Do not drop ledger information from an existing receipt to force a match or regenerate receipts merely to claim old compatibility. Tests construct old-shaped states/receipts only inside disposable fixtures.

Broader source coverage can correctly invalidate receipts that omitted real source changes. That is required freshness enforcement, not a reason to discard new coverage. Main must rerun affected verification/review on the final sources, not relabel an old result.

## UX Flow / Interaction States

CLI-only behavior: valid helper invocation returns help or defined JSON; missing/unsafe inputs return actionable nonzero failure. Doctor distinguishes payload drift, effective registration drift and unsupported/missing input. Findings distinguish open, adjudication-required, accepted-risk and resolved; only resolved clears that finding. Harmless attribution passes screening only after other review prerequisites pass. No graphical interface is added.

## Test Matrix

All execution results below are Pending. Task commands are defined verbatim in tasks.md.

| AC | Scenario | Level | Verification | Expected Result | Status |
|---|---|---|---|---|---|
| AC-01 | Double freeze current source; older source; unsafe links/limits; real helper processes | Subprocess and staging | T001; evals.test_agent_evals; evals.test_client_adapters | No import leakage; expected CLI/doctor outcome; bounded staging preserved | Pending |
| AC-02 | Same bytes but subset Claude selection; equivalent paths; source-added skill; additive discovery | Real doctor with fake homes | T002; evals.test_install_diagnostics | Actionable configuration blocker only when effective entrypoints are missing; no writes | Pending |
| AC-03 | Installed findings examples executed from product cwd, plus helper round trips | Subprocess and guidance contracts | T003; evals.test_guidance_contracts; evals.test_review_findings | Correct project ledger and JSON; no product-relative helper lookup | Pending |
| AC-04 | Tracked docs/venv/runner.py changed outside declared prose paths | Compact lifecycle and shared snapshots | T004; evals.test_compact_workflow; evals.test_evidence_workflow | validate/evidence/archive all reject; STANDARD freshness preserved | Pending |
| AC-05 | Non-Git directory link addition/retargeting and external target protection | Compact lifecycle and path boundary | T004; evals.test_compact_workflow; evals.test_evidence_parsing | Detect scope/freshness change without external traversal/write | Pending |
| AC-06 | Old absent-ledger receipt, ledger appearance/change/removal, unresolved findings | STANDARD delivery and finding state | T003; evals.test_evidence_workflow; evals.test_review_findings | Old unchanged approval remains usable; real transitions block | Pending |
| AC-07 | Long dated descriptive attribution and explicit/opaque secrets | Real evidence review boundary | T003; evals.test_evidence_workflow | Harmless fixture accepted; sensitive labels rejected | Pending |
| AC-08 | Compact, STANDARD, adapters, guidance and full upgrade | Full regression, deterministic flow, installed command, audit/syntax | T005 exact Verify argv | All required suites pass; skips/limits disclosed | Pending |
| AC-09 | Honest chronology, exact task mapping, current evidence/review and GitHub delivery | Artifact validation plus independent review | Artifact validation; T005; main's review/gates and pushed-revision evidence | Honest chronology and actual current evidence/review before recorded GitHub delivery | Pending |

Exercise the documented command boundary as well as the helper API. Existing directory-link retarget and ledger-content rewrite regressions are included in the task groups. Main reports those cases freshly passing; final source-bound results and independent review remain main-owned.

## Deploy / Release Checklist

- Main establishes the final repair source and reviews the actual diff against impact.md; shared-checkout edits are preserved.
- Main records each exact Verify command's actual result, skipped cases, source and evidence; baseline limitations are explicit.
- Main completes independent task verdicts and final whole-change review without suppressing findings.
- Main reviews artifacts and performs authorized runtime state/manifest/evidence gates against current inputs.
- Main verifies public docs/payload consistency and absence of private attribution or personal paths before GitHub delivery.
- Perform the authorized GitHub push after successful gates and record its revision/result. No internal GitLab push, npm publication, user installation, or release/version expansion is part of this scope.

This checklist defines required delivery work, not proof that delivery has occurred.

## AI Involvement Note

AI inspected current governance, source and test entrypoints, reconciled the reported history and authored this package. The prior plan's checked tasks, counts and review claims are attributed historical statements, not independently verified here. Source changed during reading, so no immutable implementation snapshot is certified. Artifact self-inspection is not independent code review; initial pending handoff statuses are recorded in notes.md and may advance with actual evidence.

## Brownfield Impact Summary

Existing CLI imports feed frozen evaluation and installed runtimes. The shared evidence helper feeds both STANDARD and compact lifecycle receipts. Doctor selection is separate from payload fingerprints. Impact and rollback are bounded in impact.md; no project-wide cognition or knowledge rewrite is necessary for this local plan.

## REQ/AC to Design Decision Mapping

| Design | Requirement | Acceptance | Task |
|---|---|---|---|
| DD-01 | REQ-01 | AC-01 | T001 |
| DD-02 | REQ-02 | AC-02 | T002 |
| DD-03 | REQ-03, REQ-05, REQ-06 | AC-03, AC-06, AC-07 | T003 |
| DD-04 | REQ-04 | AC-04, AC-05 | T004 |
| DD-05 | REQ-07 and all preserved requirements | AC-08, AC-09 | T005 |

## Risks, Rollback, and Migration

Changes to shared snapshot coverage may expose previously undetected stale evidence. Do not weaken checks to preserve an invalid pass. Narrow reviewer heuristics need adversarial secret fixtures. Doctor must retain true duplicate detection while avoiding false positives from equivalent path syntax.

No data/config migration or user installation is required; GitHub delivery remains in scope. Main can reverse only its reviewed code changes if needed, preserving user work and all finding/revision history; it must then rerun affected checks and review. No receipt or state-file editing is a rollback mechanism.

## Alternatives

Do not copy the entire source tree into evaluator trials, compare only versions/hashes for registration, accept all reviewer strings, ignore tracked cache-like paths, or delete old receipts/ledgers. Each alternative would undermine a confirmed safety or compatibility requirement.
