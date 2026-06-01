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
node scripts/audit-release.mjs
python3 evals/sdc-flow/run_sdc_flow.py
node --check bin/install.js
claude plugin validate .
npm pack --dry-run
```

## Local Install Test

```bash
node bin/install.js uninstall
node bin/install.js
claude plugin list
```

Expected:

- `sdc@sdc-local` appears in `claude plugin list`
- plugin version matches the release version
- Claude plugin cache contains `.claude/skills/sdc-spec/SKILL.md`
- Claude plugin cache contains `.claude/skills/sdc-shared/role-contracts.md`
- Claude plugin cache contains `commands/init.md`
- Claude local marketplace source does not contain a root `skills/` directory
- Claude generated skill directories contain only advanced non-public skills: `sdc-spec`, `sdc-implement`, `sdc-review`, `sdc-test`, `sdc-quality`, and `sdc-validate`
- Claude generated skill directories must not contain public command backing skills such as `sdc-init`, `sdc-change`, `sdc-plan`, `sdc-apply`, `sdc-check`, `sdc-archive`, `sdc-harness`, or `sdc-core`

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
Default Codex install should expose plugin skills (`sdc:*`) and should not leave stale `~/.agents/skills/sdc-*` direct skills unless `SDC_CODEX_DIRECT_SKILLS=1` was intentionally used. It should also remove the old direct plugin copy at `~/.codex/plugins/sdc`.

Archive output should include Knowledge Compact Gate and must not write optional decisions, standards, reports, AGENTS.md, project.md, or project-cognition.md updates without explicit confirmation.
It should also evaluate product knowledge, technical knowledge, memory, context-pack, and knowledge-candidate updates without silently writing conditional assets.

## Publish

```bash
npm publish
git tag vX.Y.Z
git push origin main --tags
```

Only publish after the release audit, npm dry run, and Claude validator pass.
