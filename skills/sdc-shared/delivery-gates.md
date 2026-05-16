# SDC Delivery Gates

This reference contains the shared validation, review, test, quality, check, and archive rules.

## Validate Gate

Validate artifacts for the target stage, not only file existence.

Check:

- `.sdc/constitution.md` exists and does not conflict with `AGENTS.md`.
- Specs contain Glossary, invariants, SCN/REQ/AC, acceptance criteria, validation strategy, and traceability.
- Tasks use `T### [REQ-*] [AC-*] [Phase] [Size]`.
- Task sizes are only `S` or `M`.
- Tests precede the implementation work they verify.
- Decision Ledger exists for high-impact decisions.
- `Proposed`, `Assumed`, `TBD`, and `Conflict` items do not enter final REQ/AC/design/tasks/apply.
- Brownfield changes have a current `impact.md` with no blocking open questions.
- Artifacts are not empty templates.

Conclusion must be either ready for next stage or blocked with concrete repair guidance.

## Review Gate

Review the actual diff and relevant surrounding code. Lead with findings ordered by severity.

Cover:

- Correctness and behavior regressions.
- Architecture and module boundaries.
- Data integrity and migration risks.
- Security and permission boundaries.
- Compatibility and public contracts.
- Performance risks.
- Maintainability and clarity.
- Brownfield impact mismatch against `impact.md`.

Every finding needs a file/line reference, consequence, and actionable fix. If no issues are found, state remaining test or context gaps.

## Test Gate

Test against acceptance criteria, not only implementation details.

Report:

- Commands run.
- Pass/fail summary.
- ACs covered and uncovered.
- Boundary, error, security, compatibility, and regression coverage.
- Flaky or skipped tests.
- Failure details sufficient to reproduce.
- Risk caused by tests that could not run.

Coverage percentage is useful but not proof of requirement validation.

## Quality Gate

Final quality checks should cover:

- User-facing flow or smoke test.
- Setup and documentation clarity.
- Code quality and formatting.
- Security baseline.
- Performance baseline when relevant.
- Maintainability.
- Release or deployment readiness.
- Validation evidence.

Any serious blocker means no ship.

## Combined Check Modes

`sdc-check` may operate in these modes:

| Mode | User intent | Behavior |
| --- | --- | --- |
| delivery | "check", "acceptance", "can ship" | Run validate + review + test + quality perspectives. |
| bug | "why failed", "debug", "analyze bug" | Analyze only; do not modify code unless user explicitly asks. |
| impact | "what will this affect", "is this safe" | Produce impact and regression risk analysis. |
| repo | "analyze repository", "onboard legacy project" | Produce code-evidence-based project cognition. |

## Bug Analysis Output

Include:

- Symptom and reproduction.
- Logs, stack traces, failing command, or failing test.
- Relevant spec/design/tasks/notes if available.
- Code evidence and recent changes.
- Root-cause candidates ordered by confidence.
- Whether artifacts need updates.
- Recommended next SDC step.

Do not fix code in bug mode unless explicitly asked.

## Repo / Brownfield Analysis Output

Include:

- Stack, entrypoints, build commands, test commands.
- Core modules and dependency direction.
- Initial business capability map.
- Data and public contract clues.
- Quality and maintainability risks.
- Suggested `.sdc/specs`, `.sdc/standards`, and `AGENTS.md` updates.
- Evidence index.

## Archive Gate

Archive only completed, validated, checked changes.

Block archive when:

- `spec.md` is still a template or draft without confirmation.
- Key tasks are unfinished.
- Traceability chain is broken.
- Check or equivalent review/test/security/quality evidence is missing.
- `.sdc/specs/<change-id>.md` already exists and overwrite is not explicitly allowed.
- Residual work is hidden instead of recorded as deferred scope or a new change.

