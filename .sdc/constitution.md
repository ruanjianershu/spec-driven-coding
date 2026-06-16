# SDC Project Constitution

## 1. Governance Priority

`.sdc/constitution.md > AGENTS.md > conversation instructions`

If these sources conflict, stop and produce a Stop-Line Report.

## 2. Fact Priority

`discovery.md > spec.md > impact.md > design.md/plan.md > tasks.md > code`

Code is evidence of current behavior, but it does not automatically override the agreed spec.

## 3. Knowledge and Memory Discipline

`.sdc/knowledge/` stores confirmed project knowledge. It is the shared project brain for product facts, domain rules, technical architecture, interfaces, operations, and validation commands.

`.sdc/memory/` stores project memory and knowledge candidates. Memory is useful for recall and continuity, but it cannot override confirmed knowledge, current specs, user confirmation, or code evidence.

Before writing a final spec, plan, task list, or implementation, read `.sdc/knowledge/index.md` and the relevant product/technical knowledge files. If the current change contradicts existing knowledge, record the conflict in the Decision Ledger and stop until it is confirmed.

No Evidence, No Fact. No Confirmation, No Execution. No Impact, No Brownfield Change.

Every durable knowledge item must record Status, Source, Verified At, Verified Against, and Scope. Missing evidence creates a Knowledge Gap; it does not authorize guessing.

Assumptions may be recorded only in discovery, Decision Ledger, or knowledge-candidates. `Assumed`, `Proposed`, `TBD`, `Conflict`, `Stale`, and open Knowledge Gaps must not drive final spec, design, context-pack, tasks, impact, apply, or archive.

For Brownfield/Legacy technical knowledge, code/config/test/build/runtime evidence is required. README files, comments, old docs, and memory are clues only.

## 4. Common Ground And Expert Routing Discipline

`.sdc/common-ground.md` records the shared project understanding. It separates:

- ESTABLISHED: confirmed facts that can drive final artifacts.
- WORKING: evidence-supported interpretations that require citation and cannot silently become truth.
- OPEN: unresolved questions or assumptions that block final artifacts when they affect scope, acceptance, data, permissions, architecture, security, rollout, or compatibility.

`.sdc/expert-routing.md` records how SDC selects internal expert lenses without adding public commands. Expert profiles can suggest questions, checks, and investigation tasks, but they cannot create unconfirmed product rules, architecture choices, data models, permissions, or rollout policies.

Before non-trivial change, spec, plan, apply, check, or archive work, read `common-ground.md` and the relevant routing entries in `expert-routing.md`.

## 5. Artifact Output Contract Discipline

Every confirmed change must record an Artifact Output Contract before final plan/apply/check.

Triggered outputs include process/state diagrams, sequence/integration diagrams, API/contract specifications, data/migration contracts, UX flow/states, Test Matrix, deploy/release checklist, and AI involvement note.

Rules:

- Discovery may keep the output contract Draft/Proposed.
- Final spec/design/context-pack must include the confirmed output contract.
- Required outputs must point to a concrete section or file.
- N/A outputs must include an evidence-based reason.
- Test Matrix is required for final plan/check and must map validation back to ACs.
- Output contracts cannot create unconfirmed product rules, schemas, permissions, rollout policy, or integrations.

## 6. Core Chain

`discovery -> spec -> impact -> plan -> tasks -> code -> verify -> archive`

## 7. Stop-The-Line Rules

Stop and produce a Stop-Line Report when:

- spec, design, or tasks are missing, conflicting, or not verifiable
- implementation requires changing business behavior, public contract, acceptance criteria, or key technical decisions
- current task requires scope expansion
- validation cannot prove the acceptance criteria
- required knowledge sources are missing, stale, or contradict the current change
- final artifacts contain unclosed Knowledge Gaps or unconfirmed assumptions
- final artifacts depend on OPEN or high-impact WORKING Common Ground
- the implementation touches a risk area without the matching expert profile or standards review
- a triggered output artifact is missing, contradictory, or marked N/A without evidence

## 8. Traceability Rules

- specs must define `SCN-*`, `REQ-*`, and `AC-*` identifiers
- tasks must reference `REQ-*` and `AC-*`
- tests or validation notes must reference `AC-*`
- implementation notes must record validation evidence
- specs, designs, plans, and context packs must list the knowledge sources and expert profiles they used
- specs, designs, and context packs must include Artifact Output Contract coverage

## 9. Human Confirmation Rules

AI may propose options, but humans own high-impact decisions.

High-impact decisions include product rules, permissions, state machines, approval flows, reminder behavior, technology stack, architecture, data model, authentication, locking, deletion, migration, rollout, and security policy.

Before a high-impact decision enters `REQ-*`, `AC-*`, `INV-*`, `design.md`, or `tasks.md`, it must be one of:

- explicitly confirmed by the user
- supported by an authoritative project document
- explicitly delegated by the user with permission to choose

## 10. No Silent Defaults

Do not turn common practice into project truth.

All AI-created defaults must be recorded in a Decision Ledger as `Proposed` or `Assumed` until confirmed. `Proposed`, `Assumed`, `TBD`, and `Conflict` items must not be treated as implementation-ready.

## 11. Discovery Gate

When requirements are uncertain, start with discovery instead of a confirmed spec.

Discovery must record current understanding, candidate directions, tradeoffs, recommended MVP, open questions, and a Decision Ledger. A confirmed spec can only be produced after the current MVP scope and high-impact decisions are confirmed or explicitly deferred.

While Discovery Gate is open, keep artifacts minimal: `discovery.md`, optional Draft `proposal.md`, and brief `notes.md` only. Do not create or update `spec.md`, `design.md`, `tasks.md`, or `impact.md` until the MVP, acceptance direction, and high-impact decisions are confirmed or explicitly deferred.

Interpretation summaries are not consent. Do not write files with "if wrong, tell me" or "如有偏差请告知，我先改". Mark the interpretation as `Proposed` or `Assumed`, ask for explicit yes/no or option confirmation, wait for the user, then write durable artifacts.
