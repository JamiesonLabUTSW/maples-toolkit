#!/usr/bin/env python3
"""Run repository-level smoke checks for the Rubric Maker plugin."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUBRIC_IMPORT_SMOKE = REPO_ROOT / "skills" / "rubric-import" / "scripts" / "smoke_test.py"
STUDENT_ARTIFACT_VALIDATOR = (
    REPO_ROOT / "skills" / "generate-student-artifact" / "scripts" / "validate_student_artifact.py"
)
GRADING_DRY_RUN_SMOKE = REPO_ROOT / "skills" / "grading-dry-run" / "scripts" / "smoke_test.py"
DRY_RUN_SUGGESTION_VALIDATOR = (
    REPO_ROOT / "skills" / "evaluate-dry-run" / "scripts" / "validate_dry_run_suggestions.py"
)
EVALUATE_DRY_RUN_GRADE_SHEET_VALIDATOR = (
    REPO_ROOT / "skills" / "evaluate-dry-run" / "scripts" / "validate_grade_sheet.py"
)


def run_command(args: list[str]) -> None:
    completed = subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        output = "\n".join(
            part for part in [completed.stdout.strip(), completed.stderr.strip()] if part
        )
        raise RuntimeError(
            f"{' '.join(args)} failed with exit code {completed.returncode}\n{output}"
        )


def run_expected_failure(args: list[str], expected_snippets: list[str]) -> None:
    completed = subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = "\n".join(
        part for part in [completed.stdout.strip(), completed.stderr.strip()] if part
    )
    if completed.returncode == 0:
        raise RuntimeError(f"{' '.join(args)} unexpectedly passed\n{output}")

    missing = [snippet for snippet in expected_snippets if snippet not in output]
    if missing:
        raise RuntimeError(f"{' '.join(args)} failed without expected output {missing}\n{output}")


def main() -> int:
    run_command([sys.executable, str(REPO_ROOT / "scripts" / "verify_plugin_compat.py")])
    print("PASS plugin compatibility")

    run_command([sys.executable, str(REPO_ROOT / "scripts" / "verify_schema_sync.py")])
    print("PASS schema sync")

    run_command([sys.executable, str(REPO_ROOT / "scripts" / "verify_grade_sheet_schema_sync.py")])
    print("PASS grade-sheet schema sync")

    run_command([sys.executable, str(RUBRIC_IMPORT_SMOKE)])
    print("PASS rubric-import smoke")

    with tempfile.TemporaryDirectory(prefix="rubric-maker-skill-smoke-") as raw_tmpdir:
        tmpdir = Path(raw_tmpdir)

        student_artifact = tmpdir / "student_artifact.json"
        student_artifact.write_text(
            """{
  "artifact_type": "note",
  "artifact_text": "HPI: Chest pain began two hours ago. Assessment: possible ACS.",
  "metadata": {
    "case_summary_used": "Adult with acute chest pain.",
    "intentional_strengths": ["Documents onset"],
    "intentional_weaknesses": ["Sparse plan"],
    "learner_profile": "Average learner",
    "limitations": ["Synthetic artifact for rubric testing"]
  }
}
""",
            encoding="utf-8",
        )
        run_command([sys.executable, str(STUDENT_ARTIFACT_VALIDATOR), str(student_artifact)])
        print("PASS generate-student-artifact validation smoke")

        invalid_observation_log = tmpdir / "invalid_observation_log.json"
        invalid_observation_log.write_text(
            """{
  "artifact_type": "observation_log",
  "artifact_text": "The learner asks several questions but sequence is unclear.",
  "metadata": {
    "case_summary_used": "Adult with acute chest pain.",
    "intentional_strengths": ["Asks about onset"],
    "intentional_weaknesses": ["Does not establish chronology"],
    "learner_profile": {
      "level": "Clerkship student"
    },
    "limitations": ["Synthetic artifact for rubric testing"]
  }
}
""",
            encoding="utf-8",
        )
        run_expected_failure(
            [sys.executable, str(STUDENT_ARTIFACT_VALIDATOR), str(invalid_observation_log)],
            [
                "$.artifact_text: observation_log should contain timestamped or row-delimited observations",
                "$.metadata.source_transcript_summary: is required for observation_log artifacts",
            ],
        )
        print("PASS generate-student-artifact negative validation smoke")

        grade_sheet = tmpdir / "grade_sheet.json"
        grade_sheet.write_text(
            """{
  "artifact_type": "note",
  "evidence_sources": ["note"],
  "items": [
    {
      "item_id": "0",
      "category": "History",
      "question_name": "Documents chest pain details",
      "max_score": 2,
      "score": 1,
      "evidence": "Chest pain began two hours ago.",
      "rationale": "The note documents onset but omits associated symptoms.",
      "confidence": "high",
      "mode": "note",
      "score_anchor": "Score1"
    }
  ],
  "total_score": 1,
  "max_score": 2,
  "percentage": 50
}
""",
            encoding="utf-8",
        )
        run_command([sys.executable, str(EVALUATE_DRY_RUN_GRADE_SHEET_VALIDATOR), str(grade_sheet)])
        print("PASS evaluate-dry-run grade-sheet validation smoke")

        dry_run_suggestions = tmpdir / "dry_run_suggestions.json"
        dry_run_suggestions.write_text(
            """{
  "suggestions": [
    {
      "location": "0:Technique",
      "current_value": "Assess the note.",
      "suggested_value": "Look for explicit documentation of chest pain onset, radiation, associated symptoms, and pertinent negatives.",
      "reasoning": "The dry run showed graders could not map vague technique text to note evidence.",
      "priority": "high",
      "row": 0,
      "field": "Technique"
    }
  ]
}
""",
            encoding="utf-8",
        )
        run_command([sys.executable, str(DRY_RUN_SUGGESTION_VALIDATOR), str(dry_run_suggestions)])
        print("PASS evaluate-dry-run suggestion validation smoke")

        source_rubric = tmpdir / "source_rubric.yaml"
        source_rubric.write_text(
            """rubric:
  - Category: "History"
    QuestionName: "Documents chest pain details"
    ScoringLogic:
      Score1: "No chest pain details are documented."
      Score2: "Some chest pain details are documented."
    Mode: "note"
    Technique: "Assess the note."
    Purpose: "Evaluates documentation of the presenting concern."
    AdditionalContext: ""
""",
            encoding="utf-8",
        )
        run_command(
            [
                sys.executable,
                str(DRY_RUN_SUGGESTION_VALIDATOR),
                "--rubric",
                str(source_rubric),
                str(dry_run_suggestions),
            ]
        )
        print("PASS evaluate-dry-run rubric-backed suggestion validation smoke")

        mismatched_current_value = tmpdir / "mismatched_current_value.json"
        mismatched_current_value.write_text(
            """{
  "suggestions": [
    {
      "location": "0:Technique",
      "current_value": "Assess the plan.",
      "suggested_value": "Look for explicit documentation of chest pain onset, radiation, associated symptoms, and pertinent negatives.",
      "reasoning": "The dry run showed graders could not map vague technique text to note evidence.",
      "priority": "high",
      "row": 0,
      "field": "Technique"
    }
  ]
}
""",
            encoding="utf-8",
        )
        run_expected_failure(
            [
                sys.executable,
                str(DRY_RUN_SUGGESTION_VALIDATOR),
                "--rubric",
                str(source_rubric),
                str(mismatched_current_value),
            ],
            ["$.suggestions[0].current_value: must exactly match the source rubric value"],
        )
        print("PASS evaluate-dry-run rubric-backed negative validation smoke")

        invalid_dry_run_suggestions = tmpdir / "invalid_dry_run_suggestions.json"
        invalid_dry_run_suggestions.write_text(
            """{
  "findings": [
    {
      "id": "F1",
      "pattern": "weak_discrimination",
      "priority": "medium",
      "dry_run_evidence": "All sample artifacts received the same score.",
      "impact": "The rubric does not separate partial from complete performance."
    }
  ],
  "suggestions": [
    {
      "location": "2:Technique.Score2",
      "current_value": "Assess the plan.",
      "suggested_value": "Separate recognition of red flags from counseling quality.",
      "reasoning": "The grade sheet showed the current item bundles distinct behaviors.",
      "priority": "urgent",
      "row": 1,
      "field": "Technique",
      "sub": "Score1",
      "finding_id": "F2",
      "failure_pattern": "unsupported_pattern",
      "confidence": "certain"
    }
  ]
}
""",
            encoding="utf-8",
        )
        run_expected_failure(
            [
                sys.executable,
                str(DRY_RUN_SUGGESTION_VALIDATOR),
                str(invalid_dry_run_suggestions),
            ],
            [
                "$.suggestions[0].priority: must be one of",
                "$.suggestions[0].finding_id: must reference a finding id",
                "$.suggestions[0].failure_pattern: must be one of",
                "$.suggestions[0].confidence: must be one of",
                "$.suggestions[0].location: row 2 does not match row field 1",
                "$.suggestions[0].sub: must match 'Score2'",
                "$.suggestions[0].location: ScoreN suffixes are only valid for ScoringLogic suggestions",
            ],
        )
        print("PASS evaluate-dry-run negative suggestion validation smoke")

    run_command([sys.executable, str(GRADING_DRY_RUN_SMOKE)])
    print("PASS grading-dry-run smoke")

    print("PASS repository smoke test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
