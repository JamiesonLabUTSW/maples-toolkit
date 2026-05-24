#!/usr/bin/env python3
"""Verify marketplace metadata and the Rubric Maker plugin package."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"
RUBRIC_PLUGIN_ROOT = PLUGINS_DIR / "rubric-maker-skill"
EXPECTED_PLUGINS = {
    "rubric-maker-skill": {
        "codex_installation": "AVAILABLE",
        "description": "Skills for creating, importing, reviewing, transforming, dry-running, validating, and formatting OSCE rubrics.",
    },
    "case-generation": {
        "codex_installation": "NOT_AVAILABLE",
        "description": "Placeholder for future case generation workflows and skills.",
    },
    "validation-analysis": {
        "codex_installation": "NOT_AVAILABLE",
        "description": "Placeholder for future validation analysis workflows and skills.",
    },
}


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


def plugin_manifest(plugin_name: str, runtime: str, errors: list[str]) -> dict:
    path = PLUGINS_DIR / plugin_name / f".{runtime}-plugin" / "plugin.json"
    payload = load_json(path, errors)
    if payload and payload.get("name") != plugin_name:
        errors.append(f"{rel(path)} name must match plugin directory {plugin_name}")
    return payload


def validate_codex_marketplace(errors: list[str]) -> None:
    path = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
    payload = load_json(path, errors)
    if not payload:
        return

    if payload.get("name") != "ut-real-project-maples":
        errors.append(f"{rel(path)} name must be ut-real-project-maples")
    interface = payload.get("interface")
    if not isinstance(interface, dict) or interface.get("displayName") != "UT REAL Project MAPLES":
        errors.append(f"{rel(path)} interface.displayName must be UT REAL Project MAPLES")

    entries = payload.get("plugins")
    if not isinstance(entries, list):
        errors.append(f"{rel(path)} plugins must be an array")
        return
    by_name = {entry.get("name"): entry for entry in entries if isinstance(entry, dict)}
    if set(by_name) != set(EXPECTED_PLUGINS):
        errors.append(f"{rel(path)} plugins must be {sorted(EXPECTED_PLUGINS)}")
        return

    for plugin_name, expected in EXPECTED_PLUGINS.items():
        entry = by_name[plugin_name]
        source = entry.get("source")
        if source != {"source": "local", "path": f"./plugins/{plugin_name}"}:
            errors.append(f"{rel(path)} entry {plugin_name} has invalid source")
        policy = entry.get("policy")
        if not isinstance(policy, dict):
            errors.append(f"{rel(path)} entry {plugin_name} policy must be an object")
        else:
            if policy.get("installation") != expected["codex_installation"]:
                errors.append(
                    f"{rel(path)} entry {plugin_name} policy.installation must be "
                    f"{expected['codex_installation']}"
                )
            if policy.get("authentication") != "ON_INSTALL":
                errors.append(f"{rel(path)} entry {plugin_name} policy.authentication must be ON_INSTALL")
        if entry.get("category") != "Education":
            errors.append(f"{rel(path)} entry {plugin_name} category must be Education")
        if not (PLUGINS_DIR / plugin_name).is_dir():
            errors.append(f"missing plugin directory plugins/{plugin_name}")
        plugin_manifest(plugin_name, "codex", errors)


def validate_claude_marketplace(errors: list[str]) -> None:
    path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
    payload = load_json(path, errors)
    if not payload:
        return

    if payload.get("name") != "ut-real-project-maples":
        errors.append(f"{rel(path)} name must be ut-real-project-maples")
    entries = payload.get("plugins")
    if not isinstance(entries, list):
        errors.append(f"{rel(path)} plugins must be an array")
        return
    by_name = {entry.get("name"): entry for entry in entries if isinstance(entry, dict)}
    if set(by_name) != set(EXPECTED_PLUGINS):
        errors.append(f"{rel(path)} plugins must be {sorted(EXPECTED_PLUGINS)}")
        return

    for plugin_name, expected in EXPECTED_PLUGINS.items():
        entry = by_name[plugin_name]
        if entry.get("source") != f"./plugins/{plugin_name}":
            errors.append(f"{rel(path)} entry {plugin_name} source must be ./plugins/{plugin_name}")
        if entry.get("description") != expected["description"]:
            errors.append(f"{rel(path)} entry {plugin_name} description drifted")
        plugin_manifest(plugin_name, "claude", errors)


def validate_manifest_alignment(errors: list[str]) -> None:
    for plugin_name in EXPECTED_PLUGINS:
        codex = plugin_manifest(plugin_name, "codex", errors)
        claude = plugin_manifest(plugin_name, "claude", errors)
        for key in ("name", "version", "homepage", "license"):
            if codex.get(key) != claude.get(key):
                errors.append(f"plugin {plugin_name} Codex and Claude manifests disagree on {key}")
        if codex.get("author", {}).get("name") != claude.get("author", {}).get("name"):
            errors.append(f"plugin {plugin_name} Codex and Claude manifests disagree on author.name")


def run_rubric_plugin_check() -> int:
    return subprocess.run(
        [sys.executable, str(RUBRIC_PLUGIN_ROOT / "scripts" / "verify_plugin_compat.py")],
        cwd=RUBRIC_PLUGIN_ROOT,
        check=False,
    ).returncode


def main() -> int:
    errors: list[str] = []
    validate_codex_marketplace(errors)
    validate_claude_marketplace(errors)
    validate_manifest_alignment(errors)

    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1

    nested_status = run_rubric_plugin_check()
    if nested_status != 0:
        return nested_status

    print("PASS marketplace compatibility: root marketplaces and plugin manifests are aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
