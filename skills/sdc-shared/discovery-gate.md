# Discovery Gate

Discovery Gate is the SDC replacement for broad brainstorming. It borrows divergent thinking, but it must converge into a small, verifiable change.

## When To Enter

Enter Discovery Gate when any of these are unclear:

- Target user or affected actor.
- Business goal.
- In-scope and out-of-scope boundary.
- Main scenario or failure scenario.
- Acceptance direction.
- High-impact decision status.
- Whether the request should be one change or several changes.

Do not produce a `Confirmed` spec, final plan, or implementation tasks while Discovery Gate is open.

## Discovery Method

Use a lightweight sequence:

1. Restate only what the user has actually said.
2. Identify missing facts and high-impact decisions.
3. Offer 2-3 candidate directions when options are useful.
4. Recommend a smallest viable change slice.
5. Ask at most 3 key questions.
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

## Draft Change Summary

Before writing final artifacts, present a short draft:

```text
## Change Draft
- Background:
- Goal:
- Non-goals:
- Scope:
- Initial SCN:
- Initial REQ:
- Initial AC:
- Risks / assumptions:
- Discovery status: not needed / active / complete
- Recommended change id:
```

If the user says "use your judgment", record the proposed path as `Proposed` or `Assumed`. Do not treat it as confirmed.

