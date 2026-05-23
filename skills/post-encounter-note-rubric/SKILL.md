---
name: post-encounter-note-rubric
description: Draft post-encounter-note grading rubrics from OSCE case files, station instructions, SP scripts, expected findings, sample notes, checklists, or clinical scenarios. Use when an agent needs to synthesize case materials into a note-mode rubric compatible with the /rubrics app schema, especially for SOAP notes, clinical documentation, assessment/plan, differential diagnosis, or written post-encounter note evaluation.
---

# Post Encounter Note Rubric

## Overview

Create a draft OSCE post-encounter-note rubric from case materials. Follow the `/rubrics` app conventions: each rubric item has `Category`, `QuestionName`, `ScoringLogic`, `Mode`, `Technique`, `Purpose`, and `AdditionalContext`.

Use `Mode: note` for every item unless the user explicitly asks for mixed video/audio/note assessment.

## Workflow

1. Read the provided case files and identify the station goal, learner level, patient problem, expected findings, red flags, clinical reasoning targets, required documentation sections, and scoring constraints.
2. If critical context is missing, make conservative assumptions about rubric structure, item count, learner level, or scoring granularity and list them before the rubric. Do not invent clinical case facts; if a clinical fact is uncertain, mark that uncertainty in `AdditionalContext`. Ask a question only when the rubric cannot be responsibly drafted without the answer.
3. Derive assessable note domains, usually: chief concern/HPI, relevant ROS, pertinent positives/negatives, PMH/medications/allergies, exam or data interpretation, problem representation, differential diagnosis, assessment, plan, safety-netting, patient-centered communication documented in the note, and organization/clarity.
4. Create 8-15 rubric items unless the user requests a different size. Keep items single-purpose and evidence-based.
5. Write scoring levels from lowest to highest as `Score1`, `Score2`, etc. Use 3-5 levels by default. Make each level independently scorable from the note text.
6. Include `Technique` as the expected documentation evidence, not physical exam technique. Include `Purpose` as the educational/clinical rationale.
7. Output YAML by default, using the exact schema in `references/rubrics-app-format.md`. Output JSON only if the user asks.

## Quality Rules

- Grade only what can be found in the written note; avoid criteria that require knowing what happened in the encounter unless the note documents it.
- Prefer concrete evidence: named symptoms, pertinent negatives, clinical reasoning, prioritized differential, justified plan, follow-up, return precautions.
- Avoid double-barrel items. Split separate skills into separate rubric rows.
- Include safety-critical omissions when the case has clear red flags, medication risks, dangerous diagnoses, or follow-up needs.
- Align difficulty with learner level. For novice learners, reward core completeness and organization; for advanced learners, reward prioritization, synthesis, and management justification.
- Do not invent case facts. If a likely criterion depends on unavailable facts, put the uncertainty in `AdditionalContext`.

## References

- Load `references/rubrics-app-schema.md` for the shared schema, mode semantics, and structured suggestion conventions.
- Load `references/rubrics-app-format.md` for the required schema and field semantics.
- Load `references/post-encounter-note-guide.md` for item design patterns and output examples.
- Load `references/openai-implementation-notes.md` when implementing API-backed generation or structured outputs.
- Load `references/rubrics-app-source-map.md` when checking how this mirrors the `/rubrics` app.
