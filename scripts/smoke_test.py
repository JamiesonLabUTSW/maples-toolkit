#!/usr/bin/env python3
"""Compatibility wrapper for the Rubric Maker smoke test."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = REPO_ROOT / "plugins" / "rubric-maker-skill"


def main() -> int:
    return subprocess.run(
        [sys.executable, str(PLUGIN_ROOT / "scripts" / "smoke_test.py")],
        cwd=PLUGIN_ROOT,
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
