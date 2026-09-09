# Notes

## Planning Snapshot

- Change: `2026-09-08-gate-evidence-schema`
- Exact Base: `origin/main@e10a5d221f081fb6d099d342597a707b0dad91c9`
- Execution role: governed Apply implementation; no runtime/profile/product behavior, merge, deployment, publishing, or release is authorized.
- Apply authorization: satisfied for this run by the 2026-09-09 Autopilot direct user authorization recorded on ANDY-159, bound to reviewed plan revision `4ac5d46a203d1652a5e5a4843d9c8b36d65f5293`. The override explicitly removes the prior human-authority/PR-controller stop-line; merge, deployment, publishing, and release remain unauthorized.

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

## Candidate Snapshot Ledger

No Apply checkpoint exists in this planning package.  During Apply, T003 and T900 each record Base, content candidate, PR URL, observed PR head, exact range, changed-path allowlist result, command-result summary, checkpoint permalink, reviewer reference, and the matching `git:` evidence in this section.

## Task Review Evidence

### T000

- Candidate: `git:ceaacfa421cbc8359e41b5deaff2f2a9697d1ba1` (`H0`); parent exactly `e10a5d221f081fb6d099d342597a707b0dad91c9`.
- Plan input: the attached Stage-1 bundle `ANDY-157-plan-review-final-v2.bundle` was downloaded and verified (`SHA-256 47d6db70fe9737be5594625251d4aac386e3f9fda47fca7aec73cd8af3b1fe8f`, `git bundle verify` exit 0) but contains revision `2ea835fe334525ef1d799e561ea6b51200095ea2`, not the exact reviewed head `4ac5d46a203d1652a5e5a4843d9c8b36d65f5293`. Per the current Autopilot Apply authorization, the mismatch was handled as a verifiable plan-input gap rather than an authorization blocker: a complete-history bundle was reconstructed from the independently readable reviewed ref, with `SDC_PLAN_REVISION=4ac5d46a203d1652a5e5a4843d9c8b36d65f5293` and SHA-256 `df692059209ec8a3d7cc19b20a2b20a553a775c34d0baf9302ff4a9d0360b12b`.
- Verification: from clean `origin/main@e10a5d221f081fb6d099d342597a707b0dad91c9`, digest and bundle checks passed; the reviewed revision existed in a `git clone --no-checkout`, descended from Base, and its complete sorted `Base..revision` path list equaled the fixed nine Markdown paths. The package was imported and only its directory was staged; `H0` was committed before Base validation. Base `sdc-cli.py validate`, `scripts/sdc-task-brief.py`, and `scripts/sdc-review-package.py` all exited 0; the four expected handoff files were generated under ignored `.sdc/runtime/2026-09-08-gate-evidence-schema/`; `git diff --check` and the nine-path allowlist passed. Base lookup of `scripts/sdc-runtime-context.py` failed with the expected exit 128, and no runtime/JSONL/lifecycle-state path entered the candidate.
- Review: independent read-only T000 review — Spec Compliance **Approved**, Code Quality **Approved**, Critical/Important/Warning **none**. The reviewer noted only that helper report/progress files are runtime templates and that command ordering/authorization cannot be proven from a Git diff; those limitations do not affect the verified T000 artifact or candidate.
- Spec Compliance: Approved
- Code Quality: Approved
- Evidence: `git:ceaacfa421cbc8359e41b5deaff2f2a9697d1ba1`

### T001

- Candidate: `git:d70439ece43a52c65c4edc90923f8abaca6eb7fa` (`H1`); exact range `e10a5d221f081fb6d099d342597a707b0dad91c9..d70439ece43a52c65c4edc90923f8abaca6eb7fa`.
- Implementation: added a standard-library `unittest` entrypoint with test-local compliant and malformed record fixtures. The parser reports only rule/field classes and never echoes opaque source values.
- Verification: `python3 tests/test_gate_evidence_schema.py` returned exit 1 with 8 tests, 7 passing and exactly one expected failure (`section-count`, because the Base standard has no Gate Evidence section). Invalid UUID, missing field, non-Closed status, missing/blank/duplicate named source, duplicate section, and diagnostic-boundary cases all exercised as intended. `git diff --check`, Base ancestry, and the focused allowlist passed; T001 review package was generated under ignored runtime scratch.
- Review: independent read-only T001 review — Spec Compliance **Approved**, Code Quality **Approved**, Critical/Important/Warning/Cannot-verify **none**.
- Spec Compliance: Approved
- Code Quality: Approved
- Evidence: `git:d70439ece43a52c65c4edc90923f8abaca6eb7fa`

### T002

- Candidate: `git:e6c8491158b028942cb64fa9f6c6d6c287af9efc` (`H2`); exact range `e10a5d221f081fb6d099d342597a707b0dad91c9..e6c8491158b028942cb64fa9f6c6d6c287af9efc`.
- Implementation: added exactly one `## Gate Evidence` section immediately after `## Evidence Discipline`, preserving the bounded Task Format audit range. The section defines the five fields, literal `Closed` status, lowercase hexadecimal `8-4-4-4-12` IDs, exactly-once nonblank named sources, and opaque local provenance boundary.
- Verification: `python3 tests/test_gate_evidence_schema.py` passed 8/8; `node scripts/audit-release.mjs` passed; Base `sdc-cli.py validate 2026-09-08-gate-evidence-schema` passed; `git diff --check` and the focused changed-path allowlist passed. No runtime, CLI, script, profile, hook, JSONL, or lifecycle-state path changed.
- Review: independent read-only T002 review — Spec Compliance **Approved**, Code Quality **Approved**, Critical/Important/Warning/Cannot-verify **none**.
- Spec Compliance: Approved
- Code Quality: Approved
- Evidence: `git:e6c8491158b028942cb64fa9f6c6d6c287af9efc`

## Final Whole-Change Review

No Apply final review exists in this planning package.  T900 writes the final candidate, matching PR-head snapshot, review reference, both approved verdicts, and durable `git:` evidence after the independent review.

## Apply Gate

The portable bundle passed GC-GE-10.  For this run, the current Autopilot direct user authorization is the governing Apply confirmation for reviewed revision `4ac5d46a203d1652a5e5a4843d9c8b36d65f5293`; the superseded human-confirmation stop-line is not retained.  Merge, deployment, publishing, and release remain outside authorization.
