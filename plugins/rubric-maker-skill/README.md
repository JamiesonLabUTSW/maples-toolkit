# Rubric Maker Skills

Codex CLI and Claude Code plugin containing skills for creating, importing, reviewing, transforming, validating, and formatting OSCE rubrics. The plugin is self-contained and defines its own bundled Rubric Maker schema.

Published by the **UT REAL Project MAPLES** research group.

Licensed under the UT Southwestern academic research use release terms in [LICENSE](LICENSE). The required release language permits academic research use and prohibits commercial use.

## Skills

| Skill | Use |
|---|---|
| `post-encounter-note-rubric` | Draft a `Mode: note` post-encounter-note grading rubric from case files, station instructions, SP scripts, sample notes, or clinical scenarios. |
| `rubric-import` | Import existing rubric source material into Rubric Maker YAML or JSON while preserving wording. Includes document extraction and render scripts. |
| `osce-rubric-review` | Review OSCE rubrics for alignment, safety, observability, objectivity, feasibility, reliability, and scoring clarity. |
| `osce-rubric-transform` | Adapt or enhance OSCE rubrics for new cases, contexts, scoring scales, missing fields, or style templates. |
| `generate-student-artifact` | Generate synthetic student notes, encounter transcripts, or transcript-derived observation logs from a case and learner performance profile. |
| `grading-dry-run` | Dry-run grade a student note, transcript, observation log, or transcript-plus-observations bundle against an OSCE rubric and produce an evidence-backed trial grade sheet. |
| `evaluate-dry-run` | Analyze a case, rubric, student artifact, and trial grade sheet to identify rubric improvements. |
| `content-validation` | Validate rubric issues through multi-perspective critique and final recommendations. |

## Installation

This directory is packaged as a Codex CLI plugin and a Claude Code plugin. The plugin route is preferred for this bundle because it installs the related skills together and keeps runtime metadata in `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`.

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

### Marketplace Install

The public marketplace repository exposes this plugin from `plugins/rubric-maker-skill`:

```bash
codex plugin marketplace add https://github.com/JamiesonLabUTSW/maples-toolkit
codex plugin install rubric-maker-skill --source ut-real-project-maples
```

For Claude Code:

```text
/plugin marketplace add https://github.com/JamiesonLabUTSW/maples-toolkit
/plugin install rubric-maker-skill@ut-real-project-maples
```

For local Claude Code development, load this plugin directory directly from the marketplace checkout:

```bash
cc --plugin-dir plugins/rubric-maker-skill
```

For Codex local development, run Codex from the marketplace root so it can read `.agents/plugins/marketplace.json`, or add a personal marketplace entry whose `source.path` points to this plugin directory.

### Direct Skill Install

If you only want one skill, install it directly into your agent runtime's skills directory. This example uses the Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R plugins/rubric-maker-skill/skills/post-encounter-note-rubric \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Each skill is self-contained: its `SKILL.md`, local `references/`, and optional local `scripts/` or `agents/` resources live inside the skill folder.

## Usage

Invoke a skill by name in Codex CLI or Claude Code:

```text
Use $post-encounter-note-rubric to draft a rubric from these case files.
```

```text
Use $rubric-import to convert this source table into Rubric Maker YAML.
```

```text
Use $osce-rubric-review to audit this rubric for safety and scoring clarity.
```

```text
Use $generate-student-artifact to create an average learner note for this case.
```

```text
Use $grading-dry-run to grade this sample note, transcript, or transcript-plus-observations bundle against the draft rubric.
```

```text
Use $evaluate-dry-run to turn this trial grade sheet into rubric improvement suggestions.
```

Unless a command explicitly starts with `plugins/rubric-maker-skill/`, run the examples below from this plugin directory.

## Document And Output Scripts

`rubric-import` includes two helper scripts.

Extract source material from DOCX, PDF, Excel, CSV, TSV, TXT, or Markdown:

```bash
python3 skills/rubric-import/scripts/extract_rubric_source.py \
  case.docx rubric.xlsx \
  -o extracted-source.md
```

Render a Rubric Maker rubric YAML or JSON file to formatted Excel:

```bash
python3 skills/rubric-import/scripts/render_rubric.py rubric.yaml -o rubric.xlsx
```

Render the same rubric to a formatted Word document:

```bash
python3 skills/rubric-import/scripts/render_rubric.py rubric.yaml -o rubric.docx
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
python3 skills/rubric-import/scripts/validate_rubric.py rubric.yaml
```

Validate structured suggestions before applying or sharing them:

```bash
python3 skills/rubric-import/scripts/validate_suggestions.py suggestions.json
```

Validate a skill with the local skill creator validator:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py \
  skills/post-encounter-note-rubric
```

Validate every skill in this plugin:

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

Verify that every skill-local grade-sheet contract and validator copy matches
the canonical grade-sheet artifacts:

```bash
python3 scripts/verify_grade_sheet_schema_sync.py
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
python3 skills/rubric-import/scripts/smoke_test.py
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
| Generate synthetic notes, transcripts, or transcript-derived observation logs for rubric testing | Yes | No |
| Dry-run grade notes, transcripts, timestamped observation logs, or transcript-plus-observations bundles | Yes, with deterministic grade-sheet checks | No |
| Evaluate dry-run grade sheets for rubric-improvement suggestions | Yes, with bundled grade-sheet validation and schema sync checks | No |
| Inspect raw audio/video or run queued grading jobs | No | Yes |
| Persist assessments, versions, suggestions, and grading jobs | No | Yes |
| Run live AI patient simulator sessions | Case design only | Yes |
| Multi-model content validation with persistence/streaming | Lightweight skill workflow only | Yes |
