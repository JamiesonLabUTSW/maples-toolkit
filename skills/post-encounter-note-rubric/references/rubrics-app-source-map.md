# Rubrics App Source Map

This skill mirrors the `/rubrics` web app behavior.

## Core Format

- `src/schemas.py`: core rubric schema and analysis suggestion schema.
- `prompts/system/structuring.j2`: required rubric JSON structure and field rules.
- `src/services.py`: two-step extraction then structuring workflow.

## Post-Encounter Note Grading

- `src/grading_services/test_station_service.py`: embedded `note` grading prompt. It instructs graders to assess a post-encounter note from a simulated patient encounter, extract relevant text, score from provided criteria, and avoid assumptions beyond the note.
- `src/grading_schemas/multimodal_grading.py`: note grading response fields are `evidence`, `rationale`, `answer`, and optional `score`.

## Review And Enhancement

- `prompts/system/clarifying_questions.j2` and `prompts/user/clarifying_questions.j2`: six-pillar audit.
- `prompts/system/enhance/fill_missing_fields_extraction.j2`: `Purpose` explains why an item matters; `Technique` gives observable actions or evidence examples.
- `prompts/system/enhance/add_scores_extraction.j2`: add intermediate score levels when the assessment spectrum needs more granularity.
- `prompts/system/enhance/expand_techniques_extraction.j2`: expand Technique field for consistent assessment.

## Embedded Prompt Reminder

Do not inspect only `prompts/`. The app also embeds operational prompt text in Python functions, especially grading prompt templates in `src/grading_services/test_station_service.py`.
