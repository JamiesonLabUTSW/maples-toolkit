# Scoring Rules

Use the rubric anchors and supplied artifact evidence to assign provisional scores.

## Score Selection

- `Score1` is the lowest performance level; higher `ScoreN` anchors represent higher performance.
- Use the highest anchor fully supported by artifact evidence.
- Partial evidence should map to the closest supported anchor, with a rationale and lower confidence when appropriate.
- If the rubric uses mixed max scores, preserve each row's actual `max_score`.
- Never assign a score greater than `max_score`.

## Unscorable Rows

Mark a row as unscorable when:

- The required modality is absent.
- The artifact lacks the evidence needed to apply the item.
- The rubric item depends on facts outside the supplied artifact.
- The item is too ambiguous to score mechanically from the artifact.

Unscorable rows still keep `max_score`, but they are omitted from subtotal and total calculations because no provisional score was assigned.

## Totals

- `total_score` is the sum of scored row `score` values.
- `max_score` is the sum of scored row `max_score` values.
- `percentage` is `total_score / max_score * 100`.
- Subtotals use the same rule within each category or section.
- If every row is unscorable, use `total_score: 0`, `max_score: 0`, and omit `percentage` or set it to `null`.
