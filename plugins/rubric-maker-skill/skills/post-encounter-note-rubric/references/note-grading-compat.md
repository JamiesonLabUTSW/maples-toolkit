# Rubric Maker App Note-Grading Compatibility

## Contents

- Purpose
- Upstream mental model
- Rubric item contract
- Field-by-field authoring implications
- Prompt behavior for note grading
- Scoring and max-rating behavior
- Section grouping strategy
- Evidence discipline
- Compatibility pitfalls
- Final compatibility check

## Purpose

Use this reference when drafting post-encounter-note rubrics that will be loaded into Rubric Maker grading workflows. The skill should not merely produce clinically reasonable rubric rows. It should produce rows that survive import, enrichment, prompt-building, section grouping, scoring, and evidence-display behavior.

The compatible output is still the standard Rubric Maker YAML shape:

```yaml
rubric:
  - Category: "Clinical Reasoning"
    QuestionName: "Documents a prioritized differential diagnosis with dangerous alternatives"
    ScoringLogic:
      Score1: "No differential diagnosis is documented, or listed diagnoses are unrelated to the case."
      Score2: "Documents a limited differential with major omissions or weak prioritization."
      Score3: "Documents a clinically plausible prioritized differential with only minor omissions."
      Score4: "Documents a comprehensive prioritized differential that includes dangerous alternatives and case-based justification."
    Mode: "note"
    Technique: "Look for explicitly documented diagnoses, prioritization, and links to written symptoms, risk factors, exam findings, or test results."
    Purpose: "Evaluates whether the learner can synthesize the written note into clinically appropriate diagnostic reasoning."
    AdditionalContext: "Dangerous alternatives should come from the case materials or standard expectations for this presentation."
```

## Upstream Mental Model

Rubric Maker grading workflows treat rubric rows as evidence-specific grading tasks. For note-mode rows, the evidence source is the student's written post-encounter note, not the SP script, video, transcript, examiner memory, or hidden case key.

The grading service enriches and reshapes rubric rows before it calls the grading model:

- `QuestionName` becomes `QuestionText` in the grading prompt.
- `Category` becomes `Section` when no explicit section is present.
- `ScoringLogic.Score1`, `Score2`, and so on become numbered response criteria.
- The highest present score anchor becomes `MaxRating`.
- `Mode` and `Section` determine prompt grouping.
- `Technique`, `Purpose`, and `AdditionalContext` are copied into the grading prompt for each item.
- The app creates `CaseID`, `ItemNum`, and `ItemKey`; the skill should not invent these fields.

Authoring implication: write each row as a complete, self-contained grading task. The grading model sees rows grouped by mode and section, but each item must still carry enough detail to be scored from note text alone.

## Rubric Item Contract

Every generated item must include these fields:

- `Category`: Human-readable section grouping. For note grading, this becomes the app's section grouping if no explicit `Section` is present.
- `QuestionName`: The actual criterion the grader will score.
- `ScoringLogic`: Ordered anchors named `Score1`, `Score2`, etc., without gaps.
- `Mode`: Always `note` for this skill.
- `Technique`: Written-note evidence instructions.
- `Purpose`: Clinical or educational rationale.
- `AdditionalContext`: Case-specific constraints, acceptable alternatives, uncertainty, or grading cautions. Use an empty string when there is nothing to add.

Do not include system-generated fields such as `CaseID`, `ItemNum`, `ItemKey`, `QuestionText`, `Response1`, `MaxRating`, or `Section` unless the user specifically asks for an expanded grading-export shape. The YAML rubric should stay in the Rubric Maker schema.

## Field-by-Field Authoring Implications

### Category

Choose categories that make useful grading sections after normalization. Good note-mode category families include:

- `History Documentation`
- `Objective Data`
- `Clinical Reasoning`
- `Assessment And Plan`
- `Safety And Follow-Up`
- `Documentation Quality`

Keep categories stable and broad enough that a section prompt contains related items. Avoid overly narrow categories that create one-item sections unless the station genuinely has a standalone domain.

### QuestionName

Write the item as a specific written-note outcome, not as a learner behavior from the live encounter.

Good:

- `Documents onset, duration, triggers, associated symptoms, and pertinent negatives for the presenting concern`
- `Prioritizes the leading diagnosis and includes dangerous alternatives supported by the case`
- `Documents a case-appropriate management plan with follow-up timing and return precautions`

Weak:

- `Takes a good history`
- `Shows clinical judgment`
- `Asks about medications`

If the source material says the learner should ask about something, convert that expectation into what should appear in the note. For example, "asks about anticoagulant use" becomes "Documents anticoagulant use or explicitly notes its absence when relevant to management."

### ScoringLogic

Write anchors that can be assigned by reading the note. Each anchor should answer: "What text would I expect to find or not find?"

Use the lowest anchor for absent, unrelated, unsafe, or not documented performance. Use middle anchors for partial documentation, major omissions, weak prioritization, or limited case linkage. Use the highest anchor for complete, prioritized, clinically accurate documentation with case support.

Prefer four levels when the source does not specify a scale:

- `Score1`: absent, unrelated, unsafe, or not documented.
- `Score2`: partially documented with major omissions or weak linkage to the case.
- `Score3`: adequately documented with core elements and minor omissions.
- `Score4`: complete, prioritized, clinically accurate, and explicitly supported by case findings.

Use three levels for simple novice rubrics. Use five levels only when the distinction between complete and exemplary synthesis is meaningful and scorable from the note.

Avoid anchors that require hidden process knowledge:

- Bad: `Score4: Asked all required questions and correctly reassured the patient.`
- Good: `Score4: Documents the required pertinent positives and negatives and includes a clinically appropriate reassurance or counseling plan when supported by the case.`

### Mode

Always use:

```yaml
Mode: "note"
```

Do not use `video` or `audio` in this skill. When the user needs to test the draft rubric against a sample note or transcript, route to `grading-dry-run`. When the user needs a synthetic sample artifact first, route to `generate-student-artifact`.

### Technique

For note mode, `Technique` is not physical exam technique. It is the evidence-finding instruction the grading prompt will include for the row.

Use `Technique` to tell the grader where and how to look in the written note:

- `Look for explicit HPI documentation of onset, duration, location, quality, triggers, associated symptoms, and pertinent negatives.`
- `Look for a problem representation that combines patient demographics, time course, key symptoms, risk factors, and leading diagnostic concern.`
- `Look for a management plan that names diagnostic workup, treatment or disposition, follow-up timing, and return precautions.`

Technique should be concrete enough that "Not found" is a legitimate grading result. Avoid vague techniques such as `Assess quality of documentation`.

### Purpose

Use `Purpose` to explain why the row matters. This helps downstream graders apply anchors consistently when note wording varies.

Good purposes:

- `Evaluates whether the learner can transform collected history into clinically relevant written synthesis.`
- `Evaluates recognition of high-risk diagnoses that must not be omitted from post-encounter documentation.`
- `Evaluates whether the learner can translate assessment into a safe and actionable care plan.`

### AdditionalContext

Use `AdditionalContext` for case-specific rules that the grading model should know but that do not belong in the question or score anchors.

Good uses:

- Required differentials for the case.
- Acceptable synonyms or alternate diagnoses.
- Findings that should not be required because they were not supplied.
- Learner-level constraints.
- Cautions not to require unavailable labs, imaging, physical findings, or treatments.
- Uncertainty where the source materials are incomplete.

Examples:

- `Accept "ACS", "MI", or "acute coronary syndrome" as equivalent dangerous cardiac diagnoses if supported by the case.`
- `Do not penalize absence of imaging interpretation if no imaging result was provided in the case materials.`
- `If the sample note conflicts with the answer key, follow the answer key and note the conflict in assumptions.`

## Prompt Behavior for Note Grading

The upstream note-grading prompt asks the grading model to:

- Assess the student's written note in several key areas.
- Extract relevant note text for each item.
- Use the provided scoring criteria to determine the score.
- Provide a rationale for the score.
- State evidence as `Not found` when the note lacks relevant text.
- Avoid inferences or assumptions beyond what is directly stated in the note.
- Consider both the item description and scoring criteria.

The schema used by the app supports a response per item with:

- `evidence`: exact note text or `Not found`.
- `rationale`: explanation for the score.
- `answer`: one of `Supports`, `Refutes`, or `Neutral`.
- `score`: numeric score when available.

Authoring implication: rows should be framed so the grader can find supporting or missing evidence in the note. Do not ask the grader to decide whether the learner actually performed a behavior unless the note itself documents it.

## Scoring and Max-Rating Behavior

The app derives the maximum score from the highest `ScoreN` key. If a row has `Score1` through `Score4`, the max rating is 4. If a row has `Score1` through `Score5`, the max rating is 5.

Rules:

- Do not skip score numbers.
- Do not mix `Score0` with `Score1` unless the user explicitly provides a source scale requiring it; the plugin convention starts at `Score1`.
- Keep all rows in a rubric on the same score depth unless the source materials justify mixed depth.
- Make the highest score realistic for the learner level and case materials.
- Make the lowest score capture both absence and unsafe unrelated documentation when appropriate.

Because downstream percentages use numeric scores and max ratings, inconsistent score depth can change weighting. If one item has five levels and another has three, the five-level item contributes a larger max score unless the app or grader normalizes it elsewhere. Prefer a consistent scale across the rubric.

## Section Grouping Strategy

The app groups rows by `Mode` and `Category`/`Section`. For this skill, `Mode` is always `note`, so `Category` largely determines grading sections.

Use section groupings that help the note grader evaluate related evidence together:

- History items together.
- Objective data items together.
- Clinical reasoning items together.
- Assessment and plan items together.
- Safety/follow-up items together.
- Documentation quality items together.

Avoid putting unrelated items under the same category merely to reduce section count. Also avoid creating so many categories that the grader sees each row in isolation.

## Evidence Discipline

A strong note-mode item can be graded with three outcomes:

1. Clear support in the note.
2. Clear absence in the note.
3. Ambiguous or partial evidence that maps to a middle score.

When drafting, ask:

- What exact words, phrases, diagnoses, data, or plan elements would support this score?
- What omissions would lower the score?
- Is the item scorable without seeing the encounter video or transcript?
- Does the item require facts from the answer key that the student's note could not reasonably document?
- Does the item unfairly reward invented detail?

Do not reward documentation of facts that contradict the case. When a learner documents a clinically dangerous but unsupported statement, score according to the anchors and call out the mismatch in `AdditionalContext` if it is a known risk for the case.

## Compatibility Pitfalls

- Requests to grade a sample note or transcript: route to `grading-dry-run`.
- Requests to generate a sample note or transcript: route to `generate-student-artifact`.
- Physical exam technique in `Technique`: rewrite as note evidence, such as "Look for documented cardiac exam findings."
- Vague score anchors: replace "good", "adequate", or "complete" with specific note evidence.
- Hidden-case-only requirements: move constraints into `AdditionalContext` or omit the item.
- Missing `Mode`: do not rely on app auto-detection because fallback behavior may choose video.
- Missing `Purpose` or `Technique`: downstream prompts become weaker and graders have less context.
- Overstuffed items: split history completeness, differential reasoning, and plan safety into separate rows.
- Case facts invented by the skill: mark uncertainty instead of inventing facts.
- Inconsistent score depth: avoid accidental weighting differences.

## Final Compatibility Check

Before final output, verify:

- Every row has `Mode: note`.
- Every row has all seven plugin convention fields.
- `Category` can serve as a section name.
- `QuestionName` names a written-note outcome.
- `ScoringLogic` keys are ordered and gap-free.
- Score anchors are distinguishable from written note evidence.
- `Technique` tells the grader what exact note evidence to look for.
- `Purpose` explains the clinical or educational reason for the row.
- `AdditionalContext` captures case-specific constraints, acceptable alternatives, or uncertainty.
- No row requires video, audio, transcript, SP actor behavior, or hidden examiner knowledge.
- The rubric can be graded using exact evidence or `Not found`.
