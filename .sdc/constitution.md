# SDC Project Constitution

## 1. Governance Priority

`.sdc/constitution.md > AGENTS.md > conversation instructions`

If these sources conflict, stop and produce a Stop-Line Report.

## 2. Fact Priority

`discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code`

Code is evidence of current behavior, but it does not automatically override the agreed spec.

## 3. Core Chain

`discovery -> spec -> impact -> plan -> tasks -> code -> verify -> archive`

## 4. Stop-The-Line Rules

Stop and produce a Stop-Line Report when:

- spec, design, or tasks are missing, conflicting, or not verifiable
- implementation requires changing business behavior, public contract, acceptance criteria, or key technical decisions
- current task requires scope expansion
- validation cannot prove the acceptance criteria

## 5. Traceability Rules

- specs must define `SCN-*`, `REQ-*`, and `AC-*` identifiers
- tasks must reference `REQ-*` and `AC-*`
- tests or validation notes must reference `AC-*`
- implementation notes must record validation evidence

## 6. Human Confirmation Rules

AI may propose options, but humans own high-impact decisions.

High-impact decisions include product rules, permissions, state machines, approval flows, reminder behavior, technology stack, architecture, data model, authentication, locking, deletion, migration, rollout, and security policy.

Before a high-impact decision enters `REQ-*`, `AC-*`, `INV-*`, `design.md`, or `tasks.md`, it must be one of:

- explicitly confirmed by the user
- supported by an authoritative project document
- explicitly delegated by the user with permission to choose

## 7. No Silent Defaults

Do not turn common practice into project truth.

All AI-created defaults must be recorded in a Decision Ledger as `Proposed` or `Assumed` until confirmed. `Proposed`, `Assumed`, `TBD`, and `Conflict` items must not be treated as implementation-ready.

## 8. Discovery Gate

When requirements are uncertain, start with discovery instead of a confirmed spec.

Discovery must record current understanding, candidate directions, tradeoffs, recommended MVP, open questions, and a Decision Ledger. A confirmed spec can only be produced after the current MVP scope and high-impact decisions are confirmed or explicitly deferred.
