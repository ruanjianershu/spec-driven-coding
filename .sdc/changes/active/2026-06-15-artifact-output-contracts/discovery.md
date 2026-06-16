# Discovery

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| User confirmation in current thread | Confirmed | 用户确认“按照推荐方案升级” | Confirms scope and acceptance for this change |
| README.md | Confirmed | Current public workflow docs | Defines public command surface and user-facing positioning |
| skills/sdc-shared/workflow-standards.md | Confirmed | Existing SDC governance reference | Defines gate and stop-line behavior to extend |
| skills/sdc-shared/delivery-gates.md | Confirmed | Existing validate/check/archive reference | Defines where output contracts must be checked |
| sdc-cli.py | Confirmed | Current managed templates and validators | Primary implementation surface |
| Internal AI dev workflow page | Confirmed | User-provided internal reference reviewed in chat | Inspires explicit stage input/output standards |

## Knowledge Gaps

| Gap ID | Missing Knowledge | Why It Matters | Blocks | Next Step | Status |
|---|---|---|---|---|---|

## Input Evidence

| Source | Type | Status | Summary | Evidence / Link |
|---|---|---|---|---|
| User request | Product direction | Confirmed | SDC lacks mandatory output format while the internal workflow requires deliverables such as flow diagrams and technical design documents. | Current conversation |
| Existing SDC source | Code evidence | Confirmed | SDC already has flow gates, knowledge gates, expert routing, and validation hooks. | sdc-cli.py, skills/sdc-shared/* |
| Internal workflow reference | Comparative design input | Confirmed | Enterprise workflow uses explicit stage inputs/outputs and delivery artifacts. | User-provided internal page |

## Artifact Output Contract

| Output | Status | Trigger | Needed Before | Notes |
|---|---|---|---|---|
| Process / State Diagram | Confirmed | Workflow/state/approval requirements | plan/check | Triggered only when current change touches workflow/state logic |
| Sequence / Integration Diagram | Confirmed | Multi-service, async, event, queue, integration | plan/check | Required when interaction order matters |
| API / Contract Specification | Confirmed | API, endpoint, event, compatibility | plan/check | Required when contracts change |
| Data Model / Migration Contract | Confirmed | Schema, data, migration, transaction, locking | plan/check | Required when data behavior changes |
| UX Flow / Interaction States | Confirmed | UI, form, user-facing states | plan/check | Required for frontend/user-facing changes |
| Test Matrix | Confirmed | Every final change needs AC validation | plan/check | Must map validation back to AC |
| Deploy / Release Checklist | Confirmed | Deployment, config, rollback, runtime | check/archive | Required when runtime/release impact exists |
| AI Involvement Note | Confirmed | AI-assisted implementation or PR summary | check/archive | Required unless documentation-only and N/A is evidenced |

## Current Understanding

SDC should keep its small command surface, but add an explicit Artifact Output Contract layer. The contract defines what inputs each stage consumes and which standard outputs must exist when triggered. The output standard is implemented as shared English references, stage prompts, managed templates, CLI validation, deterministic evals, README docs, and release audit checks.

## Candidate Directions

| Option | Description | Pros | Cons | Status |
|---|---|---|---|---|
| Add many public commands | Expose requirement-analysis, tech-design, test-plan, deploy-checklist as separate commands | Mirrors internal workflow directly | Violates SDC simplification goal | Rejected |
| Add internal Artifact Output Contract | Keep public commands stable and route stage deliverables internally | Preserves simplicity while adding enterprise output standards | Requires template/eval/validator upgrade | Confirmed |
| Documentation only | Describe expected outputs in README | Low implementation cost | AI can still skip artifacts and validate may pass | Rejected |

## Tradeoffs

The contract must be strong enough to block missing deliverables, but not force every small change to generate large documents. Therefore optional outputs support `N/A + evidence reason`, while `Test Matrix` remains required for final plan/check because every change must prove acceptance criteria.

## Recommended MVP

Add `artifact-output-contracts.md`, update public workflow prompts and advanced skills, update templates and CLI validation, add one blocking eval for missing triggered output artifacts, and update README/changelog/metadata.

## Decision Ledger

| ID | Decision | Status | Source | Impact | Next Step |
|---|---|---|---|---|---|
| DEC-01 | Keep the public SDC command surface unchanged | Confirmed | User repeatedly prefers simplified SDC commands | Avoids command sprawl | Implement through shared reference and existing stages |
| DEC-02 | Add Artifact Output Contract as an internal stage layer | Confirmed | User prefers internal workflow's input/output standard | Makes deliverables explicit and validate-able | Add reference, templates, and gates |
| DEC-03 | Require Test Matrix for final plan/check | Confirmed | Acceptance evidence is always needed | Prevents vague validation | Enforce in CLI/evals |
| DEC-04 | Allow optional outputs to be N/A only with evidence reason | Confirmed | Avoids heavy docs for small changes | Keeps output standard proportional | Enforce in CLI validation |

## Open Questions

| ID | Question | Why It Matters | Options | Required Before |
|---|---|---|---|---|

## Exit Criteria

- [x] MVP scope confirmed
- [x] high-impact decisions confirmed or explicitly deferred
- [x] acceptance direction is clear
