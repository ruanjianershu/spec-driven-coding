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

function log(color, message) {
  console.log(`${color}${message}${RESET}`);
}

function copyDir(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  
  const entries = fs.readdirSync(src, { withFileTypes: true });
  
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
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
  
  // CodeX
  const codexPaths = [
    path.join(home, '.codex', 'plugins'),
    path.join(home, '.config', 'codex', 'plugins'),
  ];
  for (const p of codexPaths) {
    if (fs.existsSync(p)) {
      platforms.push({ name: 'CodeX', path: p, type: 'codex' });
      break;
    }
  }
  
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
  
  const destPath = path.join(platform.path, 'sdc-spec');
  
  if (platform.type === 'hermes') {
    // Hermes 只需要 skills 目录
    copyDir(path.join(projectRoot, 'skills'), destPath);
  } else {
    // 其他平台复制整个插件目录
    copyDir(projectRoot, destPath);
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
platforms.forEach(installToPlatform);

console.log('\n' + '='.repeat(60));
log(GREEN, '🎉 SDC 安装完成！');
console.log('='.repeat(60));

console.log('\n📖 使用方法：');
console.log('  /sdc:spec      - 生成规范文档');
console.log('  /sdc:plan      - 生成实现计划');
console.log('  /sdc:implement - 自动开发');
console.log('  /sdc:review    - 代码审查');
console.log('  /sdc:test      - 运行测试');
console.log('  /sdc:quality   - 最终质量检查');

console.log('\n🔗 项目地址：https://github.com/ruanjianershu/spec-driven-coding');
console.log('\n');
