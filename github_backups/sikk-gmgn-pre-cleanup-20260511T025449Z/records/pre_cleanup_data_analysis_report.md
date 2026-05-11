# SIKK-GMGN Pre-Cleanup Data Analysis Backup Plan

- generated_at: 2026-05-11T02:31:56Z
- root: `/root/sikk-gmgn`
- principle: 先备份，后隔离，再清洗；当前不直接删除。

## A. 必须保留，不建议清洗

这些是系统能力/代码/合约/测试/新 HER 注册层，不能当无用目录删：

- `/root/sikk-gmgn/sikk_stable_trader_os` — 98.3K, files=109
- `/root/sikk-gmgn/hermes_harness` — 12.3M, files=1024
- `/root/sikk-gmgn/modules` — 2.1M, files=293
- `/root/sikk-gmgn/tests` — 3.3M, files=359
- `/root/sikk-gmgn/docs` — 1.3M, files=256
- `/root/sikk-gmgn/schemas` — 151.2K, files=80
- `/root/sikk-gmgn/contracts` — 80.0K, files=81
- `/root/sikk-gmgn/configs` — 23.8K, files=23
- `/root/sikk-gmgn/scripts` — 66.9K, files=15
- `/root/sikk-gmgn/tools` — 134.3K, files=14
- `/root/sikk-gmgn/skills` — 81.8K, files=63
- `/root/sikk-gmgn/knowledge` — 2.7M, files=56
- `/root/sikk-gmgn/shared_handoff` — 141.9K, files=74
- `/root/sikk-gmgn/task_books` — 183.7K, files=60
- `/root/sikk-gmgn/audits` — 237.2K, files=25
- `/root/sikk-gmgn/AGENTS.md` — 2968B, files=1

## B. 数据分析有用，建议先备份

这些包含钱包结构分析、Source Wallet Bot、token/kline/security/paper 数据、legacy 映射与方法论，是后续系统复盘/迁移/fallback 需要的：

- `/root/sikk-gmgn/data/source_wallet_bot` — 30.6M, files=2293
- `/root/sikk-gmgn/data/stable_trader_os` — 7.6M, files=226
- `/root/sikk-gmgn/data/shared_handoff` — 6.0K, files=1
- `/root/sikk-gmgn/data/runtime` — 462.4K, files=245
- `/root/sikk-gmgn/data/gmgn_candidates_live_run/index` — 2.4M, files=9
- `/root/sikk-gmgn/data/gmgn_candidates_live_run/tokens` — 2.2M, files=594
- `/root/sikk-gmgn/data/gmgn_candidates_live_run/kline_pipeline` — 6.6M, files=603
- `/root/sikk-gmgn/data/gmgn_candidates_live_run/quote_security` — 490.3K, files=193
- `/root/sikk-gmgn/data/gmgn_candidates_live_run/time_context` — 3.8M, files=8
- `/root/sikk-gmgn/data/gmgn_candidates_live_run/candidate_signal_outputs` — 472.0K, files=518
- `/root/sikk-gmgn/data/gmgn_candidates_live_run/paper_live` — 5.6M, files=462
- `/root/sikk-gmgn/data/gmgn_candidates_live_run/site` — 8.4M, files=623
- `/root/sikk-gmgn/data/sikk_sol_full_auto_workflow` — 1.2M, files=144
- `/root/sikk-gmgn/data/sikk_sol_gmgn_okx_full_auto_run_20260507` — 85.7K, files=12
- `/root/sikk-gmgn/data/sikk_sol_gmgn_okx_full_auto_run_20260507_161504` — 85.8K, files=12
- `/root/sikk-gmgn/data/sikk_sol_full_auto_workflow_run_20260507_oneshot` — 60.7K, files=10
- `/root/sikk-gmgn/data/6AVA_accumulation_test` — 1.5M, files=39
- `/root/sikk-gmgn/research_loop/methodology` — 95.8K, files=38
- `/root/sikk-gmgn/research_loop/mappings` — 85.6K, files=12
- `/root/sikk-gmgn/research_loop/phase_00_system_constitution` — 83.2K, files=17
- `/root/sikk-gmgn/research_loop/phase_01_data_fact` — 25.0K, files=16
- `/root/sikk-gmgn/research_loop/phase_01_data_fact_layer` — 83.5K, files=17
- `/root/sikk-gmgn/research_loop/phase_02_wallet_structure_layer` — 91.6K, files=22
- `/root/sikk-gmgn/research_loop/total_control` — 9.3K, files=11
- `/root/sikk-gmgn/research_loop/acceptance` — 11.0K, files=5
- `/root/sikk-gmgn/research_loop/corpus` — 13.6K, files=18
- `/root/sikk-gmgn/reports/system_audit` — 168.9K, files=66
- `/root/sikk-gmgn/reports/source_wallet_bot` — 24.7K, files=3
- `/root/sikk-gmgn/reports/intel_bot` — 175.0B, files=1
- `/root/sikk-gmgn/reports/runtime` — 103.7K, files=82
- `/root/sikk-gmgn/legacy_compat` — 11.9M, files=25
- `/root/sikk-gmgn/imports/staging` — 675.7K, files=94
- `/root/sikk-gmgn/钱包数据分析` — 7.6M, files=30
- `/root/sikk-gmgn/结构分析` — 3.5M, files=18

## C. 可归档后清洗/压缩

这些多为旧 runs、长任务 state、大体量 review/audit 或旧快照。建议打包后从工作区移走，不建议直接删：

- `/root/sikk-gmgn/research_loop/state/wallet_data_semantic_classification_v2` — 58.2M, files=13
- `/root/sikk-gmgn/research_loop/state/wallet_data_copy_v7` — 8.0M, files=3
- `/root/sikk-gmgn/research_loop/state/wallet_data_token_index_v3` — 7.2M, files=218
- `/root/sikk-gmgn/research_loop/state/wallet_data_legacy_mapping_v6` — 6.3M, files=4
- `/root/sikk-gmgn/research_loop/state/wallet_data_recon_v1` — 3.5M, files=4
- `/root/sikk-gmgn/research_loop/state/wallet_data_passports_v4` — 71.8K, files=2
- `/root/sikk-gmgn/reports/review_ops_bot` — 26.2M, files=32
- `/root/sikk-gmgn/data/gmgn_candidates_live_run_20260501T082334Z` — 1.7M, files=204
- `/root/sikk-gmgn/data/paper_live_20260501T082334Z` — 1.0K, files=7
- `/root/sikk-gmgn/runtime_logs` — 488.7K, files=425
- `/root/sikk-gmgn/outputs` — 191.4K, files=55

## D. 备份后基本可清理缓存

- `/root/sikk-gmgn/__pycache__` — 1.7M, files=88
- `/root/sikk-gmgn/.pytest_cache` — 62.2K, files=5

## E. 一键备份命令

```bash
bash /root/sikk-gmgn/research_loop/plans/data_cleanup_20260511/backup_before_cleanup.sh
```

## F. 备份后安全隔离缓存命令，不直接删除

```bash
bash /root/sikk-gmgn/research_loop/plans/data_cleanup_20260511/move_safe_cache_to_quarantine.sh
```

## G. 清洗策略建议

1. 先运行备份脚本。
2. 确认 `/root/sikk-backups/sikk-gmgn-pre-clean-*/SHA256SUMS.txt` 存在。
3. 只把 D 类缓存移动到 quarantine。
4. C 类旧 runs 先不要删，下一步生成 `archive_then_remove_paths.txt` 后再按批次移动到 `/root/sikk-archive/`。
5. 保留 B 类 canonical/legacy 有用分析资产，等 P01/P02 runner 读新目录稳定后，再冻结旧路径写入。
