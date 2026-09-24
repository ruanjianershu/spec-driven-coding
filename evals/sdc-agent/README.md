# Real-Agent SDC Evaluations

Standard-library Python runner for **real installed Codex/Claude CLIs**, separate
from deterministic `sdc-flow` evaluations. No fake provider, implicit harness
retries, model fallback, dependency installation, credential inspection, commits,
deployment, or production fixtures. Python 3.9+ and POSIX process groups required.

## Run

From the repository root:

```sh
# No model calls: inspect installed CLI versions, isolation flags and normal auth status.
python3 -B evals/sdc-agent/run_agent_evals.py --doctor --auth-mode host
python3 -B evals/sdc-agent/run_agent_evals.py --list

# Two bounded trials with the CLI's default model and an existing subscription login.
python3 -B evals/sdc-agent/run_agent_evals.py --agent codex --auth-mode host \
  --baseline --source current="$PWD" --scenario vague-intake \
  --trials 1 --timeout 45 --max-total-trials 2 --output /tmp/sdc-agent-smoke-new

# Same scenarios/model/trial count/budgets across baseline and two supplied snapshots.
# Prepare the previous source directory independently; the runner never checks out git.
python3 -B evals/sdc-agent/run_agent_evals.py --agent codex --auth-mode host \
  --baseline --source current="$PWD" --source previous=/path/to/previous-snapshot \
  --trials 1 --timeout 120 --max-total-trials 18 --output /tmp/sdc-agent-comparison-new

# Claude's confined file-only adapter; see capability limits below.
python3 -B evals/sdc-agent/run_agent_evals.py --agent claude --auth-mode host \
  --baseline --scenario vague-intake --timeout 45 --output /tmp/sdc-agent-claude-new

# Local helper and fake-agent regressions; no auth probes or model calls.
python3 -B -m unittest discover -s evals -p test_agent_evals.py -v
```

Output directories must be new. Omit `--output` to allocate one under system temp.
No raw traces belong in git. API-key/third-party-provider auth is refused; login is
never initiated. `default` means the CLI default with user settings disabled, not
necessarily the model selected in the desktop app. `--model` pins the same request
across all arms; observed model IDs are recorded only when the CLI exposes them.

## Isolation And Bounds

- Every trial gets a fresh temporary project, home, cache and environment. Each
  supplied source is frozen once and content-hashed before running the matrix.
  Only `sdc-cli.py`, `commands/`, `sdc-references/`, and the named local runtime
  helpers are copied: `scripts/sdc-runtime-context.py`, `scripts/sdc-task-brief.py`,
  `scripts/sdc-review-package.py`, `scripts/sdc_evidence.py`,
  `scripts/sdc_compact.py`, `scripts/sdc_findings.py`, and `scripts/sdc-doctor.mjs`.
  These helpers are copied when present so supplied older snapshots remain
  supported. The current CLI/runtime require the compact and findings modules;
  the doctor sidecar supports `sdc-cli.py check installation` and is the only
  explicitly allowed `.mjs` file. Nothing recursively copies `scripts/` or resolves
  dependencies from the host. Both the initial freeze and the per-trial copy
  enforce the 10,000,000-byte / 2,000-file source bounds and reject selected
  symlinks (including linked ancestors). No installer, hooks, plugin metadata,
  generated `skills/`, or source `.sdc/` state is installed.
- The **selected local `commands/sdc.md` is injected directly**. Stage instructions
  come from that snapshot's `commands/<stage>.md`, never the host's older installed
  SDC plugin. Baseline receives the identical task, fixture and safety instructions,
  without any SDC source/injection. This measures explicit-source workflow use,
  not automatic skill discovery, native hook behavior, or a plugin installation.
- Default `--auth-mode isolated` uses a clean CLI home. It normally reports
  unavailable without an existing accessible auth mechanism. `host` explicitly
  reuses CLI auth/state directories without reading/copying credentials or editing
  home configuration. The CLI may update its own auth/session/cache state.
- Codex requires `--ignore-user-config`, `--ignore-rules`, ephemeral execution and
  `skip_host_skill_discovery`; plugins/hooks/apps are disabled. Shell execution uses
  workspace-write with network disabled and no approvals. Claude requires safe mode,
  restricted file tools, no skills/hooks/MCP/Chrome, and no session persistence.
  **Claude has no shell**, so cannot execute SDC helpers/tests in this adapter;
  missing execution evidence stays unknown. Cross-CLI scores are not comparable.
- This is configuration isolation, **not a container or a complete read sandbox**.
  System/managed policy and server-side context may remain. Codex can read outside
  the project under its native policy; host auth directories remain accessible to
  the CLI. Use a disposable OS/container account for stronger isolation. Fixture
  instructions forbid external reads/actions; the harness never executes generated
  code outside the CLI sandbox. Model-service traffic is necessary, task networking
  is forbidden. Existing user processes/configuration are not modified.
- `--timeout` is one shared **model-process** wall budget per trial, including both
  revision phases; output bytes are also shared. Status probes are separately
  bounded (8 seconds each, at most four per trial). Total trials are capped (24 by
  default). Process groups are killed/reaped on timeout, output overflow, interruption
  and normal exit. Detached processes that escape a POSIX group need OS containment.
- Exactly one invocation per planned phase; no automatic rerun/fallback. Streamed
  agent error/retry events abort the process. Unreported CLI-internal retries cannot
  be disabled/count-guaranteed. **No hard token/dollar ceiling** is claimed: usage and
  cost are recorded only if reported, otherwise `null`, never estimated or zero-filled.

The local regression suite freezes the real current repository, then copies that
snapshot into a fresh project exactly as the runner does. It checks identical
manifests/hashes and executes the copied CLI/helper entrypoints there with an
isolated home and no `PYTHONPATH`. When Node.js is available, it also invokes the
doctor directly and through the copied CLI using only the empty temporary home;
the expected result is `NO_INSTALLATIONS` (exit 1), not an import/module failure.
Older snapshots, byte bounds, selected symlinks, and excluded payloads are covered
separately. These checks do not install anything, read host auth, or call models.

## Scenarios

| Scenario | Objective checks | Semantic review remains separate |
| --- | --- | --- |
| vague-intake | No newly created implementation files | Missing questions, invented requirements |
| authorized-maintenance | Trim/lowercase behavior; original tests preserved | Unnecessary approval, honest evidence |
| brownfield-conflict | Original code/tests/knowledge preserved | Confirmed case-preserving contract vs candidate memory |
| failed-test-delivery | Immutable code/tests; observed failing unittest tool exit | Failure blocks delivery, no false approval |
| revision-invalidation | Two fresh invocations; revision-2 behavior; evidence file | Stale revision-1 approval invalidated, fresh proof |
| interruption-resume | Completed artifact unchanged; pending work/progress updated | Reconcile stale claims with actual files |

Revision 2 replaces requirements between two sessions in the **same trial project**,
not a retry. Both share the trial budget. Interruption-resume is a **seeded durable
handoff fixture**, not a claim that a model was killed mid-tool and natively resumed.

## Results And Grading

`run.json` indexes per-trial `result.json`. Each records selected-source/fixture
hashes, requested model, CLI/auth/isolation metadata, limits, phase argv/process
exit/timeout/elapsed, model completion/error, reported usage, tool exits, structural
checks, execution availability/failure category, and transcript references.
`before.json`, `after.json`, `project/`, saved
prompts and phase stdout/stderr provide reviewable evidence. Revision phase projects
are retained separately. Original temporary projects are removed after each trial.

Structural checking does **not** trust prose `PASS`, execute model-written tests, or
infer absent usage. The tiny normalization checker interprets only a pure AST subset
of string method calls; other valid implementations are **unknown**, not failed or
passed. That check is not evidence that tests ran. Test execution claims require
actual tool events. CLI exit 0 without a structured completion is unknown.

`execution` distinguishes infrastructure from task behavior. Recognized authentication,
network, service/quota and CLI-configuration errors are `blocked`, with a
`failure_category`; failed readiness/launch is `unavailable`. Raw process/model exits
remain in each phase. A ready status probe is not proof that print/exec mode can
reach the model. Claude `subtype: success` is insufficient: completion also requires
explicit `is_error: false` and no earlier error; synthetic auth messages are not models.

`objective_outcome` describes the limited structural checks **only after confirmed
process and model completion**. Blocked, unavailable and otherwise incomplete runs
are `unknown`, even when an untouched fixture still fails its acceptance checks.
The individual file/check observations are retained, not promoted to a task-behavior
failure. Error diagnostics are classified separately from normal model prose and
tool output. Unrecognized execution failures remain unknown, never assumed passing.

`semantic` stores a rubric, `unknown` status and empty judgments: **no model judge is
run or fabricated**. Independent human/model review should record reviewer/model,
rubric version and transcript citations separately. Overall `outcome` never becomes
pass merely because structural checks passed. Exit codes: 1 for a completed trial's
objective failure or invalid source setup; 2 for blocked/unavailable/incomplete or
otherwise unresolved results; 0 only for list/doctor;
130 for interruption. A successful doctor invocation does not mean model availability.

This is a small, fixed-order, unseeded evaluation, not a benchmark proving general
improvement. Compare within a pinned CLI/model and identical budgets; inspect unknowns,
source differences, refusals, auth failures and capability restrictions before drawing
conclusions. Unit-test passes and smoke connection attempts are not behavioral wins.
