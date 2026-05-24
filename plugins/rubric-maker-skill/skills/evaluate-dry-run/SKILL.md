---
name: evaluate-dry-run
description: Analyze an OSCE case, draft rubric, example student artifact, and validated trial grade sheet to identify dry-run friction and produce prioritized rubric-improvement suggestions. Use when dry-run evidence shows grading ambiguity, evidence mismatch, weak scoring discrimination, missing case-critical expectations, or safety and fairness concerns.
---
# Evaluate Dry Run

## Use For

- Analyzing a completed dry run that includes case materials, a draft rubric, a student
  artifact, and a validated trial grade sheet.
- Finding rubric issues revealed by provisional grading rather than by rubric text
  alone.
- Producing prioritized rubric-improvement suggestions plus narrative dry-run findings.
- Explaining why grading friction occurred and how the rubric could better support
  reliable assessment.

## Do Not Use For

- Producing the trial grade sheet; use `grading-dry-run`.
- Generating synthetic student artifacts; use `generate-student-artifact`.
- Applying edits directly to the rubric; use `osce-rubric-transform`.
- Adjudicating disputed clinical fixes or high-stakes educator disagreements; use
  `content-validation`.
- Broad rubric review without dry-run evidence; use `osce-rubric-review`.

## Sibling Sequence

Use `generate-student-artifact` when a realistic learner output is needed, then
`grading-dry-run` to produce and validate the trial grade sheet.
Use `evaluate-dry-run` after that validated grade sheet exists to identify
rubric-improvement suggestions from dry-run friction.
Escalate selected findings to `content-validation` when clinical validity, fairness,
safety, severity, or consensus is disputed.
Use `osce-rubric-transform` when the user wants accepted changes rewritten or applied as
rubric suggestions.

## Inputs

Expected inputs are case materials, rubric, student artifact, validated trial grade
sheet, and optional educator goals.
If the grade sheet is supplied as a file, validate it with
`scripts/validate_grade_sheet.py <grade-sheet-file>` before analysis.
If the grade sheet is pasted or otherwise cannot be validated mechanically, ask for a
file when deterministic validation is needed, or clearly mark any findings that depend
on uncertain grading output.

## Workflow

1. Load `references/grade-sheet-contract.md` to interpret grade-sheet fields, evidence
   shape, unscorable rows, confidence, totals, and grading-friction notes.
2. Validate a saved grade sheet with
   `scripts/validate_grade_sheet.py <grade-sheet-file>` before using it as evidence.
3. Align the case priorities, expected learner tasks, rubric items, artifact evidence,
   and provisional scores.
4. Identify dry-run failure patterns: ambiguous anchors, unsupported items, missing
   expectations, evidence mismatch, redundancy, weak score discrimination, poor
   weighting, unsafe behavior, or fairness impact.
5. Separate artifact performance problems from rubric problems.
   Suggest rubric-improvement changes only when the dry run shows the rubric is unclear,
   incomplete, misweighted, unobservable, or unreliable.
6. Prioritize findings by assessment impact, safety/fairness risk, and likelihood that
   the issue will recur.
7. Return narrative findings first, then structured suggestions using exact current
   rubric values.
8. When a suggested fix is clinically uncertain or policy-sensitive, mark it for
   `content-validation` instead of overclaiming.

## Output Guidance

- Use `critical`, `high`, `medium`, or `low` priority.
- Preserve exact `current_value` text from the source rubric.
- Use locations like `3:Technique` or `4:ScoringLogic.Score2`.
- Prefer one comprehensive suggestion per affected rubric cell.
- Return `[]` for `suggestions` when the dry run reveals no actionable
  rubric-improvement changes.
- When deterministic validation is needed, pass the source rubric to
  `scripts/validate_dry_run_suggestions.py --rubric <rubric-file> <suggestions-file>` so
  the validator can enforce row, field, subfield, and exact `current_value` matches.
  Without `--rubric`, the script performs shape-only validation plus internal location
  consistency checks.

## References

- Load `references/rubric-schema.md` for the shared rubric and suggestion fields.
- Load `references/grade-sheet-contract.md` before interpreting a trial grade sheet.
- Load `references/dry-run-failure-patterns.md` when classifying dry-run findings.
- Load `references/suggestion-contract.md` before producing or validating structured
  suggestions.
- Use `scripts/validate_grade_sheet.py` to check grade-sheet JSON or YAML before
  analysis.
- Use `scripts/validate_dry_run_suggestions.py` to check suggestion JSON or YAML.
  Include `--rubric` whenever exact source-value enforcement is required.
