#!/usr/bin/env python3
"""Validate grading-dry-run grade-sheet JSON or YAML."""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeGuard, cast

VALID_ARTIFACT_TYPES = {"note", "observation_log", "transcript", "transcript_plus_observations"}
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_EVIDENCE_SOURCES = {"note", "observation_log", "transcript"}
VALID_OBSERVATION_SOURCES = {"observation", "observation_log"}
VALID_ITEM_MODES = {"audio", "note", "video"}
SUPPORTED_ARTIFACTS_BY_MODE = {
    "audio": {"transcript", "transcript_plus_observations"},
    "note": {"note"},
    "video": {"observation_log", "transcript_plus_observations"},
}
TOTAL_TOLERANCE = 0.01


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str


def require_module(module_name: str, package_hint: str):
    try:
        return __import__(module_name)
    except ImportError as exc:
        raise RuntimeError(
            f"Missing dependency: {package_hint}. Install it and rerun the script."
        ) from exc


def load_data(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        yaml = require_module("yaml", "PyYAML")
        return yaml.safe_load(text)
    return json.loads(text)


def is_number(value: Any) -> TypeGuard[int | float]:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def is_nonempty_string(value: Any) -> TypeGuard[str]:
    return isinstance(value, str) and bool(value.strip())


def numbers_equal(left: float, right: float) -> bool:
    return abs(left - right) <= TOTAL_TOLERANCE


def unwrap_grade_sheet(data: Any) -> tuple[dict[str, Any] | None, list[ValidationIssue]]:
    if not isinstance(data, dict):
        return None, [ValidationIssue("$", "expected a grade-sheet object")]
    if "grade_sheet" in data:
        extra_keys = set(data) - {"grade_sheet"}
        issues = []
        if extra_keys:
            issues.append(
                ValidationIssue("$", f"unexpected top-level fields: {sorted(extra_keys)}")
            )
        grade_sheet = data.get("grade_sheet")
        if not isinstance(grade_sheet, dict):
            issues.append(ValidationIssue("$.grade_sheet", "must be an object"))
            return None, issues
        return grade_sheet, issues
    return data, []


def validate_evidence(evidence: Any, path: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if is_nonempty_string(evidence):
        return issues
    if not isinstance(evidence, list) or not evidence:
        return [ValidationIssue(path, "must be a nonempty string or nonempty array")]

    for index, entry in enumerate(evidence):
        entry_path = f"{path}[{index}]"
        if is_nonempty_string(entry):
            continue
        if not isinstance(entry, dict):
            issues.append(ValidationIssue(entry_path, "must be a string or object"))
            continue
        entry = cast("dict[str, Any]", entry)
        if not is_nonempty_string(entry.get("text")):
            issues.append(ValidationIssue(f"{entry_path}.text", "must be a nonempty string"))
        if "timestamp" in entry and not is_nonempty_string(entry.get("timestamp")):
            issues.append(ValidationIssue(f"{entry_path}.timestamp", "must be a nonempty string"))
        if "source" in entry and not is_nonempty_string(entry.get("source")):
            issues.append(ValidationIssue(f"{entry_path}.source", "must be a nonempty string"))
    return issues


def has_observation_evidence(evidence: Any) -> bool:
    if not isinstance(evidence, list):
        return False
    for entry in evidence:
        if not isinstance(entry, dict):
            continue
        entry = cast("dict[str, Any]", entry)
        source = entry.get("source")
        if source in VALID_OBSERVATION_SOURCES and is_nonempty_string(entry.get("text")):
            return True
    return False


def validate_video_evidence(evidence: Any, path: str) -> list[ValidationIssue]:
    if not isinstance(evidence, list) or not evidence:
        return [
            ValidationIssue(
                f"{path}.evidence",
                "video-mode scored rows must use structured observation evidence",
            )
        ]
    if not has_observation_evidence(evidence):
        return [
            ValidationIssue(
                f"{path}.evidence",
                "video-mode scored rows require evidence with source 'observation_log' or 'observation'",
            )
        ]
    return []


def validate_evidence_sources(
    grade_sheet: dict[str, Any], artifact_type: Any
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    evidence_sources = grade_sheet.get("evidence_sources")
    if evidence_sources is None:
        if artifact_type == "transcript_plus_observations":
            issues.append(
                ValidationIssue(
                    "$.evidence_sources",
                    "is required for transcript_plus_observations and must include transcript and observation_log",
                )
            )
        return issues

    if not isinstance(evidence_sources, list) or not evidence_sources:
        return [ValidationIssue("$.evidence_sources", "must be a nonempty array when present")]

    normalized_sources = set()
    for index, source in enumerate(evidence_sources):
        path = f"$.evidence_sources[{index}]"
        if not is_nonempty_string(source):
            issues.append(ValidationIssue(path, "must be a nonempty string"))
            continue
        if source not in VALID_EVIDENCE_SOURCES:
            issues.append(
                ValidationIssue(
                    path,
                    f"must be one of {sorted(VALID_EVIDENCE_SOURCES)}",
                )
            )
            continue
        normalized_sources.add(source)

    if artifact_type == "transcript_plus_observations":
        required_sources = {"observation_log", "transcript"}
        missing_sources = sorted(required_sources - normalized_sources)
        if missing_sources:
            issues.append(
                ValidationIssue(
                    "$.evidence_sources",
                    f"must include {missing_sources} for transcript_plus_observations",
                )
            )
    elif (
        artifact_type in VALID_EVIDENCE_SOURCES
        and normalized_sources
        and artifact_type not in normalized_sources
    ):
        issues.append(
            ValidationIssue(
                "$.evidence_sources",
                f"must include artifact_type {artifact_type!r} when provided",
            )
        )

    return issues


def validate_item_mode(
    item: dict[str, Any],
    path: str,
    artifact_type: Any,
    unscorable: bool,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if "mode" not in item:
        return issues

    mode = item.get("mode")
    if not is_nonempty_string(mode):
        issues.append(ValidationIssue(f"{path}.mode", "must be a nonempty string when present"))
        return issues

    if mode not in VALID_ITEM_MODES:
        if not unscorable:
            issues.append(
                ValidationIssue(
                    f"{path}.mode",
                    f"unsupported mode {mode!r}; scored rows must use one of {sorted(VALID_ITEM_MODES)}",
                )
            )
        return issues

    if artifact_type not in VALID_ARTIFACT_TYPES:
        return issues

    supported_artifacts = SUPPORTED_ARTIFACTS_BY_MODE[mode]
    if artifact_type not in supported_artifacts and not unscorable:
        issues.append(
            ValidationIssue(
                f"{path}.mode",
                (
                    f"mode {mode!r} is not scoreable from artifact_type {artifact_type!r}; "
                    "mark the row unscorable"
                ),
            )
        )
    return issues


def validate_item(
    item: Any,
    index: int,
    artifact_type: Any,
) -> tuple[list[ValidationIssue], dict[str, Any] | None, float | None]:
    path = f"$.items[{index}]"
    issues: list[ValidationIssue] = []
    if not isinstance(item, dict):
        return [ValidationIssue(path, "must be an object")], None, None

    for field in ("item_id", "category", "question_name"):
        if not is_nonempty_string(item.get(field)):
            issues.append(
                ValidationIssue(f"{path}.{field}", "is required and must be a nonempty string")
            )

    if "max_score" not in item:
        issues.append(ValidationIssue(f"{path}.max_score", "is required"))
        max_score = None
    else:
        max_score = item.get("max_score")
        if not is_number(max_score) or max_score < 0:
            issues.append(ValidationIssue(f"{path}.max_score", "must be a non-negative number"))

    unscorable = item.get("unscorable", False)
    if not isinstance(unscorable, bool):
        issues.append(ValidationIssue(f"{path}.unscorable", "must be a boolean when present"))
        unscorable = False

    issues.extend(validate_item_mode(item, path, artifact_type, unscorable))

    if unscorable:
        if not is_nonempty_string(item.get("unscorable_reason")):
            issues.append(
                ValidationIssue(
                    f"{path}.unscorable_reason",
                    "is required for unscorable items",
                )
            )
        if "score" in item and item.get("score") is not None:
            issues.append(
                ValidationIssue(f"{path}.score", "must be omitted or null for unscorable items")
            )
        unscorable_max_score = float(max_score) if is_number(max_score) else None
        return issues, None, unscorable_max_score

    if "score" not in item:
        issues.append(ValidationIssue(f"{path}.score", "is required for scored items"))
        score = None
    else:
        score = item.get("score")
        if not is_number(score) or score < 0:
            issues.append(ValidationIssue(f"{path}.score", "must be a non-negative number"))
        elif is_number(max_score) and score > max_score:
            issues.append(
                ValidationIssue(f"{path}.score", "must be less than or equal to max_score")
            )

    if "evidence" not in item:
        issues.append(ValidationIssue(f"{path}.evidence", "is required for scored items"))
    else:
        evidence = item.get("evidence")
        issues.extend(validate_evidence(evidence, f"{path}.evidence"))
        if item.get("mode") == "video":
            issues.extend(validate_video_evidence(evidence, path))

    if not is_nonempty_string(item.get("rationale")):
        issues.append(ValidationIssue(f"{path}.rationale", "is required for scored items"))
    confidence = item.get("confidence")
    if confidence not in VALID_CONFIDENCE:
        issues.append(
            ValidationIssue(
                f"{path}.confidence",
                f"must be one of {sorted(VALID_CONFIDENCE)} for scored items",
            )
        )

    if not is_number(score) or not is_number(max_score):
        return issues, None, None
    return (
        issues,
        {
            "category": item.get("category"),
            "section": item.get("section"),
            "score": float(score),
            "max_score": float(max_score),
        },
        None,
    )


def validate_subtotals(
    subtotals: Any,
    scored_items: list[dict[str, Any]],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if subtotals is None:
        return issues
    if not isinstance(subtotals, list):
        return [ValidationIssue("$.subtotals", "must be an array when present")]

    category_totals: dict[str, dict[str, float]] = {}
    section_totals: dict[str, dict[str, float]] = {}
    for item in scored_items:
        if is_nonempty_string(item.get("category")):
            bucket = category_totals.setdefault(item["category"], {"score": 0.0, "max_score": 0.0})
            bucket["score"] += item["score"]
            bucket["max_score"] += item["max_score"]
        if is_nonempty_string(item.get("section")):
            bucket = section_totals.setdefault(item["section"], {"score": 0.0, "max_score": 0.0})
            bucket["score"] += item["score"]
            bucket["max_score"] += item["max_score"]

    for index, subtotal in enumerate(subtotals):
        path = f"$.subtotals[{index}]"
        if not isinstance(subtotal, dict):
            issues.append(ValidationIssue(path, "must be an object"))
            continue
        subtotal = cast("dict[str, Any]", subtotal)
        label_type = (
            "category" if "category" in subtotal else "section" if "section" in subtotal else None
        )
        if label_type is None:
            issues.append(ValidationIssue(path, "must include category or section"))
            continue
        label = subtotal.get(label_type)
        if not is_nonempty_string(label):
            issues.append(ValidationIssue(f"{path}.{label_type}", "must be a nonempty string"))
            continue
        expected = (
            category_totals.get(label) if label_type == "category" else section_totals.get(label)
        )
        if expected is None:
            issues.append(ValidationIssue(path, f"does not match any scored item {label_type}"))
            continue
        for field in ("score", "max_score"):
            value = subtotal.get(field)
            if not is_number(value):
                issues.append(ValidationIssue(f"{path}.{field}", "must be a number"))
            elif not numbers_equal(float(value), expected[field]):
                issues.append(
                    ValidationIssue(
                        f"{path}.{field}",
                        f"must equal summed {label_type} {field} {expected[field]:g}",
                    )
                )
    return issues


def validate_totals(
    grade_sheet: dict[str, Any],
    scored_items: list[dict[str, Any]],
    unscorable_max_scores: list[float],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    expected_total = sum(item["score"] for item in scored_items)
    expected_max = sum(item["max_score"] for item in scored_items)

    if "total_score" in grade_sheet:
        total_score = grade_sheet.get("total_score")
        if not is_number(total_score):
            issues.append(ValidationIssue("$.total_score", "must be a number"))
        elif not numbers_equal(float(total_score), expected_total):
            issues.append(
                ValidationIssue(
                    "$.total_score", f"must equal summed item scores {expected_total:g}"
                )
            )

    if "max_score" in grade_sheet:
        max_score = grade_sheet.get("max_score")
        if not is_number(max_score):
            issues.append(ValidationIssue("$.max_score", "must be a number"))
        elif not numbers_equal(float(max_score), expected_max):
            issues.append(
                ValidationIssue(
                    "$.max_score", f"must equal summed item max scores {expected_max:g}"
                )
            )

    if "percentage" in grade_sheet and grade_sheet.get("percentage") is not None:
        percentage = grade_sheet.get("percentage")
        if not is_number(percentage):
            issues.append(ValidationIssue("$.percentage", "must be a number or null"))
        elif expected_max == 0:
            issues.append(
                ValidationIssue("$.percentage", "must be null or omitted when max_score is 0")
            )
        else:
            expected_percentage = expected_total / expected_max * 100
            if not numbers_equal(float(percentage), expected_percentage):
                issues.append(
                    ValidationIssue(
                        "$.percentage",
                        f"must equal total_score / max_score * 100 ({expected_percentage:g})",
                    )
                )
    if "unscorable_count" in grade_sheet:
        unscorable_count = grade_sheet.get("unscorable_count")
        if (
            not isinstance(unscorable_count, int)
            or isinstance(unscorable_count, bool)
            or unscorable_count < 0
        ):
            issues.append(ValidationIssue("$.unscorable_count", "must be a non-negative integer"))
        elif unscorable_count != len(unscorable_max_scores):
            issues.append(
                ValidationIssue(
                    "$.unscorable_count",
                    f"must equal the number of unscorable rows {len(unscorable_max_scores)}",
                )
            )

    if "unscorable_max_score" in grade_sheet:
        unscorable_max_score = grade_sheet.get("unscorable_max_score")
        expected_unscorable_max = sum(unscorable_max_scores)
        if not is_number(unscorable_max_score):
            issues.append(ValidationIssue("$.unscorable_max_score", "must be a number"))
        elif not numbers_equal(float(unscorable_max_score), expected_unscorable_max):
            issues.append(
                ValidationIssue(
                    "$.unscorable_max_score",
                    f"must equal summed unscorable max scores {expected_unscorable_max:g}",
                )
            )
    return issues


def validate_grade_sheet(data: Any) -> list[ValidationIssue]:
    grade_sheet, issues = unwrap_grade_sheet(data)
    if grade_sheet is None:
        return issues

    artifact_type = grade_sheet.get("artifact_type")
    if artifact_type not in VALID_ARTIFACT_TYPES:
        issues.append(
            ValidationIssue(
                "$.artifact_type",
                f"must be one of {sorted(VALID_ARTIFACT_TYPES)}",
            )
        )
    issues.extend(validate_evidence_sources(grade_sheet, artifact_type))

    items = grade_sheet.get("items")
    if not isinstance(items, list):
        issues.append(ValidationIssue("$.items", "must be a nonempty array"))
        return issues
    if not items:
        issues.append(ValidationIssue("$.items", "must be a nonempty array"))

    scored_items: list[dict[str, Any]] = []
    unscorable_max_scores: list[float] = []
    for index, item in enumerate(items):
        item_issues, scored_item, unscorable_max_score = validate_item(item, index, artifact_type)
        issues.extend(item_issues)
        if scored_item is not None:
            scored_items.append(scored_item)
        if unscorable_max_score is not None:
            unscorable_max_scores.append(unscorable_max_score)

    issues.extend(validate_subtotals(grade_sheet.get("subtotals"), scored_items))
    issues.extend(validate_totals(grade_sheet, scored_items, unscorable_max_scores))
    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate grading-dry-run grade-sheet YAML/JSON.")
    parser.add_argument("inputs", nargs="+", help="Grade-sheet JSON or YAML files to validate")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON validation results.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    results: dict[str, list[dict[str, str]]] = {}
    exit_code = 0

    for raw_path in args.inputs:
        path = Path(raw_path)
        try:
            issues = validate_grade_sheet(load_data(path))
        except Exception as exc:  # noqa: BLE001 - CLI should report parse/dependency errors.
            issues = [ValidationIssue("$", str(exc))]

        if issues:
            exit_code = 1
        results[str(path)] = [{"path": issue.path, "message": issue.message} for issue in issues]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for path, issues in results.items():
            if not issues:
                print(f"OK {path}")
                continue
            print(f"FAIL {path}")
            for issue in issues:
                print(f"  {issue['path']}: {issue['message']}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
