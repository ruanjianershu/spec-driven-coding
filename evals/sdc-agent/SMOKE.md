# Local Smoke Record: 2026-09-16

- CLI status checks found Codex `0.154.0-alpha.6.2` logged in with ChatGPT and Claude
  `2.1.266` with first-party OAuth. Only normal version/help/auth status commands were
  used; the harness did not read credentials, initiate login or use API keys.
- Two genuine Codex CLI model attempts used its default model: one no-SDC baseline
  and one selected-source `vague-intake` trial, with identical 45-second / 500,000-byte
  budgets. Both reached model-service connection attempts, encountered TLS handshake
  EOF errors, and were killed at 45.0046 seconds (exit -9). No model response completed;
  tokens/cost and semantic behavior remain unknown. Model evaluation is **blocked by
  connectivity**, not demonstrated passing.
- Local raw artifacts: `/private/tmp/sdc-agent-smoke-20260916-v2/run.json`, with
  `baseline--vague-intake--1/` and `current--vague-intake--1/` trial directories.
  These are machine-local temporary paths, not distributed fixtures or checked-in traces.
- The parent ran one additional bounded Claude baseline `vague-intake` CLI trial.
  Its normal auth/status probe reported ready, but print mode returned
  `authentication_failed`, a synthetic "Not logged in" message, and a result with
  `subtype: success` **and `is_error: true`**. The process exited 1; no genuine model
  answer completed. This is **blocked authentication**, not failed SDC task behavior.
  Local raw artifacts remain at `/private/tmp/sdc-agent-claude-20260916-upgrade/`.
- The revised classifier was replayed offline against all three existing traces:
  Codex baseline/source both classify as `blocked` / `network`, and Claude baseline
  as `blocked` / `authentication`. Objective and semantic behavior are `unknown` for
  all three. Original raw logs and historical result files were not rewritten; their
  earlier `fail` labels reflect the old classifier, not a behavioral conclusion.
  No further model attempts were made for this correction. This record includes no
  user identity, credential contents, session identifiers or usage values.
- An earlier adapter/config preflight failed before model connection because this
  CLI rejects overrides of its built-in provider. Those two failed launch records
  remain at `/private/tmp/sdc-agent-smoke-20260916/`; they are not behavior trials.
- No attempt was silently retried by the harness. The CLI itself emitted reconnect
  events despite disabling its unbounded retry feature. A subsequent harness change
  now aborts on streamed errors/retry announcements; this guard is fake-process unit
  tested, not claimed as another successful real smoke.
- Codex smoke predates the final direct `commands/sdc.md` injection and runtime-support
  staging fixes. Since neither model responded, it provides no evidence about either
  instruction form. Final source-selection behavior is unit tested. No broad SDC
  improvement, baseline superiority, successful delivery or model-usage claim follows.

## Native Subagent Probes

These two additional probes used fresh Codex subagents with the revised local
instructions in disposable projects, not the CLI harness or an installed plugin.
They are narrow workflow observations, not a blinded model or client comparison.

- Vague meeting-room booking request: asked for missing context, scope, technical
  choices, and constraints; marked alternatives Proposed and requested permission
  before persisting discovery. The project remained empty.
- Explicitly authorized README typo in an uninitialized project: corrected only
  the requested text, did not repeat user questions, and a real scoped validation
  exited zero. However, more than twenty SDC files were created and the run stopped
  at `applying` before final review and delivery. This does not pass an end-to-end
  or efficiency claim. The agent's suspected README digest mismatch was checked
  using the actual snapshot helper: the receipt and current source map matched;
  source digests include permission modes, not just file bytes.
- Follow-up at the time of this initial probe: the light risk policy reduced repetition, not the then-current workspace
  and artifact schema minimum. A compact cold-start path remains future work and
  must not be advertised as delivered or token-saving based on this probe.

## Compact Upgrade Probes: 2026-09-24

Two fresh native Codex subagents read the selected source skills and references.
They did not load a released plugin or run a Codex/Claude CLI model comparison.
The experiments used disposable fixtures, not a user's product or home settings.

- **Unsettled meeting-room approval:** the user authorized discussion only and
  had not decided which reservations need approval. The agent distinguished
  Proposed alternatives from facts, asked one prerequisite question about the
  business problem and example, and created/modified **zero files**. It did not
  invent approvers, timeouts, reservation policies, or a technical stack. This
  tests one initial reply, not a complete multi-turn discovery process.
- **Confirmed README spelling:** the agent used the compact format without a
  full init or spec/design/tasks package and asked no redundant questions. It
  stopped at `applying` when independent review was unavailable rather than
  marking its own work approved. The parent then independently checked the full
  before/after text, exact resulting bytes and file mode, scoped inventory, and
  CLI validation. Both review verdicts passed with attributed evidence.
- The same agent resumed, reran the exact recorded Verify command, bound the
  actual parent review, refreshed both role manifests, verified receipts,
  advanced through `checking` and `archivable`, and archived successfully.
  The active change was absent afterward; its persisted state remains
  `archivable` inside the archive, not an invented `archived` lifecycle state.
- The completed fixture contains **12 project files**, including README and
  machine evidence/runtime bookkeeping, plus **7 transport/report files**.
  The single canonical compact record does not mean a one-file installation or
  a one-file final archive. No business spec, knowledge, or memory was promoted.
- One initial attempt was preserved and restarted once after the in-development
  baseline format changed. Both attempts together retained **31 files**. Earlier
  helper changes were recorded; fresh final verification was run. This was a
  collaborative probe during implementation, **not an immutable end-to-end
  benchmark**. No token/cost savings or client-wide success rate was measured.

Separate deterministic tests exercise cold start, real failing/passing commands,
full archive, unknown scope, missing authority/review, receipt and manifest
freshness, ignored/filtered targets, transitive governance, preserved revisions,
and baseline integrity. Windows baseline translation is simulated, not a native
Windows client run. Installation tests use real Node/installer subprocesses in
isolated homes, with Claude registration stubbed; they do not prove a running
client's command palette. Historical connectivity/authentication blockers above
remain historical blockers, not overwritten as passing results.
