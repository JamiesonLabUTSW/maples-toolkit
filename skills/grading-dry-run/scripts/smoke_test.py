#!/usr/bin/env python3
"""Smoke test grading-dry-run validation."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
VALIDATOR = SCRIPT_DIR / "validate_grade_sheet.py"


VALID_GRADE_SHEET = {
    "artifact_type": "note",
    "items": [
        {
            "item_id": "1",
            "category": "History",
            "question_name": "Documents chest pain timeline",
            "score": 3,
            "max_score": 4,
            "evidence": "Chest pain began two hours ago while walking.",
            "rationale": "The note documents onset and context but omits duration details.",
            "confidence": "high",
        },
        {
            "item_id": "2",
            "category": "Counseling",
            "question_name": "Explains return precautions verbally",
            "max_score": 4,
            "unscorable": True,
            "unscorable_reason": "The supplied artifact is a note and does not include spoken counseling.",
        },
    ],
    "subtotals": [
        {
            "category": "History",
            "score": 3,
            "max_score": 4,
        }
    ],
    "total_score": 3,
    "max_score": 4,
    "percentage": 75,
}


INVALID_GRADE_SHEET = {
    "artifact_type": "note",
    "items": [
        {
            "item_id": "1",
            "category": "History",
            "question_name": "Documents chest pain timeline",
            "score": 5,
            "max_score": 4,
            "rationale": "Unsupported high score.",
            "confidence": "high",
        },
        {
            "item_id": "2",
            "category": "Counseling",
            "question_name": "Explains return precautions verbally",
            "max_score": 4,
            "unscorable": True,
        },
    ],
    "total_score": 5,
    "max_score": 8,
}


def run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="grading-dry-run-smoke-") as raw_tmpdir:
        tmpdir = Path(raw_tmpdir)
        valid_path = tmpdir / "valid.json"
        invalid_path = tmpdir / "invalid.json"
        valid_path.write_text(json.dumps(VALID_GRADE_SHEET), encoding="utf-8")
        invalid_path.write_text(json.dumps(INVALID_GRADE_SHEET), encoding="utf-8")

        valid = run_validator(valid_path)
        if valid.returncode != 0:
            raise RuntimeError(f"valid grade sheet failed validation\n{valid.stdout}{valid.stderr}")
        print("PASS valid grade sheet")

        invalid = run_validator(invalid_path)
        if invalid.returncode == 0:
            raise RuntimeError("invalid grade sheet unexpectedly passed validation")
        required = ["score", "evidence", "unscorable_reason"]
        output = f"{invalid.stdout}\n{invalid.stderr}"
        missing = [item for item in required if item not in output]
        if missing:
            raise RuntimeError(f"invalid grade sheet did not report expected issues: {missing}\n{output}")
        print("PASS invalid grade sheet")

    print("PASS grading-dry-run smoke test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
