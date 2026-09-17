# Evidence-Governed Workflow Upgrade

Status: implementation authorized on 2026-09-16; independent review and GitHub-only submission authorized on 2026-09-17.

## Scope and Boundaries

Keep the six public lifecycle entrypoints. Preserve human ownership of high-impact decisions, minimal discovery artifacts, local-first knowledge, and candidate-only memory. The initial implementation excluded publishing/pushing; the follow-up authorizes a reviewed GitHub-only branch submission, not an npm release or GitLab update. Do not import private standards/history or modify unrelated working files.

Use existing Python standard-library helpers, Markdown references, and JavaScript packaging. Add internal operations instead of public commands. Existing human-edited project files remain protected during init upgrades.

## Implementation Tasks

- [x] T001: Add regression tests for draft confirmation, stale manifests/approvals, safe replan/resume, and execution receipts. Run failing tests before production changes.
- [x] T002: Enforce stage-specific content gates in `sdc-cli.py` and runtime helpers. Bind lifecycle evidence to source snapshots, reject stale state, support explicit revision with retained history, and keep repeat valid state transitions idempotent.
- [x] T003: Run validation through a bounded internal command runner, record actual exit status and repository snapshot, and distinguish assertions from executable evidence. Require fresh delivery receipts for upgraded changes without silently blessing legacy evidence.
- [x] T004: Replace fixed question counts with evidence-backed intake coverage. Document risk-proportionate execution, bounded authorization, selective context, source freshness, and incremental archive proposals. Keep high-impact consent and review rules.
- [x] T005: Add opt-in supported Codex hook packaging with a portable fallback, package-boundary tests, and updated audit rules. Do not enable unsupported hooks by guessing client capabilities.
- [x] T006: Add isolated, budgeted real-agent evaluation tooling with baseline/current/source comparisons and honest reports. Exercise representative scenarios with an available local CLI, reporting unavailable credentials or capabilities as blocked rather than passed.
- [x] T007: Synchronize generated skills, run full deterministic evaluation and packaging audit, inspect integrated changes independently, and document verified results and remaining limitations.

## Acceptance

Draft or open discovery never advances to confirmed. Changed governing inputs invalidate affected approvals. Malformed or stale required manifests cannot authorize execution. Replanning is explicit, traceable, and does not reapprove delivery. Same-state retry is safe only while evidence remains valid. Failed or stale validation cannot count as passed. Human decisions are not replaced by model confidence. Real-agent results are reported separately from deterministic checks.

## Verification

Use disposable fixture projects for runtime tests, including dirty and untracked source changes, missing/invalid manifests, rejected transitions without mutation, interrupted revision, failing and timed-out commands, and legacy state recovery. Run `npm run eval:sdc`, focused Python unittest suites, `npm run audit`, and deterministic plugin packaging. Use bounded real-agent trials without production resources, keep raw transcripts local, and report cost/latency only when measured.

## Verified Results (2026-09-17 Public Submission)

- `npm test`: 98 tests passed, covering evidence/state, parsing, client adapters, and agent-evaluation harness mechanics. Mock-process tests are not model behavior results.
- `npm run eval:sdc`: all 74 existing deterministic flow scenarios passed.
- Installed npm CLI regression tests: all 4 passed, preserving the public `sdc validate` dispatcher and exit statuses.
- `npm run audit`, both JavaScript entrypoint syntax checks, `git diff --check`, and npm package dry run passed.
- Claude strict marketplace and plugin validation passed. Both portable and opt-in native Codex archives built successfully; adapter tests include deterministic packaging and extracted runtime checks.
- Independent review found execution-coverage, decision-closure, race, failure-retention, and citation gaps. Fixes have regression tests, including real receipt/archive rejection paths.
- Final review fixed unsupported-gitlink omission, interrupted-run recovery, installed helper resolution, and missing direct-skill/Hermes runtime files. Regression tests exercise actual SIGINT process cleanup, per-task retries, project-local initialization, reinstall, uninstall, and direct-to-plugin migration.
- Distribution inventory now checks a freshly initialized fixture instead of depending on the repository's own workspace documents. Public payload audits reject private workspace assets and internal bootstrap links.

## Limits and Release Status

The public submission is prepared on `codex/evidence-governed-workflow-public` from GitHub `main`, retaining its installed `sdc validate` dispatch fix. Public product files are transferred without private integration history, company standards, internal installation scripts, or unrelated workspace documents. No version bump, npm publishing, or installation into active clients is part of this submission.

Real Codex CLI attempts were blocked by TLS connectivity; the Claude CLI attempt was blocked by authentication. A native subagent vague-intake probe asked before writing, but a cold-start typo probe generated excessive artifacts and stopped before delivery. See `evals/sdc-agent/SMOKE.md`. No end-to-end client, general efficiency, token-saving, or model-superiority claim is supported.

The light policy reduces review/context repetition within the existing schema, not its workspace/file minimum. A compact cold-start path and representative successful CLI trials remain separate product work before making efficiency or production-readiness claims. Local receipts are source-bound records, not tamperproof identity attestations or hermetic dependency capture.

Git submodules remain explicitly unsupported by repository source snapshots: verification fails closed instead of declaring incomplete source coverage successful.
