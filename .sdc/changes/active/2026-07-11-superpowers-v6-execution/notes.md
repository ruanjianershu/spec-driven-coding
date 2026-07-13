# Notes

## Changed Files

- Added execution orchestration shared reference and routed plan/apply/check/direct skills.
- Added task schema, preflight, review/evidence, runtime ledger, and delivery completion validators.
- Added task brief, review package, and deterministic Codex package helpers.
- Added Codex marketplace metadata, rootless/minimal portal packaging, and updated plugin descriptions/version.
- Added npm cache exclusions, safe runtime-ignore migration, eval/audit/docs, and upgraded the project `.sdc` workspace.

## Task Review Evidence

### T001

- Spec Compliance: Approved
- Code Quality: Approved
- Evidence: notes.md#validation-evidence

### T002

- Spec Compliance: Approved
- Code Quality: Approved
- Evidence: notes.md#validation-evidence

### T003

- Spec Compliance: Approved
- Code Quality: Approved
- Evidence: notes.md#validation-evidence

### T004

- Spec Compliance: Approved
- Code Quality: Approved
- Evidence: notes.md#validation-evidence

### T900

- Spec Compliance: Approved
- Code Quality: Approved
- Evidence: notes.md#validation-evidence

## Validation Evidence

- `npm run audit`: passed for SDC 1.3.0.
- `npm run eval:sdc`: all 51 deterministic scenarios passed, including strict field/section ambiguity blockers.
- Python compile passed for the CLI, helpers, package script, and eval provider/runner.
- Node syntax checks passed for the installer and release audit.
- Repeated `sdc init` left the working tree unchanged.
- Isolated Codex install exposed 14 real skills with no `sdc-shared`; isolated Claude install exposed 8 commands and 6 advanced skills with no duplicate root skills.
- Claude marketplace validation passed; npm dry-run contained 59 files with no Python cache leakage.
- Two Codex portal builds were rootless/minimal and byte-identical.
- Four independent blocking-review passes plus iterative re-review found and closed validator, migration, packaging, and install issues; the final install-boundary re-review approved both verdicts.

## Final Whole-Change Review

- Status: Approved
- Scope: complete branch diff for execution contract, CLI, helpers, packaging, evals, docs, metadata, and `.sdc` migration.
- Spec Compliance: Approved
- Code Quality: Approved
- Evidence: notes.md#validation-evidence
- Cannot verify from diff: npm registry publication and external marketplace ingestion are outside this local change and are not claimed.

## Knowledge Candidates

See knowledge-candidates.md. Archive confirmation is required before promoting them.
