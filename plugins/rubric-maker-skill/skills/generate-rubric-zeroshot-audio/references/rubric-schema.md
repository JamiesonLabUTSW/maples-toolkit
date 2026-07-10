# Rubric Maker Schema Reference

This reference is bundled with each Rubric Maker skill.
It defines the schema used by this plugin for rubric generation, normalization,
rendering, and structured improvement suggestions.

## Core Rubric Object

```yaml
rubric:
  - Category: "Clinical Reasoning"
    QuestionName: "Documents a prioritized differential diagnosis"
    ScoringLogic:
      Score1: "No differential diagnosis is documented."
      Score2: "A limited differential is documented with major omissions."
      Score3: "A plausible differential is documented with minor omissions."
      Score4: "A comprehensive, prioritized differential is documented and justified."
    Mode: "note"
    Technique: "Look for listed diagnoses and case-based justification in the written note."
    Purpose: "Evaluates diagnostic synthesis."
    AdditionalContext: ""
```

## Minimum Versus Plugin Convention

The minimal rubric shape requires:

- `Category`
- `QuestionName`
- `ScoringLogic`

The plugin skill convention requires every generated or normalized rubric item to
include:

- `Category`
- `QuestionName`
- `ScoringLogic`
- `Mode`
- `Technique`
- `Purpose`
- `AdditionalContext`

This stricter plugin convention makes generated rubrics easier to grade, render,
validate, and move between workflows.
When importing existing rubrics, missing optional fields should be normalized to empty
strings rather than omitted.

## Field Rules

- `Category`: Section or grouping for the item.
  Use a nonempty string.
- `QuestionName`: The task being assessed.
  Use a nonempty string.
- `ScoringLogic`: Ordered score anchors.
  Keys must be `Score1`, `Score2`, and so on without gaps.
- `Mode`: One of `video`, `audio`, or `note`.
- `Technique`: Evidence or actions a grader should look for.
  For note mode, describe written documentation evidence.
- `Purpose`: Clinical or educational rationale for the item.
- `AdditionalContext`: Case-specific constraints, acceptable alternatives, uncertainty,
  or evaluator guidance.
  Use an empty string if none.

## Mode Semantics

- `video`: Visible behavior only.
  Use for physical exam actions, visible professionalism, draping, posture, or other
  observable actions.
- `audio`: Spoken content only.
  Use for counseling, verbal explanations, questions, rapport, and communication skills
  when transcript/audio evidence is sufficient.
- `note`: Written post-encounter-note content only.
  Use exact note evidence or `Not found` when grading.

## Suggestion Shape

Structured improvement suggestions should use:

```json
{
  "location": "2:ScoringLogic.Score3",
  "current_value": "Existing exact text",
  "suggested_value": "Replacement text",
  "reasoning": "Why this improves alignment, safety, clarity, or reliability",
  "priority": "high",
  "row": 2,
  "field": "ScoringLogic",
  "sub": "Score3"
}
```

Rules:

- `row` is a zero-based rubric item index.
- `field` is one of `Category`, `QuestionName`, `ScoringLogic`, `Mode`, `Technique`,
  `Purpose`, or `AdditionalContext`.
- `sub` is required only when targeting an individual `ScoringLogic.ScoreN` anchor.
- `current_value` should be copied exactly from the source when editing an existing
  value.
- `priority` must be one of `critical`, `high`, `medium`, or `low`.
