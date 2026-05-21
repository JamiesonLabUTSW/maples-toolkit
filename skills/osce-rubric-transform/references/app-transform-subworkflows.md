# App Transform And Enhancement Subworkflows

This reference captures `/rubrics` app constraints for transformation and
enhancement workflows. Use it when adapting rubrics, adding score levels,
filling missing fields, expanding techniques, or applying a reference style.

Source map:

- `/rubrics/prompts/system/transform_extraction.j2`
- `/rubrics/prompts/system/transform_structure.j2`
- `/rubrics/prompts/system/enhance/add_scores_extraction.j2`
- `/rubrics/prompts/system/enhance/fill_missing_fields_extraction.j2`
- `/rubrics/prompts/system/enhance/expand_techniques_extraction.j2`
- `/rubrics/prompts/system/template_application_extraction.j2`
- `/rubrics/src/suggestion_schemas/suggestion_schemas.py`

## Shared Suggestion Contract

All transform/enhancement outputs are JSON suggestions:

```json
{
  "location": "0:ScoringLogic.Score2",
  "priority": "medium",
  "reasoning": "Specific clinical or educational justification",
  "row": 0,
  "field": "ScoringLogic",
  "sub": "Score2",
  "current_value": "Exact current text",
  "suggested_value": "Replacement text"
}
```

Rows are 0-based. `current_value` must be exact. For new content, use an empty
string for `current_value`.

For `ScoringLogic` fields, make one suggestion per score key. Do not combine
multiple score levels in one suggestion.

## Case Or Role Transformation

Purpose: adapt an existing rubric to a new clinical case, patient population,
setting, or assessed role.

Allowed fields:

- `Category`
- `QuestionName`
- `ScoringLogic`
- `Mode`
- `Technique`
- `Purpose`
- `AdditionalContext`

Required process:

- Review every item; do not skip rows or rely on pattern shortcuts.
- Assess relevance in the new case or role.
- Identify specific changes required for validity.
- Adjust expected behaviors and score criteria only where the new context
  changes what should be assessed.
- Provide clinical justification for each suggestion.

Consider:

- Patient demographics and communication needs.
- Clinical setting, acuity, time, and resources.
- Chief complaint and affected body systems.
- Role-specific scope of practice and documentation duties.
- Whether the item remains observable in the selected mode.

Constraints:

- Preserve rigor and fairness from the source rubric.
- Keep unchanged items unchanged.
- For scoring changes, separate `Score1`, `Score2`, etc. into individual
  suggestions.

## Add Scores

Purpose: add intermediate score levels or refine existing score descriptions
for better performance differentiation.

Field restrictions:

- `field` must be `ScoringLogic`.
- `sub` must be `ScoreN`.
- New score levels use `current_value: ""`.
- Do not modify `QuestionName`, `Technique`, `Purpose`, `Mode`, or other fields.

Scoring rules:

- `Score1` is the lowest score.
- Higher score numbers represent better performance.
- Use only as many score levels as meaningful. More scores are not automatically
  better.
- The configured maximum score level is a cap, not a requirement.

Quality requirements:

- Each score level must describe observable behavior.
- Adjacent levels must be mutually exclusive and clinically distinguishable.
- Avoid vague descriptors such as `adequate` unless paired with concrete
  behavior.
- New levels should represent qualitative competency differences, not just
  arbitrary quantity.
- Criteria must align with the assessment mode: video, audio, or note.

## Fill Missing Fields

Purpose: generate missing `Purpose`, `Technique`, or both.

Field restrictions:

- For Purpose-only: `field` must be `Purpose`; `sub` must be `null`.
- For Technique-only: `field` must be `Technique`; `sub` must be `null`.
- For both: create separate suggestions for `Purpose` and `Technique`.
- `current_value` must be `""` because the field is missing or empty.

Purpose guidance:

- Explain why the item matters and what competency is being evaluated.
- Connect to clinical reasoning, patient care, or educational outcomes.
- Use concise professional language, usually one or two sentences.
- Avoid repeating the `QuestionName` without adding assessment rationale.

Technique guidance:

- Provide concrete observable examples.
- Include exact phrases, physical actions, or documentation evidence when
  relevant.
- Align with the existing scoring logic.
- Include acceptable variations without becoming exhaustive.

All missing fields are high priority in the app workflow because they affect
assessment completeness.

## Expand Techniques

Purpose: enrich existing `Technique` descriptions and optionally update scoring
logic when expanded examples expose scoring gaps.

Allowed fields:

- `Technique`
- `ScoringLogic`

Field restrictions:

- Technique suggestions use `sub: null`.
- Scoring suggestions use `sub: "ScoreN"`.
- If `field` is `ScoringLogic`, `sub` is required.

Technique expansion rules:

- Expand only when examples genuinely improve assessment clarity.
- Add specific actions, verbal examples, acceptable variations, or evaluator
  cues.
- Keep examples aligned with `QuestionName`, `Purpose`, and score anchors.
- Match example density to task complexity.
- Do not turn the Technique field into a textbook.

Scoring alignment rules:

- After expanding Technique, check whether scoring logic still differentiates
  the clarified behaviors.
- Only suggest scoring changes when the expanded Technique reveals a concrete
  ambiguity, gap, overlap, or contradiction.
- Create separate suggestions for each affected score level.

## Template Or Style Application

Purpose: apply style and formatting from a reference rubric to a target rubric.

Change:

- Wording patterns.
- Naming conventions.
- Tone, tense, punctuation, capitalization.
- Score progression style.
- Technique/Purpose verbosity.
- Missing score levels when the reference has more levels.
- Empty or minimal Technique, Purpose, or AdditionalContext fields, using the
  reference pattern adapted to target content.

Preserve:

- Target clinical procedures and objectives.
- Number of questions.
- Medical meaning.
- Assessment target.
- `Mode` exactly as written in the target rubric.

Constraints:

- Do not copy clinical content from the reference into the target.
- Apply the reference pattern to the target's content.
- Each suggestion should fully restyle one cell.
- Return `[]` if the target already matches the reference style closely.

## Empty Result

Return `[]` when the requested transform or enhancement does not require
actionable app suggestions. Do not invent changes just to produce output.
