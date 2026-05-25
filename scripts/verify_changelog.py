#!/usr/bin/env python3
"""Verify release changelog structure and current version entries."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from release_metadata import (
    CLAUDE_MARKETPLACE,
    PLUGINS_DIR,
    REPO_ROOT,
    claude_marketplace,
    installable_plugins,
    plugin_manifest,
    plugin_names,
    rel,
    unavailable_plugins,
)

HEADING_RE = re.compile(
    r"^## \[([^\]]+)\](?:\[[^\]]+\])?(?: - (\d{4}-\d{2}-\d{2}))?$",
    re.MULTILINE,
)
REQUIRED_SECTIONS = ("Added", "Changed", "Deprecated", "Removed", "Fixed", "Security")


def changelog_versions(text: str) -> set[str]:
    return {match.group(1) for match in HEADING_RE.finditer(text)}


def validate_changelog_file(
    path: Path,
    release_unit: str,
    target_version: str | None,
    errors: list[str],
) -> None:
    if not path.is_file():
        errors.append(f"missing changelog for {release_unit}: {rel(path)}")
        return

    text = path.read_text(encoding="utf-8")
    if not text.startswith("# Changelog\n"):
        errors.append(f"{rel(path)} must start with '# Changelog'")
    if "## [Unreleased]" not in text:
        errors.append(f"{rel(path)} must include an [Unreleased] section")

    unreleased_start = text.find("## [Unreleased]")
    if unreleased_start != -1:
        next_release = text.find("\n## [", unreleased_start + 1)
        unreleased_block = (
            text[unreleased_start:] if next_release == -1 else text[unreleased_start:next_release]
        )
        for section in REQUIRED_SECTIONS:
            if f"### {section}" not in unreleased_block:
                errors.append(f"{rel(path)} [Unreleased] must include ### {section}")

    if target_version and target_version not in changelog_versions(text):
        errors.append(f"{rel(path)} must include a [{target_version}] release heading")


def main() -> int:
    errors: list[str] = []

    try:
        marketplace_version = claude_marketplace().get("version")
    except OSError as exc:
        errors.append(str(exc))
        marketplace_version = None

    validate_changelog_file(
        REPO_ROOT / "CHANGELOG.md",
        "marketplace",
        marketplace_version if isinstance(marketplace_version, str) else None,
        errors,
    )

    for plugin_name in installable_plugins():
        try:
            version = plugin_manifest(plugin_name, "codex").get("version")
        except OSError as exc:
            errors.append(str(exc))
            version = None
        validate_changelog_file(
            PLUGINS_DIR / plugin_name / "CHANGELOG.md",
            plugin_name,
            version if isinstance(version, str) else None,
            errors,
        )

    for plugin_name in unavailable_plugins():
        changelog = PLUGINS_DIR / plugin_name / "CHANGELOG.md"
        if changelog.is_file():
            validate_changelog_file(changelog, plugin_name, None, errors)
            text = changelog.read_text(encoding="utf-8")
            if "no public releases yet" not in text.lower():
                errors.append(
                    f"{rel(changelog)} must state that placeholder plugin has no public releases yet"
                )

    # Keep the marketplace location visible in failures if the root changelog version is absent.
    if marketplace_version is None:
        errors.append(f"{rel(CLAUDE_MARKETPLACE)} must declare the marketplace version")

    # If plugin directories are added before marketplaces are updated, surface the missing changelog.
    for plugin_name in plugin_names():
        changelog = PLUGINS_DIR / plugin_name / "CHANGELOG.md"
        if not changelog.is_file() and plugin_name not in unavailable_plugins():
            errors.append(f"missing plugin changelog: {rel(changelog)}")

    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1

    print("PASS changelog policy: release-unit changelogs are present and structured")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
