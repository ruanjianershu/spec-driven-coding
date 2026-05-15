# SDC Discipline Core

SDC v1.1 keeps the public command surface small while strengthening the internal engineering discipline.

The goal is not to copy every OpenSpec, Superpowers, or SDDInAction command. The goal is to keep their useful core:

- OpenSpec: change lifecycle, validation, archive.
- Superpowers: lightweight skill-pack distribution.
- SDDInAction / Karpathy-style skills: think before coding, thin slices, TDD, stop-line reports, evidence over vibes.

## Public Surface

Normal users should only need these commands or natural-language equivalents:

```text
/sdc:init
/sdc:change
/sdc:plan
/sdc:apply
/sdc:check
/sdc:archive
/sdc:harness
```

Detailed skills such as `sdc:spec`, `sdc:validate`, `sdc:review`, `sdc:test`, and `sdc:quality` remain available for advanced users and internal routing.

## Two Decision Chains

Every SDC workspace should have `.sdc/constitution.md`.

Governance priority:

```text
.sdc/constitution.md > AGENTS.md > conversation instructions
```

Fact priority:

```text
spec.md > design.md/plan.md > tasks.md > code
```

When these sources conflict, the agent should stop and produce a Stop-Line Report instead of guessing.

## Traceability Chain

Every meaningful change should preserve this chain:

```text
SCN-* -> REQ-* -> AC-* -> T### -> validation evidence
```

Where:

- `SCN-*` is a user or system scenario.
- `REQ-*` is a requirement or business rule.
- `AC-*` is an acceptance criterion, preferably expressed with Given/When/Then.
- `T###` is a concrete task in `tasks.md`.
- Validation evidence is a test command, review note, manual verification, or documented blocker.

## Stop-Line Report

Use a Stop-Line Report when execution cannot proceed safely:

```markdown
## Stop-Line Report
- Trigger:
- Evidence:
- Conflicting files:
- Affected REQ/AC:
- Options:
- Recommended next step:
```

Common triggers:

- spec, design, tasks, or code conflict.
- acceptance criteria are missing or unverifiable.
- implementation requires changing scope or public behavior.
- tests cannot prove the requested behavior.
- security, data migration, compatibility, or rollout risk appears.

## `/sdc:check` Modes

`/sdc:check` is the single quality entry point. It covers:

- delivery check: validate, review, test, quality.
- bug analysis: analyze only, no code changes unless the user asks for a fix.
- impact analysis: identify affected modules, contracts, data, tests, and rollback.
- repo analysis: brownfield project scan with evidence anchors.

This keeps the public interface simple without losing the deeper workflows.

## Task Format

Tasks must stay small and traceable:

```markdown
- [ ] T001 [REQ-01] [AC-01] [Phase 1] [Size: S] Write failing test for invalid login.
  - Depends on: none
  - Verify: npm test -- auth
  - Source: .sdc/changes/active/2026-05-15-login/spec.md#AC-01
```

Rules:

- `Size` is `S` or `M`; never `L`.
- tests come before implementation tasks.
- each task references at least one `REQ-*` and one `AC-*`.
- each task has dependency, verification, and source information.

## Design Principle

SDC should feel simple to operate and strict when it matters:

- simple outside: a few stable commands.
- disciplined inside: decision chains, traceability, and evidence gates.
- no ceremony for ceremony's sake.
