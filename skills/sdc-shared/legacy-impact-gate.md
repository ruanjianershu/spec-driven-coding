# Legacy Impact Gate

Legacy Impact Gate protects existing systems from accidental change. It applies to Brownfield/Legacy projects after the requirement is confirmed and before final planning or implementation.

## Timing

Correct sequence:

```text
init project cognition -> change/discovery -> confirmed spec -> impact.md -> plan -> apply -> check final impact review
```

Do not perform per-change impact analysis during `sdc-init`; init only creates or updates project-level cognition.

## Brownfield / Legacy Signals

Treat a project as Brownfield/Legacy when visible evidence includes existing source code, package/build files, runtime configuration, tests, CI, database scripts, public contracts, historical business modules, deployment scripts, or active integration points.

If uncertain, mark the project as `Unknown` or `Likely Brownfield` and preserve the uncertainty.

## Project Cognition

`project-cognition.md` is project-level memory. It should capture:

- Runtime shape, entrypoints, build commands, test commands, deployment hints.
- Module map and dependency direction.
- Core data models and public contracts.
- External integrations.
- Quality and maintenance risks.
- Reading order for future agents.
- Evidence labels: `[Confirmed Fact]`, `[Reasoned Inference]`, `[Open Question]`.

## Change Impact Gate Trigger

Run Change Impact Gate when:

- The project is Brownfield/Legacy.
- The current change has a confirmed or nearly confirmed spec.
- The change may affect existing behavior, public interfaces, data, permissions, configuration, UI, CLI, SDK, messages, scheduling, deployment, or security.

## `impact.md` Required Contents

```markdown
# Change Impact

## Analysis Snapshot
- Repository:
- Change:
- Branch / commit:
- Evidence limits:

## Entry Points And Call Chain

## Direct Changes Required
| File / Contract | Reason | Evidence |
| --- | --- | --- |

## Cascading Impact

## Contracts / Data / Config / Permissions / Security / Observability

## Tests And Regression Strategy

## Implementation Order And Rollback Boundary

## Open Questions
| Question | Why It Matters | Blocking? |
| --- | --- | --- |

## Evidence Index
| Claim | Source |
| --- | --- |
```

## Evidence Rules

- Code, configuration, build files, tests, CI, scripts, database scripts, API definitions, and runtime entrypoints are primary evidence.
- README, comments, old docs, and historical notes are clues only.
- Start from the changed entrypoint, then trace the call chain and data/contract boundaries.
- Do not list the whole repository. Identify the necessary impact radius.
- If evidence is missing, write "insufficient evidence" instead of guessing.

## Stop Conditions

Do not proceed to final plan or apply when unresolved impact questions affect scope, acceptance, public contracts, data migration, permissions, security, rollout, or rollback.

## Final Impact Review

During delivery check or review, compare actual diff against `impact.md`:

- Actual modified files, modules, interfaces, config, data, tests.
- Impact areas that match `impact.md`.
- New impact areas not captured in `impact.md`.
- Contract, data, permission, security, observability, and rollback risk.
- Regression tests that prove old behavior still works.

If actual changes exceed `impact.md` in a high-impact area, the delivery is blocked until artifacts are updated and reviewed.

