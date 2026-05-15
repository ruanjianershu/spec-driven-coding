#!/usr/bin/env node
// SDC - 规范驱动开发 一键安装器
// 用法：npx sdc-spec

import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.join(__dirname, '..');

const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const BLUE = '\x1b[34m';
const RESET = '\x1b[0m';

const PLUGIN_ENTRIES = [
  'skills',
  '.claude',
  'commands',
  '.claude-plugin',
  '.codex-plugin',
  'docs',
  'SECURITY.md',
  'PRIVACY.md',
  'CHANGELOG.md',
  'README.md',
  'LICENSE',
  'package.json',
  'sdc-cli.py',
  'bin',
];

const SDC_MARKETPLACE_NAME = 'sdc-local';
const SDC_PLUGIN_ID = 'sdc@sdc-local';
const SDC_CLAUDE_PLUGIN_ID = 'sdc@sdc-local';

const IGNORED_ENTRIES = new Set([
  '.DS_Store',
  '.git',
  '.sdc',
  'node_modules',
  '__pycache__',
]);

function log(color, message) {
  console.log(`${color}${message}${RESET}`);
}

function copyDir(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  
  const entries = fs.readdirSync(src, { withFileTypes: true });
  
  for (const entry of entries) {
    if (IGNORED_ENTRIES.has(entry.name)) {
      continue;
    }

    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    
    if (entry.isSymbolicLink()) {
      fs.rmSync(destPath, { recursive: true, force: true });
      fs.symlinkSync(fs.readlinkSync(srcPath), destPath);
    } else if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function copyIfExists(src, dest) {
  if (!fs.existsSync(src)) {
    return;
  }

  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    copyDir(src, dest);
  } else {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
  }
}

function copyPlugin(dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  for (const entry of PLUGIN_ENTRIES) {
    copyIfExists(path.join(projectRoot, entry), path.join(dest, entry));
  }

  ensureClaudeSkillLayout(dest);
}

function ensureClaudeSkillLayout(pluginRoot) {
  const sourceRoot = path.join(pluginRoot, 'skills');
  if (!fs.existsSync(sourceRoot)) {
    return;
  }

  const claudeSkillsRoot = path.join(pluginRoot, '.claude', 'skills');
  fs.rmSync(claudeSkillsRoot, { recursive: true, force: true });
  fs.mkdirSync(claudeSkillsRoot, { recursive: true });

  const aliases = {
    sdc: 'sdc-core',
    init: 'sdc-init',
    change: 'sdc-change',
    plan: 'sdc-plan',
    apply: 'sdc-apply',
    check: 'sdc-check',
    archive: 'sdc-archive',
    harness: 'sdc-harness',
    spec: 'sdc-spec',
    implement: 'sdc-implement',
    review: 'sdc-review',
    test: 'sdc-test',
    quality: 'sdc-quality',
    validate: 'sdc-validate'
  };

  for (const [alias, skillName] of Object.entries(aliases)) {
    const src = path.join(sourceRoot, skillName);
    if (fs.existsSync(src)) {
      copyDir(src, path.join(claudeSkillsRoot, alias));
    }
  }
}

function packageVersion() {
  const packageJson = JSON.parse(fs.readFileSync(path.join(projectRoot, 'package.json'), 'utf8'));
  return packageJson.version || '1.0.0';
}

function writeLocalCodexMarketplace(home) {
  const marketplaceRoot = path.join(home, '.codex', 'local-marketplaces', SDC_MARKETPLACE_NAME);
  const marketplaceFile = path.join(marketplaceRoot, '.agents', 'plugins', 'marketplace.json');
  const pluginRoot = path.join(marketplaceRoot, 'plugins', 'sdc');

  copyPlugin(pluginRoot);
  fs.mkdirSync(path.dirname(marketplaceFile), { recursive: true });
  fs.writeFileSync(marketplaceFile, JSON.stringify({
    name: SDC_MARKETPLACE_NAME,
    interface: {
      displayName: 'SDC Local'
    },
    plugins: [
      {
        name: 'sdc',
        source: {
          source: 'local',
          path: './plugins/sdc'
        },
        policy: {
          installation: 'AVAILABLE',
          authentication: 'ON_INSTALL'
        },
        category: 'Coding'
      }
    ]
  }, null, 2) + '\n');

  return marketplaceRoot;
}

function removeTomlSection(content, header) {
  const escaped = header.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const sectionPattern = new RegExp(`\\n?\\[${escaped}\\][\\s\\S]*?(?=\\n\\[|$)`, 'g');
  return content.replace(sectionPattern, '').trimEnd();
}

function enableCodexPlugin(home, marketplaceRoot) {
  const configPath = path.join(home, '.codex', 'config.toml');
  fs.mkdirSync(path.dirname(configPath), { recursive: true });

  let content = fs.existsSync(configPath) ? fs.readFileSync(configPath, 'utf8') : '';
  content = removeTomlSection(content, `marketplaces.${SDC_MARKETPLACE_NAME}`);
  content = removeTomlSection(content, `plugins."${SDC_PLUGIN_ID}"`);

  const normalizedMarketplaceRoot = marketplaceRoot.replace(/\\/g, '\\\\');
  const block = `

[marketplaces.${SDC_MARKETPLACE_NAME}]
last_updated = "${new Date().toISOString()}"
source_type = "local"
source = "${normalizedMarketplaceRoot}"

[plugins."${SDC_PLUGIN_ID}"]
enabled = true
`;

  fs.writeFileSync(configPath, `${content.trimEnd()}${block}`);
  return configPath;
}

function writeCodexPluginCache(home) {
  const cachePluginRoot = path.join(
    home,
    '.codex',
    'plugins',
    'cache',
    SDC_MARKETPLACE_NAME,
    'sdc'
  );
  const versionedPluginRoot = path.join(cachePluginRoot, packageVersion());

  fs.rmSync(cachePluginRoot, { recursive: true, force: true });
  copyPlugin(versionedPluginRoot);

  return versionedPluginRoot;
}

function runOptional(command, args) {
  try {
    execFileSync(command, args, { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

function writeLocalClaudeMarketplace(home) {
  const marketplaceRoot = path.join(home, '.claude', 'plugins', 'marketplaces', SDC_MARKETPLACE_NAME);
  fs.rmSync(marketplaceRoot, { recursive: true, force: true });
  copyPlugin(marketplaceRoot);
  return marketplaceRoot;
}

function installClaudePlugin(home) {
  const marketplaceRoot = path.join(home, '.claude', 'plugins', 'marketplaces', SDC_MARKETPLACE_NAME);

  // Remove stale pre-marketplace copies created by older SDC installers.
  fs.rmSync(path.join(home, '.claude', 'plugins', 'sdc'), { recursive: true, force: true });
  fs.rmSync(path.join(home, '.claude', 'plugins', 'sdc-spec'), { recursive: true, force: true });

  const hasClaude = runOptional('claude', ['--version']);
  if (!hasClaude) {
    return {
      marketplaceRoot,
      installed: false,
      reason: '未找到 claude 命令，请在 Claude Code 中手动添加本地 marketplace 后安装 sdc。'
    };
  }

  runOptional('claude', ['plugin', 'uninstall', 'sdc', '--scope', 'user', '--yes']);
  runOptional('claude', ['plugin', 'uninstall', SDC_CLAUDE_PLUGIN_ID, '--scope', 'user', '--yes']);
  runOptional('claude', ['plugin', 'marketplace', 'remove', SDC_MARKETPLACE_NAME]);

  writeLocalClaudeMarketplace(home);
  const marketplaceAdded = runOptional('claude', [
    'plugin',
    'marketplace',
    'add',
    marketplaceRoot,
    '--scope',
    'user'
  ]);
  const pluginInstalled = marketplaceAdded && runOptional('claude', [
    'plugin',
    'install',
    SDC_CLAUDE_PLUGIN_ID,
    '--scope',
    'user'
  ]);

  return {
    marketplaceRoot,
    installed: pluginInstalled,
    reason: pluginInstalled ? null : 'Claude marketplace 注册或插件安装失败，请运行 claude plugin validate 检查。'
  };
}

function installCodexSkills(home) {
  const installedPaths = [];
  const skillTargets = [path.join(home, '.agents', 'skills')];
  const legacyTargetRoot = path.join(home, '.codex', 'skills');
  const skillsRoot = path.join(projectRoot, 'skills');

  for (const targetRoot of skillTargets) {
    fs.mkdirSync(targetRoot, { recursive: true });

    for (const entry of fs.readdirSync(skillsRoot, { withFileTypes: true })) {
      if (!entry.isDirectory()) {
        continue;
      }

      const srcPath = path.join(skillsRoot, entry.name);
      const destPath = path.join(targetRoot, entry.name);
      fs.rmSync(destPath, { recursive: true, force: true });
      copyDir(srcPath, destPath);
    }

    installedPaths.push(targetRoot);
  }

  if (fs.existsSync(legacyTargetRoot)) {
    for (const entry of fs.readdirSync(legacyTargetRoot, { withFileTypes: true })) {
      if (entry.isDirectory() && entry.name.startsWith('sdc-')) {
        fs.rmSync(path.join(legacyTargetRoot, entry.name), { recursive: true, force: true });
      }
    }
  }

  return installedPaths;
}

function uninstallClaude(home) {
  log(BLUE, '\n卸载 Claude Code 中的 SDC...');

  if (runOptional('claude', ['--version'])) {
    runOptional('claude', ['plugin', 'uninstall', 'sdc', '--scope', 'user', '--yes']);
    runOptional('claude', ['plugin', 'uninstall', SDC_CLAUDE_PLUGIN_ID, '--scope', 'user', '--yes']);
    runOptional('claude', ['plugin', 'marketplace', 'remove', SDC_MARKETPLACE_NAME]);
  }

  const roots = [
    path.join(home, '.claude', 'plugins', 'sdc'),
    path.join(home, '.claude', 'plugins', 'sdc-spec'),
    path.join(home, '.claude', 'plugins', 'marketplaces', SDC_MARKETPLACE_NAME),
    path.join(home, '.claude', 'plugins', 'cache', SDC_MARKETPLACE_NAME),
    path.join(home, '.claude', 'plugins', 'data', 'sdc-sdc-local')
  ];

  for (const root of roots) {
    fs.rmSync(root, { recursive: true, force: true });
  }

  log(GREEN, '✅ Claude Code SDC 已卸载');
}

function uninstallCodex(home) {
  log(BLUE, '\n卸载 Codex 中的 SDC...');

  const configPath = path.join(home, '.codex', 'config.toml');
  if (fs.existsSync(configPath)) {
    let content = fs.readFileSync(configPath, 'utf8');
    content = removeTomlSection(content, `marketplaces.${SDC_MARKETPLACE_NAME}`);
    content = removeTomlSection(content, `plugins."${SDC_PLUGIN_ID}"`);
    fs.writeFileSync(configPath, content.trimEnd() ? `${content.trimEnd()}\n` : '');
  }

  const roots = [
    path.join(home, '.codex', 'local-marketplaces', SDC_MARKETPLACE_NAME),
    path.join(home, '.codex', 'plugins', 'cache', SDC_MARKETPLACE_NAME),
    path.join(home, '.codex', 'plugins', 'sdc')
  ];

  for (const root of roots) {
    fs.rmSync(root, { recursive: true, force: true });
  }

  for (const skillsRoot of [
    path.join(home, '.agents', 'skills'),
    path.join(home, '.codex', 'skills')
  ]) {
    if (!fs.existsSync(skillsRoot)) {
      continue;
    }

    for (const entry of fs.readdirSync(skillsRoot, { withFileTypes: true })) {
      if (entry.isDirectory() && entry.name.startsWith('sdc-')) {
        fs.rmSync(path.join(skillsRoot, entry.name), { recursive: true, force: true });
      }
    }
  }

  log(GREEN, '✅ Codex SDC 已卸载');
}

function uninstallHermes(home) {
  log(BLUE, '\n卸载 Hermes Agent 中的 SDC...');
  fs.rmSync(path.join(home, '.hermes', 'skills', 'sdc'), { recursive: true, force: true });
  fs.rmSync(path.join(home, '.hermes', 'skills', 'sdc-spec'), { recursive: true, force: true });
  log(GREEN, '✅ Hermes Agent SDC 已卸载');
}

function uninstallAll() {
  const home = process.env.HOME || process.env.USERPROFILE;
  if (!home) {
    log(RED, '❌ 无法识别 HOME 目录');
    process.exit(1);
  }

  console.log('\n' + '='.repeat(60));
  console.log('🔧 SDC - 规范驱动开发 一键卸载器');
  console.log('='.repeat(60));

  uninstallClaude(home);
  uninstallCodex(home);
  uninstallHermes(home);

  console.log('\n' + '='.repeat(60));
  log(GREEN, '🎉 SDC 卸载完成！');
  console.log('='.repeat(60));
  console.log('\n如 Claude Code / Codex 已打开，请完全重启应用让插件列表刷新。');
  console.log('\n');
}

function detectPlatforms() {
  const home = process.env.HOME || process.env.USERPROFILE;
  const platforms = [];
  
  // Claude Code
  const claudePaths = [
    path.join(home, '.claude', 'plugins'),
    path.join(home, 'Library', 'Application Support', 'Claude', 'plugins'),
  ];
  for (const p of claudePaths) {
    if (fs.existsSync(p)) {
      platforms.push({ name: 'Claude Code', path: p, type: 'claude' });
      break;
    }
  }
  
  // CodeX/Codex: install to the default path even on a fresh machine.
  // Some Codex builds load custom skills from ~/.agents/skills and may not
  // create ~/.codex/plugins before the first plugin install.
  const codexPath = path.join(home, '.codex', 'plugins');
  platforms.push({ name: 'CodeX', path: codexPath, type: 'codex' });
  
  // Hermes Agent
  const hermesPaths = [
    path.join(home, '.hermes', 'skills'),
  ];
  for (const p of hermesPaths) {
    if (fs.existsSync(p)) {
      platforms.push({ name: 'Hermes Agent', path: p, type: 'hermes' });
      break;
    }
  }
  
  return platforms;
}

function installToPlatform(platform) {
  log(BLUE, `\n安装到 ${platform.name}...`);
  
  const destPath = path.join(platform.path, 'sdc');
  
  if (platform.type === 'hermes') {
    // Hermes 只需要 skills 目录
    copyDir(path.join(projectRoot, 'skills'), destPath);
  } else {
    // 其他平台复制插件所需文件，避免带入 .git、.DS_Store 等本地文件
    copyPlugin(destPath);
  }

  if (platform.type === 'codex') {
    const home = process.env.HOME || process.env.USERPROFILE;
    const marketplaceRoot = writeLocalCodexMarketplace(home);
    const cachePath = writeCodexPluginCache(home);
    const configPath = enableCodexPlugin(home, marketplaceRoot);
    const skillPaths = installCodexSkills(home);
    console.log('  已注册 Codex 本地插件 marketplace：');
    console.log(`  - ${marketplaceRoot}`);
    console.log('  已写入 Codex 插件 cache：');
    console.log(`  - ${cachePath}`);
    console.log(`  已启用 Codex 插件：${SDC_PLUGIN_ID}`);
    console.log(`  - ${configPath}`);
    console.log('  已同步 Codex 可直接扫描的 skills：');
    skillPaths.forEach((p) => console.log(`  - ${p}`));
  } else if (platform.type === 'claude') {
    const home = process.env.HOME || process.env.USERPROFILE;
    const result = installClaudePlugin(home);
    console.log('  已写入 Claude Code 本地 marketplace：');
    console.log(`  - ${result.marketplaceRoot}`);
    if (result.installed) {
      console.log(`  已通过 Claude Code 启用插件：${SDC_CLAUDE_PLUGIN_ID}`);
    } else {
      console.log(`  ⚠️  ${result.reason}`);
    }
  }
  
  log(GREEN, `✅ 安装成功！路径: ${destPath}`);
}

// Main
const command = (process.argv[2] || 'install').toLowerCase();
if (['uninstall', 'remove', 'clean'].includes(command)) {
  uninstallAll();
  process.exit(0);
}

if (!['install', 'update'].includes(command)) {
  log(RED, `❌ 未知指令：${command}`);
  console.log('\n可用指令：');
  console.log('  npx sdc-spec@latest');
  console.log('  npx sdc-spec@latest uninstall');
  process.exit(1);
}

console.log('\n' + '='.repeat(60));
console.log('🔧 SDC - 规范驱动开发 一键安装器');
console.log('='.repeat(60));

const platforms = detectPlatforms();

if (platforms.length === 0) {
  log(YELLOW, '\n⚠️  未检测到已知的 AI 编码工具');
  console.log('\n支持的平台：');
  console.log('  - Claude Code');
  console.log('  - CodeX');
  console.log('  - Hermes Agent');
  console.log('\n手动安装方式：');
  console.log(`  git clone https://github.com/ruanjianershu/spec-driven-coding.git`);
  console.log('  然后在你的 AI 工具中加载本地插件');
  process.exit(0);
}

log(GREEN, `\n✅ 检测到 ${platforms.length} 个平台：`);
platforms.forEach((p, i) => {
  console.log(`  ${i + 1}. ${p.name} -> ${p.path}`);
});

console.log('\n开始安装...');
let failedCount = 0;
platforms.forEach((platform) => {
  try {
    installToPlatform(platform);
  } catch (error) {
    failedCount += 1;
    log(RED, `❌ 安装到 ${platform.name} 失败：${error.message}`);
  }
});

if (failedCount > 0) {
  log(YELLOW, `\n⚠️  ${failedCount} 个平台安装失败，请检查对应目录权限后重试。`);
  process.exit(1);
}

console.log('\n' + '='.repeat(60));
log(GREEN, '🎉 SDC 安装完成！');
console.log('='.repeat(60));

console.log('\n📖 使用方法：');
console.log('  /sdc:init');
console.log('  /sdc:change 支持用户登录');
console.log('  /sdc:plan');
console.log('  /sdc:apply');
console.log('  /sdc:check');
console.log('  /sdc:archive <change-id>');
console.log('\n高级用法：仍可直接调用 /sdc:spec、/sdc:review、/sdc:test、/sdc:quality、/sdc:validate 等细分指令');
console.log('\n⚠️  Claude Code 安装后请完全重启应用，让 slash commands 重新加载。');
console.log('⚠️  Codex 当前版本不支持插件自定义 slash commands，请通过 /skills 或自然语言触发 SDC skills。');

console.log('\n🔗 项目地址：https://github.com/ruanjianershu/spec-driven-coding');
console.log('\n');
