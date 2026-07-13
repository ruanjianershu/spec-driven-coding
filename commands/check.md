---
description: Run the combined SDC validate, review, test, and quality delivery check.
---

# SDC Check

Use "$ARGUMENTS" as the target change or scope. Run the combined validation, review, test, and quality perspectives with concrete evidence.

Run the SDC check workflow:

- Validate structure, traceability, decision status, task format, evidence, and Brownfield impact gates.
- Validate Common Ground usage and block final execution if OPEN or high-impact WORKING items were treated as facts.
- Validate Expert Profiles Used against actual diff and risk areas.
- Validate knowledge source usage, `context-pack.md`, and candidate-vs-confirmed boundaries.
- Validate the Artifact Output Contract: triggered diagrams, API/data contracts, UX flow, test matrix, deploy/release checklist, and AI involvement note must exist or be explicitly `N/A` with evidence.
- Validate the Execution Orchestration Contract: Plan Preflight passed, task interfaces are complete, checked tasks have approved dual-verdict reviews and evidence, and any present progress ledger agrees with durable task/notes evidence. A missing git-ignored ledger warns but does not override durable evidence.
- Validate "No Evidence, No Fact / No Confirmation, No Execution / No Impact, No Brownfield Change".
- Review actual diffs and surrounding code for correctness, architecture, security, data integrity, compatibility, and maintainability.
- Treat review as read-only. Report `Cannot verify from diff` separately and resolve it with focused evidence; never silently convert it to approval.
- Require one final whole-change review after all task-level reviews, covering cross-task integration and unresolved Minor/`Cannot verify` items.
- Run or assess relevant tests against acceptance criteria, boundaries, regressions, and failure modes.
- Evaluate final quality across user-facing flow, docs, security, performance, maintainability, and release readiness.
- Report whether Common Ground, expert routing, product/technical knowledge, memory candidates, standards, or AGENTS.md need archive-time updates.
- In bug mode, analyze without modifying code unless explicitly requested.
