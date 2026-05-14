# SIKK-GMGN 一键管道运行报告

- 运行时间：2026-05-10T17:35:46Z
- 模式：paper/readiness
- 执行边界：只做候选发现、K线吸筹识别、纸面信号、状态机，可选进入报价 + 安全扫描 + 确认层；不执行真实 swap。

## 阶段统计

- 新币筛选：{"总扫描数": 1, "进入候选池": 1, "排除数量": 0, "S3数量": 0, "S2数量": 0, "S1数量": 1, "S0数量": 0}
- K线吸筹管道：{"读取候选数": 0, "处理候选数": 0, "成功数量": 0, "失败数量": 0}
- 信号管道：{"读取候选数": 0, "成功数量": 0, "跳过数量": 0, "失败数量": 0}
- 状态机：{"DISCOVERED": 0, "WATCHING": 1, "ACCUMULATING": 0, "READY_TO_BUY": 0, "PAPER_READY": 0, "BLOCKED": 0, "FAILED": 0, "EXITED": 0, "候选数量": 1}
- 钱包结构门禁：{"处理数量": 0}
- 报价安全确认层：{"读取状态数": 1, "PAPER_READY数量": 0, "成功数量": 0, "跳过数量": 1, "失败数量": 0, "READY_FOR_CONFIRMATION": 0, "PAUSE": 0, "BLOCK": 0}

## 输出文件

- 候选池JSON：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/gmgn_new_token_filter/token_candidates.json
- 候选池CSV：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/gmgn_new_token_filter/token_candidates.csv
- 原始GMGN响应：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/gmgn_new_token_filter/gmgn_trenches_raw.json
- K线管道汇总：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/kline_pipeline/candidate_kline_pipeline_summary.json
- 信号汇总JSON：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/candidate_signal_outputs/candidate_signal_summary.json
- 信号汇总CSV：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/candidate_signal_outputs/candidate_signal_summary.csv
- 状态机JSON：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/state_machine/candidate_states.json
- 状态机CSV：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/state_machine/candidate_states.csv
- 状态事件JSONL：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/state_machine/state_events.jsonl
- 状态报告MD：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/state_machine/state_summary.md
- 钱包结构汇总JSON：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/wallet_structure/candidate_wallet_structure_summary.json
- 钱包结构汇总CSV：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/wallet_structure/candidate_wallet_structure_summary.csv
- 钱包结构报告MD：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/wallet_structure/candidate_wallet_structure_summary.md
- 报价安全汇总JSON：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/quote_security/candidate_quote_security_summary.json
- 报价安全汇总CSV：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/quote_security/candidate_quote_security_summary.csv
- 报价安全报告MD：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/quote_security/candidate_quote_security_summary.md
- 运行报告MD：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/orchestrator/pipeline_report.md
- 运行ManifestJSON：/root/sikk-gmgn/data/source_wallet_bot/live/6EQKNJD6KMTQv9KmhKDjs1jm1SRsNVGNqdKeEEiJpump/runtime_test/orchestrator/pipeline_manifest.json

## 下一步

- 若已启用报价 + 安全扫描 + 确认层，只能得到 READY_FOR_CONFIRMATION / PAUSE / BLOCK，不代表真实执行授权。
- 若状态机出现 PAPER_READY 但未启用确认层，可再运行 `--run-quote-security`。
- 若状态为 ACCUMULATING，继续刷新 K线与吸筹窗口。
- 若 BLOCKED / FAILED，进入风险复查或数据修复。
