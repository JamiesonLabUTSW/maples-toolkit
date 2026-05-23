---
name: post-encounter-note-rubric
description: Draft new note-only post-encounter-note OSCE grading rubrics from case files, station instructions, SP scripts, expected findings, sample notes, checklists, or clinical scenarios. Use when an agent needs to synthesize case materials into Rubric Maker app-compatible note-mode YAML for SOAP notes, clinical documentation, assessment/plan, differential diagnosis, or written post-encounter-note evaluation. Do not use for importing existing rubrics, transforming or reviewing existing rubrics, mixed video/audio/note mode setup, grading prompt setup, or live simulation case design.
---

# Post Encounter Note Rubric

## Overview

Create a draft OSCE post-encounter-note rubric from case materials. The output must be a note-only Rubric Maker rubric that can feed the upstream test-station note-grading workflow. Each rubric item has `Category`, `QuestionName`, `ScoringLogic`, `Mode`, `Technique`, `Purpose`, and `AdditionalContext`.

Use `Mode: note` for every item. If the user asks for mixed video/audio/note assessment, mode splitting, or grading prompt setup, stop using this skill and use `test-station-grading`.

## Use For

- Drafting a new post-encounter-note rubric from OSCE case materials.
- Converting case expectations into written-note assessment items.
- Building SOAP note, assessment/plan, differential diagnosis, clinical reasoning, documentation quality, safety-netting, and written management-plan criteria.
- Producing Rubric Maker app-compatible note-mode YAML from clinical scenarios, station instructions, SP scripts, answer keys, expected findings, or sample notes.

## Do Not Use For

- Importing or preserving an existing rubric, table, CSV/XLSX extract, checklist, or prose scoring guide as-is; use `rubric-import-structure`.
- Reviewing an existing rubric for quality, safety, objectivity, missing fields, or improvement suggestions; use `osce-rubric-review`.
- Transforming, restyling, adapting, expanding score levels, or filling missing fields in an existing rubric; use `osce-rubric-transform`.
- Validating a disputed concern, proposed fix, clinical-validity question, severity, or consensus recommendation; use `content-validation`.
- Assigning modes, splitting a rubric across video/audio/note evidence, designing grading prompts, or preparing test-station grading workflows; use `test-station-grading`.
- Designing live virtual patient simulation cases; treat as out of scope for this rubric-focused plugin.

## Sibling Sequence

Use `post-encounter-note-rubric` when the starting point is case material and the desired output is a new written-note rubric. After drafting, use `osce-rubric-review` for a broad quality audit, `content-validation` for contested clinical concerns, `osce-rubric-transform` for requested rewrites or score-scale changes, and `test-station-grading` when the user needs grading prompts or mixed evidence setup.

## Workflow

1. Load `references/rubric-format.md`, `references/post-encounter-note-guide.md`, and `references/note-grading-compat.md` before drafting.
2. Read the provided case files and identify the station goal, learner level, patient problem, expected findings, red flags, clinical reasoning targets, required note sections, and scoring constraints.
3. If critical context is missing, make conservative assumptions about rubric structure, item count, learner level, or scoring granularity and list them before the rubric. Do not invent clinical case facts. If a clinical fact is uncertain, mark that uncertainty in `AdditionalContext`. Ask a question only when the rubric cannot be responsibly drafted without the answer.
4. Derive assessable note domains, usually: chief concern/HPI, relevant ROS, pertinent positives/negatives, PMH/medications/allergies, exam or data interpretation, problem representation, differential diagnosis, assessment, plan, safety-netting, patient-centered communication documented in the note, and organization/clarity.
5. Create 8-15 rubric items unless the user requests a different size. Keep items single-purpose and evidence-based.
6. Write scoring levels from lowest to highest as `Score1`, `Score2`, etc. Use 3-5 levels by default. Make each level independently scorable from the note text.
7. Include `Technique` as the exact written-note evidence the grader should look for. Include `Purpose` as the educational or clinical rationale. Use `AdditionalContext` for case-specific constraints, acceptable alternatives, uncertainty, and downstream grading cautions.
8. Output YAML by default, using the exact schema in `references/rubric-format.md`. Output JSON only if the user asks.

## Quality Rules

- Grade only what can be found in the written note; avoid criteria that require knowing what happened in the encounter unless the note documents it.
- Prefer concrete evidence: named symptoms, pertinent negatives, clinical reasoning, prioritized differential, justified plan, follow-up, return precautions.
- Avoid double-barrel items. Split separate skills into separate rubric rows.
- Include safety-critical omissions when the case has clear red flags, medication risks, dangerous diagnoses, or follow-up needs.
- Align difficulty with learner level. For novice learners, reward core completeness and organization; for advanced learners, reward prioritization, synthesis, and management justification.
- Do not invent case facts. If a likely criterion depends on unavailable facts, put the uncertainty in `AdditionalContext`.

## References

- Load `references/rubric-schema.md` for the shared schema, mode semantics, and structured suggestion conventions.
- Load `references/rubric-format.md` for the required schema and field semantics.
- Load `references/post-encounter-note-guide.md` for item design patterns, section strategy, scoring guidance, and output examples.
- Load `references/note-grading-compat.md` for upstream Rubric Maker app note-grading behavior and field-level authoring implications.
- Load `references/openai-implementation-notes.md` when implementing API-backed generation or structured outputs.
