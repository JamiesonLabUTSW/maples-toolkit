#!/usr/bin/env python3
"""Render a Rubric Maker rubric to formatted XLSX or DOCX."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

FIELDS = [
    "Category",
    "QuestionName",
    "Mode",
    "Technique",
    "Purpose",
    "AdditionalContext",
]


def require_module(module_name: str, package_hint: str):
    try:
        return __import__(module_name)
    except ImportError as exc:
        raise RuntimeError(
            f"Missing dependency: {package_hint}. Install it and rerun the script."
        ) from exc


def load_rubric(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        yaml = require_module("yaml", "PyYAML")
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)

    if isinstance(data, dict) and "rubric" in data:
        rubric = data["rubric"]
    elif isinstance(data, list):
        rubric = data
    else:
        raise ValueError("Expected a top-level 'rubric' array or a raw rubric array.")

    if not isinstance(rubric, list) or not all(isinstance(item, dict) for item in rubric):
        raise ValueError("Rubric must be an array of objects.")
    return rubric


def score_keys(rubric: list[dict[str, Any]]) -> list[str]:
    keys: set[str] = set()
    for item in rubric:
        scoring = item.get("ScoringLogic") or {}
        if isinstance(scoring, dict):
            keys.update(key for key in scoring if re.fullmatch(r"Score[1-9][0-9]*", key))

    def sort_key(value: str) -> int:
        return int(value.replace("Score", ""))

    return sorted(keys, key=sort_key)


def value(item: dict[str, Any], key: str) -> str:
    raw = item.get(key, "")
    if raw is None:
        return ""
    return str(raw)


def render_xlsx(rubric: list[dict[str, Any]], output: Path) -> None:
    openpyxl = require_module("openpyxl", "openpyxl")
    Workbook = openpyxl.Workbook
    Alignment = openpyxl.styles.Alignment
    Border = openpyxl.styles.Border
    Font = openpyxl.styles.Font
    PatternFill = openpyxl.styles.PatternFill
    Side = openpyxl.styles.Side
    get_column_letter = openpyxl.utils.get_column_letter

    scores = score_keys(rubric)
    headers = ["Row"] + FIELDS + scores

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Rubric"
    sheet.freeze_panes = "A2"

    header_fill = PatternFill("solid", fgColor="1F4E78")
    score_fill = PatternFill("solid", fgColor="5B9BD5")
    header_font = Font(color="FFFFFF", bold=True)
    body_alignment = Alignment(vertical="top", wrap_text=True)
    thin_gray = Side(style="thin", color="D9E2F3")
    border = Border(bottom=thin_gray)

    for col_index, header in enumerate(headers, start=1):
        cell = sheet.cell(row=1, column=col_index, value=header)
        cell.fill = score_fill if header.startswith("Score") else header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border

    for row_index, item in enumerate(rubric, start=2):
        row_values: list[Any] = [row_index - 2]
        row_values.extend(value(item, key) for key in FIELDS)
        scoring = item.get("ScoringLogic") or {}
        row_values.extend(
            str(scoring.get(key, "")) if isinstance(scoring, dict) else "" for key in scores
        )
        for col_index, cell_value in enumerate(row_values, start=1):
            cell = sheet.cell(row=row_index, column=col_index, value=cell_value)
            cell.alignment = body_alignment
            cell.border = border

    widths = {
        "A": 8,
        "B": 22,
        "C": 34,
        "D": 12,
        "E": 42,
        "F": 42,
        "G": 34,
    }
    for column, width in widths.items():
        sheet.column_dimensions[column].width = width
    for col_index in range(8, len(headers) + 1):
        sheet.column_dimensions[get_column_letter(col_index)].width = 38

    for row in range(2, len(rubric) + 2):
        sheet.row_dimensions[row].height = 96

    sheet.auto_filter.ref = sheet.dimensions
    output.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output)


def render_docx(rubric: list[dict[str, Any]], output: Path) -> None:
    docx = require_module("docx", "python-docx")
    Document = docx.Document
    Inches = docx.shared.Inches
    Pt = docx.shared.Pt

    document = Document()
    section = document.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

    styles = document.styles
    styles["Normal"].font.name = "Aptos"
    styles["Normal"].font.size = Pt(10)

    document.add_heading("Rubric", level=1)

    for index, item in enumerate(rubric, start=1):
        title = value(item, "QuestionName") or f"Rubric Item {index}"
        document.add_heading(f"{index}. {title}", level=2)
        meta = document.add_paragraph()
        meta.add_run("Category: ").bold = True
        meta.add_run(value(item, "Category") or "Uncategorized")
        meta.add_run("    Mode: ").bold = True
        meta.add_run(value(item, "Mode") or "video")

        for label in ["Technique", "Purpose", "AdditionalContext"]:
            content = value(item, label)
            if content:
                paragraph = document.add_paragraph()
                paragraph.add_run(f"{label}: ").bold = True
                paragraph.add_run(content)

        scoring = item.get("ScoringLogic") or {}
        if isinstance(scoring, dict) and scoring:
            keys = [key for key in score_keys([item]) if key in scoring]
            table = document.add_table(rows=1, cols=2)
            table.style = "Table Grid"
            header = table.rows[0].cells
            header[0].text = "Score"
            header[1].text = "Criteria"
            for key in keys:
                row = table.add_row().cells
                row[0].text = key.replace("Score", "")
                row[1].text = str(scoring[key])

    output.parent.mkdir(parents=True, exist_ok=True)
    document.save(output)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render Rubric Maker rubric YAML/JSON to formatted XLSX or DOCX."
    )
    parser.add_argument("input", help="Input rubric YAML or JSON")
    parser.add_argument("-o", "--output", required=True, help="Output path")
    parser.add_argument(
        "--format",
        choices=["xlsx", "docx"],
        help="Output format. Defaults to output file extension.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    input_path = Path(args.input)
    output = Path(args.output)
    output_format = args.format or output.suffix.lower().lstrip(".")
    rubric = load_rubric(input_path)

    if output_format == "xlsx":
        render_xlsx(rubric, output)
    elif output_format == "docx":
        render_docx(rubric, output)
    else:
        raise ValueError("Output format must be xlsx or docx.")

    print(f"Wrote formatted rubric to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
