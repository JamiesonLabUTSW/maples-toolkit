# Grade Sheet Contract

Use this contract when producing or validating a provisional dry-run grade sheet.

## Accepted Top-Level Shape

The grade sheet may be either:

```yaml
grade_sheet:
  artifact_type: note
  items: []
```

or the grade-sheet object directly:

```yaml
artifact_type: note
items: []
```

## Required Fields

- `artifact_type`: one of `note`, `transcript`, or `observation_log`.
- `items`: nonempty array with one row per rubric item.

Optional full-grade fields:

- `subtotals`: category or section subtotal rows.
- `total_score`: sum of scored item scores.
- `max_score`: sum of max scores for scored items.
- `percentage`: `total_score / max_score * 100`, rounded reasonably.
- `grading_friction_notes`: short notes about ambiguous, unsupported, or hard-to-score rubric behavior.

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
- `audio` rows may be scored from `transcript` text.
- `video` rows may be scored from `observation_log` text or transcript text that explicitly documents observations.
- Any unsupported `mode`, or any supported mode paired with an incompatible `artifact_type`, must be marked `unscorable: true` instead of scored.

Raw audio and raw video are never inspected by this skill. A transcript, note, or observation log must already exist as text evidence.

## Evidence Shape

`evidence` may be a nonempty string or a nonempty array of evidence objects.

Evidence object fields:

- `text`: exact note/transcript text or supplied observation text.
- `timestamp`: timestamp or range for observation-log evidence.
- `source`: optional label such as `note`, `transcript`, or `observation_log`.

## Subtotals

Subtotal rows use this shape:

```yaml
subtotals:
  - category: History
    score: 5
    max_score: 8
```

Use `section` instead of `category` only when the rubric groups rows by section. Subtotals must equal the sum of scored rows in that category or section. Unscorable rows are omitted from subtotal and total math because no provisional score was assigned.
