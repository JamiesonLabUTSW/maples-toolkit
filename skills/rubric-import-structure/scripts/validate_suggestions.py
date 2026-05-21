#!/usr/bin/env python3
"""Validate /rubrics app-compatible analysis or transform suggestions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "location",
    "reasoning",
    "priority",
    "current_value",
    "suggested_value",
    "row",
    "field",
}
OPTIONAL_FIELDS = {"sub", "evaluation_context"}
ALLOWED_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS
RUBRIC_FIELDS = {
    "Category",
    "QuestionName",
    "ScoringLogic",
    "Mode",
    "Technique",
    "Purpose",
    "AdditionalContext",
}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}
LOCATION_RE = re.compile(r"^([0-9]+):([A-Za-z]+)(?:\.(Score[1-9][0-9]*))?$")
SCORE_RE = re.compile(r"^Score[1-9][0-9]*$")


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


def unwrap_suggestions(data: Any) -> tuple[list[Any] | None, list[ValidationIssue]]:
    if isinstance(data, list):
        return data, []
    if isinstance(data, dict):
        extra_keys = set(data) - {"suggestions"}
        issues = []
        if extra_keys:
            issues.append(
                ValidationIssue("$", f"unexpected top-level fields: {sorted(extra_keys)}")
            )
        suggestions = data.get("suggestions")
        if not isinstance(suggestions, list):
            issues.append(ValidationIssue("$.suggestions", "must be an array"))
            return None, issues
        return suggestions, issues
    return None, [ValidationIssue("$", "expected top-level 'suggestions' array or raw array")]


def is_text(value: Any) -> bool:
    return isinstance(value, str)


def validate_location(item: dict[str, Any], index: int) -> list[ValidationIssue]:
    path = f"$.suggestions[{index}]"
    issues: list[ValidationIssue] = []
    location = item.get("location")
    if not isinstance(location, str):
        return [ValidationIssue(f"{path}.location", "must be a string")]

    match = LOCATION_RE.fullmatch(location)
    if not match:
        return [
            ValidationIssue(
                f"{path}.location",
                "must match row:Field or row:ScoringLogic.ScoreN",
            )
        ]

    location_row = int(match.group(1))
    location_field = match.group(2)
    location_sub = match.group(3)

    if isinstance(item.get("row"), int) and not isinstance(item.get("row"), bool):
        if item["row"] != location_row:
            issues.append(
                ValidationIssue(
                    f"{path}.location",
                    f"row {location_row} does not match row field {item['row']}",
                )
            )
    if item.get("field") != location_field:
        issues.append(
            ValidationIssue(
                f"{path}.location",
                f"field {location_field!r} does not match field value {item.get('field')!r}",
            )
        )

    sub = item.get("sub")
    if location_sub:
        if sub != location_sub:
            issues.append(
                ValidationIssue(
                    f"{path}.sub",
                    f"must match location subfield {location_sub!r}",
                )
            )
    elif sub is not None:
        issues.append(ValidationIssue(f"{path}.sub", "must be omitted or null unless location has .ScoreN"))

    if location_sub and location_field != "ScoringLogic":
        issues.append(
            ValidationIssue(
                f"{path}.location",
                "ScoreN subfields are only valid for ScoringLogic suggestions",
            )
        )
    return issues


def validate_suggestion(item: Any, index: int) -> list[ValidationIssue]:
    path = f"$.suggestions[{index}]"
    issues: list[ValidationIssue] = []
    if not isinstance(item, dict):
        return [ValidationIssue(path, "must be an object")]

    missing = sorted(REQUIRED_FIELDS - set(item))
    if missing:
        issues.append(ValidationIssue(path, f"missing required fields: {missing}"))

    extra = sorted(set(item) - ALLOWED_FIELDS)
    if extra:
        issues.append(ValidationIssue(path, f"unexpected fields: {extra}"))

    for field in ["location", "reasoning", "priority", "current_value", "suggested_value", "field"]:
        if field in item and not is_text(item[field]):
            issues.append(ValidationIssue(f"{path}.{field}", "must be a string"))

    if "reasoning" in item and isinstance(item["reasoning"], str) and not item["reasoning"].strip():
        issues.append(ValidationIssue(f"{path}.reasoning", "must be nonempty"))

    if item.get("priority") not in VALID_PRIORITIES:
        issues.append(
            ValidationIssue(
                f"{path}.priority",
                f"must be one of {sorted(VALID_PRIORITIES)}",
            )
        )

    row = item.get("row")
    if not isinstance(row, int) or isinstance(row, bool) or row < 0:
        issues.append(ValidationIssue(f"{path}.row", "must be a nonnegative integer"))

    if item.get("field") not in RUBRIC_FIELDS:
        issues.append(
            ValidationIssue(
                f"{path}.field",
                f"must be one of {sorted(RUBRIC_FIELDS)}",
            )
        )

    if "sub" in item and item["sub"] is not None and not isinstance(item["sub"], str):
        issues.append(ValidationIssue(f"{path}.sub", "must be a ScoreN string or null"))
    if isinstance(item.get("sub"), str) and not SCORE_RE.fullmatch(item["sub"]):
        issues.append(ValidationIssue(f"{path}.sub", "must match Score1, Score2, etc."))

    if "evaluation_context" in item and not isinstance(item["evaluation_context"], str):
        issues.append(ValidationIssue(f"{path}.evaluation_context", "must be a string"))

    if REQUIRED_FIELDS <= set(item):
        issues.extend(validate_location(item, index))
    return issues


def validate_suggestions(data: Any) -> list[ValidationIssue]:
    suggestions, issues = unwrap_suggestions(data)
    if suggestions is None:
        return issues
    for index, item in enumerate(suggestions):
        issues.extend(validate_suggestion(item, index))
    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate app-compatible rubric suggestion YAML/JSON."
    )
    parser.add_argument("inputs", nargs="+", help="Suggestion YAML or JSON files to validate")
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
            issues = validate_suggestions(load_data(path))
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
