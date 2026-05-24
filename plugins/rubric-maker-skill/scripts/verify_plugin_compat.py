#!/usr/bin/env python3
"""Verify portable Agent Skills and dual plugin metadata invariants."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
CANONICAL_SCHEMA = REPO_ROOT / "references" / "rubric-schema.md"
SCHEMA_RELATIVE_PATH = Path("references") / "rubric-schema.md"
CANONICAL_GRADE_SHEET_CONTRACT = REPO_ROOT / "references" / "grade-sheet-contract.md"
CANONICAL_GRADE_SHEET_VALIDATOR = (
    REPO_ROOT / "skills" / "grading-dry-run" / "scripts" / "validate_grade_sheet.py"
)
GRADE_SHEET_CONTRACT_RELATIVE_PATH = Path("references") / "grade-sheet-contract.md"
GRADE_SHEET_VALIDATOR_RELATIVE_PATH = Path("scripts") / "validate_grade_sheet.py"
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
FORBIDDEN_UPSTREAM_PATTERNS = (
    "/rubrics",
    "rubrics-app",
    "web app",
    "source map",
    "source-map",
    "src/",
    "prompts/",
    "blueprints/",
)
PUBLISHED_ROOTS = (
    "README.md",
    "AGENTS.md",
    "references",
    "scripts",
    "skills",
    ".codex-plugin",
    ".claude-plugin",
)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def load_json(path: Path, errors: list[str]) -> dict:
    if not path.is_file():
        errors.append(f"missing {rel(path)}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{rel(path)} is invalid JSON: {exc}")
        return {}


def frontmatter(path: Path, errors: list[str]) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not text.startswith("---\n"):
        errors.append(f"{rel(path)} must start with YAML frontmatter")
        return {}, text
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        errors.append(f"{rel(path)} is missing closing frontmatter delimiter")
        return {}, text

    metadata: dict[str, str] = {}
    for raw_line in lines[1:end]:
        if raw_line.startswith(" ") or ": " not in raw_line:
            continue
        key, value = raw_line.split(": ", 1)
        metadata[key] = value.strip().strip('"')
    return metadata, text


def validate_manifest(
    path: Path,
    manifest: dict,
    errors: list[str],
    *,
    require_codex_paths: bool = False,
) -> None:
    name = str(manifest.get("name", ""))
    version = str(manifest.get("version", ""))
    description = str(manifest.get("description", ""))

    if not NAME_RE.fullmatch(name) or "--" in name:
        errors.append(f"{rel(path)} name must be kebab-case and 1-64 characters")
    if not SEMVER_RE.fullmatch(version):
        errors.append(f"{rel(path)} version must be semantic version format")
    if not description:
        errors.append(f"{rel(path)} must include a description")
    if not manifest.get("license"):
        errors.append(f"{rel(path)} must include license metadata")

    author = manifest.get("author")
    if not isinstance(author, dict) or not author.get("name"):
        errors.append(f"{rel(path)} must include author.name")

    if require_codex_paths:
        skills = manifest.get("skills")
        if skills != "./skills/":
            errors.append(f"{rel(path)} skills must be ./skills/")
        if isinstance(skills, str) and not skills.startswith("./"):
            errors.append(f"{rel(path)} skills path must start with ./")
        if not SKILLS_DIR.is_dir():
            errors.append("missing skills directory")


def validate_manifest_alignment(codex: dict, claude: dict, errors: list[str]) -> None:
    for key in ("name", "version", "homepage", "license"):
        if codex.get(key) != claude.get(key):
            errors.append(
                f".codex-plugin/plugin.json and .claude-plugin/plugin.json disagree on {key}"
            )

    codex_author = codex.get("author", {})
    claude_author = claude.get("author", {})
    if isinstance(codex_author, dict) and isinstance(claude_author, dict):
        if codex_author.get("name") != claude_author.get("name"):
            errors.append(
                ".codex-plugin/plugin.json and .claude-plugin/plugin.json disagree on author.name"
            )


def validate_skills(errors: list[str]) -> None:
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        errors.append("no skill files found under skills/")
        return

    canonical_bytes = CANONICAL_SCHEMA.read_bytes() if CANONICAL_SCHEMA.is_file() else None
    if canonical_bytes is None:
        errors.append(f"missing canonical schema: {rel(CANONICAL_SCHEMA)}")
    grade_sheet_contract_bytes = (
        CANONICAL_GRADE_SHEET_CONTRACT.read_bytes()
        if CANONICAL_GRADE_SHEET_CONTRACT.is_file()
        else None
    )
    if grade_sheet_contract_bytes is None:
        errors.append(
            f"missing canonical grade-sheet contract: {rel(CANONICAL_GRADE_SHEET_CONTRACT)}"
        )
    grade_sheet_validator_bytes = (
        CANONICAL_GRADE_SHEET_VALIDATOR.read_bytes()
        if CANONICAL_GRADE_SHEET_VALIDATOR.is_file()
        else None
    )
    if grade_sheet_validator_bytes is None:
        errors.append(
            f"missing canonical grade-sheet validator: {rel(CANONICAL_GRADE_SHEET_VALIDATOR)}"
        )

    for path in skill_files:
        metadata, text = frontmatter(path, errors)
        line_count = len(text.splitlines())
        skill_dir = path.parent
        name = metadata.get("name", "")
        description = metadata.get("description", "")

        if line_count > 500:
            errors.append(f"{rel(path)} has {line_count} lines; keep SKILL.md under 500")
        if name != skill_dir.name:
            errors.append(f"{rel(path)} name must match parent directory {skill_dir.name}")
        if not NAME_RE.fullmatch(name) or "--" in name:
            errors.append(f"{rel(path)} name must be lowercase letters, numbers, and hyphens only")
        if not (1 <= len(description) <= 1024):
            errors.append(f"{rel(path)} description must be 1-1024 characters")
        if "../" in text:
            errors.append(f"{rel(path)} must not reference files outside the skill root")

        schema_path = skill_dir / SCHEMA_RELATIVE_PATH
        if not schema_path.is_file():
            errors.append(f"missing {rel(schema_path)}")
        elif canonical_bytes is not None and schema_path.read_bytes() != canonical_bytes:
            errors.append(f"schema drift detected in {rel(schema_path)}")

        grade_sheet_contract_path = skill_dir / GRADE_SHEET_CONTRACT_RELATIVE_PATH
        grade_sheet_validator_path = skill_dir / GRADE_SHEET_VALIDATOR_RELATIVE_PATH
        uses_grade_sheet_contract = grade_sheet_contract_path.is_file()
        uses_grade_sheet_validator = grade_sheet_validator_path.is_file()
        if uses_grade_sheet_contract:
            if (
                grade_sheet_contract_bytes is not None
                and grade_sheet_contract_path.read_bytes() != grade_sheet_contract_bytes
            ):
                errors.append(
                    f"grade-sheet contract drift detected in {rel(grade_sheet_contract_path)}"
                )
            if not uses_grade_sheet_validator:
                errors.append(
                    f"missing {rel(grade_sheet_validator_path)} for skill with grade-sheet contract"
                )
        if (
            uses_grade_sheet_validator
            and grade_sheet_validator_bytes is not None
            and grade_sheet_validator_path.read_bytes() != grade_sheet_validator_bytes
        ):
            errors.append(
                f"grade-sheet validator drift detected in {rel(grade_sheet_validator_path)}"
            )


def validate_packaging_hygiene(errors: list[str]) -> None:
    ds_store_files = [
        path
        for path in REPO_ROOT.rglob(".DS_Store")
        if ".git" not in path.relative_to(REPO_ROOT).parts
    ]
    for path in ds_store_files:
        errors.append(f"OS metadata file must not be committed or packaged: {rel(path)}")

    zip_files = [
        path for path in REPO_ROOT.rglob("*.zip") if ".git" not in path.relative_to(REPO_ROOT).parts
    ]
    for path in zip_files:
        errors.append(f"generated archive must not be committed or packaged: {rel(path)}")

    pluginignore = REPO_ROOT / ".pluginignore"
    if not pluginignore.is_file():
        errors.append("missing .pluginignore")
        return
    pluginignore_text = pluginignore.read_text(encoding="utf-8")
    for required in ("*.zip", ".DS_Store", "**/.DS_Store"):
        if required not in pluginignore_text:
            errors.append(f".pluginignore must exclude {required}")


def published_files() -> list[Path]:
    files: list[Path] = []
    for root_name in PUBLISHED_ROOTS:
        root = REPO_ROOT / root_name
        if root.is_file():
            files.append(root)
        elif root.is_dir():
            files.extend(path for path in root.rglob("*") if path.is_file())
    return sorted(files)


def validate_no_upstream_references(errors: list[str]) -> None:
    for path in published_files():
        relative = rel(path)
        if path == Path(__file__).resolve():
            continue
        if path.suffix in {".pyc", ".zip"}:
            continue
        if any(part in {".git", "__pycache__"} for part in path.relative_to(REPO_ROOT).parts):
            continue

        lowered_name = relative.lower()
        for pattern in FORBIDDEN_UPSTREAM_PATTERNS:
            if pattern in lowered_name:
                errors.append(
                    f"{relative} must not use unpublished upstream reference marker {pattern!r}"
                )

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        lowered_text = text.lower()
        for pattern in FORBIDDEN_UPSTREAM_PATTERNS:
            if pattern in lowered_text:
                errors.append(
                    f"{relative} must not mention unpublished upstream reference marker {pattern!r}"
                )


def main() -> int:
    errors: list[str] = []

    codex_path = REPO_ROOT / ".codex-plugin" / "plugin.json"
    claude_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
    codex_manifest = load_json(codex_path, errors)
    claude_manifest = load_json(claude_path, errors)

    validate_manifest(codex_path, codex_manifest, errors, require_codex_paths=True)
    validate_manifest(claude_path, claude_manifest, errors)
    validate_manifest_alignment(codex_manifest, claude_manifest, errors)
    validate_skills(errors)
    validate_packaging_hygiene(errors)
    validate_no_upstream_references(errors)

    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1

    print(
        "PASS plugin compatibility: Agent Skills, Codex plugin, and Claude Code plugin invariants hold"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
