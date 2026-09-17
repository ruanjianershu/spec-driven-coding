# Changelog

All notable changes to SDC are documented here.

## Unreleased

- Fixed interrupted-validation recovery while preserving prior receipts; reject unsupported Git submodules instead of silently omitting source evidence.
- Fixed installed workflow helper paths and bundled runtime dependencies for direct-skill layouts; added isolated installation and retry regressions.
- Guarded public packages against private workspace/standards payloads and internal bootstrap links while retaining the installed `sdc validate` dispatcher.
- Added content gates for confirmation/planning, input/source snapshots, fresh manifest verification, idempotent state retries, and explicit revision/replanning with preserved history. Legacy unbound approvals require revalidation.
- Added bounded actual-command receipts and attributed review receipts tied to revision and source snapshots. Delivery checks reject stale runs, later failures, command mismatches, and status assertions without execution evidence.
- Replaced fixed intake question counts with evidence-backed coverage, bounded authorization, risk-proportionate effort, selective context, and incremental knowledge refresh without new public commands.
- Added explicit opt-in Codex native hook packaging (`SDC_CODEX_HOOKS=1`) while retaining portable default behavior and user-controlled hook trust.
- Added isolated real-agent evaluation tooling alongside deterministic regression tests; real trials and mock harness tests are reported separately.
- Added a Trellis-inspired local runtime with the evidence-gated lifecycle `intake -> discovery -> confirmed -> planned -> applying -> checking -> archivable`.
- Added exact-one active-change resolution using explicit argument, `SDC_ACTIVE_CHANGE`, local session pointer, then sole active directory; invalid, missing, or ambiguous targets stop without recency-based guessing.
- Added deterministic plan-generated `apply-context.jsonl` and `check-context.jsonl` manifests while retaining the human-readable `context-pack.md`.
- Added bounded local read-only memory recall whose results are always `Candidate`, plus internal research routing through runtime scratch, cited notes, and archive-gated knowledge candidates without a new public command.
- Added an optional Claude `SessionStart` adapter with safe manual fallback and a portable-by-default Codex skill adapter.
- Made the repository root a strict-valid Claude marketplace by explicitly selecting the existing advanced `skills/sdc-*` paths; local installs no longer require a generated `.claude/skills/` compatibility tree.
- Hardened lifecycle and archive gates so completed tasks, task reviews, final review evidence, full state provenance, and safe non-symlink workspace paths are revalidated before mutation.
- Restricted recall to each allowlisted root, added credential-shaped and high-entropy rejection/redaction for recall and runtime evidence, and made Claude hook payload identity authoritative over opt-in environment fallback.
- Updated privacy, security, release validation, and Trellis design-provenance documentation to match the local runtime behavior.

## 1.3.0 - 2026-07-11

- Added an internal Execution Orchestration Contract without adding public commands: exact Global Constraints, Plan Preflight, task interface contracts, file-based handoffs, project-local runtime ledger, per-task Spec Compliance + Code Quality review, and final whole-change review.
- Added `sdc-task-brief.py` and `sdc-review-package.py` helpers so implementers and reviewers exchange focused files instead of repeatedly pasting full plans, reports, and diffs into controller context.
- Strengthened CLI validation so missing task interfaces, failed preflight, completed tasks without approved review/evidence, inconsistent progress ledger, and missing final whole-change review block delivery and archive.
- Added Codex marketplace metadata under `.agents/plugins/marketplace.json`, explicit `hooks: {}`, Developer Tools classification, Interactive capability, and deterministic Codex portal packaging with SHA-256 output.
- Made the Codex portal artifact rootless and runtime-only, excluding Claude/source-side files while preserving executable modes and byte-identical rebuilds.
- Added npm packaging guards so generated Python caches cannot leak into published tarballs.
- Moved shared English contracts out of `skills/` into `sdc-references/`, so every Codex skill directory is a valid invocable skill without exposing an internal `sdc-shared` entry.
- Added `npm run sync:skills` and committed generated public workflow skills so the repo-local Codex marketplace installs the complete workflow while Claude packages continue to strip root skills and avoid duplicates.
- Added safe existing-workspace migration that appends `/runtime/` to `.sdc/.gitignore` without replacing project-specific ignore rules.
- Changed delivery checks so a missing git-ignored recovery ledger warns on fresh checkouts, while a present ledger is parsed by columns and must agree with durable task/review/evidence state.
- Fixed task-interface parsing so empty fields cannot consume the following Markdown line and silently pass validation.
- Added exact Global Constraints table validation and cross-artifact consistency checks, plus Plan Preflight source/finding validation.
- Tightened Plan Preflight closure parsing so uncertain values such as `Resolved?` cannot pass as closed findings.
- Made Plan Preflight status exact, validated current-plan constraint tables, rejected malformed constraint IDs and duplicate task IDs, and aligned the canonical task example with every required 1.3 field.
- Closed adjacent validator bypasses by requiring exact context-pack preflight/final-review markers and at least one valid uppercase `T###` task.
- Replaced keyword-first execution parsing with unique exact fields: every task checkbox must be valid, runtime paths must resolve to the active change, review contracts cannot use negated wording, and duplicate task/preflight/verdict fields block delivery.
- Enforced document-level uniqueness for Global Constraints, Plan Preflight, Execution Orchestration, per-task review blocks, and Final Whole-Change Review so a second contradictory section cannot be ignored.
- Stopped Codex local marketplace/cache installs from generating Claude-only `.claude/skills`, keeping hidden-path scans at the intended 14 Codex skills and preventing future duplicate discovery.
- Added machine-readable per-task and final Spec Compliance / Code Quality verdicts with project-local, non-ignored, resolvable Evidence references.
- Made WORKTREE review packages fail when untracked files would be omitted from the diff.
- Made Codex plugin upgrades transactionally replace stale layouts with rollback and next-run recovery, so old `skills/sdc-shared/` directories cannot survive an update and interrupted swaps retain a recoverable copy.
- Serialized implementation tasks through review and ledger completion to match the Superpowers v6 execution sequence.
- Added SHA-256 ownership fingerprints for SDC-managed workspace files; modified project rules are preserved, while exact known 1.2.x templates remain safely upgradeable with backups.
- Added deterministic eval scenarios for task-interface enforcement, review-gated completion, runtime-ledger portability/consistency, execution handoff helpers, existing-workspace runtime migration, and Codex portal packaging.
- Added Artifact Output Contracts so change/plan/check/validate can require triggered enterprise delivery outputs such as diagrams, API/data contracts, test matrices, release checklists, and AI involvement notes without adding public commands.
- Fixed Common Ground validation so `OPEN` and final-execution `WORKING` Common Ground rows now block validate/apply/archive readiness instead of passing as documentation-only warnings.

## 1.2.1 - 2026-06-15

- Added SDC Common Ground: projects now initialize `.sdc/common-ground.md` to keep `ESTABLISHED / WORKING / OPEN` assumptions visible and block OPEN/high-impact WORKING assumptions from final execution.
- Added internal Expert Routing: projects now initialize `.sdc/expert-routing.md` so SDC can use specialist product, domain, legacy, architecture, API, data, frontend, backend, test, security, operations, and documentation lenses without adding public commands.
- Added shared English references for `common-ground`, `expert-routing`, and a machine-readable workflow manifest.
- Updated init, change, spec, plan, apply, validate, review, test, quality, check, archive, harness, README, schemas, and gates to read Common Ground and Expert Routing at the right stages.
- Updated context-pack and validation rules to include `Common Ground Used` and `Expert Profiles Used`.
- Updated archive Knowledge Compact Gate to recommend confirmed Common Ground and Expert Routing updates as conditional durable project assets.
- Fixed Codex/Hermes local installs so public workflow skills are generated from command definitions while Claude Code continues to expose those workflows only as slash commands.
- Added company/team standards pack support: `sdc init --standards <path>` and `sdc standards import <path>` import private rules into `.sdc/standards/company/` with a routing index and no bundled private content.

## 1.2.0 - 2026-06-01

- Added a first-class project knowledge system under `.sdc/knowledge/`, split into product knowledge and technical knowledge with a short `knowledge/index.md` routing file.
- Added `.sdc/memory/` for candidate knowledge, reusable procedures, and episodic summaries; memory is explicitly lower authority than confirmed knowledge.
- Added `context-pack.md` and `knowledge-candidates.md` to confirmed change flows so execution agents receive short handoffs and archive can promote durable knowledge intentionally.
- Updated init, change, plan, apply, check, validate, archive, shared references, README, and marketplace docs to enforce knowledge-source reading, candidate-vs-confirmed boundaries, and archive-time knowledge compaction.
- Added deterministic SDC flow evals under `evals/sdc-flow/` plus `npm run eval:sdc`, with an optional promptfoo config for CI environments that support promptfoo.
- Added anti-guess execution gates: unconfirmed assumptions, open Knowledge Gaps, and incomplete knowledge candidates now block validate/apply/archive readiness.
- Expanded safe `sdc init` repair so stale managed constitution, discovery, design, context-pack, and knowledge-candidate templates are backed up and upgraded to the current evidence schema.

## 1.1.10

- Fixed the remaining Claude Code duplicate UX where public slash commands such as `sdc:apply` still appeared beside equivalent plugin skills such as `sdc:sdc-apply`.
- Claude Code now exposes public workflows only as slash commands; Claude skills are limited to advanced non-public capabilities: spec, implement, review, test, quality, and validate.
- Made Claude public command prompts self-contained instead of referencing backing skills that are intentionally not exposed in Claude.
- Updated installer, release audit, and docs to prevent public command backing skills from being generated in Claude `.claude/skills/`.

## 1.1.9

- Fixed Claude Code duplicate command/skill registration by generating Claude skill directories with `sdc-*` names instead of short command aliases.
- Changed the Claude plugin manifest to declare skills explicitly as an array, so public slash commands such as `/sdc:init` do not collide with same-named plugin skills.
- Updated installer and release audit checks to prevent short Claude skill alias directories from returning.

## 1.1.8

- Changed Codex installation to plugin-first by default and clean stale `~/.agents/skills/sdc-*` and `~/.codex/plugins/sdc` direct installs to avoid duplicate SDC entries.
- Added `SDC_CODEX_DIRECT_SKILLS=1` as an explicit legacy fallback for older Codex builds that only scan direct skills.
- Fixed CLI validation so confirmed Greenfield changes can proceed without `impact.md`; Brownfield/Unknown changes still require it.
- Fixed `sdc validate` and `sdc check` exit codes so structural validation errors return a non-zero status for scripts and CI.
- Split installer completion guidance by platform so Codex users are not told to expect `/sdc:*` slash commands.
- Aligned the command model so Codex declares skills only, Claude exposes only public slash commands, and detailed controls remain skills.
- Strengthened CLI validation for confirmed changes: confirmed specs must not be Draft, design.md is checked, common template placeholders are rejected, and impact.md accepts the English Change Impact Gate schema.
- Fixed Claude local install fallback so the generated marketplace is written even when the `claude` CLI is unavailable, without leaving a direct root plugin copy.
- Added a release audit script to catch version drift, command exposure drift, Codex slash-command drift, stale schema strings, and README command-model drift before publishing.
- Clarified Brownfield analysis layering: project cognition is reusable repo memory, while each confirmed change gets a focused `impact.md`; full repo cognition is refreshed only when stale, incomplete, structurally changed, or explicitly requested.
- Added positioning guidance: SDC's strongest value is safe Brownfield/Legacy iteration, while Greenfield projects benefit from early specs, standards, traceability, and test discipline.
- Added Knowledge Compact Gate inside archive so completed changes recommend the right durable updates to specs, archive history, decisions, standards, reports, AGENTS.md, project context, or project cognition without adding another public command.
- Hardened CLI archive behavior: archive now runs validation first, blocks Draft specs, unchecked tasks, existing stable specs, and existing archive directories, and writes a correct archived spec relative link.
- Updated README and release checklist with Codex duplicate-skill verification.

## 1.1.7

- Aligned spec templates with the current schema by adding explicit `INV-*` business invariant placeholders and schema metadata.
- Updated validation to require `INV-*` alongside `SCN-*`, `REQ-*`, and `AC-*`.
- Added safe init repair for stale SDC-generated templates: old managed templates are upgraded with `.bak-*` backups instead of being left to fail later validation.
- Clarified Discovery Open versus Discovery Closed active change structures.

## 1.1.6

- Added Discovery Artifact Budget: unresolved requirements now stay in `discovery.md`, optional Draft `proposal.md`, and brief `notes.md` instead of generating full `spec.md`, `design.md`, `tasks.md`, or `impact.md`.
- Added No Write-Ahead Confirmation rules to forbid "if wrong, tell me, I will update now" as authorization.
- Strengthened Decision Ledger gates so high-impact inferences remain `Proposed` or `Assumed` until explicit confirmation.
- Updated CLI `sdc change` to create a minimal Discovery Open draft by default.
- Updated validation to flag full artifacts created before Discovery Gate exits.

## 1.1.5

- Fixed Claude Code local marketplace packaging so it exposes only `.claude/skills/` and no longer registers duplicate root `skills/` entries.
- Kept Codex and Hermes skill packaging unchanged.
- Added release checklist coverage for duplicate skill registration.

## 1.1.4

- Added English Role Prompt Contracts to every SDC skill.
- Standardized each contract around Role, Operating Contract, Evidence Rules, and Output Contract.
- Strengthened expert persona behavior without adding new public commands.
- Updated README, docs, package metadata, and plugin metadata for the role contract upgrade.

## 1.1.3

- Added Brownfield/Legacy project cognition during init through `project-cognition.md`.
- Clarified that legacy change impact analysis happens after requirements are confirmed inside the current change, not during init.
- Added per-change `impact.md` generation and Change Impact Gate before plan/apply for legacy projects.
- Updated review/check to include final old-system modification and impact analysis for legacy deliveries.
- Expanded CLI/templates/docs/metadata for legacy project cognition and confirmed-requirement impact analysis.

## 1.1.2

- Added Discovery Gate as the built-in requirement exploration phase inside `/sdc:change`.
- Added `discovery.md` templates to init and change workspaces for current understanding, candidate directions, tradeoffs, recommended MVP, Decision Ledger, open questions, and exit criteria.
- Updated `/sdc:spec` to consume `discovery.md` and refuse Confirmed specs while blocking discovery questions or high-impact decisions remain unresolved.
- Documented the command model: `change` is the normal entry point, `spec` is the specification refinement inside a change.

## 1.1.1

- Added consent gates to prevent AI-generated assumptions from becoming confirmed requirements or implementation tasks.
- Added Brainstorm-first and Decision Ledger rules to `/sdc:spec`.
- Added Technical Consent Gate and MVP Slice Gate to `/sdc:plan`.
- Updated `/sdc:validate` and `/sdc:check` to flag unconfirmed decisions, silent defaults, and over-large task plans.
- Updated constitution, harness, README, and discipline docs with Human Confirmation and No Silent Defaults rules.

## 1.1.0

- Added the SDC discipline core: governance priority, fact priority, traceability chain, and Stop-Line Report rules.
- Upgraded `/sdc:init` to generate `.sdc/constitution.md`, current tasks, reports, and templates for bug, impact, repo analysis, and stop-line reports.
- Upgraded `/sdc:spec`, `/sdc:plan`, `/sdc:apply`, `/sdc:validate`, `/sdc:check`, `/sdc:archive`, and `/sdc:harness` to preserve `SCN -> REQ -> AC -> T### -> evidence` traceability.
- Extended `/sdc:check` with delivery, bug, impact, and repo/brownfield modes without adding new public commands.
- Added documentation for the v1.1 discipline core and updated README usage expectations.
- Included docs, security, privacy, and changelog files in local plugin copies created by the installer.

## 1.0.9

- Added Claude Code compatible `.claude/skills/` layout generation during install.
- Updated Claude plugin manifest to point to `./.claude/skills/` and `./commands/`.
- Renamed Claude command files to namespace-friendly names such as `commands/init.md`, producing `/sdc:init`.
- Added one-command uninstall support through `npx sdc-spec@latest uninstall`.
- Improved Codex and Claude installer cleanup behavior for stale local plugin copies.
- Documented Codex custom slash command limitation and Claude Code restart requirement.

## 1.0.8

- Added a valid Claude Code marketplace manifest.
- Updated Claude plugin metadata to current manifest schema.
- Installed SDC through Claude Code local marketplace flow.
- Added command files for Claude plugin namespace behavior.

## 1.0.7

- Added Codex local marketplace and plugin cache installation.
- Added Codex command files and plugin metadata.
- Synchronized SDC skills into Codex-discoverable skill locations.

## Earlier

- Introduced SDC core skills: init, change, spec, plan, apply, check, validate, review, test, quality, archive, and harness.
- Added `.sdc/` workspace initialization workflow.
- Added project standards generation under `.sdc/standards/`.
