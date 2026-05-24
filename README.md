# UT REAL Project MAPLES Plugin Marketplace

This repository is a marketplace for Codex CLI and Claude Code plugins published by the **UT REAL Project MAPLES** research group.

The marketplace currently contains one installable plugin, Rubric Maker, plus placeholder directories for future Case Generation and Validation Analysis plugins.

## Marketplace Layout

```text
.
├── .agents/plugins/marketplace.json
├── .claude-plugin/marketplace.json
├── plugins/
│   ├── rubric-maker-skill/
│   ├── case-generation/
│   └── validation-analysis/
├── scripts/
└── README.md
```

Each plugin is self-contained. Plugin manifests, skills, scripts, references, and Python requirements live inside `plugins/<plugin-name>/`.

This layout follows the Codex repo marketplace pattern of `.agents/plugins/marketplace.json` with one `plugins[]` entry per tracked plugin and `./plugins/<plugin-name>` source paths. It also follows the Claude Code plugin convention where each plugin has its own `.claude-plugin/plugin.json` and component directories at the plugin root.

The Codex marketplace keeps placeholder plugins visible with `policy.installation: "NOT_AVAILABLE"`. The Claude Code marketplace exposes only installable plugins because Claude marketplace entries do not have an equivalent unavailable policy.

## Plugins

| Plugin | Status | Purpose |
|---|---:|---|
| `rubric-maker-skill` | Available | Skills and scripts for creating, importing, reviewing, transforming, dry-running, validating, and formatting OSCE rubrics. |
| `case-generation` | Codex placeholder only | Future case generation workflows and skills. |
| `validation-analysis` | Codex placeholder only | Future validation analysis workflows and skills. |

## Install From This Marketplace

Use the public marketplace repository URL when adding this marketplace.

### Codex CLI

```bash
codex plugin marketplace add https://github.com/JamiesonLabUTSW/maples-toolkit
codex plugin install rubric-maker-skill --source ut-real-project-maples
```

For local development, run Codex from this repository root. Codex can read the repo marketplace at `.agents/plugins/marketplace.json`, where each plugin entry points to `./plugins/<plugin-name>`.

### Claude Code

```text
/plugin marketplace add https://github.com/JamiesonLabUTSW/maples-toolkit
/plugin install rubric-maker-skill@ut-real-project-maples
```

For local development, load a plugin directly:

```bash
cc --plugin-dir plugins/rubric-maker-skill
```

## Python Requirements

Install only the requirements for the plugin you are using:

```bash
python3 -m pip install -r plugins/rubric-maker-skill/requirements.txt
```

The root `requirements.txt` is a compatibility shim for the currently available plugin:

```bash
python3 -m pip install -r requirements.txt
```

Future plugins should maintain their own `plugins/<plugin-name>/requirements.txt` when they ship Python scripts or other Python runtime dependencies.

## Validation

Run the marketplace compatibility checks from the repository root:

```bash
python3 scripts/verify_plugin_compat.py
python3 scripts/verify_schema_sync.py
python3 scripts/verify_grade_sheet_schema_sync.py
python3 scripts/smoke_test.py
```

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

## Reference Patterns

- Codex plugin marketplace docs: https://developers.openai.com/codex/plugins/build#marketplace-metadata
- Codex official marketplace example: https://github.com/openai/plugins/blob/main/.agents/plugins/marketplace.json
- Claude Code plugin structure docs: https://github.com/anthropics/claude-code/tree/main/plugins
- Claude official marketplace example: https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json

## Plugin Documentation

- Rubric Maker: [plugins/rubric-maker-skill/README.md](plugins/rubric-maker-skill/README.md)
- Case Generation: [plugins/case-generation/README.md](plugins/case-generation/README.md)
- Validation Analysis: [plugins/validation-analysis/README.md](plugins/validation-analysis/README.md)
