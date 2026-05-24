# Repository Instructions

## Project Shape

This repository is a Codex CLI and Claude Code plugin marketplace.

- Codex marketplace: `.agents/plugins/marketplace.json`
- Claude Code marketplace: `.claude-plugin/marketplace.json`
- Plugin folders: `plugins/<plugin-name>/`
- Installable Rubric Maker plugin: `plugins/rubric-maker-skill/`
- Placeholder plugins: `plugins/case-generation/`, `plugins/validation-analysis/`

Each plugin must remain self-contained.
Do not add plugin instructions that depend on files outside that plugin folder unless
the same file is also bundled inside the plugin.

Root files describe marketplace behavior.
Plugin-specific instructions belong in each plugin directory.
Rubric Maker has its own instructions at `plugins/rubric-maker-skill/AGENTS.md`; follow
those when editing Rubric Maker skills, schemas, or plugin-local scripts.

## Marketplace Requirements

Every installable plugin entry in `.agents/plugins/marketplace.json` must:

- Use `source.source: "local"`.
- Use a `source.path` that starts with `./` and points inside `plugins/`.
- Include `policy.installation`, `policy.authentication`, and `category`.
- Have a matching plugin directory with `.codex-plugin/plugin.json`.

Every plugin entry in `.claude-plugin/marketplace.json` must point to the same plugin
directory and have a matching `.claude-plugin/plugin.json`. Claude marketplace entries
should include `description`, `author`, `category`, and `homepage` so the root
marketplace remains useful as a catalog, not only as a loader.
Because Claude Code marketplace entries are installable entries and do not have a
Codex-style `NOT_AVAILABLE` policy, do not list placeholder-only plugins in
`.claude-plugin/marketplace.json`.

Placeholder plugins must stay marked as unavailable in the Codex marketplace until they
contain real plugin surfaces.

When adding a new plugin:

- Create `plugins/<plugin-name>/`.
- Add `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`.
- Add `README.md` and `requirements.txt`, even if the requirements file only documents
  that there are no Python dependencies yet.
- Add a Codex marketplace entry.
  Use `NOT_AVAILABLE` until the plugin has real skills, commands, agents, hooks, MCP
  configuration, scripts, or other runtime surfaces.
- Add a Claude marketplace entry only when the plugin is genuinely installable.

## Dependency Policy

Each plugin owns its runtime requirements in `plugins/<plugin-name>/requirements.txt`.

The root `requirements.txt` is only a compatibility shim for current root-level
workflows.
Do not add future plugin-specific packages only to the root requirements file.

Root developer-only tooling belongs in the root `pyproject.toml` `dev` dependency group,
not in plugin runtime requirements.
The current dev tools are Ruff, ty, Flowmark, and pre-commit.
Use `make dev-install` to create `.venv/` and install the dev group with pip, or install
the same dependency group with another PEP 735-compatible tool.
`uv` is optional and must not become the only documented way to run checks.

## Developer Checks

Use the root `Makefile` for repeatable local checks:

```bash
make check
```

`make check` runs Ruff lint, Ruff format check, Flowmark lint, ty, and the marketplace
smoke/compatibility checks.
Focused targets include `make python-check`, `make markdown-check`, `make lint`,
`make format-check`, `make typecheck`, and `make format`.

Use `make pre-commit-install` to install local pre-commit hooks.
The hooks should stay fast and non-mutating; they run Makefile-backed lint,
format-check, and type-check targets.

Pull requests targeting `main` run `.github/workflows/ci.yml`. Keep CI jobs topical and
parallelizable where possible, and run checks through Makefile targets rather than raw
tool commands.

Do not run raw `flowmark --auto` on this repository.
The Flowmark version used by the dev dependency group expands `--auto` to include smart
quotes and ellipsis conversion, which is unsafe for Markdown files that document exact
YAML, JSON, TOML, shell, or schema syntax.
Use `make flowmark-format` and `make flowmark-lint`, which run Flowmark with
`--semantic --cleanups --width 88 --list-spacing preserve`.

When Flowmark changes Rubric Maker schema or contract copies, run the schema sync checks
before finishing because those files must remain byte-for-byte aligned.

## Rubric Maker Compatibility Requirements

Rubric Maker-specific schema and validator checks live under
`plugins/rubric-maker-skill/`.

`plugins/rubric-maker-skill/references/rubric-schema.md` is the canonical bundled
schema. Every Rubric Maker skill-local `references/rubric-schema.md` copy must match it
exactly.

`plugins/rubric-maker-skill/references/grade-sheet-contract.md` is the canonical bundled
grade-sheet schema. Every Rubric Maker skill-local `references/grade-sheet-contract.md`
copy must match it exactly.
Every Rubric Maker skill with a grade-sheet contract must also bundle
`scripts/validate_grade_sheet.py`, and copied grade-sheet validators must match the
canonical validator from
`plugins/rubric-maker-skill/skills/grading-dry-run/scripts/validate_grade_sheet.py`.

Before pushing marketplace or Rubric Maker changes, run from the repository root:

```bash
make check
```

If running checks manually, use:

```bash
python3 scripts/verify_plugin_compat.py
python3 scripts/verify_schema_sync.py
python3 scripts/verify_grade_sheet_schema_sync.py
python3 scripts/smoke_test.py
```

Treat any failing check as a blocking issue.

The root scripts in `scripts/` are compatibility wrappers or marketplace validators.
Preserve these root entry points unless there is a deliberate migration plan, because
existing documentation and users may run validation from the marketplace root.

If the Rubric Maker canonical schema changes, update every Rubric Maker skill-local
schema copy:

```bash
for d in plugins/rubric-maker-skill/skills/*/references; do
  cp plugins/rubric-maker-skill/references/rubric-schema.md "$d/rubric-schema.md"
done
python3 scripts/verify_schema_sync.py
```

If the grade-sheet contract changes, update every Rubric Maker skill-local grade-sheet
contract copy:

```bash
for d in plugins/rubric-maker-skill/skills/*/references; do
  if [ -f "$d/grade-sheet-contract.md" ]; then
    cp plugins/rubric-maker-skill/references/grade-sheet-contract.md "$d/grade-sheet-contract.md"
  fi
done
python3 scripts/verify_grade_sheet_schema_sync.py
```

If the grade-sheet validator changes, update every Rubric Maker skill-local validator
copy:

```bash
for d in plugins/rubric-maker-skill/skills/*/scripts; do
  if [ -f "$d/validate_grade_sheet.py" ]; then
    cp plugins/rubric-maker-skill/skills/grading-dry-run/scripts/validate_grade_sheet.py "$d/validate_grade_sheet.py"
  fi
done
python3 scripts/verify_grade_sheet_schema_sync.py
```

## Packaging Hygiene

- Do not commit generated `*.zip` skill packages.
- Do not commit `.DS_Store`, caches, local virtual environments, logs, or generated
  output directories.
- Do not commit `.copilot-tracking/`; it is local HVE workflow state and is ignored.
- Keep root marketplace metadata aligned with per-plugin manifests.
- Keep plugin `name` manifest fields aligned with plugin directory names.
- Keep skill `name` frontmatter equal to its directory name.
