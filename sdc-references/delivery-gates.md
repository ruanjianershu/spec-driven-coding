# SDC Delivery Gates

This reference contains the shared validation, review, test, quality, check, and archive rules.

For `compact.json`, use the equivalent artifact requirements in `compact-workflow.md` instead of the standard Markdown document list. Confirmation, impact assessment, current receipts, and independent review remain mandatory. Unresolved recorded findings block approval and delivery; see `review-findings.md` for issue identity and repair limits.

Load only the gate needed for the current stage. Use `workflow-standards.md` when judging risk level, authorization, or evidence freshness. All `light` / `standard` / `strict` changes meet the same semantic acceptance; validation breadth follows affected sources and named risks, not fixed full-repository loops.

## Validate Gate

Validate artifacts for the target stage, not only file existence.

Check:

- `.sdc/constitution.md` exists and does not conflict with `AGENTS.md`.
- `.sdc/common-ground.md` exists and relevant `OPEN` / high-impact `WORKING` items are not used as final execution inputs.
- `.sdc/expert-routing.md` exists and relevant expert profiles are selected for plan/check when the change touches product, domain, legacy, architecture, API, data, frontend, backend, tests, security, operations, or documentation risk.
- `.sdc/knowledge/index.md` exists and relevant product/technical knowledge sources are listed in final spec/design/context-pack.
- `.sdc/memory/` candidates are not treated as confirmed facts.
- Final spec/design/context-pack include Artifact Output Contract.
- Triggered output artifacts exist or are explicitly `N/A` with evidence: process/state diagram, sequence/integration diagram, API/contract specification, data/migration contract, UX flow/states, test matrix, deploy/release checklist, AI involvement note.
- Final spec/design/context-pack/tasks/impact do not contain `Assumed`, `Proposed`, `TBD`, `Conflict`, `Stale`, or open Knowledge Gaps.
- Knowledge rows include evidence identity: Status, Source, Verified At, Verified Against, and Scope where applicable.
- Source identity and authorization scope are current. Required manifests and approval snapshots verify; missing, malformed, or stale evidence blocks reuse. Same-state retries do not reapprove changed inputs; revisions use explicit reasoned reopen.
- Four intake categories are covered by cited user/project confirmation or evidence-based non-applicability; missing business requirements remain in discovery. Risk level, triggers, and rationale are visible, and any downgrade has new evidence and explicit user approval.
- Candidate rows include Source, Evidence Needed, Target, and Promotion Gate.
- Specs contain Glossary, invariants, SCN/REQ/AC, acceptance criteria, validation strategy, and traceability.
- Tasks use `T### [REQ-*] [AC-*] [Phase] [Size]`.
- Task sizes are only `S` or `M`.
- Final plan includes exact Global Constraints and `Plan Preflight: Passed`.
- Every task declares Files, Consumes, Produces, Verify, Expected, Review, Evidence, and Source.
- Meaningful behavior tests precede the implementation they verify; behavior-neutral edits have a justified focused validation path instead of artificial failing tests.
- Decision Ledger exists for high-impact decisions.
- `Proposed`, `Assumed`, `TBD`, and `Conflict` items do not enter final REQ/AC/design/tasks/apply.
- Brownfield changes have a current `impact.md` with no blocking open questions.
- Discovery Closed changes have a `context-pack.md` for execution handoff and `knowledge-candidates.md` for apply/check discoveries.
- `context-pack.md` lists Common Ground used and Expert Profiles Used when they materially affect execution.
- `context-pack.md` summarizes required output artifacts for apply/check handoff.
- Artifacts are not empty templates.
- Checked tasks have `Review: Approved` and durable evidence; `Cannot verify` and `Needs fixes` remain blockers.

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
- Expert profile mismatch: actual diff touches a risk area that was not routed through the corresponding profile or standards.
- Artifact output mismatch: actual diff touches workflow, integration, API, data, UX, test, deploy, or AI-assisted delivery risk not covered by the artifact contract.
- Task orchestration mismatch: completed task lacks its dual-verdict review/evidence, runtime ledger disagrees with durable artifacts, or final whole-change review is missing.

Every finding needs a file/line reference, consequence, and actionable fix. If no issues are found, state remaining test or context gaps.

Task-scoped review must return separate Spec Compliance and Code Quality verdicts. Review is read-only. Use `Cannot verify from diff` for requirements that need focused controller evidence; do not silently approve them.

Preserve independent reviewer judgment and final whole-change review. For a single-task light change, one pass over the final snapshot may supply both task and final records. Check can assess that evidence without rerunning an unchanged review. Use a separate reviewer context when supported and authorized; disclose limitations of an inline role-separated pass.

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
- Actual exit status, source snapshot, and execution receipt for commanded validation; appended assertions are not receipts.

Coverage percentage is useful but not proof of requirement validation.

Select the smallest set of checks that proves affected ACs and regression boundaries. Reuse trustworthy current receipts; rerun for changed inputs, missing coverage, or a named unresolved risk, not merely a new stage. Failed, timed-out, missing, stale, or skipped required checks cannot count as passing. Manual evidence must name the observable result and scope; it cannot silently replace a required executable check.

## Quality Gate

Final quality checks should cover:

- User-facing flow or smoke test.
- Setup and documentation clarity.
- Code quality and formatting.
- Security baseline.
- Performance baseline, or `N/A` with a concrete reason.
- Maintainability.
- Release or deployment readiness.
- Artifact Output Contract coverage and N/A reasons.
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
- Suggested `.sdc/common-ground.md` and `.sdc/expert-routing.md` updates when repo evidence or repeated checks justify them.
- Suggested `.sdc/knowledge/product`, `.sdc/knowledge/technical`, and `.sdc/memory` updates when repo or change evidence justifies them.
- Suggested Artifact Output Contract defaults when repeated repo patterns require diagrams, API/data contracts, deploy checklists, or test matrices.
- Evidence index.

## Archive Gate

Archive only completed, validated, checked changes.

Block archive when:

- `spec.md` is still a template or draft without confirmation.
- Key tasks are unfinished.
- Traceability chain is broken.
- Current review/test/security/quality evidence is missing, or a narrative assertion substitutes for a required execution receipt.
- Plan Preflight, per-task approved review evidence, or final whole-change review evidence is missing.
- `.sdc/specs/<change-id>.md` already exists and overwrite is not explicitly allowed.
- Residual work is hidden instead of recorded as deferred scope or a new change.

Archive must run Knowledge Compact Gate before it is considered complete.

Required archive outputs:

- Final confirmed spec promoted to `.sdc/specs/<change-id>.md`.
- Completed change history under `.sdc/changes/archive/<change-id>/`.
- `archive.md` with conclusion, evidence, residual risks, coverage summary, and Knowledge Compact Gate summary.

Knowledge Compact Gate must evaluate:

Use candidates and affected-source links to select destinations below; do not reread or update every asset by habit. Proposals identify exact target, evidence, freshness, and the incremental change. Unaffected destinations may be `N/A` with a short reason.

- `.sdc/specs/` promotion.
- `.sdc/changes/archive/` preservation.
- `.sdc/decisions/` for long-lived product, technical, architecture, data, permission, rollout, or security decisions.
- `.sdc/knowledge/product/` for durable product goals, roles, flows, business rules, non-goals, or product decisions.
- `.sdc/knowledge/technical/` for durable stack, architecture, module, data/interface, operations, or testing knowledge.
- `.sdc/memory/` for useful procedures, lessons, gotchas, and candidate knowledge that should remain reviewable.
- `.sdc/common-ground.md` for confirmed, rejected, promoted, demoted, or newly opened shared assumptions.
- `.sdc/expert-routing.md` for reusable expert profile triggers, stack-specific profiles, or missing risk coverage.
- `.sdc/standards/` for reusable engineering rules.
- `AGENTS.md` through `sdc-harness` for AI execution guardrails.
- `.sdc/reports/bug/` for durable root-cause records.
- `.sdc/reports/impact/` or archive final impact notes for Brownfield/Legacy effects.
- `.sdc/project.md` for long-lived project context changes.
- `.sdc/project-cognition.md` only when repo-level cognition is stale, incomplete, or structurally affected.

Optional durable memory updates may be deferred, but the archive output must say why. They must not be written without explicit human confirmation.

This includes personal/native memory and research recall: all remain Candidate until verified and explicitly approved for the specific destination. Cross-device memory writes need the user's explicit request, not implicit archive consent.

Do not add or require a separate public compact command. Knowledge compaction is an internal archive gate.
