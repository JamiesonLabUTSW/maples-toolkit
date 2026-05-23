---
name: rubric-import
description: Import existing rubric source material such as CSV, XLSX extracts, tables, checklists, or prose scoring guides into Rubric Maker YAML or JSON while preserving source wording. Use when an agent needs to convert an already-authored rubric or scoring guide into Category, QuestionName, ScoringLogic, Mode, Technique, Purpose, and AdditionalContext fields. Do not use for drafting new rubrics from case materials, improving/adapting existing rubrics, reviewing rubric quality, clinical-validity adjudication, or test-station grading setup.
---

# Rubric Import

## Purpose

Convert existing rubric source material into the Rubric Maker schema as faithfully as possible. This skill is an import and normalization workflow: it preserves source wording, extracts every assessable item and scoring anchor, maps source columns or prose sections into the schema, and produces portable YAML by default.

The bright line: use this skill when the user already has a rubric, checklist, scoring table, or prose scoring guide and wants it converted into structured Rubric Maker YAML/JSON. Do not use it to invent, improve, adjudicate, or operationalize rubric content beyond the minimal normalization needed for the schema.

## Use For

- Importing an existing rubric from CSV, XLSX, DOCX, PDF, pasted tables, Markdown, plain text, or prose scoring guides.
- Preserving source wording while mapping content into `Category`, `QuestionName`, `ScoringLogic`, `Mode`, `Technique`, `Purpose`, and `AdditionalContext`.
- Normalizing missing optional fields to empty strings.
- Inferring a row-level `Mode` only when the imported source lacks one.
- Running deterministic extraction before structuring source files.
- Rendering a finished imported rubric to XLSX or DOCX as a post-import convenience.

## Do Not Use For

- Drafting a new post-encounter-note rubric from case materials, station instructions, SP scripts, expected findings, or sample notes; use `post-encounter-note-rubric`.
- Reviewing an existing rubric for safety, objectivity, observability, feasibility, reliability, scoring clarity, or missing-field problems; use `osce-rubric-review`.
- Improving, adapting, restyling, expanding score levels, filling missing fields, applying a template, or rewriting rubric content; use `osce-rubric-transform`.
- Deciding whether a disputed rubric concern, proposed fix, severity, or clinical interpretation is valid; use `content-validation`.
- Splitting items by evidence source, designing grading prompts, or preparing video/audio/note grading workflows; use `test-station-grading`.
- Designing live virtual patient simulation cases; treat that as outside this rubric-import skill.

## Sibling Sequence

Use `rubric-import` first when source material must be preserved and converted into the schema. After import, use `osce-rubric-review` for broad quality auditing, `content-validation` for contested clinical concerns, `osce-rubric-transform` for requested changes or missing-field fills, and `test-station-grading` when the user needs evidence-mode grading setup.

If the user asks both to import and improve a rubric, import faithfully first, then clearly separate any proposed improvements as a downstream `osce-rubric-transform` or `osce-rubric-review` task. Do not silently blend preservation and improvement.

## Workflow

1. Load `references/import-structure-pattern.md` before structuring. Load `references/rubric-schema.md` when schema, mode, or suggestion semantics are needed.
2. Extract all rubric rows and scoring anchors from the source. Do not summarize away items.
3. Preserve source wording where the user is importing an existing rubric.
4. Map fields into the Rubric Maker schema:
   - `Category`
   - `QuestionName`
   - `ScoringLogic`
   - `Mode`
   - `Technique`
   - `Purpose`
   - `AdditionalContext`
5. Infer `Mode` from intended evidence when missing. Default to `video` for observable encounter behavior, `audio` for verbal-only communication, and `note` for written documentation.
6. Use empty strings for missing optional fields.
7. Output YAML by default; output JSON if requested.
8. For DOCX/PDF/XLSX/CSV source files, use `scripts/extract_rubric_source.py` to create a Markdown source bundle before structuring.
9. For finished Rubric Maker YAML/JSON rubrics, use `scripts/render_rubric.py` to create a formatted Excel workbook or polished Word document only when rendering is part of the requested import handoff.

## Mode Boundary

Infer `Mode` only to normalize imported rows. If the user asks whether items can be scored from specific evidence, wants items split across video/audio/note, or needs grading prompts or evidence requirements, stop using this skill and use `test-station-grading`.

## Output Boundary

For faithful imports, output a complete Rubric Maker YAML/JSON artifact. Do not output structured improvement suggestions from this skill; use sibling skills for review, transformation, or validation suggestions.

## Scripts

Extract source files:

```bash
python3 scripts/extract_rubric_source.py case.docx rubric.xlsx -o extracted-source.md
```

Render a structured rubric:

```bash
python3 scripts/render_rubric.py rubric.yaml -o rubric.xlsx
python3 scripts/render_rubric.py rubric.yaml -o rubric.docx
```

Dependencies:

- `.xlsx` output/input requires `openpyxl`.
- `.docx` input/output requires `python-docx`.
- `.pdf` input requires `pdfplumber` or `pypdf`.
- YAML input requires `PyYAML`; JSON input works with the standard library.

## References

- Load `references/rubric-schema.md` for the shared schema, mode semantics, and structured suggestion conventions.
- Load `references/import-structure-pattern.md` for schema details and import workflow rules.
