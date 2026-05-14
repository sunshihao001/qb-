# Source Wallet Bot 目录现状基线

- 唯一工程主根目录：`/root/sikk-gmgn`
- 旧 5 Bot 骨架目录：`/root/sikk`，仅作旧骨架/待合并区，不作为新任务默认写入根目录。
- 当前阶段：只做目录治理、注册、分类、路由和后续迁移计划。

## 目录裁决总览
- `/root/sikk-gmgn` → `active_root`；类别：`active_root`；说明：唯一工程主根目录。
- `/root/sikk-gmgn/data/gmgn_candidates_live_run` → `legacy_runtime_keep_in_place`；类别：`legacy_runtime_keep_in_place`；说明：历史运行主区，保留不动。
- `/root/sikk-gmgn/data/source_wallet_bot` → `active_data_root`；类别：`active_data_root`；说明：Source 钱包事实主数据区。
- `/root/sikk-gmgn/data/intel_bot` → `experimental_or_future_merge`；类别：`experimental_or_future_merge`；说明：Intel 未来/实验区，当前不作为主写路径。
- `/root/sikk-gmgn/data/gmgn_candidates_live_run_20260501T082334Z` → `legacy_backup_read_only`；类别：`legacy_backup_read_only`；说明：旧运行备份，只读。
- `/root/sikk-gmgn/data/paper_live_20260501T082334Z` → `legacy_backup_read_only`；类别：`legacy_backup_read_only`；说明：旧 paper 备份，只读。
- `/root/sikk-gmgn/data/6AVA_accumulation_test` → `historical_case_data`；类别：`historical_case_data`；说明：历史测试案例数据。
- `/root/sikk-gmgn/research_loop` → `active_research_root`；类别：`active_research_root`；说明：方法轮 / 长任务目录。
- `/root/sikk-gmgn/modules` → `active_code_root`；类别：`active_code_root`；说明：正式代码目录。
- `/root/sikk-gmgn/contracts` → `active_contract_root`；类别：`active_contract_root`；说明：合约目录。
- `/root/sikk-gmgn/docs` → `active_docs_root`；类别：`active_docs_root`；说明：文档目录。
- `/root/sikk-gmgn/outputs` → `legacy_output_do_not_use`；类别：`legacy_output_do_not_use`；说明：旧输出目录，不作为新写路径。
- `/root/sikk-gmgn/钱包数据分析` → `inventory_required`；类别：`inventory_required`；说明：旧钱包资料区，需要整理清单。
- `/root/sikk-gmgn/结构分析` → `inventory_required`；类别：`inventory_required`；说明：旧结构资料区，需要整理清单。

## active / legacy / read_only / future_merge / 禁止新写入
- active：`/root/sikk-gmgn`、`/root/sikk-gmgn/data/source_wallet_bot`、`/root/sikk-gmgn/research_loop`、`/root/sikk-gmgn/modules`、`/root/sikk-gmgn/contracts`、`/root/sikk-gmgn/docs`。
- legacy：`/root/sikk-gmgn/data/gmgn_candidates_live_run`、`/root/sikk-gmgn/data/gmgn_candidates_live_run_20260501T082334Z`、`/root/sikk-gmgn/data/paper_live_20260501T082334Z`、`/root/sikk-gmgn/outputs`。
- read_only：旧备份区、历史案例区、旧资料区。
- future_merge：`/root/sikk-gmgn/data/intel_bot`。
- 禁止作为新写入路径：`/root/sikk`、`/root/sikk-gmgn/data/gmgn_candidates_live_run`、`/root/sikk-gmgn/outputs`。

## 当前基线说明
- 本轮不删除旧文件。
- 本轮不移动旧文件。
- 本轮不改交易系统、状态机或 paper runner。
- 本轮只建立目录事实表、写入路由、legacy policy 与 acceptance。
