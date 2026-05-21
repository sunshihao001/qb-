# RESTORE_RUNBOOK

## Clean-room restore

```bash
RESTORE_ROOT=/tmp/sikk_restore_20260521T050802Z
mkdir -p "$RESTORE_ROOT"
bash recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/scripts/restore_snapshot.sh recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z "$RESTORE_ROOT"
bash "$RESTORE_ROOT/recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/scripts/verify_restore.sh" "$RESTORE_ROOT" "$RESTORE_ROOT/recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z"
```

## GitHub clone restore pattern

```bash
git clone <your-existing-repo-url> sikk-quant-runner
cd sikk-quant-runner
bash recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/scripts/restore_snapshot.sh recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z .
bash recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/scripts/verify_restore.sh . recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z
```

## Versioned update rule

Every update creates a new directory:

```text
recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_<UTCSTAMP>/
github_backup_upload/SIKK_GITHUB_RECOVERY_BACKUP_V0_1_<UTCSTAMP>/
```

Do not overwrite old recovery directories. This preserves rollback and historical review.
