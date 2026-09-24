# Domain Knowledge

Load this reference when domain terms, scope definitions, or competing meanings affect a requirement, interface, or acceptance criterion. Do not create a glossary exercise for an unambiguous local edit. [Workflow standards](workflow-standards.md) own authorization, source freshness, decision states, and promotion; [discovery](discovery-gate.md) owns unresolved requirements and its artifact budget.

## Reuse The Existing Domain Record

Use `.sdc/knowledge/product/domain.md`, reached through the knowledge index, rather than creating a parallel vocabulary file. Its existing template fields are sufficient:

| Existing Field | Use When Relevant |
| --- | --- |
| Concept | The confirmed canonical term within this scope. |
| Meaning | A precise definition, concrete example or counterexample, and ambiguous synonyms to avoid only where they cause confusion. |
| Related Rules | Links or IDs for the rules that constrain the concept; do not duplicate their policy text. |
| Status | Preserve the recorded knowledge status; a proposed interpretation is not confirmed by formatting it as a glossary row. |
| Source | The authoritative statement and any supporting evidence. |
| Verified At | When the cited evidence was actually checked. |
| Verified Against | The checked revision or identifiable confirmation. |
| Scope | The actor, workflow, context, or boundary where this meaning applies. |

Do not add mandatory columns, a global banned-word list, or a second source of truth. Record a banned ambiguous synonym only when it could change interpretation, and state its scope. Do not rename code or public interfaces merely to match preferred prose; that requires its own impact and authorization checks.

For example, after owner confirmation, `Workspace owner` can mean the account that controls workspace membership. `Document owner` can mean the document's named custodian without membership rights. Bare `owner` is ambiguous in a membership acceptance criterion, but need not be banned from an unrelated file-ownership discussion. An example such as "a document owner cannot invite workspace members solely through document ownership" makes the boundary testable; it is not a default permission policy to adopt without confirmation.

## Resolve Conflicts Without Promotion

When a request, domain entry, or implementation uses incompatible meanings, cite both sources and their scopes. Preserve the conflict in the current Decision Ledger or authorized discovery notes, mark the suggested resolution `Proposed`, and identify the business/domain owner who can resolve it. Ask for owner resolution of the blocking meaning; code investigation can establish current behavior but cannot choose business intent. Unrelated terminology disagreements do not expand the change.

Do not silently rewrite durable domain knowledge, rules, Common Ground, or memory to remove the conflict. Route a confirmed resolution through the existing candidate and [archive promotion](delivery-gates.md#archive-gate) process with explicit approval of content and destination. While discovery is open, use only its permitted artifacts. Dependent execution stays blocked until the governing meaning is resolved.

## Selective Decision Records

Use the existing Decision Ledger for current-change decisions. Propose an ADR in `.sdc/decisions/` when a confirmed decision materially constrains future choices, crosses durable system boundaries, or would be expensive to reverse and its alternatives or rationale matter later. A local, easily reversible implementation choice normally needs only the change's design or notes. Do not require an ADR for every term, question, or task; this threshold changes documentation depth, never confirmation requirements.

## Optional Throwaway Prototype

A prototype is optional when a bounded experiment can resolve a concrete uncertainty. Before creating it, cite explicit authorization covering the question, isolated scratch location, allowed side effects, effort limit, and disposal or retention boundary; ask only for missing authorization. Use runtime research scratch, not production paths, and stop when the question is answered or the limit is reached.

Record the observed result as evidence, including what it cannot establish. The experiment does not confirm business policy, select a production architecture, close discovery by itself, or add production scope. Do not promote its code into delivery merely because it works; production work still needs confirmed scope and the normal plan, tests, and review.
