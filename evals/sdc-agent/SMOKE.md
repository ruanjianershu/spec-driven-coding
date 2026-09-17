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
- Follow-up: the light risk policy reduces repetition, not the current workspace
  and artifact schema minimum. A compact cold-start path remains future work and
  must not be advertised as delivered or token-saving based on this probe.
