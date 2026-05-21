---
name: content-validation
description: Validate OSCE rubric issues through a multi-perspective expert discussion and synthesize actionable recommendations. Use when Codex needs to assess whether a rubric concern is clinically valid, compare competing interpretations, critique proposed fixes, or produce a final consensus-style recommendation for rubric content changes.
---

# Content Validation

## Workflow

1. Define the issue, scope, affected rubric rows, case context, and any educator guidance.
2. Produce an initial expert analysis: severity, validity, clinical rationale, risks, and proposed changes.
3. Critique alternative viewpoints if provided. Identify where evidence supports or weakens each position.
4. Refine the recommendation into a final position with implementation notes.
5. If enough perspectives exist, synthesize them into a consensus recommendation with confidence and unresolved questions.

## Output

Return a concise validation report:

- `issue_summary`
- `scope`
- `clinical_validity`
- `severity`
- `recommendation`
- `rubric_changes`
- `implementation_notes`
- `remaining_questions`

## References

- Load `../../references/rubrics-app-schema.md` when proposed changes must use app-compatible rubric or suggestion fields.
- Load `references/content-validation-pattern.md` for discussion rounds and synthesis behavior.
