# Gate Evidence Schema Proposal

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| discovery.md | Confirmed | DEC-GE-001 through DEC-GE-009 | Defines the confirmed scope and executable Base boundary. |
| ANDY-143 / ANDY-151 inputs | Confirmed | Scope and Layout A decisions | Define the contract semantics and non-goals. |
| `origin/main@e10a5d221f081fb6d099d342597a707b0dad91c9` | Confirmed | Exact Git object inspection | Shows the absent schema and supported validation/handoff tools. |

## 背景

The exact Base contains durable-evidence governance language but no authoritative, versioned `## Gate Evidence` Markdown contract, no Resolution/Closure UUID rule, and no per-ID provenance rule.  The prior plan additionally depended on a runtime-context script and JSONL/state schemas that are absent from the Base.  That contradiction prevents a clean execution handoff.

## 目标

Publish the smallest versioned Layout A contract and direct local fail-closed proof, then hand it off through the Base-supported validator and Markdown task/review handoffs.  Deliver the plan itself as a portable Git bundle with a recorded digest so an independent environment can read the exact revision without a remote push.  The result establishes local format and consistency only; it makes no external authority claim.

## 范围

- Add `## Gate Evidence` to `sdc-references/workflow-standards.md` after the bounded Task Format/Evidence Discipline boundary.
- Create `tests/test_gate_evidence_schema.py` as the direct local contract test with test-local fixtures.
- Keep the governed change package as nine Markdown artifacts: discovery, proposal, spec, impact, design, tasks, context pack, notes, and knowledge candidates.
- Use `sdc-cli.py validate`, `sdc-task-brief.py`, and `sdc-review-package.py` only as existing Base tools; no helper source changes are planned.
- Attach a portable Git bundle plus digest manifest as planning/review evidence; T000 verifies it locally, including equality to the fixed nine artifact paths, before import.

## 非目标

- Gate-Closed R0/R1 profile implementation.
- Runtime, package, public-command, product, or default `validate` behavior change.
- `scripts/sdc-runtime-context.py`, JSONL context manifests, lifecycle state, or a new runtime schema.
- External-control-plane lookup or authority verification.
- Remote publication of the plan revision or any new runtime transport protocol.
- Merge, deployment, publishing, release, or release approval.

## 初始验收标准

- The standard documents exactly one closed Layout A record with the five confirmed fields and local validation rules.
- The direct test accepts a compliant record and rejects a malformed ID, missing field, non-closed status, absent/duplicate/blank named source, and more than one Gate Evidence section.
- T000 can start from the clean Base, prove the exact fixed nine-path Markdown package, import and commit it as H0, pass the Base validator, and produce its ignored task/review handoff without the missing script or a JSON schema.
- The candidate diff remains limited to the standard, its direct test, and governed Markdown planning/evidence artifacts; `sdc-cli.py`, `scripts/`, profiles, and packages remain unchanged.

## Risks

- A placement inside the current Task Format section would break its bounded release-audit scan.  The design fixes placement after `## Evidence Discipline`.
- A static test could grow into a runtime validator.  The plan has no runtime implementation task and enforces a changed-path allowlist.
- Reintroducing JSON manifest/state terms would recreate the clean-base contradiction.  T000 validates the Base-supported Markdown handoff instead.
