# OpenAI Implementation Notes

Use official OpenAI docs as implementation references when turning this skill into an
API-backed generator.

## Responses API

The Responses API is the preferred high-level interface for model responses.
The docs describe it as supporting text and image inputs, text outputs, stateful
interactions, built-in tools such as file search and web search, and function calling.

Reference: `https://developers.openai.com/api/reference/responses/overview`

## Structured Outputs

Use Structured Outputs when the generator must return a predictable rubric object.
OpenAI docs state that Structured Outputs make model responses adhere to a supplied JSON
Schema and are preferable to JSON mode when schema adherence matters.

Reference: `https://developers.openai.com/api/docs/guides/structured-outputs`

## Prompting Pattern

For agentic or long-running work, OpenAI prompt guidance recommends explicit
role/workflow guidance, testing or validation, clean Markdown standards, planning,
preambles for major tool use, and progress tracking.

Reference: `https://developers.openai.com/api/docs/guides/prompt-engineering#coding`

## Practical API Shape

For a generator, use a schema equivalent to:

```json
{
  "type": "object",
  "required": ["rubric"],
  "properties": {
    "rubric": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["Category", "QuestionName", "ScoringLogic", "Mode", "Technique", "Purpose", "AdditionalContext"],
        "properties": {
          "Category": {"type": "string"},
          "QuestionName": {"type": "string"},
          "ScoringLogic": {
            "type": "object",
            "patternProperties": {
              "^Score[1-9][0-9]*$": {"type": "string"}
            },
            "additionalProperties": false
          },
          "Mode": {"type": "string", "enum": ["note"]},
          "Technique": {"type": "string"},
          "Purpose": {"type": "string"},
          "AdditionalContext": {"type": "string"}
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
```
