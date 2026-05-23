# Rubric Import Pattern

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

## Rules

- Preserve original wording during import unless the user asks for improvement.
- Use `Score1`, `Score2`, etc. in score order.
- Keep all special characters valid for YAML/JSON.
- Do not add extra fields.
- Ensure every row has a category, question name, and at least one score anchor.

## Bright-Line Scope

This reference supports faithful import only. It does not cover new rubric drafting, review, clinical adjudication, content improvement, template application, or grading prompt design.

When a user asks for import plus improvement, finish the import first and clearly separate downstream improvements as a different skill workflow.

## Ambiguous Column Mapping

Map source columns by meaning, not by exact header name:

- `Category`, `Section`, `Domain`, `Competency`, or similar grouping columns -> `Category`.
- `Question`, `QName`, `Question Name`, `Assessment Item`, `Item`, `Criterion`, `Behavior`, or similar item text -> `QuestionName`.
- Score, rating, points, level, anchor, or performance columns -> `ScoringLogic.ScoreN` in ascending score order.
- `Mode`, `Evidence`, `Assessment Mode`, `Source`, or modality columns -> `Mode` when values clearly mean `video`, `audio`, or `note`.
- `Technique`, `Method`, `Observable Behavior`, `Examples`, `Procedure`, or "what to look for" columns -> `Technique`.
- `Purpose`, `Rationale`, `Objective`, `Competency`, or educational aim columns -> `Purpose` when they explain why the item matters.
- `Additional Context`, `Context`, `Notes`, `Acceptable Alternatives`, `Constraints`, `Indication`, or clinical trigger columns -> `AdditionalContext` unless the source clearly uses the field as the item's educational rationale.

If a source uses older `Indication` terminology, preserve the wording and usually map it to `AdditionalContext`. Do not create an `Indication` field in the output.

## Mode Normalization

Use `Mode` only to make the imported rubric app-compatible:

- `video`: visible behavior, physical exam actions, professionalism, draping, positioning, or other observable encounter behavior.
- `audio`: spoken content, questions, counseling, explanations, rapport, or transcript-only evidence.
- `note`: written post-encounter-note evidence, documentation, differential diagnosis, assessment, or plan.

Default unclear encounter behavior to `video`. Do not use this import workflow to split a rubric by evidence source or design grading prompts; use `test-station-grading` for that.

## Row Handling

Portable Rubric Maker YAML/JSON produced by this skill should not include a top-level per-item `row` field. The upstream application may add row indexes internally after parsing for suggestion tracking. Structured suggestions use zero-based `row`, but imported rubric rows should contain only the schema fields.

## Import Versus Improvement

For faithful import, do not fill missing `Technique`, `Purpose`, or `AdditionalContext` with invented content. Use empty strings when the source omits optional fields. If the user asks to fill or improve those fields, route that downstream work to `osce-rubric-transform`.

## Deterministic File Tools

- `scripts/extract_rubric_source.py`: Converts `.docx`, `.pdf`, `.xlsx`, `.xlsm`, `.csv`, `.tsv`, `.txt`, and `.md` into a Markdown source bundle. Use this before asking Codex or a model to structure the rubric.
- `scripts/render_rubric.py`: Converts Rubric Maker YAML/JSON into formatted `.xlsx` or `.docx` output. Use this after the rubric has already been generated or structured, not as a reason to invoke the import skill by itself.

The scripts intentionally do not call an LLM. They separate deterministic file handling from rubric generation.
