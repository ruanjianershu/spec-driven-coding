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

const cli = readText('sdc-cli.py');
if (cli.includes('Schema: SDC 1.1.7')) {
  fail('sdc-cli.py still contains stale Schema: SDC 1.1.7.');
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

if (errors.length > 0) {
  console.error('Release audit failed:');
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

console.log(`Release audit passed for SDC ${version}`);
