---
name: practice-simulator-case
description: Design live OSCE patient simulation cases for practice simulator workflows, including patient persona, station instructions, hidden case details, expected learner tasks, voice/session behavior, and optional grading alignment. Use when an agent needs to create or refine a virtual patient case for history taking, counseling, clinical reasoning, or communication practice.
---

# Practice Simulator Case

## Workflow

1. Identify learner level, station duration, clinical setting, presenting concern, and simulation mode.
2. Create student-facing instructions that reveal only what a learner should know before the encounter.
3. Create hidden patient-actor details: demographics, affect, opening line, history, symptoms, relevant negatives, PMH, medications, allergies, social context, and emotional cues.
4. Define conversation behavior: how forthcoming the patient is, what requires follow-up questions, and what should never be volunteered.
5. Add examiner notes and optional rubric alignment.
6. Keep test-mode cases fair by separating student-facing and hidden information.

## Output

Use headings:

- `Case Overview`
- `Student Instructions`
- `Patient Persona`
- `Opening Statement`
- `History Details`
- `Relevant Positives And Negatives`
- `Behavior Rules`
- `Expected Learner Tasks`
- `Optional Rubric Alignment`

## References

- Load `references/rubrics-app-schema.md` when aligning cases to rubric or grading fields.
- Load `references/practice-simulator-pattern.md` for app source behavior and case design rules.
