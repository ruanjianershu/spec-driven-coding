# SDC Common Ground

Common Ground is the project-level shared understanding layer. It makes the agent's assumptions visible before those assumptions affect specs, plans, tasks, code, or archive decisions.

## Purpose

Use Common Ground to answer:

- What has the user or project already confirmed?
- What is a reasonable working interpretation, but still not project truth?
- What remains open and must be clarified before final artifacts or execution?

Common Ground does not replace `knowledge/`, `memory/`, `Decision Ledger`, or `project-cognition.md`.

It coordinates them:

```text
common-ground.md -> discovery/spec/impact/plan/apply/check/archive
knowledge/        -> confirmed product and technical facts
memory/           -> recall, candidates, procedures, lessons
Decision Ledger   -> high-impact decisions for the current change
project-cognition -> reusable Brownfield/Legacy repository map
```

## Confidence Tiers

Use exactly these tiers:

| Tier | Meaning | Can drive final execution? |
| --- | --- | --- |
| ESTABLISHED | Confirmed by the user, current code/config evidence for technical behavior, archived specs, decision records, or authoritative project documents. | Yes, within current evidence and authorization scope |
| WORKING | Evidence-supported interpretation that can guide exploration, but must be cited when used. | Only for low-impact exploration or investigation tasks |
| OPEN | Unknown, conflicting, or high-impact. Ask before relying on it. | No |

Rules:

- `OPEN` items block confirmed spec, final design, implementation tasks, apply, and archive when they affect scope, acceptance, data, permission, architecture, security, rollout, or compatibility.
- `WORKING` items must not be silently promoted to `ESTABLISHED`.
- Promotion requires user confirmation or stronger evidence.
- Demotion is required when code, current artifacts, or user feedback contradicts an item.
- Code describes current behavior; it does not authorize new business requirements. Personal/native memory is Candidate recall, not an ESTABLISHED source by itself.
- Check freshness against the affected source identity and scope, not just its timestamp. Refresh affected evidence within existing authority; record drift for confirmed durable updates rather than silently rewriting project truth.

## Assumption Origin Types

Every Common Ground entry must state its origin:

| Type | Meaning |
| --- | --- |
| stated | The user explicitly said it. |
| inferred | Derived from current project evidence such as code, config, tests, specs, or standards. |
| assumed | A proposed default or best-practice guess. |
| uncertain | Not enough evidence; needs clarification. |
| delegated | The user explicitly allowed the agent to choose within a bounded area. |

`assumed` and `uncertain` entries cannot be `ESTABLISHED`.

`delegated` can be `ESTABLISHED` only within an explicit decision area, allowed choices/constraints, impact limit, and stopping boundary. Cite the delegation and selected option. Generic "use your judgment" does not confirm unknown business requirements, scope, data, permissions, public contracts, or architecture. See `workflow-standards.md` when a delegation boundary needs interpretation.

## Required File Shape

`.sdc/common-ground.md` should use this shape:

```markdown
# Common Ground

## Snapshot
- Project:
- Updated:
- Source scope:

## ESTABLISHED
| ID | Statement | Type | Source | Verified At | Verified Against | Scope |
| --- | --- | --- | --- | --- | --- | --- |

## WORKING
| ID | Statement | Type | Source | Confidence | Risk If Wrong | Next Check |
| --- | --- | --- | --- | --- | --- | --- |

## OPEN
| ID | Question / Assumption | Type | Blocks | Options | Required Before |
| --- | --- | --- | --- | --- | --- |

## Changes Since Last Update
| Date | Change | From | To | Source |
| --- | --- | --- | --- | --- |
```

## Stage Rules

### init

- Create `common-ground.md` with starter sections.
- For Greenfield projects, leave product and technical facts mostly `OPEN` unless the user provided them.
- For Brownfield/Legacy projects, add only code-evidence-backed facts as `ESTABLISHED`; put unclear architecture or business intent in `WORKING` or `OPEN`.

### change

- Read relevant `common-ground.md` entries before intake; reuse unchanged, already-loaded sources.
- Use it to avoid repeated questions, but never treat `WORKING` as user confirmation.
- Any high-impact `OPEN` item relevant to the current change must become an intake or discovery question.
- Cover the four intake categories using cited prior/current confirmation; ask only missing blocking questions, not a fixed question set.

### spec

- Final `REQ-*`, `AC-*`, and `INV-*` may depend only on `ESTABLISHED` Common Ground, confirmed discovery, or confirmed Decision Ledger entries.
- If a `WORKING` item is needed for final requirements, ask for confirmation first.

### plan

- Read Common Ground before technical planning.
- Resolve uncertain technical assumptions by focused evidence gathering within confirmed scope before finalizing dependent tasks. Unknown business requirements remain in discovery, never in spec/design/tasks.

### apply

- Do not implement from `OPEN` or high-impact `WORKING` Common Ground entries.
- If code evidence changes an `ESTABLISHED` item, record drift in `knowledge-candidates.md` or `notes.md`; archive decides promotion.

### check

- Check whether final artifacts depended on `WORKING` or `OPEN` items.
- Check whether the implementation introduced drift that should update Common Ground.

### archive

- Common Ground updates are incremental conditional durable updates.
- Required archive assets may be written, but updating `common-ground.md` requires explicit human confirmation. A timestamp/link update cannot claim refreshed evidence without checking the affected source.

## Stop Conditions

Stop when:

- A required fact is `OPEN`.
- A high-impact fact is only `WORKING`.
- A `WORKING` or `ESTABLISHED` item conflicts with code, specs, standards, or user confirmation.
- Relevant Common Ground was neither loaded nor checked as still current before dependent change/plan/apply/check work.

Use the Stop-Line Report format from `workflow-standards.md`.
