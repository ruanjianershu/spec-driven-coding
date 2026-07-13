# Change Impact

## Analysis Snapshot

- Repository: spec-driven-coding
- Change: 2026-06-15-artifact-output-contracts
- Branch / commit: current working tree
- Evidence limits: Static source/template/eval review; no external package publish in this change.

## Entry Points And Call Chain

- User-facing workflow prompts: `commands/change.md`, `commands/plan.md`, `commands/check.md`, `commands/apply.md`, `commands/archive.md`.
- Advanced skills: `skills/sdc-spec`, `skills/sdc-validate`, `skills/sdc-review`, `skills/sdc-test`, `skills/sdc-quality`.
- Shared references: `sdc-references/*`.
- CLI managed templates and validators: `sdc-cli.py`.
- Release checks: `scripts/audit-release.mjs`, `evals/sdc-flow/*`.
- User docs and metadata: `README.md`, `CHANGELOG.md`, plugin manifests, `package.json`.

## Direct Changes Required

| File / Contract | Reason | Evidence | Related REQ/AC |
|---|---|---|---|
| `sdc-references/artifact-output-contracts.md` | Define the new stage output standard | New reference file | REQ-01 / AC-01 |
| `sdc-references/workflow-standards.md` | Add stop-line and output contract discipline | Shared governance reference | REQ-01, REQ-02 / AC-01 |
| `sdc-references/delivery-gates.md` | Add validate/check/review quality requirements | Delivery gate reference | REQ-02 / AC-02 |
| `commands/change.md`, `commands/plan.md`, `commands/check.md`, `commands/apply.md`, `commands/archive.md` | Route the output contract through public workflow stages | Public command prompts | REQ-02 / AC-02 |
| `skills/sdc-*.md` | Keep advanced detailed skills aligned | Advanced skill prompts | REQ-02 / AC-02 |
| `sdc-cli.py` | Add managed templates and validation enforcement | CLI source | REQ-02, REQ-03 / AC-02, AC-03 |
| `evals/sdc-flow/*` | Add deterministic regression coverage | Existing eval suite | REQ-04 / AC-04 |
| `scripts/audit-release.mjs` | Add release audit markers | Existing release audit | REQ-04 / AC-04 |
| `README.md`, `CHANGELOG.md`, plugin metadata | Explain product behavior | User-facing docs and marketplace metadata | REQ-01 / AC-01 |

## Cascading Impact

- Existing active changes and older `.sdc` workspaces may need safe template upgrades to gain Artifact Output Contract sections.
- Confirmed change validation becomes stricter: final design/context-pack without output contract coverage will fail.
- Prompt-only skill behavior remains compatible because no public command is added or renamed.

## Contracts / Data / Config / Permissions / Security / Observability

- Public command contract: unchanged.
- Package API/bin contract: unchanged.
- Data/schema: N/A, no persistent database.
- Security/permissions: N/A, no runtime permission change.
- Observability/deploy: N/A, no service runtime.

## Tests And Regression Strategy

- Syntax checks: Python and Node.
- Release audit: `npm run audit`.
- Deterministic flow evals: `npm run eval:sdc`.
- SDC self-validation: `python3 sdc-cli.py validate 2026-06-15-artifact-output-contracts`.

## Implementation Order And Rollback Boundary

1. Add shared reference.
2. Update prompts, skills, templates, and validators.
3. Add eval/audit coverage.
4. Update docs/metadata and project `.sdc` change record.

Rollback removes the new reference, validation function, template sections, eval scenario, and docs/metadata references.

## Open Questions

| Question | Why It Matters | Blocking? |
|---|---|---|

## Evidence Index

| Claim | Source |
|---|---|
| Public commands stay unchanged | commands/ directory, README.md |
| Output contract is internal | sdc-references/artifact-output-contracts.md |
| Validation enforces missing triggered outputs | sdc-cli.py, evals/sdc-flow/sdc_flow_provider.py |
