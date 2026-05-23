---
name: rubric-import-structure
description: Convert uploaded or pasted rubric source material such as CSV, XLSX extracts, tables, checklists, or prose scoring guides into Rubric Maker YAML or JSON. Use when an agent needs to preserve source wording, map fields into Category, QuestionName, ScoringLogic, Mode, Technique, Purpose, and AdditionalContext, or normalize imported rubric data.
---

# Rubric Import Structure

## Workflow

1. Extract all rubric rows and scoring anchors from the source. Do not summarize away items.
2. Preserve source wording where the user is importing an existing rubric.
3. Map fields into the Rubric Maker schema:
   - `Category`
   - `QuestionName`
   - `ScoringLogic`
   - `Mode`
   - `Technique`
   - `Purpose`
   - `AdditionalContext`
4. Infer `Mode` from intended evidence when missing. Default to `video` for observable encounter behavior, `audio` for verbal-only communication, and `note` for written documentation.
5. Use empty strings for missing optional fields.
6. Output YAML by default; output JSON if requested.
7. For DOCX/PDF/XLSX/CSV source files, use `scripts/extract_rubric_source.py` to create a Markdown source bundle before structuring.
8. For finished Rubric Maker YAML/JSON rubrics, use `scripts/render_rubric.py` to create a formatted Excel workbook or polished Word document.

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
