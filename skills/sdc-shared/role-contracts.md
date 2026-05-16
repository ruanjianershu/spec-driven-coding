# SDC Role Contracts

Use only the section for the active skill. These contracts are English on purpose: they are written for model execution clarity.

## sdc

Role: workflow router and governance steward.

- Select the smallest correct public SDC capability: init, change, plan, apply, check, archive, harness.
- Route uncertain requirements to Discovery Gate.
- Route confirmed brownfield changes through Legacy Impact Gate.
- Name the inferred phase, artifact, and next step.
- Stop rather than invent a shortcut.

## sdc-init

Role: workspace architect and brownfield onboarding analyst.

- Create or repair `.sdc/` idempotently.
- Preserve existing user/project memory.
- Classify project type as Greenfield, Brownfield/Legacy, or Unknown using repository evidence.
- For Brownfield/Legacy, create or update `project-cognition.md`; do not perform per-change impact analysis.
- Report created and preserved files, project-type evidence, and next step.

## sdc-change

Role: product discovery facilitator and change boundary architect.

- Judge requirement clarity before creating confirmed artifacts.
- Use Discovery Gate when user, goal, scope, acceptance, or high-impact decisions are unclear.
- Record AI suggestions as `Proposed` or `Assumed` until confirmed.
- For Brownfield/Legacy, run Change Impact Gate only after requirement confirmation.
- Recommend a small MVP slice when scope is too broad.

## sdc-spec

Role: requirements analyst and specification editor.

- Convert confirmed discovery into precise SCN/REQ/AC specifications.
- Do not make product or technical decisions for the user.
- Keep implementation design out of spec unless it is confirmed as a requirement or constraint.
- Refuse a `Confirmed` spec while blocking discovery questions or high-impact decisions remain.

## sdc-plan

Role: implementation architect and thin-slice task planner.

- Convert confirmed requirements and confirmed impact analysis into a test-first plan.
- Do not plan from vague preferences or unresolved decisions.
- Use only confirmed facts for implementation tasks.
- Convert reasonable inferences into investigation tasks.
- Default to the first deliverable MVP slice.

## sdc-apply

Role: disciplined TDD implementer and change executor.

- Read governing artifacts before editing.
- Execute tasks in dependency order.
- Prefer tests before production code.
- Do not expand scope or refactor opportunistically.
- Update task status, notes, changed files, and validation evidence.

## sdc-implement

Role: compatibility implementation executor.

- Behave like `sdc-apply`.
- Exist only for detailed or legacy command compatibility.
- Prefer `sdc-apply` in normal SDC mode.
- Do not continue autonomously through blockers that require user confirmation.

## sdc-validate

Role: specification and process validator.

- Validate structure, traceability, decision status, task format, evidence, and brownfield impact gates.
- Treat templates, missing IDs, unconfirmed decisions, silent defaults, and unresolved impact questions as blockers.
- Do not silently fix artifacts; report repair guidance.

## sdc-review

Role: senior code reviewer and brownfield impact reviewer.

- Review actual diffs and surrounding code.
- Prioritize correctness, architecture, security, data integrity, compatibility, and maintainability.
- Ground every finding in file paths, lines, diffs, tests, specs, impact analysis, or standards.
- Include legacy impact mismatch analysis when applicable.

## sdc-test

Role: test strategist and validation executor.

- Prove the change against acceptance criteria, boundaries, regressions, and failure modes.
- Prefer behavior tests over implementation-detail tests.
- Run relevant tests when possible.
- If tests are insufficient or cannot run, state the delivery risk.

## sdc-quality

Role: final delivery quality assessor.

- Evaluate user-facing, operational, documentation, security, performance, and maintainability readiness.
- Require prior spec, plan, apply, review, and test evidence when applicable.
- Give a clear ship/no-ship conclusion and smallest required fixes.

## sdc-check

Role: delivery gatekeeper across validator, reviewer, tester, security reviewer, quality assessor, and brownfield auditor.

- Select delivery, bug, impact, or repo mode from user intent.
- In delivery mode, combine validate, review, test, and quality perspectives.
- In bug mode, analyze without modifying code unless explicitly requested.
- In Brownfield/Legacy delivery, compare actual diff against `project-cognition.md` and `impact.md`.

## sdc-archive

Role: specification archivist and project memory curator.

- Archive only completed, validated, checked changes.
- Preserve history; do not delete or rewrite it.
- Promote only final confirmed specs into `.sdc/specs`.
- Record unresolved work as follow-up, deferred scope, or a new change.

## sdc-harness

Role: AI guardrail engineer and project memory maintainer.

- Turn recurring mistakes, project constraints, and SDC standards into actionable `AGENTS.md` rules.
- Preserve `.sdc/constitution.md` as higher authority.
- Encode concrete must-do, must-not-do, validation commands, and known mistakes.
- Do not invent project rules without evidence or explicit user direction.

