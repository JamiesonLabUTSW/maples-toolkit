---
name: grading-dry-run
description: Produce provisional OSCE grade sheets from a Rubric Maker rubric and text-based student artifact. Use when an agent needs to dry-run scoring against a draft rubric using post-encounter-note text, transcript text, or a timestamped observation log, with evidence, rationale, confidence, subtotals, totals, and deterministic grade-sheet validation. Do not use for generating student artifacts, revising rubrics, adjudicating clinical validity, or inspecting raw audio/video.
---

# Grading Dry Run

## Use For

- Provisionally grading an example student artifact against an existing rubric.
- Testing whether rubric items are scoreable from post-encounter-note text, transcript text, or timestamped observation logs.
- Producing a structured grade sheet with item scores, evidence, rationale, confidence, subtotals, totals, and immediate grading-friction notes.
- Checking the grade sheet mechanically with `scripts/validate_grade_sheet.py`.

## Do Not Use For

- Generating synthetic notes, transcripts, or transcript-derived observation logs; use `generate-student-artifact`.
- Rewriting, transforming, or applying rubric edits; use `osce-rubric-transform`.
- Broad rubric critique from a dry run; use `evaluate-dry-run`.
- Clinical-validity adjudication for disputed rubric concerns; use `content-validation`.
- Importing source rubrics; use `rubric-import`.
- Inspecting raw audio or video. Ask for a transcript, note, or timestamped observation log first.

## Workflow

1. Load `references/rubric-schema.md` and `references/grade-sheet-contract.md`.
2. Load `references/evidence-rules.md` for artifact-specific evidence boundaries.
3. Load `references/scoring-rules.md` for scoring and total rules.
4. Score each rubric item only from evidence present in the supplied artifact and supported by the item `mode`.
5. Quote exact note or transcript text for scored items, or cite the supplied timestamped observation evidence.
6. Mark unsupported items as unscorable instead of inferring across modalities or missing evidence.
7. Produce a grade sheet matching `references/grade-sheet-contract.md`.
8. Run `python3 scripts/validate_grade_sheet.py <grade-sheet-file>`.
9. Fix mechanical validation failures before delivering the final grade sheet.

## Output Rules

- Include one `items` row per rubric item.
- Each scored row must include `score`, `max_score`, `evidence`, `rationale`, and `confidence`.
- Each unscorable row must include `unscorable: true`, `max_score`, and `unscorable_reason`.
- If an item has `mode`, only score it from a compatible text artifact: `note` mode from note text, `audio` mode from transcript text, and `video` mode from transcript text that explicitly documents observations or from observation-log text.
- Raw audio and video are never inspected. Unsupported or incompatible item modes must be marked unscorable instead of scored.
- Include `subtotals`, `total_score`, `max_score`, and `percentage` when the user requests a full grade sheet.
- Keep rubric-change ideas separate as `grading_friction_notes`; do not rewrite the rubric in this skill.

## References

- `references/rubric-schema.md`: rubric field schema and score-anchor conventions.
- `references/grade-sheet-contract.md`: required grade-sheet shape and examples.
- `references/evidence-rules.md`: note, transcript, and observation-log evidence rules.
- `references/scoring-rules.md`: score selection, unscorable handling, and total math.
