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

Run this suite from the source checkout; npm runtime packages do not distribute the unit-test files.

```bash
npm run sync:skills
npm test
python3 -m unittest discover -s tests -v
npm run audit
npm run eval:sdc
npm run package:codex -- --output /tmp/sdc-codex-plugin.zip
node --check bin/install.js
node --check bin/sdc.js
npm pack --dry-run --json
```

The Codex package command must run from a clean worktree for release builds. It should produce a rootless archive whose top level contains `.codex-plugin/`, `skills/`, runtime helpers, and license files. Building the same ref twice must produce the same SHA-256. Use `--allow-dirty` only for local verification.

Verify both Codex packaging modes: default portable packages omit native hooks; `SDC_CODEX_HOOKS=1` includes only the separate Codex hook configuration and wrapper. Source metadata uses `hooks: []` to suppress automatic Claude discovery. Both packages include the runtime helper and `sdc_evidence.py`. Force adapter failure and verify safe manual fallback; never auto-approve client hook trust.

## Local Install Test

```bash
node bin/install.js uninstall
node bin/install.js
claude plugin validate --strict "$HOME/.claude/plugins/marketplaces/sdc-local"
claude plugin list
```

Expected:

- `sdc@sdc-local` appears in `claude plugin list`
- plugin version matches the release version
- repository root and installed Claude marketplace both pass `claude plugin validate --strict`
- Claude plugin cache contains `skills/sdc-spec/SKILL.md`
- Claude plugin cache contains `sdc-references/role-contracts.md`
- Claude plugin cache contains `commands/init.md`
- Claude plugin cache contains the optional `hooks/hooks.json` and executable `hooks/session-start`
- Claude manifest explicitly lists only the six advanced paths under `skills/`: `sdc-spec`, `sdc-implement`, `sdc-review`, `sdc-test`, `sdc-quality`, and `sdc-validate`
- Claude install contains no generated `.claude/skills/` compatibility tree; the marketplace-root explicit-path rule replaces the default scan and prevents public workflow duplicates
- repository root `skills/` contains all public and advanced Codex skills, while shared contracts live in root `sdc-references/` rather than a fake `sdc-shared` skill
- Codex portable/native hook payloads match their explicit mode and include the shared runtime dependencies
- Legacy direct-skill and Hermes installs include their isolated `sdc-runtime/` helpers. Test initialization and context recovery from a separate project directory, then verify uninstall and direct-to-plugin migration remove only SDC-owned runtime files.

## Manual Smoke Test

After restarting Claude Code:

```text
/sdc:init
/sdc:change smoke-test
Cover the four intake categories using existing confirmed evidence; ask only missing blocking questions.
/sdc:plan
/sdc:apply
/sdc:check
/sdc:archive smoke-test
```

For Codex, verify SDC skills are visible in the model prompt context or through `/skills` where supported.
Default Codex install should expose public workflow plugin skills such as `sdc:sdc-init`, `sdc:sdc-change`, `sdc:sdc-plan`, `sdc:sdc-apply`, `sdc:sdc-check`, and `sdc:sdc-archive`. It should not leave stale `~/.agents/skills/sdc-*` direct skills unless `SDC_CODEX_DIRECT_SKILLS=1` was intentionally used. It should also remove the old direct plugin copy at `~/.codex/plugins/sdc`.

For an existing `.sdc/` workspace, run `python3 /path/to/installed/sdc/sdc-cli.py init` twice from the project directory. The first run may append `/runtime/` to `.sdc/.gitignore` while preserving custom entries; the second run must report that no files were overwritten.

Exercise the runtime contract with zero, one, and multiple active changes. Resolution must follow explicit argument, `SDC_ACTIVE_CHANGE`, valid session pointer, then sole active directory; invalid or ambiguous selection must exit non-zero without using directory recency.

Advance a fixture through `intake -> discovery -> confirmed -> planned -> applying -> checking -> archivable`, including rejected backward and skipped transitions. Generate `apply-context.jsonl` and `check-context.jsonl` twice and compare bytes, JSONL validity, ordering, safe paths, and current hashes.

Run Candidate recall against matching, non-matching, and sensitive fixtures. Confirm it is bounded, local, deterministic, read-only, and does not change knowledge, memory, state, or Git. Confirm research routes through existing stages only, with runtime scratch, cited notes, and `knowledge-candidates.md` remaining separate.

Also edit one fingerprinted managed fixture before init during migration testing. The modified file must be preserved and reported; exact known legacy templates should still upgrade with a backup.

Archive output should include Knowledge Compact Gate and must not write optional decisions, standards, reports, AGENTS.md, project.md, or project-cognition.md updates without explicit confirmation.
It should also evaluate product knowledge, technical knowledge, memory, context-pack, and knowledge-candidate updates without silently writing conditional assets.

## Publish

```bash
npm publish
git tag vX.Y.Z
git push origin main --tags
```

Only publish after the release audit, deterministic evals, `npm test`, both rootless Codex package modes, npm dry run, and Claude validator pass. Run representative real-agent trials separately; record model, source hashes, isolation limits, outcomes, and unknowns. Mock harness tests do not count as agent behavior evidence. State the source version and bump the release version before distributing changed payloads; do not publish a different payload under an existing version.
