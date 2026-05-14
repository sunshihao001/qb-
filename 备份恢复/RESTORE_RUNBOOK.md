# SIKK-GMGN 大型交易系统恢复手册

## 0. 恢复目标

从 GitHub 备份分支恢复一个可检查、可验证、可继续 paper-run 的系统副本。

恢复不是直接上线，也不是直接接实盘。恢复后的第一目标是：

```text
隔离目录 clone 成功 → commit 精确一致 → 安全边界检查 → 核心测试通过 → 生成恢复验收报告
```

## 1. 固定恢复点

- 仓库：`https://github.com/sunshihao001/qb-.git`
- 分支：`backup/full-system-20260514-215254`
- 基准 commit：`83edf22ff1e1c0c5769d8ff9c2e06a0d1ae6014c`

如果后面产生新的备份分支，必须同步更新 `BACKUP_RESTORE_MANIFEST.json`。

## 2. 禁止事项

恢复过程中禁止：

- 直接覆盖 `/root/sikk-gmgn`。
- 从备份恢复真实 `.env`。
- 复制、读取、提交私钥/助记词/API key/token 实值。
- 启动真实 swap、签名、broadcast。
- 把恢复演练产生的数据写回主系统目录。
- 因恢复失败而重新设计系统；失败只写 gap 和 blocker。

## 3. 推荐恢复目录

```bash
/root/restore-test/sikk-gmgn-20260514
```

如果目录已存在，默认不覆盖。需要重试时，换新目录，例如：

```bash
/root/restore-test/sikk-gmgn-20260514-r2
```

## 4. 一键恢复命令

在任意安全工作目录执行：

```bash
bash /root/sikk-gmgn/备份恢复/scripts/restore_from_backup.sh   --repo https://github.com/sunshihao001/qb-.git   --branch backup/full-system-20260514-215254   --commit 83edf22ff1e1c0c5769d8ff9c2e06a0d1ae6014c   --target /root/restore-test/sikk-gmgn-20260514
```

脚本会执行：

1. 检查目标目录是否安全。
2. `git clone` 到隔离目录。
3. checkout 指定分支和 commit。
4. 检查 `备份恢复/` 包是否存在。
5. 若存在依赖文件则尝试安装或提示。
6. 执行目录治理检查。
7. 执行安全 guard 测试。
8. 生成 `RESTORE_ACCEPTANCE_REPORT.md`。

## 5. 手工恢复流程

如果不使用脚本，手工流程如下：

```bash
mkdir -p /root/restore-test
git clone https://github.com/sunshihao001/qb-.git /root/restore-test/sikk-gmgn-20260514
cd /root/restore-test/sikk-gmgn-20260514
git checkout backup/full-system-20260514-215254
git checkout 83edf22ff1e1c0c5769d8ff9c2e06a0d1ae6014c
```

确认 commit：

```bash
git rev-parse HEAD
```

应输出：

```text
83edf22ff1e1c0c5769d8ff9c2e06a0d1ae6014c
```

## 6. 环境恢复

当前备份包没有强制依赖锁文件。恢复时按以下顺序处理：

1. 如果未来存在 `requirements.txt`：

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

2. 如果存在 `pyproject.toml`：

```bash
python3 -m pip install -e .
```

3. 如果都不存在：

```text
跳过自动依赖安装，只执行 Python 标准库可运行的检查；pytest 不存在时记录为环境 gap。
```

## 7. 配置与密钥恢复

只允许恢复配置模板，不允许恢复真实密钥。

允许：

- `.env.example`
- `config.example.yaml`
- `SECRETS_REQUIRED.md`

禁止：

- `.env`
- 私钥
- 助记词
- exchange signing secret
- Telegram bot token 实值
- webhook secret 实值

密钥恢复必须通过人工或专门 secret manager 注入，不能通过 Git 备份展开。

## 8. 最小验收命令

恢复后执行：

```bash
python3 tools/validate_directory_constitution.py
python3 tools/validate_system_directory_governance.py
python3 -m pytest   tests/test_wallet_data_guard.py   tests/test_wallet_data_guard_legacy_quarantine.py   tests/test_sikk_transaction_broadcast_guard.py
```

如果 pytest 不存在，先记录环境 gap；不要为了通过验收去修改交易代码。

## 9. 恢复成功判定

满足以下条件才算可展开恢复：

- 目标目录不是 `/root/sikk-gmgn`。
- Git commit 精确匹配。
- `备份恢复/` 目录完整。
- 目录治理检查通过，或输出明确 gap。
- 安全 guard 测试通过，特别是 private-key / broadcast 相关测试。
- 生成恢复报告：`RESTORE_ACCEPTANCE_REPORT.md`。

## 10. 后续接 paper-run 的条件

只有在最小验收通过后，才能接下一步：

```text
sample-token dry-run / paper-run
```

仍然禁止真实交易、签名和 broadcast。
