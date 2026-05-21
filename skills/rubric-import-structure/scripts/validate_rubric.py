#!/usr/bin/env python3
"""Validate /rubrics app-compatible rubric YAML or JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CORE_FIELDS = {"Category", "QuestionName", "ScoringLogic"}
OPTIONAL_FIELDS = {"Mode", "Technique", "Purpose", "AdditionalContext"}
ALLOWED_FIELDS = CORE_FIELDS | OPTIONAL_FIELDS
PLUGIN_REQUIRED_FIELDS = ALLOWED_FIELDS
VALID_MODES = {"video", "audio", "note"}
SCORE_KEY_RE = re.compile(r"^Score([1-9][0-9]*)$")


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


def unwrap_rubric(data: Any) -> tuple[list[Any] | None, list[ValidationIssue]]:
    issues: list[ValidationIssue] = []
    if isinstance(data, dict):
        extra_keys = set(data) - {"rubric"}
        if extra_keys:
            issues.append(
                ValidationIssue("$", f"unexpected top-level fields: {sorted(extra_keys)}")
            )
        rubric = data.get("rubric")
    elif isinstance(data, list):
        rubric = data
    else:
        return None, [ValidationIssue("$", "expected top-level 'rubric' array or raw array")]

    if not isinstance(rubric, list):
        issues.append(ValidationIssue("$.rubric", "must be an array"))
        return None, issues
    if not rubric:
        issues.append(ValidationIssue("$.rubric", "must contain at least one item"))
    return rubric, issues


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_scoring(scoring: Any, row_path: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not isinstance(scoring, dict):
        return [ValidationIssue(f"{row_path}.ScoringLogic", "must be an object")]
    if not scoring:
        return [ValidationIssue(f"{row_path}.ScoringLogic", "must contain at least one ScoreN anchor")]

    score_numbers: list[int] = []
    for key, value in scoring.items():
        match = SCORE_KEY_RE.fullmatch(str(key))
        if not match:
            issues.append(
                ValidationIssue(
                    f"{row_path}.ScoringLogic.{key}",
                    "score keys must match Score1, Score2, etc.",
                )
            )
            continue
        score_numbers.append(int(match.group(1)))
        if not is_nonempty_string(value):
            issues.append(
                ValidationIssue(
                    f"{row_path}.ScoringLogic.{key}",
                    "score anchor must be a nonempty string",
                )
            )

    if score_numbers:
        expected = list(range(1, max(score_numbers) + 1))
        if score_numbers != sorted(score_numbers):
            issues.append(
                ValidationIssue(
                    f"{row_path}.ScoringLogic",
                    f"score anchors must be in numeric order; found {score_numbers}",
                )
            )
        if sorted(score_numbers) != expected:
            issues.append(
                ValidationIssue(
                    f"{row_path}.ScoringLogic",
                    f"score anchors must be contiguous from Score1; found {score_numbers}",
                )
            )
    return issues


def validate_item(item: Any, index: int, schema: str) -> list[ValidationIssue]:
    row_path = f"$.rubric[{index}]"
    issues: list[ValidationIssue] = []
    if not isinstance(item, dict):
        return [ValidationIssue(row_path, "must be an object")]

    required = PLUGIN_REQUIRED_FIELDS if schema == "plugin" else CORE_FIELDS
    missing = sorted(required - set(item))
    if missing:
        issues.append(ValidationIssue(row_path, f"missing required fields: {missing}"))

    extra = sorted(set(item) - ALLOWED_FIELDS)
    if extra:
        issues.append(ValidationIssue(row_path, f"unexpected fields: {extra}"))

    for field in sorted((CORE_FIELDS | OPTIONAL_FIELDS) & set(item)):
        if field == "ScoringLogic":
            issues.extend(validate_scoring(item[field], row_path))
            continue
        if field in CORE_FIELDS and not is_nonempty_string(item[field]):
            issues.append(ValidationIssue(f"{row_path}.{field}", "must be a nonempty string"))
        elif field in OPTIONAL_FIELDS and not isinstance(item[field], str):
            issues.append(ValidationIssue(f"{row_path}.{field}", "must be a string"))

    if "Mode" in item and item.get("Mode") not in VALID_MODES:
        issues.append(
            ValidationIssue(
                f"{row_path}.Mode",
                f"must be one of {sorted(VALID_MODES)}",
            )
        )
    return issues


def validate_rubric(data: Any, schema: str = "plugin") -> list[ValidationIssue]:
    rubric, issues = unwrap_rubric(data)
    if rubric is None:
        return issues
    for index, item in enumerate(rubric):
        issues.extend(validate_item(item, index, schema))
    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate app-compatible rubric YAML/JSON."
    )
    parser.add_argument("inputs", nargs="+", help="Rubric YAML or JSON files to validate")
    parser.add_argument(
        "--schema",
        choices=["plugin", "app"],
        default="plugin",
        help=(
            "Validation strictness. 'plugin' requires all rubric-maker-skill fields; "
            "'app' requires only the web app minimum fields."
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

    for raw_path in args.inputs:
        path = Path(raw_path)
        try:
            issues = validate_rubric(load_data(path), schema=args.schema)
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
