# Rubrics App Source Map

- `src/blueprints/assessment/analysis.py`: routes for pre-analysis questions, single rubric analysis, batch analysis, and single-row analysis.
- `src/services.py`: `analyze_rubric_issues`, `structure_analysis_suggestions`, `analyze_with_ai`, `generate_clarifying_questions`, and `generate_followup_questions`.
- `prompts/system/analysis_extraction.j2`: issue extraction prompt.
- `prompts/system/analysis_structuring.j2`: structured suggestion formatting.
- `prompts/system/clarifying_questions.j2`: senior medical education consultant role and six-pillar audit.
