---
name: sdc-archive
description: "Use when a completed SDC change is ready for archival and durable knowledge compaction."
---

> Codex/Hermes workflow skill generated from `commands/archive.md`.
> Treat the user's current request as `$ARGUMENTS`. In Codex/Hermes, route to the matching SDC skill/workflow instead of expecting `/sdc:*` slash-command support.

# SDC Archive

Use "$ARGUMENTS" as the change id. Archive only after required checks pass with current evidence; a narrative assertion is not equivalent to a required execution receipt.

During archive, run the Knowledge Compact Gate. Required spec/archive writes may proceed; optional updates to common-ground.md, expert-routing.md, decisions, standards, reports, AGENTS.md, project.md, or project-cognition.md require explicit user confirmation before writing.
This also applies to optional product knowledge, technical knowledge, and memory updates.

Run the SDC archive workflow:

- Require a final confirmed spec, completed tasks, traceability, approved final whole-change review, and check evidence tied to the delivered source snapshot. Do not repeat unchanged checks or bypass stale/missing evidence.
- Resolve exactly one active change and require lifecycle state `archivable`; do not archive from `checking` merely because the latest report looks successful.
- Promote the final spec to `.sdc/specs/<change-id>.md`.
- Create or update `archive.md` with conclusion, evidence, residual risks, coverage summary, and Knowledge Compact Gate.
- Preserve Artifact Output Contract coverage in archive evidence, including required diagrams/contracts/matrices/checklists and any N/A reasons.
- Evaluate `knowledge-candidates.md` and affected knowledge/Common Ground/routing sources only. Propose incremental updates with target, source, freshness check, and reason; mark unaffected assets `N/A` without rereading or rewriting the entire knowledge base.
- Recommend promotion to the relevant project knowledge, memory, decisions, standards, or guardrails only with explicit human confirmation of the proposed content and destination. Personal/native memory remains Candidate and cannot silently authorize project truth or cross-device writes.
- Evaluate research-derived Candidate entries; do not promote scratch, citations, or durable findings without explicit human confirmation.
- Move the completed change into `.sdc/changes/archive/<change-id>/`.
- Preserve `state.json`, `apply-context.jsonl`, and `check-context.jsonl` with the archived change as delivery provenance.
- Never delete change history or silently overwrite an existing stable spec.
