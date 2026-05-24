# Dry-Run Suggestion Contract

Use this contract when producing rubric-improvement suggestions from dry-run
grading analysis or validating suggestion output.

## Recommended Top-Level Shape

```json
{
  "findings": [
    {
      "id": "F1",
      "pattern": "ambiguous_scoring_anchors",
      "priority": "high",
      "rubric_location": "2:ScoringLogic",
      "dry_run_evidence": "The grade-sheet rationale fits both Score2 and Score3.",
      "impact": "Adjacent bands are not reliably distinguishable."
    }
  ],
  "suggestions": [
    {
      "location": "2:ScoringLogic.Score3",
      "current_value": "Existing exact text",
      "suggested_value": "Replacement text",
      "reasoning": "Why this improves dry-run grading reliability",
      "priority": "high",
      "row": 2,
      "field": "ScoringLogic",
      "sub": "Score3",
      "finding_id": "F1",
      "failure_pattern": "ambiguous_scoring_anchors",
      "dry_run_evidence": "The grade-sheet rationale fits both Score2 and Score3."
    }
  ]
}
```

For workflows that only accept rubric suggestions, a raw suggestion array is
also valid.

## Required Suggestion Fields

- `location`
- `current_value`
- `suggested_value`
- `reasoning`
- `priority`
- `row`
- `field`

Allowed rubric fields are `Category`, `QuestionName`, `ScoringLogic`, `Mode`,
`Technique`, `Purpose`, and `AdditionalContext`.

Use `sub` only for nested `ScoringLogic.ScoreN` suggestions. For other fields,
omit `sub` or set it to `null`.

## Optional Dry-Run Fields

- `finding_id`: Links a suggestion to a finding such as `F1`.
- `failure_pattern`: One of the dry-run failure pattern identifiers.
- `dry_run_evidence`: Concise evidence from the case, artifact, or grade sheet.
- `confidence`: `high`, `medium`, or `low`.

## Failure Pattern Identifiers

- `ambiguous_scoring_anchors`
- `unobservable_or_unsupported_item`
- `missing_case_critical_expectation`
- `evidence_rubric_mismatch`
- `redundant_items`
- `weak_discrimination`
- `misweighted_priority`
- `unsafe_or_fairness_impacting_behavior`

## Exact Current Value Rule

`current_value` must match the source rubric cell exactly. If multiple issues
affect one cell, create one replacement for the whole cell rather than several
partial edits. Empty string is valid only when the source rubric value is empty,
such as an empty `AdditionalContext` cell.

The validator can enforce this rule only when the source rubric is provided:

```bash
python3 scripts/validate_dry_run_suggestions.py --rubric rubric.yaml suggestions.yaml
```

With `--rubric`, the validator checks that `row`, `field`, optional `sub`, and
`current_value` match the source rubric. The rubric may be either a raw rubric
array or an object with a top-level `rubric` array. Without `--rubric`, the
validator performs shape-only validation and internal consistency checks, such
as whether `location` agrees with `row`, `field`, and `sub`; it cannot prove
that `current_value` was copied from the source rubric.

For nested scoring anchors, target the exact anchor with `sub`, for example
`field: ScoringLogic` and `sub: Score3`. This lets the validator compare
`current_value` to the exact `ScoringLogic.Score3` source text.

## No-Suggestions Behavior

Return:

```json
{
  "findings": [],
  "suggestions": []
}
```

or a raw empty array `[]` when the dry run reveals no actionable rubric changes.
