# Test Station Grading Contracts

This reference captures prompt and response contracts for test-station grading.
Use it when preparing grading instructions or when checking whether generated
grading output matches the expected shape.

## Mode Detection

Grade by mode: `audio`, `video`, or `note`.

- Prefer the rubric item's explicit `mode`.
- If mode is absent, infer from file type:
  - video file -> `video`
  - audio file -> `audio`
  - text, PDF, or document -> `note`
  - unknown -> `video`
- Gemini handles audio/video natively. Other LLM paths require transcription or a
  transcript placeholder.

## Prompt Assembly

Each mode uses a system prompt that defines the rubric item format:

```text
<ItemKey>: <Question Text>
Purpose: <Purpose of this assessment item>
Technique: <How to evaluate this item>
Additional Context: <Any additional information>
Scoring Rubric:
  1: <Response for score 1>
  2: <Response for score 2>
```

Construct one user prompt per grading section. If the rubric includes a
non-default section, the prompt states which section is being graded before the
items.

For each item, include:

- `ItemKey` or a stable fallback such as `Item1`.
- `QuestionText` or `QuestionName`.
- `Technique`, when present.
- `Purpose` or `Indication`, when present.
- `AdditionalContext`, when present.
- Ordered scoring criteria.

Scoring criteria are read in this order:

- CSV-style `MaxRating` with `Response1`, `Response2`, etc.
- `ScoringLogic.Score1` through `ScoringLogic.Score6`.
- Legacy lowercase response keys as fallback.

Score numbering is ascending: `Score1` is the lowest score and higher score
numbers represent better performance.

## Mode-Specific Prompt Requirements

### Audio

The grader assesses communication based on a transcript or audio content.

Required behavior:

- List all relevant statements from the transcript.
- Include start and end timestamps for each statement.
- If no relevant statements exist, use `["None"]` for statements and `NA` for
  timestamps.
- Base scoring only on stated transcript/audio evidence.
- Explain both statement-level and overall scoring rationale.
- Use the supplied scoring criteria; do not score by general impression.

### Video

The grader assesses practical skills visible in the video.

Required behavior:

- Provide a detailed rationale for each score.
- If the action is observed, include start and end times.
- If not observed, use `Not observed`.
- Base scoring only on visible evidence.
- Consider both the item description and scoring criteria.

### Note

The grader assesses written post-encounter-note evidence.

Required behavior:

- Extract the exact relevant text from the note.
- If evidence is absent, use `Not found` and explain why.
- Do not infer beyond documented note content.
- Classify the evidence relationship as `Supports`, `Refutes`, or `Neutral`.
- Use the scoring criteria to assign a score when applicable.

## Response Schemas

All modes return a JSON object whose keys are item identifiers.

### Audio Response

```json
{
  "ItemKey": {
    "statements": [
      {
        "text": "Exact extracted statement",
        "start_time": "MM:SS",
        "end_time": "MM:SS",
        "rationale": "Why this statement demonstrates the item"
      }
    ],
    "total_count": 1,
    "rationale": "Overall rationale tied to scoring criteria",
    "score": 4
  }
}
```

Schema notes:

- `statements` is required and must be an array.
- Each statement requires `text`, `start_time`, `end_time`, and `rationale`.
- `statement` may be accepted as an input alias for `text` during validation.
- `total_count` is a non-negative integer.
- `score` is a non-negative number.

### Video Response

```json
{
  "ItemKey": {
    "start_time": "00:00",
    "end_time": "09:45",
    "rationale": "Rationale tied to visible action and criteria",
    "score": 3
  }
}
```

Schema notes:

- `start_time`, `end_time`, `rationale`, and `score` are required.
- Time fields may be timestamps or `Not observed`.
- `score` is a non-negative number.

### Note Response

```json
{
  "ItemKey": {
    "evidence": "Exact note text, or Not found",
    "rationale": "Rationale for relationship and score",
    "answer": "Supports",
    "score": 1
  }
}
```

Schema notes:

- `evidence`, `rationale`, and `answer` are required.
- `answer` must be one of `Supports`, `Refutes`, or `Neutral`.
- `score` is optional and must be a non-negative number when present.

## Runtime Boundary

This skill can prepare grading prompts and inspect grading JSON for contract
fit. It does not implement external runtime pieces such as media upload,
multi-angle video processing, background jobs, artifact storage, persisted
grading jobs, or result export.
