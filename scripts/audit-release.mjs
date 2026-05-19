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

const publicCommands = ['sdc', 'init', 'change', 'plan', 'apply', 'check', 'archive', 'harness'];
const commandFiles = fs
  .readdirSync(path.join(root, 'commands'))
  .filter((name) => name.endsWith('.md'))
  .map((name) => name.replace(/\.md$/, ''));
sameSet(commandFiles, publicCommands, 'Claude public command files');

const advancedSkills = ['sdc-spec', 'sdc-implement', 'sdc-review', 'sdc-test', 'sdc-quality', 'sdc-validate'];
const skillsDirEntries = fs
  .readdirSync(path.join(root, 'skills'), { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name);
const allowedSkillsDirEntries = [...advancedSkills, 'sdc-shared'];
const unexpectedSkillEntries = skillsDirEntries.filter((name) => !allowedSkillsDirEntries.includes(name));
if (unexpectedSkillEntries.length > 0) {
  fail(`Source skills/ must not contain legacy public command backing skills. unexpected=${unexpectedSkillEntries.join(',')}`);
}
const missingAdvancedSkills = advancedSkills.filter((name) => !skillsDirEntries.includes(name));
if (missingAdvancedSkills.length > 0) {
  fail(`Source skills/ is missing advanced skill directories: ${missingAdvancedSkills.join(',')}`);
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

const cli = readText('sdc-cli.py');
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
if (!cli.includes('if not cmd_validate(change_id):')) {
  fail('sdc-cli.py archive must run validation before writing archive artifacts.');
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
