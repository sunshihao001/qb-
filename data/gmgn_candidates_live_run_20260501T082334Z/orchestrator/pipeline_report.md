# SIKK-GMGN 一键管道运行报告

- 运行时间：2026-05-01T08:23:42Z
- 模式：paper/readiness
- 执行边界：只做候选发现、K线吸筹识别、纸面信号、状态机，可选进入报价 + 安全扫描 + 确认层；不执行真实 swap。

## 阶段统计

- 新币筛选：{"总扫描数": 50, "进入候选池": 49, "排除数量": 1, "S3数量": 13, "S2数量": 1, "S1数量": 35, "S0数量": 1}
- K线吸筹管道：{"读取候选数": 13, "处理候选数": 13, "成功数量": 13, "失败数量": 0}
- 信号管道：{"读取候选数": 13, "成功数量": 13, "跳过数量": 0, "失败数量": 0}
- 状态机：{"DISCOVERED": 0, "WATCHING": 37, "ACCUMULATING": 0, "READY_TO_BUY": 0, "PAPER_READY": 4, "BLOCKED": 8, "FAILED": 0, "EXITED": 0, "候选数量": 49}
- 报价安全确认层：{"读取状态数": 49, "PAPER_READY数量": 4, "成功数量": 4, "跳过数量": 45, "失败数量": 0, "READY_FOR_CONFIRMATION": 0, "PAUSE": 4, "BLOCK": 0}

## 输出文件

- 候选池JSON：data/gmgn_candidates_live_run_20260501T082334Z/gmgn_new_token_filter/token_candidates.json
- 候选池CSV：data/gmgn_candidates_live_run_20260501T082334Z/gmgn_new_token_filter/token_candidates.csv
- 原始GMGN响应：data/gmgn_candidates_live_run_20260501T082334Z/gmgn_new_token_filter/gmgn_trenches_raw.json
- K线管道汇总：data/gmgn_candidates_live_run_20260501T082334Z/kline_pipeline/candidate_kline_pipeline_summary.json
- 信号汇总JSON：data/gmgn_candidates_live_run_20260501T082334Z/candidate_signal_outputs/candidate_signal_summary.json
- 信号汇总CSV：data/gmgn_candidates_live_run_20260501T082334Z/candidate_signal_outputs/candidate_signal_summary.csv
- 状态机JSON：data/gmgn_candidates_live_run_20260501T082334Z/state_machine/candidate_states.json
- 状态机CSV：data/gmgn_candidates_live_run_20260501T082334Z/state_machine/candidate_states.csv
- 状态事件JSONL：data/gmgn_candidates_live_run_20260501T082334Z/state_machine/state_events.jsonl
- 状态报告MD：data/gmgn_candidates_live_run_20260501T082334Z/state_machine/state_summary.md
- 报价安全汇总JSON：data/gmgn_candidates_live_run_20260501T082334Z/quote_security/candidate_quote_security_summary.json
- 报价安全汇总CSV：data/gmgn_candidates_live_run_20260501T082334Z/quote_security/candidate_quote_security_summary.csv
- 报价安全报告MD：data/gmgn_candidates_live_run_20260501T082334Z/quote_security/candidate_quote_security_summary.md
- 运行报告MD：data/gmgn_candidates_live_run_20260501T082334Z/orchestrator/pipeline_report.md
- 运行ManifestJSON：data/gmgn_candidates_live_run_20260501T082334Z/orchestrator/pipeline_manifest.json

## 下一步

- 若已启用报价 + 安全扫描 + 确认层，只能得到 READY_FOR_CONFIRMATION / PAUSE / BLOCK，不代表真实执行授权。
- 若状态机出现 PAPER_READY 但未启用确认层，可再运行 `--run-quote-security`。
- 若状态为 ACCUMULATING，继续刷新 K线与吸筹窗口。
- 若 BLOCKED / FAILED，进入风险复查或数据修复。
