# Discovery Gate

Discovery Gate is the SDC replacement for broad brainstorming. It borrows divergent thinking, but it must converge into a small, verifiable change.

## Mandatory Change Intake Gate

Before creating or updating any `.sdc/changes/active/*` files, ALWAYS run Change Intake Gate. Do not let the agent decide silently whether the requirement is "clear enough".

The first response to a new `/sdc:change ...` request must:

1. Restate only what the user has said.
2. If `.sdc/knowledge/index.md` exists, use it to prefill known context and reduce repetitive questioning, but mark unconfirmed or memory-derived content as `Candidate`.
3. Ask 4 intake questions, one for each required category below.
4. Wait for explicit user confirmation before writing files.
5. Avoid assuming tech stack, timeline, scope, database, framework, deployment, integrations, roles, permissions, or success criteria.

Required intake categories:

- Project context: greenfield or existing codebase, solo/team, target users.
- Core scope: must-have vs nice-to-have, MVP boundary, non-goals.
- Technical preferences: language, framework, database, platform, deployment.
- Constraints and acceptance: deadline, budget, integrations, compliance/security, how done will be proven.

The agent may propose options, but every option is `Proposed` until the user confirms it. No change files, confirmed spec, final plan, or implementation tasks may be written before intake confirmation.

## Artifact Budget While Discovery Is Open

When any blocking Open Question remains, keep artifacts minimal:

- Default: ask the next 3-5 highest-value questions in chat and do not write files.
- If persistence is useful after intake confirmation, create or update only `discovery.md`, plus an optional Draft `proposal.md` and brief `notes.md`.
- Do not create or update `spec.md`, `design.md`, `tasks.md`, or `impact.md` while Discovery Gate is open.
- Do not output a large task list, API design, database schema, or implementation plan while Discovery Gate is open.
- Do not ask every possible question. Ask only the questions required to close the next decision gate.

## When To Continue Discovery

After intake confirmation, continue Discovery Gate when any of these remain unresolved:

- Target user or affected actor.
- Business goal.
- In-scope and out-of-scope boundary.
- Main scenario or failure scenario.
- Acceptance direction.
- High-impact decision status.
- Whether the request should be one change or several changes.

Do not produce a `Confirmed` spec, final plan, or implementation tasks while Discovery Gate is open.

Open Questions are blockers unless they are explicitly deferred outside the current MVP. A Draft artifact may mention them, but they must not become final REQ/AC, design decisions, or tasks.

## Explicit Confirmation Gate

Interpretation summaries are not consent.

Forbidden write-ahead patterns:

- "If this is wrong, tell me; I will update the files now."
- "I will assume X and proceed unless you object."
- "如有偏差请告知，我先按这个更新。"
- "如果不对告诉我，我先改。"

Required pattern:

1. State the interpretation as `Proposed`.
2. Ask a yes/no or option-selection confirmation question.
3. Wait for the user's answer.
4. Write durable artifacts only after confirmation.

## Discovery Method

Use a lightweight sequence:

1. Restate only what the user has actually said.
2. Identify missing facts and high-impact decisions.
3. If the user has not selected a direction, offer 2-3 candidate directions and mark them `Proposed`.
4. Recommend a smallest viable change slice.
5. Ask 3-5 key questions when more discovery is still required after intake.
6. Record decisions in `discovery.md`.
7. Exit only when the MVP and blockers are confirmed or explicitly deferred.

## Required Output In `discovery.md`

```markdown
# Discovery

## Current Understanding

## Candidate Directions
| Option | Description | Pros | Cons | Status |
| --- | --- | --- | --- | --- |

## Tradeoffs

## Recommended MVP

## Decision Ledger
| ID | Decision | Status | Source | Impact | Next Step |
| --- | --- | --- | --- | --- | --- |

## Knowledge Sources Used
| Source | Status | Why It Matters |
| --- | --- | --- |

## Open Questions
| ID | Question | Why It Matters | Options | Required Before |
| --- | --- | --- | --- | --- |

## Exit Criteria
- [ ] MVP scope confirmed
- [ ] High-impact decisions confirmed or explicitly deferred
- [ ] Acceptance direction is clear
```

## Exit Criteria

Discovery Gate can exit only when:

- The recommended MVP or current change scope is confirmed.
- Blocking open questions are resolved.
- High-impact decisions are `Confirmed` or `Deferred` outside the current MVP.
- The user agrees the discovery can be turned into a spec.

## Intake Output

Before writing files, present an intake summary:

```text
## Change Intake
- Current understanding:
- Missing / unconfirmed facts:
- Proposed MVP direction:
- Recommended change id:

## Required Questions
1. Project context:
2. Core scope:
3. Technical preferences:
4. Constraints and acceptance:

## Next Step
Please confirm or correct the answers. I will create SDC change files only after confirmation.
```

If the user says "use your judgment", record the proposed path as `Proposed` or `Assumed`. Do not treat it as confirmed.
