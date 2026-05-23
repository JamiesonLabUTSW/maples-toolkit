---
name: osce-rubric-review
description: Review OSCE rubrics for clinical alignment, safety, observability, objectivity, feasibility, reliability, scoring clarity, missing Technique/Purpose fields, and Rubric Maker suggestion output. Use when an agent needs to audit an existing rubric, produce clarifying questions, or generate structured improvement suggestions.
---

# OSCE Rubric Review

## Workflow

1. Read the rubric and any case scenario, station instructions, learner level, modality, or evaluator constraints.
2. Audit with the six rubric quality pillars: alignment, safety, observability, objectivity, feasibility, and reliability.
3. Focus on clinical substance before wording. Flag mismatches, missing critical steps, vague anchors, double-barrel items, mode mismatches, and score levels that are not distinguishable.
4. If context is incomplete, generate 2-4 clarifying questions with concrete answer options.
5. When asked for revisions, return structured suggestions with `location`, `current_value`, `suggested_value`, `reasoning`, `priority`, `row`, `field`, and optional `sub`.

## Output Guidance

- For a quick review, lead with high-priority findings and line/row references.
- For structured suggestions, use locations like `0:QuestionName` or `2:ScoringLogic.Score3`.
- Keep `current_value` exact when editing existing text.
- Use priority values: `critical`, `high`, `medium`, `low`.

## References

- Load `references/rubric-schema.md` for the shared schema, mode semantics, and structured suggestion conventions.
- Load `references/review-framework.md` for the six-pillar audit.
