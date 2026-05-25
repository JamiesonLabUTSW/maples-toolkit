# Contributing

This repository uses Makefile targets as the stable interface for local development,
pre-commit, and CI.

## Developer Tooling

Developer-only tooling is declared in the root `pyproject.toml` `dev` dependency group.
This includes Ruff for Python linting/formatting, ty for type checking, Flowmark for
Markdown formatting, and pre-commit for local hooks.

Install the development tools into a local virtual environment:

```bash
make dev-install
```

That target creates `.venv/`, upgrades pip inside it, and installs the root `dev`
dependency group. The Makefile prefers tools from `.venv/bin/` and falls back to tools
already on `PATH`. `uv` is not required; developers who already use it can still run
equivalent commands with `uv run` or override Make variables such as
`RUFF="uv run ruff"`.

Install the local pre-commit hook after installing developer tools:

```bash
make pre-commit-install
```

The hook runs fast, non-mutating Makefile checks before each commit:
`make python-check`, `make markdown-check`, and `make typecheck`.

## Formatting And Checks

Run the full local gate from the repository root:

```bash
make check
```

Common focused targets:

```bash
make lint
make python-check
make markdown-check
make format-check
make typecheck
make format
```

`make format` runs Ruff formatting for Python and Flowmark formatting for Markdown.
Do not run raw `flowmark --auto` in this repository.
In current Flowmark versions, `--auto` also enables smart quotes and ellipsis
conversion, which is too risky for Markdown files that document YAML, JSON, TOML, shell
commands, and other exact syntax.
Use the Makefile targets so Flowmark runs with the repository settings:
`--semantic --cleanups --width 88 --list-spacing preserve`.

## CI

Pull requests targeting `main` run `.github/workflows/ci.yml`.

The workflow uses current first-party GitHub actions and splits checks into topical jobs
that can run in parallel:

- `make python-check`: Ruff lint and Ruff format check.
- `make markdown-check`: Flowmark lint.
- `make typecheck`: ty type checking.
- `make smoke`: marketplace compatibility, schema sync, grade-sheet sync, and smoke
  validation.

CI does not run mutating formatters.
Run `make format` locally when formatting changes are needed.

## Validation

Run the marketplace compatibility checks through Makefile targets:

```bash
make marketplace-check
make schema-sync-check
make grade-sheet-sync-check
make plugin-smoke
```

These checks are also included in `make smoke` and `make check`.

Validate the Rubric Maker plugin package directly:

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/rubric-maker-skill
```

Validate all Rubric Maker skills:

```bash
for d in plugins/rubric-maker-skill/skills/*/; do
  if [ -f "$d/SKILL.md" ]; then
    python3 /path/to/skill-creator/scripts/quick_validate.py "$d" || exit 1
  fi
done
```

## Versioning And Releases

This repository is a plugin marketplace, not a single application.
Release units are independent:

- Plugin release unit: `plugins/<plugin-name>/`.
- Marketplace/catalog release unit: root marketplace metadata, repository release
  automation, and repository-level docs/tooling.

Rubric Maker is currently the only installable plugin release unit.
`case-generation` and `validation-analysis` are placeholders and must not receive public
release tags or GitHub Releases while their Codex marketplace policy remains
`NOT_AVAILABLE`.

### Version Sources Of Truth

Plugin versions are sourced from the plugin manifests:

- `plugins/<plugin-name>/.codex-plugin/plugin.json`
- `plugins/<plugin-name>/.claude-plugin/plugin.json`

Keep those two manifest versions identical.
Do not duplicate an installable plugin's version in `.claude-plugin/marketplace.json`;
Claude Code uses the plugin manifest version as the install cache key, and duplicate
marketplace-entry versions can create ambiguous release state.

The root Claude marketplace `version` is the marketplace/catalog version.
It is bumped only for catalog-level changes.
The Codex marketplace does not duplicate plugin versions unless the Codex schema later
requires that field.

### SemVer Rules

Plugin releases use Semantic Versioning:

- `PATCH`: documentation fixes, typo fixes, non-breaking prompt wording improvements,
  and script or validator bug fixes that preserve contracts.
- `MINOR`: new skills, scripts, optional capabilities, expanded schema support, or
  backwards-compatible rubric behavior.
- `MAJOR`: renamed or removed skills, changed required inputs or outputs, incompatible
  schema or grade-sheet contract changes, changed install behavior, or new breaking
  auth/setup requirements.

Marketplace/catalog releases also use Semantic Versioning:

- `PATCH`: catalog metadata fixes, docs typo fixes, and non-breaking validation fixes.
- `MINOR`: new installable plugin entries, new marketplace validation features, new
  release automation, or new contributor workflows.
- `MAJOR`: incompatible marketplace structure, changed install policy semantics, removed
  installable plugin entries, or breaking repository layout changes.

### Changelog Policy

Every release unit owns a changelog:

- `CHANGELOG.md` covers marketplace/catalog/tooling/docs changes.
- `plugins/<plugin-name>/CHANGELOG.md` covers user-visible plugin behavior and
  install-surface changes.
- `.changelog-template.md` is the template for new release-unit changelogs.

Use Keep a Changelog headings with an `Unreleased` section and these categories:
`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and `Security`.

Every PR that changes `plugins/<plugin-name>/**` must update that plugin's changelog
unless the PR is explicitly marked `no-release`. Rubric Maker changelog entries must
call out schema, grade-sheet contract, validator, and skill input/output compatibility
changes when those surfaces are affected.

Every PR that changes root marketplace files, release tooling, CI release automation, or
root release policy docs must update `CHANGELOG.md` unless the PR is explicitly marked
`no-release`.

### Repository Labels

Release automation and triage use these GitHub labels:

- `release`
- `documentation`
- `automation`
- `marketplace`
- `plugin:rubric-maker-skill`
- `plugin:case-generation`
- `plugin:validation-analysis`
- `no-release`

Use `no-release` only when a PR does not need a user-facing changelog entry.

### Tag Naming

Use annotated, namespaced tags:

```bash
git tag -a rubric-maker-skill/v0.1.0 -m "Release rubric-maker-skill v0.1.0"
git tag -a marketplace/v0.1.0 -m "Release marketplace v0.1.0"
```

Rules:

- Use exact SemVer tags for real releases.
- Use plugin tags only for installable plugin releases.
- Use `marketplace/vX.Y.Z` for catalog-level releases.
- Do not create public release tags for placeholder plugins.
- Multiple release tags may point to the same commit if one PR intentionally releases
  multiple plugins or catalog changes.
- Do not create moving aliases such as `rubric-maker-skill/v1` yet.
  Revisit this only if consumers need floating release channels.

### Release PR Checklist

Before merging a release-impacting PR:

- Decide whether the change affects a plugin release, marketplace release, both, or no
  release.
- Apply the correct SemVer bump to the release unit's source of truth.
- Update the relevant changelog under `Unreleased` or add the final release heading.
- Confirm marketplace metadata and install policy are aligned with the release unit.
- For plugin changes, check schema, grade-sheet contracts, validators, skills, commands,
  hooks, MCP configuration, executable scripts, and auth/setup requirements.
- Run `make check`.
- Run the applicable release readiness target.

### Release Readiness Commands

Version and changelog checks are stable Makefile targets:

```bash
make version-check
make changelog-check
```

Check an installable plugin release:

```bash
make release-check PLUGIN=rubric-maker-skill VERSION=0.1.0
```

Check a marketplace/catalog release:

```bash
make release-check-marketplace VERSION=0.1.0
```

Release readiness checks are non-mutating by default.
They validate metadata, changelog entries, packaging hygiene, tag state, and
`make check`; they do not create tags or publish releases.
The default tag check expects the release tag not to exist yet, which supports pre-tag
release preparation.

### Maintainer Release Procedure

After the release PR is merged and CI is green:

1. Pull the latest `main`.
2. Run `make check`.
3. Run `make release-check PLUGIN=<plugin-name> VERSION=<x.y.z>` for plugin releases or
   `make release-check-marketplace VERSION=<x.y.z>` for catalog releases.
4. Create an annotated namespaced tag.
5. Push the tag.
6. Create a GitHub Release titled `<release-unit> v<x.y.z>` using the matching changelog
   entry as release notes.

Example Rubric Maker bootstrap release:

```bash
make release-check PLUGIN=rubric-maker-skill VERSION=0.1.0
git tag -a rubric-maker-skill/v0.1.0 -m "Release rubric-maker-skill v0.1.0"
git push origin rubric-maker-skill/v0.1.0
```

Example marketplace bootstrap release:

```bash
make release-check-marketplace VERSION=0.1.0
git tag -a marketplace/v0.1.0 -m "Release marketplace v0.1.0"
git push origin marketplace/v0.1.0
```

### Placeholder Plugins

Placeholder plugins remain visible only in the Codex marketplace with
`policy.installation: "NOT_AVAILABLE"`. They may keep manifest versions for local
metadata compatibility, but those versions are not public release promises.
Placeholder plugin changelogs should say `No Public Releases Yet`.

To promote a placeholder plugin:

1. Add real runtime surfaces such as skills, commands, scripts, hooks, MCP config, or
   documented setup behavior.
2. Ensure the plugin is self-contained and has `README.md`, `requirements.txt`, and
   `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`.
3. Add or update the plugin changelog with an initial release entry.
4. Change the Codex marketplace policy to `AVAILABLE`.
5. Add the plugin to `.claude-plugin/marketplace.json` without a plugin-entry `version`.
6. Run `make check`.
7. Run `make release-check PLUGIN=<plugin-name> VERSION=<x.y.z>`.
8. After merge, create the first namespaced plugin tag and GitHub Release.
