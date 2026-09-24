# Stable Review Findings

`scripts/sdc_findings.py` is a standalone internal helper, not a public slash
command or another runtime layer. It never executes commands, opens evidence
references, or infers that tests passed. Its ledger is
`.sdc/changes/active/<change-id>/findings.json`.

## Identity And Evidence

- Assign a stable finding ID once and reuse it for the same issue. IDs are
  case-sensitive and match `[A-Za-z0-9][A-Za-z0-9._-]*`. There is no delete,
  rename, automatic numbering, or merging operation.
- `record` means a failed observation. Supply a nonempty summary, source,
  evidence, and actor. For recording, `source` should be a stable source-snapshot
  digest and `evidence` a stable evidence digest or immutable evidence citation.
  Use the same representation for unchanged evidence, not a new timestamp or
  invocation ID for every identical failure. Never include secrets or raw
  sensitive output.
- The failure fingerprint is SHA-256 of canonical JSON containing `source` and
  `evidence`, after trimming surrounding whitespace. Finding ID scopes the
  count. Actor, summary, timestamp, and revision are not fingerprint inputs.
  A repeated pair appends an observation but does not increment counts, consume
  retry allowance, reopen a resolved finding, or remove a block.
- Different IDs have independent counts, even when their fingerprints match.
  Different source/evidence pairs under one ID count as distinct failures.

## State Rules

| State | Delivery gate | New distinct failure allowed? |
| --- | --- | --- |
| `open` | Blocked | Yes, within the remaining allowance |
| `adjudication-required` | Blocked | No, needs human adjudication |
| `accepted-risk` | Blocked | No, needs an explicit retry decision |
| `resolved` | Clear for this finding only | Yes, starts a new unresolved chain |

The third distinct failed observation in an unresolved chain requires human
adjudication. Counts survive revisions, risk acceptance, and retry grants. A
fourth distinct failure is rejected until a decision authorizes retry; a
duplicate observation may still be retained without allowing another attempt.

Adjudication requires an actor, explicit source citation to the human decision,
and rationale. Its only decisions are:

- `retry`: explicitly grant 1-3 additional distinct failed observations. This
  returns the finding to `open`, does not reset its failure count, and never
  clears delivery. Exhausting the grant requires another adjudication. Grants
  cannot be stacked while a finding is open. The same decision source cannot be
  reused for that finding, including under a new actor label or rationale.
- `accepted-risk`: retain the finding as blocking accepted risk with zero retry
  allowance. Risk acceptance is neither resolution nor a passing review.

Resolution is a separate operation requiring nonempty evidence, source, and
actor. A finding awaiting adjudication cannot be resolved before a decision is
recorded. An accepted-risk finding can later be resolved with explicit evidence;
the acceptance event alone never resolves it. A retry authorization also needs
a later resolution event to clear the finding.

A new distinct failure after resolution reopens the same stable ID and starts
a new count. Lifetime totals and every earlier event remain available. Replaying
any previously recorded failure pair is only an observation, not a new chain.

## Python API

Import from the existing `scripts` module search path:

```python
from sdc_findings import (
    record, resolve, adjudicate, list_findings,
    assert_clear, assert_retry_allowed,
)

record(root, change_id, "F-9", summary="Missing authorization check",
       source="sha256:source-snapshot", evidence="sha256:failure-evidence",
       actor="reviewer-label")

adjudicate(root, change_id, "F-9", decision="retry", retry_limit=1,
           source="review-thread/message-17", rationale="Try the narrower fix",
           actor="maintainer-label")  # Only after retry is blocked.

resolve(root, change_id, "F-9", source="verification/receipt-42",
        evidence="Regression passes against the corrected authorization check",
        actor="reviewer-label")
```

All functions take `root: Path` and `change_id: str`; mutations also take
`finding_id: str` and the keyword fields shown above. `adjudicate` defaults
`retry_limit` to zero for `accepted-risk`; `retry` requires an explicit 1-3.
Mutations return the derived finding. `list_findings` returns findings in
first-recorded order, with `id`, `summary`, `status`, `failed_attempts`,
`total_failed_attempts`, `retry_remaining`, and per-finding `history`.

`assert_clear(root: Path, change_id: str)` returns `None` when every finding is
resolved, or when a valid active change has no ledger (legacy compatibility).
It raises `ValueError` for open, adjudication-required, or accepted-risk findings
and for malformed ledger data. A missing active change is an error, not a legacy
ledger. Reads do not create files or acquire a delivery lock.

`assert_retry_allowed(root, change_id, finding_id)` returns `None` only for a
known open finding with allowance remaining; otherwise it raises `ValueError`.
It is a read-only preflight, not an attempt reservation or a command runner.

## Internal CLI

Keep the target project as the working directory. Resolve `SDC_PLUGIN_ROOT`
from the current installed skill/command as described in its entrypoint, using
the verified `sdc-runtime/` child for direct layouts. Common options follow the
subcommand; `--root` defaults to the current project. All change IDs are explicit.

```sh
python3 "$SDC_PLUGIN_ROOT/scripts/sdc_findings.py" record --change example --id F-9 \
  --summary 'Missing authorization check' --source 'sha256:source-snapshot' \
  --evidence 'sha256:failure-evidence' --actor 'reviewer-label'
python3 "$SDC_PLUGIN_ROOT/scripts/sdc_findings.py" list --change example
python3 "$SDC_PLUGIN_ROOT/scripts/sdc_findings.py" adjudicate --change example --id F-9 \
  --decision retry --retry-limit 1 --source 'review-thread/message-17' \
  --rationale 'Try the narrower fix' --actor 'maintainer-label'
python3 "$SDC_PLUGIN_ROOT/scripts/sdc_findings.py" resolve --change example --id F-9 \
  --source 'verification/receipt-42' --evidence 'Regression now passes' \
  --actor 'reviewer-label'
```

Successful operations emit JSON with `ok: true` and `finding` or `findings`.
Invalid arguments, blocked operations, corrupt files, unsafe paths, and lock
contention emit `{"ok": false, "error": "..."}` on stdout with a nonzero exit
status. `--help` is ordinary text. Shell-like strings supplied as evidence are
stored as data, never interpreted or executed by the helper.

## Persistence And Integration

The versioned JSON object has `schema: 1`, `change_id`, and an append-only
`history`. Each event retains its revision from `state.json` (or `initial` when
absent), timestamp, source, and actor. Status and counts are replayed from the
history instead of trusting mutable summary fields. Duplicate keys, invalid
schemas, invalid transitions, and incorrect failure fingerprints fail closed.

Mutations acquire `sdc_evidence.change_lock`, revalidate paths, and replace the
ledger atomically through a flushed temporary file in the same directory.
Existing events are never rewritten semantically or removed. Symlinked ledger,
state, active-change ancestors, and lock paths are rejected. Existing revision
archives are never modified.

Runtime integration contract:

1. Call `assert_clear(root, change_id)` inside the existing delivery lock before
   writing an approved review verdict, validating delivery, or archiving. The
   function intentionally does not reacquire that non-reentrant lock. Retain
   all existing execution, review, freshness, and lifecycle gates.
2. Keep the active `findings.json` on revision/reopen. An optional copy in a
   revision archive must not replace, clear, or truncate the active ledger.
   Archive the complete change directory, including this history.
3. Bind the ledger to review freshness. Recording or resolving a finding must
   invalidate a prior review snapshot; ledger edits alone should not invalidate
   source-execution receipts. Do not include the ledger itself in the source
   fingerprint supplied to `record`, or every observation changes its own input.
4. Before a cooperating automatic repair attempt, inspect the finding and call
   `assert_retry_allowed`. Coordinate concurrent runners externally. Mutation
   helpers acquire their own locks, so do not call them while already holding
   `change_lock`. This module neither reserves nor executes attempts.
5. Installed payloads include this helper beside `sdc_evidence.py`. The runtime
   blocks automatic verification runs while adjudication or accepted risk is
   unresolved. Public command names remain unchanged.

## Enforcement Limits

IDs and all provenance are caller-supplied. The ledger cannot recognize the same
semantic issue renamed to a fresh ID, authenticate a human or reviewer label,
verify that a cited decision exists, prove evidence content or freshness, or
prevent an external runner from ignoring its preflight. Human authorization
must be established by the parent workflow before recording adjudication.
Changing evidence representations can defeat deduplication; use stable digests.
Nonempty resolution evidence is a minimum record contract, not a test execution
receipt or proof that the issue was fixed.

This is cooperative local bookkeeping, not tamper-proof storage. A process with
filesystem write access can alter or delete history; absent-ledger legacy
compatibility cannot distinguish such deletion from a change that never had a
ledger. Shared locking and symlink checks do not protect against hostile
filesystem races. No ledger operation alone confers a passing delivery verdict.

## Verification

```sh
python3 -B -m unittest evals.test_review_findings -v
```

The tests use disposable filesystems and real subprocesses for deduplication,
per-issue failure chains, revision retention, bounded adjudication, resolution,
JSON errors, unsafe paths, shared-lock contention, and competing writers.
