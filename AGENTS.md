# Repository Instructions

## Project Shape

This repository packages Rubric Maker skills for Codex CLI and Claude Code.

- Codex plugin manifest: `.codex-plugin/plugin.json`
- Claude Code plugin manifest: `.claude-plugin/plugin.json`
- Skill folders: `skills/<skill-name>/`
- Canonical rubric schema: `references/rubrics-app-schema.md`
- Skill-local schema copies: `skills/<skill-name>/references/rubrics-app-schema.md`

Each skill must remain self-contained. Do not add skill instructions that depend on files outside that skill folder unless the same file is also bundled inside the skill.

## Schema Sync Requirement

`references/rubrics-app-schema.md` is the canonical schema. Every skill-local `references/rubrics-app-schema.md` copy must match it exactly.

Before pushing changes, run:

```bash
python3 scripts/verify_schema_sync.py
```

Treat a failing schema sync check as a blocking issue. If the canonical schema changes, update every skill-local schema copy before pushing:

```bash
for d in skills/*/references; do
  cp references/rubrics-app-schema.md "$d/rubrics-app-schema.md"
done
python3 scripts/verify_schema_sync.py
```

## Validation

For skill or packaging changes, also run:

```bash
python3 skills/rubric-import-structure/scripts/smoke_test.py
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

## Packaging Hygiene

- Do not commit generated `*.zip` skill packages.
- Do not commit `.DS_Store`, caches, local virtual environments, logs, or generated output directories.
- Keep `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` metadata aligned when changing plugin identity, version, author, homepage, license, or description.
- Keep skill `name` frontmatter equal to its directory name.
