---
name: sdc-apply
description: "Use when an approved SDC plan is ready for implementation and evidence capture."
---

> Codex/Hermes workflow skill generated from `commands/apply.md`.
> Treat the user's current request as `$ARGUMENTS`. In Codex/Hermes, route to the matching SDC skill/workflow instead of expecting `/sdc:*` slash-command support.

# SDC Apply

Resolve `SDC_PLUGIN_ROOT` from this installed command/skill: the parent of `commands/`, or two levels above `skills/<skill>/`. Do not assume this variable is already set. Verify the helper exists and keep the target project as the working directory when invoking it. For legacy direct skills and Hermes layouts, if the derived root lacks `sdc-cli.py`, use its `sdc-runtime/` child after verifying both the CLI and runtime helper exist there. Missing helpers are an installation blocker, not permission to guess another checkout.

Use "$ARGUMENTS" to identify the target change or task. Implement the planned work, keep notes/tasks updated, and preserve verification evidence.

Run the SDC apply workflow:

For `compact.json`, follow `../../sdc-references/compact-workflow.md` instead of generating the standard documents/briefs below; preserve the same permission, freshness, execution-receipt, and independent-review gates. For behavior or bugfix tests load `../../sdc-references/test-quality.md`. Track recurring review findings using `../../sdc-references/review-findings.md`, not a fresh ID on every retry.

When `findings.json` exists, inspect it before another repair attempt. `adjudication-required` or `accepted-risk` stops automatic implementation until a cited human retry decision; replan/reopen must not erase that history.

- Load binding governance, the active `context-pack.md`, current task and relevant spec/design/notes sections, plus sources selected by the verified apply manifest. Follow knowledge/routing indexes only for affected areas; do not reread unrelated files or the whole repository.
- Follow the recorded internal risk level and authorization. Consult `../../sdc-references/workflow-standards.md` if either needs reassessment; disclose new triggers and stop affected work for unconfirmed high-impact decisions. A bounded authorized reversible action needs no redundant confirmation.
- Stop if final artifacts contain open Knowledge Gaps or `Assumed` / `Proposed` / `TBD` / `Conflict` / `Stale` execution inputs.
- Stop if final artifacts depend on OPEN or high-impact WORKING Common Ground.
- Follow the Expert Profiles Used in `context-pack.md`; if implementation discovers a new high-risk profile, stop and update plan/context-pack first.
- Follow the Artifact Output Contract in `context-pack.md`; if implementation discovers new API, data, workflow, UX, deployment, test, or AI involvement output requirements, stop and update plan/context-pack first.
- Read `../../sdc-references/execution-orchestration.md` when available and stop unless Plan Preflight is `Passed`.
- Before the first production edit, verify exact manifest schema/sources/hashes with `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" manifest verify --change <change-id> --role apply`, then advance `planned -> applying` with `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" state set --change <change-id> --state applying --source apply-stage --evidence tasks.md --evidence context-pack.md`. A mismatch requires affected-source refresh or explicit reasoned reopen, not stale approval reuse. See `../../sdc-references/runtime-context.md` for mechanics.
- Resume from `.sdc/runtime/<change-id>/progress.md` when it exists; reconcile it with tasks and git evidence instead of re-running completed tasks after context loss.
- When supported opt-in native session hooks are unavailable or fail, recover compact context with `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" session-context --client codex --change <change-id>`.
- Run task validation with `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" evidence run --change <change-id> --stage apply --task T001 --timeout 300 -- <exact Verify argv>`. Repeat `--task` only when those tasks share the exact Verify argv. Shell pipelines require explicit `sh -c` in both Verify and the run. Delivery requires the latest fresh passed receipt per completed task, exactly matching its Verify argv; `evidence append` is never proof.
- Use Candidate recall only for context recovery. Keep research scratch under `.sdc/runtime/<change-id>/research/`, cite verified findings in `notes.md`, and record promotable findings in `knowledge-candidates.md` without automatic promotion.
- Execute coherent tasks serially in dependency order. Use a separate read-only reviewer when supported and authorized; otherwise record an explicit independent review pass and its isolation limitation. Do not require a fresh implementer for every tiny edit or create a multi-agent swarm.
- Hand large task text, implementer reports, and diffs through files under `.sdc/runtime/<change-id>/`; do not repeatedly paste full plans, history, or diffs into agent prompts.
- Write or update tests before production code when meaningful.
- Do not expand scope or refactor opportunistically.
- Give every completed task read-only Spec Compliance and Code Quality verdicts backed by current evidence. Resolve Critical/Important findings and every acceptance-affecting `Cannot verify` item. For a single-task light change, one final-snapshot review may record both task and whole-change coverage; do not repeat an unchanged review or test without a named risk.
- Reviewers must not mutate repository state and must not be coached to ignore, suppress, or pre-rate findings.
- Update task status, review status, evidence, notes, changed files, and validation evidence.
- After all implementation is complete, require a final whole-change review over the complete change range and record its approved verdict before check/archive. Reuse its evidence in check only while the reviewed inputs remain unchanged.
- Write last-task progress and final approved review notes, then refresh role manifests at a safe checkpoint with `manifest generate` and verify them again; this does not bless changed requirements.
- Then run `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" evidence review --change <change-id> --reviewer "<attribution>"`. This binds already-approved independent review notes/tasks and source snapshots; attribution is not authenticated reviewer identity and the command does not perform review. Later code changes invalidate the receipt. Run `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" evidence verify --change <change-id>` to check execution and review receipts before delivery. Reopen invalidates old receipts via a new revision nonce.
- After all tasks and the approved whole-change review are durably recorded, advance `applying -> checking` with `python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" state set --change <change-id> --state checking --source apply-stage --evidence tasks.md --evidence notes.md`.
- Record durable discoveries in `knowledge-candidates.md`; do not silently edit long-lived knowledge while applying code.
- Stop with a clear report if requirements, impact, design, tasks, or code conflict.
