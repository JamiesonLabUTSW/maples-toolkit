"""Shared release metadata helpers for root validation scripts."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"
CODEX_MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def is_semver(version: str) -> bool:
    return SEMVER_RE.fullmatch(version) is not None


def codex_entries() -> dict[str, dict[str, Any]]:
    payload = load_json(CODEX_MARKETPLACE)
    entries = payload.get("plugins", [])
    return {entry.get("name"): entry for entry in entries if isinstance(entry, dict)}


def claude_marketplace() -> dict[str, Any]:
    return load_json(CLAUDE_MARKETPLACE)


def claude_entries() -> dict[str, dict[str, Any]]:
    payload = claude_marketplace()
    entries = payload.get("plugins", [])
    return {entry.get("name"): entry for entry in entries if isinstance(entry, dict)}


def plugin_manifest(plugin_name: str, runtime: str) -> dict[str, Any]:
    return load_json(PLUGINS_DIR / plugin_name / f".{runtime}-plugin" / "plugin.json")


def plugin_names() -> list[str]:
    return sorted(path.name for path in PLUGINS_DIR.iterdir() if path.is_dir())


def installable_plugins() -> list[str]:
    names: list[str] = []
    for plugin_name, entry in codex_entries().items():
        policy = entry.get("policy", {})
        if isinstance(policy, dict) and policy.get("installation") == "AVAILABLE":
            names.append(plugin_name)
    return sorted(names)


def unavailable_plugins() -> list[str]:
    names: list[str] = []
    for plugin_name, entry in codex_entries().items():
        policy = entry.get("policy", {})
        if isinstance(policy, dict) and policy.get("installation") != "AVAILABLE":
            names.append(plugin_name)
    return sorted(names)


def tag_name_for_plugin(plugin_name: str, version: str) -> str:
    return f"{plugin_name}/v{version}"


def tag_name_for_marketplace(version: str) -> str:
    return f"marketplace/v{version}"
