# Rubrics App Source Map

- `src/blueprints/assessment/enhance.py`: enhancement routes for `add_scores`, `fill_missing_fields`, and `expand_techniques`.
- `prompts/system/enhance/add_scores_extraction.j2`: score-level enhancement.
- `prompts/system/enhance/fill_missing_fields_extraction.j2`: Purpose and Technique generation.
- `prompts/system/enhance/expand_techniques_extraction.j2`: Technique expansion.
- `prompts/system/enhance/enhancement_structuring.j2`: structured enhancement suggestions.
- `src/blueprints/assessment/transform.py`: case-specific rubric transformation.
- `prompts/system/transform_extraction.j2` and `prompts/system/transform_structure.j2`: transformation workflow.
- `prompts/system/template_application_extraction.j2`: style/template application between rubrics.
