# Analysis Suggestion Contracts

This reference captures rules for OSCE rubric review suggestions. Use it when
converting critique into structured suggestions or checking whether a review
result follows the bundled Rubric Maker suggestion contract.

## Contents

- [Two-Step Analysis Flow](#two-step-analysis-flow)
- [Suggestion Schema](#suggestion-schema)
- [Exact Current Value Rule](#exact-current-value-rule)
- [No-Suggestions Behavior](#no-suggestions-behavior)
- [Review Priorities](#review-priorities)
- [Field Analysis Rules](#field-analysis-rules)
- [Excel And CSV Safety](#excel-and-csv-safety)
- [Pattern Consistency](#pattern-consistency)
- [Comprehensive Single-Cell Fixes](#comprehensive-single-cell-fixes)
- [Mode-Specific Assessability Checks](#mode-specific-assessability-checks)

## Two-Step Analysis Flow

The review workflow is two-step:

1. Analyze the rubric in natural language and identify needed fixes.
2. Convert that analysis into a JSON array of suggestions.

The second step is a formatting pass, not a new critique pass. It should
mechanically extract quoted current text, proposed replacement text, location,
reasoning, and priority from the analysis.

## Suggestion Schema

Each suggestion must use this shape:

```json
{
  "location": "0:ScoringLogic.Score1",
  "reasoning": "Why this change improves the rubric",
  "priority": "high",
  "current_value": "Exact current text",
  "suggested_value": "Replacement text",
  "row": 0,
  "field": "ScoringLogic",
  "sub": "Score1"
}
```

Required fields:

- `location`
- `reasoning`
- `priority`
- `current_value`
- `suggested_value`
- `row`
- `field`

Allowed `priority` values:

- `critical`
- `high`
- `medium`
- `low`

Allowed `field` values for analysis:

- `Category`
- `QuestionName`
- `ScoringLogic`
- `Mode`
- `Technique`
- `Purpose`
- `AdditionalContext`

`sub` rules:

- For `ScoringLogic`, use the specific score key such as `Score1`.
- For non-`ScoringLogic` fields, use `null`.

`location` format:

- Simple field: `ROW:FIELD`, for example `2:Technique`.
- Nested score field: `ROW:ScoringLogic.Score3`.
- Rows are 0-based.

## Exact Current Value Rule

`current_value` must match the rubric text exactly, character for character.

Do not:

- Paraphrase.
- Normalize grammar before copying.
- Replace the original wording with a conceptual equivalent.
- Split one current cell into multiple partial current values.

Exact matching is required for filtering and applying suggestions. If a cell
has several issues, create one comprehensive replacement for that cell instead
of several suggestions for separate fragments.

## No-Suggestions Behavior

Return an empty JSON array `[]` when no actionable changes are needed.

Treat `[]` as correct when all of these are true:

- No fields start with Excel-problematic characters: `-`, `=`, `+`, or `@`.
- `QuestionName` values are clear and specific.
- Score levels are distinct, observable, and progressive.
- Language issues do not affect clarity.
- Similar content uses consistent phrasing.
- Criteria are assessable in the intended mode.

Also consider `[]` when:

- Re-analysis follows mostly rejected previous suggestions.
- Manual edits indicate the user is satisfied with the current state.
- Only low-priority punctuation or preference changes remain.
- The rubric already serves its assessment purpose.

Do not return `[]` if critical or high-priority issues remain.

## Review Priorities

Use these priority patterns:

- `critical`: Excel safety, missing score levels, contradictory criteria.
- `high`: vague question names, unclear score progression, medical spelling
  errors that impair clarity.
- `medium`: terminology improvements, consistency issues, grammar problems.
- `low`: minor wording, punctuation, or capitalization improvements.

## Field Analysis Rules

Use these field-specific rules when turning review findings into suggestions.

### QuestionName

- Use clear, specific labels that describe the assessed task, not just a body system or generic topic.
- Derive vague names from `Technique` when the technique field contains the actual procedure.
- For note-mode rubrics, do not remove note-section or location wording that tells the grader where to check the learner's note.
- If examples are embedded in `QuestionName`, consider whether they belong in `Technique` instead.

### ScoringLogic

- Score numbers increase with performance quality: `Score1` is the lowest/worst performance and higher score numbers represent better performance.
- Check every score level present, including `Score1`, `Score2`, `Score3`, and any higher levels.
- Score levels should be mutually distinguishable and progressive.
- Avoid overlapping anchors where the same performance could satisfy multiple scores.
- When criteria refer to another field, name that field clearly, such as "the actions listed in Technique."

### Technique

- Use precise clinical terminology when it improves clarity.
- Keep actions observable for the intended evidence mode.
- Do not add examination steps that are not already implied by the rubric, case, or educator context.

### Purpose And AdditionalContext

- Use `Purpose` for the educational or clinical rationale of the item.
- Use `AdditionalContext` for case-specific constraints, acceptable alternatives, uncertainty, or evaluator guidance.
- Remove leading Excel-problematic characters from both fields.
- Keep local constraints from educator context, such as equipment, telehealth limits, mannequin limitations, timing, or learner level.

### Category

Treat `Category` as administrative. Do not suggest category changes unless the category creates a clear alignment or navigation problem.

## Excel And CSV Safety

Any field that starts with `-`, `=`, `+`, or `@` can behave badly in Excel/CSV
contexts. Remove or rewrite those leading characters. For list-like text,
replace leading dash bullets with plain prose or safe separators.

## Pattern Consistency

Before suggesting a change:

- Scan all rows for the same pattern in the same field or score level.
- If the pattern recurs, suggest changes for all affected rows.
- Mention frequency in the reasoning, such as `Pattern found in 12 questions`.
- Do not give a single abstract pattern recommendation when item-level
  suggestions are required.
- Do not use pattern recognition as a shortcut that omits affected rows. If the output is structured suggestions, return each row-level suggestion that should be applied.

## Comprehensive Single-Cell Fixes

When a single cell has multiple problems, make one replacement that fixes the
whole cell.

Example problem types to combine in one cell replacement:

- Excel safety.
- Misspelled medical terminology.
- Grammar.
- Ambiguous wording.
- Missing punctuation needed for clarity.

Avoid multiple suggestions that each modify the same `row` + `field` + `sub`.

## Mode-Specific Assessability Checks

For video-assessable OSCE rubrics, suggested changes should improve:

- Observability: visible or otherwise available in the selected mode.
- Specificity: exact actions rather than vague labels.
- Measurability: clear evidence or counts when helpful.
- Distinguishability: clear separation between score levels.

For note-graded rubrics, preserve location or note-section wording that tells
the AI where to check the student's note.

For audio-graded rubrics, suggestions should focus on spoken content, questions asked, explanations, counseling, rapport, and other transcript-available evidence. Do not require visible physical actions unless the mode is changed.
