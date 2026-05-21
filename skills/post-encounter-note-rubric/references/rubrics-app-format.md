# Rubrics App Format

Use this schema for rubrics generated for the `/rubrics` app.

```yaml
rubric:
  - Category: "Clinical Reasoning"
    QuestionName: "Documents a prioritized differential diagnosis"
    ScoringLogic:
      Score1: "No differential diagnosis is documented, or listed diagnoses are unrelated to the case."
      Score2: "Documents a limited differential with major omissions or weak prioritization."
      Score3: "Documents a clinically plausible differential with appropriate prioritization and minor omissions."
      Score4: "Documents a comprehensive, prioritized differential that reflects the key case findings and dangerous alternatives."
    Mode: "note"
    Technique: "Look for explicit diagnoses in the written note, ordered or justified using case findings."
    Purpose: "Evaluates whether the learner can synthesize case information into clinically appropriate diagnostic reasoning."
    AdditionalContext: ""
```

## Fields

- `Category`: Section or grouping for the item.
- `QuestionName`: The specific task being assessed.
- `ScoringLogic`: Ordered score anchors named `Score1`, `Score2`, etc. `Score1` is the lowest performance level.
- `Mode`: Use `video`, `audio`, or `note`. For post-encounter-note rubrics, use `note`.
- `Technique`: For note grading, describe the expected documentation evidence.
- `Purpose`: Explain why the item matters clinically or educationally.
- `AdditionalContext`: Add case-specific constraints, uncertainty, or evaluator guidance. Use an empty string if none.

## Constraints

- Keep each item single-purpose.
- Keep score anchors mutually distinguishable.
- Do not include properties outside the schema.
- Use YAML by default unless JSON is requested.
