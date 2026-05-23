# Analysis Suggestion Contracts

This reference captures rules for OSCE rubric review suggestions. Use it when
converting critique into structured suggestions or checking whether a review
result follows the bundled Rubric Maker suggestion contract.

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

## Video Assessability Checks

For video-assessable OSCE rubrics, suggested changes should improve:

- Observability: visible or otherwise available in the selected mode.
- Specificity: exact actions rather than vague labels.
- Measurability: clear evidence or counts when helpful.
- Distinguishability: clear separation between score levels.

For note-graded rubrics, preserve location or note-section wording that tells
the AI where to check the student's note.
