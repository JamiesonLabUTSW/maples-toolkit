# Content Validation Round Contracts

## Table Of Contents

- [Workflow Boundary](#workflow-boundary)
- [Contract Selection](#contract-selection)
- [Scope Inputs](#scope-inputs)
- [Clarification Preflight Contract](#clarification-preflight-contract)
- [Round 1: Initial Analysis](#round-1-initial-analysis)
- [Round 2: Critique Others](#round-2-critique-others)
- [Round 3: Refined Recommendation](#round-3-refined-recommendation)
- [Synthesis Contract](#synthesis-contract)
- [Error And Fallback Behavior](#error-and-fallback-behavior)

This reference captures the JSON contracts and round structure for content validation.
Use it when simulating a multi-perspective validation workflow or when formatting
outputs for handoff.

## Workflow Boundary

The skill can simulate multiple expert perspectives, filter rubric YAML by issue scope,
and synthesize a final recommendation.
It should simulate the reasoning and JSON contracts only.

Load `workflow-guide.md` for process, boundaries, clarification, educator guidance, and
upstream-to-CLI interpretation.
Use this file for output schemas.

## Contract Selection

Use the synthesis contract as the default complete answer for content validation.
It contains the verdict, fix, agreement breakdown, alternatives, caveats, and reasoning
needed for educator handoff.

Use round-specific contracts only when:

- the user asks for a specific round,
- a workflow needs intermediate handoff artifacts,
- the user provides multiple prior model responses to critique,
- or a validation meeting is being reconstructed step by step.

When the user asks for a concise answer, preserve the same fields and semantics even if
the response is rendered as prose.

## Scope Inputs

Each validation issue may be scoped to:

- the entire rubric,
- a category,
- a specific question ID.

Use the user's clarified issue when available.
If clarification is not available, use the raw user concern.

Include only the relevant rubric section when possible and state the scope explicitly.

## Clarification Preflight Contract

Purpose: convert raw educator feedback into an actionable validation issue before
analysis.
Use this when the user's concern is ambiguous, broad, or not yet tied to rubric
evidence.

Output must be valid JSON:

```json
{
  "clarified_concern": "Clear structured version of the user's concern with rubric references when available",
  "scope": "entire_rubric",
  "target_question_id": null,
  "target_category": null,
  "confidence": 4,
  "needs_user_confirmation": false,
  "clarifying_question": null
}
```

Allowed `scope` values:

- `entire_rubric`
- `category`
- `specific_question`

Set `needs_user_confirmation` to `true` and populate `clarifying_question` only when
missing information could reverse the recommendation or when the target row/category
cannot be identified responsibly.

## Round 1: Initial Analysis

Purpose: each model independently validates whether the user's concern is a legitimate
rubric issue and proposes a specific fix if needed.

Output must be valid JSON:

```json
{
  "validation_verdict": {
    "is_valid_issue": true,
    "severity": 4,
    "priority": "high",
    "summary": "Brief explanation of whether this is a real problem and why"
  },
  "suggested_fix": {
    "field": "Exact field name from rubric",
    "row": "Question number or row identifier",
    "old_value": "Current problematic value from rubric",
    "new_value": "Proposed replacement value",
    "reasoning": "Why this specific change fixes the issue"
  },
  "response_text": "Full detailed analysis"
}
```

Requirements:

- Return JSON only.
- Quote actual problematic rubric content.
- Provide exact old and new values.
- Include complete scoring logic if modifying scores.
- Consider real OSCE practicality.
- Maintain the existing rubric structure and format.
- Recommend changes; do not apply patches unless the user explicitly asks for
  implementation.

Severity scale:

- `5`: critical impact on safety, fairness, or core validity.
- `4`: high impact on scoring accuracy or rater reliability.
- `3`: medium impact; confusion or inconsistency with possible workarounds.
- `2`: low impact.
- `1`: trivial or cosmetic.

## Round 2: Critique Others

Purpose: each model reviews its own Round 1 answer against the other models' answers,
identifies agreements and disagreements, and refines its perspective.

Use at least two previous responses before critique.

If fewer than two Round 1 responses are available, do not present critique as a
multi-perspective consensus.
Either produce additional independent perspectives or state the evidence limitation.

Output must be valid JSON:

```json
{
  "critiques": [
    {
      "model_name": "model_being_critiqued",
      "critique": "Detailed critique of their analysis and suggested fix",
      "agreement_level": 4,
      "key_points": [
        "Point they made well",
        "Point they missed",
        "Point where I disagree"
      ],
      "strengths": "What they did well",
      "weaknesses": "What could be improved",
      "alternative_approach": "Alternative if disagreeing"
    }
  ],
  "consensus_areas": [
    "Area where all or most models agree"
  ],
  "disagreement_areas": [
    "Area where models diverge"
  ],
  "refined_perspective": "Updated view after seeing other responses",
  "response_text": "Full detailed critique"
}
```

Agreement level scale:

- `5`: complete agreement.
- `4`: strong agreement with minor differences.
- `3`: partial agreement on problem but not solution or priority.
- `2`: significant disagreement.
- `1`: fundamental disagreement.

Guidelines:

- Critique reasoning and evidence, not style.
- Acknowledge when another model has a better fix.
- Avoid groupthink; validate independently.
- Explain why disagreements matter.

## Round 3: Refined Recommendation

Purpose: each model gives its final recommendation after reviewing the full discussion.

Use Round 3 only after Round 1 analysis and Round 2 critique are available.
Include educator guidance when the user provides it before final refinement.

Output must be valid JSON:

```json
{
  "final_validation": {
    "is_valid_issue": true,
    "severity": 4,
    "priority": "high",
    "confidence_level": "high",
    "reasoning": "Why the issue is valid or invalid after discussion"
  },
  "final_fix": {
    "field": "Exact field name",
    "row": "Question or row identifier",
    "old_value": "Current text from rubric",
    "new_value": "Final recommended replacement",
    "reasoning": "Why this fix is optimal",
    "alternative_approaches_considered": [
      "Alternative considered and why accepted or rejected"
    ],
    "implementation_notes": "Practical guidance for applying this fix"
  },
  "discussion_impact": {
    "what_changed": "How the discussion changed the model's view",
    "what_stayed": "What remained from Round 1",
    "key_insights": [
      "Insight from another model or critique"
    ]
  },
  "remaining_uncertainties": [
    "Uncertainty or edge case"
  ],
  "response_text": "Full narrative final recommendation"
}
```

Confidence levels:

- `high`: strong consensus or strong evidence.
- `medium`: good reasoning but valid alternatives remain.
- `low`: significant disagreement or missing information.

## Synthesis Contract

Purpose: merge all model rounds into one recommendation for the educator.

Output must be valid JSON:

```json
{
  "synthesized_verdict": {
    "is_valid_issue": true,
    "severity": 4,
    "priority": "high",
    "consensus_level": "unanimous",
    "summary": "Consensus validation statement",
    "dissenting_views": "None - full consensus",
    "confidence": "high"
  },
  "synthesized_fix": {
    "field": "Exact field name from rubric",
    "row": "Question or row identifier",
    "old_value": "Exact current text from rubric",
    "new_value": "Final recommended replacement text",
    "reasoning": "Why this fix best addresses the issue",
    "yaml_patch": {
      "question_id": "exact_question_identifier",
      "field_name": "exact_field_to_change",
      "new_value": "Replacement value for programmatic application"
    },
    "implementation_steps": [
      "Specific action",
      "Verification step"
    ],
    "expected_impact": "What improves after applying the fix"
  },
  "model_agreement_breakdown": {
    "unanimous": [
      "Aspect where all models agreed"
    ],
    "majority": [
      "Aspect where most models agreed"
    ],
    "split": [
      "Aspect with significant disagreement"
    ]
  },
  "alternative_approaches": [
    {
      "description": "Alternative fix considered",
      "proposed_by": "Model or perspective",
      "pros": "Strength",
      "cons": "Reason not chosen",
      "when_to_use": "Context where it may fit"
    }
  ],
  "caveats_and_considerations": [
    "Caveat or follow-up validation"
  ],
  "synthesized_reasoning": "Comprehensive narrative synthesis"
}
```

Consensus levels:

- `unanimous`
- `strong_majority`
- `majority`
- `split`
- `polarized`

Confidence levels:

- `high`
- `medium-high`
- `medium`
- `medium-low`
- `low`

## Error And Fallback Behavior

Consumers may parse JSON from direct text or fenced JSON. Avoid fallback parsing by
returning clean JSON for each round when a JSON contract is requested.

If the issue is not valid, still populate the verdict fields and explain why.
Use `suggested_fix` or `final_fix` to state that no rubric change is recommended when
the contract requires the object.
