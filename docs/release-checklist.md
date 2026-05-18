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
- Claude plugin cache contains `.claude/skills/init/SKILL.md`
- Claude plugin cache contains `.claude/skills/sdc-shared/role-contracts.md`
- Claude plugin cache contains `commands/init.md`
- Claude local marketplace source does not contain a root `skills/` directory; only `.claude/skills/` should be exposed to Claude Code

## Manual Smoke Test

After restarting Claude Code:

```text
/sdc:init
/sdc:change smoke-test
/sdc:plan
/sdc:check
```

For Codex, verify SDC skills are visible in the model prompt context or through `/skills` where supported.

## Publish

```bash
npm publish
git tag vX.Y.Z
git push origin main --tags
```

Only publish after the npm dry run and Claude validator pass.
