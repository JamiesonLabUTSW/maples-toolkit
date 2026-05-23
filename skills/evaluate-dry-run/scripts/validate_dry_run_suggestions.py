#!/usr/bin/env python3
"""Validate dry-run rubric-improvement suggestions."""

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
OPTIONAL_FIELDS = {
    "sub",
    "finding_id",
    "failure_pattern",
    "dry_run_evidence",
    "confidence",
}
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
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_PATTERNS = {
    "ambiguous_scoring_anchors",
    "unobservable_or_unsupported_item",
    "missing_case_critical_expectation",
    "evidence_rubric_mismatch",
    "redundant_items",
    "weak_discrimination",
    "misweighted_priority",
    "unsafe_or_fairness_impacting_behavior",
}
LOCATION_RE = re.compile(r"^([0-9]+):([A-Za-z]+)(?:\.(Score[1-9][0-9]*))?$")
SCORE_RE = re.compile(r"^Score[1-9][0-9]*$")
FINDING_ID_RE = re.compile(r"^F[1-9][0-9]*$")


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


def is_nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def unwrap_suggestions(data: Any) -> tuple[list[Any] | None, set[str], list[ValidationIssue]]:
    if isinstance(data, list):
        return data, set(), []
    if not isinstance(data, dict):
        return None, set(), [ValidationIssue("$", "expected an object or raw suggestion array")]

    allowed_top_level = {"findings", "suggestions"}
    issues: list[ValidationIssue] = []
    extra = sorted(set(data) - allowed_top_level)
    if extra:
        issues.append(ValidationIssue("$", f"unexpected top-level fields: {extra}"))

    finding_ids: set[str] = set()
    findings = data.get("findings", [])
    if findings is None:
        findings = []
    if not isinstance(findings, list):
        issues.append(ValidationIssue("$.findings", "must be an array when present"))
    else:
        issues.extend(validate_findings(findings, finding_ids))

    suggestions = data.get("suggestions")
    if not isinstance(suggestions, list):
        issues.append(ValidationIssue("$.suggestions", "must be an array"))
        return None, finding_ids, issues
    return suggestions, finding_ids, issues


def unwrap_rubric(data: Any) -> tuple[list[Any] | None, list[ValidationIssue]]:
    if isinstance(data, list):
        return data, []
    if isinstance(data, dict) and isinstance(data.get("rubric"), list):
        return data["rubric"], []
    return None, [
        ValidationIssue("$", "rubric must be a raw array or an object with a rubric array")
    ]


def load_rubric(path: Path) -> tuple[list[Any] | None, list[ValidationIssue]]:
    try:
        return unwrap_rubric(load_data(path))
    except Exception as exc:  # noqa: BLE001 - CLI should report parse/dependency errors.
        return None, [ValidationIssue("$", str(exc))]


def validate_findings(findings: list[Any], finding_ids: set[str]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    required = {"id", "pattern", "priority", "dry_run_evidence", "impact"}
    allowed = required | {"rubric_location", "recommendation"}

    for index, finding in enumerate(findings):
        path = f"$.findings[{index}]"
        if not isinstance(finding, dict):
            issues.append(ValidationIssue(path, "must be an object"))
            continue

        missing = sorted(required - set(finding))
        if missing:
            issues.append(ValidationIssue(path, f"missing required fields: {missing}"))

        extra = sorted(set(finding) - allowed)
        if extra:
            issues.append(ValidationIssue(path, f"unexpected fields: {extra}"))

        finding_id = finding.get("id")
        if not isinstance(finding_id, str) or not FINDING_ID_RE.fullmatch(finding_id):
            issues.append(ValidationIssue(f"{path}.id", "must match F1, F2, etc."))
        elif finding_id in finding_ids:
            issues.append(ValidationIssue(f"{path}.id", "must be unique"))
        else:
            finding_ids.add(finding_id)

        if finding.get("pattern") not in VALID_PATTERNS:
            issues.append(
                ValidationIssue(
                    f"{path}.pattern",
                    f"must be one of {sorted(VALID_PATTERNS)}",
                )
            )
        if finding.get("priority") not in VALID_PRIORITIES:
            issues.append(
                ValidationIssue(
                    f"{path}.priority",
                    f"must be one of {sorted(VALID_PRIORITIES)}",
                )
            )

        for key in ("dry_run_evidence", "impact"):
            if key in finding and not is_nonempty_text(finding[key]):
                issues.append(ValidationIssue(f"{path}.{key}", "must be nonempty text"))

        for key in ("rubric_location", "recommendation"):
            if key in finding and finding[key] is not None and not isinstance(finding[key], str):
                issues.append(ValidationIssue(f"{path}.{key}", "must be a string or null"))
    return issues


def validate_location(item: dict[str, Any], index: int) -> list[ValidationIssue]:
    path = f"$.suggestions[{index}]"
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

    issues: list[ValidationIssue] = []
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
            issues.append(ValidationIssue(f"{path}.sub", f"must match {location_sub!r}"))
    elif sub is not None:
        issues.append(
            ValidationIssue(
                f"{path}.sub",
                "must be omitted or null unless location has a ScoreN suffix",
            )
        )

    if location_sub and location_field != "ScoringLogic":
        issues.append(
            ValidationIssue(
                f"{path}.location",
                "ScoreN suffixes are only valid for ScoringLogic suggestions",
            )
        )
    return issues


def validate_suggestion(
    item: Any,
    index: int,
    finding_ids: set[str],
) -> list[ValidationIssue]:
    path = f"$.suggestions[{index}]"
    if not isinstance(item, dict):
        return [ValidationIssue(path, "must be an object")]

    issues: list[ValidationIssue] = []
    missing = sorted(REQUIRED_FIELDS - set(item))
    if missing:
        issues.append(ValidationIssue(path, f"missing required fields: {missing}"))

    extra = sorted(set(item) - ALLOWED_FIELDS)
    if extra:
        issues.append(ValidationIssue(path, f"unexpected fields: {extra}"))

    for field in (
        "location",
        "reasoning",
        "priority",
        "current_value",
        "suggested_value",
        "field",
    ):
        if field in item and not isinstance(item[field], str):
            issues.append(ValidationIssue(f"{path}.{field}", "must be a string"))

    for field in ("reasoning", "suggested_value"):
        if field in item and not is_nonempty_text(item[field]):
            issues.append(ValidationIssue(f"{path}.{field}", "must be nonempty text"))

    if item.get("priority") not in VALID_PRIORITIES:
        issues.append(
            ValidationIssue(f"{path}.priority", f"must be one of {sorted(VALID_PRIORITIES)}")
        )

    row = item.get("row")
    if not isinstance(row, int) or isinstance(row, bool) or row < 0:
        issues.append(ValidationIssue(f"{path}.row", "must be a nonnegative integer"))

    if item.get("field") not in RUBRIC_FIELDS:
        issues.append(ValidationIssue(f"{path}.field", f"must be one of {sorted(RUBRIC_FIELDS)}"))

    if "sub" in item and item["sub"] is not None and not isinstance(item["sub"], str):
        issues.append(ValidationIssue(f"{path}.sub", "must be a ScoreN string or null"))
    if isinstance(item.get("sub"), str) and not SCORE_RE.fullmatch(item["sub"]):
        issues.append(ValidationIssue(f"{path}.sub", "must match Score1, Score2, etc."))

    finding_id = item.get("finding_id")
    if finding_id is not None:
        if not isinstance(finding_id, str) or not FINDING_ID_RE.fullmatch(finding_id):
            issues.append(ValidationIssue(f"{path}.finding_id", "must match F1, F2, etc."))
        elif finding_ids and finding_id not in finding_ids:
            issues.append(ValidationIssue(f"{path}.finding_id", "must reference a finding id"))

    if item.get("failure_pattern") is not None and item.get("failure_pattern") not in VALID_PATTERNS:
        issues.append(
            ValidationIssue(
                f"{path}.failure_pattern",
                f"must be one of {sorted(VALID_PATTERNS)}",
            )
        )

    if item.get("confidence") is not None and item.get("confidence") not in VALID_CONFIDENCE:
        issues.append(
            ValidationIssue(f"{path}.confidence", f"must be one of {sorted(VALID_CONFIDENCE)}")
        )

    if "dry_run_evidence" in item and item["dry_run_evidence"] is not None:
        if not is_nonempty_text(item["dry_run_evidence"]):
            issues.append(ValidationIssue(f"{path}.dry_run_evidence", "must be nonempty text"))

    if REQUIRED_FIELDS <= set(item):
        issues.extend(validate_location(item, index))
    return issues


def validate_against_rubric(
    item: Any,
    index: int,
    rubric: list[Any],
) -> list[ValidationIssue]:
    path = f"$.suggestions[{index}]"
    if not isinstance(item, dict):
        return []

    row = item.get("row")
    field = item.get("field")
    sub = item.get("sub")
    if (
        not isinstance(row, int)
        or isinstance(row, bool)
        or row < 0
        or field not in RUBRIC_FIELDS
        or (sub is not None and not isinstance(sub, str))
        or "current_value" not in item
    ):
        return []

    issues: list[ValidationIssue] = []
    if row >= len(rubric):
        return [
            ValidationIssue(
                f"{path}.row",
                f"does not exist in rubric with {len(rubric)} row(s)",
            )
        ]

    rubric_row = rubric[row]
    if not isinstance(rubric_row, dict):
        return [ValidationIssue(f"{path}.row", "source rubric row must be an object")]

    if field not in rubric_row:
        return [ValidationIssue(f"{path}.field", "does not exist in source rubric row")]

    source_value = rubric_row[field]
    if sub is not None:
        if field != "ScoringLogic":
            return [
                ValidationIssue(
                    f"{path}.sub",
                    "cannot be used with non-ScoringLogic rubric fields",
                )
            ]
        if not isinstance(source_value, dict):
            return [
                ValidationIssue(
                    f"{path}.field",
                    "source rubric ScoringLogic must be an object when sub is provided",
                )
            ]
        if sub not in source_value:
            return [ValidationIssue(f"{path}.sub", "does not exist in source ScoringLogic")]
        source_value = source_value[sub]
    elif field == "ScoringLogic" and isinstance(source_value, dict):
        return [
            ValidationIssue(
                f"{path}.sub",
                "is required to validate exact current_value for ScoringLogic.ScoreN anchors",
            )
        ]

    if not isinstance(source_value, str):
        issues.append(
            ValidationIssue(
                f"{path}.current_value",
                "source rubric value must be a string for exact current_value validation",
            )
        )
    elif item.get("current_value") != source_value:
        issues.append(
            ValidationIssue(
                f"{path}.current_value",
                "must exactly match the source rubric value at row/field/sub",
            )
        )
    return issues


def validate_suggestions(data: Any, rubric: list[Any] | None = None) -> list[ValidationIssue]:
    suggestions, finding_ids, issues = unwrap_suggestions(data)
    if suggestions is None:
        return issues
    for index, item in enumerate(suggestions):
        issues.extend(validate_suggestion(item, index, finding_ids))
        if rubric is not None:
            issues.extend(validate_against_rubric(item, index, rubric))
    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate dry-run rubric-improvement suggestion YAML or JSON."
    )
    parser.add_argument("inputs", nargs="+", help="Suggestion YAML or JSON files to validate")
    parser.add_argument(
        "--rubric",
        help=(
            "Optional source rubric YAML or JSON. When provided, row/field/sub targets and "
            "current_value are validated against the rubric. Without it, only suggestion shape "
            "and internal consistency are checked."
        ),
    )
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
    rubric: list[Any] | None = None

    if args.rubric:
        rubric, rubric_issues = load_rubric(Path(args.rubric))
        if rubric_issues:
            exit_code = 1
            results[str(Path(args.rubric))] = [
                {"path": issue.path, "message": issue.message} for issue in rubric_issues
            ]

    for raw_path in args.inputs:
        path = Path(raw_path)
        try:
            issues = validate_suggestions(load_data(path), rubric)
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
