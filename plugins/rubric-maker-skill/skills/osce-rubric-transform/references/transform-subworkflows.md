# Transform And Enhancement Subworkflows

This reference carries the operational contract for OSCE rubric transformation,
enhancement, and template/style application.
Load it whenever `osce-rubric-transform` needs to produce structured suggestions or a
complete replacement rubric.

## Table Of Contents

- [Shared Suggestion Contract](#shared-suggestion-contract)
- [Output Selection](#output-selection)
- [Case Or Role Transformation](#case-or-role-transformation)
- [Add Scores](#add-scores)
- [Fill Missing Fields](#fill-missing-fields)
- [Expand Techniques](#expand-techniques)
- [Template Or Style Application](#template-or-style-application)
- [Priority Guidance](#priority-guidance)
- [Sibling Skill Boundaries](#sibling-skill-boundaries)
- [Do Not Port From The App](#do-not-port-from-the-app)
- [Empty Result](#empty-result)

## Shared Suggestion Contract

All transform/enhancement outputs for existing rubrics are JSON suggestions:

```json
{
  "location": "0:ScoringLogic.Score2",
  "priority": "medium",
  "reasoning": "Specific clinical or educational justification",
  "row": 0,
  "field": "ScoringLogic",
  "sub": "Score2",
  "current_value": "Exact current text",
  "suggested_value": "Replacement text"
}
```

Rules:

- Rows are 0-based.
- `current_value` must be copied exactly from the source cell when editing existing
  content.
- For new content, use an empty string for `current_value`.
- `field` must be one of `Category`, `QuestionName`, `ScoringLogic`, `Mode`,
  `Technique`, `Purpose`, or `AdditionalContext`.
- `sub` is required for `ScoringLogic` score anchors and must be a score key such as
  `Score1`, `Score2`, or `Score3`.
- `sub` must be `null` for non-`ScoringLogic` fields.
- For `ScoringLogic` fields, make one suggestion per score key.
  Do not combine multiple score levels in one suggestion.
- Each field change requires its own suggestion.
- Prefer `[]` over speculative suggestions when no actionable change is needed.

Location format:

- Simple field: `0:QuestionName`
- Nested score anchor: `0:ScoringLogic.Score1`
- Category on row 5: `5:Category`
- Technique on row 10: `10:Technique`

## Output Selection

Default to structured suggestions for existing rubrics because the Rubric Maker workflow
can review, accept, reject, and track individual changes.

Use complete Rubric Maker YAML only when:

- The user explicitly asks for a full replacement rubric.
- The source rubric is too incomplete for row-level suggestions to be meaningful.
- The requested transformation changes most rows and a complete rewrite is safer than a
  very large suggestion list.

When producing YAML, follow `rubric-schema.md` and preserve the plugin convention that
every row has `Category`, `QuestionName`, `ScoringLogic`, `Mode`, `Technique`,
`Purpose`, and `AdditionalContext`.

## Case Or Role Transformation

Purpose: adapt an existing rubric to a new clinical case, station, patient population,
clinical setting, or assessed role.

Use this subworkflow when the user asks to:

- Adapt this rubric for a different case.
- Transform this station for a pediatric, geriatric, telehealth, inpatient, emergency,
  outpatient, or other context.
- Change the assessed role, such as physician to nurse, student to resident, or
  clinician to allied health role.
- Make a case-specific version of a general rubric.

Allowed fields:

- `Category`
- `QuestionName`
- `ScoringLogic`
- `Mode`
- `Technique`
- `Purpose`
- `AdditionalContext`

Required process for every rubric row:

1. Assess applicability: decide whether the item remains relevant in the new context.
2. Identify required changes: determine what specific modifications are needed.
3. Check scoring adjustments: decide how performance expectations change.
4. Check observable behaviors: identify different actions, words, documentation
   evidence, or evaluator cues assessors should look for.
5. Provide clinical rationale: justify why the change is necessary for validity,
   fairness, feasibility, safety, or assessment reliability.
6. Generate separate suggestions for each field and each score anchor that needs a
   change.

Consider these transformation dimensions:

- Patient demographics: age, sex or gender where relevant, cultural background,
  language, health literacy, cognitive capacity, and communication needs.
- Clinical setting: emergency department, outpatient clinic, inpatient ward, telehealth,
  home visit, simulation center, or other setting.
- Clinical focus: chief complaint, body system, acuity, urgency, differential diagnosis,
  and dangerous-miss diagnoses.
- Available resources: equipment, time, support staff, privacy, interpreter access,
  monitoring, and physical constraints.
- Communication adaptations: age-appropriate language, trauma-informed communication,
  caregiver involvement, shared decision-making, and cultural considerations.
- Role scope: legal and professional scope of practice, team handoffs, supervision,
  documentation duties, and role-specific technical or communication expectations.
- Evidence mode: whether the item can be scored from `video`, `audio`, or `note`
  evidence alone.

Field-specific guidance:

- `QuestionName`: reword only when the task name itself must change for the new case,
  role, setting, or patient population.
- `Purpose`: update when the competency, clinical rationale, safety relevance, or
  educational objective changes.
- `Technique`: update when observable actions, exact phrases, documentation evidence,
  patient interaction, equipment, or acceptable variations change.
- `ScoringLogic`: assess each score level separately.
  Adjust criteria only when expectations, observable evidence, or fairness changes in
  the new context.
- `Mode`: change only when the evidence source must change.
  Do not change mode casually.
- `AdditionalContext`: add case-specific evaluator constraints, acceptable alternatives,
  uncertainty, or special considerations.

Constraints:

- Preserve clinically valid source content unless the target context makes it wrong,
  unsafe, unobservable, unfair, or misaligned.
- Preserve rigor and fairness from the source rubric.
- Keep unchanged items unchanged.
- Do not skip rows or rely on pattern shortcuts.
- Do not invent clinical facts that are absent from the source and target context.
  Mark uncertainty in `AdditionalContext` or assumptions when needed.
- For scoring changes, separate `Score1`, `Score2`, etc.
  into individual suggestions.

## Add Scores

Purpose: add intermediate score levels or refine existing score descriptions for better
performance differentiation.

Use this subworkflow when the user asks to:

- Add score levels.
- Expand from a 2-point scale to a 3-, 4-, or 5-point scale.
- Add intermediate performance bands.
- Make scoring more granular.
- Refine score anchors so adjacent levels are distinguishable.

Field restrictions:

- `field` must be `ScoringLogic`.
- `sub` must be a score key such as `Score1`, `Score2`, or `Score3`.
- New score levels use `current_value: ""`.
- Do not modify `QuestionName`, `Technique`, `Purpose`, `Mode`, `Category`, or
  `AdditionalContext` in this subworkflow.

Scoring rules:

- `Score1` is the lowest score.
- Higher score numbers represent better performance.
- Use only as many score levels as meaningful.
- A configured maximum score level is a cap, not a requirement.
- More score levels are not automatically better.
- If adding a new level would only repeat adjacent behavior with vague adverbs, do not
  add it.

Quality requirements:

- Each score level must describe specific, observable behavior.
- Adjacent levels must be mutually exclusive and clinically distinguishable.
- A student's performance should clearly fit one score level, not multiple.
- New levels should represent qualitative competency differences, not arbitrary quantity
  alone.
- Quantity can be useful only when clinically meaningful, such as named counts of
  landmarks, required findings, or repeated communication breakdowns.
- Replace ambiguous language such as `adequate`, `appropriate`, `good`, or
  `area in question` unless it is paired with concrete behavior.
- Prefer active descriptions over passive descriptions.
- Maintain consistent language and structure across score levels.
- Criteria must align with the assessment mode: visible behavior for `video`, spoken
  content for `audio`, written evidence for `note`.
- Consider both technical execution and professional behavior or communication when
  relevant.

## Fill Missing Fields

Purpose: generate missing `Purpose`, `Technique`, or both.
Use this for completeness of existing rubric rows, not for broad rubric review.

Use this subworkflow when the user asks to:

- Fill missing `Purpose`.
- Fill missing `Technique`.
- Add Purpose and Technique fields.
- Complete rubric metadata for existing rows.

Field restrictions:

- For Purpose-only: `field` must be `Purpose`; `sub` must be `null`.
- For Technique-only: `field` must be `Technique`; `sub` must be `null`.
- For both: create separate suggestions for `Purpose` and `Technique`.
- `current_value` must be `""` because the field is missing or empty.
- Do not modify score anchors in this subworkflow unless the user also asks for
  technique expansion or scoring alignment.

Purpose guidance:

- Explain why the item matters and what competency is being evaluated.
- Clarify the educational objective behind the assessment.
- Identify the specific clinical competency being measured.
- Connect the skill to clinical reasoning, patient care, real-world practice,
  professional standards, or broader learning outcomes.
- Use concise professional language, usually one or two sentences.
- Avoid repeating the `QuestionName` without adding assessment rationale.
- Prefer action-oriented language such as `Evaluates the student's ability to` when that
  matches local style.

Technique guidance:

- Provide examples of observable actions, exact phrases, physical actions, or
  documentation evidence.
- Align directly with existing scoring logic.
- Include acceptable variations when they improve fairness or rater reliability.
- Use concrete language that assessors can apply consistently.
- For note-mode items, describe written documentation evidence rather than physical exam
  technique.
- Keep Technique practical; do not turn it into an exhaustive clinical textbook.

All missing `Purpose` and `Technique` fields are high priority because they affect
assessment completeness.

`AdditionalContext` guidance:

- The app enhancement flow focuses on `Purpose` and `Technique`.
- Add or fill `AdditionalContext` when a case/role transformation or template
  application needs evaluator constraints, accepted alternatives, uncertainty, safety
  notes, or case-specific guidance.

## Expand Techniques

Purpose: enrich existing `Technique` descriptions and optionally update scoring logic
when expanded examples expose scoring gaps.

Use this subworkflow when the user asks to:

- Expand Technique examples.
- Add observable examples.
- Make Technique clearer for raters.
- Add acceptable variations or evaluator cues.
- Align scoring with clarified Technique examples.

Allowed fields:

- `Technique`
- `ScoringLogic`

Field restrictions:

- Technique suggestions use `field: "Technique"` and `sub: null`.
- Scoring suggestions use `field: "ScoringLogic"` and `sub: "ScoreN"`.
- If `field` is `ScoringLogic`, `sub` is required.
- Do not change `QuestionName`, `Purpose`, `Mode`, `Category`, or `AdditionalContext` in
  this subworkflow.

Technique expansion rules:

- Expand only when examples genuinely improve assessment clarity.
- Add examples where helpful; not every item needs the same number of examples.
- Include exact phrases, physical actions, documentation evidence, acceptable
  variations, or evaluator cues.
- Integrate examples naturally using phrases like `such as`, `for example`, `including`,
  or `alternatively`.
- Use parentheses for exact phrase examples when useful.
- Keep examples aligned with `QuestionName`, `Purpose`, and score anchors.
- Match example density to task complexity.
- Use clear, professional medical language.
- Do not turn Technique into a textbook or comprehensive procedure guide.

Scoring alignment rules:

- After expanding Technique, check whether scoring logic can still differentiate the
  clarified behaviors.
- Suggest scoring changes only when the expanded Technique reveals a concrete ambiguity,
  gap, overlap, contradiction, or mode mismatch.
- Create separate suggestions for each affected score level.
- Do not modify scoring merely because the Technique wording changed.

## Template Or Style Application

Purpose: apply style and formatting from a reference rubric to a target rubric while
preserving the target rubric's clinical content.

Use this subworkflow when the user asks to:

- Apply this rubric as a template.
- Restyle a target rubric to match a reference rubric.
- Match institutional rubric style.
- Standardize naming, phrasing, score-anchor style, field density, tone, or formatting
  across rubrics.

Core task:

Analyze the reference rubric's style patterns and suggest changes that make the target
rubric match that style while keeping all target clinical content intact.

Reference style patterns to analyze:

1. `QuestionName` patterns:
   - Naming convention, such as `Knee Inspection`, `Inspect knee`, or
     `Inspection of knee`.
   - Structure, such as verb-first or noun-first.
   - Whether body part, symptom, documentation section, or task detail is explicit.
   - Detail level, from specific task names to broad domain names.
   - Capitalization, such as title case, sentence case, or uppercase.
2. `ScoringLogic` style:
   - Verbose versus concise score descriptions.
   - Clinical/formal versus conversational tone.
   - Exact actions versus general criteria.
   - Complete sentences versus fragments.
   - Verb tense, such as present tense, past tense, or infinitive.
   - Score progression style and number of score levels.
3. `Technique` field format:
   - Step-by-step versus summary.
   - Technical medical terminology versus plain language.
   - Numbered, bulleted, comma-separated, or paragraph style.
   - Exhaustive steps versus key assessor cues.
4. `Purpose` field style:
   - Single sentence, multiple sentences, or phrase.
   - Clinical reasoning versus procedural justification.
   - Structure such as `To diagnose`, `Evaluates`, or `For assessing`.
5. `AdditionalContext` field:
   - Clinical pearls, warnings, anatomical notes, accepted alternatives, or evaluator
     constraints.
   - Instructional versus informational tone.
6. Language patterns:
   - Active versus passive voice.
   - Action verbs such as observe, inspect, palpate, document, ask, counsel, or explain.
   - Punctuation and list style.
   - Consistent terminology, such as patient, examinee, learner, student, or client.

Change:

- Formatting and style to match the reference.
- Wording patterns and tone.
- Terminology choices.
- Punctuation and capitalization.
- Sentence structure and verb tense.
- Level of detail and field density.
- Score progression style.
- Missing score levels when the reference has more levels.
- Empty or minimal `Technique`, `Purpose`, or `AdditionalContext` fields using the
  reference pattern adapted to target content.

Preserve:

- Target clinical procedures and objectives.
- Number of questions.
- Medical meaning.
- Assessment target.
- Target case facts.
- `Mode` exactly as written in the target rubric.

Analysis process:

1. Identify 3-5 key style patterns in the reference rubric.
2. Note how `QuestionName` values are structured.
3. Count how many score levels the reference uses.
4. Note how score levels progress.
5. Note language patterns, tense, voice, terminology, punctuation, and field density.
6. Check which fields are filled versus empty in the reference.
7. For each target field, determine how the reference would phrase the target's content.
8. Suggest complete cell-level restyling changes.
   Do not split capitalization, punctuation, and wording into separate suggestions for
   the same cell.

Content adaptation rules:

- For missing score levels, add them using the reference structure but the target's
  clinical context.
- For empty fields, fill them using the reference pattern adapted to the target content.
- For minimal fields, expand to the reference's level of completeness.
- Do not copy clinical content from the reference into the target.
- Apply the pattern, not the reference case facts.
- Return `[]` if the target already matches the reference style closely.

Template examples:

### QuestionName Styling

Reference pattern:

```yaml
QuestionName: "Inspect knee for deformities, swelling, and erythema"
```

Pattern: verb-first, specific body part, lists observable signs.

Target current:

```yaml
QuestionName: "Shoulder examination - inspection"
```

Suggested change:

```yaml
QuestionName: "Inspect shoulder for deformities, swelling, and erythema"
```

### ScoringLogic: Adding Missing Score Levels

Reference pattern:

```yaml
Score1: "Student identifies all key anatomical landmarks (medial joint line, lateral joint line, tibial tuberosity, patella)"
Score2: "Student identifies 2-3 anatomical landmarks"
Score3: "Student identifies 1-2 anatomical landmarks"
Score4: "Student identifies 0 anatomical landmarks or fails to demonstrate proper technique"
```

Target current:

```yaml
Score1: "Palpated bony landmarks"
```

Suggested changes:

```yaml
Score1: "Student palpates all major bony prominences of the shoulder (acromion, clavicle, coracoid process, spine of scapula)"
Score2: "Student palpates 2-3 major bony prominences"
Score3: "Student palpates 1 major bony prominence"
Score4: "Student identifies 0 bony prominences or fails to demonstrate proper palpation technique"
```

Each score anchor must be a separate JSON suggestion.

### Filling Empty Technique

Reference pattern:

```yaml
Technique: "Use open-ended question (e.g., 'What brings you in today?'). Allow patient to speak without interruption. Avoid leading questions."
```

Target current:

```yaml
QuestionName: "Ask about pain onset"
Technique: ""
```

Suggested change:

```yaml
Technique: "Use an open-ended question (e.g., 'When did your pain start?'). Allow the patient to describe the timeline. Avoid suggesting specific timeframes."
```

### Standardizing QuestionName Conventions

Reference pattern:

```yaml
QuestionName: "Documentation of Onset"
QuestionName: "Documentation of Duration"
QuestionName: "Documentation of Character"
```

Target current:

```yaml
QuestionName: "HPI - Onset"
QuestionName: "Duration"
QuestionName: "Character of pain"
```

Suggested changes:

```yaml
QuestionName: "Documentation of Onset"
QuestionName: "Documentation of Duration"
QuestionName: "Documentation of Character"
```

Validation checks:

- Clinical content is preserved.
- Style matches the reference patterns.
- Number of questions is unchanged.
- Score levels match the reference count when that is the requested style rule.
- Empty fields are filled using reference pattern plus target context.
- Medical accuracy is maintained.
- Each suggestion fully restyles one cell.
- `Mode` is unchanged.

## Priority Guidance

Use `critical` when a change is required to avoid unsafe, invalid, or seriously
misleading scoring after the transformation.

Use `high` when:

- A missing `Purpose` or `Technique` affects assessment completeness.
- A case/role transformation changes the validity of an item.
- A scoring anchor is unobservable, overlapping, or materially unfair.
- A core template pattern such as `QuestionName` format or score progression must change
  for consistency.

Use `medium` when:

- Wording, examples, or score criteria would improve reliability but the current item
  remains usable.
- Template application changes terminology, tone, field density, or phrasing.

Use `low` for minor punctuation, capitalization, or small style adjustments that do not
materially affect validity or reliability.

## Sibling Skill Boundaries

Use `osce-rubric-review` before this skill for broad first-pass audits, clarifying
questions, and discovery of rubric problems.

Use `content-validation` before this skill when a proposed transformation may change
clinical facts, learner expectations, fairness, safety, severity, or validity, or when
multiple interpretations are disputed.

Use `rubric-import` before this skill when the source material still needs to be
converted into Rubric Maker YAML or JSON.

Use `post-encounter-note-rubric` instead of this skill when creating a new note-mode
rubric from case materials.
Use this skill later to adapt, restyle, or expand that existing rubric.

Use `grading-dry-run` instead of this skill to produce a provisional grade sheet from a
rubric and sample artifact.
Use `evaluate-dry-run` to identify rubric changes from that trial grade sheet.
Use this skill only when the rubric content itself needs changes or accepted suggestions
need to be applied.

Virtual patient case design belongs outside this rubric-focused plugin.
Use this skill only when an existing rubric must be aligned to that case.

## Do Not Port From The App

Do not reproduce app-specific implementation details unless the user asks for app
development:

- Flask route names.
- Database tables and persistence state.
- Session keys, polling states, frontend buttons, or spinners.
- Specific model defaults or model branding.
- Storage paths, version directories, or async execution mechanics.

Preserve the workflow logic, contracts, field restrictions, and decision points.

## Empty Result

Return `[]` when the requested transform, enhancement, or style application does not
require actionable suggestions.
Do not invent changes just to produce output.
