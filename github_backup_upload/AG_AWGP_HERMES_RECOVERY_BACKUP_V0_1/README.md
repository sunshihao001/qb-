# AG-AWGP / Hermes Recovery Backup Upload Directory v0.1

本目录用于上传到 GitHub 代码仓库，作为独立的备份恢复目录。

## 目的

把当前 Hermes / GBrain / OpenASE / AG-AWGP 工作流恢复所需的非敏感文件集中存放，方便换 VPS / 换机器后恢复、调用、验证。

## 包含内容

- `recovery_pack/`：AG-AWGP / Hermes Portable Recovery Pack
- `snapshots/`：完整非敏感恢复快照、checksum、manifest
- `docs/RESTORE_RUNBOOK.md`：恢复说明书
- `docs/RECOVERY_ACCEPTANCE_CHECKLIST.md`：恢复验收清单
- `UPLOAD_MANIFEST.json`：上传清单
- `GITHUB_UPLOAD_GUIDE.md`：GitHub 上传与恢复说明

## 不包含内容

严禁上传：

- `.env` 真实值
- API token
- private key
- wallet secret
- signing material
- live trading credential
- cookies / browser sessions
- SSH keys

## 新机器恢复简要流程

```bash
git clone <your-private-github-repo-url> sikk-quant-runner
cd sikk-quant-runner

# 复制或引用本目录中的 recovery_pack
bash github_backup_upload/AG_AWGP_HERMES_RECOVERY_BACKUP_V0_1/recovery_pack/scripts/restore_snapshot.sh   github_backup_upload/AG_AWGP_HERMES_RECOVERY_BACKUP_V0_1/recovery_pack .

bash github_backup_upload/AG_AWGP_HERMES_RECOVERY_BACKUP_V0_1/recovery_pack/scripts/verify_restore.sh   . github_backup_upload/AG_AWGP_HERMES_RECOVERY_BACKUP_V0_1/recovery_pack

# 如需恢复完整非敏感项目状态
bash github_backup_upload/AG_AWGP_HERMES_RECOVERY_BACKUP_V0_1/recovery_pack/scripts/verify_full_snapshot.sh   github_backup_upload/AG_AWGP_HERMES_RECOVERY_BACKUP_V0_1/snapshots/<snapshot>.tar.zst

tar --zstd -xf github_backup_upload/AG_AWGP_HERMES_RECOVERY_BACKUP_V0_1/snapshots/<snapshot>.tar.zst -C .
```

## Secret 恢复

secrets 不在 GitHub 中恢复。请在目标机器上：

```bash
cp configs/templates/env.example .env
# 手动填入目标机器自己的真实 secret
```
