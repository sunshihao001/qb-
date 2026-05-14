# Directory Constitution

## Primary roots

- `skills/sikk_stable_trader_os/`: thin HER total-control skill.
- `docs/`: total-control governance and human-readable protocol.
- `contracts/stable_trader_os/`: machine-readable control contracts.
- `schemas/stable_trader_os/`: machine-readable schemas.
- `sikk_stable_trader_os/02_phase_controllers/`: Phase00-09 packages.
- `research_loop/total_control/`: control notes, route state, task manifests.
- `reports/system_audit/`: audit reports and validation evidence.

## Forbidden write patterns

No root-level scattered runtime JSON/CSV/MD. No deletion/move migrations without copy-only map. No private-key/sign/broadcast/swap artifacts.
