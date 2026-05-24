# Repository Instructions

## Project Shape

This repository packages Rubric Maker skills for Codex CLI and Claude Code.

- Codex plugin manifest: `.codex-plugin/plugin.json`
- Claude Code plugin manifest: `.claude-plugin/plugin.json`
- Skill folders: `skills/<skill-name>/`
- Canonical rubric schema: `references/rubric-schema.md`
- Skill-local schema copies: `skills/<skill-name>/references/rubric-schema.md`
- Canonical grade-sheet schema: `references/grade-sheet-contract.md`

Each skill must remain self-contained.
Do not add skill instructions that depend on files outside that skill folder unless the
same file is also bundled inside the skill.

## Compatibility Requirements

`references/rubric-schema.md` is the canonical bundled schema.
Every skill-local `references/rubric-schema.md` copy must match it exactly.

Before pushing changes, run:

```bash
python3 scripts/verify_plugin_compat.py
python3 scripts/verify_schema_sync.py
python3 scripts/verify_grade_sheet_schema_sync.py
```

Treat any failing check as a blocking issue.
`verify_plugin_compat.py` enforces Agent Skills naming/frontmatter rules, Codex and
Claude Code manifest presence/alignment, skill-local schema sync, grade-sheet contract
and validator sync, and packaging hygiene.

If the canonical schema changes, update every skill-local schema copy before pushing:

```bash
for d in skills/*/references; do
  cp references/rubric-schema.md "$d/rubric-schema.md"
done
python3 scripts/verify_schema_sync.py
```

`references/grade-sheet-contract.md` is the canonical bundled grade-sheet schema.
Every skill-local `references/grade-sheet-contract.md` copy must match it exactly.
Every skill with a grade-sheet contract must also bundle
`scripts/validate_grade_sheet.py`, and copied grade-sheet validators must match the
canonical validator from `skills/grading-dry-run/scripts/validate_grade_sheet.py`.

If the grade-sheet contract changes, update every skill-local grade-sheet contract copy
and verify sync:

```bash
for d in skills/*/references; do
  if [ -f "$d/grade-sheet-contract.md" ]; then
    cp references/grade-sheet-contract.md "$d/grade-sheet-contract.md"
  fi
done
python3 scripts/verify_grade_sheet_schema_sync.py
```

If the grade-sheet validator changes, update every skill-local validator copy and verify
sync:

```bash
for d in skills/*/scripts; do
  if [ -f "$d/validate_grade_sheet.py" ]; then
    cp skills/grading-dry-run/scripts/validate_grade_sheet.py "$d/validate_grade_sheet.py"
  fi
done
python3 scripts/verify_grade_sheet_schema_sync.py
```

## Validation

For skill or packaging changes, run the root repository gate when working from the
marketplace checkout:

```bash
make check
```

This includes Ruff lint, Ruff format check, Flowmark lint, ty, plugin compatibility,
schema sync, grade-sheet sync, and smoke checks.

If running plugin-local checks manually, also run:

```bash
python3 scripts/smoke_test.py
```

When local validator skills are available, run:

```bash
for d in skills/*/; do
  if [ -f "$d/SKILL.md" ]; then
    python3 /path/to/skill-creator/scripts/quick_validate.py "$d" || exit 1
  fi
done
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
```

Use the root Makefile for Markdown formatting.
Do not run raw `flowmark --auto` on skill or reference files because it enables smart
quotes and ellipsis conversion in current Flowmark versions.
Use `make flowmark-format` from the repository root so Markdown is formatted with the
repo settings that preserve exact syntax in YAML, JSON, TOML, shell, and schema
examples.

## Packaging Hygiene

- Do not commit generated `*.zip` skill packages.
- Do not commit `.DS_Store`, caches, local virtual environments, logs, or generated
  output directories.
- Keep `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` metadata aligned
  when changing plugin identity, version, author, homepage, license, or description.
- Keep skill `name` frontmatter equal to its directory name.
