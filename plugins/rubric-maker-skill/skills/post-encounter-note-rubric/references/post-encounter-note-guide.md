# Post-Encounter-Note Rubric Guide

## Contents

- Source synthesis
- Recommended categories
- Item architecture
- Note-mode evidence rules
- Scoring anchor design
- Safety-critical design
- Learner-level calibration
- Case-material conflict handling
- Final self-check
- Worked example

## Source Synthesis

Extract these signals from case files:

- Station task and learner level.
- Presenting concern and expected key history.
- Pertinent positives and negatives.
- Exam findings, labs, imaging, or provided data.
- Dangerous diagnoses and safety issues.
- Expected assessment, differential, plan, follow-up, and counseling.
- Any sample note, checklist, answer key, or scoring guide.

When source materials contain both encounter expectations and note expectations,
translate only the written-output expectation into the rubric.
For example, "student should ask about allergies" becomes "documents medication
allergies or explicitly notes no known allergies when relevant."
Do not create a note item that requires observing the student ask the question unless
the note itself must document that fact.

Separate source facts into three buckets before drafting:

- Must-document facts: key positives, negatives, diagnoses, data, or plan elements that
  should appear in the note.
- Context facts: case details that help interpret documentation but should not become
  standalone rubric requirements.
- Uncertain facts: missing, conflicting, or inferred details that should either be
  omitted or placed in `AdditionalContext` as uncertainty.

## Recommended Categories

- History documentation: chief concern, HPI chronology, relevant ROS, risk factors, PMH,
  medications, allergies.
- Objective data: relevant exam findings, vitals, labs, imaging, interpretation of
  provided data.
- Clinical reasoning: problem representation, prioritized differential, justification,
  identification of red flags.
- Assessment and plan: diagnosis, workup, treatment, patient education, follow-up,
  return precautions.
- Documentation quality: organization, concision, medical terminology, internally
  consistent note.

Use categories intentionally because the upstream Rubric Maker app grading workflow
groups rows by `Mode` and section.
For this skill, all rows are `Mode: note`, so `Category` should be a useful section
name. Prefer a small set of stable categories over one-off labels.

## Item Architecture

Each item should have one written-note target:

1. The note evidence being assessed.
2. The scoring progression for that evidence.
3. The reason the evidence matters.
4. Any case-specific grading constraint.

Good item scopes:

- HPI completeness for the presenting concern.
- Pertinent positives and negatives for a dangerous diagnosis.
- Medication/allergy/risk documentation relevant to management.
- Objective data interpretation when data are provided.
- Problem representation.
- Prioritized differential diagnosis.
- Assessment linked to evidence.
- Diagnostic or therapeutic plan.
- Follow-up and return precautions.
- Organization and internal consistency.

Weak item scopes:

- Entire note quality plus differential plus plan in one row.
- Asking behavior that is not documented in the note.
- Generic professionalism or communication unless it is specifically documented in the
  note.

## Item Writing Patterns

Use a specific, evidence-based `QuestionName`:

- Good: `Documents exertional chest pain features and associated red flags`
- Good:
  `Prioritizes myocardial infarction and pulmonary embolism in the differential when supported by case findings`
- Weak: `Writes a good HPI`
- Weak: `Shows clinical judgment`

Use `Technique` to name evidence expected in the note:

- `Look for documentation of onset, duration, provoking factors, associated symptoms, and pertinent negatives relevant to the presenting concern.`
- `Look for an assessment statement that links the leading diagnosis to the patient's documented findings.`

Use `Purpose` to state why the competency matters:

- `Evaluates whether the learner can distinguish routine documentation from clinically relevant synthesis needed for safe patient care.`

Use `AdditionalContext` for app-facing grading guidance:

- Required case-specific diagnoses or acceptable alternatives.
- Facts that should not be required because they were not provided.
- Synonyms the grader should accept.
- Learner-level expectations.
- Uncertainty or conflict in source materials.

## Note-Mode Evidence Rules

Every row must be gradable from written note text alone.
A grader should be able to return exact evidence or `Not found` without seeing the
encounter.

Use note-mode wording:

- `Documents...`
- `Includes...`
- `States...`
- `Lists...`
- `Prioritizes...`
- `Links... to documented findings`
- `Provides written return precautions...`

Avoid live-encounter wording:

- `Asks...`
- `Performs...`
- `Explains verbally...`
- `Maintains eye contact...`
- `Uses appropriate tone...`

When a case expectation came from the SP script or checklist, convert it to a note
artifact. If the note does not need to contain that information, do not create a
note-mode item for it.

## Reusable Scoring Anchor Pattern

Use this pattern when the source does not prescribe a scoring scale:

- `Score1`: absent, unrelated, unsafe, or not documented.
- `Score2`: partially documented but missing major required elements, poorly
  prioritized, or weakly connected to case facts.
- `Score3`: adequately documented with the core required elements and only minor
  omissions or clarity issues.
- `Score4`: complete, prioritized, clinically accurate, and explicitly supported by
  relevant case findings.

For simpler rubrics, collapse to 3 levels by combining partial and adequate into a
middle anchor. For advanced learners, add a fifth level only when there is a meaningful
distinction between complete and exemplary synthesis.

## Scoring Anchor Design

Write score anchors so that each level is independently scorable:

- Identify the expected note elements.
- State what major omissions mean.
- Distinguish partial completeness from clinically meaningful synthesis.
- Make unsafe, unrelated, or contradictory documentation visible in low anchors.
- Avoid relying on evaluator intuition such as "good", "excellent", or "appropriate"
  without specifying why.

Anchor examples:

- Low:
  `No relevant assessment is documented, or the assessment is unrelated to the documented presentation.`
- Partial:
  `Documents a possible diagnosis but omits major supporting findings or dangerous alternatives.`
- Adequate:
  `Documents a plausible leading diagnosis with key supporting findings and minor omissions.`
- High:
  `Documents a prioritized assessment that links the leading diagnosis and dangerous alternatives to specific case findings.`

For note rubrics that will be used by the Rubric Maker app grading workflow, keep score
depth consistent across rows unless the source requires otherwise.
Mixed score depth changes maximum points per item.

## Safety-Critical Design

Create explicit items for safety issues when the case supports them:

- Red flags requiring urgent escalation.
- Medication allergies, contraindications, pregnancy, anticoagulation,
  immunosuppression, or other treatment risks.
- Follow-up timing and return precautions.
- Dangerous diagnoses that must appear in the differential.

Safety-critical note items should still be case-supported.
Do not add a return-precautions item when the case is a pure diagnostic documentation
station unless follow-up or safety-netting is expected.
Do add one when the case includes dangerous diagnoses, outpatient management, medication
risk, abnormal vital signs, or disposition decisions.

## Learner-Level Calibration

For novice learners, emphasize:

- Complete and organized documentation of core history.
- Recognition of essential positives and negatives.
- Basic assessment and safe initial plan.
- Clear note structure.

For advanced learners, emphasize:

- Prioritization over exhaustive lists.
- Problem representation.
- Justified differential diagnosis.
- Management plans linked to acuity and risk.
- Nuanced safety-netting and follow-up.

Do not use advanced anchors that require management decisions beyond the learner's
expected role.

## Case-Material Conflict Handling

When case files conflict:

- Prefer explicit answer keys over examples if the example note appears incomplete.
- Prefer station instructions over inferred clinical expectations.
- Mark unresolved conflicts in assumptions before the rubric and in `AdditionalContext`
  for affected rows.
- Do not silently merge contradictory facts.

When case materials are sparse:

- Draft a conservative rubric around the facts provided.
- Use generic note-quality and clinical-reasoning criteria only when they are
  appropriate to the station goal.
- Avoid adding disease-specific criteria without source support.
- State assumptions before the YAML.

## Final Self-Check

- Every item is gradable from the written note alone.
- Every item uses `Mode: note`.
- The rubric covers both completeness and synthesis.
- No item requires hidden case knowledge unavailable to the grader.
- The scoring anchors are ordered from lowest to highest.
- `Technique` is written-note evidence guidance, not physical exam technique.
- `AdditionalContext` contains uncertainty, acceptable alternatives, and case-specific
  constraints.
- Categories will work as note-grading sections in the Rubric Maker app.
- The rubric can be graded with exact note evidence or `Not found`.

## Worked Example

Example case signal: adult patient with acute chest pain; expected note should document
key HPI features, include dangerous diagnoses, and propose an initial plan with
safety-netting.

```yaml
rubric:
  - Category: "History Documentation"
    QuestionName: "Documents key chest pain characteristics and associated symptoms"
    ScoringLogic:
      Score1: "Does not document chest pain characteristics or associated symptoms, or documents unrelated information."
      Score2: "Documents some chest pain characteristics but omits major elements such as onset, duration, provoking factors, radiation, or associated symptoms."
      Score3: "Documents the core chest pain characteristics and relevant associated symptoms with only minor omissions."
      Score4: "Documents a complete, clinically focused HPI including onset, duration, location, quality, radiation, provoking or relieving factors, associated symptoms, and pertinent negatives relevant to dangerous causes of chest pain."
    Mode: "note"
    Technique: "Look for explicit written HPI details about the chest pain episode and associated symptoms or pertinent negatives."
    Purpose: "Evaluates whether the learner can capture clinically relevant symptom details needed to risk-stratify chest pain."
    AdditionalContext: "Adapt required HPI elements to the case materials if the presenting symptom is not chest pain."
  - Category: "Clinical Reasoning"
    QuestionName: "Includes a prioritized differential diagnosis with dangerous alternatives"
    ScoringLogic:
      Score1: "No differential diagnosis is documented, or listed diagnoses are unrelated to the presentation."
      Score2: "Documents a limited or poorly prioritized differential that omits major dangerous alternatives supported by the case."
      Score3: "Documents a plausible prioritized differential that includes the leading diagnosis and at least one dangerous alternative."
      Score4: "Documents a comprehensive, prioritized differential that includes the leading diagnosis, dangerous alternatives, and brief case-based justification."
    Mode: "note"
    Technique: "Look for listed diagnoses, prioritization, and explicit links to documented symptoms, risk factors, exam findings, or test results."
    Purpose: "Evaluates diagnostic synthesis and recognition of high-risk conditions that must not be missed."
    AdditionalContext: "Dangerous alternatives should come from the provided case materials or standard expectations for the station."
  - Category: "Assessment And Plan"
    QuestionName: "Documents an initial management plan and return precautions"
    ScoringLogic:
      Score1: "No management plan is documented, or the plan is unsafe for the documented presentation."
      Score2: "Documents a partial plan with major omissions in workup, treatment, follow-up, or safety-netting."
      Score3: "Documents an appropriate initial plan with workup and follow-up, with minor omissions or limited justification."
      Score4: "Documents a case-appropriate plan that includes initial workup, treatment or disposition, patient counseling, follow-up timing, and clear return precautions."
    Mode: "note"
    Technique: "Look for documented diagnostic workup, treatment or disposition, follow-up, and safety-net instructions in the written note."
    Purpose: "Evaluates whether the learner can translate assessment into a safe and actionable care plan."
    AdditionalContext: "Do not require treatments or tests not supported by the case file or learner level."
```
