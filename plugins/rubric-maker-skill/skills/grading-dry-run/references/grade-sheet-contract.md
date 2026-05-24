# Grade Sheet Contract

Use this contract when producing or validating a provisional dry-run grade sheet.

## Accepted Top-Level Shape

The grade sheet may be either:

```yaml
grade_sheet:
  artifact_type: note
  evidence_sources:
    - note
  items: []
```

or the grade-sheet object directly:

```yaml
artifact_type: note
evidence_sources:
  - note
items: []
```

## Required Fields

- `artifact_type`: one of `note`, `transcript`, `observation_log`, or
  `transcript_plus_observations`.
- `items`: nonempty array with one row per rubric item.

Optional full-grade fields:

- `evidence_sources`: one or more of `note`, `transcript`, or `observation_log`.
  Required when `artifact_type` is `transcript_plus_observations`.
- `subtotals`: category or section subtotal rows.
- `total_score`: sum of scored item scores.
- `max_score`: sum of max scores for scored items.
- `percentage`: provisional scored-evidence percentage, calculated as
  `total_score / max_score * 100`, rounded reasonably.
  Unscorable rows are omitted from this denominator.
- `unscorable_count`: count of rows marked unscorable.
- `unscorable_max_score`: sum of max scores from unscorable rows.
- `grading_friction_notes`: short notes about ambiguous, unsupported, or hard-to-score
  rubric behavior.

## Item Row Fields

Required for every row:

- `item_id`: stable identifier, such as a rubric row number or item key.
- `category`: rubric category or section.
- `question_name`: rubric item text.
- `max_score`: highest available score for this item.
- `rationale`: concise explanation tied to rubric anchors, unless the row is unscorable.
- `confidence`: `high`, `medium`, or `low`, unless the row is unscorable.

Required for scored rows:

- `score`: numeric score assigned from the rubric anchors.
- `evidence`: exact supporting artifact evidence.

Required for unscorable rows:

- `unscorable: true`
- `unscorable_reason`: why the artifact does not support scoring this item.

Optional row fields:

- `mode`: rubric evidence mode when present.
- `score_anchor`: selected rubric anchor key, such as `Score3`.
- `caveat`: brief uncertainty that affects confidence.

## Item Mode Compatibility

When present, `mode` should be one of `note`, `audio`, or `video`.

- `note` rows may be scored only when `artifact_type` is `note`.
- `audio` rows may be scored from `artifact_type: transcript` or
  `artifact_type: transcript_plus_observations`.
- `video` rows may be scored from `artifact_type: observation_log` or
  `artifact_type: transcript_plus_observations`.
- `transcript_plus_observations` must include both `transcript` and `observation_log` in
  `evidence_sources`.
- Any unsupported `mode`, or any supported mode paired with an incompatible
  `artifact_type`, must be marked `unscorable: true` instead of scored.

Raw audio and raw video are never inspected by this skill.
A transcript, note, observation log, or transcript-plus-observation bundle must already
exist as text evidence.

## Evidence Shape

For note and audio rows, `evidence` may be a nonempty string or a nonempty array of
evidence objects.

For video rows, `evidence` must be a nonempty array of evidence objects with at least
one object whose `source` is `observation_log` or `observation`.

Evidence object fields:

- `text`: exact note/transcript text or supplied observation text.
- `timestamp`: timestamp or range for observation-log evidence.
- `source`: label such as `note`, `transcript`, or `observation_log`. Required for video
  evidence objects and optional otherwise.

## Subtotals

Subtotal rows use this shape:

```yaml
subtotals:
  - category: History
    score: 5
    max_score: 8
```

Use `section` instead of `category` only when the rubric groups rows by section.
Subtotals must equal the sum of scored rows in that category or section.
Unscorable rows are omitted from subtotal and total math because no provisional score
was assigned. Use `unscorable_count` and `unscorable_max_score` to preserve
denominator-loss visibility.
