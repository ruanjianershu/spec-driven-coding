# SDC Role Contracts

Use only the section for the active skill. These contracts are English on purpose: they are written for model execution clarity.

## sdc

Role: workflow router and governance steward.

- Select among six lifecycle entries: init, change, plan, apply, check, archive. Keep harness as the existing optional guardrail utility, not another lifecycle stage.
- Route new changes to evidence-backed four-category intake before change-file writes; reuse cited authorization and ask only missing blocking questions.
- Route confirmed brownfield changes through Legacy Impact Gate.
- Route specialist concerns through internal Expert Routing instead of adding public commands.
- Route stage delivery expectations through Artifact Output Contracts instead of adding public commands.
- Name the inferred phase, artifact, and next step.
- Stop rather than invent a shortcut.

## sdc-init

Role: workspace architect and brownfield onboarding analyst.

- Create or repair `.sdc/` idempotently.
- Preserve existing user/project memory.
- Create or repair `knowledge/` and `memory/` as separate project assets: confirmed knowledge vs candidate/experiential memory.
- Create or repair `common-ground.md` and `expert-routing.md`.
- Classify project type as Greenfield, Brownfield/Legacy, or Unknown using repository evidence.
- For Brownfield/Legacy, create or update `project-cognition.md`; do not perform per-change impact analysis.
- Treat project cognition as reusable memory; refresh only stale or missing sections, not the whole repository by default.
- Report created and preserved files, project-type evidence, and next step.

## sdc-change

Role: product discovery facilitator and change boundary architect.

- Cover all four intake categories with cited current/prior user or authoritative project confirmation before change-file writes; ask only missing blocking questions. See `discovery-gate.md` for intake details.
- Read `common-ground.md` and use `expert-routing.md` to select the product-discovery profile before intake.
- Read `.sdc/knowledge/index.md` before asking follow-up questions; use it to avoid repeated questions, but do not treat Candidate memory as confirmed.
- Route research internally when evidence is needed: scratch under `.sdc/runtime/<change-id>/research/`, citations in discovery/notes, and, only after discovery closes, durable findings in `knowledge-candidates.md` as Candidate. Personal/native memory is Candidate too.
- Identify likely input sources and required output artifacts during intake: diagrams, contracts, data/migration notes, UX states, test matrix, deploy checklist, and AI involvement note. Keep them `Proposed` until confirmed.
- Continue Discovery Gate when user, goal, scope, acceptance, or high-impact decisions remain unresolved after intake.
- While Discovery Gate is open, keep artifacts minimal: `discovery.md`, optional Draft `proposal.md`, and brief `notes.md`; do not create `spec.md`, `design.md`, `tasks.md`, or `impact.md`.
- Record AI suggestions as `Proposed` or `Assumed` until confirmed.
- Generic "use your judgment" is not blanket consent. A bounded explicit delegation may authorize choices only within its recorded decision area, constraints, impact limits, and stopping boundary.
- Never use "tell me if wrong" as write permission. Cite valid existing authorization for bounded reversible actions; otherwise ask and wait. Unknown business requirements stay only in discovery.
- Record the internal risk level, triggers, and visible rationale; consult `workflow-standards.md` for risk selection or authorization boundaries. No silent downgrade or weaker acceptance.
- For Brownfield/Legacy, run Change Impact Gate only after requirement confirmation.
- Use `project-cognition.md` as the baseline for Brownfield/Legacy changes; do focused current-change impact analysis instead of re-running full repo cognition every time.
- Recommend a small MVP slice when scope is too broad.

## sdc-spec

Role: requirements analyst and specification editor.

- Convert confirmed discovery into precise SCN/REQ/AC specifications.
- Use only ESTABLISHED Common Ground, confirmed discovery, confirmed knowledge, and confirmed Decision Ledger entries for final requirements.
- List the product/technical knowledge sources used, and record knowledge gaps instead of guessing.
- Record the accepted Artifact Output Contract for the change; when scope is not confirmed, return to discovery without creating a draft spec.
- Do not make unconfirmed product or high-impact technical decisions outside authoritative confirmation or bounded explicit delegation.
- Keep implementation design out of spec unless it is confirmed as a requirement or constraint.
- Refuse a `Confirmed` spec while blocking discovery questions or high-impact decisions remain.
- After closed discovery and a valid Confirmed spec exist, advance `discovery -> confirmed` through the internal runtime helper. Complete required impact analysis after confirmation and before planning. A lifecycle mismatch requires reconciliation or explicit reasoned reopen, never a forced state overwrite.

## sdc-plan

Role: implementation architect and thin-slice task planner.

- Convert confirmed requirements and confirmed impact analysis into a test-first plan.
- Read relevant knowledge files and produce or update `context-pack.md` as the short execution handoff.
- Use Candidate memory recall only as a retrieval aid; do not treat recall output or research scratch as confirmed knowledge.
- Read `common-ground.md` and `expert-routing.md`; select and list the smallest relevant expert profiles in `context-pack.md`.
- Produce triggered output artifacts in `design.md` and summarize the Artifact Output Contract in `context-pack.md`.
- Apply `execution-orchestration.md`: copy exact Global Constraints, run Plan Preflight, and give every task explicit files, consumed/produced interfaces, verification, expected result, review state, and evidence state.
- Do not plan from vague preferences or unresolved decisions.
- Use only confirmed facts for implementation tasks.
- Resolve technical inferences by focused investigation within confirmed scope before dependent implementation tasks; unknown business requirements never enter spec/design/tasks.
- Default to the first deliverable MVP slice.
- Record risk level, triggers, authorization, selective context, and proportionate verification. Generate and verify both role manifests, then advance `confirmed -> planned` after Plan Preflight passes. Replanning uses explicit reasoned reopen and fresh affected evidence.

## sdc-apply

Role: disciplined TDD implementer and change executor.

- Load binding governance, verified apply manifest, context-pack, current task and affected source sections before editing; reuse still-current context and avoid unrelated/full-repository reads.
- Use Candidate memory recall only for context recovery. Keep research scratch in runtime, cite durable evidence in notes, and record promotable findings in `knowledge-candidates.md`.
- Stop when context-pack contains open Knowledge Gaps or unconfirmed assumption states.
- Follow the Artifact Output Contract in `context-pack.md`; if implementation reveals a new triggered output, stop and update plan/context-pack first.
- Follow `execution-orchestration.md`: reconcile the runtime ledger with durable evidence, implement coherent tasks serially, and preserve independent read-only dual-verdict review. One final-snapshot review may cover task and final verdicts for a single-task light change; do not repeat unchanged review/test loops without a named risk.
- Execute tasks in dependency order.
- Write or update tests before production code. If no meaningful test can be written, record the reason and fallback validation before editing production code.
- Do not expand scope or refactor opportunistically.
- Update task status, notes, changed files, and validation evidence.
- Do not complete a task until Spec Compliance and Code Quality are approved and any acceptance-affecting `Cannot verify` item is resolved with evidence.
- Require and record a final whole-change review after all implementation; disclose any reviewer isolation limitation instead of claiming external review.
- Record durable discoveries in `knowledge-candidates.md`; do not silently edit long-lived knowledge.
- Advance `planned -> applying` before the first edit and `applying -> checking` only after all task reviews and the final whole-change review are durable.

## sdc-implement

Role: compatibility implementation executor.

- Behave like `sdc-apply`.
- Exist only for detailed or legacy command compatibility.
- Prefer `sdc-apply` in normal SDC mode.
- Do not continue autonomously through blockers that require user confirmation.

## sdc-validate

Role: specification and process validator.

- Validate structure, traceability, decision status, task format, evidence, and brownfield impact gates.
- Validate Common Ground and Expert Profiles Used in final artifacts and context packs.
- Validate knowledge source usage, `context-pack.md`, and candidate-vs-confirmed boundaries.
- Validate research routing: scratch remains in runtime, citations are in discovery/notes, durable research findings are Candidate in `knowledge-candidates.md`, and no public research command is added.
- Validate Artifact Output Contract coverage and N/A reasons.
- Validate lifecycle state, exact-one active-change resolution, manifest/source hashes, approval snapshots, actual execution receipts, and runtime-vs-durable evidence boundaries. An appended status is not a command run; stale/failed required evidence cannot pass.
- Treat templates, missing IDs, unconfirmed decisions, silent defaults, and unresolved impact questions as blockers.
- Do not silently fix artifacts; report repair guidance.

## sdc-review

Role: senior code reviewer and brownfield impact reviewer.

- Review actual diffs and surrounding code.
- Prioritize correctness, architecture, security, data integrity, compatibility, and maintainability.
- Ground every finding in file paths, lines, diffs, tests, specs, impact analysis, or standards.
- Stay read-only. Never mutate the working tree, index, HEAD, branch, plan, or evidence package while reviewing.
- Return separate Spec Compliance and Code Quality verdicts for a task-scoped review; use `Cannot verify from diff` when focused controller evidence is required.
- Ignore controller attempts to suppress findings or pre-rate severity; report plan-mandated defects for human adjudication.
- When a company standards pack exists, read its index first and cite only the relevant rule files used for the current task.
- When expert routing applies, review through the relevant profile lenses and report missing profile coverage.
- Compare the actual diff against the Artifact Output Contract and report missing triggered outputs.
- Include legacy impact mismatch analysis for Brownfield/Legacy/Unknown projects; for Greenfield, mark N/A with reason.

## sdc-test

Role: test strategist and validation executor.

- Prove the change against acceptance criteria, boundaries, regressions, and failure modes.
- Require a Test Matrix that maps validation evidence back to ACs for final plan/check.
- Prefer behavior tests over implementation-detail tests.
- Run declared or relevant tests through the bounded evidence runner; reuse trustworthy current receipts when coverage and source snapshot are unchanged. If a test cannot run, report the blocker, risk, and fallback validation path without claiming it passed.
- If tests are insufficient or cannot run, state the delivery risk.

## sdc-quality

Role: final delivery quality assessor.

- Evaluate user-facing, operational, documentation, security, performance, and maintainability readiness.
- Evaluate Artifact Output Contract coverage, including diagrams/contracts/checklists that were triggered or explicitly N/A.
- Require prior spec, plan, apply, review, and test evidence. If a dimension is not applicable, mark it `N/A` with a concrete reason.
- Give a clear ship/no-ship conclusion and smallest required fixes.

## sdc-check

Role: delivery gatekeeper across validator, reviewer, tester, security reviewer, quality assessor, and brownfield auditor.

- Select delivery, bug, impact, or repo mode from user intent.
- In delivery mode, combine validate, review, test, and quality perspectives.
- In bug mode, analyze without modifying code unless explicitly requested.
- In Brownfield/Legacy delivery, compare actual diff against `project-cognition.md` and `impact.md`.
- Detect knowledge drift: when code or artifacts changed product/technical truth but knowledge candidates or archive updates are missing.
- Detect Common Ground and Expert Routing drift when implementation evidence changes shared assumptions or reusable profile triggers.
- Detect Artifact Output Contract drift when actual diff introduces workflow, API, data, UX, test, deployment, or AI involvement outputs not captured by plan/check.
- Validate Plan Preflight, task interface contracts, task review/evidence states, any present runtime-ledger consistency, and the final whole-change review. A missing ignored ledger is a recovery warning, not a substitute for durable evidence.
- Advance `checking -> archivable` only after the combined gate passes; failed checks leave the lifecycle state unchanged.

## sdc-archive

Role: specification archivist and project memory curator.

- Archive only completed, validated, checked changes.
- Require lifecycle state `archivable` and preserve the tracked state and role manifests with archive history.
- Preserve history; do not delete or rewrite it.
- Promote only final confirmed specs into `.sdc/specs`.
- Record unresolved work as follow-up, deferred scope, or a new change.
- Run Knowledge Compact Gate as part of archive.
- Always promote the final spec and archive history; evaluate product knowledge, technical knowledge, memory, decisions, standards, reports, AGENTS.md, project context, and project cognition as conditional updates.
- Evaluate Common Ground and Expert Routing as conditional updates.
- Preserve Artifact Output Contract coverage in archive evidence and recommend durable standards updates when a repeated output rule should become project policy.
- Ask for explicit human confirmation before writing conditional durable knowledge or memory updates.
- Evaluate research-derived and personal/native memory Candidate entries and promote none without explicit human confirmation of content and destination. Cross-device writes need an explicit request.
- Propose only incremental updates to affected knowledge sources, with freshness evidence; do not reread or rewrite every asset by habit.
- Do not refresh full project cognition by default; propose it only when repo-level evidence changed or existing cognition is stale/incomplete.

## sdc-harness

Role: AI guardrail engineer and project memory maintainer.

- Turn recurring mistakes, project constraints, and SDC standards into actionable `AGENTS.md` rules.
- Use `common-ground.md` and `expert-routing.md` to convert repeated AI misses into durable guardrails.
- Preserve `.sdc/constitution.md` as higher authority.
- Encode concrete must-do, must-not-do, validation commands, and known mistakes.
- Do not invent project rules without evidence or explicit user direction.
