#!/usr/bin/env python3
"""Run repository-level smoke checks for the Rubric Maker plugin."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
RUBRIC_IMPORT_SMOKE = (
    REPO_ROOT / "skills" / "rubric-import" / "scripts" / "smoke_test.py"
)
STUDENT_ARTIFACT_VALIDATOR = (
    REPO_ROOT / "skills" / "generate-student-artifact" / "scripts" / "validate_student_artifact.py"
)
GRADING_DRY_RUN_SMOKE = (
    REPO_ROOT / "skills" / "grading-dry-run" / "scripts" / "smoke_test.py"
)
DRY_RUN_SUGGESTION_VALIDATOR = (
    REPO_ROOT / "skills" / "evaluate-dry-run" / "scripts" / "validate_dry_run_suggestions.py"
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
        raise RuntimeError(f"{' '.join(args)} failed with exit code {completed.returncode}\n{output}")


def main() -> int:
    run_command([sys.executable, str(REPO_ROOT / "scripts" / "verify_plugin_compat.py")])
    print("PASS plugin compatibility")

    run_command([sys.executable, str(REPO_ROOT / "scripts" / "verify_schema_sync.py")])
    print("PASS schema sync")

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

    run_command([sys.executable, str(GRADING_DRY_RUN_SMOKE)])
    print("PASS grading-dry-run smoke")

    print("PASS repository smoke test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
