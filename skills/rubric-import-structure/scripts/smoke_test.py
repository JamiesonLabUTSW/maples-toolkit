#!/usr/bin/env python3
"""Smoke test rubric-maker-skill deterministic tooling."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
SAMPLE_RUBRIC = SKILL_DIR / "references" / "sample-rubric.yaml"


def has_module(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def run_command(args: list[str]) -> None:
    completed = subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        output = "\n".join(
            part for part in [completed.stdout.strip(), completed.stderr.strip()] if part
        )
        raise RuntimeError(f"{' '.join(args)} failed with exit code {completed.returncode}\n{output}")


def validate_plugin_manifest() -> None:
    manifest_path = REPO_ROOT / ".codex-plugin" / "plugin.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not data.get("name"):
        raise AssertionError("plugin manifest is missing name")
    if not data.get("version"):
        raise AssertionError("plugin manifest is missing version")


def frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    if end == -1:
        return ""
    return text[4:end]


def validate_skill_files() -> None:
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        raise AssertionError("no skill files found")

    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        meta = frontmatter(text)
        missing: list[str] = []
        if "name:" not in meta:
            missing.append("frontmatter name")
        if "description:" not in meta:
            missing.append("frontmatter description")
        if "# " not in text:
            missing.append("heading")
        if "## Workflow" not in text:
            missing.append("Workflow section")
        if missing:
            raise AssertionError(f"{path.relative_to(REPO_ROOT)} missing {', '.join(missing)}")


def exercise_extractors(tmpdir: Path) -> list[str]:
    skipped: list[str] = []
    extractor = SCRIPT_DIR / "extract_rubric_source.py"
    sample_text = tmpdir / "sample-source.txt"
    sample_text.write_text(
        "Case summary: learner documents symptom timeline, prioritized differential, and initial plan.\n",
        encoding="utf-8",
    )
    run_command([sys.executable, str(extractor), str(sample_text), "-o", str(tmpdir / "extracted-text.md")])

    sample_csv = tmpdir / "sample-source.csv"
    sample_csv.write_text(
        "Category,QuestionName,Mode\nHistory,Documents symptom timeline,note\n",
        encoding="utf-8",
    )
    run_command([sys.executable, str(extractor), str(sample_csv), "-o", str(tmpdir / "extracted-csv.md")])

    return skipped


def exercise_renderers(tmpdir: Path) -> list[str]:
    skipped: list[str] = []
    renderer = SCRIPT_DIR / "render_rubric.py"

    if has_module("yaml") and has_module("openpyxl"):
        run_command([sys.executable, str(renderer), str(SAMPLE_RUBRIC), "-o", str(tmpdir / "rubric.xlsx")])
    else:
        skipped.append("xlsx rendering requires PyYAML and openpyxl")

    if has_module("yaml") and has_module("docx"):
        run_command([sys.executable, str(renderer), str(SAMPLE_RUBRIC), "-o", str(tmpdir / "rubric.docx")])
    else:
        skipped.append("docx rendering requires PyYAML and python-docx")

    return skipped


def main() -> int:
    validate_plugin_manifest()
    print("PASS plugin manifest")

    validate_skill_files()
    print("PASS skill files")

    run_command([sys.executable, str(SCRIPT_DIR / "validate_rubric.py"), str(SAMPLE_RUBRIC)])
    print(f"PASS rubric validation: {SAMPLE_RUBRIC.relative_to(REPO_ROOT)}")

    with tempfile.TemporaryDirectory(prefix="rubric-maker-smoke-") as raw_tmpdir:
        tmpdir = Path(raw_tmpdir)
        skipped = exercise_extractors(tmpdir)
        skipped.extend(exercise_renderers(tmpdir))

    if skipped:
        for item in skipped:
            print(f"SKIP {item}")
    print("PASS smoke test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
