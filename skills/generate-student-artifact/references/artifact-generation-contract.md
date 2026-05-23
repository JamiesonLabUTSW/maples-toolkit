# Student Artifact Generation Contract

Use this contract for synthetic learner artifacts generated from OSCE case materials.

## Inputs

- `case_materials`: Station instructions, patient details, expected findings, sample chart data, or other case context supplied by the user.
- `artifact_type`: `note` or `transcript`.
- `template`: Optional user-provided structure or a built-in template from `builtin-templates.md`.
- `learner_profile`: Learner level and performance characteristics to represent.
- `target_performance_band`: Optional overall quality target, such as low, borderline, passing, high, or user-defined.
- `rubric_focus`: Optional rubric items, categories, or evidence targets the artifact should exercise.

## Output Shape

Return one JSON or YAML object:

```yaml
artifact_type: "note"
artifact_text: "Student-facing artifact text..."
metadata:
  case_summary_used: "Brief summary of supplied case facts used."
  learner_profile: "Learner profile represented in the artifact."
  intentional_strengths:
    - "Accurately documents the symptom timeline."
  intentional_weaknesses:
    - "Omits a key pertinent negative."
  limitations:
    - "No physical exam details were supplied."
```

Optional fields:

- `title`: Short artifact title.
- `template_name`: Name of the supplied or built-in template used.
- `target_performance_band`: Performance band requested by the user.
- `rubric_focus`: List of rubric items, categories, or evidence targets considered.
- `metadata.assumptions`: Conservative assumptions made because inputs were incomplete.
- `metadata.source_materials_summary`: Brief description of source materials received.

## Required Field Rules

- `artifact_type` must be `note` or `transcript`.
- `artifact_text` must be a nonempty string and must contain the generated learner artifact only.
- `metadata.case_summary_used` must summarize only facts supplied by the user.
- `metadata.learner_profile` may be a nonempty string or an object.
- `metadata.intentional_strengths`, `metadata.intentional_weaknesses`, and `metadata.limitations` must be lists of nonempty strings.
- Do not place grading, scores, rubric revisions, or evaluator commentary inside `artifact_text`.

## Generation Boundaries

- Do not grade the artifact.
- Do not revise the rubric.
- Do not create raw audio or video.
- Do not invent hidden case facts inconsistent with the provided case.
- If the user requests unsupported evidence, create a transcript or observation-log style text artifact only when that fits the request.
