#!/usr/bin/env python3
"""Verify grade-sheet contract and validator copies stay synchronized."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CANONICAL_CONTRACT = REPO_ROOT / "references" / "grade-sheet-contract.md"
DEFAULT_CANONICAL_VALIDATOR = (
    REPO_ROOT / "skills" / "grading-dry-run" / "scripts" / "validate_grade_sheet.py"
)
DEFAULT_SKILLS_DIR = REPO_ROOT / "skills"
CONTRACT_RELATIVE_PATH = Path("references") / "grade-sheet-contract.md"
VALIDATOR_RELATIVE_PATH = Path("scripts") / "validate_grade_sheet.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check that each skill-local grade-sheet contract matches the canonical "
            "contract and each copied grade-sheet validator matches the canonical validator."
        )
    )
    parser.add_argument(
        "--canonical-contract",
        type=Path,
        default=DEFAULT_CANONICAL_CONTRACT,
        help="Canonical grade-sheet contract. Defaults to references/grade-sheet-contract.md.",
    )
    parser.add_argument(
        "--canonical-validator",
        type=Path,
        default=DEFAULT_CANONICAL_VALIDATOR,
        help=(
            "Canonical grade-sheet validator. Defaults to "
            "skills/grading-dry-run/scripts/validate_grade_sheet.py."
        ),
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=DEFAULT_SKILLS_DIR,
        help="Skills directory to scan. Defaults to skills/.",
    )
    return parser.parse_args()


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def skill_dirs(skills_dir: Path) -> list[Path]:
    return sorted(path.parent for path in skills_dir.glob("*/SKILL.md"))


def main() -> int:
    args = parse_args()
    canonical_contract = args.canonical_contract.resolve()
    canonical_validator = args.canonical_validator.resolve()
    skills_dir = args.skills_dir.resolve()

    errors: list[str] = []
    if not canonical_contract.is_file():
        errors.append(f"missing canonical grade-sheet contract: {rel(canonical_contract)}")
        canonical_contract_bytes = None
    else:
        canonical_contract_bytes = canonical_contract.read_bytes()

    if not canonical_validator.is_file():
        errors.append(f"missing canonical grade-sheet validator: {rel(canonical_validator)}")
        canonical_validator_bytes = None
    else:
        canonical_validator_bytes = canonical_validator.read_bytes()

    if not skills_dir.is_dir():
        errors.append(f"missing skills directory: {rel(skills_dir)}")

    checked_contracts = 0
    checked_validators = 0
    if not errors:
        for skill_dir in skill_dirs(skills_dir):
            contract_path = skill_dir / CONTRACT_RELATIVE_PATH
            validator_path = skill_dir / VALIDATOR_RELATIVE_PATH
            uses_contract = contract_path.is_file()
            uses_validator = validator_path.is_file()

            if uses_contract:
                checked_contracts += 1
                if contract_path.read_bytes() != canonical_contract_bytes:
                    errors.append(f"grade-sheet contract drift detected in {rel(contract_path)}")

                if not uses_validator:
                    errors.append(
                        f"missing {rel(validator_path)} for skill with grade-sheet contract"
                    )

            if uses_validator:
                checked_validators += 1
                if validator_path.read_bytes() != canonical_validator_bytes:
                    errors.append(f"grade-sheet validator drift detected in {rel(validator_path)}")

    if checked_contracts == 0:
        errors.append("no skill-local grade-sheet contracts found")
    if checked_validators == 0:
        errors.append("no skill-local grade-sheet validators found")

    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(
            "Run: cp references/grade-sheet-contract.md "
            "skills/<skill-name>/references/grade-sheet-contract.md",
            file=sys.stderr,
        )
        print(
            "Run: cp skills/grading-dry-run/scripts/validate_grade_sheet.py "
            "skills/<skill-name>/scripts/validate_grade_sheet.py",
            file=sys.stderr,
        )
        return 1

    print(
        "PASS grade-sheet sync: "
        f"{checked_contracts} contract file(s) match {rel(canonical_contract)}; "
        f"{checked_validators} validator file(s) match {rel(canonical_validator)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
