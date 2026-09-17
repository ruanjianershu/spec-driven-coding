# Discovery Gate

Discovery converges uncertain requirements into a small, verifiable change. Load this reference for intake, unresolved business requirements, or a return to discovery, not to repeat an interview the user has already completed.

## Evidence-Backed Change Intake Gate

Before change-file writes, cover four categories and establish authorization. Coverage is mandatory; asking four new questions is not.

For a new `/sdc:change ...` request:

1. Summarize the requested scope and cite current or still-valid prior user/project confirmation.
2. Start with the knowledge index and relevant Common Ground/routing entries. Use current `ESTABLISHED` sources; `WORKING`, personal/native/project memory, and model inference remain Candidate or Proposed.
3. Use `product-discovery` and relevant domain/security/data lenses to identify gaps, not create facts.
4. Cover each category below with a cited source and scope, an evidence-based non-applicability reason, or a missing blocking question. Code can establish current technical behavior, not authorize new business policy.
5. Ask only missing blocking questions. Do not ask about irrelevant deadlines, databases, or deployment preferences for a bounded wording change.
6. Cite explicit authorization before writes; existing valid approval satisfies this gate. If authority is missing, ask and wait. An explicit request to persist discovery permits only minimal discovery artifacts while business requirements remain open.
7. Make risk and authorization visible; consult `workflow-standards.md` for internal `light` / `standard` / `strict` triggers, delegation, and freshness. Risk level never converts uncertainty into consent.

Required intake categories:

- Project context: greenfield or existing codebase, solo/team, target users.
- Core scope: must-have vs nice-to-have, MVP boundary, non-goals.
- Technical preferences: language, framework, database, platform, deployment.
- Constraints and acceptance: deadline, budget, integrations, compliance/security, how done will be proven.

Options remain `Proposed` until authoritative confirmation or selection within bounded explicit delegation. Delegation must name the decision area, allowed choices/constraints, impact limits, and stopping boundary; record the selected option and approving source. Generic "use your judgment" cannot supply unknown business requirements or grant blanket consent.

## Artifact Budget While Discovery Is Open

When any blocking Open Question remains, keep artifacts minimal:

- Default: ask only missing blocking questions in chat, without a fixed count.
- With persistence authorization, create or update only `discovery.md`, plus an optional Draft `proposal.md` and brief `notes.md`. The internal lifecycle record may track discovery but cannot declare its own confirmation.
- Do not create or update `spec.md`, `design.md`, `tasks.md`, `impact.md`, `context-pack.md`, or `knowledge-candidates.md` while Discovery Gate is open, including speculative drafts.
- Do not output a large task list, API design, database schema, or implementation plan while Discovery Gate is open.
- Do not ask every possible question. Ask only the questions required to close the next decision gate.
- Keep research scratch in `.sdc/runtime/<change-id>/research/` and citations in discovery/notes; candidate files are available only after discovery closes.
- Unknown business requirements belong only in discovery, not in spec/design/tasks or tasks disguised as investigations.

## When To Continue Discovery

After intake confirmation, continue Discovery Gate when any of these remain unresolved:

- Target user or affected actor.
- Business goal.
- In-scope and out-of-scope boundary.
- Main scenario or failure scenario.
- Acceptance direction.
- High-impact decision status.
- Whether the request should be one change or several changes.
- Any relevant Common Ground item is still `OPEN`.
- Any high-impact Common Ground item is only `WORKING`.

Do not produce a `Confirmed` spec, final plan, or implementation tasks while Discovery Gate is open.

Questions needed for current scope or acceptance are blockers unless explicitly deferred outside the current MVP without weakening acceptance. Unrelated open questions do not block this change. Draft discovery may mention gaps, but they must not become REQ/AC, design decisions, or tasks.

## Explicit Confirmation Gate

Interpretation summaries are not consent.

Forbidden write-ahead patterns:

- "If this is wrong, tell me; I will update the files now."
- "I will assume X and proceed unless you object."
- "如有偏差请告知，我先按这个更新。"
- "如果不对告诉我，我先改。"

When existing explicit authorization does not cover the action:

1. State the interpretation as `Proposed`.
2. Ask a yes/no or option-selection confirmation question.
3. Wait for the user's answer.
4. Write durable artifacts only after confirmation.

When authorization already covers a bounded reversible action, cite it and proceed within its boundaries. Scope, data, permissions, public contracts, architecture, and other high-impact decisions still require authoritative confirmation or bounded explicit delegation; a stage/session change alone does not require asking again.

## Discovery Method

Use a lightweight sequence:

1. Restate only what the user has actually said.
2. Identify missing facts and high-impact decisions.
3. If the user has not selected a direction, offer 2-3 candidate directions and mark them `Proposed`.
4. Recommend a smallest viable change slice.
5. Ask only missing blocking questions when more discovery is required.
6. Record decisions in `discovery.md`.
7. Exit only when the MVP and blockers are confirmed or explicitly deferred.

## Required Output In `discovery.md`

```markdown
# Discovery

## Current Understanding

## Intake Coverage
| Category | Confirmed Understanding / Gap | Source And Scope | Blocking? |
| --- | --- | --- | --- |
| Project context | | | |
| Core scope | | | |
| Technical preferences | | | |
| Constraints and acceptance | | | |

## Authorization And Risk
- Approving source, authorized action, constraints, and stopping boundary:
- Risk level, triggers, evidence, and rationale:

## Candidate Directions
| Option | Description | Pros | Cons | Status |
| --- | --- | --- | --- | --- |

## Tradeoffs

## Recommended MVP

## Decision Ledger
| ID | Decision | Status | Source | Impact | Next Step |
| --- | --- | --- | --- | --- | --- |

## Knowledge Sources Used
| Source | Status | Verified Against | Scope | Why It Matters |
| --- | --- | --- | --- | --- |

## Open Questions
| ID | Question | Why It Matters | Options | Required Before |
| --- | --- | --- | --- | --- |

## Exit Criteria
- [ ] MVP scope confirmed
- [ ] High-impact decisions confirmed or explicitly deferred
- [ ] Acceptance direction is clear
- [ ] Authorization to produce the spec is cited
```

## Exit Criteria

Discovery Gate can exit only when:

- The recommended MVP or current change scope is confirmed.
- Blocking open questions are resolved.
- High-impact decisions are `Confirmed` or `Deferred` outside the current MVP.
- Explicit authorization to turn discovery into a spec is cited; prior approval is reusable when still valid.

If later evidence changes business requirements or their authority, stop dependent execution and explicitly reopen to discovery with a reason. Preserve old artifacts and approvals as history, not execution inputs. For planning-only revisions with requirements still confirmed, use the confirmed-state reopen path. See `runtime-context.md` for mechanics; editing a state label cannot close discovery.

## Intake Output

Before writing files, present an intake summary:

```text
## Change Intake
- Current understanding:
- Four-category coverage with cited confirmation or non-applicability:
- Missing blocking questions (omit if none):
- Proposed MVP direction:
- Recommended change id:

- Authorization source and boundaries:
- Risk level, triggers, and evidence plan:

## Next Step
State the next authorized step, or the specific confirmation needed before writing.
```

Cite an identifiable user statement or authoritative project section/revision, not "already discussed". Keep the summary proportional to the request and act on valid prior approval without repeating answered questions.
