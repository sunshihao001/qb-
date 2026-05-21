# SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z

SIKK Portable Recovery & State Snapshot Pack.

This pack restores SIKK control-plane state, clean rehydration protocol, current pointer, contracts, tests, scripts, and non-secret run evidence.

## One-command restore into an empty project directory

```bash
mkdir -p /tmp/sikk_restore && cd /tmp/sikk_restore
bash /path/to/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/scripts/restore_snapshot.sh /path/to/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z .
bash recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/scripts/verify_restore.sh . recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z
```

## Restore inside a cloned repo

```bash
cd /path/to/sikk-quant-runner
bash recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/scripts/restore_snapshot.sh recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z .
bash recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/scripts/verify_restore.sh . recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z
```

## Clean start after restore

```bash
cat data/operating_backbone/canonical/current/CURRENT_STATE_POINTER.json
# Then enter SIKK Clean Start Mode: validate pointer, apply READ_ALLOWLIST_POLICY, run CONTAMINATION_CHECKLIST, produce Operational Brief.
```

## Boundary

This pack does not authorize GMGN calls, feature generation, structure signals, decision tickets, paper validation, or live/swap/signing/broadcast.
