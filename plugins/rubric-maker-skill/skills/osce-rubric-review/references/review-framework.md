# OSCE Rubric Review Framework

Use this framework for review and clarifying questions.

## Contents

- [Six Pillars](#six-pillars)
- [Clarifying Questions](#clarifying-questions)
- [Station Type Heuristics](#station-type-heuristics)
- [Safety Kill-Step Checks](#safety-kill-step-checks)
- [Question Tone And Options](#question-tone-and-options)
- [Suggestion Shape](#suggestion-shape)

## Six Pillars

- Alignment: The rubric matches the station task, case facts, learner level, and clinical objective.
- Safety: Critical omissions, dangerous diagnoses, contraindications, escalation, follow-up, and return precautions are covered.
- Observability: Criteria can be evaluated from the intended mode: video, audio, or note.
- Objectivity: Score anchors are concrete and distinguishable.
- Feasibility: Item count and expected performance fit station time and evaluator workload.
- Reliability: Items are not double-barrel, inconsistent, overlapping, or dependent on hidden assumptions.

## Clarifying Questions

Generate 2-4 focused questions when context would materially change the review. Use concrete options and include "Leave as currently written" when appropriate.

Before asking questions:

1. Classify the station type silently so the review does not raise irrelevant flags.
2. If the educator supplied evaluation context or concerns, address those first and reference their wording.
3. Ask about clinical substance, assessment validity, safety, observability, feasibility, or reliability. Do not ask about formatting unless the rubric is illegible.

Use the same six pillar category labels in clarifying-question output: `ALIGNMENT`, `SAFETY`, `OBSERVABILITY`, `OBJECTIVITY`, `FEASIBILITY`, and `RELIABILITY`.

## Station Type Heuristics

- Procedural stations such as suturing, IV placement, catheterization, or injections: focus on sterility, sharps, consent, correct patient/site, and post-procedure monitoring.
- Prescribing or medication stations: focus on allergies, the medication rights, contraindications, dosing, route, timing, and documentation.
- Communication or history stations: focus on empathy cues, red flags, risk assessment, patient understanding, and closure.
- Physical exam stations: focus on draping, technique, patient comfort, visible actions, and whether findings must be spoken aloud.
- Acute or emergency stations: focus on recognition of severity, early escalation, ABCDE-style assessment, and immediate management.

## Safety Kill-Step Checks

Use restraint with safety-critical suggestions. Suggest at most 1-2 kill steps per station, or no more than about 10% of items, unless the user explicitly asks for a safety-critical checklist.

Check for these likely safety gaps:

- Any patient-facing station: hand hygiene, patient identification, consent when needed, allergy check when medications or contrast are involved, and safe follow-up or return precautions.
- Prescribing or medication station: allergies, patient/drug/dose/route/time/documentation checks, high-risk drug contraindications, and escalation for dangerous adverse effects.
- Procedural station: aseptic technique, correct patient and site, sharps disposal, consent, and post-procedure monitoring.
- Acute or emergency station: recognition of severity, call for help, initial stabilization, and appropriate early management.

Do not propose critical-fail items for minor politeness behaviors. Acknowledge program variation when asking about kill steps, for example whether the program wants a critical fail item, a standard weighted item, or no change.

## Question Tone And Options

Use a collegial "second pair of eyes" tone:

- Prefer "Would you like to..." and "In your context..."
- Acknowledge uncertainty with "If this is intentional, I can leave it as-is."
- Avoid "You should", "This is wrong", "This is unsafe", and "You forgot."

Question options should be concrete and mutually distinct:

- Include 2-3 options.
- Include "Leave as currently written" unless the existing rubric is structurally unusable.
- Use `include_other: false` for binary or narrow decisions and `include_other: true` when local policy, equipment, learner level, or station design could require another answer.

## Suggestion Shape

```json
{
  "location": "2:ScoringLogic.Score3",
  "current_value": "Existing exact text",
  "suggested_value": "Replacement text",
  "reasoning": "Why this improves alignment, safety, clarity, or reliability",
  "priority": "high",
  "row": 2,
  "field": "ScoringLogic",
  "sub": "Score3"
}
```
