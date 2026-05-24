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
    "evidence_sources": ["note"],
    "items": [
        {
            "item_id": "1",
            "category": "History",
            "question_name": "Documents chest pain timeline",
            "mode": "note",
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
            "mode": "audio",
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


VALID_TRANSCRIPT_GRADE_SHEET = {
    "artifact_type": "transcript",
    "evidence_sources": ["transcript"],
    "items": [
        {
            "item_id": "1",
            "category": "Counseling",
            "question_name": "Explains return precautions verbally",
            "mode": "audio",
            "score": 4,
            "max_score": 4,
            "evidence": "If the chest pain returns or you feel short of breath, call 911.",
            "rationale": "The transcript includes verbal return precautions.",
            "confidence": "high",
        },
        {
            "item_id": "2",
            "category": "Format",
            "question_name": "Uses an institution-specific unsupported mode",
            "mode": "sensor",
            "max_score": 1,
            "unscorable": True,
            "unscorable_reason": "Mode sensor is not supported by the dry-run validator.",
        },
    ],
    "total_score": 4,
    "max_score": 4,
    "percentage": 100,
    "unscorable_count": 1,
    "unscorable_max_score": 1,
}


VALID_TRANSCRIPT_PLUS_OBSERVATIONS_GRADE_SHEET = {
    "artifact_type": "transcript_plus_observations",
    "evidence_sources": ["transcript", "observation_log"],
    "items": [
        {
            "item_id": "1",
            "category": "Counseling",
            "question_name": "Explains return precautions verbally",
            "mode": "audio",
            "score": 4,
            "max_score": 4,
            "evidence": [
                {
                    "text": "If the chest pain returns or you feel short of breath, call 911.",
                    "timestamp": "00:06:10",
                    "source": "transcript",
                }
            ],
            "rationale": "The transcript includes verbal return precautions.",
            "confidence": "high",
        },
        {
            "item_id": "2",
            "category": "Exam",
            "question_name": "Maintains appropriate draping",
            "mode": "video",
            "score": 2,
            "max_score": 2,
            "evidence": [
                {
                    "text": "Learner kept the patient covered except during the exam.",
                    "timestamp": "00:03:20-00:04:05",
                    "source": "observation_log",
                }
            ],
            "rationale": "The observation row documents the visible draping behavior.",
            "confidence": "medium",
        },
    ],
    "total_score": 6,
    "max_score": 6,
    "percentage": 100,
}


VALID_OBSERVATION_GRADE_SHEET = {
    "artifact_type": "observation_log",
    "evidence_sources": ["observation_log"],
    "items": [
        {
            "item_id": "1",
            "category": "Exam",
            "question_name": "Washes hands before exam",
            "mode": "video",
            "score": 1,
            "max_score": 1,
            "evidence": [
                {
                    "timestamp": "00:01:15",
                    "text": "Learner used hand sanitizer before touching the patient.",
                    "source": "observation_log",
                }
            ],
            "rationale": "The observation log documents the visible hand-hygiene action.",
            "confidence": "high",
        }
    ],
    "total_score": 1,
    "max_score": 1,
    "percentage": 100,
}


INVALID_TRANSCRIPT_VIDEO_GRADE_SHEET = {
    "artifact_type": "transcript",
    "evidence_sources": ["transcript"],
    "items": [
        {
            "item_id": "1",
            "category": "Exam",
            "question_name": "Maintains appropriate draping",
            "mode": "video",
            "score": 2,
            "max_score": 2,
            "evidence": "The learner said they would keep the patient covered.",
            "rationale": "This incorrectly scores visible behavior from transcript-only speech.",
            "confidence": "medium",
        }
    ],
    "total_score": 2,
    "max_score": 2,
    "percentage": 100,
}


INVALID_GRADE_SHEET = {
    "artifact_type": "note",
    "items": [
        {
            "item_id": "1",
            "category": "History",
            "question_name": "Documents chest pain timeline",
            "mode": "note",
            "score": 5,
            "max_score": 4,
            "rationale": "Unsupported high score.",
            "confidence": "high",
        },
        {
            "item_id": "2",
            "category": "Counseling",
            "question_name": "Explains return precautions verbally",
            "mode": "audio",
            "max_score": 4,
            "unscorable": True,
        },
        {
            "item_id": "3",
            "category": "Counseling",
            "question_name": "Explains return precautions verbally",
            "mode": "audio",
            "score": 4,
            "max_score": 4,
            "evidence": "Return precautions documented in the note.",
            "rationale": "This incorrectly scores spoken content from a note artifact.",
            "confidence": "medium",
        },
        {
            "item_id": "4",
            "category": "Exam",
            "question_name": "Uses an unsupported sensor mode",
            "mode": "sensor",
            "score": 1,
            "max_score": 1,
            "evidence": "Sensor signal detected.",
            "rationale": "Unsupported modes must not be scored.",
            "confidence": "low",
        },
    ],
    "total_score": 10,
    "max_score": 13,
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
        valid_transcript_path = tmpdir / "valid_transcript.json"
        valid_transcript_plus_observations_path = tmpdir / "valid_transcript_plus_observations.json"
        valid_observation_path = tmpdir / "valid_observation.json"
        invalid_transcript_video_path = tmpdir / "invalid_transcript_video.json"
        invalid_path = tmpdir / "invalid.json"
        valid_path.write_text(json.dumps(VALID_GRADE_SHEET), encoding="utf-8")
        valid_transcript_path.write_text(
            json.dumps(VALID_TRANSCRIPT_GRADE_SHEET),
            encoding="utf-8",
        )
        valid_transcript_plus_observations_path.write_text(
            json.dumps(VALID_TRANSCRIPT_PLUS_OBSERVATIONS_GRADE_SHEET),
            encoding="utf-8",
        )
        valid_observation_path.write_text(
            json.dumps(VALID_OBSERVATION_GRADE_SHEET),
            encoding="utf-8",
        )
        invalid_transcript_video_path.write_text(
            json.dumps(INVALID_TRANSCRIPT_VIDEO_GRADE_SHEET),
            encoding="utf-8",
        )
        invalid_path.write_text(json.dumps(INVALID_GRADE_SHEET), encoding="utf-8")

        for label, path in (
            ("valid note grade sheet", valid_path),
            ("valid transcript grade sheet", valid_transcript_path),
            (
                "valid transcript-plus-observations grade sheet",
                valid_transcript_plus_observations_path,
            ),
            ("valid observation grade sheet", valid_observation_path),
        ):
            valid = run_validator(path)
            if valid.returncode != 0:
                raise RuntimeError(f"{label} failed validation\n{valid.stdout}{valid.stderr}")
            print(f"PASS {label}")

        invalid_transcript_video = run_validator(invalid_transcript_video_path)
        if invalid_transcript_video.returncode == 0:
            raise RuntimeError("transcript-only video grade sheet unexpectedly passed validation")
        transcript_video_output = (
            f"{invalid_transcript_video.stdout}\n{invalid_transcript_video.stderr}"
        )
        if "video" not in transcript_video_output or "observation" not in transcript_video_output:
            raise RuntimeError(
                "transcript-only video grade sheet did not report video observation issue\n"
                f"{transcript_video_output}"
            )
        print("PASS invalid transcript-only video grade sheet")

        invalid = run_validator(invalid_path)
        if invalid.returncode == 0:
            raise RuntimeError("invalid grade sheet unexpectedly passed validation")
        required = ["score", "evidence", "unscorable_reason", "mode"]
        output = f"{invalid.stdout}\n{invalid.stderr}"
        missing = [item for item in required if item not in output]
        if missing:
            raise RuntimeError(
                f"invalid grade sheet did not report expected issues: {missing}\n{output}"
            )
        print("PASS invalid grade sheet")

    print("PASS grading-dry-run smoke test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
