---
name: generate-rubric-zeroshot-multimodal
description: Draft new multimodal generic rubrics from case presented by the user with additional optional uploaded reference materials. Use when an agent needs to synthesize user-provided case materials into one Rubric Maker app-compatible YAML file containing any requested combination of note, audio, and video rubric items, then upload it straight to OASIS. Do not use for single-modality note-only, audio-only, or video-only rubrics, importing existing rubrics, transforming or reviewing existing rubrics, generating sample student artifacts, dry-run grading, or live simulation case design.
---
# Generate Rubric Zero-Shot Multimodal

## Overview

Create a draft generic rubric from case materials.
The output must be one multimodal Rubric Maker rubric that can feed downstream
note-, audio-, and/or video-grading workflows. Each rubric item has `Category`,
`QuestionName`, `ScoringLogic`, `Mode`, `Technique`, `Purpose`, and
`AdditionalContext`.

Use `Mode: note`, `Mode: audio`, or `Mode: video` on each item according to the
evidence source that item should grade. Include only modalities requested or clearly
implied by the user-provided scenario. Do not create separate YAML files for separate
modalities.

## Required YAML Shape

Use the row-oriented YAML shape below exactly. Do not nest items under `cases`,
`activities`, or `items`. Do not use fields such as `rubric_name`,
`rubric_description`, `modalities`, `case_name`, `activity_name`, `item_key`,
`question_text`, `max_rating`, or numeric scoring keys.

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
  - ItemKey: ITEM-002
    Category: Example category
    QuestionName: What spoken behavior should the grader assess?
    ScoringLogic:
      Score1: Lowest performance description.
      Score2: Middle performance description.
      Score3: Highest performance description.
    Mode: audio
    Technique: Exact spoken, paralinguistic, or interactional evidence to listen for.
    Purpose: Educational or technical rationale.
    AdditionalContext: Acceptable alternatives, transcript-quality limitations, or grading cautions.
  - ItemKey: ITEM-003
    Category: Example category
    QuestionName: What visible behavior should the grader assess?
    ScoringLogic:
      Score1: Lowest performance description.
      Score2: Middle performance description.
      Score3: Highest performance description.
    Mode: video
    Technique: Exact visible behavior, task performance, or observable interaction evidence to look for.
    Purpose: Educational or technical rationale.
    AdditionalContext: Acceptable alternatives, camera-angle or visibility limitations, or grading cautions.
```

`rubric` must be a non-empty list. Every list entry must be a flat item mapping.
Every item must have exactly one `Mode`: `note`, `audio`, or `video`.
`ScoringLogic` must use sequential keys from `Score1` through `ScoreN`, ordered from
lowest to highest. Never start at `Score0`.

## Use For

- Drafting one new rubric that combines any requested subset of note, audio, and video items.
- Converting case expectations into written-note, spoken-communication, observable-performance,
  physical-exam, procedural, and interaction assessment items.
- Producing Rubric Maker app-compatible multimodal YAML from simple user prompts with additional case materials if provided.

## Do Not Use For

- Generating note-only rubrics; use `generate-rubric-zeroshot` instead.
- Generating audio-only rubrics; use `generate-rubric-zeroshot-audio` instead.
- Generating video-only rubrics; use `generate-rubric-zeroshot-video` instead.
- Generating OSCE-specific rubrics with `Mode: osce` or `Mode: virtual-patient-simulation`;
  use `post-encounter-note-rubric` instead.
- Importing or preserving an existing rubric, table, CSV/XLSX extract, checklist, or
  prose scoring guide as-is; use `rubric-import`.
- Reviewing an existing rubric for quality, safety, objectivity, missing fields, or
  improvement suggestions; use `osce-rubric-review`.
- Transforming, restyling, adapting, expanding score levels, or filling missing fields
  in an existing rubric; use `osce-rubric-transform`.
- Validating a disputed concern, proposed fix, clinical-validity question, severity, or
  consensus recommendation; use `content-validation`.
- Generating synthetic student notes, transcripts, videos, or artifacts for rubric testing; use
  `generate-student-artifact`.
- Dry-run grading a student artifact against a rubric or producing a trial grade sheet;
  use `grading-dry-run`.
- Analyzing a trial grade sheet to identify rubric improvements; use `evaluate-dry-run`.
- Designing live virtual patient simulation cases; treat as out of scope for this
  rubric-focused plugin.

## Sibling Sequence

Use `generate-rubric-zeroshot-multimodal` when the starting point is a generic user
prompt and the desired output is one rubric containing any combination of note,
audio, and video items.
Use `generate-rubric-zeroshot` for note-only rubrics,
`generate-rubric-zeroshot-audio` for audio-only rubrics, and
`generate-rubric-zeroshot-video` for video-only rubrics.
After drafting, use `osce-rubric-review` for a broad quality audit, `osce-rubric-transform` for requested rewrites or score-scale changes, `grading-dry-run` to produce a trial grade sheet, and `evaluate-dry-run` to turn dry-run friction into rubric improvement suggestions.

## Workflow

1. Load `references/MAPLES Rubric Specification.md` before drafting.
2. Read the provided scenario.
3. DO NOT ask clarifying questions. Draft the rubric from whatever the user provides,
   even if the materials are sparse or ambiguous. Make conservative assumptions about
   rubric structure, item count, learner level, and scoring granularity, and list those
   assumptions in a short preamble before the rubric. Do not invent scenario case facts —
   if a fact is uncertain, capture that uncertainty in `AdditionalContext` on the
   affected item rather than pausing to ask the user.
4. Create 8-15 rubric items unless the user requests a different size.
   Keep items single-purpose and evidence-based.
   Allocate items across `note`, `audio`, and `video` according to the requested
   modalities and the evidence that can be scored from each modality.
5. Write scoring levels from lowest to highest as `Score1`, `Score2`, etc.
   Use 3-5 levels by default.
   Make each level independently scorable from the item's declared modality.
6. Include `Technique` as the exact modality-specific evidence the grader should use:
   written-note evidence for `Mode: note`, spoken or transcript evidence for
   `Mode: audio`, and visible behavior or task performance for `Mode: video`.
   Include `Purpose` as the educational or technical rationale.
   Use `AdditionalContext` for case-specific constraints, acceptable alternatives,
   uncertainty, transcript-quality limitations, camera-angle or visibility limitations,
   and downstream grading cautions.
7. Produce the rubric as YAML by default; produce JSON only if the user explicitly asks.
8. Upload the rubric directly to OASIS by calling `upload_rubric` with the YAML body
   passed as `content` and a `filename` like `<rubric-name>.yaml`. Use only
   `Mode: note`, `Mode: audio`, and/or `Mode: video` as appropriate for each item.
   Do not write the rubric to disk first — passing `content` avoids creating and then
   cleaning up a temporary file.
9. If the upload fails, analyze and compare the generated rubric to the required YAML shape
   and examples in references/ two more time. If it fails after the third attempt,
   return an error instead of continuing.

## Quality Rules

- Grade each item only from evidence available in that item's `Mode`.
- For `Mode: note`, grade only what can be found in the written note. Prefer concrete
  evidence such as named symptoms, pertinent negatives, clinical reasoning,
  prioritized differential, justified plan, follow-up, and return precautions.
- For `Mode: audio`, grade only what can be heard in the audio recording or reliably
  represented in an audio transcript. Prefer spoken questions, explanations,
  clinical reasoning, patient-centered language, teach-back, summaries, respectful
  tone, and verbal handling of safety-critical concerns.
- For `Mode: video`, grade only what can be observed in the video recording. Prefer
  physical-exam maneuvers, procedural steps, infection-control behaviors, patient
  positioning, use of equipment, safety checks, nonverbal rapport, task sequencing,
  and visible response to patient cues.
- Do not mix evidence channels inside a single item. Split criteria into separate rows
  when one part is note-scorable, another is audio-scorable, and another is video-scorable.
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

- Load `references/BloodPressure_OSCE.fixed.xlsx` for a sample rubric source scenario 
- Load `references/MAPLES Rubric Specification.md` for the rubric item field definitions and quality rules.
- Load `../../../../../mcp/tools/rubric.py` for the `upload_rubric` tool to upload the output rubric to OASIS.
