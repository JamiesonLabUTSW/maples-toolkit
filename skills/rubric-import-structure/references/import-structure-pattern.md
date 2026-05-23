# Import Structure Pattern

Rubric imports use a two-step pattern:

1. Extract every rubric item and score anchor from source material.
2. Structure the result into the Rubric Maker schema.

Schema:

```yaml
rubric:
  - Category: ""
    QuestionName: ""
    ScoringLogic:
      Score1: ""
      Score2: ""
    Mode: "video"
    Technique: ""
    Purpose: ""
    AdditionalContext: ""
```

Rules:

- Preserve original wording during import unless the user asks for improvement.
- Use `Score1`, `Score2`, etc. in score order.
- Keep all special characters valid for YAML/JSON.
- Do not add extra fields.
- Ensure every row has a category, question name, and at least one score anchor.

## Deterministic File Tools

- `scripts/extract_rubric_source.py`: Converts `.docx`, `.pdf`, `.xlsx`, `.xlsm`, `.csv`, `.tsv`, `.txt`, and `.md` into a Markdown source bundle. Use this before asking Codex or a model to structure the rubric.
- `scripts/render_rubric.py`: Converts Rubric Maker YAML/JSON into formatted `.xlsx` or `.docx` output. Use this after the rubric has already been generated or structured.

The scripts intentionally do not call an LLM. They separate deterministic file handling from rubric generation.
