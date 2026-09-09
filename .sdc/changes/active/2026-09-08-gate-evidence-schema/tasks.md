# Tasks

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
- Reviewed Against: spec.md, impact.md, design.md, tasks.md, context-pack.md, Artifact Output Contract, Base `sdc-cli.py`, Base task/review helpers, and execution-orchestration.md
- Findings: Resolved: the former missing runtime-context dependency, undeclared JSON schemas, allowlist mismatch, executor-local-only plan revision, cross-task shell-environment dependency, zsh Git-object pipeline masking, cardinality-only package acceptance, implicit H0 materialization, inconsistent Apply gate, and task-trace mismatch are removed; each task now has a Base-existing interface and verification command.

## Apply Preconditions

- A human explicitly authorizes Apply before T000 and supplies full `SDC_PLAN_BUNDLE`, `SDC_PLAN_BUNDLE_SHA256`, `SDC_PLAN_REVISION`, plus the authorized PR controller.
- The executor creates an isolated branch directly from the Base in GC-GE-01 with empty porcelain status.
- The recorded-digest `SDC_PLAN_BUNDLE` must pass `git bundle verify`; its `SDC_PLAN_REVISION` must descend from Base and its complete sorted changed-path list must equal T000's fixed nine repository-relative package paths.
- Before T003 and T900, the authorized PR controller supplies an open PR URL whose observed head equals the recorded candidate SHA.

## 实现任务

- [x] T000 [REQ-GE-03] [AC-GE-03] [Phase 0] [Size: M] Verify, import, and validate the approved nine-file plan bundle from a clean Base, then create the Base-supported ignored T000 handoff.
  - Depends on: explicit human Apply confirmation with `SDC_PLAN_BUNDLE`, `SDC_PLAN_BUNDLE_SHA256`, `SDC_PLAN_REVISION`, and authorized PR controller
  - Files: `.sdc/changes/active/2026-09-08-gate-evidence-schema/discovery.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/proposal.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/spec.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/impact.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/design.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/tasks.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/context-pack.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/notes.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/knowledge-candidates.md`
  - Consumes: `BASE=e10a5d221f081fb6d099d342597a707b0dad91c9`; exact full `SDC_PLAN_BUNDLE`, `SDC_PLAN_BUNDLE_SHA256`, and `SDC_PLAN_REVISION`; Base `sdc-cli.py`; Base `scripts/sdc-task-brief.py`; Base `scripts/sdc-review-package.py`; GC-GE-01, GC-GE-02, GC-GE-07 through GC-GE-10
  - Produces: one clean committed plan-package candidate `H0`; recorded-digest bundle verification; successful Base validation; ignored `.sdc/runtime/2026-09-08-gate-evidence-schema/task-T000-brief.md`, `task-T000-report.md`, `progress.md`, and `task-T000-review-package.md`; a separate read-only review bound to `Base..H0`; durable T000 review evidence in tracked tasks/notes.
  - Verify: Set `BASE=e10a5d221f081fb6d099d342597a707b0dad91c9`, `CHANGE=2026-09-08-gate-evidence-schema`, and require `SDC_PLAN_BUNDLE`, `SDC_PLAN_BUNDLE_SHA256`, and `SDC_PLAN_REVISION`. Run `set -o pipefail`, then `test "$(git rev-parse HEAD)" = "$BASE" && test -z "$(git status --porcelain --untracked-files=all)" && test "$(shasum -a 256 "$SDC_PLAN_BUNDLE" | awk '{print $1}')" = "$SDC_PLAN_BUNDLE_SHA256" && git bundle verify "$SDC_PLAN_BUNDLE"`; set `PLAN_SOURCE="$(mktemp -d)"` and run `git clone --quiet --no-checkout "$SDC_PLAN_BUNDLE" "$PLAN_SOURCE"`, then run `git -C "$PLAN_SOURCE" cat-file -e "$SDC_PLAN_REVISION^{commit}" && git -C "$PLAN_SOURCE" merge-base --is-ancestor "$BASE" "$SDC_PLAN_REVISION"`. Set `EXPECTED_PLAN_PATHS="$(printf '%s\n' ".sdc/changes/active/$CHANGE/context-pack.md" ".sdc/changes/active/$CHANGE/design.md" ".sdc/changes/active/$CHANGE/discovery.md" ".sdc/changes/active/$CHANGE/impact.md" ".sdc/changes/active/$CHANGE/knowledge-candidates.md" ".sdc/changes/active/$CHANGE/notes.md" ".sdc/changes/active/$CHANGE/proposal.md" ".sdc/changes/active/$CHANGE/spec.md" ".sdc/changes/active/$CHANGE/tasks.md" | LC_ALL=C sort)"` and `ACTUAL_PLAN_PATHS="$(git -C "$PLAN_SOURCE" diff --name-only "$BASE..$SDC_PLAN_REVISION" | LC_ALL=C sort)"`, then run `test "$ACTUAL_PLAN_PATHS" = "$EXPECTED_PLAN_PATHS"`. Import that directory with `git -C "$PLAN_SOURCE" archive "$SDC_PLAN_REVISION" ".sdc/changes/active/$CHANGE" | tar -x`; stage only its path with `git add ".sdc/changes/active/$CHANGE" && git commit -m "docs(sdc): import approved gate-evidence plan package"` as `H0`, then run `git cat-file -e "${BASE}:sdc-cli.py" && git show "${BASE}:sdc-cli.py" | python3 - validate "$CHANGE" && python3 scripts/sdc-task-brief.py "$CHANGE" T000 && test -f ".sdc/runtime/$CHANGE/task-T000-brief.md" && test -f ".sdc/runtime/$CHANGE/task-T000-report.md" && test -f ".sdc/runtime/$CHANGE/progress.md" && python3 scripts/sdc-review-package.py "$BASE" "$(git rev-parse HEAD)" "$CHANGE" T000 && git diff --check "$BASE..HEAD" && ! git diff --name-only "$BASE..HEAD" | rg -n -v "^\.sdc/changes/active/$CHANGE/"`.
  - Expected: every check succeeds using only Base-existing tools plus locally verified Git-bundle transport; no runtime-context script, JSONL manifest, or lifecycle-state file is read, written, or listed in the candidate diff; an absent/altered bundle, incorrect base, non-descendant revision, any missing/extra/renamed/non-Markdown path in the fixed nine-path set, validation failure, missing helper output, or out-of-allowlist path stops the task before T001.
  - Review: Approved
  - Evidence: `git:ceaacfa421cbc8359e41b5deaff2f2a9697d1ba1`
  - Source: `spec.md#REQ-GE-03`, `spec.md#AC-GE-03`

- [x] T001 [REQ-GE-02] [AC-GE-02] [Phase 1] [Size: M] Write the direct red local Gate Evidence contract test and obtain its exact-candidate review.
  - Depends on: T000 approved review and durable evidence
  - Files: `tests/test_gate_evidence_schema.py`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/tasks.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/notes.md`
  - Consumes: T000 `H0`; `design.md#gate-evidence-contract`; GC-GE-03 through GC-GE-05 and GC-GE-08
  - Produces: clean candidate `H1` containing a standard-library `unittest` entrypoint and test-local fixtures; a nonzero red result because the Base-standard shape lacks the section; an ignored T001 review package; separate read-only review; durable T001 evidence.
  - Verify: From clean reviewed T000 head, write and commit `H1`; in that task's fresh shell run `set -o pipefail && BASE=e10a5d221f081fb6d099d342597a707b0dad91c9 && CHANGE=2026-09-08-gate-evidence-schema && H1="$(git rev-parse HEAD)" && ! python3 tests/test_gate_evidence_schema.py && python3 scripts/sdc-review-package.py "$BASE" "$H1" "$CHANGE" T001 && git diff --check "$BASE..$H1" && CHANGED_PATHS="$(git diff --name-only "$BASE..$H1")" && ! printf '%s\n' "$CHANGED_PATHS" | rg -n -v "^(tests/test_gate_evidence_schema\.py|\.sdc/changes/active/$CHANGE/)"`.
  - Expected: the test fails only for the missing governed section; diagnostics identify a rule/field class without printing a source value; the review package binds the full candidate SHA.
  - Review: Approved
  - Evidence: `git:d70439ece43a52c65c4edc90923f8abaca6eb7fa`
  - Source: `spec.md#REQ-GE-02`, `spec.md#AC-GE-02`

- [ ] T002 [REQ-GE-01,REQ-GE-02] [AC-GE-01,AC-GE-02] [Phase 2] [Size: M] Add the audit-safe Layout A section, turn the direct test green, and obtain its exact-candidate review.
  - Depends on: T001 approved review and durable evidence
  - Files: `sdc-references/workflow-standards.md`, `tests/test_gate_evidence_schema.py`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/tasks.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/notes.md`
  - Consumes: T001 test; `design.md#gate-evidence-contract`; GC-GE-03 through GC-GE-08
  - Produces: clean candidate `H2` with exactly one `## Gate Evidence` section after `## Evidence Discipline`; green direct test; ignored T002 review package; separate read-only review; durable T002 evidence.
  - Verify: Commit the standard edit as `H2`; in that task's fresh shell run `set -o pipefail && BASE=e10a5d221f081fb6d099d342597a707b0dad91c9 && CHANGE=2026-09-08-gate-evidence-schema && H2="$(git rev-parse HEAD)" && python3 tests/test_gate_evidence_schema.py && python3 scripts/sdc-review-package.py "$BASE" "$H2" "$CHANGE" T002 && git diff --check "$BASE..$H2" && CHANGED_PATHS="$(git diff --name-only "$BASE..$H2")" && ! printf '%s\n' "$CHANGED_PATHS" | rg -n -v "^(sdc-references/workflow-standards\.md|tests/test_gate_evidence_schema\.py|\.sdc/changes/active/$CHANGE/)"`.
  - Expected: compliant record passes; every named malformed record is rejected; audit boundary stays intact; no runtime or default-command path changes.
  - Review: Pending
  - Evidence: Pending
  - Source: `spec.md#REQ-GE-01`, `spec.md#AC-GE-01`, `spec.md#REQ-GE-02`, `spec.md#AC-GE-02`

- [ ] T003 [REQ-GE-01,REQ-GE-02,REQ-GE-03] [AC-GE-01,AC-GE-02,AC-GE-03] [Phase 3] [Size: M] Capture the full clean candidate, verify all acceptance checks, and bind it to the authorized PR head.
  - Depends on: T002 approved review and durable evidence; authorized PR controller and PR URL
  - Files: `.sdc/changes/active/2026-09-08-gate-evidence-schema/tasks.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/notes.md`
  - Consumes: `C3=HEAD` at task start; Base; T002 green test; authorized PR URL; GC-GE-01 through GC-GE-09
  - Produces: an append-only PR checkpoint that names Base, full `C3`, observed matching PR head, `Base..C3` range, allowlist result, and command results; ignored T003 review package; separate read-only review; durable Candidate Snapshot Ledger in notes.
  - Verify: In that task's fresh shell, require `SDC_PR_URL` and run `set -o pipefail && BASE=e10a5d221f081fb6d099d342597a707b0dad91c9 && CHANGE=2026-09-08-gate-evidence-schema && : "${SDC_PR_URL:?set SDC_PR_URL to the authorized PR URL}" && C3="$(git rev-parse HEAD)" && PR_HEAD="$(gh pr view "$SDC_PR_URL" --json headRefOid --jq .headRefOid)" && test -z "$(git status --porcelain --untracked-files=all)" && test "$C3" = "$PR_HEAD" && git merge-base --is-ancestor "$BASE" "$C3" && python3 tests/test_gate_evidence_schema.py && git cat-file -e "${BASE}:sdc-cli.py" && git show "${BASE}:sdc-cli.py" | python3 - validate "$CHANGE" && git diff --check "$BASE..$C3" && CHANGED_PATHS="$(git diff --name-only "$BASE..$C3")" && ! printf '%s\n' "$CHANGED_PATHS" | rg -n -v "^(sdc-references/workflow-standards\.md|tests/test_gate_evidence_schema\.py|\.sdc/changes/active/$CHANGE/)" && python3 scripts/sdc-review-package.py "$BASE" "$C3" "$CHANGE" T003`.
  - Expected: absent PR, failed query, changed PR head, test failure, package-validation failure, or allowlist failure stops the task before reviewer dispatch; otherwise every checkpoint and review names the same full `C3`.
  - Review: Pending
  - Evidence: Pending
  - Source: `spec.md#AC-GE-01`, `spec.md#AC-GE-02`, `spec.md#AC-GE-03`

- [ ] T004 [REQ-GE-01,REQ-GE-02,REQ-GE-03] [AC-GE-01,AC-GE-02,AC-GE-03] [Phase 4] [Size: M] Obtain a fresh independent review of the recorded T003 content candidate and preserve only its durable result.
  - Depends on: T003 approved review and durable evidence
  - Files: `.sdc/changes/active/2026-09-08-gate-evidence-schema/tasks.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/notes.md`
  - Consumes: Candidate Snapshot Ledger; exact Base and `C3`; T003 review package; GC-GE-02 and GC-GE-06 through GC-GE-09
  - Produces: fresh read-only review of exact `Base..C3` with separate Spec Compliance and Code Quality verdicts; durable T004 evidence citing `git:C3`.
  - Verify: Copy the exact full `C3` from the Candidate Snapshot Ledger into the fresh task shell, then run `set -o pipefail && BASE=e10a5d221f081fb6d099d342597a707b0dad91c9 && CHANGE=2026-09-08-gate-evidence-schema && : "${C3:?set C3 from the Candidate Snapshot Ledger}" && git cat-file -e "$C3^{commit}" && git merge-base --is-ancestor "$BASE" "$C3" && python3 tests/test_gate_evidence_schema.py && git cat-file -e "${BASE}:sdc-cli.py" && git show "${BASE}:sdc-cli.py" | python3 - validate "$CHANGE" && git diff --check "$BASE..$C3" && CHANGED_PATHS="$(git diff --name-only "$BASE..$C3")" && ! printf '%s\n' "$CHANGED_PATHS" | rg -n -v "^(sdc-references/workflow-standards\.md|tests/test_gate_evidence_schema\.py|\.sdc/changes/active/$CHANGE/)" && python3 scripts/sdc-review-package.py "$BASE" "$C3" "$CHANGE" T004`.
  - Expected: no Critical or Important finding and no acceptance-affecting `Cannot verify`; any durable evidence update is limited to this package's tasks/notes and cites `C3`.
  - Review: Pending
  - Evidence: Pending
  - Source: `spec.md#AC-GE-01`, `spec.md#AC-GE-02`, `spec.md#AC-GE-03`

## 验证任务

- [ ] T900 [REQ-GE-01,REQ-GE-02,REQ-GE-03] [AC-GE-01,AC-GE-02,AC-GE-03] [Phase Verify] [Size: M] Capture one final candidate, execute the full matrix, and obtain a whole-change review.
  - Depends on: T000 through T004 each approved with durable evidence; authorized PR controller and PR URL
  - Files: `.sdc/changes/active/2026-09-08-gate-evidence-schema/tasks.md`, `.sdc/changes/active/2026-09-08-gate-evidence-schema/notes.md`
  - Consumes: final `C900=HEAD`; all prior approval evidence; Candidate Snapshot Ledger; Artifact Output Contract; GC-GE-01 through GC-GE-09
  - Produces: final PR checkpoint for Base, `C900`, PR URL, and observed matching head; final review package; Final Whole-Change Review with separate approved verdicts and durable `git:C900` evidence.
  - Verify: In that task's fresh shell, require `SDC_PR_URL` and run `set -o pipefail && BASE=e10a5d221f081fb6d099d342597a707b0dad91c9 && CHANGE=2026-09-08-gate-evidence-schema && : "${SDC_PR_URL:?set SDC_PR_URL to the authorized PR URL}" && C900="$(git rev-parse HEAD)" && PR_HEAD="$(gh pr view "$SDC_PR_URL" --json headRefOid --jq .headRefOid)" && test "$C900" = "$PR_HEAD" && test -z "$(git status --porcelain --untracked-files=all)" && git merge-base --is-ancestor "$BASE" "$C900" && python3 tests/test_gate_evidence_schema.py && git cat-file -e "${BASE}:sdc-cli.py" && git show "${BASE}:sdc-cli.py" | python3 - validate "$CHANGE" && git diff --check "$BASE..$C900" && CHANGED_PATHS="$(git diff --name-only "$BASE..$C900")" && ! printf '%s\n' "$CHANGED_PATHS" | rg -n -v "^(sdc-references/workflow-standards\.md|tests/test_gate_evidence_schema\.py|\.sdc/changes/active/$CHANGE/)" && python3 scripts/sdc-review-package.py "$BASE" "$C900" "$CHANGE" final`.
  - Expected: every AC is covered; final review names the same Base/`C900`/PR-head snapshot; no product, runtime, profile, default-command, JSON manifest, or lifecycle-state path changes.
  - Review: Pending
  - Evidence: Pending
  - Source: `spec.md#AC-GE-01`, `spec.md#AC-GE-02`, `spec.md#AC-GE-03`

## Per-Task Review Gates

| Task | Required before the next task starts | Durable controller update |
|---|---|---|
| T000 | Separate reviewer approves Base, bundle digest/integrity, nine-file package, validator, handoff, and allowlist evidence. | Mark T000 complete; record `Evidence: git:H0` and review reference in notes. |
| T001 | Separate reviewer approves red-test coverage and diagnostic boundary. | Mark T001 complete; record exact candidate evidence and review reference. |
| T002 | Separate reviewer approves section wording, audit-safe placement, green test, and allowlist. | Mark T002 complete; record exact candidate evidence and review reference. |
| T003 | Separate reviewer approves exact candidate snapshot, test matrix, Base/PR equality, and allowlist. | Mark T003 complete; record Candidate Snapshot Ledger and review reference. |
| T004 | Fresh reviewer approves the exact recorded `Base..C3` review. | Mark T004 complete; record `Evidence: git:C3` and review reference. |
| T900 | Whole-change reviewer approves exact final range, all AC evidence, and matching PR head. | Mark T900 complete; record Final Whole-Change Review and `Evidence: git:C900`. |
