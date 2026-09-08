# Notes

## Planning Snapshot

- Change: `2026-09-08-gate-evidence-schema`
- Exact Base: `origin/main@e10a5d221f081fb6d099d342597a707b0dad91c9`
- Planning role: architecture planning only; no runtime/profile/product implementation, PR, merge, deployment, publishing, or release occurred.
- Apply authorization: the latest Autopilot handoff for ANDY-159 explicitly authorized governed Apply for reviewed revision `4ac5d46a203d1652a5e5a4843d9c8b36d65f5293` and instructed the executor not to retain the superseded Apply stop-line. This execution follows that direct authorization; the handoff also authorizes a PR when the candidate is ready, but not merge, deploy, release, or publication.

## Root-Cause Repair

| Item | Old T000 interface | Revised T000 interface |
|---|---|---|
| Base runtime dependency | `scripts/sdc-runtime-context.py` generated Apply/Check JSONL records and lifecycle state. | Base `sdc-cli.py validate` validates nine Markdown artifacts; Base task/review helpers create ignored Markdown handoff files. |
| Script availability | Absent from exact Base. | `sdc-cli.py`, `sdc-task-brief.py`, and `sdc-review-package.py` are tracked Base files. |
| Schema | Referenced `sdc.change-state/v1` and `sdc.context-manifest-record/v1` without Base support. | Uses existing Markdown task brief/report/progress/review-package format; no JSON schema is consumed or produced. |
| Allowlist | Excluded the required runtime script. | Contains only the shared standard, direct test, and focused Markdown package; helpers are read-only tools. |
| Apply gate | Inconsistent between first and second task. | One rule: human Apply authorization is required before T000. |
| Review-object availability | The exact plan revision existed only in the executor's local object database. | The nine-file revision is delivered as an attached portable Git bundle with a SHA-256 digest; T000 verifies digest, bundle, revision, Base ancestry, and exact fixed nine-path equality before import. |
| Shell pipeline | In zsh, `"$BASE:sdc-cli.py"` is an invalid parameter expansion and its failed `git show` can be masked by a pipeline's final command. | Use `${BASE}:sdc-cli.py`, preflight `git cat-file -e`, and `set -o pipefail` for every Git-object validator pipeline. |
| Plan path set | A check that accepts only a count of nine can admit a missing required artifact plus an unexpected replacement. | Compare the complete sorted `Base..revision` changed-path list to the fixed nine repository-relative paths before archive/import. |
| Candidate materialization | Archive import alone does not identify the exact planned files as the candidate commit. | Stage only the verified package directory and create `H0` before Base validation, handoff, diff, and review checks. |

## Evidence Read

| Command | Exit code | Result |
|---|---:|---|
| `git fetch origin main` | 0 | Refreshed the exact remote main object for this planning run. |
| `git rev-parse origin/main` | 0 | `e10a5d221f081fb6d099d342597a707b0dad91c9`. |
| `git cat-file -e origin/main:scripts/sdc-runtime-context.py` | 128 | The former required script is not in the Base. |
| `git ls-tree -r --name-only origin/main -- scripts` | 0 | Base scripts contain audit, package, task-brief, and review-package helpers; not the former script. |
| `git show origin/main:sdc-cli.py` | 0 | Base validates active Markdown change packages. |
| `git show origin/main:scripts/sdc-task-brief.py` | 0 | Base emits task brief/report/progress Markdown handoff from tasks/context. |
| `git show origin/main:scripts/sdc-review-package.py` | 0 | Base emits a review package for an exact Git range. |
| `git show origin/main:sdc-references/artifact-schemas.md` | 0 | Runtime directory is ignored scratch; no JSONL manifest/lifecycle-state schema is defined. |

## Plan Preflight Evidence

- Status: Passed
- Reviewed Against: spec.md, impact.md, design.md, tasks.md, context-pack.md, Artifact Output Contract, Base validator, Base helper interfaces, portable-bundle replay, and execution-orchestration.md.
- Findings: Resolved: old runtime dependency, schema claim, allowlist mismatch, executor-local-only review object, zsh Git-object pipeline masking, cardinality-only package acceptance, implicit H0 materialization, Apply-gate mismatch, and traceability mismatch have been removed.
- Raw validator and mechanical-check output are recorded after the revision package is generated and checked in this planning run.

## Validation Evidence

| Command | Exit code | Result |
|---|---:|---|
| `git show origin/main:sdc-cli.py \| python3 - validate 2026-09-08-gate-evidence-schema` | 0 | Exact-Base artifact validation passed. |
| `python3 sdc-cli.py validate 2026-09-08-gate-evidence-schema` | 0 | Current-worktree structural cross-check passed. |
| `git show origin/main:scripts/sdc-task-brief.py \| python3 - 2026-09-08-gate-evidence-schema T000` | 0 | Exact-Base helper emitted T000 brief, report, and progress ledger. |
| `git archive origin/main` plus plan-package archive smoke | 0 | Reconstructed source bytes from the exact Base plus this plan package in ignored scratch. |
| Base-snapshot `python3 sdc-cli.py validate 2026-09-08-gate-evidence-schema` | 0 | The nine-file package passed using the Base executable from that snapshot. |
| Base-snapshot `test ! -e scripts/sdc-runtime-context.py` | 0 | Confirms the smoke contains no former script. |
| Base-snapshot `python3 scripts/sdc-task-brief.py 2026-09-08-gate-evidence-schema T000` | 0 | Emitted the expected T000 brief, report, and progress ledger from Base source bytes. |
| Legacy runtime command/schema scan | 1 | No old invocation, generator command, JSONL filename, or state-set command remains in the revised package. |
| Unconfirmed-input scan | 1 | No forbidden execution-input marker occurs in the revised package. |
| `git diff --check` | 0 | No whitespace error before staging the plan revision. |

## Task Review Evidence

### T000 — approved

- Candidate: `git:9e6484ba0bda0fd0bfc98d6972aa33abe7136d12` (`H0`), parent exactly `e10a5d221f081fb6d099d342597a707b0dad91c9`.
- Plan input: `.sdc/runtime/plan-input/ANDY-159-plan-review-reconstructed.bundle`, SHA-256 `b99400ab6ba4c4d7a2a83250bee37bc97e8fc510555c1b0fd1ed60dd94ba5cc8`; `git bundle verify` passed; revision `4ac5d46a203d1652a5e5a4843d9c8b36d65f5293` is a Base descendant and its complete sorted diff is exactly the nine planned Markdown paths.
- Source/provenance note: the attached Stage-1 bundle available to this run was obsolete (`2ea835fe334525ef1d799e561ea6b51200095ea2`, SHA-256 `47d6db70fe9737be5594625251d4aac386e3f9fda47fca7aec73cd8af3b1fe8f`). Per the latest Apply handoff, the current reviewed revision was reconstructed from the independently retrievable `origin` ref `refs/heads/ANDY-158-runtime-context-plan` and verified before import; the obsolete attachment was not used.
- Verification: Base `sdc-cli.py validate` passed; Base task-brief and review-package helpers emitted only ignored Markdown handoffs; `git diff --check` and the focused nine-path allowlist passed; no runtime-context script, JSONL manifest, or lifecycle-state path entered the candidate.
- Review: independent read-only `t000_reviewer_luna` — Spec Compliance **Approved**, Code Quality **Approved**, no Critical/Important/Warning findings. The reviewer could not independently attest to human-vs-agent authorship of the platform Apply handoff; the current execution is authorized by the latest direct Autopilot instruction recorded above.

### T001 — approved

- Candidate: `git:4f1e9dbd634aa8e97d604474257fae7342f7e274` (`H1`), exact range `e10a5d221f081fb6d099d342597a707b0dad91c9..4f1e9dbd634aa8e97d604474257fae7342f7e274`.
- Verification: `python3 tests/test_gate_evidence_schema.py` returned nonzero with 8 tests, 7 passing and the one expected `section-count: 0 != 1` failure on the Base-standard shape; diagnostics do not echo opaque source values. `git diff --check` and the focused allowlist passed; the test uses only Python standard library and local Markdown fixtures.
- Review: independent read-only `t001_reviewer_retry` — Spec Compliance **Approved**, Code Quality **Approved**, no Critical/Important/Warning/Cannot-verify findings.

### T002 — approved

- Candidate: `git:d73900c5a3b63497211c5079c2827d82f78909a4` (`H2`), exact reviewed range `e10a5d221f081fb6d099d342597a707b0dad91c9..d73900c5a3b63497211c5079c2827d82f78909a4`.
- Implementation: added the Layout A `## Gate Evidence` standard immediately after `## Evidence Discipline`, preserving the `## Task Format` → `## Evidence Discipline` audit boundary. The section has exactly the five required fields and the specified Closed/lowercase-UUID/source-opacity rules.
- Verification: `python3 tests/test_gate_evidence_schema.py` passed all 8 tests; T002 review package was generated and bound to Base/Head; `git diff --check` and the focused allowlist passed. No runtime, default-command, script, profile, hook, or CLI path changed.
- Review: independent read-only `t001_reviewer_retry` — Spec Compliance **Approved**, Code Quality **Approved**, no Critical/Important/Warning/Cannot-verify findings.

### T003 — approved

- Candidate snapshot: `C3=git:6d05819c2fab2f000b43fee421f730203dc8363b`; Base `e10a5d221f081fb6d099d342597a707b0dad91c9`; exact range `Base..C3`.
- PR controller snapshot: `https://github.com/ruanjianershu/spec-driven-coding/pull/7`, observed open PR head exactly matched C3. Title `ANDY-152: Gate Evidence schema contract`; body included `ANDY-152` and no `closes`/`fixes`/`resolves` auto-close directive. The PR body explicitly disclaimed merge, deploy, release, and publication authorization.
- Verification: clean porcelain, Base ancestry, green 8-test direct suite, Base validator pass, `git diff --check`, focused changed-path allowlist, and T003 review package all passed. No runtime/default-command/script/profile/hook/JSONL/lifecycle-state path changed.
- Review: independent read-only `t001_reviewer_retry` — Spec Compliance **Approved**, Code Quality **Approved**, no Critical/Important/Warning/Cannot-verify findings.

### T004 — approved

- Reviewed candidate: `C3=git:6d05819c2fab2f000b43fee421f730203dc8363b`; exact range `e10a5d221f081fb6d099d342597a707b0dad91c9..6d05819c2fab2f000b43fee421f730203dc8363b`.
- Verification: exact C3 existed and descended from Base; isolated C3 test/standard content passed all 8 tests; Base validator, `git diff --check`, focused allowlist, and T004 review package all passed. No runtime/default-command/script/profile/hook/JSONL/lifecycle-state path changed.
- Review: fresh independent read-only `t001_reviewer_retry` — Spec Compliance **Approved**, Code Quality **Approved**, no Critical/Important/Warning/Cannot-verify findings. The reviewer confirmed the current HEAD was later than C3 only because it contains durable task evidence updates; product files matched C3.

## Candidate Snapshot Ledger

No Apply checkpoint exists in this planning package.  During Apply, T003 and T900 each record Base, content candidate, PR URL, observed PR head, exact range, changed-path allowlist result, command-result summary, checkpoint permalink, reviewer reference, and the matching `git:` evidence in this section.

## Final Whole-Change Review

No Apply final review exists in this planning package.  T900 writes the final candidate, matching PR-head snapshot, review reference, both approved verdicts, and durable `git:` evidence after the independent review.

## Apply Gate

The only current execution prerequisites are a portable bundle that passes GC-GE-10 and explicit human Apply confirmation meeting GC-GE-09.  This plan revision does not substitute for that confirmation.
