# Repository Instructions

## Project Shape

This repository is a Codex CLI and Claude Code plugin marketplace.

- Codex marketplace: `.agents/plugins/marketplace.json`
- Claude Code marketplace: `.claude-plugin/marketplace.json`
- Plugin folders: `plugins/<plugin-name>/`
- Installable Rubric Maker plugin: `plugins/rubric-maker-skill/`
- Placeholder plugins: `plugins/case-generation/`, `plugins/validation-analysis/`

Each plugin must remain self-contained. Do not add plugin instructions that depend on files outside that plugin folder unless the same file is also bundled inside the plugin.

## Marketplace Requirements

Every installable plugin entry in `.agents/plugins/marketplace.json` must:

- Use `source.source: "local"`.
- Use a `source.path` that starts with `./` and points inside `plugins/`.
- Include `policy.installation`, `policy.authentication`, and `category`.
- Have a matching plugin directory with `.codex-plugin/plugin.json`.

Every plugin entry in `.claude-plugin/marketplace.json` must point to the same plugin directory and have a matching `.claude-plugin/plugin.json`.

Placeholder plugins must stay marked as unavailable in the Codex marketplace until they contain real plugin surfaces.

## Rubric Maker Compatibility Requirements

Rubric Maker-specific schema and validator checks live under `plugins/rubric-maker-skill/`.

`plugins/rubric-maker-skill/references/rubric-schema.md` is the canonical bundled schema. Every Rubric Maker skill-local `references/rubric-schema.md` copy must match it exactly.

`plugins/rubric-maker-skill/references/grade-sheet-contract.md` is the canonical bundled grade-sheet schema. Every Rubric Maker skill-local `references/grade-sheet-contract.md` copy must match it exactly. Every Rubric Maker skill with a grade-sheet contract must also bundle `scripts/validate_grade_sheet.py`, and copied grade-sheet validators must match the canonical validator from `plugins/rubric-maker-skill/skills/grading-dry-run/scripts/validate_grade_sheet.py`.

Before pushing marketplace or Rubric Maker changes, run from the repository root:

```bash
python3 scripts/verify_plugin_compat.py
python3 scripts/verify_schema_sync.py
python3 scripts/verify_grade_sheet_schema_sync.py
python3 scripts/smoke_test.py
```

Treat any failing check as a blocking issue.

If the Rubric Maker canonical schema changes, update every Rubric Maker skill-local schema copy:

```bash
for d in plugins/rubric-maker-skill/skills/*/references; do
  cp plugins/rubric-maker-skill/references/rubric-schema.md "$d/rubric-schema.md"
done
python3 scripts/verify_schema_sync.py
```

If the grade-sheet contract changes, update every Rubric Maker skill-local grade-sheet contract copy:

```bash
for d in plugins/rubric-maker-skill/skills/*/references; do
  if [ -f "$d/grade-sheet-contract.md" ]; then
    cp plugins/rubric-maker-skill/references/grade-sheet-contract.md "$d/grade-sheet-contract.md"
  fi
done
python3 scripts/verify_grade_sheet_schema_sync.py
```

If the grade-sheet validator changes, update every Rubric Maker skill-local validator copy:

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
- Do not commit `.DS_Store`, caches, local virtual environments, logs, or generated output directories.
- Keep root marketplace metadata aligned with per-plugin manifests.
- Keep plugin `name` manifest fields aligned with plugin directory names.
- Keep skill `name` frontmatter equal to its directory name.
