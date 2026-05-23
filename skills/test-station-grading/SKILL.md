---
name: test-station-grading
description: "Prepare OSCE rubrics and grading instructions for multimodal test-station evidence: video, audio, and post-encounter-note text. Use when an agent needs to split rubric items by mode, design evidence-based grading prompts, or make rubrics compatible with the /rubrics test station grading workflow."
---

# Test Station Grading

## Workflow

1. Identify the evidence type: `video`, `audio`, `note`, or mixed.
2. Assign each rubric item a compatible `Mode`. Use `note` for written post-encounter-note evidence, `audio` for spoken communication/transcript evidence, and `video` for visible actions.
3. Ensure each item can be scored from the selected evidence alone.
4. For grading prompt design, include item key, question text, `Purpose`, `Technique`, `AdditionalContext`, and ordered scoring criteria.
5. Require evidence in the grading output: timestamps for video/audio, exact text evidence for note grading, and concise rationale for every score.

## Mode Rules

- `video`: visible behavior only; use start/end timestamps or `Not observed`.
- `audio`: verbal content only; use exact statements and timestamps.
- `note`: written documentation only; use exact note evidence or `Not found`.

## References

- Load `references/rubrics-app-schema.md` for the shared schema, mode semantics, and structured suggestion conventions.
- Load `references/multimodal-grading.md` for response schemas and prompt patterns.
- Load `references/rubrics-app-source-map.md` for the embedded grading prompts in `/rubrics`.
