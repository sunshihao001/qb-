# SIKK_GITHUB_RECOVERY_BACKUP_V0_1_20260521T050802Z

Versioned upload-ready SIKK recovery backup. This directory is intentionally new for each update to preserve rollback/history.

## Restore command

```bash
mkdir -p /tmp/sikk_restore && cd /tmp/sikk_restore
bash /path/to/SIKK_GITHUB_RECOVERY_BACKUP_V0_1_20260521T050802Z/recovery_pack/scripts/restore_snapshot.sh /path/to/SIKK_GITHUB_RECOVERY_BACKUP_V0_1_20260521T050802Z/recovery_pack .
bash recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z/scripts/verify_restore.sh . recovery/SIKK_PORTABLE_RECOVERY_PACK_V0_1_20260521T050802Z
```

## GitHub upload pattern

Copy this whole directory into your existing GitHub backup repository as a new folder, then run secret scan and dry-run before push.

```bash
cd <your-existing-github-repo-local-clone>
cp -a /root/sikk-quant-runner/github_backup_upload/SIKK_GITHUB_RECOVERY_BACKUP_V0_1_20260521T050802Z ./
python SIKK_GITHUB_RECOVERY_BACKUP_V0_1_20260521T050802Z/recovery_pack/scripts/scan_for_secrets.py SIKK_GITHUB_RECOVERY_BACKUP_V0_1_20260521T050802Z
git add SIKK_GITHUB_RECOVERY_BACKUP_V0_1_20260521T050802Z
git commit -m "Add SIKK recovery backup V0_1_20260521T050802Z"
git push --dry-run
# Only after manual approval:
# git push
```
