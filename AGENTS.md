# Repository Instructions

## Project Shape

This repository packages Rubric Maker skills for Codex CLI and Claude Code.

- Codex plugin manifest: `.codex-plugin/plugin.json`
- Claude Code plugin manifest: `.claude-plugin/plugin.json`
- Skill folders: `skills/<skill-name>/`
- Canonical rubric schema: `references/rubric-schema.md`
- Skill-local schema copies: `skills/<skill-name>/references/rubric-schema.md`

Each skill must remain self-contained. Do not add skill instructions that depend on files outside that skill folder unless the same file is also bundled inside the skill.

## Compatibility Requirements

`references/rubric-schema.md` is the canonical bundled schema. Every skill-local `references/rubric-schema.md` copy must match it exactly.

Before pushing changes, run:

```bash
python3 scripts/verify_plugin_compat.py
python3 scripts/verify_schema_sync.py
```

Treat either failing check as a blocking issue. `verify_plugin_compat.py` enforces Agent Skills naming/frontmatter rules, Codex and Claude Code manifest presence/alignment, skill-local schema sync, and packaging hygiene.

If the canonical schema changes, update every skill-local schema copy before pushing:

```bash
for d in skills/*/references; do
  cp references/rubric-schema.md "$d/rubric-schema.md"
done
python3 scripts/verify_schema_sync.py
```

## Validation

For skill or packaging changes, also run:

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

## Packaging Hygiene

- Do not commit generated `*.zip` skill packages.
- Do not commit `.DS_Store`, caches, local virtual environments, logs, or generated output directories.
- Keep `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` metadata aligned when changing plugin identity, version, author, homepage, license, or description.
- Keep skill `name` frontmatter equal to its directory name.
