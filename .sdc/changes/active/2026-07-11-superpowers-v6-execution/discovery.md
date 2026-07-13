# Discovery

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| Superpowers v6.0.0-v6.1.1 release notes | Confirmed | Official GitHub releases reviewed 2026-07-11 | Defines the execution mechanisms being evaluated |
| Existing SDC 1.2.1 workflow | Confirmed | commands, shared references, CLI, evals | Shows current governance and execution gaps |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## Current Understanding

SDC already has stronger requirement, knowledge, impact, and traceability governance. The confirmed gap is post-plan execution: task interfaces, context-efficient handoffs, recoverable progress, independent task review, and final cross-task review.

## Candidate Directions

| Option | Description | Pros | Cons | Status |
|---|---|---|---|---|
| Internal orchestration contract | Strengthen plan/apply/check without new public commands | Preserves SDC simplicity and adds execution reliability | Requires schema and eval migration | Confirmed |
| Add public subagent commands | Expose separate execution/review commands | Explicit controls | Reintroduces command sprawl | Rejected |

## Tradeoffs

Runtime handoff files reduce repeated context cost but are local scratch, so durable outcomes must still be promoted into tasks, notes, reports, and archive evidence.

## Recommended MVP

Add Global Constraints, Plan Preflight, per-task interfaces, file-based brief/report/review packages, runtime ledger, dual-verdict task review, final whole-change review, and Codex marketplace packaging hardening.

## Decision Ledger

| ID | Decision | Status | Source | Impact | Next Step |
|---|---|---|---|---|---|
| DEC-01 | Keep public commands unchanged | Confirmed | User direction and SDC product principle | No command sprawl | Implement internally in plan/apply/check |
| DEC-02 | Support subagent execution with inline fallback | Confirmed | Cross-client compatibility requirement | Works in Codex, Claude Code, and simpler clients | Keep tool names vendor-neutral |
| DEC-03 | Use `.sdc/runtime/` for ignored handoffs and recovery ledger | Confirmed | Superpowers v6 file-handoff evidence plus SDC durability model | Reduces context while preserving durable records | Add helpers and gitignore rule |
| DEC-04 | Release as SDC 1.3.0 | Confirmed | Feature scope is a workflow-level enhancement | Requires metadata/schema migration | Update all version sources |
| DEC-05 | Execute implementation tasks serially through review and ledger completion | Confirmed | User request to align with Superpowers v6 execution design | Prevents cross-task state and review races | Encode in apply and execution reference |

## Open Questions

| ID | Question | Why It Matters | Options | Required Before |
|---|---|---|---|---|

## Exit Criteria

- [x] MVP scope confirmed
- [x] high-impact decisions confirmed or explicitly deferred
- [x] acceptance direction is clear
