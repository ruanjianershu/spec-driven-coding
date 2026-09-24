#!/usr/bin/env node
// Read-only, dependency-free diagnostics for the layouts produced by install.js.
import fs from 'fs';
import os from 'os';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

const PACKAGE_ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const SCHEMA = 'sdc.install-diagnostics/v1';
const CLIENTS = ['codex', 'claude', 'hermes'];
const HELPERS = [
  'sdc-cli.py', 'scripts/sdc-runtime-context.py', 'scripts/sdc_evidence.py',
  'scripts/sdc-task-brief.py', 'scripts/sdc-review-package.py',
  'scripts/sdc_compact.py', 'scripts/sdc_findings.py',
];
const OPTIONAL_HELPERS = ['scripts/sdc-doctor.mjs'];
const PUBLIC = ['core', 'init', 'change', 'plan', 'apply', 'check', 'archive', 'harness'];
const ADVANCED = ['spec', 'implement', 'review', 'test', 'quality', 'validate'];
const IGNORE = new Set(['.DS_Store', '__pycache__', '.git', 'node_modules']);
const MAX_FILE = 4 * 1024 * 1024;
const MAX_TOTAL = 64 * 1024 * 1024;
const MAX_ENTRIES = 16384;
const MAX_DEPTH = 16;
const REPAIR = 'Review this path, then reinstall from the intended SDC source with explicit approval and restart the client.';
const REGISTRY_ACTION = 'Review the SDC registration in this file; use the client installer to correct it after approval. No settings were changed.';
const PATH_ACTION = 'Use an existing local directory and regular payload files; remove traversal or replace linked entries with an approved real copy.';
const isObject = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const safeName = value => typeof value === 'string' && /^[A-Za-z0-9_-][A-Za-z0-9_.-]{0,99}$/.test(value);
const localPath = value => typeof value === 'string' && value.length > 0 && !/[\x00-\x1f\x7f]/.test(value);
const within = (root, target) => target === root || target.startsWith(root + path.sep);
const fingerprint = files => {
  const hash = crypto.createHash('sha256');
  for (const [name, digest] of [...files].sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0)) {
    hash.update(name + '\0' + digest + '\n');
  }
  return hash.digest('hex');
};

class DiagnosticError extends Error {
  constructor(code, message, file, action = REPAIR) {
    super(message);
    this.code = code;
    this.file = file;
    this.action = action;
  }
}

function invalidRegistry(file) {
  throw new DiagnosticError('INVALID_REGISTRY', 'Unsupported or malformed SDC registration.', file, REGISTRY_ACTION);
}

// Only the installer's table-form Codex registration is interpreted. This lexer
// keeps unrelated multiline strings/arrays opaque instead of finding fake tables
// inside them. Unsupported relevant TOML forms fail closed, never guess enabled.
function tomlStatements(raw, file) {
  const result = [];
  let value = '', quote = '', triple = false, escaped = false, depth = 0;
  for (let i = 0; i < raw.length; i++) {
    const c = raw[i];
    if (quote) {
      value += c;
      if (escaped) { escaped = false; continue; }
      if (quote === '"' && c === '\\') { escaped = true; continue; }
      if (c === quote && (!triple || raw.slice(i, i + 3) === quote.repeat(3))) {
        if (triple) { value += quote.repeat(2); i += 2; }
        quote = '';
      }
      continue;
    }
    if (c === '#' ) {
      while (i < raw.length && raw[i] !== '\n') i++;
      i--;
      continue;
    }
    if (c === '"' || c === "'") {
      quote = c;
      triple = raw.slice(i, i + 3) === c.repeat(3);
      value += triple ? c.repeat(3) : c;
      if (triple) i += 2;
    } else if (c === '\n' && depth === 0) {
      if (value.trim()) result.push(value.trim());
      value = '';
    } else {
      value += c;
      if (c === '[' || c === '{') depth++;
      if (c === ']' || c === '}') depth--;
      if (depth < 0) invalidRegistry(file);
    }
  }
  if (quote || depth) invalidRegistry(file);
  if (value.trim()) result.push(value.trim());
  return result;
}

function tomlString(value, file) {
  if (/^'[^'\n]*'$/.test(value)) return value.slice(1, -1);
  try {
    const parsed = JSON.parse(value);
    if (typeof parsed === 'string') return parsed;
  } catch { /* Report shape only, never configuration contents. */ }
  invalidRegistry(file);
}

function tomlKeys(value, file) {
  const parts = [];
  let rest = value.trim();
  while (rest) {
    const match = rest.match(/^("(?:[^"\\]|\\.)*"|'[^']*'|[A-Za-z0-9_-]+)\s*/);
    if (!match) invalidRegistry(file);
    parts.push(/^["']/.test(match[1]) ? tomlString(match[1], file) : match[1]);
    rest = rest.slice(match[0].length);
    if (!rest) break;
    if (!rest.startsWith('.')) invalidRegistry(file);
    rest = rest.slice(1).trimStart();
    if (!rest) invalidRegistry(file);
  }
  return parts;
}

function codexTables(raw, file) {
  const tables = Object.assign(Object.create(null), { plugins: new Map(), marketplaces: new Map() });
  let section = [];
  for (const statement of tomlStatements(raw, file)) {
    if (statement.startsWith('[')) {
      if (statement.startsWith('[[')) {
        const arraySection = tomlKeys(statement.slice(2, -2), file);
        if (arraySection[0] === 'plugins' && /^sdc(?:-spec)?@/.test(arraySection[1])) invalidRegistry(file);
        section = [];
        continue;
      }
      if (!statement.endsWith(']')) invalidRegistry(file);
      section = tomlKeys(statement.slice(1, -1), file);
      if (tables[section[0]] && section.length !== 2) {
        if (section.length === 1 || (section[0] === 'plugins' && /^sdc(?:-spec)?@/.test(section[1]))) invalidRegistry(file);
        section = [];
      }
      if (tables[section[0]]) {
        if (tables[section[0]].has(section[1])) invalidRegistry(file);
        tables[section[0]].set(section[1], new Map());
      }
      continue;
    }
    if (!tables[section[0]]) {
      // Quoted keys name the same namespaces as bare keys; do not silently skip
      // unsupported inline/dotted registrations before discovering other clients.
      const first = statement.match(/^("(?:[^"\\]|\\.)*"|'[^']*'|[A-Za-z0-9_-]+)\s*[.=]/);
      if (!first && /^["']/.test(statement)) invalidRegistry(file);
      if (first) {
        const key = /^["']/.test(first[1]) ? tomlString(first[1], file) : first[1];
        if (key === 'plugins' || key === 'marketplaces') invalidRegistry(file);
      }
      continue;
    }
    const relevant = section[0] === 'marketplaces' || /^sdc(?:-spec)?@/.test(section[1]);
    if (!relevant) continue;
    const match = statement.match(/^([A-Za-z0-9_-]+)\s*=\s*([\s\S]+)$/);
    if (!match) invalidRegistry(file);
    const entry = tables[section[0]].get(section[1]);
    if (entry.has(match[1])) invalidRegistry(file);
    entry.set(match[1], match[2]);
  }
  return tables;
}

/** Synchronous, read-only inspection. No client process, network, or repair. */
export function diagnose(options = {}) {
  const report = { schema: SCHEMA, ok: false, issues: [], installations: [] };
  const aliases = [];
  const sourceProfiles = new Map();
  const capabilities = new Map();
  let entries = 0, bytes = 0;
  const issue = (code, message, file, action = REPAIR, extra = {}) => {
    report.issues.push({ code, severity: 'error', message, ...(file ? { path: file } : {}), action, ...extra });
  };
  const attempt = (fn, client) => {
    try { return fn(); } catch (error) {
      issue(error.code && error instanceof DiagnosticError ? error.code : 'READ_ERROR',
        error instanceof DiagnosticError ? error.message : 'Could not read an installation path.',
        error instanceof DiagnosticError ? error.file : undefined,
        error instanceof DiagnosticError ? error.action : 'Check directory access and retry; no files were changed.',
        client ? { client } : {});
      return null;
    }
  };
  const normalize = value => {
    if (!localPath(value)) throw new DiagnosticError('UNSAFE_PATH', 'Expected a local filesystem path.', undefined, PATH_ACTION);
    let absolute = path.resolve(value);
    for (const [alias, real] of aliases) {
      if (within(alias, absolute)) { absolute = real + absolute.slice(alias.length); break; }
    }
    return absolute;
  };
  const root = value => {
    const absolute = normalize(value);
    try {
      const real = fs.realpathSync(absolute);
      if (!fs.statSync(real).isDirectory()) throw new Error();
      aliases.push([absolute, real]);
      return real;
    } catch {
      throw new DiagnosticError('MISSING_ROOT', 'Home or source root is missing, unreadable, or not a directory.', absolute,
        'Pass --home and --source pointing to existing readable directories. Nothing is created automatically.');
    }
  };
  const stat = value => {
    const absolute = normalize(value);
    const anchor = aliases.map(([, real]) => real).find(base => within(base, absolute)) || path.parse(absolute).root;
    let cursor = anchor;
    let result = fs.lstatSync(cursor);
    for (const part of path.relative(anchor, absolute).split(path.sep).filter(Boolean)) {
      cursor = path.join(cursor, part);
      try { result = fs.lstatSync(cursor); } catch (error) {
        if (error.code === 'ENOENT') return null;
        throw new DiagnosticError('READ_ERROR', 'Cannot inspect this path; check access and directory types.', cursor);
      }
      if (result.isSymbolicLink()) throw new DiagnosticError('UNSAFE_PATH', 'Linked installation entries are not followed (including broken links and loops).', cursor, PATH_ACTION);
    }
    return result;
  };
  const read = value => {
    const file = normalize(value);
    const info = stat(file);
    if (!info || !info.isFile()) throw new DiagnosticError('MISSING_PAYLOAD', 'Expected a regular payload file.', file);
    if (info.size > MAX_FILE || bytes + info.size > MAX_TOTAL) {
      throw new DiagnosticError('SCAN_LIMIT', 'Diagnostic file/byte budget exceeded.', file,
        'Inspect this oversized input manually; provide a bounded SDC source/installation and retry.');
    }
    // O_NOFOLLOW prevents a last-component link swap after lstat. No writes occur.
    const fd = fs.openSync(file, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0));
    try {
      const opened = fs.fstatSync(fd);
      if (!opened.isFile() || opened.size !== info.size) throw new DiagnosticError('READ_ERROR', 'File changed while being inspected; retry.', file);
      const buffer = Buffer.alloc(opened.size + 1);
      let count = 0, amount;
      while (count < buffer.length && (amount = fs.readSync(fd, buffer, count, buffer.length - count, null)) > 0) count += amount;
      if (count !== opened.size) throw new DiagnosticError('READ_ERROR', 'File changed while being inspected; retry.', file);
      bytes += count;
      return buffer.subarray(0, count);
    } finally { fs.closeSync(fd); }
  };
  const json = (file, optional = false) => {
    if (optional && !stat(file)) return null;
    const raw = read(file);
    let value;
    try { value = JSON.parse(raw.toString('utf8')); } catch {
      throw new DiagnosticError('INVALID_JSON', 'Malformed JSON; configuration contents are omitted.', file, REGISTRY_ACTION);
    }
    if (!isObject(value)) invalidRegistry(file);
    return value;
  };
  const list = dir => {
    const info = stat(dir);
    if (!info) return [];
    if (!info.isDirectory()) throw new DiagnosticError('MISSING_PAYLOAD', 'Expected a directory.', dir);
    const handle = fs.opendirSync(dir);
    const names = [];
    try {
      let entry;
      while ((entry = handle.readSync())) {
        if (++entries > MAX_ENTRIES) throw new DiagnosticError('SCAN_LIMIT', 'Diagnostic directory-entry budget exceeded.', dir, 'Inspect excess entries manually and retry with a bounded installation.');
        if (!IGNORE.has(entry.name) && !/\.py[co]$/.test(entry.name)) names.push(entry.name);
      }
    } finally { handle.closeSync(); }
    return names.sort();
  };
  const addFile = (map, logical, file, helper = false) => {
    if (!stat(file)) throw new DiagnosticError(helper ? 'MISSING_HELPER' : 'MISSING_PAYLOAD',
      helper ? 'Required SDC runtime helper is missing.' : 'Required SDC payload is missing.', file);
    map.set(logical, crypto.createHash('sha256').update(read(file)).digest('hex'));
  };
  const tree = (map, dir, prefix, depth = 0) => {
    if (depth > MAX_DEPTH) throw new DiagnosticError('SCAN_LIMIT', 'Diagnostic depth budget exceeded.', dir, PATH_ACTION);
    if (!stat(dir)) throw new DiagnosticError('MISSING_PAYLOAD', 'Required payload directory is missing.', dir);
    for (const name of list(dir)) {
      const file = path.join(dir, name), logical = prefix + '/' + name;
      if (stat(file)?.isDirectory()) tree(map, file, logical, depth + 1);
      else addFile(map, logical, file);
    }
  };
  const relative = (base, value) => {
    if (!localPath(value) || path.isAbsolute(value) || value.split(/[\\/]/).includes('..')) {
      throw new DiagnosticError('UNSAFE_PATH', 'Plugin payload paths must stay inside their registered root.', base, PATH_ACTION);
    }
    const result = path.resolve(base, value);
    if (!within(base, result)) throw new DiagnosticError('UNSAFE_PATH', 'Plugin path escapes its root.', base, PATH_ACTION);
    return result;
  };
  const registered = (value, registry) => {
    if (!localPath(value) || !path.isAbsolute(value)) invalidRegistry(registry);
    return normalize(value);
  };
  const pluginId = id => {
    const parts = id.split('@');
    if (!['sdc', 'sdc-spec'].includes(parts[0])) return null;
    if (parts.length !== 2 || !safeName(parts[1])) invalidRegistry(undefined);
    return { name: parts[0], market: parts[1] };
  };
  const registerCapability = (client, capability, file) => {
    const key = client + ':' + capability;
    if (!capabilities.has(key)) capabilities.set(key, []);
    capabilities.get(key).push(file);
  };
  const skillsCapabilities = (client, dir, seen = new Set()) => {
    const registerSkill = (folder, name) => {
      const file = path.join(folder, 'SKILL.md');
      if (!stat(file) || seen.has(file)) return;
      seen.add(file);
      const body = read(file).toString('utf8');
      const match = body.match(/^---\r?\n[\s\S]*?^name:\s*["']?([\w-]+)["']?\s*$/m);
      let capability = match ? match[1] : name;
      if (capability === 'sdc-core') capability = 'sdc';
      if (capability === 'sdc' || capability.startsWith('sdc-')) registerCapability(client, capability, file);
    };
    registerSkill(dir, path.basename(dir));
    for (const name of list(dir)) {
      if (stat(path.join(dir, name))?.isDirectory()) registerSkill(path.join(dir, name), name);
    }
  };
  const skillPayload = (files, dir, profile) => {
    const required = profile === 'claude' ? ADVANCED : [...PUBLIC, ...ADVANCED];
    for (const name of required) addFile(files, `skills/sdc-${name}/SKILL.md`, path.join(dir, `sdc-${name}/SKILL.md`));
    for (const name of list(dir)) {
      if (name !== 'sdc' && !name.startsWith('sdc-')) continue;
      if (profile === 'claude' && PUBLIC.some(suffix => name === `sdc-${suffix}`)) continue;
      tree(files, path.join(dir, name), 'skills/' + name);
    }
  };
  const commandPayload = (files, dir) => {
    for (const name of PUBLIC) {
      const entry = `${name === 'core' ? 'sdc' : name}.md`;
      addFile(files, `commands/${entry}`, path.join(dir, entry));
    }
    tree(files, dir, 'commands');
  };
  let home, source, helpers;
  const expected = profile => {
    if (sourceProfiles.has(profile)) return sourceProfiles.get(profile);
    const files = new Map();
    for (const helper of helpers) addFile(files, helper, path.join(source, helper), true);
    tree(files, path.join(source, 'sdc-references'), 'sdc-references');
    skillPayload(files, path.join(source, 'skills'), profile);
    if (profile === 'claude') commandPayload(files, path.join(source, 'commands'));
    sourceProfiles.set(profile, files);
    return files;
  };
  const inspect = (client, kind, location, active, direct = false, provenance = null) => attempt(() => {
    const folder = normalize(location);
    if (!stat(folder)?.isDirectory()) throw new DiagnosticError('MISSING_INSTALLATION', 'Registered installation directory is missing.', folder);
    const item = { client, kind, path: folder, active, fingerprint: null, sourceFingerprint: null };
    report.installations.push(item);
    if (kind === 'legacy') issue('LEGACY_LAYOUT', 'Old direct SDC layout is still discoverable.', folder,
      'Review legacy skills/plugin copies before migrating; keep only one loader for each SDC capability.', { client, severity: 'warning' });
    const profile = !direct && client === 'claude' ? 'claude' : 'skills';
    const parent = direct ? path.dirname(folder) : folder;
    const runtime = direct ? path.join(parent, 'sdc-runtime') : folder;
    const skillRoot = direct ? folder : path.join(folder, 'skills');
    let skillScanRoots = [skillRoot];
    let hookFiles = [];
    if (!direct) {
      const manifestPath = path.join(folder, client === 'claude' ? '.claude-plugin' : '.codex-plugin', 'plugin.json');
      const manifest = json(manifestPath);
      if (!['sdc', 'sdc-spec'].includes(manifest.name)) invalidRegistry(manifestPath);
      if (client === 'codex' && manifest.skills !== './skills/' && manifest.skills !== './skills') invalidRegistry(manifestPath);
      if (client === 'claude') {
        if (manifest.commands !== undefined && !['./commands', './commands/'].includes(manifest.commands)) invalidRegistry(manifestPath);
        const values = manifest.skills === undefined ? [] : typeof manifest.skills === 'string' ? [manifest.skills] : manifest.skills;
        if (!Array.isArray(values) || values.some(value =>
          typeof value !== 'string' || !/^\.\/skills(?:\/sdc-[\w-]+)?\/?$/.test(value))) invalidRegistry(manifestPath);
        const declared = values.map(value => relative(folder, value));
        for (const dir of declared) {
          if (dir !== skillRoot) addFile(new Map(), dir, path.join(dir, 'SKILL.md'));
        }
        // Only registered marketplace-root provenance grants Claude's replacement
        // exception. Cached manifests and legacy copies cannot establish it.
        const replacesDefault = provenance?.rootSource === true && declared.length > 0 && declared.every(dir => dir !== skillRoot);
        skillScanRoots = replacesDefault ? declared : [skillRoot, ...declared];
      }
      // The portable Codex manifest uses [] to explicitly declare no hooks.
      if (manifest.hooks !== undefined && typeof manifest.hooks !== 'string' &&
        !(client === 'codex' && Array.isArray(manifest.hooks) && manifest.hooks.length === 0)) invalidRegistry(manifestPath);
      if (typeof manifest.hooks === 'string') {
        if (manifest.hooks !== (client === 'codex' ? './hooks/codex.json' : './hooks/hooks.json')) invalidRegistry(manifestPath);
        const hooks = relative(folder, manifest.hooks);
        json(hooks);
        hookFiles = client === 'codex' ? ['hooks/codex.json', 'hooks/codex-session-start.py'] : ['hooks/hooks.json', 'hooks/session-start'];
      }
      if (client === 'claude' && stat(path.join(source, 'hooks/hooks.json'))) hookFiles = ['hooks/hooks.json', 'hooks/session-start'];
      if (safeName(manifest.version)) item.version = manifest.version;
    }
    // A partial legacy copy can still be loaded, even when its runtime is broken.
    if (active) {
      const seen = new Set();
      for (const dir of skillScanRoots) attempt(() => skillsCapabilities(client, dir, seen), client);
      if (client === 'claude' && !direct) {
        for (const name of list(path.join(folder, 'commands'))) {
          if (name.endsWith('.md')) {
            const stem = name.slice(0, -3);
            registerCapability(client, stem === 'sdc' || stem.startsWith('sdc-') ? stem : 'sdc-' + stem, path.join(folder, 'commands', name));
          }
        }
      }
    }
    const canonical = new Map(sourcePayload(profile));
    if (profile === 'claude') {
      // Payload hashes alone cannot prove that Claude selects the skills on disk.
      const missing = [...canonical.keys()].filter(name => /^skills\/[^/]+\/SKILL\.md$/.test(name) &&
        !skillScanRoots.some(dir => dir === skillRoot || dir === path.dirname(path.join(folder, name)))).sort();
      if (missing.length) {
        issue('CONFIGURATION_DRIFT', 'Effective Claude skill selection omits entrypoints from the intended source profile.',
          path.join(folder, '.claude-plugin/plugin.json'), REPAIR,
          { client, missing: missing.slice(0, 30), missingCount: missing.length });
      }
    }
    item.sourceFingerprint = fingerprint(canonical);
    const actual = new Map();
    for (const hook of hookFiles) {
      if (!stat(path.join(source, hook))) throw new DiagnosticError('SOURCE_UNAVAILABLE', 'Source lacks the selected client hook payload.', source,
        'Pass --source pointing to the complete intended SDC distribution, including its client hook helpers.');
      addFile(canonical, hook, path.join(source, hook), true);
      addFile(actual, hook, path.join(folder, hook), true);
    }
    item.sourceFingerprint = fingerprint(canonical);
    for (const helper of helpers) addFile(actual, helper, path.join(runtime, helper), true);
    tree(actual, path.join(parent, 'sdc-references'), 'sdc-references');
    skillPayload(actual, skillRoot, profile);
    if (profile === 'claude') commandPayload(actual, path.join(folder, 'commands'));
    item.fingerprint = fingerprint(actual);
    if (item.fingerprint !== item.sourceFingerprint) {
      const changed = [...new Set([...canonical.keys(), ...actual.keys()])].filter(name => canonical.get(name) !== actual.get(name)).sort();
      issue('PAYLOAD_DRIFT', 'Critical payload differs from the selected source (versions are not freshness evidence).', folder, REPAIR,
        { client, changed: changed.slice(0, 30), changedCount: changed.length });
    }
  }, client);

  const sourcePayload = profile => {
    try { return expected(profile); } catch (error) {
      if (['MISSING_HELPER', 'MISSING_PAYLOAD'].includes(error.code)) {
        throw new DiagnosticError('SOURCE_UNAVAILABLE', 'Source lacks critical helpers, skills, references, or client workflow payload.', source,
          'Pass --source pointing to a complete intended SDC checkout or compatible plugin payload. A minimal direct runtime is not a comparison source.');
      }
      throw error;
    }
  };

  const marketplace = (client, marketRoot, name) => {
    const file = path.join(marketRoot, client === 'codex' ? '.agents/plugins/marketplace.json' : '.claude-plugin/marketplace.json');
    const data = json(file);
    if (!Array.isArray(data.plugins)) invalidRegistry(file);
    const matches = data.plugins.filter(entry => isObject(entry) && entry.name === name);
    if (matches.length !== 1) invalidRegistry(file);
    const entry = matches[0];
    let value = entry.source;
    if (client === 'codex' && isObject(value) && value.source === 'local') value = value.path;
    if (typeof value !== 'string' || /^[A-Za-z][A-Za-z0-9+.-]*:/.test(value)) {
      throw new DiagnosticError('UNSUPPORTED_SOURCE', 'Marketplace entry is not a supported local payload.', file,
        'Inspect the installed cache locally or use a local SDC marketplace; doctor never fetches remote sources.');
    }
    const pluginRoot = relative(marketRoot, value);
    const provenance = { rootSource: pluginRoot === marketRoot };
    inspect(client, 'marketplace', pluginRoot, false, false, provenance);
    return provenance;
  };

  const inspectCodex = () => {
    const config = path.join(home, '.codex/config.toml');
    const tables = stat(config) ? codexTables(read(config).toString('utf8'), config) : { plugins: new Map(), marketplaces: new Map() };
    for (const [id, settings] of tables.plugins) {
      const parsed = pluginId(id);
      if (!parsed) continue;
      attempt(() => {
        if (!['true', 'false'].includes(settings.get('enabled'))) invalidRegistry(config);
        if (settings.get('enabled') === 'false') return;
        const registration = tables.marketplaces.get(parsed.market);
        if (!registration) invalidRegistry(config);
        const type = tomlString(registration.get('source_type') || '', config);
        const marketRoot = registered(tomlString(registration.get('source') || '', config), config);
        if (type !== 'local') throw new DiagnosticError('UNSUPPORTED_SOURCE', 'Only local Codex marketplace registrations are supported.', config, REGISTRY_ACTION);
        attempt(() => marketplace('codex', marketRoot, parsed.name), 'codex');
        const cache = path.join(home, '.codex/plugins/cache', parsed.market, parsed.name);
        const versions = list(cache);
        if (!versions.length) throw new DiagnosticError('MISSING_INSTALLATION', 'Enabled Codex plugin has no cache payload.', cache);
        if (versions.length > 1) issue('AMBIGUOUS_CACHE', 'Multiple cache candidates exist; doctor cannot prove which one the client loads.', cache,
          'Review the client cache and retain the intended version through an approved reinstall; no highest-version guess is made.', { client: 'codex' });
        for (const version of versions) inspect('codex', 'cache', path.join(cache, version), true);
      }, 'codex');
    }
  };

  const inspectClaude = () => {
    const settingsPath = path.join(home, '.claude/settings.json');
    const settings = json(settingsPath, true);
    if (!settings) return;
    if (settings.enabledPlugins !== undefined && !isObject(settings.enabledPlugins)) invalidRegistry(settingsPath);
    const enabled = Object.entries(settings.enabledPlugins || {}).filter(([id]) => pluginId(id));
    for (const [id, value] of enabled) {
      if (typeof value !== 'boolean') invalidRegistry(settingsPath);
      if (!value) continue;
      attempt(() => {
        const parsed = pluginId(id);
        const knownFile = path.join(home, '.claude/plugins/known_marketplaces.json');
        const known = json(knownFile);
        const registration = known[parsed.market];
        if (!isObject(registration)) invalidRegistry(knownFile);
        const marketRoot = registered(registration.installLocation, knownFile);
        const provenance = attempt(() => marketplace('claude', marketRoot, parsed.name), 'claude');
        const installedFile = path.join(home, '.claude/plugins/installed_plugins.json');
        const installed = json(installedFile);
        if (!isObject(installed.plugins) || !Array.isArray(installed.plugins[id]) || !installed.plugins[id].length) invalidRegistry(installedFile);
        for (const record of installed.plugins[id]) {
          if (!isObject(record) || record.scope !== 'user') invalidRegistry(installedFile);
          inspect('claude', 'cache', registered(record.installPath, installedFile), true, false, provenance);
        }
      }, 'claude');
    }
  };

  const inspectDirect = client => {
    const roots = client === 'codex' ? ['.agents/skills', '.codex/skills'] :
      client === 'claude' ? ['.claude/skills'] : ['.hermes/skills/sdc', '.hermes/skills/sdc-spec'];
    for (const relativeRoot of roots) attempt(() => {
      const folder = path.join(home, relativeRoot);
      if (stat(folder) && (stat(path.join(folder, 'SKILL.md')) || list(folder).some(name => name === 'sdc' || name.startsWith('sdc-')))) {
        inspect(client, client === 'hermes' && relativeRoot.endsWith('/sdc') ? 'direct' : 'legacy', folder, true, true);
      }
    }, client);
    if (client === 'hermes') return;
    for (const name of ['sdc', 'sdc-spec']) {
      const folder = path.join(home, `.${client}/plugins`, name);
      attempt(() => { if (stat(folder)) inspect(client, 'legacy', folder, true); }, client);
    }
  };

  attempt(() => {
    if (!isObject(options)) throw new DiagnosticError('INVALID_ARGUMENT', 'diagnose expects an options object.', undefined, 'Pass {home, sourceRoot, clients?}.');
    const clients = options.clients === undefined ? CLIENTS : options.clients;
    if (!Array.isArray(clients) || !clients.length || clients.some(client => !CLIENTS.includes(client))) {
      throw new DiagnosticError('INVALID_ARGUMENT', 'clients must be a nonempty array of codex, claude, or hermes.', undefined, 'Select a supported client or omit clients for discovery.');
    }
    home = root(options.home === undefined ? process.env.HOME || process.env.USERPROFILE || os.homedir() : options.home);
    source = root(options.sourceRoot === undefined ? PACKAGE_ROOT : options.sourceRoot);
    helpers = [...HELPERS, ...OPTIONAL_HELPERS.filter(name => stat(path.join(source, name)))];
    for (const client of new Set(clients)) {
      if (client === 'codex') attempt(inspectCodex, client);
      if (client === 'claude') attempt(inspectClaude, client);
      inspectDirect(client);
      if (options.clients && !report.installations.some(item => item.client === client && item.active)) {
        issue('CLIENT_MISSING', 'No active SDC installation was found for the explicitly requested client.', undefined,
          'Install/enable SDC for this client with approval, or select a client that has SDC installed.', { client });
      }
    }
    for (const [key, locations] of capabilities) {
      if (locations.length < 2) continue;
      const [client, capability] = key.split(':');
      issue('DUPLICATE_CAPABILITY', 'The same SDC capability is discoverable through multiple entrypoints.', undefined,
        'Review the listed commands/skills and legacy registrations; retain one entrypoint per capability after approval.',
        { client, capability, paths: locations.slice(0, 30), count: locations.length });
    }
    if (!report.installations.some(item => item.active)) {
      issue('NO_INSTALLATIONS', 'No active SDC installation was diagnosed.', undefined,
        'Verify --home or install/enable SDC for one supported client with approval. Other clients are not required.');
    }
  });
  report.ok = !report.issues.some(item => item.severity === 'error');
  return report;
}

export function main(argv = process.argv.slice(2)) {
  const options = {};
  const asJson = argv.includes('--json');
  let report;
  try {
    for (let i = 0; i < argv.length; i++) {
      const flag = argv[i];
      if (flag === '--json') continue;
      if (!['--home', '--source', '--client'].includes(flag) || !argv[i + 1] || argv[i + 1].startsWith('--')) throw new Error();
      const value = argv[++i];
      if (flag === '--client') (options.clients || (options.clients = [])).push(value);
      else options[flag === '--home' ? 'home' : 'sourceRoot'] = value;
    }
    report = diagnose(options);
  } catch {
    report = { schema: SCHEMA, ok: false, issues: [{ code: 'INVALID_ARGUMENT', severity: 'error',
      message: 'Unknown option or missing option value.',
      action: 'Usage: node scripts/sdc-doctor.mjs [--json] [--home path] [--source path] [--client codex|claude|hermes]' }], installations: [] };
  }
  if (asJson) console.log(JSON.stringify(report, null, 2));
  else {
    console.log(`SDC installation diagnostics: ${report.ok ? 'OK' : 'BLOCKED'}`);
    for (const item of report.installations) console.log(`${item.client} ${item.kind}: ${JSON.stringify(item.path)}`);
    for (const item of report.issues) {
      console.log(`${item.severity} ${item.code}: ${item.message}${item.path ? ' ' + JSON.stringify(item.path) : ''}`);
      console.log(`  ${item.action}`);
    }
  }
  return report.ok ? 0 : 1;
}

let invokedDirectly = false;
try { invokedDirectly = fs.realpathSync(process.argv[1]) === fileURLToPath(import.meta.url); } catch { /* Imported, not a file entrypoint. */ }
if (invokedDirectly) process.exitCode = main();
