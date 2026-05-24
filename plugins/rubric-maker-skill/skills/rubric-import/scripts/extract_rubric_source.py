#!/usr/bin/env python3
"""Extract rubric source text from common document formats.

This script does not generate a rubric. It converts source files into a
clean Markdown/text bundle that Codex can use with the rubric-import
or post-encounter-note-rubric skills.
"""

from __future__ import annotations

import argparse
import csv
import html
import sys
from pathlib import Path
from typing import Iterable


SUPPORTED = {".docx", ".pdf", ".xlsx", ".xlsm", ".csv", ".tsv", ".txt", ".md"}


def require_module(module_name: str, package_hint: str):
    try:
        return __import__(module_name)
    except ImportError as exc:
        raise RuntimeError(
            f"Missing dependency for this file type: {package_hint}. "
            f"Install it and rerun the script."
        ) from exc


def normalize_cell(value) -> str:
    if value is None:
        return ""
    text = str(value).replace("\r\n", "\n").replace("\r", "\n").strip()
    return " ".join(line.strip() for line in text.splitlines() if line.strip())


def markdown_table(rows: list[list[str]], max_rows: int | None = None) -> str:
    if not rows:
        return ""
    if max_rows is not None:
        rows = rows[:max_rows]
    width = max(len(row) for row in rows)
    padded = [row + [""] * (width - len(row)) for row in rows]
    escaped = [[cell.replace("|", "\\|") for cell in row] for row in padded]
    header = escaped[0]
    sep = ["---"] * width
    body = escaped[1:]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(sep) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in body)
    return "\n".join(lines)


def extract_docx(path: Path) -> str:
    docx = require_module("docx", "python-docx")
    document = docx.Document(str(path))
    parts: list[str] = []

    paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    if paragraphs:
        parts.append("## Paragraphs\n")
        parts.extend(paragraphs)

    for table_index, table in enumerate(document.tables, start=1):
        rows = [[normalize_cell(cell.text) for cell in row.cells] for row in table.rows]
        if rows:
            parts.append(f"\n## Table {table_index}\n")
            parts.append(markdown_table(rows))

    return "\n\n".join(parts).strip()


def extract_pdf(path: Path) -> str:
    try:
        pdfplumber = __import__("pdfplumber")
    except ImportError:
        pdfplumber = None

    if pdfplumber is not None:
        parts: list[str] = []
        with pdfplumber.open(str(path)) as pdf:
            for page_index, page in enumerate(pdf.pages, start=1):
                text = (page.extract_text() or "").strip()
                if text:
                    parts.append(f"## Page {page_index}\n\n{text}")
        return "\n\n".join(parts).strip()

    try:
        pypdf = __import__("pypdf")
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency for PDF extraction. Install pdfplumber or pypdf."
        ) from exc

    reader = pypdf.PdfReader(str(path))
    parts = []
    for page_index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            parts.append(f"## Page {page_index}\n\n{text}")
    return "\n\n".join(parts).strip()


def extract_excel(path: Path, max_rows: int | None = None) -> str:
    openpyxl = require_module("openpyxl", "openpyxl")
    workbook = openpyxl.load_workbook(str(path), data_only=False, read_only=True)
    parts: list[str] = []
    for sheet in workbook.worksheets:
        rows: list[list[str]] = []
        for row in sheet.iter_rows(values_only=True):
            values = [normalize_cell(value) for value in row]
            if any(values):
                rows.append(values)
        if rows:
            parts.append(f"## Sheet: {sheet.title}\n")
            parts.append(markdown_table(rows, max_rows=max_rows))
    workbook.close()
    return "\n\n".join(parts).strip()


def extract_delimited(path: Path, delimiter: str) -> str:
    rows: list[list[str]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        for row in reader:
            values = [normalize_cell(value) for value in row]
            if any(values):
                rows.append(values)
    return markdown_table(rows)


def extract_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def extract_file(path: Path, max_rows: int | None = None) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return extract_docx(path)
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix in {".xlsx", ".xlsm"}:
        return extract_excel(path, max_rows=max_rows)
    if suffix == ".csv":
        return extract_delimited(path, ",")
    if suffix == ".tsv":
        return extract_delimited(path, "\t")
    if suffix in {".txt", ".md"}:
        return extract_text(path)
    raise ValueError(f"Unsupported file type: {suffix}")


def build_output(paths: Iterable[Path], max_rows: int | None = None) -> str:
    parts: list[str] = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        if path.suffix.lower() not in SUPPORTED:
            raise ValueError(f"Unsupported file type for {path}: {path.suffix}")
        extracted = extract_file(path, max_rows=max_rows)
        title = html.escape(path.name)
        parts.append(f"# Source: {title}\n\n{extracted or '_No extractable text found._'}")
    return "\n\n---\n\n".join(parts).strip() + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract DOCX/PDF/XLSX/CSV/TXT source content into Markdown."
    )
    parser.add_argument("inputs", nargs="+", help="Input source files")
    parser.add_argument("-o", "--output", required=True, help="Output .md/.txt path")
    parser.add_argument(
        "--max-excel-rows",
        type=int,
        default=None,
        help="Optional per-sheet row limit for very large workbooks",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    paths = [Path(value) for value in args.inputs]
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_output(paths, max_rows=args.max_excel_rows), encoding="utf-8")
    print(f"Wrote extracted source text to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
