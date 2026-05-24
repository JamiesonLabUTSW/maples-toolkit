#!/usr/bin/env python3
"""Verify skill-local rubric schema references match the canonical copy."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CANONICAL = REPO_ROOT / "references" / "rubric-schema.md"
DEFAULT_SKILLS_DIR = REPO_ROOT / "skills"
SCHEMA_RELATIVE_PATH = Path("references") / "rubric-schema.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check that every skill with a SKILL.md file has a local "
            "references/rubric-schema.md matching the canonical schema."
        )
    )
    parser.add_argument(
        "--canonical",
        type=Path,
        default=DEFAULT_CANONICAL,
        help="Canonical schema file. Defaults to references/rubric-schema.md.",
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=DEFAULT_SKILLS_DIR,
        help="Skills directory to scan. Defaults to skills/.",
    )
    return parser.parse_args()


def skill_dirs(skills_dir: Path) -> list[Path]:
    return sorted(path.parent for path in skills_dir.glob("*/SKILL.md"))


def main() -> int:
    args = parse_args()
    canonical = args.canonical.resolve()
    skills_dir = args.skills_dir.resolve()

    if not canonical.is_file():
        print(f"ERROR missing canonical schema: {canonical}", file=sys.stderr)
        return 1

    if not skills_dir.is_dir():
        print(f"ERROR missing skills directory: {skills_dir}", file=sys.stderr)
        return 1

    canonical_bytes = canonical.read_bytes()
    errors: list[str] = []
    checked = 0

    for skill_dir in skill_dirs(skills_dir):
        checked += 1
        schema_path = skill_dir / SCHEMA_RELATIVE_PATH
        relative_schema_path = schema_path.relative_to(REPO_ROOT)
        if not schema_path.is_file():
            errors.append(f"missing {relative_schema_path}")
            continue
        if schema_path.read_bytes() != canonical_bytes:
            errors.append(f"drift detected in {relative_schema_path}")

    if checked == 0:
        errors.append(f"no skill directories found in {skills_dir.relative_to(REPO_ROOT)}")

    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(
            "Run: cp references/rubric-schema.md skills/<skill-name>/references/rubric-schema.md",
            file=sys.stderr,
        )
        return 1

    print(
        f"PASS schema sync: {checked} skill-local schema files match {canonical.relative_to(REPO_ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
