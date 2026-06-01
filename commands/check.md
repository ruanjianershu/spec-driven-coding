---
description: Run the combined SDC validate, review, test, and quality delivery check.
---

# SDC Check

Use "$ARGUMENTS" as the target change or scope. Run the combined validation, review, test, and quality perspectives with concrete evidence.

Run the SDC check workflow:

- Validate structure, traceability, decision status, task format, evidence, and Brownfield impact gates.
- Validate knowledge source usage, `context-pack.md`, and candidate-vs-confirmed boundaries.
- Validate "No Evidence, No Fact / No Confirmation, No Execution / No Impact, No Brownfield Change".
- Review actual diffs and surrounding code for correctness, architecture, security, data integrity, compatibility, and maintainability.
- Run or assess relevant tests against acceptance criteria, boundaries, regressions, and failure modes.
- Evaluate final quality across user-facing flow, docs, security, performance, maintainability, and release readiness.
- Report whether product/technical knowledge, memory candidates, standards, or AGENTS.md need archive-time updates.
- In bug mode, analyze without modifying code unless explicitly requested.
