# Evidence Rules

Dry-run grading can only use text evidence supplied in the current task.

## Supported Artifacts

- `note`: written post-encounter-note text.
- `transcript`: spoken encounter text that has already been transcribed.
- `observation_log`: timestamped observations written by a human or another extraction step.

## Evidence Requirements

- If a rubric item includes `mode`, score it only from compatible text evidence:
  - `note` requires a `note` artifact.
  - `audio` can be supported by `transcript` text.
  - `video` can be supported by `observation_log` text or transcript text that explicitly documents observations.
- Quote exact note or transcript words for scored rows.
- For observation logs, cite the supplied timestamp or timestamp range and the observed behavior.
- Evidence must support the selected score anchor, not just the general topic.
- If evidence is absent, contradictory, or outside the artifact type, mark the row unscorable or assign the lowest anchor only when the rubric explicitly scores absence.
- Do not infer visual actions from a transcript unless the transcript explicitly documents them.
- Do not infer spoken counseling from a note unless the note explicitly documents it.
- Unsupported item modes, or modes incompatible with the supplied artifact, must be marked unscorable instead of scored.

## Unsupported Evidence

- Do not inspect raw audio or video.
- Do not rely on unstated case facts to award points.
- Do not reward facts that contradict the supplied case context.
- Do not convert missing evidence into a score when the rubric requires a modality that was not supplied.
