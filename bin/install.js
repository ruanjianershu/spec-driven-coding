#!/usr/bin/env node
// SDC - 规范驱动开发 一键安装器
// 用法：npx sdc-spec

import fs from 'fs';
import path from 'path';
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
  '.claude-plugin',
  '.codex-plugin',
  'README.md',
  'LICENSE',
  'package.json',
  'sdc-cli.py',
  'bin',
];

const SDC_MARKETPLACE_NAME = 'sdc-local';
const SDC_PLUGIN_ID = 'sdc@sdc-local';

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
    
    if (entry.isDirectory()) {
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
    const configPath = enableCodexPlugin(home, marketplaceRoot);
    const skillPaths = installCodexSkills(home);
    console.log('  已注册 Codex 本地插件 marketplace：');
    console.log(`  - ${marketplaceRoot}`);
    console.log(`  已启用 Codex 插件：${SDC_PLUGIN_ID}`);
    console.log(`  - ${configPath}`);
    console.log('  已同步 Codex 可直接扫描的 skills：');
    skillPaths.forEach((p) => console.log(`  - ${p}`));
  }
  
  log(GREEN, `✅ 安装成功！路径: ${destPath}`);
}

// Main
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
console.log('\n⚠️  Codex 安装后请完全重启应用，让 slash commands 重新加载。');

console.log('\n🔗 项目地址：https://github.com/ruanjianershu/spec-driven-coding');
console.log('\n');
