# GitHub Upload Guide

Use your existing previous backup repository. Create a new directory for every update.

```bash
cd <your-existing-github-repo-local-clone>
cp -a /root/sikk-quant-runner/github_backup_upload/SIKK_GITHUB_RECOVERY_BACKUP_V0_1_20260521T050802Z ./
python SIKK_GITHUB_RECOVERY_BACKUP_V0_1_20260521T050802Z/recovery_pack/scripts/scan_for_secrets.py SIKK_GITHUB_RECOVERY_BACKUP_V0_1_20260521T050802Z
git add SIKK_GITHUB_RECOVERY_BACKUP_V0_1_20260521T050802Z
git status
git commit -m "Add SIKK recovery backup V0_1_20260521T050802Z"
git push --dry-run
```

Do not run real `git push` until explicitly approved.
