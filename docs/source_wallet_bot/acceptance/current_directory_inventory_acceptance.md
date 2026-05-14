# Current Directory Inventory Acceptance

## 已扫描目录

- `/root/sikk-gmgn`
- `/root/sikk-gmgn/data/gmgn_candidates_live_run`
- `/root/sikk-gmgn/data/source_wallet_bot`
- `/root/sikk-gmgn/data/intel_bot`
- `/root/sikk-gmgn/data/gmgn_candidates_live_run_20260501T082334Z`
- `/root/sikk-gmgn/data/paper_live_20260501T082334Z`
- `/root/sikk-gmgn/data/6AVA_accumulation_test`
- `/root/sikk-gmgn/research_loop`
- `/root/sikk-gmgn/modules`
- `/root/sikk-gmgn/contracts`
- `/root/sikk-gmgn/docs`
- `/root/sikk-gmgn/outputs`
- `/root/sikk-gmgn/钱包数据分析`
- `/root/sikk-gmgn/结构分析`

## 已生成 registry / 路由

- `data/source_wallet_bot/registry/current_directory_inventory.json`
- `data/source_wallet_bot/registry/new_task_route_table.json`
- `docs/source_wallet_bot/directory_governance/current_directory_baseline.md`
- `docs/source_wallet_bot/directory_governance/write_routing_policy.md`
- `docs/source_wallet_bot/directory_governance/legacy_runtime_policy.md`

## 主目录裁决

- `/root/sikk-gmgn`：唯一工程主根目录
- `/root/sikk`：旧 5 Bot 骨架 / 待合并区
- `/root/sikk-gmgn/data/gmgn_candidates_live_run`：legacy_runtime_keep_in_place
- `/root/sikk-gmgn/data/source_wallet_bot`：active_wallet_intel_data_root
- `/root/sikk-gmgn/data/intel_bot`：experimental_or_future_merge_intel_area
- `/root/sikk-gmgn/research_loop`：active_research_loop_root
- `/root/sikk-gmgn/modules`：active_code_root
- `/root/sikk-gmgn/contracts`：active_contract_root
- `/root/sikk-gmgn/docs`：active_docs_root
- `/root/sikk-gmgn/outputs`：legacy_outputs_do_not_use_as_new_write_root
- `/root/sikk-gmgn/data/gmgn_candidates_live_run_20260501T082334Z`：legacy_backup_read_only
- `/root/sikk-gmgn/data/paper_live_20260501T082334Z`：legacy_paper_output_read_only
- `/root/sikk-gmgn/data/6AVA_accumulation_test`：historical_case_data
- `/root/sikk-gmgn/钱包数据分析`：legacy_wallet_material_inventory_required
- `/root/sikk-gmgn/结构分析`：legacy_structure_material_inventory_required

## 变更结论

- 未删除旧文件
- 未移动旧文件
- 未修改 runner.py
- 未修改状态机
- 未修改 paper runner
- 未新增交易代码
- 未读取私钥
- 未签名
- 未广播
- 未 swap
- 未把 `/root/sikk` 作为新写入路径
- 未把 `gmgn_candidates_live_run` 作为新主写路径
- 未把 `outputs` 作为新主写路径

## 下一轮建议

1. 用 inventory JSON 继续补全 `钱包数据分析/` 与 `结构分析/` 的历史文件分类。
2. 为 `data/source_wallet_bot/history/` 和 `imports/` 建立实际目录骨架。
3. 把 token 输出新任务全部收敛到 `data/source_wallet_bot/<mode>/<token_address>/`。
4. 继续把 `legacy_compat/` 变成旧路径索引中心。
5. 若需要 Intel 独立化，再由目录宪法单独批准。
