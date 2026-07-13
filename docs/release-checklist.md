# Release Checklist

Use this checklist before publishing a new SDC version or submitting to a marketplace.

## Versioning

- Update `package.json`
- Update `.claude-plugin/plugin.json`
- Update `.claude-plugin/marketplace.json`
- Update `.codex-plugin/plugin.json`
- Update `CHANGELOG.md`

Claude Code uses the plugin version as a cache key. If the version is not bumped, users may not receive updates even when the repository changes.

## Validation

```bash
npm run sync:skills
npm run audit
npm run eval:sdc
npm run package:codex -- --output /tmp/sdc-codex-plugin.zip
node --check bin/install.js
npm pack --dry-run --json
```

The Codex package command must run from a clean worktree for release builds. It should produce a rootless archive whose top level contains `.codex-plugin/`, `skills/`, runtime helpers, and license files. Building the same ref twice must produce the same SHA-256. Use `--allow-dirty` only for local verification.

Keep `.codex-plugin/plugin.json` at exact `"hooks": {}`. Superpowers v6.1.1 documents that an absent field or list value can trigger Codex hook auto-discovery; older generic scaffold validators may not yet recognize this current portal exception.

## Local Install Test

```bash
node bin/install.js uninstall
node bin/install.js
claude plugin validate "$HOME/.claude/plugins/marketplaces/sdc-local"
claude plugin list
```

Expected:

- `sdc@sdc-local` appears in `claude plugin list`
- plugin version matches the release version
- Claude plugin cache contains `.claude/skills/sdc-spec/SKILL.md`
- Claude plugin cache contains `.claude/sdc-references/role-contracts.md`
- Claude plugin cache contains `commands/init.md`
- Claude local marketplace source does not contain a root `skills/` directory
- Claude generated skill directories contain only advanced non-public skills: `sdc-spec`, `sdc-implement`, `sdc-review`, `sdc-test`, `sdc-quality`, and `sdc-validate`
- Claude generated skill directories must not contain public command backing skills such as `sdc-init`, `sdc-change`, `sdc-plan`, `sdc-apply`, `sdc-check`, `sdc-archive`, `sdc-harness`, or `sdc-core`
- repository root `skills/` contains all public and advanced Codex skills, while shared contracts live in root `sdc-references/` rather than a fake `sdc-shared` skill

## Manual Smoke Test

After restarting Claude Code:

```text
/sdc:init
/sdc:change smoke-test
Confirm the four intake answers before expecting any change files.
/sdc:plan
/sdc:check
/sdc:archive smoke-test
```

For Codex, verify SDC skills are visible in the model prompt context or through `/skills` where supported.
Default Codex install should expose public workflow plugin skills such as `sdc:sdc-init`, `sdc:sdc-change`, `sdc:sdc-plan`, `sdc:sdc-apply`, `sdc:sdc-check`, and `sdc:sdc-archive`. It should not leave stale `~/.agents/skills/sdc-*` direct skills unless `SDC_CODEX_DIRECT_SKILLS=1` was intentionally used. It should also remove the old direct plugin copy at `~/.codex/plugins/sdc`.

For an existing `.sdc/` workspace, run `sdc init` twice. The first run may append `/runtime/` to `.sdc/.gitignore` while preserving custom entries; the second run must report that no files were overwritten.

Also edit one fingerprinted managed fixture before init during migration testing. The modified file must be preserved and reported; exact known legacy templates should still upgrade with a backup.

Archive output should include Knowledge Compact Gate and must not write optional decisions, standards, reports, AGENTS.md, project.md, or project-cognition.md updates without explicit confirmation.
It should also evaluate product knowledge, technical knowledge, memory, context-pack, and knowledge-candidate updates without silently writing conditional assets.

## Publish

```bash
npm publish
git tag vX.Y.Z
git push origin main --tags
```

Only publish after the release audit, deterministic evals, rootless Codex package check, npm dry run, and Claude validator pass.
