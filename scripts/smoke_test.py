#!/usr/bin/env python3
"""Run repository-level smoke checks for the Rubric Maker plugin."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
RUBRIC_IMPORT_SMOKE = (
    REPO_ROOT / "skills" / "rubric-import" / "scripts" / "smoke_test.py"
)


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


def main() -> int:
    run_command([sys.executable, str(REPO_ROOT / "scripts" / "verify_plugin_compat.py")])
    print("PASS plugin compatibility")

    run_command([sys.executable, str(REPO_ROOT / "scripts" / "verify_schema_sync.py")])
    print("PASS schema sync")

    run_command([sys.executable, str(RUBRIC_IMPORT_SMOKE)])
    print("PASS rubric-import smoke")

    print("PASS repository smoke test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
