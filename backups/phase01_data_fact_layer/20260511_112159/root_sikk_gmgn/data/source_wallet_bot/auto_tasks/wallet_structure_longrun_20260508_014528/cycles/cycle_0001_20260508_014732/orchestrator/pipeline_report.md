# SIKK-GMGN 一键管道运行报告

- 运行时间：2026-05-08T01:47:32Z
- 模式：paper/readiness
- 执行边界：只做候选发现、K线吸筹识别、纸面信号、状态机，可选进入报价 + 安全扫描 + 确认层；不执行真实 swap。

## 阶段统计

- 新币筛选：{"总扫描数": 3, "进入候选池": 3, "排除数量": 0, "S3数量": 3, "S2数量": 0, "S1数量": 0, "S0数量": 0}
- K线吸筹管道：{"读取候选数": 3, "处理候选数": 3, "成功数量": 3, "失败数量": 0}
- 信号管道：{"读取候选数": 3, "成功数量": 3, "跳过数量": 0, "失败数量": 0}
- 状态机：{"DISCOVERED": 0, "WATCHING": 0, "ACCUMULATING": 0, "READY_TO_BUY": 0, "PAPER_READY": 3, "BLOCKED": 0, "FAILED": 0, "EXITED": 0, "候选数量": 3}
- 钱包结构门禁：{"处理数量": 3, "WALLET_BLOCK": 3}
- 报价安全确认层：{"状态": "skipped"}

## 输出文件

- 候选池JSON：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/gmgn_new_token_filter/token_candidates.json
- 候选池CSV：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/gmgn_new_token_filter/token_candidates.csv
- 原始GMGN响应：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/gmgn_new_token_filter/gmgn_trenches_raw.json
- K线管道汇总：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/kline_pipeline/candidate_kline_pipeline_summary.json
- 信号汇总JSON：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/candidate_signal_outputs/candidate_signal_summary.json
- 信号汇总CSV：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/candidate_signal_outputs/candidate_signal_summary.csv
- 状态机JSON：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/state_machine/candidate_states.json
- 状态机CSV：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/state_machine/candidate_states.csv
- 状态事件JSONL：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/state_machine/state_events.jsonl
- 状态报告MD：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/state_machine/state_summary.md
- 钱包结构汇总JSON：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/wallet_structure/candidate_wallet_structure_summary.json
- 钱包结构汇总CSV：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/wallet_structure/candidate_wallet_structure_summary.csv
- 钱包结构报告MD：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/wallet_structure/candidate_wallet_structure_summary.md
- 报价安全汇总JSON：未生成
- 报价安全汇总CSV：未生成
- 报价安全报告MD：未生成
- 运行报告MD：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/orchestrator/pipeline_report.md
- 运行ManifestJSON：data/source_wallet_bot/auto_tasks/wallet_structure_longrun_20260508_014528/cycles/cycle_0001_20260508_014732/orchestrator/pipeline_manifest.json

## 下一步

- 若已启用报价 + 安全扫描 + 确认层，只能得到 READY_FOR_CONFIRMATION / PAUSE / BLOCK，不代表真实执行授权。
- 若状态机出现 PAPER_READY 但未启用确认层，可再运行 `--run-quote-security`。
- 若状态为 ACCUMULATING，继续刷新 K线与吸筹窗口。
- 若 BLOCKED / FAILED，进入风险复查或数据修复。
