# archive_then_remove_paths 执行记录

## 执行状态

已执行。

- 执行时间：2026-05-11T03:52:23Z
- 项目根目录：`/root/sikk-gmgn`
- GitHub 备份 commit：`fa0b8f9`
- GitHub 备份目录：`github_backups/sikk-gmgn-pre-cleanup-20260511T025449Z/`
- 本地归档根目录：`/root/sikk-archive/`
- 执行计划文件：`/root/sikk-gmgn/research_loop/plans/data_cleanup_20260511/archive_then_remove_paths.txt`
- 执行脚本：`/root/sikk-gmgn/research_loop/plans/data_cleanup_20260511/execute_archive_then_remove.sh`
- 执行日志：`/root/sikk-gmgn/github_backups/sikk-gmgn-pre-cleanup-20260511T025449Z/cleanup_execution/cleanup.log`

## 本次执行原则

本次没有直接删除核心资产。

执行方式是：

- 历史运行状态 / 历史报告 / 旧 run 输出：移动到 `/root/sikk-archive/`
- 缓存：移动到 `/root/sikk-archive/quarantine/`
- 强保留资产不移动、不删除

## 已归档目录

以下目录已从 `/root/sikk-gmgn/` 移动到 `/root/sikk-archive/`：

- `research_loop/state/wallet_data_semantic_classification_v2`
- `research_loop/state/wallet_data_copy_v7`
- `research_loop/state/wallet_data_token_index_v3`
- `research_loop/state/wallet_data_legacy_mapping_v6`
- `research_loop/state/wallet_data_recon_v1`
- `reports/review_ops_bot`
- `data/gmgn_candidates_live_run_20260501T082334Z`
- `data/paper_live_20260501T082334Z`
- `runtime_logs`
- `outputs`

## 已隔离缓存

以下缓存目录已移动到 `/root/sikk-archive/quarantine/`：

- `__pycache__`
- `.pytest_cache`

## 验证结果

执行后检查结果：

- 以上 12 个源路径在 `/root/sikk-gmgn/` 下均已不存在；
- `/root/sikk-archive/` 已存在归档内容；
- `/root/sikk-archive/` 当前大小约 `118M`；
- 未移动 `hermes_harness/`、`sikk_stable_trader_os/`、`docs/`、`modules/`、`contracts/`、`schemas/`、`tests/`、`skills/` 等强保留资产；
- 未移动当前兼容运行目录 `data/gmgn_candidates_live_run/`；
- 未移动 `legacy_compat/`，避免破坏 fallback/兼容读取。

## 恢复方法

如需恢复某个归档目录，例如：

```bash
mv /root/sikk-archive/runtime_logs /root/sikk-gmgn/runtime_logs
```

如需恢复全部本次归档目录，按 `cleanup.log` 中的 `ARCHIVED` / `QUARANTINED` 记录反向 `mv` 即可。

## 后续建议

下一步如果继续瘦身，应先做“抽样保留”而不是直接删除：

1. 从 `data/source_wallet_bot/` 选 1-3 个代表 token 作为 fixture；
2. 从 `data/gmgn_candidates_live_run/` 保留 index/tokens/kline/quote/security/paper/live 的小样本；
3. 将剩余可重拉历史数据归档；
4. 将长期规则 copy-only 提炼到 `docs/system_cleanup_constitution.md`；
5. 再提交新的 cleanup execution record 到 GitHub。
