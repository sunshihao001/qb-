# Canonical Path Standard V1

## Purpose

This standard defines where future Hermes/SIKK outputs should be read from and written to. It does not move old files.

## Core rule

Every new artifact must answer four questions before write:

1. Bot / domain?
2. Asset class?
3. Asset ID?
4. Canonical write path?

## Canonical roots

- `hermes_harness/` — Hermes control plane, runtime state, verification, recovery, audit, workflow modules.
- `docs/` — stable system documentation and directory constitution.
- `modules/` — functional code modules.
- `tests/` — tests only.
- `data/` — runtime data and standardized outputs.
- `reports/` — human-readable report index.
- `research_loop/` — methodology, plans, checkpoints, task packages, research artifacts.
- `imports/` — external/staging imports.
- `schemas/` — shared schemas.
- `contracts/` — shared and bot-handoff contracts.
- `tools/` — project-level utility tools.
- `legacy_compat/` — compatibility manifests, path maps, and read fallbacks.

## Write rules

- Code goes to `modules/<bot_or_domain>/`.
- Tests go to `tests/`.
- Runtime data goes to `data/<bot>/<mode>/<asset_id>/`.
- Human reports go to `reports/<bot>/<mode>/<asset_id>/` unless the report is Hermes control-plane evidence, then it stays under `hermes_harness/08_reports/`.
- Methodology and long-task plans go to `research_loop/`.
- Legacy path maps go to `legacy_compat/path_maps/`.

## Non-rules

- This standard does not delete old files.
- This standard does not move old directories.
- This standard does not classify unknown roots as removable.
