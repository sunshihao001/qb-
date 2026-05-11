# Legacy Keep-In-Place Policy V1

## Purpose

Legacy paths remain readable and traceable, but are not automatically moved, renamed, or deleted.

## Hard rules

- Do not delete legacy files.
- Do not move legacy directories.
- Do not rename core files.
- Do not make legacy runtime directories the new main write path.
- Use copy-only mapping if future standardization is approved.
- Record `old_path -> new_path` before any copy.
- Unknown paths require human review.

## Current legacy candidates

Detected legacy/reference candidates: `164`.

## Allowed handling

- `retain_only`
- `read_fallback`
- `copy_only_after_review`
- `manifest_only`

## Forbidden handling

- `delete`
- `move_without_manifest`
- `overwrite_runtime_output`
- `classify_unknown_as_disposable`
