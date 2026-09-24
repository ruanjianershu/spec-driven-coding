# Installation Diagnostics

Use this read-only sidecar from the existing SDC **check** or **init** routing
when installation freshness, missing runtime helpers, or duplicate capabilities
are in question. It does not introduce a public slash command, authorize a
repair, or establish that a project is ready for delivery.

## Invocation

Resolve the installed SDC root from the current command/skill, not the target
project's working directory. Verify the module exists before invoking it:

```sh
node "$SDC_PLUGIN_ROOT/scripts/sdc-doctor.mjs" --json --client claude
node "$SDC_PLUGIN_ROOT/scripts/sdc-doctor.mjs" --json --home "/path/to/home" --source "/path/to/intended/sdc" --client codex
```

The terminal router exposes the same operation through
`node bin/sdc.js check installation`, forwarding the options and exit status.
No separate public command or executable registration is needed. The `.mjs`
extension allows the module to run in portal/direct distributions without
`package.json` or a `bin/` directory.

When invoking the module inside an installed plugin, pass **the current client**
with `--client` (use `codex` in Codex, `claude` in Claude). A Claude distribution
can share Codex's generated public skill files without loading them in Claude;
discovery depends on its marketplace provenance and manifest paths below.
Source validation is performed only for profiles actually being diagnosed.
Codex portable/native sources do not need Claude commands or hook payloads.
For cross-client discovery/comparison, pass `--source` pointing to the complete
public SDC checkout/distribution containing the profiles for all selected
clients. Do not interpret an incompatible comparison source as a broken install.

- `--home` defaults to `HOME`, then `USERPROFILE`, then the OS home directory.
- `--source` defaults to the parent of the module's `scripts/` directory,
  independent of the working directory. Choose an independently trusted,
  intended distribution to detect stale installs; comparing a copy against
  itself is not proof that it is the latest release.
- `--client codex|claude|hermes` is repeatable. Omit it to discover supported
  installations. An explicitly selected client with no active SDC installation
  produces `CLIENT_MISSING`; an empty discovery produces `NO_INSTALLATIONS`.
  Installing all three clients is never required.
- Exit status is **0** with no blocking issues, **1** for blockers or invalid
  arguments. `--json` emits one report on stdout, without configuration dumps
  or stack traces. Plain output contains issue codes and suggested next steps.

The synchronous API is safe to import without running the CLI:

```js
import { diagnose } from './scripts/sdc-doctor.mjs';
const report = diagnose({ home, sourceRoot, clients: ['codex'] });
```

`diagnose()` returns exactly `{schema, ok, issues, installations}` with schema
`sdc.install-diagnostics/v1`. Each issue has `code`, `severity`, `message`, and
`action`, plus optional path/client or bounded duplicate/drift details. Each
installation identifies `client`, `kind`, absolute `path`, `active`,
`fingerprint`, and `sourceFingerprint`, with optional manifest `version`.
Fingerprints remain `null` when a payload cannot be completely inspected.
`ok` is true only when no issue has severity `error`. A `LEGACY_LAYOUT` warning
alone does not fail an otherwise complete, unique direct installation.

## Discovery Boundary

This is a local, user-home diagnostic for the layouts produced by `install.js`,
not a universal client configuration parser or a probe of a running client.
Like the current installer, the doctor uses fixed paths below `HOME` (or the
explicit `--home`): `.codex`, `.claude`, and `.hermes`. The installer does not
read `CODEX_HOME` or `CLAUDE_CONFIG_DIR`, and neither does the doctor. Those
environment variables therefore do not redirect its scan or prove which
configuration a running client uses. Project/local settings are not merged.

| Client | Inspected loading evidence |
| --- | --- |
| Codex | Enabled `plugins."sdc@marketplace"` (or legacy `sdc-spec`) tables in `.codex/config.toml`; corresponding local marketplace registration and `.agents/plugins/marketplace.json`; `.codex/plugins/cache/<marketplace>/<plugin>/<version>` candidates. |
| Claude | `enabledPlugins` in `.claude/settings.json`; matching `known_marketplaces.json` `installLocation` and marketplace entry; user-scope `installed_plugins.json` `installPath` records. The installed registry is authoritative, not a guessed cache directory. |
| Direct/legacy | Codex `.agents/skills` and `.codex/skills`; Claude `.claude/skills`; old `.codex/plugins/{sdc,sdc-spec}` and `.claude/plugins/{sdc,sdc-spec}`; Hermes `.hermes/skills/{sdc,sdc-spec}`. Direct layouts use sibling `sdc-references/` and `sdc-runtime/`. |

Only exact SDC plugin identities are selected from registries. Unrelated plugin
payloads are not scanned. Disabled plugins do not count as active, and stale
unregistered cache copies are not assumed to load. Codex cache selection with
multiple candidates is `AMBIGUOUS_CACHE`, never a highest-version/mtime guess.
Marketplace payloads are inspected for freshness but are not counted as a second
active installation of their cached plugin.

The bounded Codex TOML reader supports the installer's table form, quoted/bare
table names, literal/basic single-line strings, booleans, and comments. It keeps
unrelated multiline strings/arrays opaque. Unsupported relevant forms (such as
inline plugin maps or plugin arrays of tables) fail with `INVALID_REGISTRY`.
Assignment classification decodes the first key, so `"plugins"`/`'plugins'`
and `"marketplaces"`/`'marketplaces'` cannot hide inline or dotted registrations.
Unsupported quoted key syntax or escapes fail closed rather than allowing a
healthy installation of another client to mask an uninspected Codex registration.
Supported quoted table sections remain valid; dots inside a single quoted key
are literal characters, not namespace separators.
Remote sources, non-user Claude scopes, and custom component locations are not
silently treated as supported. Review such configurations with the client; the
doctor never accesses the network or rewrites them into a supported form.

## Payload And Duplicates

SHA-256 fingerprints bind sorted logical paths to file-content hashes. They
cover the core CLI, runtime-context/evidence/task-brief/review-package helpers,
SDC skill payloads, and shared references. The current CLI/runtime imports
`scripts/sdc_compact.py` and `scripts/sdc_findings.py`, so both are mandatory in
the source and installation, even when their absence would otherwise produce
equal hashes. Older runtime versions are not a separate supported profile.
The doctor module itself is also required and fingerprinted in the installation
when present in the chosen source.

Claude additionally compares commands and its conventional session hook pair;
an explicitly configured Codex native hook compares its own hook configuration
and helper. Portable Codex payloads do not require native hooks, commands,
`package.json`, or `bin/`. Generated public workflow skills are required for
Codex/direct layouts; Claude's command-based profile compares advanced skills
and commands instead. Versions are informational, not the freshness check.

Both the source and every inspected Claude plugin must contain all eight public
command entrypoints: `commands/{sdc,init,change,plan,apply,check,archive,harness}.md`.
Missing source commands produce `SOURCE_UNAVAILABLE`; missing installed commands
produce `MISSING_PAYLOAD` when the source is complete. An empty or equally damaged
command tree cannot pass by matching hashes, including when the installed cache
is selected explicitly or used as the default source. Shared Codex public skills
do not substitute for these Claude command entrypoints or change the
marketplace-root skill-selection exception below.

Manifest `hooks` may be absent or use the existing conventional string path:
`./hooks/codex.json` for Codex or `./hooks/hooks.json` for Claude. The corresponding
configuration and helper are still required and fingerprinted. Codex also accepts
`[]`, the shipped portable manifest's explicit no-hook declaration. Other forms
fail with `INVALID_REGISTRY`, including nonempty arrays (even of conventional
paths), inline objects, `null`, booleans, numbers, empty strings, and Claude's
empty array. These forms are not interpreted as disabled hooks, followed as
paths, or allowed to bypass missing-helper checks. This is a conservative
diagnostic boundary, not a claim that clients cannot support additional forms.

Missing core source helpers, skills, references, or required client payloads
produce `SOURCE_UNAVAILABLE` with an explicit `--source` recovery instruction.
A minimal Hermes/direct `sdc-runtime/` distribution can execute the doctor but
cannot serve as a complete comparison source: pass an explicit full `--source`.
`SOURCE_UNAVAILABLE` says the comparison cannot be made, not that the installed
runtime is necessarily broken. The absence of `package.json` alone is fine.

Duplicate detection normalizes `sdc-core` to `sdc`, and command `init` to
`sdc-init` (likewise for the other workflows). Claude's `skills` paths normally
add to default discovery. When the registered marketplace entry's `source`
resolves to the marketplace root, a list of specific skill subdirectories
replaces the default scan instead. This follows the official
[Claude plugin path behavior rules](https://code.claude.com/docs/en/plugins-reference#path-behavior-rules).

The doctor carries that resolved provenance from `known_marketplaces.json` and
the selected marketplace entry to its active cache. It does not infer provenance
from a cached marketplace file, the chosen comparison source, or a legacy copy.
SDC's `source: "./"` and explicit six advanced skill paths therefore coexist
with shared Codex public skills without creating Claude duplicates. No installer
restructure or removal of those shared files is needed.

For nonroot/legacy/direct layouts the default scan remains additive; an absent,
empty, or broad `skills/` declaration does not trigger the exception. The same
file found through overlapping default and declared paths is counted once per
installation. Distinct loaded skills with the same name, explicit public skill
paths overlapping commands, and partial legacy copies still produce duplicate
findings. Codex's inert copied `commands/` directory is not counted as a loaded
slash-command surface. Findings describe on-disk loading evidence, not proof of
a particular running client's UI state.

Matching payload fingerprints do not establish loading completeness. For each
Claude plugin copy, the doctor also checks the intended source profile's skill
entrypoints against the effective scan roots above. This covers all six advanced
skills and any additional nonpublic SDC skill entrypoints in that source. A
marketplace or cache manifest selecting only `./skills/sdc-spec` at a registered
marketplace root produces blocking `CONFIGURATION_DRIFT`, even when every file
is present and both payload fingerprints match. The finding identifies the
manifest and lists omitted logical entrypoint paths in `missing`, capped at 30,
with the full `missingCount`.

This is an effective-selection check, not a raw manifest comparison: reordering
or repeating equivalent paths, trailing slashes, and unrelated metadata do not
create drift. Empty/absent/broad declarations and nonroot subsets still use the
default scan; they pass when the intended skills load uniquely, and still report
duplicates when public skills overlap commands.

## Safety And Recovery

No files are written, no client/runtime processes or hooks are executed, and no
repair, installation, network call, or configuration migration is performed.
Reports include only installation paths, safe manifest versions, hashes, issue
codes, and bounded path/capability details, never settings values or raw parser
exceptions. Paths with spaces are passed as normal arguments, not shell text.

Explicit home/source roots are canonicalized, including OS path aliases.
Descendant installation/payload symlinks are rejected with `UNSAFE_PATH`, even
if internal, broken, or cyclic. Relative marketplace/component paths may not
traverse out of their registered root. Registry-specified absolute local
directories may be outside the selected home. The scanner is read-only, not a
security sandbox or atomic snapshot against concurrently changing directories;
retry after the installer/client finishes changing them.

Limits per diagnosis: **4 MiB per file**, **64 MiB total bytes read**,
**16,384 enumerated directory entries**, and **16 recursive payload levels**.
Exceeding a limit produces `SCAN_LIMIT`; inaccessible or unstable files produce
an actionable read error. Duplicate paths and changed-file lists are capped at
30 entries, with total counts retained. No recursive home scan is performed.

For `PAYLOAD_DRIFT`, `CONFIGURATION_DRIFT`, `MISSING_HELPER`,
`MISSING_INSTALLATION`, or duplicate registrations, review the affected paths
and intended source with the user.
Obtain approval before an installer update, cache cleanup, settings edit, or
removal of a legacy directory. After repair, restart the client and rerun this
diagnostic. A passing report does not grant hook trust or replace normal SDC
project validation, review, or delivery gates.

## Integration And Verification

The npm, portal, and direct-runtime payloads bundle `scripts/sdc-doctor.mjs`.
Keep complete skills/references available as the comparison source or pass
`--source` explicitly. Existing check/init routing preserves structured
failures and the installer/repair consent boundary. Keep generated skills
synchronized with commands before comparing a newly built distribution.

Run the real-subprocess regression suite with isolated fake homes and source
roots:

```sh
python3 -B -m unittest evals.test_install_diagnostics -v
node --check scripts/sdc-doctor.mjs
```

The suite covers the real installer's Claude/Codex/Hermes layouts, a standalone
module without package metadata, enabled Claude registries and marketplace-root
discovery, same-version drift, effective skill selection against the source,
missing individual/all public commands with selected/default sources, required
runtime modules, supported optional hooks and rejected hook forms, true duplicates,
absent clients, quoted Codex inline/dotted registrations alongside healthy Hermes,
malformed input, unrelated plugins, bounds,
and unsafe paths. Fixtures compare source/home
content and modification times before/after diagnosis to detect writes.
