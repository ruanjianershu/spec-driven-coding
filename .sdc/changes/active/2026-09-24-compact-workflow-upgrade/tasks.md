# Tasks

Current repair/verification plan, not a reconstruction of initial implementation progress. Every checkbox, Review and Evidence field remains pending until main-owned evidence and independent verdicts exist. Existing candidate fixes are reconciled and verified, not assumed complete.

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

## Execution Contract

Run from the repository root. Verify fields are exact executable argv after shell-style tokenization; retain their spelling for matching runtime receipts. The final task intentionally invokes sh -c for the grouped full regression. All subprocess probes use disposable projects/fake homes. PYTHONDONTWRITEBYTECODE is inherited by child Python processes.

Work serially. T001-T003 have no semantic dependency on one another. T004 consumes T003's shared snapshot compatibility contract; T005 consumes all repairs. For each behavior slice, establish a discriminating regression, repair or reconcile the existing implementation, run the exact Verify group, and obtain separate Spec Compliance and Code Quality verdicts before completion. If an original failure cannot be reproduced because the source is already repaired, report that limitation and inspect a known-unfixed isolated snapshot when available; do not fabricate red evidence or revert shared work.

Required review is independent and read-only. No instruction may suppress findings. A passing command is not a code-review verdict, and schema validation is not delivery evidence. Initial handoff boundaries are in notes.md and do not prohibit main's runtime, evidence or delivery work.

## 实现任务 / Implementation Tasks

- [x] T001 [REQ-01] [AC-01] [Phase Repair] [Size: S] Reconcile frozen evaluator helper completeness
  - Depends on: none
  - Files: evals/sdc-agent/run_agent_evals.py; evals/test_agent_evals.py; evals/test_client_adapters.py (regression consumer)
  - Consumes: Current sdc-cli.py and scripts/sdc-runtime-context.py imports; explicit SOURCE_FILES staging allowlist; existing install_source return manifest and bounds.
  - Produces: Runnable current source -> frozen source -> disposable project helper chain including compact/findings and doctor; older-source compatibility and bounded staging retained.
  - Verify: env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest evals.test_agent_evals evals.test_client_adapters -v
  - Expected: Both real test modules pass; double-snapshot helpers execute without host PYTHONPATH, expected doctor structured failure is not an import failure, and link/byte-limit/older-source cases pass. Report skipped prerequisites explicitly.
  - Review: Approved
  - Evidence: notes.md#task-review-evidence
  - Source: spec.md#scenarios-and-requirements REQ-01; spec.md#ac-01; design.md DD-01; discovery.md F-001.
  - Work: Exercise the two-stage copy in isolated subprocesses, verify the independently expected file set/outcomes, include only explicitly selected helpers, and retain old sources that do not import new modules. Do not add blanket script copying.

- [x] T002 [REQ-02] [AC-02] [Phase Repair] [Size: M] Diagnose missing effective Claude skill registrations
  - Depends on: none
  - Files: scripts/sdc-doctor.mjs; evals/test_install_diagnostics.py; sdc-references/installation-diagnostics.md; evals/test_client_adapters.py (regression consumer)
  - Consumes: diagnose options and sdc.install-diagnostics/v1 report; canonical source profile; registered marketplace-root provenance; supported additive/replacement skill discovery.
  - Produces: Actionable CONFIGURATION_DRIFT for omitted effective source entrypoints despite equal payload hashes; required public commands, unsupported hook forms and quoted registration keys are checked; equivalent/default/additive selections and true duplicates remain correctly handled.
  - Verify: env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest evals.test_install_diagnostics evals.test_client_adapters -v
  - Expected: Both modules pass; subset-selection and source-added-skill cases fail diagnosis for the intended reason, equivalent-path/default/additive cases avoid false drift, genuine duplicates still block, and fake source/home bytes and modification times do not change.
  - Review: Approved
  - Evidence: notes.md#task-review-evidence
  - Source: spec.md#scenarios-and-requirements REQ-02; spec.md#ac-02; design.md DD-02; discovery.md F-002.
  - Work: Separate effective capability coverage from payload hashing, retain the existing provenance exception and defensive bounds, and update only the directly affected diagnosis contract documentation. Do not expand to unverified client configuration formats.

- [x] T003 [REQ-03, REQ-05, REQ-06] [AC-03, AC-06, AC-07] [Phase Repair] [Size: M] Preserve installed findings and review evidence compatibility
  - Depends on: none
  - Files: sdc-references/review-findings.md; scripts/sdc_evidence.py; scripts/sdc-runtime-context.py; evals/test_guidance_contracts.py; evals/test_review_findings.py; evals/test_evidence_workflow.py; evals/test_evidence_parsing.py (regression consumer)
  - Consumes: Installed plugin/runtime root resolution, product-project cwd, stable finding ledger semantics, old STANDARD review_artifacts snapshots without findings.json, and existing sensitive-value screening.
  - Produces: Usable installed findings examples; unchanged absent-ledger STANDARD approvals; real ledger changes invalidate review; non-sensitive reviewer labels pass without weakening screening; the bundled conditional company-index reference stays optional unless also explicitly required, with absence bound for freshness.
  - Verify: env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest evals.test_review_findings evals.test_guidance_contracts evals.test_evidence_workflow evals.test_evidence_parsing -v
  - Expected: All four modules pass; documented command forms work from a project without SDC source; unchanged old-shaped STANDARD state/receipt verifies and archives; real ledger transitions and blocking findings reject delivery; harmless label passes and credential fixtures fail.
  - Review: Approved
  - Evidence: notes.md#task-review-evidence
  - Source: spec.md#scenarios-and-requirements REQ-03, REQ-05, REQ-06; spec.md#ac-03; spec.md#ac-06; spec.md#ac-07; design.md DD-03; discovery.md F-003, F-005, F-006.
  - Work: Run documented command examples at the product cwd as well as helper round trips. Restore omission of an absent ledger without erasing present-ledger hashes, retain and verify existing ledger-content rewrite coverage, and narrowly classify descriptive dated labels without relaxing general secret redaction. This is one review-evidence compatibility boundary.

- [x] T004 [REQ-04] [AC-04, AC-05] [Phase Repair] [Size: M] Close compact source coverage and freshness escapes
  - Depends on: T003
  - Files: scripts/sdc_evidence.py; evals/test_compact_workflow.py; evals/test_evidence_workflow.py; evals/test_evidence_parsing.py
  - Consumes: T003's compatible STANDARD review snapshot contract in the shared evidence helper; source_snapshot, change_source_snapshot and compact captured baseline; existing symlink/gitlink/explicit-target guards.
  - Produces: Tracked product files remain covered despite filtered directory names; non-Git directory links and linked ancestors of indexed files bind their destinations without traversal; compact validation/evidence/archive and shared STANDARD freshness agree.
  - Verify: env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest evals.test_compact_workflow evals.test_evidence_workflow evals.test_evidence_parsing -v
  - Expected: All three modules pass; modifying tracked docs/venv/runner.py or adding/retargeting an undeclared directory link blocks compact validate, evidence verify and archive; external contents remain untouched and STANDARD legacy/source-safety tests remain green.
  - Review: Approved
  - Evidence: notes.md#task-review-evidence
  - Source: spec.md#scenarios-and-requirements REQ-04; spec.md#ac-04; spec.md#ac-05; design.md DD-04; discovery.md F-004.
  - Work: Distinguish indexed product files from disposable untracked caches, record directory-link identity during non-Git enumeration, retain independent SDC bookkeeping snapshots, and retain and verify the existing directory-link retarget regression. Do not traverse external targets or widen compact eligibility.

## 验证任务 / Verification Tasks

- [x] T005 [REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07] [AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07, AC-08, AC-09] [Phase Verify] [Size: M] Run full regression and establish reviewed GitHub delivery readiness
  - Depends on: T001, T002, T003, T004
  - Files: This change's tasks.md and notes.md (durable results after main verification); package.json, evals/, tests/, scripts/audit-release.mjs, bin/install.js, bin/sdc.js, scripts/sdc-doctor.mjs, sdc-cli.py (verification inputs)
  - Consumes: T001-T004 repaired final sources, exact-command execution evidence and independent task verdicts; complete spec/design/impact/output contract.
  - Produces: Actual final regression results and limits, AC coverage reconciliation, independent whole-change verdict and inputs for current runtime delivery gates. GitHub push and its revision/result record follow those gates as whole-change delivery actions, not prerequisites for completing T005.
  - Verify: sh -c 'export PYTHONDONTWRITEBYTECODE=1; npm test && npm run eval:sdc && python3 -B -m unittest discover -s tests -v && npm run audit && node --check bin/install.js && node --check bin/sdc.js && node --check scripts/sdc-doctor.mjs'
  - Expected: The shell exits 0 only when every full suite, deterministic flow, installed-command test, audit and syntax check succeeds. Direct STANDARD validation is run separately from this Verify argv. Review and receipt obligations remain separate; failures/skips or missing AC evidence block the corresponding completion claim.
  - Review: Approved
  - Evidence: notes.md#task-review-evidence
  - Source: spec.md#traceability--追溯关系矩阵 REQ-01 through REQ-07; spec.md#ac-01 through spec.md#ac-09; design.md DD-05; discovery.md U-01.
  - Work: Main reviews artifacts, captures actual counts, failures/skips and snapshot-bound exact-command receipts, reconciles output-contract/impact coverage and obtains independent task/whole-change verdicts before completing T005. Main then performs authorized lifecycle/evidence gates, pushes to GitHub and records the revision/result. T005 covers AC-09's pre-push evidence and chronology; the final delivery record closes its post-push obligation without a task/gate dependency cycle.
