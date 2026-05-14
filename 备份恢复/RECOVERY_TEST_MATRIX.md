# 恢复验收矩阵

## A. 来源一致性

- 检查项：repo 可 clone
- 命令：`git clone <repo> <target>`
- 通过标准：目标目录生成 `.git/`
- 失败处理：记录网络/权限 blocker

- 检查项：分支存在
- 命令：`git ls-remote --heads origin backup/full-system-20260514-215254`
- 通过标准：返回目标分支 hash
- 失败处理：确认远端仓库和分支名

- 检查项：commit 精确匹配
- 命令：`git rev-parse HEAD`
- 通过标准：输出 `83edf22ff1e1c0c5769d8ff9c2e06a0d1ae6014c`
- 失败处理：不要继续恢复，先固定正确 commit

## B. 恢复包完整性

- 检查项：恢复目录存在
- 命令：`test -d 备份恢复`
- 通过标准：目录存在

- 检查项：恢复清单存在
- 命令：`test -f 备份恢复/BACKUP_RESTORE_MANIFEST.json`
- 通过标准：文件存在且 JSON 可解析

- 检查项：恢复脚本存在
- 命令：`test -x 备份恢复/scripts/restore_from_backup.sh`
- 通过标准：脚本可执行

- 检查项：验收模板存在
- 命令：`test -f 备份恢复/RESTORE_ACCEPTANCE_TEMPLATE.md`
- 通过标准：文件存在

## C. 目录治理

- 检查项：目录宪法校验
- 命令：`python3 tools/validate_directory_constitution.py`
- 通过标准：exit code 0
- 失败处理：写入恢复报告 known_gaps，不直接修改主系统

- 检查项：系统目录治理校验
- 命令：`python3 tools/validate_system_directory_governance.py`
- 通过标准：exit code 0
- 失败处理：写入恢复报告 known_gaps

## D. 安全边界

- 检查项：钱包数据 guard
- 命令：`python3 -m pytest tests/test_wallet_data_guard.py`
- 通过标准：测试通过

- 检查项：legacy quarantine guard
- 命令：`python3 -m pytest tests/test_wallet_data_guard_legacy_quarantine.py`
- 通过标准：测试通过

- 检查项：交易广播 guard
- 命令：`python3 -m pytest tests/test_sikk_transaction_broadcast_guard.py`
- 通过标准：测试通过，确认不会真实 broadcast

## E. 环境完整性

- 检查项：Python 可用
- 命令：`python3 --version`
- 通过标准：返回版本

- 检查项：pytest 可用
- 命令：`python3 -m pytest --version`
- 通过标准：返回版本
- 失败处理：环境 gap，不代表代码备份失败

- 检查项：依赖入口存在
- 命令：`test -f requirements.txt || test -f pyproject.toml`
- 当前状态：已补 `requirements.txt`
- 通过标准：fresh checkout 后可执行 `pip install -r requirements.txt`
- 处理建议：如果后续引入更多外部库，同步更新 `requirements.txt`

## F. 可展开恢复结论

满足 A+B+D，且 C 至少能给出明确结果，即可认为：

```text
代码/规则/恢复入口可展开；环境依赖和外部数据按 gap 处理。
```

满足 A+B+C+D+E 后，才可认为：

```text
可在新机器上完整展开并进入 paper-run 验证。
```
