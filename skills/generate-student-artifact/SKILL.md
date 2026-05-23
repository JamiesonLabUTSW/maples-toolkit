---
name: generate-student-artifact
description: Generate synthetic OSCE student artifacts such as post-encounter notes, encounter transcripts, or transcript-derived observation logs from case materials, optional templates, learner profiles, target performance bands, and rubric focus areas. Use when an agent needs realistic sample learner output for dry-run grading. Do not use for grading, rubric critique, rubric revision, raw audio or video generation, native media analysis, or inventing hidden case facts.
---

# Generate Student Artifact

## Use For

- Creating synthetic post-encounter notes from case materials.
- Creating synthetic encounter transcripts from case materials.
- Creating timestamped synthetic observation logs only from a supplied or already generated encounter transcript.
- Modeling learner strengths, omissions, misunderstandings, or performance bands.
- Producing examples for later dry-run grading or rubric evaluation.

## Do Not Use For

- Grading the artifact or producing a grade sheet; use `grading-dry-run`.
- Evaluating rubric quality from dry-run results; use `evaluate-dry-run`.
- Drafting, importing, reviewing, or transforming rubrics; use the rubric-focused sibling skill.
- Creating raw audio, video, images, or non-text evidence.
- Inferring visual or procedural observations directly from case materials without a transcript source.
- Adding hidden case facts that are inconsistent with the supplied case.

## Workflow

1. Read the case materials, requested artifact type, learner profile, optional target performance band, optional template, any rubric focus, and any supplied transcript.
2. Load `references/artifact-generation-contract.md` before producing the final artifact.
3. Load `references/builtin-templates.md` when the user asks for a note, transcript, or observation-log template, does not provide one, or requests template selection.
4. If case facts conflict, preserve the uncertainty in metadata and avoid resolving it by invention.
5. For `observation_log`, use only a supplied or already generated transcript as the source. If no transcript is available, produce or request a transcript first instead of generating the observation log.
6. Generate one text artifact that intentionally reflects the requested strengths and weaknesses.
7. Return YAML or JSON with `artifact_type`, `artifact_text`, and `metadata`.
8. Run `scripts/validate_student_artifact.py` on saved JSON or YAML when a file output is requested or when validating a generated artifact.

## Quality Rules

- Keep the artifact plausible for the stated learner level and performance band.
- Make omissions visible through absent, vague, incorrect, or incomplete text rather than explanatory labels inside the artifact.
- Put generation notes, intentional strengths, intentional weaknesses, case summary, learner profile, and limitations in metadata only.
- For transcripts, keep speaker turns explicit and use only text evidence.
- For observation logs, write concise timestamped observer-style rows derived from the transcript; do not claim native audio/video inspection.
- For notes, write the artifact as the learner would submit it, not as a rubric or answer key.

## References

- Load `references/artifact-generation-contract.md` for required output fields and validation rules.
- Load `references/builtin-templates.md` for built-in note, transcript, and observation-log templates.
- Load `references/rubric-schema.md` only when rubric focus is supplied and field semantics matter.
