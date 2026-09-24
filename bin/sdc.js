#!/usr/bin/env node

import { spawnSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const args = process.argv.slice(2);

function exitWithChildStatus(result, command) {
  if (result.error) {
    console.error(`❌ 无法运行 ${command}：${result.error.message}`);
    process.exit(1);
  }

  process.exit(typeof result.status === 'number' ? result.status : 1);
}

if (args[0] === 'check' && args[1] === 'installation') {
  exitWithChildStatus(
    spawnSync(process.execPath, [path.join(__dirname, '..', 'scripts', 'sdc-doctor.mjs'), ...args.slice(2)], { stdio: 'inherit' }),
    'SDC installation diagnostics',
  );
}

if (args[0] === 'validate') {
  if (args.length !== 2 || !args[1] || args[1].startsWith('-')) {
    console.error('❌ 用法: sdc validate <change>');
    process.exit(1);
  }

  exitWithChildStatus(
    spawnSync('python3', [path.join(__dirname, '..', 'sdc-cli.py'), 'validate', args[1]], {
      stdio: 'inherit',
    }),
    'sdc-cli.py validate',
  );
}

exitWithChildStatus(
  spawnSync(process.execPath, [path.join(__dirname, 'install.js'), ...args], { stdio: 'inherit' }),
  'SDC installer',
);
