# Changelog

All notable changes to this release unit are documented in this file.

The format is based on Keep a Changelog, and this release unit follows Semantic
Versioning.

## [Unreleased][unreleased]

### Added

- Added note-only, audio-only, video-only, and multimodal zero-shot rubric generation
  skills for Wayfinder/OASIS rubric upload workflows.

### Changed

### Deprecated

### Removed

### Fixed

- Renamed zero-shot vendored mapping docs from the platform-spec name
  (`MAPLES Rubric Specification.md`) to `rubric-maker-yaml-to-maples-mapping.md` so
  agents load the toolkit YAML→MAPLES adapter, not a false canonical workbook contract
  (issue #13).

### Security

## [0.1.0][rubric-maker-skill-v0.1.0] - 2026-05-24

### Added

- Added the initial Rubric Maker plugin for Codex CLI and Claude Code.
- Added skills for post-encounter-note rubric drafting, rubric import, OSCE rubric
  review, rubric transformation, synthetic student artifact generation, grading
  dry-runs, dry-run evaluation, and content validation.
- Added bundled rubric schema references and grade-sheet contract references.
- Added plugin-local validators and smoke checks for rubric schema, grade-sheet
  contract, validator sync, and sample workflows.
- Added plugin-local Python runtime requirements.

### Changed

- Nothing.

### Deprecated

- Nothing.

### Removed

- Nothing.

### Fixed

- Nothing.

### Security

- Added plugin packaging hygiene checks for generated archives, OS metadata, caches,
  local environments, logs, and generated outputs.

[unreleased]: https://github.com/JamiesonLabUTSW/maples-toolkit/compare/rubric-maker-skill/v0.1.0...HEAD
[rubric-maker-skill-v0.1.0]: https://github.com/JamiesonLabUTSW/maples-toolkit/releases/tag/rubric-maker-skill/v0.1.0
