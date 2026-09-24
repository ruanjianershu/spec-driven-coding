# Proportionate Workflow Upgrade

## Authorized Scope

The user approved the preceding comparison and requested implementation on
2026-09-24. Preserve existing public commands, confirmation boundaries, private
distribution separation, and existing standard changes. The original approval
excluded release, push, local plugin replacement, new stack, and enterprise data
import. After the full verification exposed six further defects, the user
explicitly authorized their repair and a GitHub push on the same date. That
follow-up does not authorize a GitLab push, npm publication, main-branch merge,
or local plugin replacement.

## Design

1. Add a deliberately narrow compact format for new, confirmed, behavior-neutral
   documentation edits. One structured `compact.json` owns intake, authorization,
   risk exclusions, affected paths, acceptance, task verification, and review.
   It may start without full workspace initialization; existing governance still
   binds it. Standard changes keep their existing schema. Unknown scope, risk,
   non-document edits, or wider changes block compact execution. Escalation
   preserves history and requires standard discovery, never silent downgrade.
2. Reuse the current lifecycle, manifests, command receipts, snapshot freshness,
   reviewer attribution, and archive boundaries. A compact record is not a bypass
   and generated state/manifests never authorize their own inputs. Only mutable
   completion/review fields are excluded from execution-contract hashes.
3. Add read-only installation diagnostics behind existing init/check routing,
   including source fingerprints, missing runtime files, duplicate registrations,
   and an actionable machine-readable nonzero failure. Do not repair user config
   or assume equal package versions mean equal installed content.
4. Improve dependency-aware discovery, contextual vocabulary, vertical tasks,
   and falsifiable tests through targeted English references. Keep SKILL.md thin,
   reuse existing domain knowledge and confirmation/promotion gates, and do not
   require exhaustive questioning, an expert swarm, or extra public commands.
5. Track stable review finding IDs and bounded repeated failures without treating
   risk acceptance as approval. Preserve findings across retries and revisions;
   caller attribution is not authenticated identity.

## Acceptance

- A confirmed README correction can run through change, plan, apply, check, and
  archive without full init or a spec/design/tasks document package.
- Open questions, missing authority, unsafe paths, changed scope, stale inputs,
  stale/failed receipts, missing review, and unfinished findings fail closed.
- Existing standard lifecycle and all distribution adapters remain compatible.
- Installer diagnostics detect stale same-version payloads and duplicates using
  isolated fake homes; diagnostics never mutate installations.
- Discovery asks only reachable blocking decisions; code facts do not authorize
  business policy. Test assessment distinguishes a command passing from a test
  capable of detecting the original problem.
- Verify source and installed packages, focused regressions, existing full tests,
  workflow scenarios, and independent review. Report measured evidence and limits,
  not unmeasured token savings or universal client compatibility.

## Implementation Checklist

- [x] T001 Compact contract and failing CLI lifecycle tests.
- [x] T002 Integrate compact lifecycle, receipts, revision, and archive.
- [x] T003 Read-only installation diagnostics and isolated installation tests.
- [x] T004 Focused discovery/domain/testing guidance and behavioral probes.
- [x] T005 Finding identity and bounded repair evidence.
- [x] T006 Synchronize generated skills, packaging, README, and changelog.
- [x] T007 Full regression, installation simulation, independent review.

## Verification Commands

Run focused `python3 -m unittest` modules before and after each implementation.
Then run `npm test`, `npm run eval:sdc`, `python3 -m unittest discover -s tests -v`,
`npm run audit`, `git diff --check`, and portable/native plugin packaging. Use
temporary project and home directories for all behavioral/installation probes.

## Review Checkpoint

Independent review reproduced ignored-target freshness, transitive governing
source freshness, and escalation-note preservation defects. A second review
identified directory-filter variants, automatic governance roots, Windows text
translation of baseline bytes, and standalone receipt baseline integrity. Each
has a failing regression observed before its fix. The final focused review found
no remaining actionable compact issues: 23 compact regressions passed, missing
optional-root citations were rejected across eight hash seeds, and an initialized
workspace also completed its compact lifecycle and archive.

The source-baseline map is machine evidence outside the canonical context record,
and compact stdout returns a digest instead of dumping repository-sized maps.
Installation diagnosis follows Claude's documented marketplace-root skill
selection exception, with genuine additive-discovery duplicate regressions.
Native subagent observations and their limitations are in
`evals/sdc-agent/SMOKE.md`; these are not an installed-client A/B benchmark.

## Earlier Verification (Superseded)

These measurements describe the earlier implementation checkpoint, not the
post-repair delivery gate. A subsequent wider verification found the defects
below despite this green suite.

- `npm test`: 225 tests passed, including lifecycle, evidence, findings,
  installation diagnostics, client adapters, and guidance contracts.
- `npm run eval:sdc`: all 74 deterministic workflow scenarios passed.
- `python3 -m unittest discover -s tests -v`: 4 installed-command tests passed.
- `npm run audit`, `git diff --check`, Node syntax checks, and Claude's plugin
  manifest validator passed.
- Portable and opt-in native-hook Codex ZIPs built successfully. The three new
  runtime helpers were compared byte-for-byte against the source payload.
- `npm pack --dry-run --json` succeeded with 79 entries and all new helpers.
  No npm publication, user-home installation, commit, or push was performed.

Limits: semantic approval/reviewer identity remain cooperative assertions, not
authenticated attestations. Windows newline handling was simulated. Installation
tests do not prove a running client's command palette, and native subagent probes
do not establish token savings or general model reliability.

## Follow-Up Repair And Reconciliation

The fuller verification identified six reproducible issues. Each repair adds a
regression that was observed failing before the implementation fix:

| ID | Defect | Repair boundary |
|---|---|---|
| F-001 | Frozen agent sources omitted imported runtime modules. | Explicit helper allowlist, double snapshot execution, and retained bounds. |
| F-002 | Equal file fingerprints hid incomplete Claude skill selection. | Compare the effective discovered entrypoints to the intended profile. |
| F-003 | Findings examples assumed the plugin was the product working directory. | Resolve the installed helper root while keeping the product cwd. |
| F-004 | Cache-like directory names hid tracked code and non-Git directory links. | Snapshot tracked product files and link entries without following external content. |
| F-005 | An absent findings field invalidated unchanged pre-ledger approvals. | Omit absent ledgers; hash real ledgers and invalidate on appearance/removal. |
| F-006 | A long dated reviewer label was treated as an opaque secret. | Narrow descriptive-label handling while retaining credential/token rejection. |

Independent review then found four further boundary cases in the same repair
surfaces, rather than treating the green suite as sufficient:

| ID | Defect | Required regression |
|---|---|---|
| F-007 | A cached default source with missing public commands could diagnose itself healthy. | Require public command entrypoints in both source and installed profiles. |
| F-008 | Non-string hook declarations bypassed path/helper checks. | Reject unsupported manifest forms explicitly. |
| F-009 | Quoted top-level TOML registration keys were silently skipped. | Classify quoted keys before rejecting unsupported registration shapes. |
| F-010 | A tracked child's symlinked ancestor used a constant snapshot marker. | Bind the first ancestor link's destination without traversing its target. |
| F-011 | Real planning treated the bundled optional company-index routing condition as mandatory. | Recognize the exact bundled condition, bind absence, and preserve explicit required-citation precedence. |

The initial upgrade did not have the formal standard change artifacts required
by its own workflow. The active change
`.sdc/changes/active/2026-09-24-compact-workflow-upgrade/` reconciles that omission
prospectively for repair verification and delivery. It must not claim that new
state transitions, approvals, or receipts existed before they were recorded.
Current post-repair results, independent review, and limitations are recorded in
that change's `notes.md` and measured evidence; the earlier totals above are not
reused as delivery evidence.
