---
name: generate-rubric-zeroshot
description: Draft new note-only generic rubrics from case presented by the user with additional optional uploaded reference materials. Use when an agent needs to synthesize user-provided case materials into Rubric Maker app-compatible note-mode YAML file which is then uploaded straight to OASIS. Do not use for generating OSCE-specific rubrics, importing existing rubrics, transforming or reviewing existing rubrics, generating sample student artifacts, dry-run grading, or live simulation case design.
---
# Generate Rubric Zero-Shot

## Overview

Create a draft generic rubric from case materials.
The output must be a note-only Rubric Maker rubric that can feed downstream note-grading
workflows. Each rubric item has `Category`, `QuestionName`, `ScoringLogic`, `Mode`,
`Technique`, `Purpose`, and `AdditionalContext`.

Use `Mode: note` for every item.

## Required YAML Shape

Use the row-oriented YAML shape below exactly.
Do not nest items under `cases`, `activities`, or `items`. Do not use fields such as
`rubric_name`, `rubric_description`, `modalities`, `case_name`, `activity_name`,
`item_key`, `question_text`, `max_rating`, or numeric scoring keys.

```yaml
name: example-rubric
description: Example rubric
station: Default
version: "1"
context: ""
rubric:
  - ItemKey: ITEM-001
    Category: Example category
    QuestionName: What should the grader assess?
    ScoringLogic:
      Score1: Lowest performance description.
      Score2: Middle performance description.
      Score3: Highest performance description.
    Mode: note
    Technique: Exact written-note evidence to look for.
    Purpose: Educational or technical rationale.
    AdditionalContext: Acceptable alternatives, constraints, or grading cautions.
```

`rubric` must be a non-empty list.
Every list entry must be a flat item mapping.
`ScoringLogic` must use sequential keys from `Score1` through `ScoreN`, ordered from
lowest to highest. Never start at `Score0`.

## Use For

- Drafting a new note-only rubric from user-provided materials.
- Converting case expectations into written-note assessment items.
- Producing Rubric Maker app-compatible note-mode YAML from simple user prompts with
  additional case materials if provided.

## Do Not Use For

- Generating OSCE-specific rubrics with `Mode: osce` or
  `Mode: virtual-patient-simulation`; use `post-encounter-note-rubric` instead.
- Importing or preserving an existing rubric, table, CSV/XLSX extract, checklist, or
  prose scoring guide as-is; use `rubric-import`.
- Reviewing an existing rubric for quality, safety, objectivity, missing fields, or
  improvement suggestions; use `osce-rubric-review`.
- Transforming, restyling, adapting, expanding score levels, or filling missing fields
  in an existing rubric; use `osce-rubric-transform`.
- Validating a disputed concern, proposed fix, clinical-validity question, severity, or
  consensus recommendation; use `content-validation`.
- Generating synthetic student notes or transcripts for rubric testing; use
  `generate-student-artifact`.
- Dry-run grading a student artifact against a rubric or producing a trial grade sheet;
  use `grading-dry-run`.
- Analyzing a trial grade sheet to identify rubric improvements; use `evaluate-dry-run`.
- Designing live virtual patient simulation cases; treat as out of scope for this
  rubric-focused plugin.

## Sibling Sequence

Use `generate-rubric-zeroshot` when the starting point is generic user prompt and the
desired output is a new written-note rubric.
After drafting, use `osce-rubric-review` for a broad quality audit,
`osce-rubric-transform` for requested rewrites or score-scale changes, `grading-dry-run`
to produce a trial grade sheet, and `evaluate-dry-run` to turn dry-run friction into
rubric improvement suggestions.

## Workflow

1. Load `references/rubric-maker-yaml-to-maples-mapping.md` before drafting.
2. Read the provided scenario.
3. DO NOT ask clarifying questions.
   Draft the rubric from whatever the user provides, even if the materials are sparse or
   ambiguous. Make conservative assumptions about rubric structure, item count, learner
   level, and scoring granularity, and list those assumptions in a short preamble before
   the rubric. Do not invent scenario case facts — if a fact is uncertain, capture that
   uncertainty in `AdditionalContext` on the affected item rather than pausing to ask
   the user.
4. Create 8-15 rubric items unless the user requests a different size.
   Keep items single-purpose and evidence-based.
5. Write scoring levels from lowest to highest as `Score1`, `Score2`, etc.
   Use 3-5 levels by default.
   Make each level independently scorable from the note text.
6. Include `Technique` as the exact written-note evidence the grader should look for.
   Include `Purpose` as the educational or technical rationale.
   Use `AdditionalContext` for case-specific constraints, acceptable alternatives,
   uncertainty, and downstream grading cautions.
7. Produce the rubric as YAML by default; produce JSON only if the user explicitly asks.
8. Upload the rubric directly to OASIS by calling `upload_rubric` with the YAML body
   passed as `content` and a `filename` like `<rubric-name>.yaml`. Use `Mode: note`. Do
   not write the rubric to disk first — passing `content` avoids creating and then
   cleaning up a temporary file.
9. If the upload fails, analyze and compare the generated rubric to the required YAML
   shape and examples in references/ two more times.
   If it fails after the third attempt, return an error instead of continuing.

## Quality Rules

- Grade only what can be found in the written note; avoid criteria that require knowing
  what happened in the encounter unless the note documents it.
- Prefer concrete evidence: named symptoms, pertinent negatives, clinical reasoning,
  prioritized differential, justified plan, follow-up, return precautions.
- Avoid double-barrel items.
  Split separate skills into separate rubric rows.
- Include safety-critical omissions when the case has clear red flags, medication risks,
  dangerous diagnoses, or follow-up needs.
- Align difficulty with learner level.
  For novice learners, reward core completeness and organization; for advanced learners,
  reward prioritization, synthesis, and management justification.
- Do not invent case facts.
  If a likely criterion depends on unavailable facts, put the uncertainty in
  `AdditionalContext`.

## References

- Load `references/BloodPressure_OSCE.fixed.xlsx` for a sample rubric source scenario.
- Load `references/rubric-maker-yaml-to-maples-mapping.md` for the rubric item field
  definitions and quality rules.
