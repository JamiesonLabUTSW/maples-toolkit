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
