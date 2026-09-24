# Compact Documentation Workflow

Load this reference only for a new, confirmed, behavior-neutral prose change or
an existing change containing `compact.json`. It is an alternative artifact
format, not a weaker acceptance level. `sdc_compact.py` defines its executable
contract; the standard Markdown templates are not compact templates.

## Eligibility And Authority

- All `light` criteria in `workflow-standards.md` must hold. This first compact
  format supports non-executable `.md`, `.txt`, and `.rst` prose only, not source
  code, skills, commands, governance, security policy, interfaces, or deployment.
- A prose extension does not establish behavior neutrality. Inspect the actual
  content and relevant references; editing a business rule in a README changes
  behavior/contract even if no code changes. Use standard/strict instead.
- Cite confirmed scope, acceptance, four-category coverage, authority, known
  impact, applicable governance, and why richer outputs are not triggered.
  No fixed interview count. Open questions remain in chat/minimal discovery.
- Existing project rules still bind. If they demand full artifacts, use standard.
  Do not rewrite a constitution to enable compact or silently downgrade an
  existing standard change. Do not generate a constitution just to fix a typo.
- Compact can start without full `init`. Explicit `init` still creates the normal
  workspace. Existing governance is read and fingerprinted, never skipped.

## Canonical Record

The agent builds this record from confirmed evidence, not from invented defaults.
Use stdin (`--record -`) or a temporary file outside the project to avoid adding
the intake transport to the implementation snapshot. The creator captures the
source baseline, change ID, pending review, and incomplete task itself.

```json
{
  "schema": "sdc.compact/v1",
  "intake": {
    "request": "Correct the stated spelling error in README.md",
    "context": "Existing project documentation; current maintainer request",
    "scope": "Only the confirmed spelling correction; no instruction changes",
    "preferences": "Preserve Markdown; language and database are unaffected",
    "acceptance": "Confirmed spelling is present; original typo is absent",
    "authorization": "Cite the user's correction-and-verification request; no publish",
    "open_questions": [],
    "decisions": []
  },
  "risk": {
    "level": "light",
    "rationale": "Cite inspected content and why only spelling changes",
    "exclusions": {
      "behavior": false, "data": false, "security": false,
      "public_contract": false, "architecture": false, "deployment": false
    }
  },
  "paths": ["README.md"],
  "impact": "Cite the affected text and evidence of no runtime/caller impact",
  "governance": [],
  "governance_review": "Cite applicable rules or establish their absence",
  "output_assessment": "Explain why diagrams, API/data/UX/release contracts are not triggered",
  "task": {
    "id": "T001", "scenario": "SCN-001", "requirement": "REQ-001", "acceptance": "AC-001",
    "verify": ["python3", "-c", "from pathlib import Path; s=Path('README.md').read_text(); assert 'the overview' in s and 'teh overview' not in s"],
    "expected": "Independent spelling assertion passes and diff is in scope"
  }
}
```

This is an illustrative spelling test, not a universal validation command. Use
the actual confirmed expected text. Record decisions only if needed, with
`decision`, `status`, and `source`; `Deferred` also needs `outside_scope` evidence.
List applicable extra standards/knowledge paths in `governance`. Root AGENTS.md,
CLAUDE.md, constitution, Common Ground, expert routing, and knowledge index are
automatically bound when present. A digest is freshness evidence, not proof the
agent has read or understood a source.

## Existing Commands, Compact Artifacts

`change`: after intake is closed and writes are authorized:

```sh
python3 "$SDC_PLUGIN_ROOT/sdc-cli.py" change <name> --compact --record <temporary-record.json>
```

This creates `compact.json` and `state.json` as the top-level change artifacts,
plus the generated source baseline below. It adds `/runtime/` to
`.sdc/.gitignore` without replacing existing entries. Validate
the contract, then advance `discovery -> confirmed` using the existing runtime
helper with `--source spec-stage --evidence compact.json`.

The source-baseline map lives in generated `evidence/baseline/source.json`, bound
by a digest in compact.json. Do not load this repository-sized machine map into
agent context. Compact state/receipt stdout reports the snapshot digest; full
snapshots remain in durable machine evidence for verification.

`plan`: check the affected paths, single coherent task, independent expected
result, and existing governance. Edit the task only before planning; generate and
verify both role manifests. Advance to `planned` with source `plan-stage`, then
`apply` advances to `applying` with source `apply-stage`. Both use only
`--evidence compact.json`. Do not manufacture spec/design/tasks/context-pack or
separate task briefs for this format.

`apply`: stay within declared paths; use the same exact Verify argv through
`evidence run --task T001`. When complete set `task.complete` to true. Inspect
the final diff independently and record `review.spec` and `review.quality` as
`approved` only with findings closed, plus `reviewer`, concrete `evidence`, and
`behavior_neutral: true`. This single pass covers task and whole-change review.
Reviewer attribution is caller-declared, not identity authentication.

`check`: validate the contract and real diff, test quality, fresh execution and
review receipts, and any finding ledger. Bind the recorded reviewer via
`evidence review --reviewer <same-attribution>`. Refresh both manifests after
completion/review edits, verify them and `evidence verify`, then advance to
`checking` (source `apply-stage`) and `archivable` (source `check-stage`), both
with `--evidence compact.json`. Failed, absent, or stale evidence cannot pass.

`archive`: use the existing CLI archive. It preserves compact requirements,
state, manifests, receipts, and archive summary under changes/archive. It does
not create a new business spec or promote knowledge/memory for a spelling fix.
Unexpected reusable facts require a separate, explicitly confirmed promotion.

## Revisions And Escalation

Contract edits invalidate approvals; completion/review updates do not rewrite
the task contract. Changed code invalidates execution/review receipts. Compact
also compares the source tree against its captured baseline: edits outside
declared paths stop execution, including unrelated concurrent changes. Report
those changes and preserve them; never revert someone else's work.

Use existing `state reopen --state confirmed --reason ...` for a planning-only
revision with unchanged requirements, or `--state discovery` for changed scope.
It preserves the old compact record and receipts, resets reviews, and requires
new confirmation when discovery reopens.

If the task needs behavior, data, policy, or wider scope, stop and explain the
evidence. Once the revised discovery action is authorized:

```sh
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" state reopen \
  --change <id> --state discovery --to-standard --reason "<evidence and authority>"
```

This archives the compact record under revisions and creates only standard
discovery/proposal/notes drafts. Run normal init if the broader workflow lacks a
workspace, then close discovery before generating spec/design/tasks. Never
rename or delete compact.json to evade a gate. Old standard changes are never
converted to compact automatically.

## Limits

The runtime checks declared facts and file/snapshot/evidence integrity; it cannot
authenticate a user's approval or prove semantic neutrality from a filename.
Independent diff review remains necessary. Lower artifact counts are measurable;
token savings and improved agent completion need separate actual-client trials.
