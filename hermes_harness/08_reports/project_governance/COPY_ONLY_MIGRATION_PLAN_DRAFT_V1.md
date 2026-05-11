# Copy-Only Migration Plan Draft V1

## Status
Draft only. Do not execute automatically.

## Principle
Legacy paths remain in place. Any future migration must be copy-only first, with manifests, checksums, and human approval.

## Required steps before copy

1. Confirm source path belongs to a known review group.
2. Confirm destination canonical path.
3. Generate source manifest.
4. Generate file checksums.
5. Confirm no secrets are copied into reports or public docs.
6. Copy to staging or canonical destination.
7. Verify file count and checksums.
8. Record `old_path -> new_path` in `legacy_compat/path_maps/`.
9. Keep old path in place.

## Forbidden

- no `mv`
- no delete
- no overwrite
- no secret exposure
- no migration of `.git`, cache, or unknown system directories

## Recommended first copy-only candidates

Start only with low semantic-risk documentation/navigation folders after manual review. Do not start with data outputs or domain analysis folders.
