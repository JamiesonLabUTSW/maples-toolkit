---
name: osce-rubric-transform
description: This skill should be used when the user asks to adapt an OSCE rubric to a new case, patient population, clinical setting, learner role, scoring scale, institutional template, or accepted dry-run finding; "add score levels"; "fill missing Purpose or Technique"; "expand Technique examples"; "apply this rubric as a template"; or "restyle this target rubric" while preserving clinical intent.
---

# OSCE Rubric Transform

## Use For

- Directly adapting an existing OSCE rubric to a new case, station, patient population, clinical setting, learner level, or assessed role.
- Generating row-level Rubric Maker suggestions for content changes, score expansion, missing fields, technique expansion, or template/style application.
- Adding or refining `ScoringLogic.ScoreN` levels when the user asks for a new scoring scale or more granular performance bands.
- Filling missing `Purpose`, `Technique`, or `AdditionalContext` fields for existing rubric rows.
- Applying naming, phrasing, score-anchor style, field density, or institutional template patterns from a reference rubric to a target rubric.
- Applying accepted rubric-improvement suggestions produced by dry-run evaluation.

## Do Not Use For

- Broad first-pass rubric audits or issue discovery; use `osce-rubric-review`.
- Adjudicating whether a disputed concern or proposed fix is clinically valid, severe, fair, or preferred; use `content-validation`.
- Mechanical import from source files, CSV/XLSX extracts, tables, checklists, or prose guides; use `rubric-import`.
- New post-encounter-note rubric drafting from case materials; use `post-encounter-note-rubric`.
- Generating synthetic student notes or transcripts; use `generate-student-artifact`.
- Dry-run grading a student artifact against a rubric or producing a trial grade sheet; use `grading-dry-run`.
- Evaluating a dry-run grade sheet for rubric improvement opportunities; use `evaluate-dry-run`.
- Live virtual patient simulation case design; treat as out of scope for this rubric-focused plugin.

## Sibling Sequence

Use `osce-rubric-review` to discover broad rubric issues. Use `evaluate-dry-run` to identify changes based on a case, sample artifact, and trial grade sheet. Use `content-validation` when a finding, proposed fix, or transformation would change clinical facts or needs validity/severity adjudication. Use `osce-rubric-transform` when the user wants selected rubric content, scoring, missing fields, dry-run findings, or style changes implemented as suggestions or an explicit complete rewrite.

## Workflow

1. Identify the source rubric, target context, learner level, modality, and transformation goal.
2. Preserve clinically valid source content unless the target context makes it wrong, unsafe, unobservable, or misaligned.
3. Generate specific row-level changes. Do not rewrite the entire rubric when targeted suggestions are safer.
4. For missing fields, write `Purpose` as the educational rationale and `Technique` as observable examples or documentation evidence.
5. For score expansion, keep score levels ordered from lowest to highest and make adjacent levels meaningfully different.
6. For template application, copy style patterns without changing clinical facts unless explicitly requested.

## Subworkflow Routing

Load `references/transform-subworkflows.md` for every structured suggestion workflow. It contains the exact JSON contract, field restrictions, upstream transformation/enhancement/template rules, sibling boundaries, and empty-result behavior.

Within that reference:

- Use **Case Or Role Transformation** for new case, station, population, setting, or learner-role adaptation.
- Use **Add Scores** for score-scale expansion or score-anchor refinement.
- Use **Fill Missing Fields** for missing `Purpose`, `Technique`, or `AdditionalContext`.
- Use **Expand Techniques** for richer observable examples and any resulting scoring alignment changes.
- Use **Template Or Style Application** for reference-rubric style, institutional template, naming, phrasing, score progression, field density, or formatting transfer.

## Output Guidance

- Prefer structured suggestions using `location`, `current_value`, `suggested_value`, `reasoning`, `priority`, `row`, `field`, and optional `sub`.
- For existing rubrics, structured suggestions are the default. Output full Rubric Maker schema YAML only when the user explicitly asks for a complete replacement artifact or when suggestions cannot represent the requested rewrite cleanly.
- Explain assumptions when transforming a case with incomplete information.

## References

- Load `references/rubric-schema.md` for the shared schema, mode semantics, and structured suggestion conventions.
- Load `references/transform-subworkflows.md` for the required transform/enhancement/template workflow contract and field-level rules.
- Load `references/transform-patterns.md` only as a quick orientation summary when a lightweight reminder is enough.
