#!/usr/bin/env python3
"""Run non-mutating release readiness checks for a plugin or marketplace release."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from release_metadata import (
    PLUGINS_DIR,
    REPO_ROOT,
    claude_marketplace,
    installable_plugins,
    is_semver,
    plugin_manifest,
    rel,
    tag_name_for_marketplace,
    tag_name_for_plugin,
)
from verify_changelog import changelog_versions

FORBIDDEN_NAMES = {".DS_Store"}
FORBIDDEN_SUFFIXES = {".zip", ".tar", ".tgz", ".gz", ".log"}
FORBIDDEN_DIRS = {
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "build",
    "dist",
    "tmp",
    "output",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    unit = parser.add_mutually_exclusive_group(required=True)
    unit.add_argument("--plugin", help="Plugin release unit name")
    unit.add_argument("--marketplace", action="store_true", help="Check marketplace release unit")
    parser.add_argument("--version", required=True, help="SemVer version without v prefix")
    parser.add_argument(
        "--tag-state",
        choices=("absent", "present", "any"),
        default="absent",
        help="Expected git tag state. Defaults to absent for release preparation.",
    )
    parser.add_argument(
        "--skip-make-check",
        action="store_true",
        help="Skip running make check. Use only when an enclosing workflow already ran it.",
    )
    return parser.parse_args()


def git_tag_exists(tag: str) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def validate_tag(tag: str, tag_state: str, errors: list[str]) -> None:
    exists = git_tag_exists(tag)
    if tag_state == "absent" and exists:
        errors.append(f"tag {tag} already exists")
    elif tag_state == "present" and not exists:
        errors.append(f"tag {tag} does not exist")


def validate_changelog_entry(path: Path, version: str, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing changelog: {rel(path)}")
        return
    versions = changelog_versions(path.read_text(encoding="utf-8"))
    if version not in versions:
        errors.append(f"{rel(path)} must include a [{version}] release heading")


def validate_packaging_hygiene(errors: list[str]) -> None:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
    )
    if result.returncode != 0:
        errors.append("git ls-files failed during packaging hygiene check")
        return

    for raw_path in result.stdout.decode("utf-8").split("\0"):
        if not raw_path:
            continue
        path = REPO_ROOT / raw_path
        if path.name in FORBIDDEN_NAMES:
            errors.append(f"forbidden packaged file: {rel(path)}")
        if path.is_file() and any(path.name.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES):
            errors.append(f"forbidden generated artifact: {rel(path)}")
        if any(part in FORBIDDEN_DIRS for part in path.relative_to(REPO_ROOT).parts):
            errors.append(f"forbidden generated path: {rel(path)}")


def validate_plugin_safety(plugin_name: str, errors: list[str]) -> None:
    plugin_root = PLUGINS_DIR / plugin_name
    result = subprocess.run(
        ["git", "ls-files", "-z", f"plugins/{plugin_name}"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
    )
    if result.returncode != 0:
        errors.append(f"git ls-files failed during {plugin_name} safety check")
        return

    for raw_path in result.stdout.decode("utf-8").split("\0"):
        if not raw_path:
            continue
        path = REPO_ROOT / raw_path
        relative = path.relative_to(plugin_root)
        if path.is_symlink():
            errors.append(f"{plugin_name} contains symlink {relative}")
        if path.is_file() and path.stat().st_mode & 0o111:
            errors.append(f"{plugin_name} contains executable file {relative}")
        if any(part in {"hooks", "mcp", "mcp-servers"} for part in relative.parts):
            errors.append(f"{plugin_name} contains release-review-required surface {relative}")

    for manifest_name in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
        manifest = plugin_root / manifest_name
        text = manifest.read_text(encoding="utf-8")
        if "../" in text:
            errors.append(f"{rel(manifest)} must not reference paths outside the plugin")


def run_make_check(errors: list[str]) -> None:
    result = subprocess.run(["make", "check"], cwd=REPO_ROOT, check=False)
    if result.returncode != 0:
        errors.append("make check failed")


def validate_plugin_release(
    plugin_name: str, version: str, tag_state: str, errors: list[str]
) -> None:
    if plugin_name not in installable_plugins():
        errors.append(
            f"plugin {plugin_name} is not installable; release tags are only for AVAILABLE plugins"
        )
        return

    codex = plugin_manifest(plugin_name, "codex")
    claude = plugin_manifest(plugin_name, "claude")
    if codex.get("version") != version:
        errors.append(
            f"{plugin_name} Codex manifest version is {codex.get('version')}, not {version}"
        )
    if claude.get("version") != version:
        errors.append(
            f"{plugin_name} Claude manifest version is {claude.get('version')}, not {version}"
        )

    validate_changelog_entry(PLUGINS_DIR / plugin_name / "CHANGELOG.md", version, errors)
    validate_tag(tag_name_for_plugin(plugin_name, version), tag_state, errors)
    validate_plugin_safety(plugin_name, errors)


def validate_marketplace_release(version: str, tag_state: str, errors: list[str]) -> None:
    marketplace_version = claude_marketplace().get("version")
    if marketplace_version != version:
        errors.append(f"marketplace version is {marketplace_version}, not {version}")
    validate_changelog_entry(REPO_ROOT / "CHANGELOG.md", version, errors)
    validate_tag(tag_name_for_marketplace(version), tag_state, errors)


def main() -> int:
    args = parse_args()
    errors: list[str] = []

    if not is_semver(args.version):
        errors.append("VERSION must be SemVer without a leading v")
    else:
        if args.plugin:
            validate_plugin_release(args.plugin, args.version, args.tag_state, errors)
        else:
            validate_marketplace_release(args.version, args.tag_state, errors)

    validate_packaging_hygiene(errors)

    if not args.skip_make_check:
        run_make_check(errors)

    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1

    unit = args.plugin or "marketplace"
    print(f"PASS release readiness: {unit} v{args.version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
