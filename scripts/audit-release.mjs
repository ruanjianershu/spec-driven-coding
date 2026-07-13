#!/usr/bin/env node

import fs from 'fs';
import path from 'path';

const root = process.cwd();
const errors = [];

function readJSON(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), 'utf8'));
}

function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), 'utf8');
}

function fail(message) {
  errors.push(message);
}

function sameSet(actual, expected, label) {
  const actualSorted = [...actual].sort();
  const expectedSorted = [...expected].sort();
  if (JSON.stringify(actualSorted) !== JSON.stringify(expectedSorted)) {
    fail(`${label} mismatch. actual=${actualSorted.join(',')} expected=${expectedSorted.join(',')}`);
  }
}

const packageJson = readJSON('package.json');
const version = packageJson.version;
const versionSources = {
  'package.json': version,
  '.codex-plugin/plugin.json': readJSON('.codex-plugin/plugin.json').version,
  '.claude-plugin/plugin.json': readJSON('.claude-plugin/plugin.json').version,
  '.claude-plugin/marketplace.json': readJSON('.claude-plugin/marketplace.json').plugins?.[0]?.version,
};

for (const [file, fileVersion] of Object.entries(versionSources)) {
  if (fileVersion !== version) {
    fail(`${file} version ${fileVersion} does not match package.json ${version}`);
  }
}

if (packageJson.files?.includes('.claude/')) {
  fail('package.json files must not include root .claude/; installers generate platform-specific .claude/skills.');
}

if (!packageJson.scripts?.audit) {
  fail('package.json must expose npm run audit.');
}
if (!packageJson.scripts?.['eval:sdc']) {
  fail('package.json must expose npm run eval:sdc.');
}
if (!packageJson.scripts?.['package:codex']) {
  fail('package.json must expose npm run package:codex.');
}
if (!packageJson.scripts?.['sync:skills']) {
  fail('package.json must expose npm run sync:skills.');
}
if (!packageJson.files?.includes('.agents/')) {
  fail('package.json files must include the repo-local Codex marketplace manifest under .agents/.');
}
const expectedEvalFiles = [
  'evals/sdc-flow/README.md',
  'evals/sdc-flow/promptfooconfig.yaml',
  'evals/sdc-flow/run_sdc_flow.py',
  'evals/sdc-flow/sdc_flow_provider.py',
];
for (const evalFile of expectedEvalFiles) {
  if (!packageJson.files?.includes(evalFile)) {
    fail(`package.json files must include ${evalFile}.`);
  }
}
if (packageJson.files?.includes('evals/')) {
  fail('package.json files must list eval files explicitly so __pycache__ is not published.');
}
if (packageJson.files?.includes('scripts/')) {
  fail('package.json files must list scripts explicitly so __pycache__ is not published.');
}
for (const scriptFile of [
  'scripts/audit-release.mjs',
  'scripts/package-codex-plugin.py',
  'scripts/sdc-review-package.py',
  'scripts/sdc-task-brief.py',
]) {
  if (!packageJson.files?.includes(scriptFile)) {
    fail(`package.json files must include ${scriptFile}.`);
  }
}

const npmIgnore = readText('.npmignore');
for (const marker of ['**/__pycache__/', '**/*.py[cod]']) {
  if (!npmIgnore.includes(marker)) {
    fail(`.npmignore must exclude generated Python artifacts: missing ${marker}`);
  }
}

const publicCommands = ['sdc', 'init', 'change', 'plan', 'apply', 'check', 'archive', 'harness'];
const commandFiles = fs
  .readdirSync(path.join(root, 'commands'))
  .filter((name) => name.endsWith('.md'))
  .map((name) => name.replace(/\.md$/, ''));
sameSet(commandFiles, publicCommands, 'Claude public command files');

const publicWorkflowSkills = [
  { dir: 'sdc-core', name: 'sdc', command: 'sdc', skillDescription: 'Use when a development request must be routed through the SDC lifecycle.' },
  { dir: 'sdc-init', name: 'sdc-init', command: 'init', skillDescription: 'Use when a project needs an SDC workspace, project cognition, or standards import.' },
  { dir: 'sdc-change', name: 'sdc-change', command: 'change', skillDescription: 'Use when starting or clarifying a focused requirement change under SDC governance.' },
  { dir: 'sdc-plan', name: 'sdc-plan', command: 'plan', skillDescription: 'Use when a confirmed SDC change needs an executable design, task plan, and context handoff.' },
  { dir: 'sdc-apply', name: 'sdc-apply', command: 'apply', skillDescription: 'Use when an approved SDC plan is ready for implementation and evidence capture.' },
  { dir: 'sdc-check', name: 'sdc-check', command: 'check', skillDescription: 'Use when an SDC change needs validation, review, testing, quality, impact, or repository checks.' },
  { dir: 'sdc-archive', name: 'sdc-archive', command: 'archive', skillDescription: 'Use when a completed SDC change is ready for archival and durable knowledge compaction.' },
  { dir: 'sdc-harness', name: 'sdc-harness', command: 'harness', skillDescription: 'Use when project-level AI guardrails must be generated from SDC standards.' },
];
for (const workflow of publicWorkflowSkills) {
  const raw = readText(`commands/${workflow.command}.md`).replace(/\r\n/g, '\n');
  const match = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  const body = match ? match[2].trimStart() : raw;
  const skillBody = body.replace(/`sdc-references\//g, '`../../sdc-references/');
  const expected = `---\nname: ${workflow.name}\ndescription: ${JSON.stringify(workflow.skillDescription)}\n---\n\n> Codex/Hermes workflow skill generated from \`commands/${workflow.command}.md\`.\n> Treat the user's current request as \`$ARGUMENTS\`. In Codex/Hermes, route to the matching SDC skill/workflow instead of expecting \`/sdc:*\` slash-command support.\n\n${skillBody}`;
  if (readText(`skills/${workflow.dir}/SKILL.md`) !== expected) {
    fail(`skills/${workflow.dir}/SKILL.md is stale; run npm run sync:skills.`);
  }
}

const publicSkillDirs = ['sdc-core', 'sdc-init', 'sdc-change', 'sdc-plan', 'sdc-apply', 'sdc-check', 'sdc-archive', 'sdc-harness'];
const advancedSkills = ['sdc-spec', 'sdc-implement', 'sdc-review', 'sdc-test', 'sdc-quality', 'sdc-validate'];
const skillsDirEntries = fs
  .readdirSync(path.join(root, 'skills'), { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name);
const allowedSkillsDirEntries = [...publicSkillDirs, ...advancedSkills];
const unexpectedSkillEntries = skillsDirEntries.filter((name) => !allowedSkillsDirEntries.includes(name));
if (unexpectedSkillEntries.length > 0) {
  fail(`Source skills/ contains unsupported directories. unexpected=${unexpectedSkillEntries.join(',')}`);
}
const missingSkills = allowedSkillsDirEntries.filter((name) => !skillsDirEntries.includes(name));
if (missingSkills.length > 0) {
  fail(`Source skills/ is missing public or advanced skill directories: ${missingSkills.join(',')}`);
}

const sourceClaudeSkills = path.join(root, '.claude', 'skills');
if (fs.existsSync(sourceClaudeSkills)) {
  fail('Source repo must not contain .claude/skills/; the installer generates it from skills/. Ignore via .gitignore.');
}

const claudePlugin = readJSON('.claude-plugin/plugin.json');
const expectedClaudeSkills = [
  './.claude/skills/sdc-spec',
  './.claude/skills/sdc-implement',
  './.claude/skills/sdc-review',
  './.claude/skills/sdc-test',
  './.claude/skills/sdc-quality',
  './.claude/skills/sdc-validate',
];
if (!Array.isArray(claudePlugin.skills)) {
  fail('Claude plugin skills must be an explicit array, not a whole .claude/skills/ directory scan.');
} else {
  sameSet(claudePlugin.skills, expectedClaudeSkills, 'Claude plugin explicit skills');
}

const codexPlugin = readJSON('.codex-plugin/plugin.json');
if (Object.prototype.hasOwnProperty.call(codexPlugin, 'commands')) {
  fail('Codex plugin must be skill-plugin only and must not declare slash commands.');
}
if (JSON.stringify(codexPlugin.hooks) !== '{}') {
  fail('Codex plugin must declare hooks: {} to disable SessionStart auto-discovery fallback.');
}
if (typeof codexPlugin.author !== 'object' || !codexPlugin.author?.name) {
  fail('Codex plugin author must use the current object form with author.name.');
}
for (const legacyField of ['displayName', 'tags', 'min_codex_version']) {
  if (Object.prototype.hasOwnProperty.call(codexPlugin, legacyField)) {
    fail(`Codex plugin must not retain legacy top-level field: ${legacyField}`);
  }
}
if (!Array.isArray(codexPlugin.keywords) || !codexPlugin.keywords.includes('execution-orchestration')) {
  fail('Codex plugin keywords must describe the execution-orchestration capability.');
}
if (codexPlugin.interface?.category !== 'Developer Tools') {
  fail('Codex plugin category must be Developer Tools.');
}
if (!codexPlugin.interface?.capabilities?.includes('Interactive')) {
  fail('Codex plugin must declare Interactive capability.');
}

const codexMarketplace = readJSON('.agents/plugins/marketplace.json');
const codexMarketplaceEntry = codexMarketplace.plugins?.find((plugin) => plugin.name === 'sdc');
if (codexMarketplaceEntry?.source?.url !== './' || codexMarketplaceEntry?.category !== 'Developer Tools') {
  fail('Repo-local Codex marketplace must expose sdc from ./ as Developer Tools.');
}

const installJs = readText('bin/install.js');
if (installJs.includes('CodeX')) {
  fail('Use Codex spelling consistently; found CodeX in bin/install.js.');
}
if (/\/sdc:(spec|implement|review|test|quality|validate)/.test(installJs)) {
  fail('Installer completion guidance must not advertise hidden detailed skills as public slash commands.');
}
const pluginEntriesBlock = installJs.slice(
  installJs.indexOf('const PLUGIN_ENTRIES'),
  installJs.indexOf('const SDC_MARKETPLACE_NAME')
);
if (pluginEntriesBlock.includes("'.claude',")) {
  fail('PLUGIN_ENTRIES must not copy a root .claude directory; Claude layout is generated.');
}
for (const marker of ["'scripts'", "'.agents'", "'sdc-references'"]) {
  if (!pluginEntriesBlock.includes(marker)) {
    fail(`PLUGIN_ENTRIES must package execution helpers and Codex marketplace metadata: missing ${marker}`);
  }
}
if (/\b(init|change|plan|apply|check|archive|harness|spec|implement|review|test|quality|validate):\s*'sdc-/.test(installJs)) {
  fail('Claude skill layout must not generate short alias skill directories that collide with slash command names.');
}
if (/'sdc-(core|init|change|plan|apply|check|archive|harness)'/.test(installJs.slice(
  installJs.indexOf('const skillNames'),
  installJs.indexOf('for (const skillName of skillNames)')
))) {
  fail('Claude skill layout must not generate public command backing skills.');
}
if (!installJs.includes("'sdc-spec'") || !installJs.includes("path.join(claudeSkillsRoot, skillName)")) {
  fail('Claude skill layout must generate advanced sdc-* skill directories.');
}
for (const marker of [
  'PUBLIC_WORKFLOW_SKILLS',
  "dir: 'sdc-core'",
  "name: 'sdc-init'",
  'ensurePublicWorkflowSkills',
  'writeCompleteAgentSkillLayout',
  'replacePluginTransactionally',
  'includePublicWorkflowSkills: true',
]) {
  if (!installJs.includes(marker)) {
    fail(`Installer must generate and synchronize public workflow skills for Codex/Hermes: missing ${marker}`);
  }
}

const cli = readText('sdc-cli.py');
const sharedReferences = [
  'sdc-references/common-ground.md',
  'sdc-references/expert-routing.md',
  'sdc-references/artifact-output-contracts.md',
  'sdc-references/execution-orchestration.md',
  'sdc-references/workflow-manifest.yaml',
];
for (const reference of sharedReferences) {
  if (!fs.existsSync(path.join(root, reference))) {
    fail(`Missing shared SDC reference: ${reference}`);
  }
}
const currentSchema = `Schema: SDC ${version}`;
const schemaMatches = [...cli.matchAll(/Schema: SDC ([0-9.]+)/g)].map((match) => match[0]);
if (!schemaMatches.includes(currentSchema) || schemaMatches.some((schema) => schema !== currentSchema)) {
  fail(`sdc-cli.py schema markers must all match ${currentSchema}. found=${schemaMatches.join(',')}`);
}
if (!cli.includes('--confirmed-intake')) {
  fail('sdc-cli.py must enforce Change Intake Gate with --confirmed-intake for file creation.');
}
if (!cli.includes('## Analysis Snapshot')) {
  fail('sdc-cli.py impact template must use the English Change Impact Gate schema.');
}
if (!cli.includes('if not cmd_validate(change_id, require_delivery_evidence=True):')) {
  fail('sdc-cli.py archive must require delivery evidence before writing archive artifacts.');
}
if (!cli.includes('仍有未完成任务，不能归档')) {
  fail('sdc-cli.py archive must block unchecked tasks.');
}
if (!cli.includes('稳定规范已存在，未覆盖也不归档')) {
  fail('sdc-cli.py archive must block when the stable spec already exists.');
}
if (!cli.includes('归档目录已存在，不能重复归档')) {
  fail('sdc-cli.py archive must block when the archive directory already exists.');
}
if (!cli.includes('../../../specs/{change_id}.md')) {
  fail('sdc-cli.py archive.md must link from archived change directory back to .sdc/specs using ../../../specs.');
}
if (!cli.includes('"common-ground.md"') || !cli.includes('"expert-routing.md"') || !cli.includes('"knowledge/index.md"') || !cli.includes('"memory/candidates.md"')) {
  fail('sdc-cli.py init must create common-ground.md, expert-routing.md, knowledge/index.md, and memory/candidates.md.');
}
for (const marker of [
  'cmd_import_standards',
  '--standards',
  'standards/company/README.md',
  'SDC-MANAGED-STANDARDS-PACK',
]) {
  if (!cli.includes(marker)) {
    fail(`sdc-cli.py must support company standards pack import: missing ${marker}`);
  }
}
for (const marker of [
  'Execution Orchestration Discipline',
  '## Global Constraints',
  '## Plan Preflight',
  'validate_plan_preflight',
  'validate_execution_handoff',
  'validate_delivery_completion',
  'parse_progress_ledger',
  'validate_dual_review_evidence',
  'evidence_reference_exists',
  '"check-ignore", "--no-index"',
  'Review 不是 Approved',
  '.sdc/runtime',
  'Final Whole-Change Review',
  'validate_global_constraints_consistency',
  'MANAGED_TEMPLATE_PATHS',
  'LEGACY_MANAGED_HASHES',
  'is_unmodified_managed_file',
  'preserved-user-owned',
]) {
  if (!cli.includes(marker)) {
    fail(`sdc-cli.py must enforce execution orchestration; missing marker: ${marker}`);
  }
}
const executionOrchestration = readText('sdc-references/execution-orchestration.md');
if (!executionOrchestration.includes('do not dispatch multiple implementation tasks in parallel')) {
  fail('Execution orchestration must serialize implementation tasks through review and ledger completion.');
}

for (const helper of ['scripts/sdc-task-brief.py', 'scripts/sdc-review-package.py', 'scripts/package-codex-plugin.py']) {
  if (!fs.existsSync(path.join(root, helper))) {
    fail(`Missing SDC execution/packaging helper: ${helper}`);
  }
}
if (!readText('scripts/sdc-review-package.py').includes('would omit untracked files')) {
  fail('WORKTREE review packages must refuse to silently omit untracked files.');
}
const codexPackager = readText('scripts/package-codex-plugin.py');
for (const marker of [
  'PAYLOAD_ENTRIES',
  'stage_payload',
  'verify_payload',
  'scripts/sdc-task-brief.py',
  'scripts/sdc-review-package.py',
  'relative = path.relative_to(source)',
]) {
  if (!codexPackager.includes(marker)) {
    fail(`Codex portal packager must build a minimal rootless runtime payload: missing ${marker}`);
  }
}
if (codexPackager.includes('Path("sdc") / path.relative_to(source)')) {
  fail('Codex portal archive must be rootless; do not wrap payload entries in sdc/.');
}
if (!cli.includes('"templates/context-pack.md"') || !cli.includes('"templates/common-ground.md"') || !cli.includes('"templates/expert-routing.md"') || !cli.includes('"templates/knowledge-candidates.md"')) {
  fail('sdc-cli.py must ship context-pack, common-ground, expert-routing, and knowledge-candidates templates.');
}
if (!cli.includes('validate_context_pack')) {
  fail('sdc-cli.py validate must check context-pack.md.');
}
if (!cli.includes('## Common Ground Used') || !cli.includes('## Expert Profiles Used') || !cli.includes('## Artifact Output Contract')) {
  fail('sdc-cli.py context-pack templates must include Common Ground Used, Expert Profiles Used, and Artifact Output Contract.');
}
if (!cli.includes('["Knowledge Sources Used", "Common Ground Used", "Decision Ledger"')) {
  fail('sdc-cli.py spec validation must require Common Ground Used.');
}
if (!cli.includes('"## Knowledge Sources Used", "## Knowledge Gaps", "## Common Ground Used"')) {
  fail('sdc-cli.py design/context validation must require Common Ground Used.');
}
for (const marker of [
  'ARTIFACT_OUTPUT_CONTRACTS',
  'validate_artifact_output_contract',
  'Process / State Diagram',
  'API / Contract Specification',
  'Data Model / Migration Contract',
  'Test Matrix',
  'Deploy / Release Checklist',
  'AI Involvement Note',
]) {
  if (!cli.includes(marker)) {
    fail(`sdc-cli.py must enforce artifact output contracts; missing marker: ${marker}`);
  }
}
if (!cli.includes('.sdc/knowledge/product/') || !cli.includes('.sdc/knowledge/technical/')) {
  fail('sdc-cli.py archive Knowledge Compact Gate must evaluate product and technical knowledge updates.');
}
if (!cli.includes('.sdc/common-ground.md') || !cli.includes('.sdc/expert-routing.md')) {
  fail('sdc-cli.py archive Knowledge Compact Gate must evaluate Common Ground and Expert Routing updates.');
}
for (const marker of [
  'No Evidence, No Fact',
  'No Confirmation, No Execution',
  'No Impact, No Brownfield Change',
  'validate_no_unconfirmed_execution_inputs',
  'validate_common_ground_execution_inputs',
  'validate_knowledge_candidates_file',
  'Knowledge Gap',
  'OPEN Common Ground',
  'WORKING Common Ground',
  'Evidence Needed',
  'Promotion Gate',
]) {
  if (!cli.includes(marker)) {
    fail(`sdc-cli.py must enforce anti-guess knowledge gates; missing marker: ${marker}`);
  }
}

const readme = readText('README.md');
if (readme.includes('├── standards/') && readme.match(/├── standards\//g)?.length > 1) {
  fail('README.md workspace tree lists standards/ more than once.');
}
if (readme.includes('`/sdc:spec`、`/sdc:implement`')) {
  fail('README.md still advertises detailed skills as public slash commands.');
}
if (!readme.includes('Knowledge Compact Gate')) {
  fail('README.md must document archive Knowledge Compact Gate.');
}
if (!readme.includes('common-ground.md') || !readme.includes('expert-routing.md') || !readme.includes('Expert Routing')) {
  fail('README.md must document Common Ground and internal Expert Routing.');
}
if (!readme.includes('Artifact Output Contract') || !readme.includes('Test Matrix') || !readme.includes('上线检查清单')) {
  fail('README.md must document Artifact Output Contract and triggered delivery outputs.');
}
if (!readme.includes('Plan Preflight') || !readme.includes('Spec Compliance') || !readme.includes('.sdc/runtime/')) {
  fail('README.md must document SDC execution orchestration and runtime handoffs.');
}
if (!readme.includes('.sdc/knowledge/product/') || !readme.includes('.sdc/knowledge/technical/') || !readme.includes('context-pack.md')) {
  fail('README.md must document product/technical knowledge and context-pack usage.');
}
if (!readme.includes('.sdc/standards/company/') || !readme.includes('sdc standards import /path/to/spec-rules')) {
  fail('README.md must document company standards pack import.');
}

const evalRunner = readText('evals/sdc-flow/run_sdc_flow.py');
const evalProvider = readText('evals/sdc-flow/sdc_flow_provider.py');
if (!evalRunner.includes('All {len(SCENARIOS)} evals passed')) {
  fail('SDC flow eval runner must report all scenario results.');
}
for (const scenario of ['init_greenfield', 'init_upgrades_stale_managed_templates', 'discovery_open_blocks_context_pack', 'brownfield_requires_impact', 'archive_knowledge_compact_gate']) {
  if (!evalProvider.includes(scenario)) {
    fail(`SDC flow eval provider is missing scenario: ${scenario}`);
  }
}
for (const marker of ['.sdc/common-ground.md', '.sdc/expert-routing.md', '## Expert Profiles Used']) {
  if (!evalProvider.includes(marker)) {
    fail(`SDC flow eval provider must cover Common Ground / Expert Routing marker: ${marker}`);
  }
}
for (const marker of ['## Artifact Output Contract', 'Test Matrix', 'API / Contract Specification']) {
  if (!evalProvider.includes(marker)) {
    fail(`SDC flow eval provider must cover Artifact Output Contract marker: ${marker}`);
  }
}
for (const scenario of [
  'unconfirmed_assumption_blocks_execution',
  'open_knowledge_gap_blocks_execution',
  'open_common_ground_blocks_execution',
  'working_common_ground_blocks_final_execution',
  'incomplete_candidate_blocks_archive_readiness',
  'missing_artifact_output_contract_blocks_execution',
  'missing_task_interface_blocks_plan',
  'empty_task_interface_blocks_plan',
  'empty_global_constraints_blocks_plan',
  'conflicting_global_constraints_blocks_plan',
  'incomplete_plan_preflight_blocks_plan',
  'open_plan_preflight_findings_blocks_plan',
  'uncertain_plan_preflight_findings_blocks_plan',
  'uncertain_plan_preflight_status_blocks_plan',
  'current_plan_global_constraints_are_validated',
  'malformed_global_constraint_id_blocks_plan',
  'duplicate_task_id_blocks_plan',
  'uncertain_context_pack_preflight_status_blocks_plan',
  'invalid_task_ids_block_plan',
  'mixed_invalid_task_id_blocks_plan',
  'invalid_runtime_workspace_blocks_plan',
  'negated_task_review_contract_blocks_plan',
  'duplicate_plan_preflight_field_blocks_plan',
  'duplicate_task_interface_field_blocks_plan',
  'contradictory_dual_review_verdict_blocks_check',
  'duplicate_plan_preflight_section_blocks_plan',
  'duplicate_task_review_block_blocks_check',
  'duplicate_final_review_section_blocks_check',
  'completed_task_without_review_blocks_check',
  'missing_dual_review_verdict_blocks_check',
  'missing_review_evidence_target_blocks_check',
  'ignored_review_evidence_blocks_check',
  'delivery_check_allows_missing_runtime_ledger',
  'inconsistent_runtime_ledger_blocks_check',
  'execution_helpers_create_file_handoffs',
  'review_package_blocks_untracked_worktree',
  'execution_contract_serializes_tasks',
  'init_preserves_user_modified_managed_file',
  'init_upgrades_exact_legacy_template',
  'managed_fingerprint_is_not_real_content',
  'codex_install_removes_stale_layout',
  'codex_install_recovers_interrupted_swap',
  'codex_package_is_rootless_and_deterministic',
  'standards_pack_import',
]) {
  if (!evalProvider.includes(scenario)) {
    fail(`SDC anti-guess eval provider is missing scenario: ${scenario}`);
  }
}

const workflowStandards = readText('sdc-references/workflow-standards.md');
const taskFormatMatch = workflowStandards.match(/## Task Format([\s\S]*?)## Evidence Discipline/);
if (!taskFormatMatch) {
  fail('workflow-standards.md must include a bounded Task Format section.');
} else {
  for (const field of ['Depends on', 'Files', 'Consumes', 'Produces', 'Verify', 'Expected', 'Review', 'Evidence', 'Source']) {
    if (!taskFormatMatch[1].includes(`- ${field}:`)) {
      fail(`workflow-standards.md Task Format is missing required field: ${field}`);
    }
  }
}

const publicDocs = [
  readme,
  readText('CHANGELOG.md'),
  readText('docs/sdc-discipline-core.md'),
  ...commandFiles.map((name) => readText(path.join('commands', `${name}.md`))),
].join('\n');
if (/\/sdc:compact/.test(publicDocs)) {
  fail('Do not advertise a public /sdc:compact command; compaction belongs inside archive.');
}

const commandDocs = commandFiles.map((name) => readText(path.join('commands', `${name}.md`))).join('\n');
if (/Follow the installed `sdc-(core|init|change|plan|apply|check|archive|harness)` skill exactly/.test(commandDocs)) {
  fail('Claude public commands must be self-contained and must not reference hidden public backing skills.');
}

if (errors.length > 0) {
  console.error('Release audit failed:');
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

console.log(`Release audit passed for SDC ${version}`);
