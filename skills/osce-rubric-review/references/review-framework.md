# OSCE Rubric Review Framework

Use this framework for review and clarifying questions.

## Six Pillars

- Alignment: The rubric matches the station task, case facts, learner level, and clinical objective.
- Safety: Critical omissions, dangerous diagnoses, contraindications, escalation, follow-up, and return precautions are covered.
- Observability: Criteria can be evaluated from the intended mode: video, audio, or note.
- Objectivity: Score anchors are concrete and distinguishable.
- Feasibility: Item count and expected performance fit station time and evaluator workload.
- Reliability: Items are not double-barrel, inconsistent, overlapping, or dependent on hidden assumptions.

## Clarifying Questions

Generate 2-4 focused questions when context would materially change the review. Use concrete options and include "Leave as currently written" when appropriate.

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
