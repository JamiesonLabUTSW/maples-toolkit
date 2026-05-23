---
name: osce-rubric-transform
description: Adapt, enhance, or restyle OSCE rubrics for new cases, patient populations, clinical contexts, scoring scales, or institutional templates. Use when an agent needs to transform rubric content, add score levels, fill missing Purpose or Technique fields, expand Technique examples, or apply style from one rubric to another while preserving clinical intent.
---

# OSCE Rubric Transform

## Workflow

1. Identify the source rubric, target context, learner level, modality, and transformation goal.
2. Preserve clinically valid source content unless the target context makes it wrong, unsafe, unobservable, or misaligned.
3. Generate specific row-level changes. Do not rewrite the entire rubric when targeted suggestions are safer.
4. For missing fields, write `Purpose` as the educational rationale and `Technique` as observable examples or documentation evidence.
5. For score expansion, keep score levels ordered from lowest to highest and make adjacent levels meaningfully different.
6. For template application, copy style patterns without changing clinical facts unless explicitly requested.

## Output Guidance

- Prefer structured suggestions using `location`, `current_value`, `suggested_value`, `reasoning`, `priority`, `row`, `field`, and optional `sub`.
- For full rewrites, output Rubric Maker schema YAML.
- Explain assumptions when transforming a case with incomplete information.

## References

- Load `references/rubric-schema.md` for the shared schema, mode semantics, and structured suggestion conventions.
- Load `references/transform-patterns.md` for enhancement and transformation rules.
