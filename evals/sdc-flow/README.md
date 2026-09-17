# SDC Flow Evals

This directory contains deterministic SDC workflow evals inspired by open-source agent/prompt testing tools such as Waza and promptfoo.

## Local Runner

```bash
npm run eval:sdc
```

The local runner does not call an LLM or require API keys. It creates temporary projects and verifies SDC CLI behavior for:

- `init` knowledge/memory workspace creation
- safe `init` upgrade of stale managed SDC templates with backups
- fingerprint-based preservation of user-modified managed files
- exact-hash upgrade support for known 1.2.x generated templates
- managed fingerprints excluded from real-content detection
- additive migration of existing `.sdc/.gitignore` files so runtime scratch stays local without losing team rules
- importing a company/team standards pack with a routing index and no local path leak
- Discovery Open minimal artifacts
- blocking premature `context-pack.md`
- blocking Brownfield changes without `impact.md`
- archive Knowledge Compact Gate recommendations for product knowledge, technical knowledge, and memory
- blocking unconfirmed assumptions from final execution artifacts
- blocking open Knowledge Gaps from execution handoff
- blocking OPEN and final-execution WORKING Common Ground
- blocking incomplete knowledge candidates before archive readiness
- blocking missing triggered Artifact Output Contracts
- blocking task plans without explicit interfaces
- blocking present-but-empty task interfaces
- blocking empty or cross-artifact-conflicting Global Constraints
- blocking self-declared Plan Preflight without reviewed sources and closed findings
- blocking explicitly open Plan Preflight findings
- rejecting uncertain closure forms such as `Resolved?`
- blocking completed tasks without approved review evidence
- requiring separate Spec Compliance and Code Quality verdicts per completed task and final review
- resolving durable review Evidence references instead of accepting arbitrary text
- rejecting ignored runtime or external files as durable review evidence
- warning rather than blocking when the ignored recovery ledger is absent after checkout
- blocking when a present recovery ledger conflicts with durable task state
- file-based task brief and review-package handoffs
- refusing incomplete WORKTREE review packages when untracked files would be omitted
- keeping shared/apply/generated execution contracts serial and in sync
- validating all seven lifecycle states, legal forward transitions, and mutation-free rejected transitions
- resolving exactly one active change with explicit/environment/session/sole-directory precedence and non-zero ambiguity failures
- generating byte-identical, ordered, path-safe, hash-backed apply/check JSONL context manifests
- keeping bounded local memory recall deterministic, read-only, and `Candidate`-only while excluding sensitive or unsafe sources
- routing research scratch, citations, and knowledge candidates internally without adding a public command
- emitting compact Claude `SessionStart` context with safe failure fallback
- using the Codex skill adapter without a native hook field or client-package cross-contamination
- validating the repository root as a Claude marketplace with explicit advanced source skills and no duplicate public workflow registration
- removing stale pre-1.3 Codex plugin layout during upgrade
- recovering interrupted Codex plugin replacement transactions
- rootless, minimal, deterministic Codex portal packaging

## promptfoo Config

`promptfooconfig.yaml` lets teams run the same scenarios through promptfoo when it is available in CI:

```bash
npx --yes promptfoo@latest eval -c evals/sdc-flow/promptfooconfig.yaml
```

The provider is deterministic Python (`sdc_flow_provider.py`), so these evals stay stable and do not depend on model output.
