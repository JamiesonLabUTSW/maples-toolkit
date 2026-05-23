#!/usr/bin/env python3
"""Validate generated student artifact YAML or JSON."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


VALID_ARTIFACT_TYPES = {"note", "observation_log", "transcript"}
REQUIRED_TOP_LEVEL_FIELDS = {"artifact_type", "artifact_text", "metadata"}
OPTIONAL_TOP_LEVEL_FIELDS = {
    "rubric_focus",
    "target_performance_band",
    "template_name",
    "title",
}
ALLOWED_TOP_LEVEL_FIELDS = REQUIRED_TOP_LEVEL_FIELDS | OPTIONAL_TOP_LEVEL_FIELDS
REQUIRED_METADATA_FIELDS = {
    "case_summary_used",
    "intentional_strengths",
    "intentional_weaknesses",
    "learner_profile",
    "limitations",
}
OPTIONAL_METADATA_FIELDS = {
    "assumptions",
    "source_materials_summary",
    "source_transcript_summary",
}
ALLOWED_METADATA_FIELDS = REQUIRED_METADATA_FIELDS | OPTIONAL_METADATA_FIELDS


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
    text = sys.stdin.read() if str(path) == "-" else path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        yaml = require_module("yaml", "PyYAML")
        return yaml.safe_load(text)
    if suffix == ".json":
        return json.loads(text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        yaml = require_module("yaml", "PyYAML")
        return yaml.safe_load(text)


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_nonempty_string_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(is_nonempty_string(item) for item in value)
    )


def validate_optional_string(value: Any, path: str) -> list[ValidationIssue]:
    if value is None or is_nonempty_string(value):
        return []
    return [ValidationIssue(path, "must be a nonempty string when present")]


def validate_optional_string_list(value: Any, path: str) -> list[ValidationIssue]:
    if value is None:
        return []
    if is_nonempty_string_list(value):
        return []
    return [ValidationIssue(path, "must be a nonempty list of nonempty strings when present")]


def validate_learner_profile(value: Any) -> list[ValidationIssue]:
    if is_nonempty_string(value):
        return []
    if isinstance(value, dict) and value:
        blank_keys = [str(key) for key, item in value.items() if item in (None, "", [], {})]
        if blank_keys:
            return [
                ValidationIssue(
                    "$.metadata.learner_profile",
                    f"object values must not be empty: {sorted(blank_keys)}",
                )
            ]
        return []
    return [
        ValidationIssue(
            "$.metadata.learner_profile",
            "must be a nonempty string or nonempty object",
        )
    ]


def validate_metadata(metadata: Any) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not isinstance(metadata, dict):
        return [ValidationIssue("$.metadata", "must be an object")]

    missing = sorted(REQUIRED_METADATA_FIELDS - set(metadata))
    if missing:
        issues.append(ValidationIssue("$.metadata", f"missing required fields: {missing}"))

    extra = sorted(set(metadata) - ALLOWED_METADATA_FIELDS)
    if extra:
        issues.append(ValidationIssue("$.metadata", f"unexpected fields: {extra}"))

    if "case_summary_used" in metadata and not is_nonempty_string(
        metadata["case_summary_used"]
    ):
        issues.append(
            ValidationIssue("$.metadata.case_summary_used", "must be a nonempty string")
        )

    if "learner_profile" in metadata:
        issues.extend(validate_learner_profile(metadata["learner_profile"]))

    for field in ("intentional_strengths", "intentional_weaknesses", "limitations"):
        if field in metadata and not is_nonempty_string_list(metadata[field]):
            issues.append(
                ValidationIssue(
                    f"$.metadata.{field}",
                    "must be a nonempty list of nonempty strings",
                )
            )

    if "assumptions" in metadata:
        issues.extend(validate_optional_string_list(metadata["assumptions"], "$.metadata.assumptions"))

    if "source_materials_summary" in metadata and not is_nonempty_string(
        metadata["source_materials_summary"]
    ):
        issues.append(
            ValidationIssue(
                "$.metadata.source_materials_summary",
                "must be a nonempty string when present",
            )
        )

    return issues


def validate_artifact(data: Any) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not isinstance(data, dict):
        return [ValidationIssue("$", "must be an object")]

    missing = sorted(REQUIRED_TOP_LEVEL_FIELDS - set(data))
    if missing:
        issues.append(ValidationIssue("$", f"missing required fields: {missing}"))

    extra = sorted(set(data) - ALLOWED_TOP_LEVEL_FIELDS)
    if extra:
        issues.append(ValidationIssue("$", f"unexpected fields: {extra}"))

    artifact_type = data.get("artifact_type")
    if artifact_type not in VALID_ARTIFACT_TYPES:
        issues.append(
            ValidationIssue(
                "$.artifact_type",
                f"must be one of {sorted(VALID_ARTIFACT_TYPES)}",
            )
        )

    artifact_text = data.get("artifact_text")
    if "artifact_text" in data and not is_nonempty_string(artifact_text):
        issues.append(ValidationIssue("$.artifact_text", "must be a nonempty string"))
    elif artifact_type == "observation_log" and is_nonempty_string(artifact_text):
        if ":" not in artifact_text and "-" not in artifact_text:
            issues.append(
                ValidationIssue(
                    "$.artifact_text",
                    "observation_log should contain timestamped or row-delimited observations",
                )
            )

    for field in ("target_performance_band", "template_name", "title"):
        if field in data:
            issues.extend(validate_optional_string(data[field], f"$.{field}"))

    if "rubric_focus" in data:
        issues.extend(validate_optional_string_list(data["rubric_focus"], "$.rubric_focus"))

    metadata = data.get("metadata")
    if "metadata" in data:
        issues.extend(validate_metadata(metadata))
        if artifact_type == "observation_log" and isinstance(metadata, dict):
            if not is_nonempty_string(metadata.get("source_transcript_summary")):
                issues.append(
                    ValidationIssue(
                        "$.metadata.source_transcript_summary",
                        "is required for observation_log artifacts",
                    )
                )

    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate generated student artifact YAML/JSON."
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Student artifact YAML or JSON files to validate. Use '-' for stdin.",
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
            issues = validate_artifact(load_data(path))
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
