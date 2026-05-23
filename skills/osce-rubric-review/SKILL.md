---
name: osce-rubric-review
description: Review OSCE rubrics for clinical alignment, safety, observability, objectivity, feasibility, reliability, scoring clarity, missing Technique/Purpose fields, and Rubric Maker suggestion output. Use when an agent needs to audit an existing rubric, produce clarifying questions, or generate structured improvement suggestions. Use content-validation instead when a specific concern or proposed fix needs clinical-validity adjudication, severity, consensus, or educator-guided tie-breaking.
---

# OSCE Rubric Review

## Use For

- Broad first-pass audits of existing OSCE rubrics.
- Clarifying questions before rubric analysis when case context, station constraints, modality, or educator priorities could change the review.
- Structured Rubric Maker improvement suggestions for discovered issues.
- Finding issues that may later need content validation or transformation.

## Do Not Use For

- Adjudicating a disputed concern, proposed fix, severity, or consensus recommendation; use `content-validation`.
- Direct adaptation, restyling, score expansion, or template application as the main task; use `osce-rubric-transform`.
- Mechanical import from source files; use `rubric-import`.
- New post-encounter-note rubric drafting; use `post-encounter-note-rubric`.
- Grading prompt setup, evidence requirements, or mode assignment for test-station grading; use `test-station-grading`.
- Live patient simulation case design; treat as out of scope for this rubric-focused plugin.

## Sibling Sequence

Use `osce-rubric-review` to discover and frame rubric issues. Escalate selected findings to `content-validation` when their clinical validity, severity, fairness, safety impact, or best fix is contested or high-stakes. Use `osce-rubric-transform` after review or validation when the user wants the rubric content adapted or rewritten.

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
- Load `references/review-framework.md` for the six-pillar audit and clarifying-question workflow.
- Load `references/suggestion-contracts.md` when producing or validating structured improvement suggestions.
