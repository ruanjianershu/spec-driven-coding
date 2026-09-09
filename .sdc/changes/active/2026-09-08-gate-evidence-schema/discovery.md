# Discovery

## Knowledge Sources Used

| Source | Status | Evidence | Why It Matters |
|---|---|---|---|
| ANDY-143 / ANDY-151 issue inputs | Confirmed | Assigned scope and Layout A decisions | Define the local-only Gate Evidence contract and its boundaries. |
| ANDY-157 issue input | Confirmed | Root-cause statement and completion conditions | Requires a clean-base rebuild of the plan without an invented runtime dependency. |
| ANDY-157 independent revalidation | Confirmed | Persistent, independently readable review-object requirement | Requires a portable plan-delivery object instead of an executor-local-only commit. |
| `origin/main@e10a5d221f081fb6d099d342597a707b0dad91c9` | Confirmed | `git fetch origin main`; `git rev-parse origin/main` | Supplies the only implementation baseline. |
| Base `sdc-cli.py` | Confirmed | `cmd_validate` and active-change validation | Provides the supported plan validation entrypoint. |
| Base `scripts/sdc-task-brief.py` and `scripts/sdc-review-package.py` | Confirmed | Tracked release helpers and source inspection | Provide the existing ignored task-handoff format; neither creates JSON manifests or lifecycle state. |
| Base `artifact-schemas.md` and `execution-orchestration.md` | Confirmed | Runtime scratch and durable-evidence rules | Define the supported Markdown handoff/ledger boundary. |

## Current Understanding

This focused Brownfield change defines one versioned local Markdown Gate Evidence contract and one direct local fail-closed test.  Its executable plan begins from the exact Base and uses only interfaces present there: `python3 sdc-cli.py validate <change>` validates the nine Markdown change artifacts; `scripts/sdc-task-brief.py <change> <T###>` and `scripts/sdc-review-package.py <base> <head> <change> <label>` create ignored task/review handoffs.  The nine-file plan package is delivered as a portable Git bundle with a recorded SHA-256 digest, then locally verified and imported by T000; this is plan transport, not a runtime-context interface.

The Base does not contain `scripts/sdc-runtime-context.py`, `sdc.change-state/v1`, or `sdc.context-manifest-record/v1`.  They are excluded from this change rather than reconstructed from a divergent worktree.  The change does not implement a Gate-Closed profile, change runtime/default command behavior, authenticate an external system, merge, deploy, publish, or release.

## Decision Ledger

| ID | Decision | Status | Source | Impact | Next Step |
|---|---|---|---|---|---|
| DEC-GE-001 | Use Layout A: `Status: Closed`; separate Resolution and Closure ID/source pairs. | Confirmed | ANDY-151 decision input | Fixes exact field names and closed value. | Carry into the specification and direct test. |
| DEC-GE-002 | IDs use lowercase `8-4-4-4-12` hexadecimal textual UUID form. | Confirmed | ANDY-143 / ANDY-151 inputs | Fixes accepted identifier shape. | Test accepted and rejected forms. |
| DEC-GE-003 | Each named source occurs once and is nonempty after trimming; the target is not parsed or authenticated. | Confirmed | ANDY-151 decision input | Defines local provenance consistency. | Test absent, duplicate, and whitespace-only fields. |
| DEC-GE-004 | The proof remains a direct local test and does not change `sdc-cli.py`, profiles, packages, or public commands. | Confirmed | ANDY-143 scope and Base inspection | Preserves the implementation boundary. | Stop for plan revision if a broader surface is needed. |
| DEC-GE-005 | Every implementation/review check names the exact Base and one full candidate SHA. | Confirmed | ANDY-151 completion conditions | Makes review reproducible. | Record the full SHA before independent review. |
| DEC-GE-006 | T000 uses the Base-supported Markdown package validator and ignored task/review handoffs; it does not generate JSONL manifests or lifecycle state. | Confirmed | ANDY-157 root cause; Base helper and schema inspection | Removes the contradictory dependency without expanding runtime scope. | Verify the clean-base dry run in T000. |
| DEC-GE-007 | T000 receives the exact nine-file plan revision through a portable Git bundle whose digest, revision, Base ancestry, and complete sorted fixed path set are verified locally before import. | Confirmed | ANDY-157 independent revalidation requirement; isolated replay finding | Makes the review object independently retrievable without a remote push or a runtime dependency. | Verify digest, bundle, commit, ancestry, and equality of the complete `Base..revision` changed-path list to the fixed nine paths in T000. |
| DEC-GE-008 | Shell verification uses `set -o pipefail` and braces a revision before a Git path colon as `${BASE}:path`. | Confirmed | ANDY-157 independent replay evidence in zsh | Prevents a failed `git show` from being masked by the validator pipeline. | Exercise valid and invalid Base paths before Preflight passes. |
| DEC-GE-009 | After the verified archive import, T000 stages only the fixed package directory and creates committed `H0` before Base validation and helper handoff. | Confirmed | ANDY-157 isolated replay of exact Base | Converts the approved source package into the clean candidate that later checks review. | Verify the staged path set and committed `H0` in T000. |

## Open Questions

| ID | Question | Why It Matters | Options | Required Before |
|---|---|---|---|---|

No acceptance-relevant question remains for this local documentation/test slice.  A human Apply authorization is an execution gate, not a design input.

## Artifact Output Contract

| Output | Status | Trigger | Needed Before | Notes |
|---|---|---|---|---|
| Process / State Diagram | N/A | `Status` is a record field | plan | N/A because no product workflow or runtime state machine changes. |
| Sequence / Integration Diagram | N/A | No integration is allowed | plan | N/A because the test makes no external call. |
| API / Contract Specification | Required | Versioned Markdown contract | plan | `design.md#gate-evidence-contract` defines the exact local interface. |
| Data Model / Migration Contract | N/A | No persistent data change | plan | N/A because the Markdown standard is not stored application data. |
| UX Flow / Interaction States | N/A | No user interface change | plan | N/A because this change has no UI surface. |
| Test Matrix | Required | Fail-closed acceptance proof | plan | `design.md#test-matrix` maps valid and invalid local records to ACs. |
| Deploy / Release Checklist | N/A | No deployment or release action | plan | N/A because deployment, publishing, and release remain outside scope. |
| AI Involvement Note | Required | AI-assisted delivery | plan | Requires human Apply confirmation and independent review. |

## Exit Criteria

- [x] The local-only MVP scope is confirmed.
- [x] The Layout A fields, ID shape, closed value, and source predicate are confirmed.
- [x] The clean Base and its supported validator/handoff boundaries are confirmed.
- [x] The acceptance direction for valid and fail-closed records is confirmed.
