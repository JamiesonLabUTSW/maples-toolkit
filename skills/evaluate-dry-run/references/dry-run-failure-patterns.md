# Dry-Run Failure Patterns

Use these patterns to classify friction found by comparing the case materials,
rubric, student artifact, and validated trial grade sheet.

## Pattern Catalog

### Ambiguous scoring anchors

The provisional grader could not distinguish adjacent score levels because
anchors use vague quantities, overlapping criteria, subjective terms, or mixed
dimensions.

Suggestion targets usually include `ScoringLogic.ScoreN`, `Technique`, or
`AdditionalContext`.

### Unobservable or unsupported item

The rubric asks for evidence that is unavailable in the artifact mode or absent
from the provided material. Do not penalize the student for evidence that the
grading setup cannot observe.

Suggestion targets usually include `Mode`, `Technique`, or `AdditionalContext`.

### Missing case-critical expectation

The case requires an important clinical, communication, safety, or
documentation behavior that is not represented in the rubric or is too weakly
represented.

Suggestion targets may include a new rubric item recommendation or a targeted
edit to `QuestionName`, `Technique`, `Purpose`, or `ScoringLogic`.

### Evidence and rubric mismatch

The artifact contains relevant evidence, but the rubric wording makes it hard
to decide whether the evidence satisfies the item. This includes mismatched
terminology, overly narrow acceptable examples, or missing acceptable
alternatives.

Suggestion targets usually include `Technique`, `AdditionalContext`, or a
specific score anchor.

### Redundant items

Multiple rubric items assess the same behavior in a way that may double count
or distort feedback.

Suggestion targets usually include `QuestionName`, `Purpose`, or a merge/split
recommendation in narrative findings.

### Weak discrimination

Most artifact evidence maps to multiple bands, or many bands differ only by
grammar rather than performance quality.

Suggestion targets usually include `ScoringLogic.ScoreN` anchors.

### Misweighted priority

The score impact of an item does not match case priorities, safety impact,
learner level, or educator goals.

Suggestion targets usually include `ScoringLogic`, `Purpose`, or
`AdditionalContext`. If the scoring system has weights outside the shared
rubric fields, describe the issue narratively.

### Unsafe or fairness-impacting behavior

The rubric could reward unsafe care, penalize reasonable alternatives, encode
biased assumptions, or create inconsistent grading for comparable learner work.

Use `critical` for direct patient-safety or material fairness risk. Route
clinically disputed fixes to `content-validation`.

## Severity Guide

- `critical`: Direct safety risk, material fairness risk, impossible grading, or contradiction that can invalidate scores.
- `high`: Likely score distortion, missing case-critical expectation, or major reliability problem.
- `medium`: Recurrent ambiguity, moderate mismatch, weak discrimination, or noncritical missing guidance.
- `low`: Minor clarity issue revealed by dry-run use with limited score impact.

## Analysis Rules

- Tie every finding to dry-run evidence: case expectation, artifact evidence,
  grade-sheet rationale, score spread, or missing evidence.
- Distinguish rubric defects from true student-performance gaps.
- Do not create structured edits for speculative improvements that the dry run
  did not support.
- When the best fix requires adding or deleting an entire item, describe it as
  a narrative finding unless the receiving workflow supports item-level changes.
