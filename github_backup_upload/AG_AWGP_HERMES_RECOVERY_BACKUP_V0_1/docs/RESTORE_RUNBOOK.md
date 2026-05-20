# RESTORE_RUNBOOK.md

## Purpose
Restore AG-AWGP / Hermes Portable Recovery Pack on a new VPS or clean checkout.

## Steps
1. `git clone <repo> sikk-quant-runner && cd sikk-quant-runner`
2. Confirm pack exists: `recovery/AG_AWGP_HERMES_PORTABLE_RECOVERY_PACK_V0_1`
3. Run restore: `bash recovery/AG_AWGP_HERMES_PORTABLE_RECOVERY_PACK_V0_1/scripts/restore_snapshot.sh recovery/AG_AWGP_HERMES_PORTABLE_RECOVERY_PACK_V0_1 .`
4. Run verify: `bash recovery/AG_AWGP_HERMES_PORTABLE_RECOVERY_PACK_V0_1/scripts/verify_restore.sh . recovery/AG_AWGP_HERMES_PORTABLE_RECOVERY_PACK_V0_1`
5. Load `docs/protocols/ag_awgp/AG_AWGP_TRIGGER_PROMPT.md` into GPT/Hermes to rehydrate protocol behavior.

## Boundaries
- No secrets from GitHub; use local secret manager and env.example only.
- GBrain is context retrieval only, not runtime truth.
- OpenASE is workflow routing only, not strategy judgment or runner approval.
- Hermes must use Operational Brief + Intake Gate.
- No live trading / swap / private key / signing / broadcast.
