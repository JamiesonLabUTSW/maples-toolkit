# Rubric Maker Skills

Codex CLI and Claude Code plugin containing skills for creating, importing, reviewing, transforming, validating, and formatting OSCE rubrics. The plugin is self-contained and defines its own bundled Rubric Maker schema.

Published by the **UT REAL Project MAPLES** research group.

Licensed under the UT Southwestern academic research use release terms in [LICENSE](LICENSE). The required release language permits academic research use and prohibits commercial use.

## Skills

| Skill | Use |
|---|---|
| `post-encounter-note-rubric` | Draft a `Mode: note` post-encounter-note grading rubric from case files, station instructions, SP scripts, sample notes, or clinical scenarios. |
| `rubric-import-structure` | Convert pasted or extracted source material into Rubric Maker YAML or JSON. Includes document extraction and render scripts. |
| `osce-rubric-review` | Review OSCE rubrics for alignment, safety, observability, objectivity, feasibility, reliability, and scoring clarity. |
| `osce-rubric-transform` | Adapt or enhance OSCE rubrics for new cases, contexts, scoring scales, missing fields, or style templates. |
| `test-station-grading` | Prepare mode-aware rubrics and grading instructions for video, audio, or note evidence. |
| `content-validation` | Validate rubric issues through multi-perspective critique and final recommendations. |

## Installation

This repository is packaged as a Codex CLI plugin and a Claude Code plugin. The plugin route is preferred for this bundle because it installs all six related skills together and keeps runtime metadata in `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`.

### Supported Runtimes

| Runtime | Support files | Notes |
|---|---|---|
| OpenAI Codex CLI | `.codex-plugin/plugin.json`, `skills/` | Codex loads the plugin through a marketplace entry and discovers bundled skills from the plugin root. |
| Claude Code | `.claude-plugin/plugin.json`, `skills/` | Claude Code loads the plugin from a plugin source or local plugin directory and discovers bundled skills from the plugin root. |

References:

- OpenAI Codex plugin docs: https://developers.openai.com/codex/plugins/build
- Claude Code plugin docs: https://github.com/anthropics/claude-code/tree/main/plugins

### Publisher Metadata

Publisher identity is conveyed in runtime manifests and marketplace metadata:

- `.codex-plugin/plugin.json`: `author.name` and `interface.developerName` are set to `UT REAL Project MAPLES`; `author.url`, `homepage`, and `interface.websiteURL` point to `https://ut-real-ai-project-maples.com/`.
- `.claude-plugin/plugin.json`: `author.name` is set to `UT REAL Project MAPLES`; `author.url` and `homepage` point to `https://ut-real-ai-project-maples.com/`.
- Public marketplace repository: the marketplace root should use `name: "ut-real-project-maples"` and `interface.displayName: "UT REAL Project MAPLES"`.

Keep the plugin package name stable as `rubric-maker-skill`; use the publisher fields and marketplace display name to identify the research group.

### License

This plugin is published under the UT Southwestern software release language required by the Office for Technology Development:

https://www.utsouthwestern.edu/about-us/administrative-offices/technology-development/agreements/open-source-release-of-software.html

The plugin manifest uses `LicenseRef-UTSW-Academic-Research-Only` because this is a custom institutional license rather than a standard SPDX license such as `MIT` or `Apache-2.0`.

### Public GitHub Marketplace

Recommended public marketplace layout:

```text
<marketplace-repo>/
  .agents/
    plugins/
      marketplace.json
  plugins/
    rubric-maker-skill/
      .codex-plugin/
        plugin.json
      .claude-plugin/
        plugin.json
      skills/
      README.md
      requirements.txt
```

Example `.agents/plugins/marketplace.json` for the public marketplace repository:

```json
{
  "name": "ut-real-project-maples",
  "interface": {
    "displayName": "UT REAL Project MAPLES"
  },
  "plugins": [
    {
      "name": "rubric-maker-skill",
      "source": {
        "source": "local",
        "path": "./plugins/rubric-maker-skill"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Education"
    }
  ]
}
```

For local testing of the public marketplace, clone the marketplace repository and point Codex at its `.agents/plugins/marketplace.json`. Keep local test data and generated artifacts out of the published plugin package; `.pluginignore` documents the intended exclusions.

### Plugin Install

For local use, copy or clone this repository into your local plugin directory:

```bash
mkdir -p "$HOME/plugins"
cp -R ./rubric-maker-skill "$HOME/plugins/rubric-maker-skill"
```

Then add or update a personal marketplace entry at `$HOME/.agents/plugins/marketplace.json`:

```json
{
  "name": "personal",
  "interface": {
    "displayName": "Personal"
  },
  "plugins": [
    {
      "name": "rubric-maker-skill",
      "source": {
        "source": "local",
        "path": "./plugins/rubric-maker-skill"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Education"
    }
  ]
}
```

Restart OpenAI Codex CLI after installation so the plugin and skills are discovered. You can browse installed plugins with `/plugins` and browse local skills with `/skills`.

For Claude Code local development, load this repository directly:

```bash
cc --plugin-dir /path/to/rubric-maker-skill
```

For Claude Code distribution, install this repository as a plugin from a source that preserves `.claude-plugin/plugin.json`. Claude Code discovers the top-level `skills/` directory from the plugin root.

### Direct Skill Install

If you only want one skill, install it directly into your agent runtime's skills directory. This example uses the Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/post-encounter-note-rubric "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Each skill is self-contained: its `SKILL.md`, local `references/`, and optional local `scripts/` or `agents/` resources live inside the skill folder.

## Usage

Invoke a skill by name in Codex CLI or Claude Code:

```text
Use $post-encounter-note-rubric to draft a rubric from these case files.
```

```text
Use $rubric-import-structure to convert this source table into Rubric Maker YAML.
```

```text
Use $osce-rubric-review to audit this rubric for safety and scoring clarity.
```

```text
Use $test-station-grading to prepare this rubric for note and video grading.
```

## Document And Output Scripts

`rubric-import-structure` includes two helper scripts.

Extract source material from DOCX, PDF, Excel, CSV, TSV, TXT, or Markdown:

```bash
python3 skills/rubric-import-structure/scripts/extract_rubric_source.py \
  case.docx rubric.xlsx \
  -o extracted-source.md
```

Render a Rubric Maker rubric YAML or JSON file to formatted Excel:

```bash
python3 skills/rubric-import-structure/scripts/render_rubric.py rubric.yaml -o rubric.xlsx
```

Render the same rubric to a formatted Word document:

```bash
python3 skills/rubric-import-structure/scripts/render_rubric.py rubric.yaml -o rubric.docx
```

## Script Dependencies

Install script dependencies from the manifest:

```bash
python3 -m pip install -r requirements.txt
```

Or install only the packages needed for the file types you use:

```bash
python3 -m pip install openpyxl python-docx PyYAML
```

For PDF extraction, install one of:

```bash
python3 -m pip install pdfplumber
```

or:

```bash
python3 -m pip install pypdf
```

Dependency map:

- Excel input/output: `openpyxl`
- Word input/output: `python-docx`
- YAML input: `PyYAML`
- PDF input: `pdfplumber` or `pypdf`
- CSV, TSV, TXT, JSON: Python standard library

## Rubric Format

The skills target the bundled Rubric Maker schema:

```yaml
rubric:
  - Category: "Clinical Reasoning"
    QuestionName: "Documents a prioritized differential diagnosis"
    ScoringLogic:
      Score1: "No differential diagnosis is documented."
      Score2: "A limited differential is documented with major omissions."
      Score3: "A plausible differential is documented with minor omissions."
      Score4: "A comprehensive, prioritized differential is documented and justified."
    Mode: "note"
    Technique: "Look for listed diagnoses and case-based justification in the written note."
    Purpose: "Evaluates diagnostic synthesis."
    AdditionalContext: ""
```

Valid `Mode` values are `video`, `audio`, and `note`.

## Validation

Validate a generated rubric before rendering:

```bash
python3 skills/rubric-import-structure/scripts/validate_rubric.py rubric.yaml
```

Validate structured suggestions before applying or sharing them:

```bash
python3 skills/rubric-import-structure/scripts/validate_suggestions.py suggestions.json
```

Validate a skill with the local skill creator validator:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py \
  skills/post-encounter-note-rubric
```

Validate every skill in this repo:

```bash
for d in skills/*/; do
  if [ -f "$d/SKILL.md" ]; then
    python3 /path/to/skill-creator/scripts/quick_validate.py "$d" || exit 1
  fi
done
```

Verify that every skill-local schema copy matches the canonical schema:

```bash
python3 scripts/verify_schema_sync.py
```

Validate Agent Skills, Codex plugin, and Claude Code plugin compatibility invariants:

```bash
python3 scripts/verify_plugin_compat.py
```

Validate the plugin wrapper:

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
```

Run the repository smoke test:

```bash
python3 scripts/smoke_test.py
```

The skill-local deterministic tooling smoke test can also be run after a direct
skill install:

```bash
python3 skills/rubric-import-structure/scripts/smoke_test.py
```

## Runtime Boundaries

This plugin is a standalone agent CLI package. It does not rely on unpublished
application source files, external prompt templates, or a separate web runtime.

| Capability | Plugin skill support | Requires external runtime |
|---|---|---|
| Import and structure rubric source files | Yes, via skill guidance and extraction scripts | No |
| Draft post-encounter-note rubrics | Yes | No |
| Review rubric quality and suggest improvements | Yes, as skill-guided analysis | No |
| Transform or enhance rubrics | Yes, as skill-guided analysis | No |
| Validate rubric YAML/JSON shape | Yes, via validation scripts | No |
| Render rubric YAML/JSON to XLSX/DOCX | Yes, via render script | No |
| Grade uploaded video/audio/note files with queued jobs | Prompt preparation only | Yes |
| Persist assessments, versions, suggestions, and grading jobs | No | Yes |
| Run live AI patient simulator sessions | Case design only | Yes |
| Multi-model content validation with persistence/streaming | Lightweight skill workflow only | Yes |
