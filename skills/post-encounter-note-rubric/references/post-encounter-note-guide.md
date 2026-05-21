# Post-Encounter-Note Rubric Guide

## Source Synthesis

Extract these signals from case files:

- Station task and learner level.
- Presenting concern and expected key history.
- Pertinent positives and negatives.
- Exam findings, labs, imaging, or provided data.
- Dangerous diagnoses and safety issues.
- Expected assessment, differential, plan, follow-up, and counseling.
- Any sample note, checklist, answer key, or scoring guide.

## Recommended Categories

- History documentation: chief concern, HPI chronology, relevant ROS, risk factors, PMH, medications, allergies.
- Objective data: relevant exam findings, vitals, labs, imaging, interpretation of provided data.
- Clinical reasoning: problem representation, prioritized differential, justification, identification of red flags.
- Assessment and plan: diagnosis, workup, treatment, patient education, follow-up, return precautions.
- Documentation quality: organization, concision, medical terminology, internally consistent note.

## Item Writing Patterns

Use a specific, evidence-based `QuestionName`:

- Good: `Documents exertional chest pain features and associated red flags`
- Good: `Prioritizes myocardial infarction and pulmonary embolism in the differential when supported by case findings`
- Weak: `Writes a good HPI`
- Weak: `Shows clinical judgment`

Use `Technique` to name evidence expected in the note:

- `Look for documentation of onset, duration, provoking factors, associated symptoms, and pertinent negatives relevant to the presenting concern.`
- `Look for an assessment statement that links the leading diagnosis to the patient's documented findings.`

Use `Purpose` to state why the competency matters:

- `Evaluates whether the learner can distinguish routine documentation from clinically relevant synthesis needed for safe patient care.`

## Reusable Scoring Anchor Pattern

Use this pattern when the source does not prescribe a scoring scale:

- `Score1`: absent, unrelated, unsafe, or not documented.
- `Score2`: partially documented but missing major required elements, poorly prioritized, or weakly connected to case facts.
- `Score3`: adequately documented with the core required elements and only minor omissions or clarity issues.
- `Score4`: complete, prioritized, clinically accurate, and explicitly supported by relevant case findings.

For simpler rubrics, collapse to 3 levels by combining partial and adequate into a middle anchor. For advanced learners, add a fifth level only when there is a meaningful distinction between complete and exemplary synthesis.

## Safety-Critical Design

Create explicit items for safety issues when the case supports them:

- Red flags requiring urgent escalation.
- Medication allergies, contraindications, pregnancy, anticoagulation, immunosuppression, or other treatment risks.
- Follow-up timing and return precautions.
- Dangerous diagnoses that must appear in the differential.

## Final Self-Check

- Every item is gradable from the written note alone.
- Every item uses `Mode: note`.
- The rubric covers both completeness and synthesis.
- No item requires hidden case knowledge unavailable to the grader.
- The scoring anchors are ordered from lowest to highest.

## Worked Example

Example case signal: adult patient with acute chest pain; expected note should document key HPI features, include dangerous diagnoses, and propose an initial plan with safety-netting.

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
