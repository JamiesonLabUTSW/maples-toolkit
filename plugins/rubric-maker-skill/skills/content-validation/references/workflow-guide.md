# Content Validation Workflow Guide

## Table Of Contents

- [Purpose](#purpose)
- [Inputs To Gather](#inputs-to-gather)
- [Decision Boundary](#decision-boundary)
- [CLI Workflow](#cli-workflow)
- [Round Gates](#round-gates)
- [Expert Lenses](#expert-lenses)
- [Educator Guidance](#educator-guidance)
- [Output Routing](#output-routing)
- [Sibling Skill Boundaries](#sibling-skill-boundaries)
- [Do Not Port From The App](#do-not-port-from-the-app)

## Purpose

Use content validation to adjudicate a specific OSCE rubric concern after rubric use,
dry-run testing, rater feedback, learner data, colleague review, or a disputed proposed
fix.

The core question is:

> Is this rubric concern clinically or educationally valid, how severe is it, and what
> should change after weighing competing interpretations?

This is not a broad rubric audit or a generic rewrite workflow.
It is a focused validity judgment with an actionable recommendation.

## Inputs To Gather

Gather these inputs when available:

- Raw concern from the educator, rater, learner data, colleague, or prior agent.
- Rubric YAML or the relevant row/category.
- Case context, learner level, station duration, modality, and evaluator constraints.
- Affected `Category`, `QuestionName`, scoring fields, `Technique`, `Purpose`, or
  `AdditionalContext`.
- Proposed fix or competing interpretations, if any.
- Educator guidance such as preferred perspective, tie-breaker, focus area, or priority.

Ask a clarifying question only when the concern cannot be safely scoped or when the
missing context could reverse the recommendation.

## Decision Boundary

Prefer `content-validation` when:

- A specific rubric concern needs validation, severity, and priority.
- Multiple fixes or interpretations conflict.
- A prior review finding needs clinical or assessment-quality adjudication.
- A proposed change might alter clinical facts, learner expectations, safety, fairness,
  or rater reliability.
- The user asks for a consensus, critique, final recommendation, or "is this a real
  issue?"

Do not use this skill as the first tool for broad artifact creation, import,
transformation, grading setup, or simulation design.
Use the sibling boundaries below.

## CLI Workflow

1. Clarify the concern.
   - Restate the concern in structured form.
   - Identify whether the scope is `entire_rubric`, `category`, or `specific_question`.
   - If the user supplied a raw complaint, convert it into an actionable validation
     issue before judging it.
   - Load `validation-round-contracts.md` if the clarification needs to be returned as
     JSON.

2. Scope the rubric evidence.
   - Use the full rubric only when the issue affects global consistency.
   - For category issues, focus on rows with the matching `Category`.
   - For specific-question issues, focus on the matching `QuestionName`.
   - If the target cannot be found, state that and proceed cautiously with the nearest
     relevant evidence.

3. Analyze independently through expert lenses.
   - Produce distinct judgments for clinical correctness, assessment quality,
     implementation feasibility, and risk/safety.
   - Avoid false consensus.
     Identify where perspectives genuinely disagree.

4. Critique alternatives.
   - Compare proposed fixes, prior model responses, or plausible alternatives.
   - Evaluate evidence, not style.
   - Prefer fixes that preserve valid source content while improving scoring clarity and
     feasibility.

5. Refine with educator guidance.
   - Treat educator guidance as high-priority domain context.
   - If the educator identifies a tie-breaker model or perspective, explain whether and
     how that changes the final recommendation.
   - If guidance conflicts with clinical safety, fairness, or station feasibility, state
     the conflict directly.

6. Synthesize the final recommendation.
   - State whether the issue is valid.
   - Assign severity and priority.
   - Provide exact old and new values for rubric changes.
   - Include implementation steps and verification guidance.
   - List dissenting views, alternatives, caveats, and remaining uncertainties.
   - Recommend patches; do not apply rubric edits unless the user explicitly asks for
     implementation.

## Round Gates

Use gates as quality checks, not as app state:

- Clarification gate: proceed only when the issue can be scoped well enough that the
  missing context is unlikely to reverse the recommendation.
- Round 1 gate: produce at least two independent perspectives before using critique or
  synthesis contracts.
  If only one perspective is available, state that confidence is limited.
- Round 2 gate: critique at least two Round 1 perspectives before final refinement.
- Round 3 gate: final refinement should consider Round 1 analysis, Round 2 critique, and
  any educator guidance.
- Synthesis gate: distinguish unanimous, majority, split, or polarized agreement before
  choosing a final fix.

In interactive CLI use, pause after critique if educator guidance would materially
improve the final recommendation.
In autonomous use, proceed with clearly stated assumptions.

## Expert Lenses

Use these lenses to simulate a multi-perspective review in a single Agent CLI session:

- Clinical correctness: Is the content medically accurate and appropriate for the case
  and learner level?
- Educational assessment quality: Does the rubric support valid, reliable, observable,
  and fair scoring?
- Practical implementation: Can raters apply the item in the station time, available
  modality, and likely evidence source?
- Risk and safety: Could the item create unsafe expectations, unfair scoring, or
  misleading feedback?

## Educator Guidance

Educator guidance may arrive before analysis, after critique, or after a synthesized
recommendation. Represent it explicitly:

- `guidance_text`: what the educator wants models to consider.
- `tie_breaker`: a model, response, or perspective the educator finds more persuasive.
- `focus_area`: the aspect to prioritize, such as clinical accuracy, scoring
  reliability, feasibility, or safety.
- `priority_level`: the educator's stated urgency.

Use this guidance to refine the recommendation, not to bypass independent validation.

## Output Routing

Load `validation-round-contracts.md` for exact JSON shapes.

Default to the synthesis contract for a complete content-validation answer.
Use round-specific contracts only when the user asks to simulate a specific phase or
when another workflow needs intermediate handoff artifacts.

Use the rubric schema reference when proposing changes to `Category`, `QuestionName`,
`ScoringLogic`, `Mode`, `Technique`, `Purpose`, or `AdditionalContext`.

If the user explicitly asks for prose, keep the same contract semantics and headings:
verdict, fix, agreement, alternatives, caveats, and reasoning.

## Sibling Skill Boundaries

Use `osce-rubric-review` for broad audit/discovery of rubric problems.
Escalate to `content-validation` only for findings whose validity, severity, or fix is
contested or high-stakes.

Use `osce-rubric-transform` for direct adaptation, restyling, score expansion,
Technique/Purpose filling, or template application.
Use `content-validation` first when the transformation may change clinical facts or when
preservation of valid source content is uncertain.

Use `post-encounter-note-rubric` to create note-mode rubrics from case materials.
Use `content-validation` for debated documentation expectations, safety-critical
omissions, or whether a note criterion fits the learner and case.

Use `rubric-import` to convert source material into Rubric Maker YAML or JSON. Do not
use `content-validation` for mechanical import.
Use it after import if preserved source wording contains questionable clinical criteria
or conflicting score anchors.

Use `generate-student-artifact` to create synthetic sample notes or transcripts.
Use `grading-dry-run` to produce trial grade sheets from sample artifacts.
Use `evaluate-dry-run` for routine rubric improvements based on trial grading results.
Use `content-validation` when the dry-run evidence, scoring basis, or proposed fix
raises a substantive clinical validity, fairness, safety, or severity concern.

Live OSCE simulation case design belongs outside this rubric-focused plugin.
Use `content-validation` only when case-to-rubric alignment is disputed or expected
learner tasks need clinical validity review.

## Do Not Port From The App

Do not reproduce app-specific implementation details unless the user asks for app
development:

- Database tables and persistence states.
- Flask route names.
- Frontend panels, buttons, and streaming UI behavior.
- Specific model defaults or model branding.
- Raw Jinja prompt templates.

Preserve the workflow logic, contracts, and decision points instead.
