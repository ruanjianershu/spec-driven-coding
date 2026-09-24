# SDC Runtime Context Contract

For a change with `compact.json`, first read `compact-workflow.md`. The same lifecycle, manifests, receipts, and freshness checks apply, but each state cites `compact.json` rather than the standard Markdown artifact set. Never invent missing standard documents for a compact change.

Resolve `SDC_PLUGIN_ROOT` to the installed plugin root (the parent of `sdc-references/`); do not assume this variable is already set. Verify the helper exists and invoke it from the target project root, not the plugin directory. For legacy direct skills and Hermes layouts, if the derived root lacks `sdc-cli.py`, use its `sdc-runtime/` child after verifying both the CLI and runtime helper exist there. Missing helpers are an installation blocker, not permission to guess another checkout.

This reference defines the internal local runtime helper used by existing SDC stages. It does not add public slash commands.

## Helper

Run from the project root:

```text
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py"
```

The helper uses the Python standard library. Metadata operations write tracked change artifacts or ignored runtime files. `evidence run` executes an explicitly authorized validation command with the host's permissions; it is not a sandbox or an authorization grant.

## Lifecycle State

State schema:

```json
{"schema":"sdc.change-state/v1","change_id":"2026-08-25-example","state":"planned","updated_at":"RFC3339 UTC","source":{"kind":"stage-evidence","paths":["spec.md","design.md","tasks.md","context-pack.md"]}}
```

Legal states are fixed:

```text
intake -> discovery -> confirmed -> planned -> applying -> checking -> archivable
```

Commands:

```text
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" state get --change <change-id>
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" state set --change <change-id> --state <next-state> --source <kind> --evidence <path>
```

Invalid or skipped `state set` transitions exit non-zero and leave `state.json` unchanged. Repeating a valid, fresh state is idempotent. File presence never derives an approved state.

Each persisted transition is evidence-gated:

| Target state | Required source | Required active-change evidence |
|---|---|---|
| `discovery` | `change-stage` | `discovery.md` |
| `confirmed` | `spec-stage` | `spec.md` |
| `planned` | `plan-stage` | `design.md`, `tasks.md`, `context-pack.md`, plus generated apply/check manifests |
| `applying` | `apply-stage` | `tasks.md`, `context-pack.md` |
| `checking` | `apply-stage` | `tasks.md`, `notes.md` |
| `archivable` | `check-stage` | `tasks.md`, `notes.md` |

Evidence must be a real top-level file of the selected active change. Missing files, wrong-stage provenance, absolute paths, path traversal, symbolic links, malformed state payloads, or timezone-free timestamps fail before mutation. Archive additionally requires a valid persisted `archivable` state.

`confirmed` checks a closed discovery, explicit Confirmed spec, and acceptance/traceability structure. `planned` and `applying` also check design, task interfaces, preflight, context, and current manifests. Delivery checks require actual task execution and independent-review receipts, not only Markdown claims.

State records bind a snapshot of governing inputs. Planning additionally binds design, context, and task contracts; ordinary task checkbox/review/evidence updates are excluded from the task-contract hash. Checking and archival additionally bind repository sources, including dirty and untracked non-ignored files. File source digests include permission modes as well as bytes; compare snapshots through the helper, not against a plain file SHA-256. Explicitly cited knowledge/standards files are included, not an indiscriminate copy of every knowledge document. An invalid or changed snapshot blocks continuation.

Tracked product files remain bound even beneath cache-like directory names.
Root `.sdc` and `.git` bookkeeping remains separate. Without Git, known generated
directories are excluded, but directory symlink entries are recorded without
following them. Link destinations are bound as paths, not as external content;
external dependencies still require their own verification boundary.
When the Git index still lists a child below a replaced directory, the snapshot
binds the first symbolic-link ancestor and its destination, including dangling
destinations, without following that ancestor to inspect the child.

Git submodules/gitlinks are not recursively snapshotted by this implementation. Source-bound verification stops with an unsupported-submodule error instead of silently omitting their contents. Use a separately reviewed verification boundary; do not claim whole-project delivery evidence while tracked gitlinks remain unsupported.

### Revisions and Recovery

Use existing change/plan entrypoints to route these internal operations:

```text
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" state reopen --change <id> --state confirmed --reason "Implementation approach needs revision"
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" state reopen --change <id> --state discovery --reason "Scope requires renewed confirmation"
```

Replanning to `confirmed` is allowed only when previously snapshotted requirements remain unchanged. Scope or governing-input changes require discovery and renewed confirmation. Reopening archives downstream artifacts under `revisions/<revision-id>/`, retains state history, and creates a new revision identity. Old execution/review receipts cannot authorize the new revision. No downstream artifacts are silently reapproved. Requirements and impact are also archived when reopening discovery.

If interrupted, inspect `state.json` and the revision archive before proceeding. The lowered state is persisted before obsolete downstream files are removed, so an interrupted cleanup does not retain delivery authorization. Never restore old approvals merely to unblock execution. Legacy confirmed-or-later states without snapshots must reopen discovery and revalidate; missing state defaults only to intake/discovery.

## Active Change Resolution

Resolution precedence is:

1. explicit `--change`
2. `SDC_ACTIVE_CHANGE`
3. valid `.sdc/runtime/sessions/<session-id>/active-change.json`
4. the only directory under `.sdc/changes/active/`

Zero active changes, multiple active changes, invalid selectors, or unsafe IDs exit non-zero with candidate details. Directory recency is never authority.

The `.sdc` workspace, active-change tree, session pointers, research scratch, state, manifests, and runtime evidence must remain inside the repository and may not traverse symbolic-link ancestors.

Commands:

```text
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" resolve --change <change-id>
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" select --change <change-id> --session-id <safe-session-id>
```

Session pointers are ignored local data and never override confirmed artifacts. They require the complete `sdc.session-pointer/v1` schema, an RFC3339 `selected_at` timestamp, `source: explicit`, and a valid active change. The Claude hook trusts the event payload session ID first; environment fallback is disabled unless `SDC_ALLOW_ENV_SESSION_ID=1` is set intentionally.

Recall stays beneath each allowlisted root and skips symbolic-link components. Credential-shaped values, authorization headers, private-key markers, and high-entropy values are rejected or redacted from recall and runtime evidence. This defense-in-depth filter does not replace a dedicated secret scanner.

## Role Context Manifests

Plan generates deterministic role manifests:

```text
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" manifest generate --change <change-id> --role apply
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" manifest generate --change <change-id> --role check
```

Outputs:

```text
.sdc/changes/active/<change-id>/apply-context.jsonl
.sdc/changes/active/<change-id>/check-context.jsonl
```

Each JSONL record uses this key order:

```text
schema, manifest, change_id, role, order, path, section, purpose, required, source_type, sha256
```

Records contain repository-relative paths, selected sections, purpose, required flag, source type, and current SHA-256. They do not copy file content. Generation validates all required sources before writing; missing or unsafe sources fail without replacing the prior manifest.

Run `manifest verify --change <id> --role apply` (or `check`) to compare every record, schema, source set, and hash with current inputs. Session recovery rejects stale or malformed manifests. After legitimate task/notes updates, refresh manifests at a safe checkpoint; changed governing inputs must be reapproved through revision first. Regenerating a manifest does not refresh lifecycle approvals.

## Candidate Memory Recall

Recall is local, lexical, bounded, and read-only:

```text
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" recall --change <change-id> --query "<terms>" --limit 5
```

Output is JSONL. Every record has `status: Candidate`; recall never writes `knowledge/`, `memory/`, `state.json`, manifests, notes, or Git. Search is limited to allowlisted Markdown under `.sdc/knowledge/`, `.sdc/memory/`, `.sdc/current/`, and the selected active change. `.sdc/runtime/`, generated payloads, and escaping paths are excluded.

## Internal Research Routing

Research remains an internal role and artifact route, not a public command:

```text
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" research route --change <change-id> --stage <change|plan|apply|check|archive> --title "<short-title>"
```

The route returns:

- scratch: `.sdc/runtime/<change-id>/research/<short-title>.md`
- citation: `discovery.md` for change-stage research, otherwise `notes.md`
- durable_candidate: `knowledge-candidates.md`

Scratch material is ignored runtime evidence. Citations are concise pointers in discovery or notes. Durable findings remain Candidate in `knowledge-candidates.md` until archive and human confirmation decide promotion.

## Session Context Adapter

The same helper is the portable fallback when a client cannot inject native hooks:

```text
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" session-context --client codex --change <change-id>
```

Claude Code may invoke the same adapter from `hooks/session-start` and receives:

```json
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"compact context"}}
```

Codex and unsupported clients receive a normal JSON object with `schema: sdc.session-context/v1`, `additionalContext`, selection source, lifecycle state, manifest summaries, and optional Candidate recall count. The context is compact and non-authoritative. Ambiguous active-change resolution still exits non-zero, so adapters must ask for `--change` or `SDC_ACTIVE_CHANGE` instead of guessing from directory recency.

Hook wrappers must degrade to manual SDC instructions on failure and exit successfully so normal stage execution remains usable.

Supported Codex clients may opt into native packaging with `SDC_CODEX_HOOKS=1` at install/package time, then review and trust the hook in the client. The Codex wrapper converts portable context to `hookSpecificOutput.additionalContext` for SessionStart, including supported compact/resume events. Default installation remains portable; never infer capability or auto-approve trust. Hooks provide context only, not enforcement or permission to skip CLI gates.

## Runtime Evidence

Adapters and stages can append local run evidence without modifying durable change artifacts:

```text
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" evidence append --change <change-id> --stage apply --command "<command>" --status <passed|failed> --path <repo-relative-evidence>
```

Evidence records use `schema: sdc.evidence-record/v1` and are written to:

```text
.sdc/runtime/<change-id>/evidence.jsonl
```

The JSONL file is bounded, local, and git-ignored. These records are explicitly agent assertions, not proof that a command ran or passed.

## Measured Delivery Evidence

Run only authorized commands from the project root, with arguments after `--`:

```text
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" evidence run --change <id> --stage check --task T001 --timeout 300 -- python3 -m unittest
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" evidence review --change <id> --reviewer "independent reviewer attribution"
python3 "$SDC_PLUGIN_ROOT/scripts/sdc-runtime-context.py" evidence verify --change <id>
```

`evidence run` records actual exit status, timeout, duration, output digest, environment identity, revision, and input/source snapshot in `evidence/<receipt-id>.json` under the change. It never persists environment values or raw output. Failed commands and source mutations during validation return non-zero. The runner uses direct argv, not implicit shell interpretation; pipelines require an explicitly authorized `sh -c` command also written in the task's Verify field.

Before launching, the runner persists a `running` receipt and holds a per-change OS lock shared with revision and archival. Archive cannot reuse an earlier pass while a newer command is running. Snapshot errors after execution still retain the actual failure result. After a process stops, a fresh successful run can supersede its interrupted/unresolved receipt for each covered task without deleting history or reopening an unchanged plan. Tasks without fresh passing coverage remain blocked; changed requirements or plans still require explicit reopen. Quote knowledge paths containing spaces with backticks or Markdown links so their complete source identity is bound.

Extra durable scripts and fixtures inside the active change are also snapshotted, independently of their extension. Symlinks are rejected. Known governance/progress artifacts use their dedicated snapshots; receipt and revision directories are excluded. Runtime scratch and external tools/dependencies are not a hermetic environment: keep authoritative test inputs in durable source files, and use isolated CI when stronger reproducibility is required.

Every completed task needs a latest passing receipt for the current snapshot and revision whose argv exactly matches that task's Verify command. A single run can name multiple tasks with identical verification. A later failure cannot fall back to an earlier pass. After implementation changes, rerun affected planned verification before delivery; the current conservative source snapshot can require broader reruns when dependency scope is not proven.

Finish task/notes updates and the actual read-only whole-change review before recording `evidence review`. This records attribution and binds the approved review to exact task/notes and source content; it does not perform the review, authenticate the reviewer, or prevent a local user from tampering with files. Preserve independent reviewer execution in the host and use CI attestations for stronger organizational assurance. Structural `validate` alone is not evidence of tested behavior.

An absent findings ledger adds no field to the review snapshot, preserving
unchanged standard approvals created before ledger support. An actual ledger
is hashed, so adding, changing, or removing it invalidates the bound review.
Prefer readable reviewer labels. Bounded lowercase review labels with an ISO
date are checked as descriptive words; explicit credential patterns and opaque
high-entropy values are still rejected. This does not authenticate attribution.
