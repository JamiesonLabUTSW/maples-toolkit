---
name: generate-student-artifact
description: Generate synthetic OSCE student artifacts such as post-encounter notes or encounter transcripts from case materials, optional templates, learner profiles, target performance bands, and rubric focus areas. Use when an agent needs realistic sample learner output for dry-run grading. Do not use for grading, rubric critique, rubric revision, raw audio or video generation, or inventing hidden case facts.
---

# Generate Student Artifact

## Use For

- Creating synthetic post-encounter notes from case materials.
- Creating synthetic encounter transcripts from case materials.
- Modeling learner strengths, omissions, misunderstandings, or performance bands.
- Producing examples for later dry-run grading or rubric evaluation.

## Do Not Use For

- Grading the artifact or producing a grade sheet; use `grading-dry-run`.
- Evaluating rubric quality from dry-run results; use `evaluate-dry-run`.
- Drafting, importing, reviewing, or transforming rubrics; use the rubric-focused sibling skill.
- Creating raw audio, video, images, or non-text evidence.
- Adding hidden case facts that are inconsistent with the supplied case.

## Workflow

1. Read the case materials, requested artifact type, learner profile, optional target performance band, optional template, and any rubric focus.
2. Load `references/artifact-generation-contract.md` before producing the final artifact.
3. Load `references/builtin-templates.md` when the user asks for a note or transcript template, does not provide one, or requests template selection.
4. If case facts conflict, preserve the uncertainty in metadata and avoid resolving it by invention.
5. Generate one text artifact that intentionally reflects the requested strengths and weaknesses.
6. Return YAML or JSON with `artifact_type`, `artifact_text`, and `metadata`.
7. Run `scripts/validate_student_artifact.py` on saved JSON or YAML when a file output is requested or when validating a generated artifact.

## Quality Rules

- Keep the artifact plausible for the stated learner level and performance band.
- Make omissions visible through absent, vague, incorrect, or incomplete text rather than explanatory labels inside the artifact.
- Put generation notes, intentional strengths, intentional weaknesses, case summary, learner profile, and limitations in metadata only.
- For transcripts, keep speaker turns explicit and use only text evidence.
- For notes, write the artifact as the learner would submit it, not as a rubric or answer key.

## References

- Load `references/artifact-generation-contract.md` for required output fields and validation rules.
- Load `references/builtin-templates.md` for built-in note and transcript templates.
- Load `references/rubric-schema.md` only when rubric focus is supplied and field semantics matter.
