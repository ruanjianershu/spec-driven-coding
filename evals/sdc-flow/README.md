# SDC Flow Evals

This directory contains deterministic SDC workflow evals inspired by open-source agent/prompt testing tools such as Waza and promptfoo.

## Local Runner

```bash
npm run eval:sdc
```

The local runner does not call an LLM or require API keys. It creates temporary projects and verifies SDC CLI behavior for:

- `init` knowledge/memory workspace creation
- safe `init` upgrade of stale managed SDC templates with backups
- Discovery Open minimal artifacts
- blocking premature `context-pack.md`
- blocking Brownfield changes without `impact.md`
- archive Knowledge Compact Gate recommendations for product knowledge, technical knowledge, and memory
- blocking unconfirmed assumptions from final execution artifacts
- blocking open Knowledge Gaps from execution handoff
- blocking incomplete knowledge candidates before archive readiness

## promptfoo Config

`promptfooconfig.yaml` lets teams run the same scenarios through promptfoo when it is available in CI:

```bash
npx --yes promptfoo@latest eval -c evals/sdc-flow/promptfooconfig.yaml
```

The provider is deterministic Python (`sdc_flow_provider.py`), so these evals stay stable and do not depend on model output.
