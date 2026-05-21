# Multimodal Grading

## Modes

- `video`: grade visible actions. Response should include `start_time`, `end_time`, `rationale`, and `score`.
- `audio`: grade spoken statements. Response should include extracted statements with timestamps, rationale, count, and score.
- `note`: grade written post-encounter-note content. Response should include exact `evidence`, `rationale`, `answer` (`Supports`, `Refutes`, or `Neutral`), and score when applicable.

## Prompt Assembly

For each item, include:

- Item key or stable row label.
- Question text.
- Purpose.
- Technique.
- Additional context.
- Ordered scoring rubric.

## Evidence Rules

- Video: do not infer what is not shown.
- Audio: do not infer what is not stated.
- Note: do not infer what is not documented.
- Always connect score to the scoring criteria, not general impression.
