---
name: content-validation
description: Validate specific OSCE rubric concerns for clinical validity, assessment quality, severity, and actionable fixes through expert-style critique and synthesis. Use when an agent needs to judge whether a disputed rubric issue or proposed change is valid, including concerns surfaced by dry-run grading, compare competing interpretations, incorporate educator guidance, or produce a consensus recommendation with exact rubric changes.
---

# Content Validation

## Use For

- Validating whether a specific rubric concern is clinically or educationally valid.
- Comparing disputed interpretations or proposed fixes.
- Assigning severity, priority, confidence, and implementation implications.
- Synthesizing a final recommendation after critique or educator guidance.

## Do Not Use For

- Broad first-pass rubric audits; use `osce-rubric-review`.
- Direct adaptation, restyling, score expansion, or template application; use `osce-rubric-transform`.
- Mechanical import from source files; use `rubric-import`.
- New post-encounter-note rubric drafting; use `post-encounter-note-rubric`.
- Generating synthetic student notes or transcripts; use `generate-student-artifact`.
- Dry-run grading a sample artifact against a rubric; use `grading-dry-run`.
- Analyzing a trial grade sheet for routine rubric improvements; use `evaluate-dry-run`. Use `content-validation` only when a dry-run finding needs clinical-validity, fairness, safety, severity, or consensus adjudication.
- Live patient simulation case design; treat as out of scope for this rubric-focused plugin.

## Workflow

1. Clarify the concern, scope, affected rubric rows, case context, learner level, and any educator guidance.
2. Limit rubric evidence to the relevant `QuestionName`, `Category`, or whole-rubric scope.
3. Analyze the concern through distinct lenses: clinical correctness, assessment quality, practical implementation, and safety/fairness.
4. Critique competing interpretations or proposed fixes. Identify real agreement, disagreement, and trade-offs.
5. Refine the recommendation with educator guidance when provided, without overriding clinical safety or assessment validity.
6. Synthesize a final recommendation with exact rubric changes, implementation steps, confidence, caveats, and remaining questions.

## Output

Return the synthesis JSON contract by default. Use round-specific JSON only when the user asks for a specific phase or a workflow needs intermediate artifacts.

For a complete validation, include:

- `synthesized_verdict`
- `synthesized_fix`
- `model_agreement_breakdown`
- `alternative_approaches`
- `caveats_and_considerations`
- `synthesized_reasoning`

If the user explicitly asks for prose, preserve the same sections and semantics.

## References

- Load `references/workflow-guide.md` for CLI workflow, clarification, scope handling, educator guidance, expert lenses, and sibling-skill boundaries.
- Load `references/validation-round-contracts.md` for exact JSON contracts, output routing, severity scales, critique scales, and synthesis format.
- Load `references/rubric-schema.md` when proposed changes must use bundled rubric or suggestion fields.
