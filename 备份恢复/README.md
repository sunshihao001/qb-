# 备份恢复

本目录是大型交易系统备份分支里的“可展开恢复包”。它不是新的业务系统，也不是新的交易模块，只负责回答三个问题：

1. 这个备份从哪里来？
2. 按什么步骤恢复到隔离目录？
3. 恢复后如何判断“能跑、没泄密、没越权、没污染主系统”？

当前备份点：

- 仓库：https://github.com/sunshihao001/qb-
- 分支：`backup/full-system-20260514-215254`
- 基准 commit：`83edf22ff1e1c0c5769d8ff9c2e06a0d1ae6014c`
- 本目录用途：给后续恢复、迁移、灾备演练提供固定入口。

## 文件索引

- `BACKUP_RESTORE_MANIFEST.json`：备份恢复清单，记录来源、范围、排除项、安全边界、验证命令。
- `RESTORE_RUNBOOK.md`：人工可读恢复手册。
- `RECOVERY_TEST_MATRIX.md`：恢复验收矩阵。
- `SECRETS_REQUIRED.md`：密钥/环境变量恢复规则，只写占位，不保存真实值。
- `RESTORE_ACCEPTANCE_TEMPLATE.md`：恢复演练报告模板。
- `scripts/restore_from_backup.sh`：从 GitHub 分支恢复到隔离目录并执行最小验收。
- `scripts/check_restore_readiness.sh`：在当前仓库静态检查恢复包是否完整。
- `scripts/create_backup_snapshot.sh`：后续创建新备份分支的最小脚本模板。
- `scripts/run_restore_smoke_test.sh`：从当前备份分支执行一次真实 clone/checkout/验收演练，并把结果写入 `备份恢复/results/latest_restore_result.md`。

## 依赖恢复入口

本分支现在包含根目录 `requirements.txt`，用于 fresh checkout 后安装最小恢复/验收依赖：

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## 最短恢复命令

```bash
bash 备份恢复/scripts/restore_from_backup.sh   --repo https://github.com/sunshihao001/qb-.git   --branch backup/full-system-20260514-215254   --commit 83edf22ff1e1c0c5769d8ff9c2e06a0d1ae6014c   --target /root/restore-test/sikk-gmgn-20260514
```

恢复原则：

- 只恢复到隔离目录，不直接覆盖 `/root/sikk-gmgn`。
- 不恢复真实 `.env`、私钥、助记词、交易签名材料。
- 恢复后先跑目录检查和安全 guard，再考虑 paper-run。
- 恢复成功的标准不是“clone 完成”，而是最小验收命令通过，并生成恢复验收报告。
