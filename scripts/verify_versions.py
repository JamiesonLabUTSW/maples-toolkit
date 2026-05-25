#!/usr/bin/env python3
"""Verify marketplace and plugin release version policy."""

from __future__ import annotations

import sys

from release_metadata import (
    CLAUDE_MARKETPLACE,
    CODEX_MARKETPLACE,
    PLUGINS_DIR,
    claude_entries,
    claude_marketplace,
    installable_plugins,
    is_semver,
    plugin_manifest,
    plugin_names,
    rel,
    unavailable_plugins,
)


def validate_required_files(plugin_name: str, errors: list[str]) -> None:
    plugin_root = PLUGINS_DIR / plugin_name
    for relative in ("README.md", "requirements.txt"):
        path = plugin_root / relative
        if not path.is_file():
            errors.append(f"installable plugin {plugin_name} is missing {rel(path)}")

    changelog = plugin_root / "CHANGELOG.md"
    if not changelog.is_file():
        errors.append(f"installable plugin {plugin_name} is missing {rel(changelog)}")


def validate_plugin_versions(errors: list[str]) -> None:
    for plugin_name in plugin_names():
        try:
            codex = plugin_manifest(plugin_name, "codex")
            claude = plugin_manifest(plugin_name, "claude")
        except FileNotFoundError as exc:
            errors.append(f"missing manifest for {plugin_name}: {exc.filename}")
            continue

        for runtime, manifest in (("codex", codex), ("claude", claude)):
            path = PLUGINS_DIR / plugin_name / f".{runtime}-plugin" / "plugin.json"
            version = manifest.get("version")
            if not isinstance(version, str) or not is_semver(version):
                errors.append(f"{rel(path)} version must be SemVer without a leading v")

        for key in ("name", "version", "homepage", "license"):
            if codex.get(key) != claude.get(key):
                errors.append(f"plugin {plugin_name} Codex and Claude manifests disagree on {key}")

        codex_author = codex.get("author", {})
        claude_author = claude.get("author", {})
        if isinstance(codex_author, dict) and isinstance(claude_author, dict):
            if codex_author.get("name") != claude_author.get("name"):
                errors.append(
                    f"plugin {plugin_name} Codex and Claude manifests disagree on author.name"
                )


def validate_marketplace_versions(errors: list[str]) -> None:
    try:
        claude = claude_marketplace()
    except FileNotFoundError:
        errors.append(f"missing {rel(CLAUDE_MARKETPLACE)}")
        return

    version = claude.get("version")
    if not isinstance(version, str) or not is_semver(version):
        errors.append(f"{rel(CLAUDE_MARKETPLACE)} version must be SemVer without a leading v")

    if not CODEX_MARKETPLACE.is_file():
        errors.append(f"missing {rel(CODEX_MARKETPLACE)}")


def validate_installable_policy(errors: list[str]) -> None:
    claude = claude_entries()
    installable = set(installable_plugins())
    unavailable = set(unavailable_plugins())

    if set(claude) != installable:
        errors.append(
            "Claude marketplace plugins must exactly match Codex AVAILABLE plugins: "
            f"expected {sorted(installable)}, found {sorted(claude)}"
        )

    for plugin_name in sorted(installable):
        validate_required_files(plugin_name, errors)
        claude_entry = claude.get(plugin_name, {})
        if "version" in claude_entry:
            errors.append(
                f"{rel(CLAUDE_MARKETPLACE)} entry {plugin_name} must not duplicate "
                "plugin manifest version"
            )

    for plugin_name in sorted(unavailable):
        if plugin_name in claude:
            errors.append(
                f"placeholder plugin {plugin_name} is NOT_AVAILABLE in Codex and must not be "
                "listed in the Claude marketplace"
            )

        plugin_root = PLUGINS_DIR / plugin_name
        if (plugin_root / "skills").exists() or (plugin_root / "commands").exists():
            errors.append(
                f"placeholder plugin {plugin_name} has runtime surfaces but remains NOT_AVAILABLE"
            )


def main() -> int:
    errors: list[str] = []
    try:
        validate_plugin_versions(errors)
        validate_marketplace_versions(errors)
        validate_installable_policy(errors)
    except OSError as exc:
        errors.append(str(exc))

    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1

    print("PASS version policy: marketplace and plugin versions are aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
