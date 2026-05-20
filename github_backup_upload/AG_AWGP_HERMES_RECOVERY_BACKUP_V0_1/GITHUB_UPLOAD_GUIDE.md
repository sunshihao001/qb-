# GITHUB_UPLOAD_GUIDE.md

## 上传目标

把整个目录上传到私有 GitHub 仓库：

```text
github_backup_upload/AG_AWGP_HERMES_RECOVERY_BACKUP_V0_1/
```

## 推荐提交范围

```bash
git add .gitignore github_backup_upload/AG_AWGP_HERMES_RECOVERY_BACKUP_V0_1 docs/recovery scripts/recovery configs/templates recovery/AG_AWGP_HERMES_PORTABLE_RECOVERY_PACK_V0_1
```

如果你只想上传独立备份目录，则执行：

```bash
git add github_backup_upload/AG_AWGP_HERMES_RECOVERY_BACKUP_V0_1 .gitignore
```

## 提交

```bash
git commit -m "Add AG-AWGP Hermes portable recovery backup pack v0.1"
git push origin main
```

## 上传前必须检查

```bash
bash github_backup_upload/AG_AWGP_HERMES_RECOVERY_BACKUP_V0_1/recovery_pack/scripts/verify_restore.sh   . github_backup_upload/AG_AWGP_HERMES_RECOVERY_BACKUP_V0_1/recovery_pack
```

## 禁止上传

- `.env`
- private key
- API token
- wallet secret
- signing material
- live trading credential

## 恢复测试

clone 后执行 `README.md` 中的新机器恢复流程。通过 `VERIFY_RESTORE: PASS` 才算恢复可用。
